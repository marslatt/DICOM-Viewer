from viewer import ImageViewer
from tkinter import Tk
 
def main():
    root = Tk()
    frame = ImageViewer(root)
    frame.pack()
    root.mainloop()
 
if __name__ == '__main__':
    main()
