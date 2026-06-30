#!/usr/bin/env python3
from runtime.v106_review_core import (
    review_repository_checkpoint_discrepancy as base_review,
)
from runtime.v106_review_hil import minimize_human_review


def review_repository_checkpoint_discrepancy(*args, **kwargs):
    return minimize_human_review(base_review(*args, **kwargs))
