def clamp(n, smallest, largest):
    """Clamp a value within [smallest] and [largest] inclusive"""
    return max(smallest, min(n, largest))
