#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_reference_update_authorization_v0_96 import (
    authorize_repository_reference_update as _authorize,
    repository_reference_update_authorization_certificate_issues as _issues,
)


def _issue_call(certificate, args, kwargs):
    if args:
        return _issues(certificate, *args[1:], **kwargs)
    issue_kwargs = dict(kwargs)
    issue_kwargs.pop("authorization_id", None)
    return _issues(certificate, **issue_kwargs)


def authorize_repository_reference_update(*args, **kwargs):
    certificate = _authorize(*args, **kwargs)
    issues = _issue_call(certificate, args, kwargs)
    if issues:
        raise ValueError(f"reference_update_certificate_invalid:{issues[0]}")
    return certificate


def repository_reference_update_authorization_certificate_issues(
    certificate, *args, **kwargs
):
    return _issue_call(certificate, args, kwargs)
