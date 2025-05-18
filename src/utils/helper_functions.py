import re


def check_coordinates(data):
    try:
        lat = float(data["latitude"])
        lng = float(data["longitude"])
    except (KeyError, ValueError, TypeError):
        return False, "Latitude and longitude must be valid numbers"

    if not (-90 <= lat <= 90):
        return False, "Latitude must be between -90 and 90"
    if not (-180 <= lng <= 180):
        return False, "Longitude must be between -180 and 180"

    return True, None

def check_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
