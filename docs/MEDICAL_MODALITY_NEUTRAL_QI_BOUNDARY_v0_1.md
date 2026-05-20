# Medical-Modality-Neutral Qi Boundary v0.1

## Purpose

This document clarifies how KuuOS describes the medical boundary around Qi motion validation.

The boundary is medical-modality neutral.

It does not state that biomedicine is superior.
It does not state that Qi is false.
It does not state that East Asian medical reasoning is invalid.
It does not reduce Qi, pattern differentiation, or practitioner judgment to a Western biomedical-only frame.

## Core clarification

KuuOS separates three surfaces:

```text
Qi observation / Qi motion candidate
  != standalone diagnosis
  != standalone treatment authorization
  != medical act authorization
```

This means only that repository validators, CI checks, and public governance files do not by themselves authorize diagnosis, treatment decisions, procedures, prescriptions, institutional care pathways, or medical acts.

## What Qi motion validation may support

Qi motion validation may support:

```text
structured observation
pattern-sensitive reasoning
candidate generation
traceable explanation
evidence-bounded review
professional reflection
East Asian medical reasoning support
integrative reasoning support
```

## What Qi motion validation must not claim by itself

Qi motion validation must not be treated by itself as:

```text
standalone diagnosis authority
standalone treatment authorization
medical act authorization
execution authority
institutional approval
theorem authority
replacement for practitioner judgment
replacement for patient context
```

## Preferred wording

Prefer:

```text
Qi motion validation alone is not standalone diagnosis, standalone treatment authorization, or medical act authorization.
```

Avoid:

```text
Qi motion validation does not grant clinical authority.
```

The avoided wording can be misread as implying that only biomedicine is clinically valid or that Qi is non-clinical. That is not the KuuOS position.

## Governance rule

When medical language is used around Qi, KuuOS should preserve:

```text
medical_modality_neutrality
qi_not_false_by_boundary
biomedicine_not_privileged_by_wording
professional_judgment_required
patient_context_required
validator_not_medical_act_authority
```

## Interpretation

KuuOS does not deny Qi.

KuuOS does not deny East Asian medicine.

KuuOS only prevents repository validation, CI pass, and runtime candidate generation from being mistaken for a complete professional diagnosis, treatment decision, or medical act authorization.