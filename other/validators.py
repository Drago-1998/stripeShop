from django.core.exceptions import ValidationError


def discount_percent_off_validator(value: float):

    """
    Это функция валидатор для проверки правелносты фильтров
    :param value:
    :return:
    """

    if value < 0.1:
        ValidationError(
            'Discount percentage cannot be lower than 0.1'
        )
    elif value > 100:
        ValidationError(
            'Discount percentage cannot be higher than 100'
        )