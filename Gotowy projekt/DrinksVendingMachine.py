import json
from automatExeptions import InsufficientFunds, NoGoodsForSelling, NoProductWithThisCode, ProductIsNotAvailable
from Interface import DrinksVendingMachineUI, set_text, play_sound


class DrinksVendingMachine:
    """
    Klasa DrinksVendingMachine:
    DrinksVendingMachine - klasa opisuje wydajność automatu z napojami

    Методы:
    set_commands
    put_number (number:int)
    info_by_number
    screen_label_add_text (text:str)
    money_option_click(option:str)
    fill_goods(file_name="goods.json")
    buy_button_click
    can_give_rest
    give_rest
    deny_transaction_button_click
    """

    def __init__(self, aui:DrinksVendingMachineUI):
        """
        Konstruktor - tworzy obiekt typu DrinksVendingMachine

        Argumenty:
        aui (DrinksVendingMachineUI) - interfejs użytkownika maszyny

        Pola klasy:
        interface (класс DrinksVendingMachineUI, обьект tkinter) - wygląd zewnętrzny maszyny (interfejs użytkownika)
        __coint_option__ (słownik) - klucze: lista różnych nominałów, wartości, reprezentacja nominałów w złotówkach
        __code (str) - kod produktu
        __credits (int) - pieniądze, które użytkownik ma na koncie
        __confirmation (bool) - flaga odpowiedzialna za zgodę użytkownika na zakup bez wydawania reszty     
        """
        self.interface = aui
        self.__coint_option__ = {"1 grosz": 1, "2 grosze": 2, "5 groszy": 5, "10 groszy": 10, "20 groszy": 20, "50 groszy": 50,
                            "1 złoty": 100, "2 złote": 200, "5 złotych": 500}
        self.set_commands() 
        self.__code = ""
        self.__credits = 0
        self.__confirmation = False

    @property
    def code(self):
        return self.__code

    @property
    def credits(self):
        return self.__credits


    def set_commands(self):          
        """
        Ustawia komendy dla kontrolek
        """
        self.interface.set_command(self.interface.numbers_buttons[0], lambda: self.put_number(0))
        self.interface.set_command(self.interface.numbers_buttons[1], lambda: self.put_number(1))
        self.interface.set_command(self.interface.numbers_buttons[2], lambda: self.put_number(2))
        self.interface.set_command(self.interface.numbers_buttons[3], lambda: self.put_number(3))
        self.interface.set_command(self.interface.numbers_buttons[4], lambda: self.put_number(4))
        self.interface.set_command(self.interface.numbers_buttons[5], lambda: self.put_number(5))
        self.interface.set_command(self.interface.numbers_buttons[6], lambda: self.put_number(6))
        self.interface.set_command(self.interface.numbers_buttons[7], lambda: self.put_number(7))
        self.interface.set_command(self.interface.numbers_buttons[8], lambda: self.put_number(8))
        self.interface.set_command(self.interface.numbers_buttons[9], lambda: self.put_number(9))
        self.interface.set_command(self.interface.buy_button, self.buy_button_click)
        self.interface.set_command(self.interface.deny_transaction_button, self.deny_transaction_button_click)
        self.interface.set_command(self.interface.money_option, self.money_option_click, options=self.__coint_option__)


    def put_number(self, number:int):           ## wywoływana po naciśnięciu przycisków numerycznych
        """
        Obsługa kliknięcia przycisku numerycznego

        Argumenty:
        number (int) - cyfry na przyciskach
        """
        text = ""
        if len(self.__code) in (0, 2):
            self.__code = str(number)
            text += self.__code
            set_text(self.interface.screen_label, text)
        elif len(self.__code) == 1: 
            self.__code += str(number)
            self.info_by_number()


    def info_by_number(self): 
        """
        Zapisuje informacje o produkcie do screen_label
        """
        text = ""           
        with open("goods.json", "rt") as fo:
            goods = json.load(fo)
        if not self.__code in list(goods.keys()):
            text+="No product\nwith this code"
            set_text(self.interface.screen_label, text)
            raise NoProductWithThisCode()
        elif goods[self.__code]["count"] == 0:
            text+="This product\nis not available"
            set_text(self.interface.screen_label, text)
            raise ProductIsNotAvailable()
        else:
            text += goods[self.__code]["name"] 
            text += "\n" 
            text += str(goods[self.__code]["price"]/100)
            text += " zł"
        set_text(self.interface.screen_label, text)


    def money_option_click(self, option:str):
        """
        Program obsługi zdarzeń związanych z pieniędzmi

        Argumenty:
        option (str) - ilość pieniędzy
        """
        play_sound("coin_throwing_sound.mp3")
        if len(self.__code) == 2:
            self.info_by_number()
        self.__credits += self.__coint_option__[option]
        set_text(self.interface.money_screen_label, "Credits - " + str(self.__credits / 100))
        with open("money.json", "rt") as fo:
            money = json.load(fo)
        money[str(self.__coint_option__[option])] += 1
        with open("money.json", "wt") as fo:
            json.dump(money, fo)
        self.interface.reset_money_option()       

        
    def fill_goods(self, file_name="goods.json"):
        """
        Wypisuje listę towarów z pliku w goods_list_text

        Argumenty:
        file_name (str) - plik towarów
        """
        try: 
            with open(file_name) as fo:
                goods = json.load(fo)
                goods_str = ""
                for __code, info in goods.items():
                    goods_str += __code + "."
                    goods_str += info["name"]
                    if info["count"]>0:
                        goods_str += " " * (40 - len(info["name"]))
                        goods_str += str(info["price"]/100) + "\n"
                    else:
                        goods_str += " " * (30 - len(info["name"]))
                        goods_str += "Not available" + "\n"
                goods_str = goods_str[:-1]
                set_text(self.interface.goods_list_text, goods_str)
        except FileNotFoundError:
            raise FileNotFoundError


    def buy_button_click(self):             ## sprzedaje towary
        """
        sprzedaje towary
        """
        play_sound("sound_to_buy_and_deny_transaction.mp3")
        if len(self.__code) == 2:
            with open ("goods.json", "rt") as fo:
                goods = json.load(fo)
            if self.__confirmation:
                goods[self.__code]["count"] -= 1
                with open ("goods.json", "wt") as fo:
                    json.dump(goods, fo)
                set_text(self.interface.screen_label, "")
                self.__confirmation = False
                self.__credits -= goods[self.__code]["price"]
                self.__code = ""                
                set_text(self.interface.money_screen_label, "Credits - " + str(self.__credits / 100))
                return
            if self.__credits < goods[self.__code]["price"]:
                set_text(self.interface.screen_label, "Insufficient funds")
                raise InsufficientFunds()
            elif self.__credits == goods[self.__code]["price"]:
                goods[self.__code]["count"] -= 1
                self.__credits -= goods[self.__code]["price"]
                set_text(self.interface.money_screen_label, "Credits - " + str(self.__credits / 100))
                with open ("goods.json", "wt") as fo:
                    json.dump(goods, fo)
                set_text(self.interface.screen_label, "")
                self.__code = ""
            else:                                                                   ## gdy trzeba wydać resztę     
                rest = self.__credits - goods[self.__code]["price"]       
                if self.can_give_rest(rest):                                            ## gdy możemy wydać resztę
                    goods[self.__code]["count"] -= 1
                    self.__credits -= goods[self.__code]["price"]
                    set_text(self.interface.money_screen_label, "Credits - " + str(self.__credits / 100))
                    with open("goods.json", "wt") as fo:
                        json.dump(goods, fo)
                    set_text(self.interface.screen_label, "")
                    self.__code = ""
                else:
                    set_text(self.interface.screen_label, "Cannot give change, push Buy \nbutton to buy without rest")
                    self.__confirmation = True
        else:
            raise NoGoodsForSelling


    def can_give_rest(self, rest):                      ## sprawdza, czy możemy wydać resztę
        """
        Sprawdza, czy automat sprzedający może wydać resztę użytkownikowi

        Argumenty:
        rest - reszta

        Returns:
        True - automat może dać resztę
        False - automat nie może dać reszty
        """
        with open ("money.json", "rt") as fo:
                money = json.load(fo)
        for i in sorted(list(map(int, list(money.keys()))), reverse=True):
            minimal = min(rest//i, money[str(i)])           # 425//500, 80  minimal 2 = 425//200, 80    
            money[str(i)] -= minimal                                  # 80 - 0        80 - 2 = 78
            rest = rest - minimal*i                    # 425 - 0       425 - 2*200 = 25
        if rest==0:           
            return True
        else:
            return False


    def give_rest(self, rest):			## wydaję resztę
        """
        Wydaje resztę użytkownikowi

        Argumenty:
        rest - reszta
        """
        with open ("money.json", "rt") as fo:
                money = json.load(fo)
        for i in sorted(list(map(int, list(money.keys()))), reverse=True):
            minimal = min(rest//i, money[str(i)])      # 425//500, 80  minimal 2 = 425//200, 80    
            money[str(i)] -= minimal                        # 80 - 0        80 - 2 = 78
            rest = rest - minimal*i               # 425 - 0       425 - 2*200 = 25
        with open ("money.json", "wt") as fo:           
            json.dump(money, fo)
            
        
    def deny_transaction_button_click(self):
        """
        Obsługa zdarzeń, klikając przycisk Odrzuć transakcję
        """
        play_sound("sound_to_buy_and_deny_transaction.mp3")
        self.__confirmation = False
        set_text(self.interface.screen_label, "")
        if self.__credits > 0: 
            rest = self.__credits 
            if self.can_give_rest(rest):                     ## gdy automat może dać resztę   
                self.give_rest(rest) 
                self.__credits = 0
                set_text(self.interface.money_screen_label, "Credits - 0")
                set_text(self.interface.screen_label, "")
            else:
                self.__credits = 0
                set_text(self.interface.money_screen_label, "Credits - 0")
                set_text(self.interface.screen_label, "")           
