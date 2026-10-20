from backend.loan_rules import COMMON_REQUIRED, NUMERIC_FIELDS

def validate(loan_type, data):
    errors = []
    if loan_type not in COMMON_REQUIRED:
        return ["Unsupported loan type."]
    for field in COMMON_REQUIRED[loan_type]:
        if str(data.get(field, "")).strip() == "":
            errors.append(f"{field.replace('_', ' ').capitalize()} is required.")
    for field in NUMERIC_FIELDS:
        value = data.get(field)
        if value in (None, ""):
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            errors.append(f"{field.replace('_', ' ').capitalize()} must be a number.")
            continue
        if number < 0:
            errors.append(f"{field.replace('_', ' ').capitalize()} cannot be negative.")
    if data.get("age") not in (None, ""):
        try:
            age = int(data["age"])
            if age < 18 or age > 100:
                errors.append("Age must be between 18 and 100.")
        except (TypeError, ValueError):
            errors.append("Age must be a whole number.")
    if data.get("tenure_months") not in (None, ""):
        try:
            if int(data["tenure_months"]) <= 0 or int(data["tenure_months"]) > 600:
                errors.append("Tenure must be between 1 and 600 months.")
        except (TypeError, ValueError):
            errors.append("Tenure must be a whole number of months.")
    amount = data.get("requested_amount")
    if amount not in (None, ""):
        try:
            if float(amount) <= 0:
                errors.append("Requested amount must be greater than zero.")
        except (TypeError, ValueError):
            pass
    if loan_type == "home" and data.get("down_payment") not in (None, "") and data.get("property_value") not in (None, ""):
        try:
            if float(data["down_payment"]) > float(data["property_value"]):
                errors.append("Down payment cannot exceed the stated property value.")
        except (TypeError, ValueError):
            pass
    return errors
