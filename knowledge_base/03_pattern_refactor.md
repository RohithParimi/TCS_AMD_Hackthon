# Pattern: Refactor (Re-architect)

## Decision
**Refactor** — significantly redesign and rewrite the application to be cloud-native, while preserving its essential business capability. Also called "re-architect."

## What it means in plain terms
You keep *what the app does* but fundamentally change *how it does it*. You break a monolith into services, adopt cloud-native patterns, modernise the codebase, and rebuild it to scale and operate well in the cloud. This is the most expensive and highest-effort option — but it produces the best long-term result for applications worth the investment.

## When to choose Refactor — the signals
Choose Refactor when:
- The application is **strategic** — it's core to the business and will be around for years.
- The **business logic is valuable and worth preserving**, but the current implementation is holding the business back.
- The app is on **outdated/unsupported technology** (old framework, EOL OS) AND has accumulating security or operational problems — but killing it isn't an option because the capability is essential.
- The team has **deep understanding of the logic**, making a careful re-architecture feasible.
- There is a **clear business case** for the cloud-native benefits (scalability, agility, lower long-term cost) that justifies the high upfront cost.

## When NOT to choose Refactor
- If the app is obsolete, duplicated, or low-value, Refactor is wasted money — Retire.
- If only the infrastructure is the problem and the logic is fine, Refactor is overkill — Replatform.
- If a commercial product now does the job better, don't rebuild it — Replace.
- If the app is healthy and modern, leave it — Retain.

## Why it's the right call when signals match
Refactor is the right answer when an application is **too important to kill but too broken to keep as-is**. You're making a deliberate, expensive investment because the capability is strategic and the current form is a liability. The payoff is a modern, maintainable, scalable system the business can build on.

## Risks and trade-offs
- **Highest cost and longest timeline** of all 6R options.
- **Highest execution risk** — rewrites can introduce bugs and lose subtle behaviour. Strong testing and domain knowledge are essential.
- Easy to under-estimate; the most common modernisation failure mode is refactoring something that should have been replatformed or retired.

## Representative example
A settlement orchestration wrapper around a mainframe core (e.g. .NET Framework 4.0 on an end-of-life Windows Server, multiple critical CVEs) whose business logic is complex, proprietary, and deeply understood by the team. The logic is a strategic asset; the implementation is a liability. The right move is to re-architect it cloud-native while preserving the hard-won settlement logic.

## Keywords for matching
refactor, re-architect, redesign, cloud-native, rewrite, break up monolith, strategic application, valuable logic, modernise codebase, high investment, scalability, long-term, preserve capability
