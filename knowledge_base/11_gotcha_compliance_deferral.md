# Gotcha: Compliance and Certification Deferrals

## The trap
An application's technical signals point clearly toward modernisation (move it, refactor it, replatform it) — but a regulatory, compliance, or certification constraint makes acting *right now* the wrong call, even though the technology says "go."

## Why it's dangerous
Technical health is only half the picture. Some applications operate under constraints that override the engineering signal:
- **Re-certification requirements** — moving the app invalidates an existing audit certification, triggering a months-long (sometimes 12–18 month) re-certification before it can run in production again.
- **Data residency / sovereignty** — the data legally cannot leave a jurisdiction or a controlled zone, blocking certain cloud moves.
- **Audit freeze windows** — the app cannot be changed during a regulatory audit period.
- **Validated environments** — in regulated industries (finance, pharma, healthcare), the running environment itself is validated; changing it means re-validating.

Ignore these and you don't just create technical risk — you create **legal and regulatory exposure**, which is far more expensive than running on slightly older infrastructure for another year.

## How it affects the 6R decision
A compliance constraint can **override an otherwise-clear modernisation decision** and push it to **Retain — with a review date tied to the compliance cycle.**

Critically, this only applies when the app is *otherwise healthy and secure*. A compliance constraint is a reason to defer a move on a healthy app; it is **not** an excuse to leave an insecure, end-of-life app running forever (see the "Retaining Insecure Legacy" anti-pattern). The two must not be confused.

## What to check
- Is the app **COMPLIANCE_CRITICAL** or in a regulated/isolated zone (e.g. a secure vault zone)?
- Is there an explicit **re-certification or review timeline**?
- Has the **owning compliance team flagged it** as out of scope for the current cycle?
- Is the app **otherwise healthy** (so deferral is reasonable, not negligent)?

## The right way to flag it
"The technical signals would suggest [Replatform/Refactor], but this is a compliance-critical system under an 18-month re-certification constraint and is currently healthy and secure. The correct decision is **Retain**, with a review scheduled at the next compliance cycle." Naming both the override *and* the review date is what makes it defensible.

## Representative example
An audit-trail vault on modern, hardened infrastructure (Java 17, hardened RHEL 8), zero incidents, near-perfect availability — but governed by a regulatory framework requiring 18-month re-certification before any infrastructure migration. Healthy enough to defer, constrained enough that moving now is the wrong call. Retain with a review date.

## Keywords for matching
gotcha, compliance, certification, re-certification, regulatory constraint, data residency, sovereignty, audit freeze, validated environment, compliance-critical, secure zone, defer modernisation, retain with review date, regulatory exposure
