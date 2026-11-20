def admit(key, residents, recent):
    return len(residents) < 16 or key in recent
