import re

def validate_wo_number(wo_number):
    wo_number = wo_number.upper()  # Convert to uppercase for consistent validation
    pattern = r"^[A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{5}$"
    if not wo_number.strip():
        return False, "WO Number cannot be empty."
    
    if not re.match(pattern, wo_number):
        return False, "WO Number is not in the correct format."

    return True, ""

 