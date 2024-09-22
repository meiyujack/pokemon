from tkinter import Tk, Toplevel,ttk
from tkinter import PhotoImage
import sqlite3
import tkinter
import tkinter.messagebox
import random

class App(Tk):
    def __init__(self):
        super().__init__()
        self.now=1
        self.iconbitmap("resources/favicon.ico")
        self.title("宝可梦图鉴")
        self.geometry("310x333+650+207")
        self.resizable(0,0)
        frm=ttk.Frame(self)
        self.idVar=tkinter.StringVar()
        self.nameVar=tkinter.StringVar()
        self.subnameVar=tkinter.StringVar()
        self.typeVar1=tkinter.StringVar()
        self.typeVar2=tkinter.StringVar()
        self.typeVar=tkinter.StringVar()
        frm.grid()
        one=App.select("select number,id,name,subname,type,img from basic limit 1;")
        self.total=App.select("SELECT COUNT(*) FROM basic;")[0]
        self.photo=PhotoImage(data=one[5])
        self.basic_photo=self.photo.subsample(3)
        self.pokemon=tkinter.Button(self,image=self.basic_photo,bd=0,command=self.window_info).grid(column=1,row=3,columnspan=2)

        id=ttk.Label(self,textvariable=self.idVar).grid(column=0,row=4,sticky="W",padx=10)
        self.idVar.set(one[1])
        name=ttk.Label(self,textvariable=self.nameVar,style="myNormal.TLabel").grid(column=0,row=5,columnspan=2,sticky="W",padx=10)
        self.nameVar.set(one[2])
        subname=ttk.Label(self,textvariable=self.subnameVar).grid(column=0,row=6,columnspan=3)
        self.subnameVar.set(one[3] if one[3] else "")
        type_1=ttk.Label(self,textvariable=self.typeVar1,style="myMiddle.TLabel").grid(column=0,row=7,columnspan=2,sticky="W")
        self.typeVar1.set(self.select(f"select name from type where id={int(one[4].split(",")[0])}")[0])
        type_2=ttk.Label(self,textvariable=self.typeVar2,style="myMiddle.TLabel").grid(column=2,row=7,columnspan=2,sticky="W")
        self.typeVar2.set(self.select(f"select name from type where id={int(one[4].split(",")[1])}")[0])
        type=ttk.Label(self,textvariable=self.typeVar,style="myMiddle.TLabel").grid(column=1,row=7,columnspan=2,sticky="W")
        self.typeVar.set("")

        self.left=PhotoImage(file="resources/arrow_left_btn.png")
        self.left=self.left.subsample(4,4)
        self.right=PhotoImage(file="resources/arrow_right_btn.png")
        self.right=self.right.subsample(4,4)
        self.entryVar=tkinter.StringVar()
        self.entry=ttk.Entry(self,width=10,textvariable=self.entryVar)
        self.entry.grid(column=1,row=0,pady=5,sticky="E",padx=(85,0))
        button=ttk.Button(self,text="确定",width=4,command=self.search)
        button.grid(column=2,row=0,sticky="E")
        rdm=ttk.Button(self,text="随机",width=4,command=self.random).grid(column=3,row=0)
        self.entry.focus_set()
        self.entry.bind("<Return>",lambda x:self.search())
        left_btn=tkinter.Button(self,image=self.left,bd=0,command=self.arrow_left).grid(column=0,row=3,sticky="E")
        right_btn=tkinter.Button(self,image=self.right,bd=0,command=self.arrow_right).grid(column=3,row=3,sticky="W")

        lbl_normal_style=ttk.Style()
        lbl_normal_style.configure("myNormal.TLabel",font=("微软雅黑",11))
        lbl_middle_style=ttk.Style()
        lbl_middle_style.configure("myMiddle.TLabel",font=("微软雅黑",13))
        lbl_large_style=ttk.Style()
        lbl_large_style.configure("myLarge.TLabel",font=("微软雅黑",18))
    
    @staticmethod
    def select(sql):
        conn=sqlite3.connect("resources/pokemon.db")
        cur=conn.cursor()
        return cur.execute(sql).fetchone()
    
    def change(self,sql):
        one=App.select(sql)
        if one:
            self.now=one[0]
            self.photo=PhotoImage(data=one[5])
            self.basic_photo=self.photo.subsample(3,3)     
            self.pokemon=tkinter.Button(self,image=self.basic_photo,bd=0,command=self.window_info).grid(column=1,row=3,columnspan=2)

            self.idVar.set(one[1])
            self.nameVar.set(one[2])
            self.subnameVar.set(one[3] if one[3] else "")
            if ',' in one[4]:
                self.typeVar1.set(self.select(f"select name from type where id={int(one[4].split(",")[0])}")[0])
                self.typeVar2.set(self.select(f"select name from type where id={int(one[4].split(",")[1])}")[0])
                self.typeVar.set('')
            else:
                
                self.typeVar.set(self.select(f"select name from type where id={int(one[4])}")[0])
                self.typeVar1.set('')
                self.typeVar2.set('')
    
    def arrow_left(self):
        if self.now>1:
            self.now-=1
        else:
            self.now=self.total
        self.change(f"select * from basic where number = {self.now};")

    def arrow_right(self):
        if self.now<self.total:
            self.now+=1
        else:
            self.now=1
        self.change(f"select * from basic where number = {self.now};")


    def search(self):
        s=self.entryVar.get()
        if s.isalpha():
            self.change(f"select * from basic where name like '%{s}%'")
        elif s.isdigit():
            self.change(f"select * from basic where number = {s}")
        else:
            tkinter.messagebox.showwarning("警告","请输入内容进行查询")

    def random(self):
        r=random.randint(1,self.total)
        self.now=r
        self.change(f"select * from basic where number = {r};")

    def window_info(self):
        details=App.select(f"select gender,story,category,height,weight,ability,weakness,hp,atk,def,spatk,spdef,spd from info where number = {self.now}")
        window=Toplevel()
        window.iconbitmap("resources/favicon.ico")
        window.title(f"宝可梦详情-{self.nameVar.get()}")
        window.geometry("1078x521")
        window.focus_set()
        window.resizable(0,0)
        frm=ttk.Frame(window)
        frm.grid()
        ttk.Label(window,text=self.idVar.get(),style="myMiddle.TLabel").grid(row=0,column=2,columnspan=3)
        ttk.Label(window,text=self.nameVar.get(),style="myLarge.TLabel").grid(row=1,column=2,columnspan=3)
        window.info_photo=self.photo.subsample(2)
        # tkinter.messagebox.showinfo("",f"{self.photo.width()}x{self.photo.height()}")
        pokemon=tkinter.Label(window,image=window.info_photo,width=315,height=315).grid(column=1,row=2,columnspan=5,rowspan=5)
        ttk.Label(window,text="性别",style="myNormal.TLabel").grid(row=7,column=1,sticky="NE")
        ttk.Label(window,text="属性",style="myNormal.TLabel").grid(row=8,column=1,sticky="NE")
        ttk.Label(window,text="故事",style="myNormal.TLabel").grid(row=9,column=1,sticky="NE")

        ttk.Label(window,text="分类",style="myNormal.TLabel").grid(row=2,column=6,pady=(70,0),sticky="NW")
        ttk.Label(window,text=details[2]).grid(row=2,column=7,pady=(71,0),sticky="NW")

        ttk.Label(window,text="身高",style="myNormal.TLabel").grid(row=3,column=6,sticky="NW")
        ttk.Label(window,text=details[3]).grid(row=3,column=7,sticky="NW",pady=(1,0))

        ttk.Label(window,text="体重",style="myNormal.TLabel").grid(row=4,column=6,sticky="NW")
        ttk.Label(window,text=details[4]).grid(row=4,column=7,sticky="NW",pady=(1,0))

        ttk.Label(window,text="特性",style="myNormal.TLabel").grid(row=5,column=6,sticky="NW")
        ability=str(details[9])
        if ',' in ability:
            ability_id1,ability_id2=ability.split(',')
            result1=self.select(f"select name,detail from ability where id = {ability_id1}")
            ability_name1,ability_detail1=result1[0],result1[1]
            result2=self.select(f"select name,detail from ability where id = {ability_id2}")
            ability_name2,ability_detail2=result2[0],result2[1]
            ttk.Label(window,text=ability_name1).grid(row=5,column=7,sticky="NW",pady=(1,0))
            ttk.Label(window,text=ability_detail1).grid(row=5,column=8,columnspan=2,sticky="NW",pady=(1,0))
            ttk.Label(window,text=ability_name2).grid(row=6,column=7,sticky="NW",pady=(1,0))
            ttk.Label(window,text=ability_detail2).grid(row=6,column=8,columnspan=2,sticky="NW",pady=(1,0))
        else:
            result=self.select(f"select name,detail from ability where id = {ability}")
            ability_name,ability_detail=result[0],result[1]
            ttk.Label(window,text=ability_name).grid(row=5,column=7,sticky="NW",pady=(2,0))
            ttk.Label(window,text=ability_detail).grid(row=5,column=8,columnspan=2,sticky="NW",pady=(1,0))

        ttk.Label(window,text="弱点",style="myNormal.TLabel").grid(row=7,column=6,sticky="NW")
        weakness=details[6]
        if weakness:
            n=len(weakness.split(","))
            if n==1:
                ttk.Label(window,text=self.select(f"select name from type where id = {weakness}")[0]).grid(row=7,column=7,sticky="NW",pady=(2,0))
            if n==2:
                one,two=weakness.split(",")
                ttk.Label(window,text=self.select(f"select name from type where id = {one}")[0]).grid(row=7,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {two}")[0]).grid(row=7,column=8,sticky="NW",pady=(2,0))
            if n==3:
                one,two,three=weakness.split(",")
                ttk.Label(window,text=self.select(f"select name from type where id = {one}")[0]).grid(row=7,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {two}")[0]).grid(row=7,column=8,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {three}")[0]).grid(row=8,column=7,sticky="NW",pady=(1,0))
            if n==4:
                one,two,three,four=weakness.split(",")
                ttk.Label(window,text=self.select(f"select name from type where id = {one}")[0]).grid(row=7,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {two}")[0]).grid(row=7,column=8,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {three}")[0]).grid(row=8,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {four}")[0]).grid(row=8,column=8,sticky="NW",pady=(2,0))
            if n==5:
                one,two,three,four,five=weakness.split(",")
                ttk.Label(window,text=self.select(f"select name from type where id = {one}")[0]).grid(row=7,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {two}")[0]).grid(row=7,column=8,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {three}")[0]).grid(row=7,column=9,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {four}")[0]).grid(row=8,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {five}")[0]).grid(row=8,column=8,sticky="NW",pady=(2,0))
            if n==6:
                one,two,three,four,five,six=weakness.split(",")
                ttk.Label(window,text=self.select(f"select name from type where id = {one}")[0]).grid(row=7,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {two}")[0]).grid(row=7,column=8,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {three}")[0]).grid(row=7,column=9,sticky="NW",padx=(0,150),pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {four}")[0]).grid(row=8,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {five}")[0]).grid(row=8,column=8,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {six}")[0]).grid(row=8,column=9,sticky="NW",padx=(0,150),pady=(2,0))
            if n==7:
                one,two,three,four,five,six,seven=weakness.split(",")
                ttk.Label(window,text=self.select(f"select name from type where id = {one}")[0]).grid(row=7,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {two}")[0]).grid(row=7,column=8,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {three}")[0]).grid(row=7,column=9,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {four}")[0]).grid(row=8,column=7,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {five}")[0]).grid(row=8,column=8,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {six}")[0]).grid(row=8,column=9,sticky="NW",pady=(2,0))
                ttk.Label(window,text=self.select(f"select name from type where id = {seven}")[0]).grid(row=7,column=10,sticky="NW",pady=(2,0))
        else:
            ttk.Label(window,text="无").grid(row=7,column=7,sticky="NW",pady=(2,0))

        gender=details[0]
        if gender:
            window.male=PhotoImage(file="resources/icon_male.png")
            window.male=window.male.subsample(4,4)
            window.female=PhotoImage(file="resources/icon_female.png")
            window.female=window.female.subsample(4,4)
            if ',' in gender:    
                tkinter.Label(window,image=window.male).grid(column=2,row=7,sticky="NE")
                tkinter.Label(window,image=window.female).grid(column=3,row=7,sticky="NE")
            elif gender=='0':
                tkinter.Label(window,image=window.female).grid(column=2,row=7,sticky="N")
            else:
                tkinter.Label(window,image=window.male).grid(column=2,row=7,sticky="N")
        else:
            gender='无'
            tkinter.Label(window,text=gender).grid(column=2,row=7,sticky="N")

        ttk.Label(window,text=self.typeVar1.get(),style="myNormal.TLabel").grid(column=2,row=8,columnspan=2,pady=(1,0))
        ttk.Label(window,text=self.typeVar2.get(),style="myNormal.TLabel").grid(column=4,row=8,columnspan=2,pady=(1,0))
        ttk.Label(window,text=self.typeVar.get(),style="myNormal.TLabel").grid(column=3,row=8,columnspan=2,pady=(1,0))

        story=details[1]
        if story:
            if "\t" in story:
                story=story.split("\t")
                if len(story)==2:
                    tkinter.Label(window,text=story[0]).grid(column=2,row=9,columnspan=4,pady=(1,0))
                    tkinter.Label(window,text=story[1]).grid(column=2,row=10,columnspan=4,pady=(1,0))
                    tkinter.Label(window,text="").grid(column=2,row=11,columnspan=4)
                if len(story)==3:
                    tkinter.Label(window,text=story[0]).grid(column=2,row=9,columnspan=4,pady=(1,0))
                    tkinter.Label(window,text=story[1]).grid(column=2,row=10,columnspan=4,pady=(1,0))
                    tkinter.Label(window,text=story[2]).grid(column=2,row=11,columnspan=4,pady=(1,0))
            else:
                tkinter.Label(window,text=story).grid(column=2,row=9,columnspan=4,pady=(1,0))
                tkinter.Label(window,text="").grid(column=2,row=10,columnspan=4)
                tkinter.Label(window,text="").grid(column=2,row=11,columnspan=4)

            ttk.Label(window,text="HP:").grid(row=12,column=0,sticky="E",padx=(10,0))
            ttk.Label(window,text=details[7]).grid(row=12,column=1,sticky="W",padx=(0,50))
            ttk.Label(window,text="ATK:").grid(row=12,column=2,sticky="E")
            ttk.Label(window,text=details[8]).grid(row=12,column=3,sticky="W")
            ttk.Label(window,text="DEF:").grid(row=12,column=4,sticky="E")
            ttk.Label(window,text=details[9]).grid(row=12,column=5,sticky="W")
            ttk.Label(window,text="SPATK:").grid(row=12,column=6,sticky="W")
            ttk.Label(window,text=details[10]).grid(row=12,column=7,sticky="W")
            ttk.Label(window,text="SPDEF:").grid(row=12,column=8,sticky="E")
            ttk.Label(window,text=details[11]).grid(row=12,column=9,sticky="W")
            ttk.Label(window,text="SPD:").grid(row=12,column=10,sticky="E")
            ttk.Label(window,text=details[12]).grid(row=12,column=11,sticky="W")

if __name__=="__main__":
    app=App()
    app.mainloop()


