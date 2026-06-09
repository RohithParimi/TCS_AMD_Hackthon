# Gotcha: Hidden Dependency Traps

## The trap
An application looks like an obvious Retire or easy Rehost — until you discover that something critical quietly depends on it, or that it depends on something that isn't ready to move. Modernising it in isolation breaks the systems around it.

## Why it's dangerous
The dependency graph is where modernisation plans go wrong. The two failure modes:

1. **Retiring a quiet provider.** An app that looks unused may have a low-traffic but business-critical consumer (a nightly batch job, a compliance feed, a downstream settlement step). Switch it off and something important fails — often silently, often days later.

2. **Moving a dependent before its dependency.** If App A depends on App B, and you migrate or rehost App A while App B is still on-prem, you can introduce latency, break network paths, or create a split-brain configuration.

## What to check before deciding
- **`depended_on_by`** — who relies on this app? If anything critical does, Retire is risky and the dependents must be handled first.
- **`depends_on`** — what does this app rely on? Those dependencies may need to move first, or move together.
- **Criticality of the dependency edges** — a HIGH-criticality dependency is a hard blocker; a LOW one is a manageable risk.

## How it affects the 6R decision
- A clear-Retire app with a **critical inbound dependency** becomes **"Retire — but only after the dependent is migrated or the dependency is severed."** The decision is right; the *sequencing* is the catch.
- A Rehost or Replatform candidate with **critical outbound dependencies still on-prem** may need to move **as part of a group**, not alone.

## The right way to flag it
A good recommendation doesn't just give the 6R decision — it **names the dependency risk**: "Retire is correct, but this app is depended on by [X]; resolve that dependency before decommissioning." That sequencing note is what separates a real recommendation from a naive one.

## Representative example
A billing ledger that's a clear Retire on its own merits (EOL OS, many CVEs, redundant) — but the dependency graph shows other legacy systems still call it. The decision stays Retire; the recommendation must flag that the inbound dependents have to be cleared first.

## Keywords for matching
gotcha, hidden dependency, dependency graph, depended on by, blast radius, quiet consumer, critical dependency, sequencing, migrate together, break downstream, retire blocked by dependents, move dependency first
