# A simple multiplayer minecraft with ursina
<center class="half">
  <img src="https://github.com/lujiazho/pythonGadget/blob/main/minecraft_multiplayer/minecraft_multiplayer.gif" width="600"/>
</center>

# Run
The server(server.py) and client(main.py) should be under the same LAN (such as the same wifi)
- Run server.py first, then get the computer's IP address of server.py (win+R -> ipconfig ...)
- Modify the line of 127 in main.py before running it.

```py
# this should be the server's IP
server_addr = input("Enter server IP: ") if False else '192.168.1.217' 
# server's default port is 8000 so you may not need to change it
server_port = input("Enter server port: ") if False else '8000' 
```
- Run another main.py on the same computer or another one which is within the same LAN
