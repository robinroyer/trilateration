EARTH_RADIUS = 6378100.0
SPEED_OF_LIGHT = .2997924580 # meter/ns.second

def is_number(to_test):
    """Check if an object is float, int or long.

    Args:
        object to test

    Returns:
        True if is is as float, int or long, False otherwise

    """
    return isinstance(to_test, float) \
        or isinstance(to_test, int) \
        or isinstance(to_test, long)