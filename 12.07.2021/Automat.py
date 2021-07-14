import json


class Automat:
    def __init__(self, aui):
        self.interface = aui 
        self.set_commands() 
        self.code = ""
        self.credits = 0
    
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
        coins_options = (1, 2, 5, 10, 20, 50, 100, 200, 500)
        self.interface.set_command(self.interface.money_option, self.money_option_click, options=coins_options)

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

    def screen_label_clean(self):
        self.interface.screen_label['text'] = ""

    def screen_label_add_text(self, text):
        self.interface.screen_label['text'] += text

    def money_option_click(self, option):
        self.credits += option
        with open ("money.json", "rt") as fo:
            money = json.load(fo)
        money[str(option)] += 1
        with open ("money.json", "wt") as fo:
            json.dump(money, fo)
        self.interface.set_text(self.interface.money_screen_label, "Credits - " + str(self.credits / 100))

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
        print("Buy")

    def deny_transaction_button_click(self):
        print("Deny")