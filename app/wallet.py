# wallet.py

"""
Модуль, содержащий класс Wallet для работы с данными из хранилища.
"""

import pandas as pd

from app.storage import Storage
from app.entry import Entry

class Wallet:
    """
    Класс для работы с данными из хранилища.
    """

    def __init__(self, storage: Storage):
        """
        Инициализирует экземпляр класса Wallet.

        :param: storage (Storage): Экземпляр класса Storage для доступа к хранилищу данных.
        """

        self.storage = storage

    def add_entry(self, data: dict) -> None:
        """
        Добавляет новую запись операции в хранилище.

        :param: data (dict): Словарь с данными новой записи.
        """

        entries = self.get_entries()
        entry_series = pd.Series(
            Entry(**data).model_dump(),
            index=entries.columns
        )
        # noinspection PyProtectedMember
        entries = entries._append(entry_series, ignore_index=True)
        self.storage.to_write(entries)

    def get_entries(self) -> pd.DataFrame:
        """
        Получает все записи операций из хранилища.

        :return: pandas.DataFrame: DataFrame со всеми записями из хранилища.
        """

        entries = self.storage.read_entries()
        entries['amount'] = entries['amount'].astype('Float64')
        return entries

    def calculate_balance(self) -> float:
        """
        Вычисляет баланс кошелька.

        :return: float: Баланс кошелька (разница между доходами и расходами).
        """

        entries = self.get_entries()
        filter_by_incomes = entries['category'] == 'Доходы'
        incomes = entries[filter_by_incomes]['amount'].sum()

        filter_by_expenses = entries['category'] == 'Расходы'
        expenses = entries[filter_by_expenses]['amount'].sum()

        return incomes - expenses

    def remove_row(self, index: int) -> None:
        """
        Удаляет запись операции из кошелька по индексу.

        :param: index: Индекс записи операции, которую нужно удалить.
        """

        entries = self.get_entries()
        entries = entries.drop(index)
        self.storage.to_write(entries)






