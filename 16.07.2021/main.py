from tkinter import mainloop
from Interface import AutomatUI
from Automat import Automat


AUI = AutomatUI()
automat = Automat(AUI)
automat.fill_goods()

automat.interface.mainloop()