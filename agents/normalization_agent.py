from models.preference import UserPreference


def normalize_preferences(prefs: UserPreference) -> UserPreference:
    """
    Normalize messy LLM output into clean internal rules
    """

    # Normalize priorities
    normalized_priorities = []
    for p in prefs.priorities:
        p_lower = p.lower()

        if "camera" in p_lower:
            normalized_priorities.append("camera")
        elif "battery" in p_lower:
            normalized_priorities.append("battery")
        elif "performance" in p_lower:
            normalized_priorities.append("performance")
        else:
            normalized_priorities.append(p_lower)

    # Normalize brand constraints
    normalized_constraints = []
    for b in prefs.brand_constraints:
        b_lower = b.lower()

        if "no" in b_lower and "china" in b_lower:
            normalized_constraints.append("no_chinese")
        elif "avoid" in b_lower and "china" in b_lower:
            normalized_constraints.append("no_chinese")
        else:
            normalized_constraints.append(b_lower)

    prefs.priorities = list(set(normalized_priorities))
    prefs.brand_constraints = list(set(normalized_constraints))

    return prefs
