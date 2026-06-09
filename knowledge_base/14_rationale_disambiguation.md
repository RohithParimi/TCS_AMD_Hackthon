# Decision Rationale: Disambiguating Between Close 6R Decisions

## Purpose
The hardest part of 6R decisioning isn't the obvious cases — it's telling apart two decisions that look similar. This document gives the deciding questions for each commonly-confused pair.

## Rehost vs. Replatform
**Both** move the app to the cloud. The difference is whether you change anything on the way.
- **Deciding question:** *Is the current platform/runtime a problem?*
  - No, it's fine, just exiting the data centre → **Rehost** (change nothing).
  - Yes — EOL OS, outdated runtime, or an easy managed-service win available → **Replatform** (targeted changes).
- **Tell:** If the OS is end-of-life, it's almost never Rehost — rehosting an EOL box just relocates the security problem. Lean Replatform.

## Replatform vs. Refactor
**Both** improve the app for the cloud. The difference is how deep the change goes.
- **Deciding question:** *Is the problem the platform, or the application logic itself?*
  - The logic is fine; the infrastructure/runtime is the issue → **Replatform** (leave the code alone).
  - The logic itself is holding the business back and the app is strategic → **Refactor** (rewrite it).
- **Tell:** If the team says "the code works great, it's just stuck on old infrastructure," that's Replatform. If they say "we need it to do more / scale / be maintainable and it can't in its current form," that's Refactor.

## Refactor vs. Replace
**Both** result in a modern system. The difference is build vs. buy.
- **Deciding question:** *Is this capability differentiating, and do we own the code?*
  - Differentiating, unique logic, we own the source → **Refactor** (rebuild and keep ownership).
  - Non-differentiating, or a commercial product does it better, or it's a vendor binary we can't rewrite → **Replace** (buy the capability).
- **Tell:** COTS / pre-compiled vendor binary → it can only be Replace (or Replatform/Rehost), never Refactor.

## Retire vs. everything else
- **Deciding question:** *Does the business still need this capability, and is it provided elsewhere?*
  - No longer needed, or duplicated by another system → **Retire**.
  - Still needed → it's one of the four "keep the capability" decisions (Rehost/Replatform/Refactor/Replace).
- **Tell:** Duplication is the loudest Retire signal. Two apps doing the same job is one app too many.

## Retain vs. an active decision
- **Deciding question:** *Is leaving it alone justified by health/compliance, or is it just avoidance?*
  - Healthy, secure, recently modernised, or compliance-locked with a review date → **Retain**.
  - Old, insecure, unhealthy, and untouched only because it's scary → **NOT Retain**; pick an active decision.

## The reasoning order that works
1. Is the capability still needed? (No → Retire.)
2. Do we own the code? (No → Replace / Replatform / Rehost only.)
3. Is the app healthy and modern? (Yes → Retain, unless data-centre exit forces a move.)
4. Is the *logic* the problem or the *platform*? (Logic → Refactor; platform → Replatform.)
5. Does a commercial successor do it better? (Yes → Replace.)
6. Is it fine as-is and just needs to move? (Yes → Rehost.)

## Keywords for matching
disambiguation, rehost vs replatform, replatform vs refactor, refactor vs replace, retire vs retain, deciding question, close decision, ambiguous case, build vs buy, logic vs platform, reasoning order, how to choose 6R
