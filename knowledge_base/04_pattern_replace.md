# Pattern: Replace (Repurchase)

## Decision
**Replace** — retire the existing application and adopt a different product, usually a commercial off-the-shelf (COTS) or SaaS solution, to deliver the same capability. Also called "repurchase" or "drop and shop."

## What it means in plain terms
Instead of moving or rebuilding the app, you stop using it and switch to a product that already does the job — often a modern SaaS subscription. You're buying the capability instead of maintaining it. The classic case is moving from a custom or legacy system to a commercial product the whole industry already uses.

## When to choose Replace — the signals
Choose Replace when:
- The application is a **vendor product (COTS) approaching or past end-of-support**, and the **vendor offers a successor product** with a defined migration path.
- A **mature commercial or SaaS product now does the job as well or better** than the in-house/legacy system.
- The app is a **pre-compiled vendor binary** — you *cannot* refactor it because you don't own the source. Your only modernisation levers are Replace or Replatform.
- The cost of maintaining the current system **exceeds the cost of subscribing** to a modern equivalent.
- The capability is **non-differentiating** — it's not a competitive advantage, so there's no reason to custom-build it.

## When NOT to choose Replace
- If the application encodes **unique, differentiating business logic** that no commercial product replicates, Replace loses that value — Refactor instead.
- If the current product is fine and supported, Replace is unnecessary churn — Retain or Rehost.
- If no suitable replacement exists, you can't replace it — consider Refactor or Replatform.

## Why it's the right call when signals match
Replace is the right answer when **someone else already solved this problem better than you can**. For vendor products nearing end-of-life with a clear successor, replacing is the vendor-sanctioned, lowest-friction path. For non-differentiating capabilities, buying beats building and maintaining.

## Risks and trade-offs
- **Data migration** and **integration rework** can be significant — the new product won't fit the old one's integrations exactly.
- **Change management** — users must be retrained, processes adjusted.
- Risk of **feature gaps** — the replacement may not do everything the old system did.

## Representative examples
- An enterprise ERP on a vendor edition approaching end-of-maintenance (e.g. SAP ECC 6.0, with SAP S/4HANA as the vendor-mandated successor). It's a pre-compiled vendor binary — it cannot be refactored. The vendor-defined path is to replace it.
- An identity manager at end-of-support (e.g. IBM Tivoli Identity Manager v7.0.1) where the vendor's modern SaaS successor (IBM Security Verify) eliminates on-prem overhead. Replace with the successor product.

## Keywords for matching
replace, repurchase, drop and shop, COTS, SaaS, commercial product, vendor successor, end-of-support, pre-compiled binary, cannot refactor, buy not build, non-differentiating, migration path, subscription
