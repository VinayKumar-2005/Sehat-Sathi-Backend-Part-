import re

def validate_health_data(data):
    errors = []
    
    # 1. Age Validation
    age = data.get('age')
    if not age or not isinstance(age, (int, float)):
        errors.append("Age is required and must be a number.")
    elif age < 5 or age > 120:
        errors.append("Age must be between 5 and 120.")

    # 2. BP Validation (Format: 120/80)
    bp = data.get('bp')
    if bp:
        if not re.match(r'^\d{2,3}/\d{2,3}$', bp):
            errors.append("BP format must be like '120/80'.")
        else:
            sys, dia = map(int, bp.split('/'))
            if sys > 300 or dia > 200:
                errors.append("BP values seem medically impossible.")

    # 3. Weight/Height
    weight = data.get('weight')
    if weight and (weight < 2 or weight > 500):
        errors.append("Weight seems invalid (2kg - 500kg allowed).")

    return errors