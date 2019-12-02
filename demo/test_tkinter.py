import tkinter  # 图形化界面GUI


def main():
    root = tkinter.Tk()
    root.title('我的第一个Python窗体')
    root.geometry('400x400')
    w = tkinter.Label(root, text="Hello Tkinter!")
    w.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
