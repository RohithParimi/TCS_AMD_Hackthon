# Pattern: Retain (Revisit Later)

## Decision
**Retain** — deliberately leave the application as it is for now, with no modernisation action. Also called "revisit" or "do nothing (on purpose)."

## What it means in plain terms
You make a conscious decision NOT to touch the application right now. This is different from neglect — it's an active call that, weighing cost against benefit, modernising this app today is the wrong use of resources. You'll revisit the decision at a defined future point.

## When to choose Retain — the signals
Choose Retain when:
- The application is **recently modernised** — current language version, supported OS, modern architecture.
- It has **excellent operational health** — zero or very few incidents, high availability, low MTTR.
- It has **few or no security findings**, and any that exist are patched or mitigated.
- There is **no business case to change it** — it works, it's cheap to run, and modernising it wouldn't produce meaningful benefit.
- A **regulatory, compliance, or certification constraint** makes change expensive or risky right now (e.g. an 18-month re-certification requirement before any infrastructure migration).
- The **owning team has explicitly flagged it as out of scope** for the current modernisation cycle.

## When NOT to choose Retain
- If the app is old, insecure, or unhealthy, Retain is just neglect dressed up — pick an active decision (Refactor, Replatform, Replace, or Retire).
- If there's a clear business benefit to moving it, Retain wastes that opportunity.
- If it runs on end-of-life infrastructure, "leave it alone" is a security risk, not a strategy.

## Why it's the right call when signals match
Retain is the right answer when **the smartest modernisation move is to spend your budget elsewhere**. Modernisation resources are finite. An app that's healthy, secure, recently updated, or locked by compliance is exactly where you should NOT spend them. Retaining it frees budget for the apps that actually need it (the Retires and Refactors). Crucially, Retain is a *decision with a review date*, not a permanent ignore.

## Risks and trade-offs
- **Decay over time** — a "Retain" today can become a "Replatform" in two years as the OS approaches EOL. Set a review date.
- **Mistaking neglect for Retain** — make sure the decision is justified by data, not by avoidance.

## Representative examples
- An immutable audit-trail vault on Java 17 and hardened RHEL 8, modernised 18 months ago, with zero incidents, 99.98% availability, one patched low-severity CVE, and a regulatory framework requiring 18-month re-certification before any migration. Moving it now costs more than it saves. Retain.
- A KYC validation ledger on .NET 8 and hardened RHEL 8, zero incidents, 99.95% availability, actively maintained, explicitly flagged by the compliance team as out of scope until the 2027 review. Retain.

## Keywords for matching
retain, revisit, do nothing on purpose, leave alone, recently modernised, healthy, supported OS, current version, zero incidents, high availability, no business case, compliance constraint, re-certification, out of scope, review date
