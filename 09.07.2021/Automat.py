import json


class Automat:
    def __init__(self, aui):
        self.interface = aui 
        self.set_commands() 
    
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
        if len(self.interface.screen_label['text']) == 2:
            self.screen_label_clean()
        else:            
            self.screen_label_add_text(str(number))

    def screen_label_clean(self):
        self.interface.screen_label['text'] = ""

    def screen_label_add_text(self, text):
        self.interface.screen_label['text'] += text

    def money_option_click(self, option):
        print(option)

    def fill_goods(self):
        with open("goods.json") as fo:
            goods = json.load(fo)            
            print(goods)
            goods_str = ""
            for code, info in goods.items():
                goods_str += code + "."
                goods_str += info["name"] + "\t"       
                goods_str += str(info["price"]/100)
                goods_str += "\n"
            self.interface.set_text(self.interface.goods_list_text, goods_str)
            print(goods_str)

    def buy_button_click(self):
        print("Buy")

    def deny_transaction_button_click(self):
        print("Deny")