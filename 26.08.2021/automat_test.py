"""
Testy sprawdzające działanie automatu z napojami
"""

from tkinter import Button
import pytest
import json
import os
from DrinksVendingMachine import DrinksVendingMachine
from Interface import DrinksVendingMachineUI, set_text
from automatExeptions import InsufficientFunds, NoGoodsForSelling, ProductIsNotAvailable, NotStrException 
from automatExeptions import TypeObjectException, NoProductWithThisCode


## 1. Sprawdzenie ceny jednego towaru - oczekiwana informacja o cenie.
def test_put_number():
    with open("goods.json", "rt") as fo:
        goods = json.load(fo)
    real_result = ""
    real_result += str(goods["30"]["price"]/100)
    expected_result = "2.60"   
    assert real_result == expected_result


## 2. Wrzucenie odliczonej kwoty, zakup towaru - oczekiwany brak reszty.
def test_buying_stuff():
    with open("goods.json", "rt") as fo:
        goods = json.load(fo)
    a = DrinksVendingMachine(DrinksVendingMachineUI())
    a.money_option_click("1 usd")
    a.money_option_click("20 cents")
    expected_result = goods["42"]["count"]
    a.put_number(4)
    a.put_number(2)
    a.buy_button_click()
    with open("goods.json", "rt") as fo:
        goods = json.load(fo)
    expected_result -= 1
    real_result = goods["42"]["count"]
    assert real_result == expected_result and a.credits == 0


## 3. Wrzucenie większej kwoty, zakup towaru - oczekiwana reszta.
def test_give_rest():
    with open("goods.json", "rt") as fo:
        goods = json.load(fo)
    a = DrinksVendingMachine(DrinksVendingMachineUI())
    a.money_option_click("1 usd")
    a.money_option_click("1 usd")
    expected_result_rest = 80
    expected_result_count = goods["37"]["count"]
    a.put_number(3)
    a.put_number(7)
    a.buy_button_click()
    with open("goods.json", "rt") as fo:
        goods = json.load(fo)
    expected_result_count -= 1
    real_result_count = goods["37"]["count"]
    assert a.credits == expected_result_rest and expected_result_count == real_result_count

## 4. Wykupienie całego asortymentu, próba zakupu po wyczerpaniu towaru - oczekiwana informacja o braku.
def test_buying_all_stuff():
    with open("goods.json", "rt") as fo:
        goods = json.load(fo)
    a = DrinksVendingMachine(DrinksVendingMachineUI())
    for i in range(goods["31"]["count"]):
        a.code = "31"
        a.credits = goods["31"]["price"]
        a.buy_button_click()
    with pytest.raises(ProductIsNotAvailable):
        a.put_number("3") 
        a.put_number("1")


## 5. Sprawdzenie ceny towaru o nieprawidłowym numerze (<30 lub >50) - oczekiwana informacja o błędzie.
def test_not_included_in_the_limit():
    a = DrinksVendingMachine(DrinksVendingMachineUI())  
    a.put_number(8)
    with pytest.raises(NoProductWithThisCode):
        a.put_number(4)

## 6. Wrzucenie kilku monet, przerwanie transakcji - oczekiwany zwrot monet.
def test_deny_transaction():
    a = DrinksVendingMachine(DrinksVendingMachineUI())  
    a.money_option_click("50 groszy")
    a.money_option_click("5 groszy")
    a.deny_transaction_button_click()
    assert a.credits == 0


## 7. Wrzucenie za małej kwoty, wybranie poprawnego numeru towaru, wrzucenie reszty monet do odliczonej kwoty, ponowne wybranie poprawnego numeru towaru 
## - oczekiwany brak reszty.
def test_purchase_with_added_money():
    a = DrinksVendingMachine(DrinksVendingMachineUI())  
    with open("goods.json", "rt") as fo:
        goods = json.load(fo)
    expected_result_count = goods["32"]["count"]
    a.put_number(3) 
    a.put_number(2)
    a.money_option_click("20 groszy")
    a.money_option_click("1 złoty")
    with pytest.raises(InsufficientFunds):
        a.buy_button_click()
    a.money_option_click("50 groszy")
    a.money_option_click("20 groszy")
    a.money_option_click("10 groszy")
    a.put_number(3) 
    a.put_number(2)
    a.buy_button_click()
    with open("goods.json", "rt") as fo:
        goods = json.load(fo)
    expected_result_count -= 1
    real_result_count = goods["32"]["count"]
    assert real_result_count == expected_result_count and a.credits == 0



## 8. Zakup towaru płacąc po 1 gr - suma stu monet ma być równa 1 zł
def test_add_one_cent():
    a = DrinksVendingMachine(DrinksVendingMachineUI())  
    for i in range(100):
        a.money_option_click("1 grosz")
    a.put_number(3)
    a.put_number(8)
    a.buy_button_click()
    assert a.credits == 0

		### Dodatkowe testy

def test_set_text():
    """
    Sprawdzanie generowania NotStrException
    """
    AUI = DrinksVendingMachineUI()
    with pytest.raises(NotStrException):
        set_text(AUI.screen_label, 123)


def test_set_command():
    """
    Sprawdzanie generowania TypeObjectException
    """
    a = DrinksVendingMachine(DrinksVendingMachineUI())    
    with pytest.raises(TypeObjectException):
        a.interface.set_command(12458, lambda: print()) 


def test_no_goods_for_selling():
    """
    Sprawdzanie generowania NoGoodsForSelling
    """
    a = DrinksVendingMachine(DrinksVendingMachineUI())  
    a.put_number("h")
    with pytest.raises(NoGoodsForSelling):
        a.buy_button_click()


def test_set_text2():
    """
    Sprawdzanie generowania TypeObjectException
    """   
    with pytest.raises(TypeObjectException):
        set_text(Button(), "abcdf")


def test_file_not_found_goods():
    """
    Sprawdzanie działania klasy bez pliku towarów
    """
    a = DrinksVendingMachine(DrinksVendingMachineUI())
    try:
        with open("goods.json", "rt") as fo:
            goods = json.load(fo)
        os.remove("goods.json")
        with pytest.raises(FileNotFoundError):
            a.fill_goods()    
    except FileNotFoundError:
        assert False
    finally:
        with open("goods.json", "wt") as fo:
            json.dump(goods, fo)

        
def test_file_not_found_money():
    """
    Sprawdzanie działania klasy bez pliku z monetami
    """
    a = DrinksVendingMachine(DrinksVendingMachineUI())
    try:
        with open("money.json", "rt") as fo:
            money = json.load(fo)
        os.remove("money.json")
        with pytest.raises(FileNotFoundError):
            a.can_give_rest(10)    
    except FileNotFoundError:
        assert False
    finally:
        with open("money.json", "wt") as fo:
            json.dump(money, fo)


def test_money_option_click():
    """
    Sprawdzanie prawidłowego wrzucania pieniędzy
    """
    a = DrinksVendingMachine(DrinksVendingMachineUI())
    a.money_option_click("1 grosz")
    assert a.credits == 1


def test_money_option_click2():
    """
    Sprawdzanie prawidłowego wrzucania pieniędzy
    """
    a = DrinksVendingMachine(DrinksVendingMachineUI())
    a.money_option_click("1 złoty")
    a.money_option_click("20 groszy")
    assert a.credits == 120

def test_put_number():
    """
    Sprawdzanie wyboru produktu
    """
    a = DrinksVendingMachine(DrinksVendingMachineUI())
    a.put_number("4") 
    a.put_number("5")
    assert a.code == "45"