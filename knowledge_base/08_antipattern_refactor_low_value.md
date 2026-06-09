# Anti-Pattern: Refactoring Low-Value Applications

## The mistake
Pouring expensive re-architecture effort into an application that isn't strategic enough to justify it — when a cheaper decision (Replatform, Replace, or Retire) would have served the business better.

## Why it happens
- Engineers enjoy rewriting things; a greenfield cloud-native rebuild is more interesting than a lift-and-shift.
- "Modernise" gets equated with "rewrite," so refactoring feels like the most thorough, responsible option.
- The true value of the app to the business is never honestly assessed.

## Why it's wrong
Refactor is the **most expensive and highest-risk** of all 6R decisions. Spending it on a non-strategic app means:
- You burn the budget that strategic apps needed.
- You take on rewrite risk (lost behaviour, new bugs) for little payoff.
- You delay the whole portfolio because one team is deep in an unnecessary rebuild.

A non-differentiating capability should usually be **bought (Replace)**. A stable app on bad infrastructure should be **Replatformed**. A low-value app should be **Retired**. Refactor is reserved for the apps the business genuinely cannot do without and wants to build on.

## How to spot it
A Refactor is proposed for an app that is: low or medium criticality, non-differentiating, replaceable by a commercial product, or whose only real problem is the infrastructure (not the logic). The business value doesn't justify the cost of a rewrite.

## The correct decision
- Non-differentiating + commercial equivalent exists → **Replace**
- Good logic + bad infrastructure → **Replatform**
- Low value / redundant → **Retire**
- Only Refactor when the logic is **strategic, valuable, and worth preserving through a rebuild.**

## Rule of thumb
> Refactor is a strategic investment, not a default. If you can't name the specific, lasting business value the rewrite unlocks, you've picked the wrong decision.

## Keywords for matching
anti-pattern, mistake, refactor low value, unnecessary rewrite, expensive re-architecture, rewrite for its own sake, non-strategic refactor, over-engineering, wasted modernisation budget, should replatform or replace, rewrite risk
