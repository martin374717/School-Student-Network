from flet.security import encrypt, decrypt
import flet as ft
import os
import time
import socket
import random
import subprocess
import threading
import struct
import netifaces

def enc(data,key):
    return encrypt(data, key)

def dec(data,key):
    return decrypt(data,key)
def brdtcast_ip(addr):
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ipv4_info = addresses[netifaces.AF_INET][0]
            if ipv4_info["addr"] == addr and ipv4_info.get('broadcast'):
                return ipv4_info.get('broadcast')
def main(page: ft.Page):
    page.title = "School Student Network (Server)"
    page.window_resizable = True
    page.window_min_height = 670
    page.window_min_width = 800
    page.window_height = 670
    page.window_width = 800

    rnd_path_server = subprocess.run("powershell Get-Date -UFormat %s",capture_output=True,shell=True).stdout.decode().strip().replace(".","")

    temp = subprocess.run("echo %temp%",capture_output=True,shell=True).stdout.decode()
    temp = temp.strip()

    def server_build(name,ip,port,password):
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen()
        global ip_server
        global port_server
        global name_server
        global password_server
        password_server = password
        name_server = name
        ip_server = ip
        port_server = port


    def submit(name,ip,port,password):
        submit_btn.disabled = True
        submit_btn.update()
        try:
            scanner = name != "" and ip !="" and ip != "Select Your Network" and str(type(int(port))) == "<class 'int'>" and int(port) != 4747
        except:
            scanner = False

        if scanner == True:
            try:
                server_build(name,ip,int(port),password)
                PANEL()
            except:
                if auto_switch.value == True:
                    server_port.disabled = True
                    server_port.value = random.randint(60000,65000)
                    server_port.update()
                    submit_btn.disabled = False
                    submit_btn.update()
                    submit(name,server_ip.value,server_port.value)
                    return "error switch random port"
                else:
                    rols_error.visible = True
                    error.value = "Could not build the server!       "
                    error.update()
                    rols_error.update()
                    time.sleep(2)
                    rols_error.visible = False
                    error.value = "Please enter the correct entries!"
                    error.update()
                    rols_error.update()
        else:
            rols_error.visible = True
            rols_error.update()
            time.sleep(2)
            rols_error.visible = False
            rols_error.update()
        
        submit_btn.disabled = False
        submit_btn.update()

    def switch_auto(e):
        data = e.control.value
        if data == True:
            server_port.disabled = True
            server_port.value = random.randint(60000,65000)
            server_port.update()
        else:
            server_port.disabled = False
            server_port.value = ""
            server_port.update()
            

    def BUILD():
        page.clean()
        global error
        global rols_error
        global submit_btn
        global server_ip
        global server_port
        global auto_switch
        server_icon = ft.Icon(ft.icons.PODCASTS,size=100)
        server_name = ft.TextField(width=700,label="enter your server name",max_length=20)
        server_ip = ft.Dropdown(
            options=[
                ft.dropdown.Option("Select Your Network")
            ],
            width=480,
        )
        server_ip.value = "Select Your Network"

        host_name = socket.gethostname()
        ips = socket.gethostbyname_ex(host_name)[-1]

        for ip in ips:
            server_ip.options.append(ft.dropdown.Option(ip))
        server_port = ft.TextField(width=100,hint_text="port",text_align=ft.TextAlign.CENTER)
        server_port.disabled = True
        server_port.value = random.randint(60000,65000)
        auto_switch = ft.Switch(label="Auto",width=100,on_change=switch_auto,value=True)
        server_information = ft.Row(controls=[server_ip,server_port,ft.Row(controls=[auto_switch],height=57)],height=77,vertical_alignment=ft.CrossAxisAlignment.START)
        server_password = ft.TextField(width=700,label="enter your server password",password=True,can_reveal_password=True)
        error = ft.Text("Please enter the correct entries!",color=ft.colors.RED)
        rols_error = ft.Row(spacing=10,controls=[ft.Text(),error],visible=False)
        submit_btn = ft.Container(
            content=ft.Text("Submit",color=ft.colors.WHITE,size=17,weight=ft.FontWeight.W_400),
            alignment=ft.alignment.center,
            width=80,
            height=45,
            bgcolor=ft.colors.BLUE_GREY_900,
            border_radius=7,
            on_click=lambda e: submit(server_name.value,server_ip.value,server_port.value,server_password.value)
        )
        BODY = ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Row(controls=[server_icon,ft.Text("School Student Network (Server)",size=40)],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[]),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            server_name
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            server_information
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            server_password
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            ft.Row(controls=[rols_error,ft.Text("                                                                                                                        ")])
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(controls=[]),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            submit_btn
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ]
            )
        )

        def change_theme(e):
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                theme_btn.icon = ft.icons.SUNNY
                page.client_storage.set("theme","dark")
                page.update()
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                theme_btn.icon = ft.icons.NIGHTLIGHT
                page.client_storage.set("theme","light")
                page.update()

        theme_btn = ft.FloatingActionButton(icon=ft.icons.NIGHTLIGHT,on_click=change_theme)

        if page.client_storage.get("theme"):
            pass
        else:
            page.client_storage.set("theme","light")

        if page.client_storage.get("theme") == "light":
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_btn.icon = ft.icons.NIGHTLIGHT
            page.client_storage.set("theme","light")
            page.update()
        elif page.client_storage.get("theme") == "dark":
            page.theme_mode = ft.ThemeMode.DARK
            theme_btn.icon = ft.icons.SUNNY
            page.client_storage.set("theme","dark")
            page.update()

        page.add(BODY,theme_btn)
        page.update()

    def PANEL():
        page.clean()
        page.scroll = ft.ScrollMode.AUTO
        name =  ft.Text(value=name_server,selectable=True)
        
        if ip_server == "0.0.0.0":
            ip = ft.Text(selectable=True,value=ip_server)
            note = ft.Text(selectable=True,expand=True,value="Note : To use, send one of the IPs of your network card to the desired person")
            mode  = ft.Text(selectable=True,value="AUTO")
        elif ip_server[:3] == "127":
            ip = ft.Text(selectable=True,value=ip_server)
            note = ft.Text(selectable=True,expand=True,value="Note: This server is only available on your computer.")
            mode  = ft.Text(selectable=True,value="LOCAL")
        else:
            ip = ft.Text(selectable=True,value=ip_server)
            note = ft.Text(selectable=True,expand=True,value="Note: To use, send the server IP to the desired person")
            mode  = ft.Text(selectable=True,value="LAN")

        port = ft.Text(selectable=True,value=port_server)

        def change_theme(e):
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                theme_btn.icon = ft.icons.SUNNY
                page.client_storage.set("theme","dark")
                page.update()
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                theme_btn.icon = ft.icons.NIGHTLIGHT
                page.client_storage.set("theme","light")
                page.update()

        theme_btn = ft.IconButton(icon=ft.icons.NIGHTLIGHT,on_click=change_theme)

        if page.client_storage.get("theme"):
            pass
        else:
            page.client_storage.set("theme","light")

        if page.client_storage.get("theme") == "light":
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_btn.icon = ft.icons.NIGHTLIGHT
            page.client_storage.set("theme","light")
            page.update()
        elif page.client_storage.get("theme") == "dark":
            page.theme_mode = ft.ThemeMode.DARK
            theme_btn.icon = ft.icons.SUNNY
            page.client_storage.set("theme","dark")
            page.update()

        def logout_server(e):
            if e.data == "close":
                text_broadcast(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(3,name_server)}".encode(),server) # server destroyed message
                broadcast_server.sendto(f"{(5,ip_server,port_server,name_server)}".encode(), (brdtcast_ip(ip_server), 4747)) # server details broadcast (destory)
                for client in clients:
                    client.close()
                page.window_destroy()
            elif e.control.data == "btn":
                text_broadcast(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(3,name_server)}".encode(),server) # server destroyed message
                broadcast_server.sendto(f"{(5,ip_server,port_server,name_server)}".encode(), (brdtcast_ip(ip_server), 4747)) # server details broadcast (destory)
                for client in clients:
                    client.close()
                page.window_destroy()
        
        page.window_prevent_close = True
        page.on_window_event = logout_server

        logout_server_btn = ft.IconButton(ft.icons.LOGOUT,icon_color=ft.colors.RED,on_click=logout_server,data="btn")

        server_log = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(expand=True,value="Server Information :",size=20),
                        theme_btn,
                        logout_server_btn
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text("name :"),
                        name,
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text("ip :"),
                        ip,
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text("port :"),
                        port,
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text("mode :"),
                        mode,
                    ]
                ),
                ft.Row(
                    controls=[
                        note,
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text(expand=True,value="Your system IPs :",size=20)
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text(selectable=True,value=subprocess.run("ipconfig",capture_output=True).stdout.decode()),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Text(expand=True,value="Server Logs :",size=20)
                    ]
                )
            ]
        )

        BODY = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"sm": 2},
                    alignment=ft.alignment.top_center,
                    content=ft.Text(""),
                ),
                ft.Container(
                    col={"sm": 8},
                    content=server_log,
                    border=ft.border.all(2,ft.colors.BLUE_GREY_900),
                    padding=10
                ),
            ]
        )

        global clients
        clients = []
        global GIL
        GIL = []

        def text_broadcast(message,use):
            number = 0
            for client in clients:
                if client != use:
                    try:
                        client.send(message) # text message
                        time.sleep(0.7)
                        number += 1
                    except:
                        continue
            return number

        def file_broadcast(packet,file_path,use):
            number = 0
            for client in clients:
                if client != use:
                    try:
                        file_name = packet[1]
                        filesize = os.path.getsize(file_path)
                        buflen = struct.pack("<Q", filesize)
                        client.send(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(1,file_name,buflen,packet[3])}".encode()) # file message
                        with open(file_path, "rb") as f:
                            while read_bytes := f.read(1024):
                                client.sendall(read_bytes)
                        time.sleep(0.7)
                        number += 1
                    except:
                        continue
            return number
            

        def handle(client,client_address):
            global GIL
            while True:
                try:
                    message = client.recv(1024)
                    GIL.append(client)
                    while True:
                        if GIL[0] == client:
                            break
                        else:
                            time.sleep(1)
                            continue
                    tuples = message.decode().split("2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312")
                    tuples.pop(0)
                    for t in tuples:
                        packet = eval(t)
                        if packet[0] == 0:
                            server_log.controls.append(ft.Row(controls=[ft.Text(key="new",selectable=True,expand=True,value=f"{client_address[0]} ({packet[2]}) : {packet[1]}")]))
                            server_log.update()
                            server_log.scroll_to(key="new", duration=1000)
                            number_sended = text_broadcast(message,client)
                            if number_sended != 0:
                                client.send(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(4,number_sended,packet[3])}".encode()) # response message
                        elif packet[0] == 1:
                            try:
                                fmt = "<Q"
                                stream = bytes()
                                stream += packet[2]
                                filesize = struct.unpack(fmt, stream)[0]
                                received_bytes = 0
                                rnd_path_file = subprocess.run("powershell Get-Date -UFormat %s",capture_output=True,shell=True).stdout.decode().strip().replace(".","")
                                file_path = temp + f"\\SSN{rnd_path_server}\\{packet[3]}\\{rnd_path_file}{packet[1]}"
                                folder_path = os.path.dirname(file_path)
                                if not os.path.exists(folder_path):
                                    os.makedirs(folder_path)
                                with open(file_path, "wb") as f:
                                    received_bytes = 0
                                    while received_bytes < filesize:
                                        chunk = client.recv(1024)
                                        if chunk:
                                            f.write(chunk)
                                            received_bytes += len(chunk)
                                server_log.controls.append(ft.Row(controls=[ft.Text(key="new",selectable=True,expand=True,value=f"ftp {packet[1]} file transfered! to the server! from ---> {packet[3]}")]))
                                server_log.update()
                                server_log.scroll_to(key="new", duration=1000)
                                number_sended = file_broadcast(packet,file_path,client)
                                if number_sended != 0:
                                    client.send(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(4,number_sended,packet[4])}".encode()) # response message
                            except:
                                continue
                        elif packet[0] == 2:
                            server_log.controls.append(ft.Row(controls=[ft.Text(key="new",selectable=True,expand=True,value=f"{client_address[0]} ({packet[1]}) disconnected!")]))
                            server_log.update()
                            server_log.scroll_to(key="new", duration=1000)
                            text_broadcast(message,client)
                    GIL.remove(client)
                except:
                    clients.remove(client)
                    client.close()
                    break

        def receive():
            while True:
                try:
                    client, address = server.accept()
                    pass_ack = client.recv(1024).decode()
                    try:
                        dt = dec(pass_ack,password_server)
                        if dt == password_server:
                            client.send("yes!".encode())
                        else:
                            client.send("no!".encode())
                            client.close()
                            continue
                    except:
                        client.send("no!".encode())
                        client.close()
                        continue
                    clname = client.recv(1024).decode()
                    client.send(str((address,name_server)).encode())
                    clients.append(client)
                    if clname != "":
                        server_log.controls.append(ft.Row(controls=[ft.Text(key="new",selectable=True,expand=True,value=f"{address[0]} : {address[1]} connected to the server! name ---> {clname}")]))
                        server_log.update()
                        server_log.scroll_to(key="new", duration=1000)
                    thread = threading.Thread(target=handle, args=(client,address))
                    thread.start()
                except:
                    continue
        def server_details_broadcast():
            global broadcast_server
            
            broadcast_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            broadcast_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcast_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            broadcast_server.bind((ip_server, 4747))

            MESSAGE = f"{(4,ip_server,port_server,name_server)}".encode() # server details broadcast

            while True:
                broadcast_server.sendto(MESSAGE, (brdtcast_ip(ip_server), 4747))
                time.sleep(1)

        listen = threading.Thread(target=receive)
        listen.start()
        broadcast = threading.Thread(target=server_details_broadcast)
        broadcast.start()

        page.add(BODY)
        page.update()
        
    BUILD()
    
ft.app(target=main)