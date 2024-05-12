# entry.py

"""
Модуль, содержащий определение класса Entry для представления записей в хранилище.
"""

from datetime import date
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
from colorama import init, Fore

init(autoreset=True)


class Entry(BaseModel):
    """
    Класс для представления записей в хранилище.

    Каждая запись содержит дату, категорию, сумму и описание операции.
    """

    date: date
    category: str
    amount: float
    description: str

    # noinspection PyNestedDecorators
    @field_validator('date', mode='before')
    @classmethod
    def is_correct_date(cls, value):
        """
        Валидатор для проверки корректности формата даты.

        Проверяет, соответствует ли значение даты формату гггг-мм-дд.
        """
        if value == '': return date.today()

        try:
            converted_value = date.fromisoformat(value)
        except ValueError as _ex:
            if _ex.args[0] == 'month must be in 1..12':
                _ex.args = ('Месяц должен быть в пределах 1..12',)

            if _ex.args[0] == 'day is out of range for month':
                _ex.args = ('День выходит за пределы допустимых значений для данного месяца',)

            if 'Invalid isoformat string' in _ex.args[0]:
                _ex.args = ('Не соответствует формату гггг-мм-дд - "isoformat"',)

            raise PydanticCustomError('date_from_datetime_parsing', Fore.LIGHTRED_EX + f'Дата >>> {_ex.args[0]}')
        else:
            error_type = 'date_from_datetime_parsing'
            template = Fore.LIGHTRED_EX + f'Дата >>> Дата не должна быть больше текущего дня'
            if converted_value > date.today(): raise PydanticCustomError(error_type, template)
            return converted_value

    # noinspection PyNestedDecorators
    @field_validator('amount', mode='before')
    @classmethod
    def is_correct_amount(cls, value):
        """
        Валидатор для проверки корректности формата суммы.

        Проверяет, что значение может быть преобразовано в число и что оно больше нуля.
        """

        try:
            converted_value = float(value)
        except ValueError as _ex:
            error_type = 'float_parsing'
            template = Fore.LIGHTRED_EX + 'Сумма >>> Введенное значение должно быть числом, введено: "[{wrong_value}]"'
            context = dict(wrong_value=value)
            raise PydanticCustomError(error_type, template, context)
        else:
            error_type = 'greate_then'
            template = Fore.LIGHTRED_EX + 'Сумма >>> Введенное число должно быть больше нуля, введено:: {wrong_value}'
            context = dict(wrong_value=value)
            if converted_value <= 0: raise PydanticCustomError(error_type, template, context)
            return converted_value
