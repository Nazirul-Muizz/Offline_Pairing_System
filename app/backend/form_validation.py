import re

def validate_wo_number(wo_number):
    wo_number = wo_number.upper()  # Convert to uppercase for consistent validation
    pattern = r"^[A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{5}$"
    if not wo_number.strip():
        return False, "WO Number cannot be empty."
    
    if not re.match(pattern, wo_number):
        return False, "WO Number is not in the correct format."

    return True, ""

def validate_wo_quantity(wo_quantity):
    if not wo_quantity.strip():
        return False, "Quantity cannot be empty"

    if not wo_quantity.isdigit():
        return False, "Quantity must be a number"

    if int(wo_quantity) <= 0:
        return False, "Quantity must be > 0"
    
    return True, ""

VALIDATORS = {
    'wo_number': validate_wo_number,
    'wo_quantity': validate_wo_quantity,
}

 