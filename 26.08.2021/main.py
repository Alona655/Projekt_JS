from tkinter import mainloop
from Interface import DrinksVendingMachineUI
from DrinksVendingMachine import DrinksVendingMachine


AUI = DrinksVendingMachineUI()
automat = DrinksVendingMachine(AUI)
automat.fill_goods()

automat.interface.mainloop()