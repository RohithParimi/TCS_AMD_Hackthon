# Anti-Pattern: Rehosting What Should Be Retired

## The mistake
Taking an old, low-value, redundant, or barely-used application and lifting it to the cloud as-is — instead of switching it off.

## Why it happens
- It feels safer to move something than to kill it ("we might need it").
- Nobody wants to be the person who decommissioned a system that turned out to matter.
- Retiring requires confirming the app is truly unneeded, which takes investigation; rehosting is the path of least resistance.

## Why it's wrong
You're now **paying cloud costs forever to run something that delivers no value**. You've also spent migration effort and testing on it. Worse, you've legitimised it — an app that's been "successfully migrated to the cloud" is much harder to retire later. The cheapest, most secure application is the one that's switched off. Rehosting dead weight is the opposite of that.

## How to spot it
The app shows Retire signals — duplicated capability, end-of-life OS, many unpatched CVEs, poor operational health, no clear owner, low business value — but someone is proposing to Rehost it because that feels less drastic.

## The correct decision
**Retire.** If you're genuinely unsure whether it's needed, the answer is to *investigate the dependency graph and confirm with the business* — not to default to a rehost. Only rehost an app that is healthy, used, and worth keeping.

## Rule of thumb
> Never spend cloud budget moving something you should be switching off. If an app's strongest signals point to Retire, rehosting is just deferring the retirement at a recurring cost.

## Keywords for matching
anti-pattern, mistake, rehost instead of retire, lift dead weight, migrate redundant app, paying to run useless app, should be decommissioned, legitimising legacy, avoid retiring, low value cloud cost
