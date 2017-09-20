#encoding=utf-8
import pymssql
import easygui as g
import sys


#简易GUI界面
msg='请填写您的连接信息'
title='简易版 python 通讯录 by:ywd'
fields=['host','user','password','database']
values=[]
values=g.multenterbox(msg,title,fields)
while True:
    if values==None:
        break
    errmsg=''
    for i in range(len(fields)):
        if values[i].strip()=='' :
            errmsg += ("【%s】为必填项   " %fields[i])
    if errmsg == "":
        break
    values=g.multenterbox(errmsg,title,fields,values)
print("您填写的资料如下:%s" %str(values))
host=values[0]
user=values[1]
password=values[2]
database=values[3]
db=pymssql.connect(host,user,password,database,charset="utf8")
print(db)
print('成功连接')
cur=db.cursor()
print('此时游标为cur')

#创建表格，第一次使用完注释掉
'''

sql='CREATE TABLE PhoneList(
id INT NOT NULL IDENTITY,
name NVARCHAR(255) NOT NULL,
address NVARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
phoneNumber BIGINT NOTNUL
)'
cur.execute(sql)
db.commit()



'''
#创建并且保存联系人
def insert():
    words=str(input('请输入您需要保存的信息并以"姓名;住址;邮箱;手机号"格式输入：\n'))
    name=words.split(';')[0]
    address=words.split(';')[1]    
    email=words.split(';')[2]
    phonenumber=words.split(';')[3]
    sql="INSERT INTO PhoneList (name,address,Email,phoneNumber) "
    sql+="values('%s','%s','%s','%s');"%(name,address,email,phonenumber)
    cur.execute(sql)
    db.commit()
    print('保存成功！')
#删除联系人    
def delete():
    words=str(input('请输入您想删除的联系人姓名\n'))
    try:
        sql=("select name,address,Email,phoneNumber from PhoneList where name='%s'"%words).encode('utf-8')
        cur.execute(sql)
        rows=cur.fetchall()
        for row in rows:
            print('姓名：'+str(row[0])  ,  '地址：'+str(row[1])  ,  'Email:'+str(row[2])  ,  '手机号：'+str(row[3]))
        
        choice=str(input('请确认您是否想要删除此联系人?(Y/N)\n'))
        if choice=='Y':
            
            sql=("delete from PhoneList where name='%s'"%words).encode('utf-8')
            cur.execute(sql)
            
            db.commit()
            sql='select name,address,Email,phoneNumber from PhoneList'
            cur.execute(sql)
            rows=cur.fetchall()
            for row in rows:
                print('姓名：'+str(row[0])  ,  '地址：'+str(row[1])  ,  'Email:'+str(row[2])  ,  '手机号：'+str(row[3]))
            
        if choice=='N':
            sql='select name,address,Email,phoneNumber from PhoneList'
            cur.execute(sql)
            rows=cur.fetchall()
            for row in rows:
                print('姓名：'+str(row[0])  ,  '地址：'+str(row[1])  ,  'Email:'+str(row[2])  ,  '手机号：'+str(row[3]))
    except:
        print('删除失败，请检查是否存在联系人\n')
    finally:
        
        sql='select name,address,Email,phoneNumber from PhoneList'
        cur.execute(sql)
        rows=cur.fetchall()
        for row in rows:        
            for i in range(4):
                print(row[i])
#搜寻联系人并且输出联系方式
def search():
    words=str(input('请输入您需要查询的联系人：姓名\n'))
    try:
        sql=("select name,address,Email,phoneNumber from PhoneList where name='%s'"%words).encode('utf-8')
        cur.execute(sql)
        rows=cur.fetchall()
        #for i in range(1,5):
         #  print(row[i])
        for row in rows:
            print('姓名：'+str(row[0])  ,  '地址：'+str(row[1])  ,  'Email:'+str(row[2])  ,  '手机号：'+str(row[3]))
                
                    
    except:
        print('未找到联系人，请检查是否存在联系人\n')
    finally:
        pass
#打印出所有联系人    
def printall():
    sql='select * from PhoneList'
    cur.execute(sql)
    rows=cur.fetchall()
    for row in rows:
        print('姓名：'+str(row[1])  ,  '地址：'+str(row[2])  ,  'Email:'+str(row[3])  ,  '手机号：'+str(row[4]))

#主菜单    
def main():
    while True:
        print('***'*4+'---'*4+'简易版python通讯录by:ywd '+'---'*4+'****'*4+'*')
        print('欢迎测试使用^_^')
        print('***'*26)
        choice=input('1.新建联系人  2.删除联系人  3.寻找联系人  4. 输出所有联系人  5.退出系统   6.清屏\n')
        if choice=='1':
            insert()
        elif choice=='2':
            delete()
        elif choice=='3':
            search()
        elif choice=='4':
            printall()
        elif choice=='5':
            sys.exit()
        elif choice=='6':
            print(' '*200*20)
        else:
            print('请输入正确的选项，谢谢!\n')


if __name__=='__main__':
    main()
    
