"""
ModernizeIQ — 3-agent pipeline (Phase 2: RAG-grounded decision).

Pipeline:  Assessment Agent  ->  6R Decision Agent (grounded in retrieved patterns)  ->  Explanation Agent

The decision agent no longer decides from the model's own memory. Before it runs, we
retrieve the most relevant modernization patterns from the knowledge base (ChromaDB)
and inject them into its prompt. Every decision is grounded in known practice, and we
record which patterns were retrieved so the recommendation is traceable.

Run:
    uv run src/ingest_kb.py     # once, to build the knowledge base
    uv run src/crew.py          # run the pipeline
"""

import os
import re
import sys
import json
from pydantic import BaseModel, Field, ValidationError
from crewai import Agent, Task, Crew, Process, LLM

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LLM_BASE_URL, LLM_MODEL, LLM_API_KEY, DATA_PATH  # noqa: E402
from rag import retrieve_patterns  # noqa: E402

# -----------------------------------------------------------------------------
# LLM — same object works for local Ollama and AMD vLLM (config decides which)
# -----------------------------------------------------------------------------
llm = LLM(
    model=f"openai/{LLM_MODEL}",
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    temperature=0.2,
)

VALID_6R = ["Rehost", "Replatform", "Refactor", "Replace", "Retire", "Retain"]

# -----------------------------------------------------------------------------
# Structured outputs
# -----------------------------------------------------------------------------
class AssessmentOutput(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    key_risk_factors: list[str]
    summary: str

class DecisionOutput(BaseModel):
    decision: str
    confidence: str
    reasoning: str

class ExplanationOutput(BaseModel):
    headline: str
    explanation: str
    caveats: str

# -----------------------------------------------------------------------------
# Robust JSON extraction
# -----------------------------------------------------------------------------
def extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"```(?:json)?", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    return json.loads(text)

def parse_or_raise(raw: str, model, label: str):
    try:
        return model(**extract_json(raw))
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"\n[PARSE ERROR in {label}] Raw model output was:\n{raw}\n")
        raise e

# -----------------------------------------------------------------------------
# Agents
# -----------------------------------------------------------------------------
assessment_agent = Agent(
    role="Enterprise Application Risk Assessor",
    goal="Score how urgently an application needs modernization attention, from 0 to 100.",
    backstory=(
        "You are a veteran infrastructure analyst. You read an application's technical and "
        "operational data and judge how risky it is to leave it as-is. You are precise, "
        "evidence-driven, and you always answer with a single JSON object and nothing else."
    ),
    llm=llm, allow_delegation=False, verbose=True,
)

decision_agent = Agent(
    role="Application Modernization Strategist",
    goal="Choose the single best 6R decision, grounded strictly in the retrieved patterns.",
    backstory=(
        "You are a cloud modernization strategist. You never decide from memory — you ground every "
        "decision in the modernization patterns retrieved for you. You match the application's "
        "signals against those patterns and pick the one that fits. You always answer with a single "
        "JSON object and nothing else."
    ),
    llm=llm, allow_delegation=False, verbose=True,
)

explanation_agent = Agent(
    role="Technical Communicator",
    goal="Explain the modernization decision in clear language a business leader can act on.",
    backstory=(
        "You translate technical decisions into plain English. You state the decision, prove it "
        "with the application's own data, and flag risks or dependencies to handle first. You "
        "always answer with a single JSON object and nothing else."
    ),
    llm=llm, allow_delegation=False, verbose=True,
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def format_app(app: dict) -> str:
    s, o, i = app["security"], app["operational_metrics"], app["infrastructure"]
    deps_on = ", ".join(app["dependencies"]["depends_on"]) or "none"
    deps_by = ", ".join(app["dependencies"]["depended_on_by"]) or "none"
    return (
        f"Application: {app['name']} (id: {app['id']})\n"
        f"Archetype: {app['archetype']}\n"
        f"Language / Runtime: {app['language']} / {app['runtime_version']}\n"
        f"Business criticality: {app['criticality']}\n"
        f"Age: {app['age_years']} years | Last major update: {app['last_major_update_years_ago']} years ago\n"
        f"Monthly cost: ${app['monthly_cost_usd']:,}\n"
        f"Infrastructure: {i['os']} (end-of-life: {i['os_eol_date']}), hosted {i['type']}\n"
        f"Security: {s['cve_count']} CVEs ({s['critical_cve_count']} critical); "
        f"examples: {', '.join(s['sample_cves'][:3])}\n"
        f"Operations: {o['incidents_last_quarter']} incidents last quarter, MTTR {o['mttr_hours']}h, "
        f"availability {o['availability_pct']}%, CPU {o['cpu_utilization_pct']}%\n"
        f"Business description: {app['business_description']}\n"
        f"Depends on: {deps_on}\n"
        f"Depended on by: {deps_by}"
    )

def build_retrieval_query(app: dict) -> str:
    """Concise, signal-rich query. Business description carries the decisive signal,
    so we keep it within the embedding model's token window."""
    return (
        f"{app['archetype']} application in {app['language']} on {app['infrastructure']['os']} "
        f"(end of life {app['infrastructure']['os_eol_date']}), criticality {app['criticality']}, "
        f"{app['security']['cve_count']} CVEs. {app['business_description']}"
    )

# -----------------------------------------------------------------------------
# The pipeline
# -----------------------------------------------------------------------------
def analyze_app(app: dict) -> dict:
    app_block = format_app(app)

    # --- RAG: retrieve grounding patterns BEFORE the decision agent runs ---
    retrieval_query = build_retrieval_query(app)
    retrieved = retrieve_patterns(retrieval_query, k=4)
    retrieved_sources = [src for src, _ in retrieved]
    patterns_block = "\n\n".join(f"### Retrieved pattern: {src}\n{doc}" for src, doc in retrieved)

    assessment_task = Task(
        description=(
            f"Assess the modernization risk of this application.\n\n{app_block}\n\n"
            "Consider obsolescence (OS end-of-life, outdated runtime), security posture "
            "(CVE count and severity), operational health (incidents, MTTR, availability), and "
            "business context (criticality, cost). Produce a risk score from 0 to 100 where higher "
            "means more urgent and risky to leave unchanged."
        ),
        expected_output=(
            "Return ONLY a JSON object, no markdown, no prose, exactly these keys:\n"
            '{"risk_score": <integer 0-100>, '
            '"key_risk_factors": [<3 to 5 short strings>], '
            '"summary": "<2-3 sentence assessment>"}'
        ),
        agent=assessment_agent,
    )

    decision_task = Task(
        description=(
            "Choose exactly ONE 6R decision for the application below: "
            f"{', '.join(VALID_6R)}.\n\n"
            "You MUST ground your decision in the retrieved modernization patterns below. They "
            "define the exact conditions under which each decision applies. Match the application's "
            "signals to the patterns and choose the one that fits best. Pay special attention to "
            "whether the capability is duplicated or no longer needed (Retire), and whether the "
            "application is a custom system or a vendor product (only vendor products are Replace "
            "candidates).\n\n"
            f"=== RETRIEVED MODERNIZATION PATTERNS ===\n{patterns_block}\n\n"
            f"=== APPLICATION ===\n{app_block}\n\n"
            "In your reasoning, name which retrieved pattern(s) support your choice."
        ),
        expected_output=(
            "Return ONLY a JSON object, no markdown, no prose, exactly these keys:\n"
            '{"decision": "<one of: Rehost, Replatform, Refactor, Replace, Retire, Retain>", '
            '"confidence": "<High, Medium, or Low>", '
            '"reasoning": "<why this decision, citing the retrieved pattern(s) and the app data>"}'
        ),
        agent=decision_agent,
        context=[assessment_task],
    )

    explanation_task = Task(
        description=(
            "Write a clear, defensible explanation of the modernization decision for a business "
            "audience. State the decision and its main reason, back it with the application's own "
            "data (cite real numbers), and flag dependencies or risks to handle first."
        ),
        expected_output=(
            "Return ONLY a JSON object, no markdown, no prose, exactly these keys:\n"
            '{"headline": "<one sentence, decision + main reason>", '
            '"explanation": "<plain-English paragraph an executive could read aloud>", '
            '"caveats": "<risks, dependencies, or sequencing notes>"}'
        ),
        agent=explanation_agent,
        context=[assessment_task, decision_task],
    )

    crew = Crew(
        agents=[assessment_agent, decision_agent, explanation_agent],
        tasks=[assessment_task, decision_task, explanation_task],
        process=Process.sequential,
        verbose=True,
    )
    crew.kickoff()

    assessment = parse_or_raise(assessment_task.output.raw, AssessmentOutput, "assessment")
    decision = parse_or_raise(decision_task.output.raw, DecisionOutput, "decision")
    explanation = parse_or_raise(explanation_task.output.raw, ExplanationOutput, "explanation")

    decision_clean = decision.decision.strip().title()

    return {
        "app_id": app["id"],
        "app_name": app["name"],
        "expected_6r": app.get("expected_6r"),
        "risk_score": assessment.risk_score,
        "key_risk_factors": assessment.key_risk_factors,
        "assessment_summary": assessment.summary,
        "retrieved_patterns": retrieved_sources,
        "decision": decision_clean,
        "decision_valid": decision_clean in VALID_6R,
        "confidence": decision.confidence,
        "decision_reasoning": decision.reasoning,
        "headline": explanation.headline,
        "explanation": explanation.explanation,
        "caveats": explanation.caveats,
    }

# -----------------------------------------------------------------------------
# Run on the first app
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, DATA_PATH)) as f:
        apps = json.load(f)

    app = apps[0]  # CoreBillingLedger-646 — should land on Retire
    print(f"\n{'='*70}\nAnalyzing: {app['name']}  (expected: {app.get('expected_6r')})\n{'='*70}\n")

    result = analyze_app(app)

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)
    print(f"App:            {result['app_name']}")
    print(f"Risk score:     {result['risk_score']}/100")
    print(f"Retrieved KB:   {', '.join(result['retrieved_patterns'])}")
    print(f"Decision:       {result['decision']}  (expected: {result['expected_6r']})  "
          f"{'[VALID]' if result['decision_valid'] else '[INVALID 6R VALUE]'}")
    print(f"Confidence:     {result['confidence']}")
    print("\nKey risk factors:")
    for fct in result["key_risk_factors"]:
        print(f"  - {fct}")
    print(f"\nDecision reasoning: {result['decision_reasoning']}")
    print(f"\nHeadline:    {result['headline']}")
    print(f"\nExplanation: {result['explanation']}")
    print(f"\nCaveats:     {result['caveats']}")
    print("=" * 70)