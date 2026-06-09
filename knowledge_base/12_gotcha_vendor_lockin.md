# Gotcha: Vendor Lock-In and COTS Constraints

## The trap
Treating a commercial off-the-shelf (COTS) vendor product the same way you'd treat custom in-house software — and proposing to Refactor it, when in fact you don't own the source code and physically cannot.

## Why it's dangerous
A COTS product is a **pre-compiled vendor binary**. You did not write it, you cannot see its source, and you cannot legally or technically rewrite it. This fundamentally limits which 6R decisions are even available:

- **Refactor is OFF the table** — you can't re-architect code you don't own.
- Your realistic options are **Replatform** (if the vendor offers a cloud-native edition or a supported way to move the runtime), **Replace** (adopt the vendor's successor product or a competitor), **Rehost** (if it's still supported and you just need to move the box), or **Retire** (if the capability is no longer needed).

Proposing a Refactor for a vendor binary is an immediate tell that the recommendation didn't understand what the application actually is.

## What to check
- Is the `archetype` **COTS_VENDOR**? Is the language a **"Pre-compiled Binary"**?
- Does the **vendor offer a successor** product or cloud edition? (Determines Replace vs Replatform.)
- Is the current version **still supported**, or past **end-of-support**? (End-of-support with a successor → Replace.)
- Is there a **documented vendor migration path**? (A clean path lowers the risk of either Replatform or Replace.)

## How it affects the 6R decision
- COTS, end-of-support, vendor successor exists → **Replace** (the vendor-sanctioned path).
- COTS, still supported, vendor cloud edition needs only config changes → **Replatform**.
- COTS, still supported, no changes needed, just exiting the data centre → **Rehost**.
- COTS, capability no longer needed → **Retire**.
- COTS → **never Refactor.**

## The right way to flag it
"This is a pre-compiled vendor binary (COTS), so Refactor is not an available option. Given [end-of-support / successor product / supported status], the correct decision is [Replace / Replatform / Rehost]." Stating *why Refactor is excluded* demonstrates the recommendation understood the constraint.

## Representative examples
- An ERP vendor binary nearing end-of-maintenance with a vendor-mandated successor → **Replace** (not Refactor — you can't rewrite SAP).
- A vendor ETL platform, still supported, with a documented cloud-native edition needing only configuration → **Replatform**.
- A vendor endpoint-security product, supported and stable, that just needs to move to cloud hosting → **Rehost**.

## Keywords for matching
gotcha, vendor lock-in, COTS, pre-compiled binary, cannot refactor, no source code, vendor successor, end-of-support, vendor migration path, replace not refactor, commercial product constraint, SaaS successor, vendor edition
