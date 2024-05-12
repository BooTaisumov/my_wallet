# storage.py

"""
Модуль, содержащий класс Storage для работы с файловым хранилищем данных.
"""

import os
import warnings
import pandas as pd


# Отключаем предупреждения FutureWarning для библиотеки pandas.
warnings.simplefilter(action='ignore', category=FutureWarning)


class Storage:
    """
    Класс для работы с файловым хранилищем данных.
    """

    def __init__(self, file_path: str = '__storage.csv') -> None:
        """
        Инициализируем экземпляр класса Storage.

        :param file_path: Путь к файлу хранилища данных.

        Если файл не существует, создаем новый файл.
        """
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            # Создаем пустой DataFrame с нужными колонками.
            empty_df = pd.DataFrame(columns=['date', 'category', 'amount', 'description'])
            # Записываем пустой DataFrame с колонками в файл в формате CSV.
            empty_df.to_csv(self.file_path, sep=";", index=False)

    def to_write(self, entries: pd.DataFrame) -> None:
        """
        Записывает данные из entries: pd.DataFrame в файл.

        :param entries: Обновленный DataFrame
        """

        entries.to_csv(self.file_path, sep=";", index=False)

    def read_entries(self) -> pd.DataFrame:
        """
        Читаем содержимое файла хранилища и возвращаем его в виде DataFrame.

        :return: DataFrame со всеми записями.
        """
        return pd.read_csv(self.file_path, sep=";")


