from tkinter import *  
root = Tk()  
v = StringVar()  
def test(f,s1,s2):
    if f == '小甲鱼':
        print('正确')
        print(f,s1,s2)
        return True
    else:
        print('错误')
        print(f,s1,s2)
        return False
test_register = root.register(test) #root调用register方法才能用到下边的validatecommand选项中
e1 = Entry(root,textvariable = v,validate = 'focusout',\
           validatecommand = (test_register,'%P','%i','%s')) #这些额外的参数带引号啊 ，要注意
e2 = Entry(root)
e1.pack()
e2.pack()
mainloop()


'''用验证函数模拟简单计算器'''
from tkinter import *
root = Tk()
frame = Frame(root) #把整个布局放到框架中，更好调节
frame.pack(padx = 10,pady = 10)
v1 = StringVar()
v2 = StringVar()
v3 = StringVar()

def test(content):
    if content.isdigit():#isdigit()方法，这是str的一个函数，只允许输入数字
       return True
    else:
        return False


testCmd = root.register(test)#通过register方法转换为validatecommand选项能接收的函数
Entry(frame,textvariable = v1,width = 10,validate = 'key',\
      validatecommand = (testCmd,'%P')).grid(row = 0,column = 0) #用%P获取最新输入的字符串,而不用v1.get()小甲鱼说了很多，没看明白，这就不写了，呵呵
Label(frame,text = '+').grid(row = 0,column = 1)
Entry(frame,textvariable = v2,width = 10,validate = 'key',\
      validatecommand = (testCmd,'%P')).grid(row = 0,column = 2)
Label(frame,text = '=').grid(row = 0,column = 3)
Entry(frame,textvariable = v3,width = 10,state = 'readonly',validate = 'key',\
      validatecommand = (testCmd,'%P')).grid(row = 0,column = 4)

def calc():
    result = int(v1.get()) + int(v2.get())
    v3.set(result)

Button(frame,text = '计算结果',command = calc).grid(row = 1,column = 2,pady =5)
mainloop()