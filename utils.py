def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min(value, max_value), min_value)


def sign(a: float) -> float:
    return 1 if a > 0 else -1 if a < 0 else 0


def step(edge: float, x: float) -> float:
    return x > edge
