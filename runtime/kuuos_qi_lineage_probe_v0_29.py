VERSION = "kuuos_qi_candidate_lineage_v0_29"


def lineage_probe() -> dict[str, object]:
    return {
        "version": VERSION,
        "finite": True,
        "review_only": True,
        "automatic_action": False,
    }


__all__ = ["VERSION", "lineage_probe"]
