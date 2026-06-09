# Decision Rationale: Writing a Defensible Recommendation

## Purpose
A 6R decision is only useful if a human can read it, trust it, and act on it. This document defines what a good recommendation explanation contains — the standard the Explanation Agent should meet.

## A recommendation without a reason is a guess
The single rule: every recommendation must show **why**. "The AI said Retire" is worthless to a decision-maker. "Retire, because the app runs on an OS that lost support in 2020, carries 8 unpatched critical vulnerabilities, fails 8 times a quarter, and duplicates a system already in use" is something a manager can take to a board.

## The four parts of a defensible explanation

### 1. The decision and the headline reason
State the 6R decision and the single most important reason in one sentence. Lead with the strongest signal.
> "Retire — this billing ledger is a high-risk liability whose function is already covered by another system."

### 2. The evidence (cite the actual data)
Point to the specific data points that drove the decision. Use real numbers from the app record, not vague claims.
> "It runs on RHEL 6 (end-of-support since 2020), carries 11 CVEs including 8 critical, recorded 8 incidents last quarter with a 17.7-hour mean recovery time, and costs $41,200/month."

### 3. The grounding (cite the retrieved pattern)
Reference the modernization pattern the decision was grounded in — this is the RAG payoff. It shows the decision follows known practice, not model guesswork.
> "This matches the standard retirement profile: end-of-life infrastructure plus duplicated capability plus poor operational health."

### 4. The caveat (flag risks and sequencing)
Name what could go wrong or what must happen first. This is what separates a naive recommendation from a real one.
> "Before decommissioning, confirm the inbound dependencies from the settlement systems are migrated, and archive the transaction history for regulatory retention."

## What makes an explanation weak
- **Vague:** "This app is old and risky." (No data, no specifics.)
- **Unfounded:** Claims not backed by the app's actual record.
- **No grounding:** Doesn't reference any pattern or prior practice.
- **No caveat:** Pretends the decision is risk-free, ignores dependencies and sequencing.
- **Wrong audience:** Written in jargon a CIO can't follow. The test: could a non-technical executive read it aloud in a meeting and sound informed?

## Confidence calibration
State a confidence level, and make it mean something:
- **High confidence** — signals are strong and aligned (clear Retire, clear Retain). High-confidence calls should be right far more often than low-confidence ones.
- **Medium / low confidence** — signals conflict (e.g. strong technical case to move, but a compliance constraint), or the decision is a close call between two options. Say so honestly, and name the tension.

## The standard to hold
> A good recommendation states the decision, proves it with the app's own data, grounds it in a known pattern, names the risks, and could be read aloud by a manager who'd then sound like they understood the system. Anything less is a guess with a label on it.

## Keywords for matching
explanation, defensible recommendation, reasoning, cite evidence, grounding, retrieved pattern, caveat, dependency sequencing, confidence calibration, plain language, executive readable, why decision, justification, audit trail
