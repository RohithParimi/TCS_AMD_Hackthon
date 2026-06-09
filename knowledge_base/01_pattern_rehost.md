# Pattern: Rehost (Lift and Shift)

## Decision
**Rehost** — move the application to the cloud as-is, with no changes to its code or architecture. Also called "lift and shift."

## What it means in plain terms
You pick the application up from where it runs today and drop it onto cloud infrastructure unchanged. The app doesn't know it moved. You get cloud benefits (managed hardware, elasticity, no data-centre overhead) without touching the software itself.

## When to choose Rehost — the signals
Choose Rehost when ALL of these tend to be true:
- The application is **stable and vendor-supported** — it works, and someone still patches it.
- The **operating system is still supported** (not past end-of-life).
- There is **no custom code to maintain**, or the code is simple and self-contained.
- **Dependencies are few and simple** — it doesn't sit at the centre of a tangled web.
- There is **no immediate business driver to redesign** it — the goal is to exit the data centre, not to improve the app.
- The app has **moderate operational health** — occasional incidents, but nothing systemic.

## When NOT to choose Rehost
- If the OS is end-of-life, rehosting just moves an insecure box to the cloud — that's a security problem with a new IP address. Consider Replatform or Refactor.
- If the app is barely used or duplicated, don't rehost it — Retire it.
- If the app is strategic and you want it cloud-native, Rehost wastes the migration window — Refactor instead.

## Why it's the right call when signals match
Rehost is the **fastest, lowest-risk** cloud move. Minimal engineering, minimal testing, quick win. It's the right answer when the app is healthy enough to leave alone but the data centre needs to close. You can always optimise later, once it's in the cloud.

## Risks and trade-offs
- You inherit the app's existing inefficiencies — it won't be cheaper to run just because it's in the cloud.
- It's a tactical move, not a strategic one. Don't expect performance or cost gains.

## Representative example
A vendor-supported endpoint security control plane (e.g. Carbon Black App Control v8.9.2) running on a current, supported Windows Server. No custom code, stable operations, well-documented vendor cloud-deployment path. The fast win is to lift it to cloud infrastructure unchanged.

## Keywords for matching
lift and shift, rehost, move as-is, no code change, fast cloud migration, supported OS, vendor-supported, stable, low complexity, quick win, exit data centre, tactical migration
