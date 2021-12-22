import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5 as PKCS1
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class RSACipher():
    '''
    RSA加密、解密、签名、验签工具类
    '''

    def encrypt(self, key, text):
        '''
        加密方法
        :param key: 公钥
        :param text: 需要加密的明文
        :return: 加密后的密文
        '''
        public_key = RSA.importKey(base64.b64decode(key))
        # cipher = PKCS1_OAEP.new(public_key)
        cipher = PKCS1.new(public_key)
        return base64.b64encode(cipher.encrypt(text.encode())).decode()

    def decrypt(self, key, text):
        '''
        解密方法
        :param key: 私钥
        :param text: 加密后的密文
        :return: 解密后的明文
        '''
        default_length = 117
        private_key = RSA.importKey(base64.b64decode(key))
        # cipher = PKCS1_OAEP.new(private_key,hashAlgo=SHA256)
        cipher = PKCS1.new(private_key)
        length = len(text)
        print("length:{}".format(length))
        encrypt_byte = base64.b64decode(text)
        length = len(encrypt_byte)
        print("length:{}".format(length))
        return cipher.decrypt(encrypt_byte,'failure').decode()
        print(text)
        encrypt_byte = base64.b64decode(text)
        length = len(encrypt_byte)
        print(length)
        if length < default_length:
            decrypt_byte = cipher.decrypt(encrypt_byte, 'failure')
        else:
            offset = 0
            res = []
            while length - offset > 0:
                if length - offset > default_length:
                    res.append(cipher.decrypt(encrypt_byte[offset: offset + 
                        default_length], 'failure'))
                else:
                    res.append(cipher.decrypt(encrypt_byte[offset:], 'failure'))
                offset += default_length
            decrypt_byte = b''.join(res)
        decrypted = decrypt_byte.decode()
        return decrypted

    def sign(self, key, text):
        '''
        签名方法
        :param key: 私钥
        :param text: 需要签名的文本
        :return: 签名信息
        '''
        private_key = RSA.importKey(base64.b64decode(key))
        hash_value = SHA256.new(bytes(text, encoding="utf-8"))
        signer = PKCS1_v1_5.new(private_key)
        signature = signer.sign(hash_value)
        return base64.b64encode(signature).decode()

    def verify(self, key, text, signature):
        '''
        验签方法
        :param key: 公钥
        :param text: 需要验签的文本
        :param signature: 签名信息
        :return: 验签结果
        '''
        public_key = RSA.importKey(base64.b64decode(key))
        hash_value = SHA256.new(bytes(text, encoding="utf-8"))
        verifier = PKCS1_v1_5.new(public_key)
        return verifier.verify(hash_value, base64.b64decode(signature))

if __name__ == '__main__':
    PUBLIC_KEY = '''
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3PasOFQfBGHs2S14cVZD
mN3A/idjU1pOK3HI9CxWjFpjwTACb/E8VVQK8/vr0ecVcBTktgQ2qbaUNQnA5f/K
uUb+ER5j8TbQEKtm4bMGar88aukDZmZzNqRMp/XnHAkjbeEVZyvSG91pUv5IJ8Rp
68/ylbPlaflcDXFMK0i9rvojP55tQ8iY/erEQa8dCl9mkKORRsrV8T8TTic5vOjI
RPBdzzElvk2Ma4y6wYIlsgewxqC+lTe8d1pI9aS78B8ahAb9ITFvbNqkWQbFJE+e
WfDJ3LfWrIVUNzZfRncQw1PInOA3nvgGGDRmKQVADeX5MX5MoQW8ob+6SLHPm1+z
HQIDAQAB
'''
    PRIVATE_KEY = '''
MIIEpQIBAAKCAQEA3PasOFQfBGHs2S14cVZDmN3A/idjU1pOK3HI9CxWjFpjwTAC
b/E8VVQK8/vr0ecVcBTktgQ2qbaUNQnA5f/KuUb+ER5j8TbQEKtm4bMGar88aukD
ZmZzNqRMp/XnHAkjbeEVZyvSG91pUv5IJ8Rp68/ylbPlaflcDXFMK0i9rvojP55t
Q8iY/erEQa8dCl9mkKORRsrV8T8TTic5vOjIRPBdzzElvk2Ma4y6wYIlsgewxqC+
lTe8d1pI9aS78B8ahAb9ITFvbNqkWQbFJE+eWfDJ3LfWrIVUNzZfRncQw1PInOA3
nvgGGDRmKQVADeX5MX5MoQW8ob+6SLHPm1+zHQIDAQABAoIBAQDB5zm0aKWba++z
mcJy+vdw41Cj956jG8EzQLPPCkWc/wlBE8dfwrtmSc0e1HjaB0Z5x+v4inQJtG4U
qQ19CF42/sSf8yJTH/2wUymCcF72OAFl9DsGlmsOjVmznwgDQ0Wy++2TTxIfX8o4
iWp6c1NcG2zO0EJHIAsWxNDJvxitvbQPS8aIuS5uZBiN6M61jkWMxczIERfzamcM
eAYh6nLMJFXgWzVIC+uHpJK5UfIbZxPmijIlX4ZkCEnjQG9uNdX9NgJn/G1E036F
r6S7aO060Z0ZhySZ2YoQAwvQrkfwc9ea/15F5BIufiBmz1/h579cd58nbvqu0qYT
ylSCsERlAoGBAPzsinrjV7LxwE7rsw+1s2/hfqT9wzeGUWDD/fr9oTeVK4zAoWLj
FAN5BFdEXrf9LRZQEIeNJ5Sag4E2SZKGuUjVaeMKdqb2bZXaGZ9uWJYcpjgXVLlv
1Ku7DtmfCe5xTIcLErvffTq+J6ItCIsMjQW/2pBEWFt3IMwYNWvuXZkPAoGBAN+m
oCIOm/JZMrYaQ5dJ+aygl1934Wd1mwwy5IJylu78OD1FGCa6wqainP8iXTImki73
JNCaoh2ZkUzIINL7YdImNjmCvLxt9xBZ6I5eu+J2UWA34gwrtSioibyhCclkoaL6
gb0NWqD2uMB0Z8IeG+5Yn4x84KY9EMzWkBt9FzkTAoGAXCDNUHX/O+9TXWv9jXti
IR7CQtcshM0oV1cM7J/2WYi8lEiWgK62W415R1BgMCTIh5gibT29bSPbQvXDVtw8
IYubRlhJYAfjYvJO4wQOwJ8u7L+S3PkfPm6kuiB0PaaHealO6aA+vWcGiMxekEfC
FpYLxwEeLjL2f2FSFD5/WYECgYEAhqroZVlyoX0AQhKSfHh4tG+Gdl/TA98W20OR
wNKK+6A3pP0Dy95M8tWbvyzL/TSodUsvicRytWwQx7EBwsjHYCjOIdcNGlEEoX3h
wEhezb/8w/kiTb3LuY2yUjiNkgzcHyzEDjgKSD4HhSsShxpmKyCGAav4AWFnyk+w
Oj0aTK0CgYEA0UZfircywHUmSkMENyQGtxEWtEGNIICnIHOo65UBGxdOhS/u5cw1
00B6BgwCTj9U7lLllPhFGk88H30b+LnoozkxIEjlo62SQa404QU+gXdqH+FrpsuB
jsYtrm8l460SJkD+KgpQcO9U1UeVxRBYfxGPtEsBPJxIrwXvPOJpAEU=
'''
    text = 'hellasdasdasdashesdasdasdasdasdohellasdasdasdasdasdasdasdohellasdasdasdasdasdasdasdohellasdasdasdasdasdasdasdohellasdasdasdasdasdasdasdohellasdasdasdasdasdasdasdodahellasdasdasdasdasdasdasdoshellasdasdasdasdasdasdasdodasdasdo'
    cipher = RSACipher()
    # 加密
    encrypt_text = cipher.encrypt(PUBLIC_KEY, text)
    print('加密后:\n%s' % encrypt_text)
    # 签名
    # signature = cipher.sign(PRIVATE_KEY, text)
    # print('签名:\n%s' % signature)
    # 解密
    decrypt_text = cipher.decrypt(PRIVATE_KEY, encrypt_text)
    print('解密后:\n%s' % decrypt_text)
    # 验签
    # result = cipher.verify(PUBLIC_KEY, decrypt_text, signature)
    # print('验签:\n%s' % result)

    encrypt_text = cipher.encrypt( PRIVATE_KEY, text)
    print('加密后:\n%s' % encrypt_text)
    # 签名
    # signature = cipher.sign(PRIVATE_KEY, text)
    # print('签名:\n%s' % signature)
    # 解密
    decrypt_text = cipher.decrypt(PUBLIC_KEY, encrypt_text)
    print('解密后:\n%s' % decrypt_text)