from tkinter import Button
import pytest
import json
import os
from Automat import Automat
from Interface import AutomatUI
from automatExeptions import NoGoodsForSelling, SetCommandException, NotStrException, SetTextException


def test_set_text():
    AUI = AutomatUI()
    with pytest.raises(NotStrException):
        AUI.set_text(AUI.screen_label, 123)

def test_set_command():
    a = Automat(AutomatUI())    
    with pytest.raises(SetCommandException):
        a.interface.set_command(12458, lambda: print()) 

def test_no_goods_for_selling():
    a = Automat(AutomatUI())  
    a.code = "h"
    with pytest.raises(NoGoodsForSelling):
        a.buy_button_click()


def test_set_text2():
    a = Automat(AutomatUI())    
    with pytest.raises(SetTextException):
        a.interface.set_text(Button(), "abcdf")

def test_file_not_found_goods():
    a = Automat(AutomatUI())
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
    a = Automat(AutomatUI())
    try:
        with open("money.json", "rt") as fo:
            money = json.load(fo)
        os.remove("money.json")
        with pytest.raises(FileNotFoundError):
            a.can_give_rest()    
    except FileNotFoundError:
        assert False
    finally:
        with open("money.json", "wt") as fo:
            json.dump(money, fo)

def test_money_option_click():
    a = Automat(AutomatUI())
    a.money_option_click("1 cent")
    assert a.credits == 1

def test_money_option_click2():
    a = Automat(AutomatUI())
    a.money_option_click("1 złoty")
    a.money_option_click("20 groszy")
    assert a.credits == 120

def test_put_number():
    a = Automat(AutomatUI())
    a.put_number("5") 
    a.put_number("5")
    assert a.code == "55"



