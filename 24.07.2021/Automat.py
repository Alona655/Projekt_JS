from Interface import AutomatUI
import json


class Automat:
    def __init__(self, aui:AutomatUI):
        self.interface = aui
        self.coint_option = {"1 grosz": 1, "2 grosze": 2, "5 groszy": 5, "10 groszy": 10, "20 groszy": 20, "50 groszy": 50,
                            "1 usd": złoty, "2 złote": 200, "5 złotych": 500} 
        self.set_commands() 
        self.code = ""
        self.credits = 0
        self.confirmation = False
        self.rest = 0
    
    def set_commands(self):
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
        self.interface.set_command(self.interface.money_option, self.money_option_click, options=self.coint_option)


    def put_number(self, number):
        text = ""
        if len(self.code) in (0, 2):
            self.code = str(number)
            text += self.code
        elif len(self.code) == 1: 
            self.code += str(number)            
            with open("goods.json", "rt") as fo:
                goods = json.load(fo)
            if not self.code in list(goods.keys()):
                text+="No product\nwith this code"
            elif goods[self.code]["count"] == 0:
                text+="This product\nis not available"
            else:
                text += goods[self.code]["name"]  
        self.interface.set_text(self.interface.screen_label, text)        

    def screen_label_add_text(self, text):
        self.interface.screen_label['text'] += text

    def money_option_click(self, option):
        self.credits += self.coint_option[option]
        self.interface.set_text(self.interface.money_screen_label, "Credits - " + str(self.credits / 100))
        with open("money.json", "rt") as fo:
            money = json.load(fo)
        money[str(self.coint_option[option])] += 1
        with open("money.json", "wt") as fo:
            json.dump(money, fo)
        self.interface.reset_money_option()

    def fill_goods(self):
        with open("goods.json") as fo:
            goods = json.load(fo)
            goods_str = ""
            for code, info in goods.items():
                goods_str += code + "."
                goods_str += info["name"]       
                goods_str += " " * (40 - len(info["name"]))
                goods_str += str(info["price"]/100) + "\n"
            goods_str = goods_str[:-1]
            self.interface.set_text(self.interface.goods_list_text, goods_str)
            print(goods_str)

    def fill_money(self):
        with open("money.json") as fo:
            money = json.load(fo)
            money_str = ""
            for code, info in money.items():
                money_str += str(code["price"]/100) + " "
                money_str += info["count"] + "\t"
                money_str += "\n"
            self.interface.set_text(self.interface.money_list_text, money_str)
            print(money_str)

    def buy_button_click(self):
        if len(self.code) == 2:
            with open ("goods.json", "rt") as fo:
                goods = json.load(fo)
            if self.confirmation:
                goods[self.code]["count"] -= 1
                with open ("goods.json", "wt") as fo:
                    json.dump(goods, fo)
                self.interface.set_text(self.interface.screen_label, "")
                self.confirmation = False
                self.credits -= goods[self.code]["price"]
                self.code = ""                
                self.interface.set_text(self.interface.money_screen_label, "Credits - " + str(self.credits / 100))
                return
            if self.credits < goods[self.code]["price"]:
                self.interface.set_text(self.interface.screen_label, "Insufficient funds")
            elif self.credits == goods[self.code]["price"]:
                goods[self.code]["count"] -= 1
                self.credits -= goods[self.code]["price"]
                self.interface.set_text(self.interface.money_screen_label, "Credits - " + str(self.credits / 100))
                with open ("goods.json", "wt") as fo:
                    json.dump(goods, fo)
                self.interface.set_text(self.interface.screen_label, "")
                self.code = ""
            else:                                                                   ## gdy trzeba wydać resztę      
                self.rest = self.credits - goods[self.code]["price"]       
                if self.can_give_rest():                                            ## gdy możemy wydać resztę
                    goods[self.code]["count"] -= 1
                    self.credits -= goods[self.code]["price"]
                    self.interface.set_text(self.interface.money_screen_label, "Credits - " + str(self.credits / 100))
                    with open("goods.json", "wt") as fo:
                        json.dump(goods, fo)
                    self.interface.set_text(self.interface.screen_label, "")
                    self.code = ""
                else:
                    self.interface.set_text(self.interface.screen_label, "Cannot give change,\npush Buy button to continue")
                    self.confirmation = True

    def can_give_rest(self):                      ## sprawdza, czy możemy wydać resztę
        with open ("money.json", "rt") as fo:
                money = json.load(fo)
        for i in sorted(list(map(int, list(money.keys()))), reverse=True):
            minimal = min(self.rest//i, money[str(i)])           # 425//500, 80  minimal 2 = 425//200, 80    
            money[str(i)] -= minimal                                  # 80 - 0        80 - 2 = 78
            self.rest = self.rest - minimal*i                    # 425 - 0       425 - 2*200 = 25
        if self.rest==0:           
            return True
        else:
            return False

    def give_rest(self):			## wydaję resztę
        with open ("money.json", "rt") as fo:
                money = json.load(fo)
        for i in sorted(list(map(int, list(money.keys()))), reverse=True):
            minimal = min(self.rest//i, money[str(i)])      # 425//500, 80  minimal 2 = 425//200, 80    
            money[str(i)] -= minimal                        # 80 - 0        80 - 2 = 78
            self.rest = self.rest - minimal*i               # 425 - 0       425 - 2*200 = 25
        with open ("money.json", "wt") as fo:           
            json.dump(money, fo)
        
    def deny_transaction_button_click(self):
        self.confirmation = False
        self.interface.set_text(self.interface.screen_label, "")
        if self.credits > 0: 
            if self.can_give_rest():                     ## jeśli możemy dać resztę              
                self.rest = self.credits 
                self.give_rest() 
                self.credits = 0
                self.interface.set_text(self.interface.money_screen_label, "Credits - 0")
                self.interface.set_text(self.interface.screen_label, "")
            else:
                self.credits = 0
                self.interface.set_text(self.interface.money_screen_label, "Credits - 0")
                self.interface.set_text(self.interface.screen_label, "")           
