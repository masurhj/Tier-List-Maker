
from tkinter import Canvas, Tk


class tkWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("584x322")
        self.root.configure(bg = "#FFFFFF")

    def start(self):
        from loginPage.loginPage import loginPage
        self.canvas = loginPage(self.root)
        self.root.mainloop()    