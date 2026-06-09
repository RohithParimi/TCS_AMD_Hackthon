# Decision Rationale: How to Score Modernization Risk

## Purpose
This document explains how to turn an application's raw data into a **modernization risk/readiness score (0–100)** and how that score relates to the 6R decision. A higher score means more urgent and more risky to leave alone.

## The four signal groups
Weigh these four dimensions together. No single one decides the score.

### 1. Obsolescence (how outdated is it?)
- **Operating system support:** Is the OS past end-of-life? An EOL OS is the single strongest risk signal — it means no security patches.
- **Runtime / language version:** Java 6/7, .NET Framework 4.0, COBOL on legacy mainframe runtimes are high-obsolescence. Java 17, .NET 8, current Python/Node are low.
- **Age:** Older apps trend higher, but age alone is weak — a 21-year-old app with stable logic and supported infra can be lower risk than a 5-year-old app on an EOL OS.

### 2. Security posture (how exposed is it?)
- **CVE count and severity:** Many critical, unpatched CVEs = high risk. A handful of patched/mitigated low-severity CVEs = low risk.
- **Remediation availability:** If fixes exist but aren't applied, that's a management problem and elevates risk. If the app simply can't be patched (EOL), risk is higher still.

### 3. Operational health (is it healthy in production?)
- **Incidents per quarter:** High incident counts signal instability.
- **MTTR (mean time to recovery):** Long recovery times mean failures hurt. Sub-hour MTTR is healthy; double-digit hours is not.
- **Availability %:** Below ~98% is a concern; 99.9%+ is healthy.

### 4. Business context (does it matter, and can it change?)
- **Criticality:** MISSION_CRITICAL raises the *stakes* of both action and inaction.
- **Dependencies:** Heavy inbound/outbound dependencies raise execution risk.
- **Compliance constraints:** Can override the technical score (see compliance gotcha).

## Turning signals into a score band
| Score band | Profile |
|------------|---------|
| **80–100** | EOL OS + many unpatched critical CVEs + poor operational health. Urgent. Usually Retire or Refactor. |
| **60–79** | Outdated tech and real problems, but salvageable value. Usually Refactor or Replatform. |
| **40–59** | Aging but functional; supported or near-supported. Usually Replatform, Replace, or Rehost. |
| **20–39** | Mostly healthy, minor concerns. Usually Rehost or Retain. |
| **0–19** | Modern, secure, healthy. Usually Retain. |

## The key principle
**The score measures urgency, not the decision.** Two apps can both score 85 and get *different* decisions — one Retire (low value), one Refactor (strategic value). The score tells you *how loudly the app is asking for attention*; the business context tells you *what to do about it*. Always pair the score with the value judgement.

## Keywords for matching
risk score, readiness score, scoring rubric, obsolescence, security posture, CVE severity, operational health, MTTR, availability, incidents, criticality, urgency, score band, how to score, 0-100
