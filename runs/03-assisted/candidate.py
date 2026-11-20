def admit(key, residents, recent):
    if len(residents) < 16:
        return True
    return key in recent
