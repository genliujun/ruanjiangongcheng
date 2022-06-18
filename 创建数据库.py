import openpyxl
import pymysql

students = []
# 读取excel数据并存入数组
def read_excel_file():
    wb = openpyxl.load_workbook('./database.xlsx')
    sheet = wb.get_sheet_by_name('Sheet1')
    cells = sheet['A2':f'C{sheet.max_row}']
    for r in cells:
        student = []
        for c in r:
            student.append(c.value)
        students.append(student)
    print(students)

# 创建数据库
def create_database():
    con = pymysql.Connect(host='localhost', port=3306, user='root', password='123456')
    cur = con.cursor()
    cur.execute("create database shujuku;")
    con.select_db("shujuku")
    cur.execute("create table students(name char(10),id int(10),score int(4));")
    for student in students:
        cur.execute(f"insert into students(name, id, score) values ('{student[0]}',{student[1]},{student[2]});")
        con.commit()
    cur.execute("select * from students;")
    result = cur.fetchall()
    print(result)
    print("数据库创建成功！")

if __name__ == '__main__':
    read_excel_file()
    create_database()