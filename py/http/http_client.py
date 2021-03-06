import requests
import sys

#HOST = "https://192.168.199.145:8000/"
#HOST = "https://localhost:8000/"

#certificate_file = './certificate.pem'
certificate_file = './cert.test.pem'


argc = len(sys.argv)
if argc < 2 :
    i = 0
else:
    i = int(sys.argv[1])

if i == 1:
    r = requests.get("https://localhost:8000/",verify=False)

    print(r.status_code)
    print(r.headers)
    print(r.text)
elif i == 2:
    r = requests.get("https://localhost:8000/cert",verify=certificate_file)

    print("----------------------------------")
    print(r.status_code)
    print("----------------------------------")
    print(r.headers)
    print("----------------------------------")
    print(r.text)

    try:
        with open("cert.test.pem","wb") as f:
            f.write(r.text)
    except Exception as e:
        print('{}: {}'.format(e.__class__.__name__, e))
    
elif i == 3:
    r = requests.get("http://localhost:8080/certificate.pem")
    
    print("----------------------------------")
    print(r.status_code)
    print("----------------------------------")
    print(r.headers)
    print("----------------------------------")
    print(r.text)

    try:
        with open("cert.test.pem","wb") as f:
            f.write(r.text.encode())
    except Exception as e:
        print('{}: {}'.format(e.__class__.__name__, e))
    
elif i == 4:
    r = requests.get("http://192.168.199.145:9000")
    
    print("----------------------------------")
    print(r.status_code)
    print("----------------------------------")
    print(r.headers)
    print("----------------------------------")
    print(r.text)
    
elif i == 5:
    r = requests.get("https://www.baidu.com")
    
    print("----------------------------------")
    print(r.status_code)
    print("----------------------------------")
    print(r.headers)
    print("----------------------------------")
    print(r.text)