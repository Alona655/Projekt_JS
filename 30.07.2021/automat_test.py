import pytest
from Automat import Automat
from Interface import AutomatUI
from automatExeptions import NotObjectException, NotStrException


def test_set_text():
    AUI = AutomatUI()
    with pytest.raises(NotStrException):
        AUI.set_text(AUI.screen_label, 123)

'''
def test_set_command():
    a = Automat(AutomatUI())    
    with pytest.raises(NotObjectException):
        a.interface.set_command("12458", len("12458")) 
'''


def test_money_option_click():
    a = Automat(AutomatUI())
    a.money_option_click("1 cent")
    assert a.credits == 1

def test_money_option_click2():
    a = Automat(AutomatUI())
    a.money_option_click("1 usd")
    a.money_option_click("20 cents")
    assert a.credits == 120

def test_put_number():
    a = Automat(AutomatUI())
    a.put_number("5") 
    a.put_number("5")
    assert a.code == "55"



