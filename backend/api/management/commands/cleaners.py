import random


def random_float(*args, **kwargs) -> float:
    """
    Returns a random floating-point number from a uniform distribution
    in the range 1 to 40.
    """
    return round(random.uniform(1, 40), 2)


def nonzero(value) -> float:
    """
    This function returns the input value if it is not zero, otherwise
    it generates a random float value.
    """
    return value if value else random_float()
