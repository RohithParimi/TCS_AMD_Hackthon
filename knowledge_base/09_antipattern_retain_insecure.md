# Anti-Pattern: Retaining Insecure Legacy ("Do Nothing" as Neglect)

## The mistake
Labelling an old, insecure, unhealthy application as "Retain" — when in reality nobody has made a decision at all. This is neglect disguised as a strategy.

## Why it happens
- The app is scary to touch (mission-critical, poorly understood, no documentation).
- Whoever understood it has left.
- "It still works, don't poke it" becomes the unofficial policy.
- Retain sounds like a legitimate 6R decision, so it provides cover for inaction.

## Why it's wrong
Genuine Retain is for **healthy, secure, recently-modernised apps**, or apps locked by a real compliance constraint with a review date. Applying it to an app on an **end-of-life OS with unpatched critical CVEs and frequent incidents** is dangerous:
- The security risk compounds every day — unpatched critical CVEs on EOL infrastructure are how breaches happen.
- The longer it's neglected, the more expensive and risky it eventually becomes to fix.
- Calling it "Retain" stops anyone from owning the problem.

## How to distinguish real Retain from neglect
| Signal | Real Retain | Neglect mislabelled as Retain |
|--------|-------------|-------------------------------|
| OS support | Supported, years of life left | End-of-life, unsupported |
| Security | Few/no CVEs, patched | Many unpatched critical CVEs |
| Operational health | High availability, low incidents | Frequent incidents, high MTTR |
| Justification | Data-backed, has a review date | "It still works, don't touch it" |

## The correct decision
For an old, insecure, unhealthy app, the right answer is an **active** decision:
- Strategic + worth preserving → **Refactor**
- Good logic, bad platform → **Replatform**
- Commercial successor exists → **Replace**
- Low value / redundant → **Retire**

Never **Retain.**

## Rule of thumb
> Retain is a decision, not a hiding place. If the only reason you're not modernising an insecure legacy app is that it's scary, that's exactly why it needs an active decision.

## Keywords for matching
anti-pattern, mistake, retain insecure legacy, neglect, do nothing, unpatched CVEs, end-of-life OS, scary to touch, no owner, security risk compounding, false retain, inaction, needs active decision
