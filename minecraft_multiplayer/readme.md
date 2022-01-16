# A simple multiplayer minecraft with ursina

# Run
The server(server.py) and client(main.py) should be under the same LAN (such as the same wifi)
- Run server.py first
 - get the computer's IP of server.py
- Modify the line of 127 in main.py before running it.
'''
    server_addr = input("Enter server IP: ") if False else '192.168.1.217' # this should be the server's IP
    server_port = input("Enter server port: ") if False else '8000' # server's default port is 8000 so you may not need to change it
'''
- Run another main.py on the same computer or another one which is inside the same LAN