from tkinter import *
from tkinter import messagebox
from process_sql import Poem
from PIL import Image, ImageTk

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.createwWidget()

        self.pack()

    def createwWidget(self):
        self.frame1 = Frame(self)
        self.frame1.pack()
        self.label1 = Label(self.frame1, text="请输入古诗名称：")
        self.label1.pack(side=LEFT)
        self.text1 = Text(self.frame1, width=20, height=1, borderwidth=1)
        self.text1.pack()

        self.frame2 = Frame(self)
        self.frame2.pack()

        self.button1 = Button(self.frame2, text="show", command=self.show)
        self.button1.pack(side=LEFT)
        self.button2 = Button(self.frame2, text="replay", command=lambda : self.frame3.destroy())
        self.button2.pack()

    def show(self):
        self.frame3 = Frame(self)
        self.text1.update()
        self.pome_titel= self.text1.get("0.0", "end")
        pome = Poem(None, None, None, None)
        results = pome.select(self.pome_titel[0:-1])
        for result in results:
            self.pome_text = result[3]
        # self.pome_text = "床前明月光，疑似地上霜.\n举头望明月，低头思故乡"
            self.poem_titel_label = Label(self.frame3, text=self.pome_titel)
            self.poem_text_label = Label(self.frame3, text=self.pome_text)
            self.poem_titel_label.update()
            self.poem_text_label.update()
            self.poem_titel_label.pack()
            self.poem_text_label.pack()

            self.frame4 = Frame(self.frame3)
            self.img1 = Image.open(result[1])  # 打开图片
            self.img1 = self.img1.resize((int(self.img1.size[0]/3), int(self.img1.size[1]/3)))
            self.photo1 = ImageTk.PhotoImage(self.img1)  # 用PIL模块的PhotoImage打开
            print("./poem_image/" + result[1][19:])

            self.img2 = Image.open("./poem_image/" + result[1][20:])  # 打开图片
            self.img2 = self.img2.resize((int(self.img2.size[0] / 3), int(self.img2.size[1] / 3)))
            self.photo2 = ImageTk.PhotoImage(self.img2)  # 用PIL模块的PhotoImage打开

            self.imglabel1 = Label(self.frame4, image=self.photo1)
            self.imglabel1_text = Label(self.frame4, text="调整后:")
            self.imglabel2 = Label(self.frame4, image=self.photo2)
            self.imglabel2_text = Label(self.frame4, text="调整前")
            self.imglabel1_text.pack(side=LEFT)
            self.imglabel1.pack(side=LEFT)
            self.imglabel2_text.pack(side=LEFT)
            self.imglabel2.pack()
            self.frame4.pack()
        self.frame3.update()
        self.frame3.pack()
        pome.close()


root = Tk()
root.geometry("800x400+200+300")
root.title('古诗生成器')
app = Application(root)

while True:
    root.mainloop()


# photo = None
# img = None
#
# def show():
#     global photo
#     global img
#     img = Image.open('../img.png')  # 打开图片
#     photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
#     imglabel = Label(root, image=photo)
#     imglabel.grid(row=0, column=0, columnspan=3)
#
# frame = Frame(root)
# frame.grid(row=0, column=0)
#
# ent = Text(root)
# ent.grid(row=0, column=0)
# # ent.destroy()
# btn = Button(root, text="show", bg="blue", command=show)
# btn.grid(row=1, column=0)
#
# menu = Menu(root)



root.mainloop()
# mainloop()

