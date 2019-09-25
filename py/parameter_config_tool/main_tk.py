import os
import crypt 
import json
from tkinter import  *
from tkinter import ttk

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
         
        tabControl.pack(expand=1, fill="both",padx=5, pady=5) 
    def create_top_frame_first(self,p):
        top_frame = ttk.LabelFrame(p,text = "operation")       
        top_frame.pack(expand = False,fill="x",side = "top",padx=8, pady=4)
        
        self.dat_op = StringVar()
        self.dat_cmd = StringVar()
        self.dat_tag = IntVar()
              
        ttk.Label(top_frame, text = "op",width=3).grid(row=0, column=0,padx=8, pady=4)       
        temp = ttk.Combobox(top_frame,show=None,width=8, font=('Arial', 10),values = ("set","dump"),state='readonly',textvariable = self.dat_op)
        temp.grid(row=0, column=1)
        temp.current(0) 
        
        ttk.Label(top_frame, text = "cmd",width=4).grid(row=0, column=2,padx=8, pady=4) 
        temp = ttk.Combobox(top_frame,show=None,width=8, font=('Arial', 10),values = ("all","single","tag"),state='readonly',textvariable = self.dat_cmd)
        temp.grid(row=0, column=3)
        temp.current(0) 
        
        ttk.Label(top_frame, text = "tag",width=3).grid(row=0, column=4,padx=8, pady=4)       
        ttk.Entry(top_frame,show=None,width=8, font=('Arial', 10),textvariable = self.dat_tag).grid(row=0, column=5)
        
    def butn_test(self):
        
        print_all(self.dat_op.get())
        print_all(self.dat_cmd.get())
        print(self.dat_tag.get())
        print(self.radvar.get())
        
    def create_data_widget(self,parent,index,name,unit):        
    
        ttk.Label(parent, text = name,width=15).grid(row = index, column=0,padx=20)
        
        self.datarr[index] = IntVar()
        
        ttk.Entry(parent,show=None, font=('Arial', 10),foreground='red',textvariable = self.datarr[index]).grid(row = index, column=1,padx=8)
        
        ttk.Label(parent, text = unit,width=10).grid(row = index, column=2,padx=8)

        Radiobutton(parent,variable=self.radvar, value=index , command = self.butn_test).grid(row = index, column=3,padx=8)
        
    def create_mid_frame_first(self,p):
        mid_frame = ttk.LabelFrame(p,text = "information") 
        mid_frame.pack(expand = True,fill="both",side = "top",padx=8, pady=4)
        
        self.radvar = IntVar()
        self.radvar.set(100)
        
        self.datlen = 14
        self.datarr = {}
        
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
    
    def dat_generate(self):
        datarr = [0]*self.datlen
        
        for i in self.datarr:      
            #print(self.datarr[i].get(),end = " ")
            datarr[i] = self.datarr[i].get()        
        print()
        
        json_dict = {"op":self.dat_op.get(),"cmd":self.dat_cmd.get(),"tag":self.dat_tag.get()}
        json_dict["par"] = datarr
        
        json_file = open(relative_path_to_abs('dat.json'),'w')
        json.dump(json_dict,json_file,indent=4)
        json_file.close()
        
        
        if self.key.get() == "":
            key = "1234567891234567"
        else:
            key = self.key.get()

        json_str = json.dumps(json_dict)
        print(json_str)
        aes = crypt.aes_cipher(key)
        
        print("<---------->")
        
        encrypt_str = aes.encrypts(json_str)
        print(encrypt_str)
        decrypt_str = aes.decrypts(encrypt_str)
        print(decrypt_str)
        print("<---------->")
        

        with open(relative_path_to_abs("dat.json.aes"),"wb") as f:
            dat = f.write(encrypt_str)        

        with open(relative_path_to_abs("dat.json.aes"),"rb") as f:
            dat = f.read()
        print(dat)
        decrypt_str = aes.decrypts(dat)
        print(decrypt_str)

        print("<---------->")
        
    def create_bot_frame_first(self,p):
    
        bot_frame = ttk.LabelFrame(p,text = "sys") 
        bot_frame.pack(expand = True,fill="x",side = "top",padx=8, pady=4)
        
        quitButton = ttk.Button(bot_frame, style="R.TButton",text='Quit', command=self.quit)
        quitButton["state"] = "enable"
        quitButton.pack(side = "right") 
        
        quitButton = ttk.Button(bot_frame, style="R.TButton",text='生成', command=self.dat_generate)
        quitButton["state"] = "enable"
        quitButton.pack(side = "right",padx=10) 
        
        self.key = StringVar()
        ttk.Label(bot_frame, text = "key").pack(side = "left",padx=8)
        ttk.Entry(bot_frame,show=None, font=('Arial', 10),textvariable = self.key).pack(side = "left",padx=10)
        

app = application(title = "Tool")
app.run()