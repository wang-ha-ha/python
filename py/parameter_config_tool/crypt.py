#pip install pycryptodome 安装AES 包

import os
import pickle
from Crypto.Cipher import AES
from binascii import hexlify,unhexlify

current_path = os.path.dirname(__file__)

def print_all(dat,str=""):
    pass
    #print("%s-->type:%s len:%s content:%s"%(str,type(dat),len(dat),dat))
   

    
class aes_cipher(object):
 
    def __init__(self, key,mode = AES.MODE_CBC):
        # self.key = hashlib.sha256(key).digest()
        # self.iv = self.key[:16]
        # key是16个字节，也就是128位 16*8
        # key可以是16*8=128, 24*8=192, 32*8=256位
        self.key = self.iv = self.add_to_16(key)
        self.encipher = AES.new(self.key, mode, self.iv)
        self.decipher = AES.new(self.key, mode, self.iv)
        
    def add_to_16(self,text):
        # 如果text不足16位的倍数就用空格补足为16位
        print_all(text)
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0
        text = text + ('\0' * add)
        return text.encode('utf-8')
        
    def encrypts(self, data):
        data = self.pkcs7padding(data)
        data = bytes(data.encode("utf-8"))        
        encrypted = self.encipher.encrypt(data)     
        return encrypted
    
    def encrypt(self, data , file):
        data = self.pkcs7padding(data)
        data = bytes(data.encode("utf-8"))        
        encrypted = self.encipher.encrypt(data)     
        file.write(encrypted)
 
    def decrypts(self, data):        
        decrypted = self.decipher.decrypt(data)
        decrypted = self.pkcs7unpadding(decrypted)        
        return decrypted
        
    def decrypt(self, file):        
        data = file.read()        
        decrypted = self.decipher.decrypt(data)
        decrypted = self.pkcs7unpadding(decrypted)        
        return decrypted
 
    def pkcs7padding(self, data):
        #AES.block_size 16位
        bs = AES.block_size
        padding = bs - len(data) % bs
        padding_text = chr(padding) * padding
        return data + padding_text
 
    def pkcs7unpadding(self, data):
        lengt = len(data)
        print_all(data,"pkcs7unpadding")
        unpadding = data[lengt - 1]
        return data[0:lengt-unpadding]


if __name__ == '__main__':

    key = "1234567891234567"	    
    aes = aes_cipher(key)
    
    with open(current_path+"\dat.aes","rb") as f:
        dat = f.read()
    print_all(dat)
    '''
    res = aes.encrypt(dat)
    print_all(res,"encrypt")
    print_all(hexlify(res),"encrypt-hex")
    '''
    result = aes.decrypt(dat)
    print_all(result,"decrypt")
    

