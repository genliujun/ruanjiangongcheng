import random
import tkinter as tk
from tkinter import *
import pymysql

# 连接数据库
con = pymysql.Connect(host='localhost',port=3306,user='root',password='123456')
cur = con.cursor()
con.select_db("ysc")
cur.execute("select * from students;")
students = cur.fetchall()

stop = False  # 判断是否滚动学生数据的标志
student = '' # 抽中的学生
def refreshText():
    global Lucker,student
    if(stop):
        student = random.choice(students)
        Lucker = student
        text1.delete(0.0, tk.END)
        text1.insert(tk.INSERT, student)
        text1.update()
        window.after(10, refreshText)
    else:
        pass

# 开始按钮
def button_start_click():
    global stop
    stop= True
    window.after(10, refreshText)

# 停止按钮
def button_stop_click():
    global stop,student
    stop = False
    print(student)
    # 将点中的人记入名单
    with open('本次抽点名单.txt','a') as f:
        f.write(str(student)+'\n')

# 赋分
def getScore1():
    global student
    score = student[2]+3
    cur.execute(f"update students set score={score} where name='{student[0]}';")  # 把修改后的数据重新写入数据库
    con.commit()
    with open('本次抽点名单.txt', 'a') as f:
        f.write("优秀  +3分" + '\n')
        print("优秀  +3分")
def getScore2():
    global student
    score = student[2] + 1
    cur.execute(f"update students set score={score} where name='{student[0]}';")
    con.commit()
    with open('本次抽点名单.txt', 'a') as f:
        f.write("一般  +1分" + '\n')
        print("一般  +1分")
def getScore3():
    with open('本次抽点名单.txt', 'a') as f:
        f.write("不太行  +0分" + '\n')
        print("不太行  +0分")
def getScore4():
    global student
    score = student[2] - 5
    cur.execute(f"update students set score={score} where name='{student[0]}';")
    con.commit()
    with open('本次抽点名单.txt', 'a') as f:
        f.write("没来  -5分" + '\n')
        print("没来  -5分")

if __name__ == '__main__':
    window = tk.Tk()
    window.title('点名')
    window.geometry('500x500')  # 设置窗口大小500*500像素
    text1 = tk.Text(window, width=15, height=1)
    text1.grid(row=0, column=1, padx=80, pady=80)
    text1.config(font=("Courier", 30),background="yellow")
    text1.pack()
    button_start = Button(text='开始点名',command=button_start_click,width=40,background="green")
    button_start.pack()
    button_stop = Button(text='停止',command=button_stop_click,width=40,background="red")
    button_stop.pack()

    button_get_score1 = Button(text='优秀',command=getScore1,width=10,background="#FF6347").place(x=90,y=110)
    button_get_score2 = Button(text='一般', command=getScore2,width=10,background="yellow").place(x=170,y=110)
    button_get_score3 = Button(text='不太行', command=getScore3,width=10,background="#7FFF00").place(x=250,y=110)
    button_get_score4 = Button(text='没来', command=getScore4,width=10,background="#00FFFF").place(x=330,y=110)

    window.mainloop()

