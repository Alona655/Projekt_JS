from tkinter import *
from pygame import mixer
from automatExeptions import TypeObjectException, NotStrException



def set_text(obj, text:str):       ## elementy sterujące z obj i przypisanie text 
    """
    Ustawia tekst na kontrolki

    Argumenty:
    obj () - element sterujący
    text (str) - tekst do napisania do kontrolki
    """
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
        raise TypeObjectException(f'Object can be only Text or Label!')


def play_sound(sound:str):
    """
    Odtwarza dźwięk

    sound (str) - ścieżka do pliku z dźwiękiem
    """
    mixer.init()
    mixer.music.load(sound)
    mixer.music.play()


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
        __numbers_buttons (lista) - przyciski numeryczne
        __goods_list_text (tekst) - lista towarów
        __buy_button (button) - przycisk zakupu
        __deny_transaction_button (button) - przycisk przerwania transakcji
        __money_variable (StringVar) - pole do zmiany nagłówka __money_option
        __money_option (OptionMenu) - rozwijana lista do rzutu monety
        __screen_label (label) - ekran do prezentacji informacji o zakupie
        __money_screen_label (label) - ekran prezentujący informacje o pieniądzach na koncie użytkownika
        """
        super().__init__()
        self.geometry('600x400')
        self.__numbers_buttons = [Button(self, text=str(i), bg="blue", fg="black", font= ("Times New Roman", "15", "bold")) for i in range (10)]    ## generator lista
        for i in range (1, len(self.__numbers_buttons)):
            self.__numbers_buttons[i].place(x = ((i-1)%3*35 + 430), y = ((i-1)//3*35 + 125), width=30, height=30)
        self.__numbers_buttons[0].place(x = (35 + 430), y = 230, width=30, height=30)
        self.__goods_list_text = Text(self)             										   ## tworzymy pole dla listy towarow
        self.__goods_list_text.place(x = 0, y = 0, width=380, height=400)
        self.__buy_button = Button(self, text="Buy", bg="green", fg="black", font= ("Times New Roman", "15", "bold"))
        self.__buy_button.place(x = 400, y = 300, width=60, height=60)
        self.__deny_transaction_button = Button(self, text="Deny\ntransaction", bg="red", fg="black", font= ("Times New Roman", "15", "bold"))
        self.__deny_transaction_button.place(x = 490, y = 300, width=100, height=60)
        self.__money_variable = StringVar(self)
        self.__money_variable.set("Add funds")
        self.__money_option = OptionMenu(self, self.__money_variable, [])
        self.__screen_label = Label(text="", bg="black", fg="white")
        self.__screen_label.place(x=400, y=90, width=170, height=30)
        self.__money_screen_label = Label(text="", bg="black", fg="white")
        self.__money_screen_label.place(x=400, y=60, width=170, height=30)


    """
    Dekorator, zwraca wartość atrybutu

    Returns:
    Atrybut
    """
    @property
    def numbers_buttons(self):
        return self.__numbers_buttons

    @property
    def goods_list_text(self):
        return self.__goods_list_text

    @property
    def buy_button(self):
        return self.__buy_button

    @property
    def deny_transaction_button(self):
        return self.__deny_transaction_button

    @property
    def money_variable(self):
        return self.__money_variable

    @property
    def money_option(self):
        return self.__money_option

    @property
    def screen_label(self):
        return self.__screen_label

    @property
    def money_screen_label(self):
        return self.__money_screen_label


    def configure_money_option(self, command, options:dict):         ## wygląd zewnętrzny listy rozwijanej
        """
        Zmienia wygląd __money_option

        Argumenty:
        command () - moduł obsługi zdarzenia kliknięcia na __money_option
        options (dict) - wybory z listy rozwijanej
        """
        options = list(options.keys())
        self.__money_option = OptionMenu(self, self.__money_variable, *options, command=command)
        self.__money_option.place(x = 420, y = 10, width= 100, height=30)


    def set_command(self, obj, command, **kwargs):    ## lączy obiekt interfejsu i polecenie
        """
        Ustawia obsługę zdarzeń dla kontrolek

        Argumenty:
        obj () - element sterujący
        command () - element sterujący
        kwargs (dict) - wypełnienie listy rozwijanej
        """
        try:
            if obj == self.__money_option:
                self.configure_money_option(command, kwargs["options"])
                return        
            else:
                obj.config(command=command)
        except Exception:
            raise TypeObjectException(f'Variable object is {type(obj)}, not tkinter!')
            

    def reset_money_option(self):
        """
        Zapisuję Add funds na górę listy po każdym wyborze z __money_option
        """
        self.__money_variable.set("Add funds")