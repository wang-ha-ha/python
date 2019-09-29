import os
import crypt 
import json
from tkinter import  *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

def relative_path_to_abs(path):
	current_path = os.path.dirname(__file__)
	return current_path + '\\' + path


def print_all(dat,str=""):
    print("%s-->type:%s len:%s content:%s"%(str,type(dat),len(dat),dat))


class application(Frame):
    def __init__(self, master=None,title="My Window"):
        Frame.__init__(self, master)
        self.master.resizable(0,0)
        self.master.title(title)
        self.master.iconbitmap(relative_path_to_abs("fruit.ico"))
        self.pack()
        
        self.init_parameter()
        self.create_widgets()
        
    def run(self):
        self.master.mainloop()    
        
    def create_widgets(self):           
        tabControl = ttk.Notebook(self.master)          
         
        tab1 = ttk.Frame(tabControl)           
        tabControl.add(tab1, text='加密数据')   
        
        self.create_top_frame_first(tab1)
        self.create_mid_frame_first(tab1)
        self.create_bot_frame_first(tab1)
         
        tab2 = ttk.Frame(tabControl)            
        tabControl.add(tab2, text='解密数据')
        
        self.create_frame_second(tab2) 
        
        tabControl.pack(expand=1, fill="both",padx=5, pady=5) 
        
    def create_frame_second(self,p):
    
        self.text_decode = Text(p,width=50,font=('Times', 14))
        self.text_decode.pack(side = "top",padx=10, pady=10)
        
        fram = ttk.LabelFrame(p,text = "operation") 
        fram.pack(expand = False,fill="x",side = "top",padx=8, pady=4)
        
        self.key_second = StringVar()
        ttk.Label(fram, text = "key").pack(side = "left",padx=8, pady=4)
        ttk.Entry(fram,show=None, font=('Arial', 10),textvariable = self.key_second).pack(side = "left",padx=8, pady=4)
   
        ttk.Button(fram, text='打开解密文件', command=self.dat_decrypts).pack(side = "right",padx=8, pady=4)

    def create_top_frame_first(self,p):
        top_frame = ttk.LabelFrame(p,text = "operation")       
        top_frame.pack(expand = False,fill="x",side = "top",padx=8, pady=4)                                                
        
        ttk.Label(top_frame, text = "op",width=3).grid(row=0, column=0,padx=8, pady=4)       
        temp = ttk.Combobox(top_frame,show=None,width=8, font=('Arial', 10),values = ("set","dump"),state='readonly',textvariable = self.dat_op)
        temp.grid(row=0, column=1)
        #temp.current(0) 
        
        ttk.Label(top_frame, text = "cmd",width=4).grid(row=0, column=2,padx=8, pady=4) 
        temp = ttk.Combobox(top_frame,show=None,width=8, font=('Arial', 10),values = ("all","add","single","tag"),state='readonly',textvariable = self.dat_cmd)
        temp.grid(row=0, column=3)
        #temp.current(0) 
        
        ttk.Label(top_frame, text = "tag",width=3).grid(row=0, column=4,padx=8, pady=4)       
        ttk.Entry(top_frame,show=None,width=8, font=('Arial', 10),textvariable = self.dat_tag).grid(row=0, column=5)
        
    def radbutn_test(self):
        pass
        '''
        print_all(self.dat_op.get())
        print_all(self.dat_cmd.get())
        print(self.dat_tag.get())
        print(self.radvar.get())
        '''
    def create_data_widget(self,parent,index,name,unit):        
    
        ttk.Label(parent, text = name,width=15).grid(row = index, column=0,padx=20)
        
        ttk.Entry(parent,show=None, font=('Arial', 10),foreground='red',textvariable = self.datarr[index]).grid(row = index, column=1,padx=8)
        
        ttk.Label(parent, text = unit,width=10).grid(row = index, column=2,padx=8)

        Radiobutton(parent,variable=self.radvar, value=index , command = self.radbutn_test).grid(row = index, column=3,padx=8)
        
    def create_mid_frame_first(self,p):
        mid_frame = ttk.LabelFrame(p,text = "information") 
        mid_frame.pack(expand = True,fill="both",side = "top",padx=8, pady=4)

        #----------------------------
        self.create_data_widget(mid_frame,0,"左仓余量","(0,10000)")
        #----------------------------
        self.create_data_widget(mid_frame,1,"右仓余量","(0,10000)")
        #----------------------------
        self.create_data_widget(mid_frame,2,"右仓规格","(50,500)")
        #----------------------------
        self.create_data_widget(mid_frame,3,"报警量","(0,1000)")        
        #----------------------------
        self.create_data_widget(mid_frame,4,"右仓杯量调节","(0,10000)")
        #----------------------------
        self.create_data_widget(mid_frame,5,"历史左仓消费总量","(0,10000)")
        #----------------------------
        self.create_data_widget(mid_frame,6,"历史右仓消费总量","(0,10000)")
        #----------------------------
        self.create_data_widget(mid_frame,7,"待机时间","(0,10000)")
        #----------------------------
        self.create_data_widget(mid_frame,8,"右仓杯量调节","(0,10000)")
        #----------------------------
        self.create_data_widget(mid_frame,9,"右仓规格","(50,500)")
        #----------------------------
        self.create_data_widget(mid_frame,10,"免支付模式","(0,1)")
        #----------------------------
        self.create_data_widget(mid_frame,11,"左仓脉冲周期","(50,500)")
        #----------------------------
        self.create_data_widget(mid_frame,12,"右仓脉冲周期","(50,500)")
        #----------------------------
        self.create_data_widget(mid_frame,13,"控料模式","(0,1)")
        #----------------------------        
        
    def create_bot_frame_first(self,p):
    
        bot_frame = ttk.LabelFrame(p,text = "sys") 
        bot_frame.pack(expand = True,fill="x",side = "top",padx=8, pady=4)
        
        quitButton = ttk.Button(bot_frame, style="R.TButton",text='Quit', command=self.quit)
        quitButton["state"] = "enable"
        quitButton.pack(side = "right") 

        quitButton = ttk.Button(bot_frame, style="R.TButton",text='生成', command=self.dat_generate)
        quitButton["state"] = "enable"
        quitButton.pack(side = "right",padx=10) 
        
        self.key_first = StringVar()
        ttk.Label(bot_frame, text = "key").pack(side = "left",padx=8)
        ttk.Entry(bot_frame,show=None, font=('Arial', 10),textvariable = self.key_first).pack(side = "left",padx=10)
    
    def init_parameter(self):
        
        self.dat_dict = {}        
        
        try:
            with open(relative_path_to_abs("dat.config"),"rb") as f:
                self.dat_dict = json.load(f);
                print(self.dat_dict)
        except: #FileNotFoundError:
            self.dat_dict = {"op": "set", "cmd": "all", "tag": 0, "par": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
            print("init ")
            print(self.dat_dict)
        
        self.dat_op = StringVar()        
        self.dat_cmd = StringVar()
        self.dat_tag = IntVar()
        
        self.dat_op.set(self.dat_dict["op"])
        self.dat_cmd.set(self.dat_dict["cmd"])
        self.dat_tag.set(self.dat_dict["tag"])
        
        self.radvar = IntVar()
        self.radvar.set(100)
        
        self.datlen = 14
        self.datarr = {}
        
        for i in range(self.datlen):
            self.datarr[i] = IntVar()
            self.datarr[i].set(self.dat_dict["par"][i])
        
    def dat_decrypts(self):

        file = filedialog.askopenfilename(title='打开文件',filetypes=[("加密文件", "*.aes"),("全部文件","*.*")],initialdir=relative_path_to_abs(""))

        with open(file,"rb") as f:
            if self.key_second.get() == "":
                key = "1234567891234567"
            else:
                key = self.key.get()
            
            aes = crypt.aes_cipher(key)
            dat = aes.decrypt(f)                
            print(len(dat))
            
        json_dat = json.loads(dat)
        json_str = json.dumps(json_dat,indent=4)
        
        self.text_decode.delete(1.0,END)
        self.text_decode.insert(END,json_str)        
        
        
    def dat_configuration(self):
        
        json_dict = {"op":self.dat_op.get(),"cmd":self.dat_cmd.get(),"tag":self.dat_tag.get()}
        
        self.dat_dict["op"] = self.dat_op.get()
        self.dat_dict["cmd"] = self.dat_cmd.get()
        self.dat_dict["tag"] = self.dat_tag.get()
        
        if json_dict["op"] == "set":
            if json_dict["cmd"] == "all":
                datarr = [0]*self.datlen 
                
                for i in self.datarr:      
                    datarr[i] = self.datarr[i].get()  
                    self.dat_dict["par"][i] = datarr[i]
                    
                json_dict["par"] = datarr
            elif json_dict["cmd"] == "add":
                
                datarr = [0]*2
                
                datarr[0] = self.datarr[0].get() 
                datarr[1] = self.datarr[1].get() 
                
                self.dat_dict["par"][0] = datarr[0]
                self.dat_dict["par"][1] = datarr[1]
                json_dict["par"] = datarr
            elif json_dict["cmd"] == "single":
                
                try:
                    index = self.radvar.get()                
                    dat = self.datarr[index].get()  
                    json_dict["index"] = index
                    json_dict["par"] = dat
                    self.dat_dict["par"][index] = dat
                except KeyError:
                    messagebox.showwarning("错误","请选择一个要配置的参数")
                    return ""                      
        elif json_dict["op"] == "dump":  
            if json_dict["cmd"] == "all":
                pass
            elif json_dict["cmd"] == "single":
                pass
            elif json_dict["cmd"] == "tag":
                pass      
        
        with open(relative_path_to_abs("dat.config"),"w") as f:
            json.dump(self.dat_dict,f,indent=4)
        
        with open(relative_path_to_abs("dat.json"),"w") as f:
            json.dump(json_dict,f,indent=4)        
        
        json_str = json.dumps(json_dict)
        print(json_str)
        
        return json_str
    
    def dat_generate(self):
   
        json_str = self.dat_configuration()
        if json_str == "":
            return 
        
        if self.key_first.get() == "":
            key = "1234567891234567"
        else:
            key = self.key.get()

        
        aes = crypt.aes_cipher(key)

        encrypt_str = aes.encrypts(json_str)
        
        file = filedialog.asksaveasfilename(title='保存文件',initialfile   = "dat.json.aes",filetypes=[("加密文件", ".aes")],initialdir=relative_path_to_abs(""))
        if file == '':
            return
            
        with open(file,"wb") as f:
            dat = f.write(encrypt_str)                
        

app = application(title = "Tool")
app.run()