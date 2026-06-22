# Sample AI PRD Risk Review

> Fictional example. This demonstrates the format and depth of the paid review without exposing client material.

## Verdict

🟡 **Needs confirmation before implementation** · Human review load: medium

The proposal is directionally coherent, but the adoption forecast is unsupported, the primary success metric is not computable as written, and the launch criteria omit a rollback threshold.

## Must-check items

### 🔴 1. Adoption forecast is presented as fact without evidence

**Document claim**

“The feature will increase weekly active usage by 20% in the first month.”

**Risk**

No experiment, comparable launch, user research, or model is cited. The wording converts a target or hypothesis into a forecast. This can distort prioritization and capacity planning.

**Recommended change**

Label this as a hypothesis and record the evidence required to validate it:

> Hypothesis: the feature may increase weekly active usage. Initial target: +5% to +10%, subject to experiment design and baseline confirmation.

**Human decision required**

Who owns the target, and what evidence justifies the range?

### 🔴 2. Success metric has no denominator or time window

**Document claim**

“Success means 30% activation.”

**Risk**

It is unclear whether activation means all registered users, eligible users, exposed users, or users who started onboarding. The measurement window is also missing.

**Recommended definition**

> Activation rate = eligible new users who complete setup within 7 days / eligible new users exposed to the onboarding flow.

**Human decision required**

Confirm eligibility rules, exposure logging, and the seven-day window.

### 🟡 3. Launch plan has no rollback criterion

**Document claim**

“Roll out to 100% after the beta is stable.”

**Risk**

“Stable” is not operational. The team cannot make a consistent go/no-go decision, and incident response may be delayed.

**Recommended change**

Define a minimum observation period plus measurable rollback triggers, such as error rate, support-contact rate, or task-completion degradation.

### 🟡 4. Privacy dependency is acknowledged but has no owner

The document says legal/privacy review is required, but gives no owner, deadline, or artifact. Add an accountable owner and make approval a launch prerequisite.

## Lower-risk notes

- The user problem and proposed workflow are internally consistent.
- The non-goals section is clear.
- Copy details can be finalized after the metric and rollout decisions; they do not block approval.

## Decision checklist

- [ ] Reclassify the 20% usage increase as a hypothesis or support it with evidence
- [ ] Approve a computable activation metric
- [ ] Define rollback thresholds and observation period
- [ ] Assign an owner and deadline for privacy review
