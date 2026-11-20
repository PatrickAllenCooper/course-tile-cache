"""Scan-resistant admission for a 16-entry LRU tile cache."""


def admit(key, residents, recent):
    """Admit freely while filling, then require a recent prior request."""
    return len(residents) < 16 or key in recent
