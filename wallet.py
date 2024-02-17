"""
Создание шаблона электронного кошелька,
Реализация 'Обыкновенной' карты (Card): при списании не возвращаются проценты, при balance < 0 будет отказано в переводе,
Реализация 'Продвинутой' карты (ProCard): при списании возвращается 5% от транша, при balance < 0 будет отказано в переводе,
Реализация 'Кредитной' карты (CreditCard): при списании не возвращаются проценты, возможно списание до лимита (-1000 от нулевого баланса).
"""

from abc import ABC # Ограничение использования класса Wallet для создания объектов

class Wallet(ABC):
    """Кошелёк"""
    def __init__(self, name: str, type: str = "General"):
        self.balance: int = 0 # баланс
        self.name: str = name # имя владельца карты
        self.type: str = type # тип кошелька

    def get_balance(self) -> int:
        """Геттер, возвращающий баланс"""
        return self.balance

    def change_balance(self, value: int):
        """Применяем balance к value (положительное или отрицательное число, в зависимости от поступления/списания средств)"""
        if self.balance + value < 0:
            print(f"Недостаточно средств, отказано")
        else:
            self.balance += value # изменение баланса


class CardBalance:
    """Изменение состояния баланса обычной карты"""
    def change_type(self):
        return card
class ProBalance:
    """Изменение состояния баланса PRO-карты"""
    def change_balance(self, value: int):
        if self.balance + value * 0.95 < 0:  # скидка пользователю
            print(f"Недостаточно средств, отказано")
        else:
            self.balance += value * 0.95 if self.balance + value * 0.95 < self.balance else value  # пользователю ПРО возвращается 5% от списанных средств
class CreditBalance:
    """Изменение состояния баланса кредитной карты"""
    def change_balance(self, value: int):
        """Проверка возможности выходить ниже нуля до limit"""
        if self.balance + value < self.limit: # отрицаительное значение приведёт к минусу в операции с value
            print(f"Недостаточно средств, отказано")
        else:
            self.balance += value


class Card(CardBalance, Wallet):
    """Обыкновенная карта"""
    def __init__(self,name):
        super().__init__(name) # метод super(). позволяет вызвать метод __init__ родителя нашего класса (Wallet)

class ProCard(ProBalance, Wallet):
    """Продвинутая карта"""
    def __init__(self, name, type="PRO"):
        super().__init__(name, type)

class CreditCard(CreditBalance, Wallet):
    """Кредитная карта"""
    def __init__(self, name, limit=-1000, type="Credit"):
        self.limit = limit
        super().__init__(name, type)


if __name__ == "__main__":

    tranche_1 = 1000 # первый транш
    tranche_2 = 800 # второй транш
    tranche_3 = 250 # третий транш

    card = Card("Connor") # проценты не начисляются, будет отказано в списании при балансе < 0
    # card = ProCard("Connor") # возвращается 5% с каждого списания, будет отказано в списании при балансе < 0
    # card = CreditCard("Connor") # проценты не начисляются, возможно списание в пределах лимита (до 1201$, учитывая проценты).

    print(f"Ваш баланс: {round(card.get_balance(), 2)}$")
    print(f"~~~ Зачислено +{round(tranche_1, 2)}$")
    card.change_balance(+tranche_1)
    print(f"Текущий баланс: {round(card.get_balance(), 2)}$")

    print(f"{'-' * 21}")

    print(f"Ваш баланс: {round(card.get_balance(), 2)}$")
    print(f"~~~ Списание в размере -{round(tranche_2, 2)}$")
    card.change_balance(-tranche_2)
    print(f"Текущий баланс: {round(card.get_balance(), 2)}$")

    print(f"{'-' * 21}")

    print(f"Ваш баланс: {round(card.get_balance(), 2)}$")
    print(f"~~~ Списание в размере -{round(tranche_3, 2)}$")
    card.change_balance(-tranche_3)
    print(f"Текущий баланс: {round(card.get_balance(), 2)}$")