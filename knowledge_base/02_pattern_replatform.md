# Pattern: Replatform (Lift, Tinker, and Shift)

## Decision
**Replatform** — move the application to the cloud with minor, targeted changes that take advantage of cloud capabilities, but without rewriting the core application. Sometimes called "lift, tinker, and shift."

## What it means in plain terms
You move the app to the cloud and make a few smart changes along the way — like swapping a self-managed database for a managed cloud database, containerising it, or putting it behind a managed load balancer. The core business logic stays untouched. You change the platform underneath, not the application itself.

## When to choose Replatform — the signals
Choose Replatform when:
- The **core business logic is stable and valuable** — it works, it's tested, and rewriting it is unnecessary risk.
- The **infrastructure or runtime is the actual problem** — the OS is unsupported, the hardware is failing, or the runtime is outdated — NOT the application logic.
- There's a **clear, low-effort optimisation available** — a managed database, containerisation, or a managed runtime — that improves operations without a rewrite.
- A **vendor migration path exists** for COTS products (e.g. an on-prem product with a documented cloud-native edition that needs only configuration changes).
- The team wants **operational improvement** (less patching, better scaling) but a full refactor isn't justified.

## When NOT to choose Replatform
- If the logic itself is the problem (badly designed, unmaintainable), Replatform just relocates the mess — Refactor instead.
- If the app is healthy and the infrastructure is fine, Replatform is unnecessary effort — Rehost or Retain.
- If the app is obsolete or duplicated, Retire it.

## Why it's the right call when signals match
Replatform is the **sweet spot between Rehost and Refactor**. You get real operational gains (managed services, supported platforms, better scaling) for far less effort and risk than a full redesign — precisely because you leave the proven business logic alone. It's the right answer for "the code is fine, the platform is the problem."

## Risks and trade-offs
- Scope creep: "minor changes" can quietly grow into a refactor. Discipline is required to keep changes targeted.
- You don't get the full benefits of a cloud-native redesign.

## Representative examples
- A 21-year-old COBOL payroll engine whose logic is stable and handles two decades of regulatory edge cases, but which runs on an end-of-life Windows Server. The right move is to move the platform (managed cloud, containerisation) without touching the COBOL.
- A vendor ETL platform (e.g. Informatica PowerCenter v10.5) with a documented migration to the vendor's cloud-native edition requiring only configuration changes, not custom-code rewrites.

## Keywords for matching
replatform, lift tinker shift, managed database, containerise, minor changes, infrastructure problem, stable logic, supported platform, vendor cloud edition, operational improvement, no rewrite, optimise without redesign
