from django.core.exceptions import ValidationError


def percent_validator(value: float):

    """Percent can be in range 0.1, 100"""

    if value < 0.1:
        ValidationError(
            'Discount percentage cannot be lower than 0.1'
        )
    elif value > 100:
        ValidationError(
            'Discount percentage cannot be higher than 100'
        )
