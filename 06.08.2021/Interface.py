from tkinter import *
import tkinter
from automatExeptions import SetCommandException, NotStrException, SetTextException



class DrinksVendingMachineUI(Tk):      ## glowna klasa interfejsu   
    '''
    Klasa DrinksVendingMachineUI:
    DrinksVendingMachineUI - klasa opisuje interfejs do pracy z automatem z napojami

    Metody:
    configure_money_option(command, options:dict)
    set_command(obj, command, **kwargs)
    set_text(obj, text)
    reset_money_option
    '''

    def __init__(self):    ## konstruktor
        """
        Konstruktor - tworzy obiekt typu DrinksVendingMachineUI, dziedziczy po konstruktorze klasy Tk

        Pola klasy:
        numbers_buttons (lista) - przyciski numeryczne
        goods_list_text (tekst) - lista towarów
        buy_button (button) - przycisk zakupu
        deny_transaction_button (button) - przycisk przerwania transakcji
        money_variable (StringVar) - pole do zmiany nagłówka money_option
        money_option (OptionMenu) - rozwijana lista do rzutu monetą
        screen_label (label) - ekran do prezentacji informacji o zakupie
        money_screen_label (label) - ekran prezentujący informacje o pieniądzach na koncie użytkownika
        """
        super().__init__()
        self.geometry('550x600')
        self.numbers_buttons = [Button(self, text=str(i)) for i in range (10)]    ## generator lista
        for i in range (1, len(self.numbers_buttons)):
            self.numbers_buttons[i].place(x = ((i-1)%3*20), y = ((i-1)//3*30+10))
        self.numbers_buttons[0].place(x = 20, y = 100)
        self.goods_list_text = Text(self)                ## tworzymy pole dla listy towarow
        self.goods_list_text.place(x = 0, y = 140)
        self.buy_button = Button(self, text="Buy")
        self.buy_button.place(x = 10, y = 540)
        self.deny_transaction_button = Button(self, text="Deny transaction")
        self.deny_transaction_button.place(x = 60, y = 540)
        self.money_variable = StringVar(self)
        self.money_variable.set("Add funds")
        self.money_option = OptionMenu(self, self.money_variable, [])
        self.screen_label = Label(text="", bg="black", fg="white")
        self.screen_label.place(x=190, y=95, width=170, height=30)
        self.money_screen_label = Label(text="", bg="black", fg="white")
        self.money_screen_label.place(x=190, y=65, width=170, height=30)


    def configure_money_option(self, command, options:dict):         ## wygląd zewnętrzny listy rozwijanej
        options = list(options.keys())
        self.money_option = OptionMenu(self, self.money_variable, *options, command=command)
        self.money_option.place(x = 190, y = 10, width= 100, height=30)


    def set_command(self, obj, command, **kwargs):    ## laczy obiekt interfejsu i polecenie
        try:
            if obj == self.money_option:
                self.configure_money_option(command, kwargs["options"])
                return        
            else:
                obj.config(command=command)
        except Exception:
            raise SetCommandException(f'Variable object is {type(obj)}, not tkinter!')


    def set_text(self, obj, text):       ## elementy sterujące z obj i przypisz text
        if type(text) != str:
            raise NotStrException(f'Variable \'text\' is {type(text)}, not str!')
        if type(obj) == Text:
            obj.configure(state= 'normal')
            obj.delete(1.0, END)
            obj.insert(1.0, text)
            obj.configure(state= 'disabled')
        elif type(obj) == Label:
            obj.configure(text= text)
        else:
            raise SetTextException(f'Object can be only Text or Label!')
            

    def reset_money_option(self):
        self.money_variable.set("Add funds")