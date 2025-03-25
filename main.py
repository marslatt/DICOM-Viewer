 
from viewer import MainFrame
from tkinter import Tk

def main():
    root = Tk()
    frame = MainFrame(root)
    frame.pack()
    root.mainloop()
 
if __name__ == '__main__':
    main()

