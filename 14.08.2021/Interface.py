from tkinter import *
from automatExeptions import TypeObjectException



def set_text(obj, text):       ## elementy sterujące z obj i przypisz text
    """
    Ustawia tekst na kontrolki

    Argumenty:
    obj () - element sterujący
    text (str) - tekst do napisania do kontrolki
    """
    if type(text) != str:
        raise TypeObjectException(f'Variable \'text\' is {type(text)}, not str!')
    if type(obj) == Text:
        obj.configure(state= 'normal')
        obj.delete(1.0, END)
        obj.insert(1.0, text)
        obj.configure(state= 'disabled')
    elif type(obj) == Label:
        obj.configure(text= text)
    else:
        raise TypeObjectException(f'Object can be only Text or Label!')


class DrinksVendingMachineUI(Tk):     ## glowna klasa interfejsu  

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
        __money_variable__ (StringVar) - pole do zmiany nagłówka money_option
        money_option (OptionMenu) - rozwijana lista do rzutu monetą
        __screen_label__ (label) - ekran do prezentacji informacji o zakupie
        __money_screen_label__ (label) - ekran prezentujący informacje o pieniądzach na koncie użytkownika
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
        self.__money_variable__ = StringVar(self)
        self.__money_variable__.set("Add funds")
        self.money_option = OptionMenu(self, self.__money_variable__, [])
        self.__screen_label__ = Label(text="", bg="black", fg="white")
        self.__screen_label__.place(x=190, y=95, width=170, height=30)
        self.__money_screen_label__ = Label(text="", bg="black", fg="white")
        self.__money_screen_label__.place(x=190, y=65, width=170, height=30)

    def configure_money_option(self, command, options:dict):         ## wygląd zewnętrzny listy rozwijanej
        """
        Zmienia wygląd money_option

        Argumenty:
        command () - moduł obsługi zdarzenia kliknięcia na money_option
        options (dict) - wybory z listy rozwijanej
        """
        options = list(options.keys())
        self.money_option = OptionMenu(self, self.__money_variable__, *options, command=command)
        self.money_option.place(x = 190, y = 10, width= 100, height=30)


    def set_command(self, obj, command, **kwargs):    ## laczy obiekt interfejsu i polecenie
        """
        Ustawia obsługę zdarzeń dla kontrolek

        Argumenty:
        obj () - element sterujący
        command () - obsługa zdarzeń
        kwargs (dict) - wypełnienie listy rozwijanej
        """
        try:
            if obj == self.money_option:
                self.configure_money_option(command, kwargs["options"])
                return        
            else:
                obj.config(command=command)
        except Exception:
            raise TypeObjectException(f'Variable object is {type(obj)}, not tkinter!')
            

    def reset_money_option(self):
        """
	Pisze Add funds na górę listy po każdym wyborze z money_option
        """
        self.__money_variable__.set("Add funds")