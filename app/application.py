import pandas as pd
from pydantic import ValidationError
from colorama import init, Fore, Style

from .storage import Storage
from .wallet import Wallet

init(autoreset=True)

BUTTON_BALANCE = f'[1] Остаток на счете'
BUTTON_HISTORY = f'[2] История операций'
BUTTON_CREATE_ENTRY = f'[3] Создать запись'
BUTTON_REMOVE_ENTRY = f'[4] Удалить запись'
BUTTON_QUIT = f'[0] Выход'

BUTTON_INCOME = '[1] Доходы'
BUTTON_EXPENSE = '[2] Расходы'
BUTTON_BACK = '[0] Вернуться в главное меню'


class Application:
    category_menu = {
        BUTTON_INCOME: 'Доходы',
        BUTTON_EXPENSE: 'Расходы',
        BUTTON_BACK: None
    }

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        cls.mainmenu = {
            BUTTON_BALANCE: instance.display_balance,
            BUTTON_HISTORY: instance.display_history,
            BUTTON_CREATE_ENTRY: instance.create_entry,
            BUTTON_REMOVE_ENTRY: instance.remove_entry,
            BUTTON_QUIT: None
        }

        return instance

    def __init__(self):
        self.storage = Storage()
        self.wallet = Wallet(self.storage)

    def run(self):
        print('Добро пожаловать!!!')

        while True:
            print('\n>>> Главное меню')
            mainmenu_buttons: list = list(self.mainmenu.keys())
            self.show_menu(mainmenu_buttons)

            try:
                choice = int(input(f'{Fore.LIGHTBLUE_EX}Выберите пункт::: {Style.RESET_ALL}'))
                choice = mainmenu_buttons[choice - 1]

                option = self.mainmenu[choice]
                if option is None: break
                option()

            except (ValueError, IndexError):
                print(f'{Fore.LIGHTRED_EX}Введенное значение некорректно.')

    @staticmethod
    def show_menu(menu) -> None:
        max_size_option = max(menu, key=lambda item: len(item))
        temp: int = len(max_size_option)
        print('#' * temp, *menu, '#' * temp, sep='\n')

    def display_balance(self):
        balance = self.wallet.calculate_balance()
        print(f'\n>>> {BUTTON_BALANCE.split(maxsplit=1)[1]}: {Fore.LIGHTGREEN_EX}{balance}')

    def display_history(self):
        print(f'\n>>> {BUTTON_HISTORY.split(maxsplit=1)[1]}')
        entries = self.wallet.get_entries()

        print(
            f'{Fore.LIGHTRED_EX}На данный момент история отсутствует.'
            if entries.empty else
            f'{Fore.LIGHTGREEN_EX}{entries}'
        )

    def create_entry(self):
        while True:
            print(f'\n>>> {BUTTON_CREATE_ENTRY.split(maxsplit=1)[1]}')
            categories_buttons: list = list(self.category_menu.keys())
            self.show_menu(categories_buttons)

            try:
                choice: int = int(input(f'{Fore.LIGHTBLUE_EX}Выберите категорию::: {Style.RESET_ALL}'))
                choice: str = categories_buttons[choice - 1]

                category = self.category_menu[choice]
                if category is None: break
                print(f'\n>>> {choice.split(maxsplit=1)[1]}')
                print('Для выбора текущей даты [ ↵]')

                data = {
                    'date': input(f'{Fore.LIGHTBLUE_EX}Укажите дату (гггг-мм-дд)::: {Style.RESET_ALL}'),
                    'category': category,
                    'amount': input(f'{Fore.LIGHTBLUE_EX}Укажите сумму::: {Style.RESET_ALL}'),
                    'description': input(f'{Fore.LIGHTBLUE_EX}Введите описание::: {Style.RESET_ALL}').capitalize()
                }

                try:
                    self.wallet.add_entry(data)
                except ValidationError as _ex:
                    print(*[item['msg'] for item in _ex.errors()], sep='\n')
                else:
                    choice: str = input(
                        f'{Fore.LIGHTGREEN_EX}Операция выполнена.{Style.RESET_ALL}\n'
                        f'{Fore.LIGHTBLUE_EX}Продолжить [д/н]? {Style.RESET_ALL}')
                    if choice.upper() != 'Д': break

            except (ValueError, IndexError):
                print(f'{Fore.LIGHTRED_EX}Введенное значение некорректно.')

    def remove_entry(self):
        while True:
            print(f'\n>>> {BUTTON_REMOVE_ENTRY.split(maxsplit=1)[1]}')
            entries = self.wallet.get_entries()
            print(
                f'{Fore.LIGHTRED_EX}На данный момент история отсутствует.'
                if entries.empty else
                f'{Fore.LIGHTGREEN_EX}{entries}'
            )

            if entries.empty: break

            try:
                print("Для возврата в главное меню используйте [пробел]")
                index = int(input(f'{Fore.LIGHTBLUE_EX}Введите индекс строки::: {Style.RESET_ALL}'))
                self.wallet.remove_row(index)
            except (KeyError, ValueError) as _ex:
                if ": ' '" in _ex.args[0]: break
                print(f'{Fore.LIGHTRED_EX}Введенное значение некорректно.')
            else:
                choice: str = input(
                    f'{Fore.LIGHTGREEN_EX}Операция выполнена.{Style.RESET_ALL}\n'
                    f'{Fore.LIGHTBLUE_EX}Продолжить [д/н]? {Style.RESET_ALL}')
                if choice.upper() != 'Д': break

