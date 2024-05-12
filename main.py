# main.py

"""
Основной модуль приложения my_wallet.

Этот модуль содержит точку входа в приложение кошелька. Он создает экземпляр класса Application и запускает его.
"""

from app import Application


def main():
    """
    Функция main - точка входа в приложение.

    Создает экземпляр класса Application и запускает его.
    """
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print('\nЗавершение работы.')


if __name__ == '__main__':
    main()