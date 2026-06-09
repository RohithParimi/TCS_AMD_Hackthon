# Pattern: Retire (Decommission)

## Decision
**Retire** — shut the application down and remove it from the portfolio entirely. Also called "decommission" or "sunset."

## What it means in plain terms
You stop running the app, migrate or archive any data that still matters, and switch it off for good. No cloud move, no rebuild, no replacement of the system itself — the capability is either no longer needed, or it's already provided somewhere else. Every application you retire is one you never have to secure, patch, or pay for again.

## When to choose Retire — the signals
Choose Retire when:
- The application is **barely used, redundant, or duplicated** by another system that does the same thing.
- It runs on **end-of-life OS and outdated runtime** with **many unpatched critical CVEs** — it's a liability, not an asset.
- It has **poor operational health** — frequent incidents, high MTTR, low availability — and fixing it isn't worth it.
- **Maintenance cost is high relative to the value** it delivers.
- **No team owns the expertise** anymore (e.g. nobody knows the COBOL/legacy stack).
- The business has **confirmed the capability is no longer required**, or is covered elsewhere.

## When NOT to choose Retire
- If the application is **essential and irreplaceable**, even if it's old and insecure — you cannot retire it; you must Refactor or Replatform.
- If something **critical depends on it** and nothing else provides the capability, retiring it breaks the dependents. Resolve dependencies first.
- If it's healthy and used, Retire makes no sense — Retain.

## Why it's the right call when signals match
Retire is the **highest-leverage modernisation decision** because it removes work permanently. The cheapest application to run, secure, and maintain is the one you've switched off. When an app is a high-cost, high-risk, low-value liability — especially if its function is duplicated — retiring it is the disciplined choice. Don't spend modernisation budget moving dead weight to the cloud.

## Risks and trade-offs
- **Hidden dependencies** — an app that looks unused may have a quiet but critical consumer. Always check the dependency graph before decommissioning.
- **Data retention / compliance** — some data must be archived for regulatory reasons before shutdown.
- **Irreversibility** — once it's gone, recovering it is expensive. Confirm before pulling the plug.

## Representative examples
- A Java 7 billing ledger on an end-of-life RHEL 6 (EOL 2020), with 11 CVEs (8 critical), 8 incidents per quarter, and a 17.7-hour mean time to recovery. High cost, high risk, no roadmap. Retire it.
- A COBOL billing ledger duplicating an existing system, on an EOL OS, with no engineer on the team who knows COBOL and a business confirmation that it can be decommissioned. Retire once its small dependency set is cleared.

## Keywords for matching
retire, decommission, sunset, shut down, switch off, redundant, duplicated, barely used, end-of-life, unpatched CVEs, high cost low value, liability, no owner, dead weight, remove from portfolio
