#!/usr/bin/env python3

REVIEW_AUTOMATIC = "REPOSITORY_CHECKPOINT_REVIEW_AUTOMATIC"


def human_review_required_for(discrepancy_kind: str) -> bool:
    return discrepancy_kind == "CHECKPOINT_SUBSTITUTED"
