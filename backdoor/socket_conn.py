import socket

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('192.168.56.1', 8080))

str_data = "\n[+] Connection established.\n"

conn.send(str_data.encode())

received_data = conn.recv(1024)
print(received_data)

conn.close()
