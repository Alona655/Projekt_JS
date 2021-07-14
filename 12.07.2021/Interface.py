from tkinter import *


class AutomatUI (Tk):      ## glowna klasa interfejsu
    def __init__(self):    ## konstruktor
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
        self.money_option = OptionMenu(self, StringVar(self), [])
        self.screen_label = Label(text="", bg="black", fg="white")
        self.screen_label.place(x=190, y=95, width=100, height=30)
        self.money_screen_label = Label(text="", bg="black", fg="white")
        self.money_screen_label.place(x=190, y=70, width=100, height=30)

    def configure_money_option(self, command, option):
        variable = StringVar(self)
        self.money_option = OptionMenu(self, variable, *option, command=command)
        self.money_option.place(x = 190, y = 10, width= 100, height=30)

    def set_command(self, obj, command, **kwargs):    ## laczy obiekt interfejsu i polecenie
        if obj == self.money_option:
            self.configure_money_option(command, kwargs["options"])
            return        
        obj["command"] = command

    def set_text(self, obj, text):
        if type(obj) == Text:
            obj.configure(state= 'normal')
            obj.delete(1.0, END)
            obj.insert(1.0, text)
            obj.configure(state= 'disabled')
        elif type(obj) == Label:
            obj.configure(text= text)

        



