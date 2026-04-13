import re

def create_prefix(serial_number1, serial_number2):

    return

def validate_motor_prefix():

    return

def validate_pump_prefix():

    return

def validate_carton_prefix():

    return

def validate_rating_plate():

    return

def validate_ean_number():

    return

def validate_wip_number(wip_number):
    wip_number = wip_number.upper()  # Convert to uppercase for consistent validation
    pattern = r"^[A-Z0-9]{6}-[A-Z0-9]{4}-[A-Z0-9]{5}[A-Z]{2}[0-9]{5}$"

    if not wip_number.strip():
        return False, "WIP Number cannot be empty."
    
    if not re.match(pattern, wip_number):
        return False, "WIP Number is not in the correct format."
    
    # additional logic to check for duplicates
    
    return True, f"PASS: {wip_number}"

VALIDATORS = {
    'wip_number': validate_wip_number,
    'motor_sn': validate_motor_prefix,
    'pump_sn': validate_pump_prefix,
    'carton_sn': validate_carton_prefix,
    'rating_plate': validate_rating_plate,
    'ean_number': validate_ean_number,
}