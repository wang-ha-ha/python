import requests


#HOST = "https://192.168.199.145:8000/"

HOST = "https://localhost:8000/"
certificate_file = './certificate.pem'


r = requests.get(HOST,verify=certificate_file)

print(r.status_code)
print(r.headers)
print(r.text)