from automatExeptions import InsufficientFunds, NoGoodsForSelling, NoProductWithThisCode, ProductIsNotAvailable
from Interface import DrinksVendingMachineUI, set_text
import json
## from playsound import playsound
import multiprocessing


class DrinksVendingMachine:
    """
    Klasa DrinksVendingMachine:
    DrinksVendingMachine - klasa opisuje wydajność automatu z napojami
    Metody:
    set_commands
    put_number (number:int)
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
        interface (Klasa DrinksVendingMachineUI, obiekt tkinter) - wygląd maszyny (interfejs użytkownika)
        coint_option (słownik) - klucze: lista różnych nominałów, wartości, reprezentacja nominałów w złotówkach
        code (str) - kod produktu
        credits (int) - pieniądze, które użytkownik ma na koncie
        confirmation (bool) - flaga odpowiedzialna za zgodę użytkownika na zakup bez wydawania reszty
        rest (int) - reszta       
        """
        self.interface = aui
        self.__coint_option__ = {"1 grosz": 1, "2 grosze": 2, "5 groszy": 5, "10 groszy": 10, "20 groszy": 20, "50 groszy": 50,
                            "1 złoty": 100, "2 złote": 200, "5 złotych": 500}
        self.set_commands() 
        self.__code__ = ""
        self.__credits__ = 0
        self.__confirmation__ = False

    
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
        if len(self.__code__) in (0, 2):
            self.__code__ = str(number)
            text += self.__code__
        elif len(self.__code__) == 1: 
            self.__code__ += str(number)            
            with open("goods.json", "rt") as fo:
                goods = json.load(fo)
            if not self.__code__ in list(goods.keys()):
                text+="No product\nwith this __code__"
                raise NoProductWithThisCode()
            elif goods[self.__code__]["count"] == 0:
                text+="This product\nis not available"
                raise ProductIsNotAvailable()
            else:
                text += goods[self.__code__]["name"] 
                text += "\n" 
                text += str(goods[self.__code__]["price"]/100)
                text += " usd"
        set_text(self.interface.screen_label, text)


    def money_option_click(self, option:str):
        """
        Program obsługi zdarzeń związanych z pieniędzmi

        Argumenty:
        option (str) - ilość pieniędzy
        """
        ##p = multiprocessing.Process(target=playsound, args=("00923.mp3",))
        ##p.start()
        self.__credits__ += self.__coint_option__[option]
        set_text(self.interface.money_screen_label, "Credits - " + str(self.__credits__ / 100))
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
                for __code__, info in goods.items():
                    goods_str += __code__ + "."
                    goods_str += info["name"]       
                    goods_str += " " * (40 - len(info["name"]))
                    goods_str += str(info["price"]/100) + "\n"
                goods_str = goods_str[:-1]
                set_text(self.interface.goods_list_text, goods_str)
        except FileNotFoundError:
            raise FileNotFoundError


    def buy_button_click(self):             ## sprzedaje towary
        """
        Sprzedaje towary
        """
        if len(self.__code__) == 2:
            with open ("goods.json", "rt") as fo:
                goods = json.load(fo)
            if self.__confirmation__:
                goods[self.__code__]["count"] -= 1
                with open ("goods.json", "wt") as fo:
                    json.dump(goods, fo)
                set_text(self.interface.screen_label, "")
                self.__confirmation__ = False
                self.__credits__ -= goods[self.__code__]["price"]
                self.__code__ = ""                
                set_text(self.interface.money_screen_label, "Credits - " + str(self.__credits__ / 100))
                return
            if self.__credits__ < goods[self.__code__]["price"]:
                set_text(self.interface.screen_label, "Insufficient funds")
                raise InsufficientFunds()
            elif self.__credits__ == goods[self.__code__]["price"]:
                goods[self.__code__]["count"] -= 1
                self.__credits__ -= goods[self.__code__]["price"]
                set_text(self.interface.money_screen_label, "Credits - " + str(self.__credits__ / 100))
                with open ("goods.json", "wt") as fo:
                    json.dump(goods, fo)
                set_text(self.interface.screen_label, "")
                self.__code__ = ""
            else:                                                                   ## gdy trzeba wydać resztę      
                rest = self.__credits__ - goods[self.__code__]["price"]       
                if self.can_give_rest(rest):                                            ## gdy możemy wydać resztę
                    goods[self.__code__]["count"] -= 1
                    self.__credits__ -= goods[self.__code__]["price"]
                    set_text(self.interface.money_screen_label, "Credits - " + str(self.__credits__ / 100))
                    with open("goods.json", "wt") as fo:
                        json.dump(goods, fo)
                    set_text(self.interface.screen_label, "")
                    self.__code__ = ""
                else:
                    set_text(self.interface.screen_label, "Cannot give change,\npush Buy button to continue")
                    self.__confirmation__ = True
        else:
            raise NoGoodsForSelling


    def can_give_rest(self, rest):                      ## sprawdza, czy możemy wydać resztę
        """
        Sprawdza, czy automat sprzedający może wydać resztę użytkownikowi

        Argumenty:
        rest - reszta

        Returns:
        True - może dać resztę
        False - nie może dać reszty
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
        self.__confirmation__ = False
        set_text(self.interface.screen_label, "")
        if self.__credits__ > 0: 
            rest = self.__credits__ 
            if self.can_give_rest(rest):                     ## jeśli możemy dać resztę   
                self.give_rest(rest) 
                self.__credits__ = 0
                set_text(self.interface.money_screen_label, "Credits - 0")
                set_text(self.interface.screen_label, "")
            else:
                self.__credits__ = 0
                set_text(self.interface.money_screen_label, "Credits - 0")
                set_text(self.interface.screen_label, "")           
