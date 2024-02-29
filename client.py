from flet.security import encrypt, decrypt
import flet as ft
import os
import time
import socket
import threading
import random
import struct
from notifypy import Notify
import subprocess
from tendo import singleton
import sys

try:
    application = singleton.SingleInstance()
except:
    sys.exit(-1)

def enc(data,key):
    return encrypt(data, key)

def dec(data,key):
    return decrypt(data,key)

def main(page: ft.Page):
    page.title = "School Student Network (Client)"
    page.window_min_height = 670
    page.window_min_width = 800
    page.window_height = 670
    page.window_width = 800

    rnd_path_client = subprocess.run("powershell Get-Date -UFormat %s",capture_output=True,shell=True).stdout.decode().strip().replace(".","")

    temp = subprocess.run("echo %temp%",capture_output=True,shell=True).stdout.decode()
    temp = temp.strip()

    def CLIENT(client_name,server_ip,server_port,server_password):
        page.clean()
        
        chat = ft.ListView(expand=True, spacing=10, width=page.width-30)
        def change_resize_page(e):
            chat.width = page.width-30
            chat.update()
        page.on_resize = change_resize_page
        global client_ip
        global server_name
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        client_socket.send(str(enc(server_password,server_password)).encode())
        pass_res_ack = client_socket.recv(1024)
        if pass_res_ack.decode() == "yes!":
            pass
        else:
            page.window_destroy()
        found_server.close()
        client_socket.send(str(client_name).encode())
        server_data = eval(client_socket.recv(1024).decode())
        client_ip = server_data[0][0]
        client_port = server_data[0][1]
        server_name = server_data[1]

        def yes_click(e):
            try:
                client_socket.send(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(2,client_name)}".encode()) # disconnect message
                page.window_destroy()
            except:
                page.window_destroy()

        def no_click(e):
            confirm_dialog.open = False
            page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to exit this app?"),
            actions=[
                ft.ElevatedButton("Yes", on_click=yes_click),
                ft.OutlinedButton("No", on_click=no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def window_event(e):
            if e.data == "close":
                page.dialog = confirm_dialog
                confirm_dialog.open = True
                page.update()

        page.window_prevent_close = True
        page.on_window_event = window_event

        def on_keyboard(e: ft.KeyboardEvent):
            if e.alt == True and e.key == "T":
                if page.client_storage.get("theme") == "light":
                    page.theme_mode = ft.ThemeMode.DARK
                    change_theme_button.icon = ft.icons.SUNNY
                    page.client_storage.set("theme", "dark")
                    page.update()
                else:
                    page.theme_mode = ft.ThemeMode.LIGHT
                    change_theme_button.icon = ft.icons.NIGHTLIGHT
                    page.client_storage.set("theme", "light")
                    page.update()

            elif e.shift == True and e.key == "Tab":
                if message_field.multiline == False:
                    message_field.value = ""
                    message_field.multiline = True
                    message_field.prefix_icon = ft.icons.ARTICLE_OUTLINED
                    message_field.focus()
                    message_field.update()
                elif message_field.multiline == True:
                    message_field.value = ""
                    message_field.multiline = False
                    message_field.prefix_icon = None
                    message_field.focus()
                    message_field.update()

        page.on_keyboard_event = on_keyboard

        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]

        information = [client_name,client_ip,colors_lookup[hash(client_name) % len(colors_lookup)],server_name,server_ip,server_port,client_port]
        information_server_btn = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text=f"your name : {information[0]}"),
                ft.PopupMenuItem(text=f"your ip : {information[1]}"),
                ft.PopupMenuItem(text=f"your port : {information[6]}"),
                ft.PopupMenuItem(text=f"your message color : {information[2]}"),
                ft.PopupMenuItem(text=f"server name : {information[3]}"),
                ft.PopupMenuItem(text=f"server ip : {information[4]}"),
                ft.PopupMenuItem(text=f"server port : {information[5]}"),
            ],
            icon=ft.icons.INFO_OUTLINED
        )
        if page.client_storage.get("theme"):
            pass
        else:
            page.client_storage.set("theme", "light")
        
        def change_theme(e):
            if page.client_storage.get("theme") == "light":
                page.theme_mode = ft.ThemeMode.DARK
                change_theme_button.icon = ft.icons.SUNNY
                page.client_storage.set("theme", "dark")
                page.update()
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                change_theme_button.icon = ft.icons.NIGHTLIGHT
                page.client_storage.set("theme", "light")
                page.update()

        change_theme_button = ft.IconButton(ft.icons.NIGHTLIGHT,on_click=change_theme)

        if page.client_storage.get("theme") == "light":
            page.theme_mode = ft.ThemeMode.LIGHT
            change_theme_button.icon = ft.icons.NIGHTLIGHT
            page.client_storage.set("theme", "light")
            page.update()
        elif page.client_storage.get("theme") == "dark":
            page.theme_mode = ft.ThemeMode.DARK
            change_theme_button.icon = ft.icons.SUNNY
            page.client_storage.set("theme", "dark")
            page.update()

        def close_server(e):
            try:
                client_socket.send(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(2,client_name)}".encode()) # disconnect message
                page.window_destroy()
            except:
                page.window_destroy()

        close_server_btn = ft.IconButton(ft.icons.LOGOUT,icon_color=ft.colors.RED,on_click=close_server)
        page.appbar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(controls=[ft.Text("    "),ft.Icon(ft.icons.GROUPS,size=30),ft.Text(f"{server_name}",size=25)],expand=True),
                    change_theme_button,
                    information_server_btn,
                    close_server_btn,
                    ft.Text("")
                ],
                expand=True
            ),
            border=ft.border.all(1,ft.colors.BLUE_GREY_900),
            padding=ft.Padding(bottom=7,top=7,right=0,left=0),
            border_radius=7
        )
        page.update()

        def receive():
            colors_lookup = [
                ft.colors.AMBER,
                ft.colors.BLUE,
                ft.colors.BROWN,
                ft.colors.CYAN,
                ft.colors.GREEN,
                ft.colors.INDIGO,
                ft.colors.LIME,
                ft.colors.ORANGE,
                ft.colors.PINK,
                ft.colors.PURPLE,
                ft.colors.RED,
                ft.colors.TEAL,
                ft.colors.YELLOW,
            ]
            while True:
                try:
                    try:
                        message = client_socket.recv(1024).decode().split("2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312")
                        message.pop(0)
                        for t in message:
                            packet = eval(t)
                    except WindowsError:
                        obj_message = ft.Text(value="  your connection to the server has been disconnected!",selectable=True,key="new")
                        chat.controls.append(obj_message)
                        chat.update()
                        chat.scroll_to(key="new", duration=1000)
                        message_field.value = ""
                        message_field.focus()
                        message_field.update()
                        field_message.disabled = True
                        field_message.update()
                        time.sleep(0.4)
                        field_message.disabled = False
                        field_message.update()
                        break
                    except:
                        obj_message = ft.Text(value="  error receiving message!",color=ft.colors.RED,key="new")
                        chat.controls.append(obj_message)
                        chat.update()
                        chat.scroll_to(key="new", duration=1000)
                        message_field.value = ""
                        message_field.focus()
                        message_field.update()
                        field_message.disabled = True
                        field_message.update()
                        time.sleep(0.4)
                        field_message.disabled = False
                        field_message.update()
                        continue
                    for t in message:
                        packet = eval(t)
                        if packet[0] == 0:
                            obj_message = ft.Row(
                                controls=[
                                    ft.CircleAvatar(
                                        content=ft.Text(f"{packet[2][0:1]}".upper()),
                                        color=ft.colors.WHITE,
                                        bgcolor=colors_lookup[hash(packet[2]) % len(colors_lookup)],
                                        width=70
                                    ),
                                    ft.Column(
                                        expand=True,
                                        controls=[
                                            ft.Text(value=f"{packet[2]}", weight="bold"),
                                            ft.Text(value=f"{packet[1]}\n", selectable=True),
                                        ],
                                        tight=True,
                                        spacing=5,
                                    ),
                                ],
                                expand=True,
                                key="new"
                            )
                            chat.controls.append(obj_message)
                            chat.update()
                            chat.scroll_to(key="new", duration=1000)
                            if page.window_focused == False or page.window_minimized == True:
                                notification = Notify()
                                notification.application_name = "School Student Network"
                                notification.title = f"{packet[2]}"
                                notification.message = f"{packet[1]}"
                                notification.audio = r"SSN Data\\notification.wav"
                                notification.icon = r"SSN Data\\client.ico"
                                notification.send()
                        elif packet[0] == 1:
                            try:
                                fmt = "<Q"
                                stream = bytes()
                                stream += packet[2]
                                filesize = struct.unpack(fmt, stream)[0]
                                received_bytes = 0
                                rnd_path_file = subprocess.run("powershell Get-Date -UFormat %s",capture_output=True,shell=True).stdout.decode().strip().replace(".","")
                                file_path = temp + f"\\SSNC{rnd_path_client}\\{packet[3]}\\{rnd_path_file}{packet[1]}"
                                folder_path = os.path.dirname(file_path)
                                if not os.path.exists(folder_path):
                                    os.makedirs(folder_path)
                                with open(file_path, "wb") as f:
                                    received_bytes = 0
                                    while received_bytes < filesize:
                                        chunk = client_socket.recv(1024)
                                        try:
                                            resp = chunk.decode().split("2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312")
                                            resp.pop(0)
                                            for t in resp:
                                                resp_packet = eval(t)
                                                if resp_packet[0] == 4:
                                                    time.sleep(1)
                                                    index = resp_packet[2]
                                                    chat.controls[index].controls[1].controls[0].controls[2].value = str(int(chat.controls[index].controls[1].controls[0].controls[2].value) + resp_packet[1])
                                                    page.update()
                                        except:
                                            pass
                                        if chunk:
                                            f.write(chunk)
                                            received_bytes += len(chunk)
                                obj_file = ft.Row(
                                    controls=[
                                        ft.CircleAvatar(
                                            content=ft.Text(f"{packet[3][0:1]}".upper()),
                                            color=ft.colors.WHITE,
                                            bgcolor=colors_lookup[hash(packet[3]) % len(colors_lookup)],
                                            width=70
                                        ),
                                        ft.Column(
                                            expand=True,
                                            controls=[
                                                ft.Text(value=f"{packet[3]}", weight="bold"),
                                                ft.Row(
                                                    controls=[
                                                        ft.IconButton(data={"name":packet[1],"path":file_path,"extension":os.path.splitext(packet[1])[1]},icon_color=colors_lookup[hash(client_name) % len(colors_lookup)],icon=ft.icons.FILE_DOWNLOAD,on_click=lambda e: save_file(e.control.data)),
                                                        ft.Text(expand=True,selectable=True,value=packet[1])
                                                    ]
                                                )
                                            ],
                                            tight=True,
                                            spacing=5,
                                        ),
                                    ],
                                    expand=True,
                                    key="new"
                                )
                                chat.controls.append(obj_file)
                                chat.update()
                                chat.scroll_to(key="new", duration=1000)
                                if page.window_focused == False or page.window_minimized == True:
                                    notification = Notify()
                                    notification.application_name = "School Student Network"
                                    notification.title = f"{packet[3]}"
                                    notification.message = f"{packet[1]}"
                                    notification.audio = r"SSN Data\\notification.wav"
                                    notification.icon = r"SSN Data\\client.ico"
                                    notification.send()
                            except:
                                continue
                        elif packet[0] == 2:
                            obj_message = ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Text(selectable=True,value=f"  {packet[1]} disconnected!"),
                                            ]
                                        )
                                    )
                                ],
                                key="new"
                            )
                            chat.controls.append(obj_message)
                            chat.update()
                            chat.scroll_to(key="new", duration=1000)
                            if page.window_focused == False or page.window_minimized == True:
                                notification = Notify()
                                notification.application_name = "School Student Network"
                                notification.title = f"{packet[1]}"
                                notification.message = f"  {packet[1]} disconnected!"
                                notification.audio = r"SSN Data\\notification.wav"
                                notification.icon = r"SSN Data\\client.ico"
                                notification.send()
                        elif packet[0] == 3:
                            obj_message = ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Text(selectable=True,value=f"  server ({packet[1]}) destroyed!"),
                                            ]
                                        )
                                    )
                                ],
                                key="new"
                            )
                            chat.controls.append(obj_message)
                            chat.update()
                            chat.scroll_to(key="new", duration=1000)
                            if page.window_focused == False or page.window_minimized == True:
                                notification = Notify()
                                notification.application_name = "School Student Network"
                                notification.title = f"{packet[1]}"
                                notification.message = f"  server ({packet[1]}) destroyed!"
                                notification.audio = r"SSN Data\\notification.wav"
                                notification.icon = r"SSN Data\\client.ico"
                                notification.send()
                        elif packet[0] == 4:
                            time.sleep(1)
                            index = packet[2]
                            chat.controls[index].controls[1].controls[0].controls[2].value = str(int(chat.controls[index].controls[1].controls[0].controls[2].value) + packet[1])
                            page.update()
                except:
                    page.window_destroy()

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        def send(e):
            if message_field.value:
                try:
                    colors_lookup = [
                        ft.colors.AMBER,
                        ft.colors.BLUE,
                        ft.colors.BROWN,
                        ft.colors.CYAN,
                        ft.colors.GREEN,
                        ft.colors.INDIGO,
                        ft.colors.LIME,
                        ft.colors.ORANGE,
                        ft.colors.PINK,
                        ft.colors.PURPLE,
                        ft.colors.RED,
                        ft.colors.TEAL,
                        ft.colors.YELLOW,
                    ]
                    obj_message = ft.Row(
                        controls=[
                            ft.CircleAvatar(
                                content=ft.Text(f"{client_name[0:1]}".upper()),
                                color=ft.colors.WHITE,
                                bgcolor=colors_lookup[hash(client_name) % len(colors_lookup)],
                                width=70
                            ),
                            ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(controls=[ft.Text(value=f"{client_name} (you) ", weight="bold"),ft.Icon(ft.icons.GROUP,size=20),ft.Text("0")]),
                                    ft.Text(value=f"{message_field.value}\n", selectable=True),
                                ],
                                tight=True,
                                spacing=5,
                            ),
                        ],
                        expand=True,
                        key="new"
                    )
                    chat.controls.append(obj_message)
                    chat.update()
                    chat.scroll_to(key="new", duration=1000)
                    client_socket.send(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(0,message_field.value,client_name,len(chat.controls)-1)}".encode()) # text message
                    message_field.value = ""
                    message_field.focus()
                    message_field.update()
                    field_message.disabled = True
                    field_message.update()
                    time.sleep(0.7)
                    field_message.disabled = False
                    field_message.update()
                except:
                    message_field.value = ""
                    message_field.focus()
                    message_field.update()
                    field_message.disabled = True
                    field_message.update()
                    time.sleep(1)
                    index = len(chat.controls)-1
                    chat.controls[index].controls[1].controls[0].controls[2].value = "❌  message not send!"
                    chat.controls[index].controls[1].controls[0].controls[2].color = ft.colors.RED
                    page.update()
                    time.sleep(0.4)
                    field_message.disabled = False
                    field_message.update()
            else:
                pass

        def save_file_to_path(e: ft.FilePickerResultEvent):
            file_path_field.value = e.path
            file_path_field.update()
        

        file_path_save = ft.FilePicker(on_result=save_file_to_path)
        
        def save_file(data):
            global file_path_field

            def name_and_ext():
                global ext_name
                ext_name = file_name.value + data["extension"]
            file_extension = data["extension"]
            file_name = ft.TextField(label="enter your file name",max_length=40,suffix_text=f"{file_extension}",on_change=lambda e: name_and_ext())
            file_name.value = os.path.splitext(data["name"])[0]
            file_path_field = ft.TextField(label="enter the folder path",expand=True)
            text_error = ft.Text("Please enter the correct folder path!",color=ft.colors.RED)
            file_path_field_error = ft.Row(controls=[text_error],visible=False)

            file_path = ft.TextButton(text="Browse",on_click=file_path_save.get_directory_path)
            name_and_ext()

            obj = ft.ResponsiveRow(
                controls=
                [
                    file_name,
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[file_path_field,file_path]),
                    file_path_field_error
                ]
            )

            def save():
                try:
                    if file_name.value != "":
                        if file_path_field.value != "":
                            path = file_path_field.value + "\\" + ext_name
                            subprocess.call(["copy",data["path"],path], shell=True)
                            page.dialog = dlg_modal
                            dlg_modal.open = False
                            page.update()
                        else:
                            text_error.value = "Please enter the correct folder path!"
                            text_error.update()
                            raise Exception("path is not currect!")
                    else:
                        text_error.value = "Please enter the correct name!"
                        text_error.update()
                        raise( Exception("name is not currect!"))
                except:
                    file_path_field_error.visible = True
                    file_path_field_error.update()
                    time.sleep(2)
                    file_path_field_error.visible = False
                    file_path_field_error.update()
                    text_error.value = "Please enter the correct folder path!"
                    text_error.update()

            stdo = data["name"]
            dlg_modal = ft.AlertDialog(
                title=ft.Text(text_align=ft.TextAlign.CENTER,value=f"Save the {stdo} file"),
                content=obj,
                actions=[
                    ft.Text(text_align=ft.TextAlign.CENTER,value="                                        "),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[ft.OutlinedButton(width=90,text="cancel", on_click=lambda e:cancel()),ft.OutlinedButton(width=90,text="save", on_click=lambda e:save())]),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: cancel(),
            )
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()
            
            def cancel():
                page.dialog = dlg_modal
                dlg_modal.open = False
                page.update()

        def file_pick(e: ft.FilePickerResultEvent):
            try:
                field_message.disabled = True
                field_message.update()
                try:
                    with open(e.files[0].path,"rb") as f:
                        data_file = f.read()
                except:
                    field_message.disabled = False
                    field_message.update()
                    return 0
                file_name = e.files[0].name
                file_extension = os.path.splitext(e.files[0].name)[1]
                filesize = os.path.getsize(e.files[0].path)
                buflen = struct.pack("<Q", filesize)
                rnd_path_file = subprocess.run("powershell Get-Date -UFormat %s",capture_output=True,shell=True).stdout.decode().strip().replace(".","")
                file_path = temp + f"\\SSNC{rnd_path_client}\\admin(you){rnd_path_client}\\{rnd_path_file}{file_name}"
                folder_path = os.path.dirname(file_path)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                subprocess.call(["copy",e.files[0].path,file_path], shell=True)
                colors_lookup = [
                    ft.colors.AMBER,
                    ft.colors.BLUE,
                    ft.colors.BROWN,
                    ft.colors.CYAN,
                    ft.colors.GREEN,
                    ft.colors.INDIGO,
                    ft.colors.LIME,
                    ft.colors.ORANGE,
                    ft.colors.PINK,
                    ft.colors.PURPLE,
                    ft.colors.RED,
                    ft.colors.TEAL,
                    ft.colors.YELLOW,
                ]
                obj_file = ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Text(f"{client_name[0:1]}".upper()),
                            color=ft.colors.WHITE,
                            bgcolor=colors_lookup[hash(client_name) % len(colors_lookup)],
                            width=70
                        ),
                        ft.Column(
                            expand=True,
                            controls=[
                                ft.Row(controls=[ft.Text(value=f"{client_name} (you) ", weight="bold"),ft.Icon(ft.icons.GROUP,size=20),ft.Text("0")]),
                                ft.Row(
                                    controls=[
                                        ft.IconButton(data={"name":file_name,"path":file_path,"extension":file_extension},icon_color=colors_lookup[hash(client_name) % len(colors_lookup)],icon=ft.icons.FILE_DOWNLOAD,on_click=lambda e: save_file(e.control.data)),
                                        ft.Text(expand=True,selectable=True,value=e.files[0].name)
                                    ]
                                )
                            ],
                            tight=True,
                            spacing=5,
                        ),
                    ],
                    expand=True,
                    key="new"
                )
                chat.controls.append(obj_file)
                chat.update()
                chat.scroll_to(key="new", duration=1000)
                client_socket.send(f"2d14ab97cc3dc294c51c0d6814f4ea45f4b4e312{(1,file_name,buflen,client_name,len(chat.controls)-1)}".encode()) # file message
                with open(e.files[0].path, "rb") as f:
                    while read_bytes := f.read(1024):
                        client_socket.sendall(read_bytes)
                time.sleep(2)
                field_message.disabled = False
                field_message.update()
            except:
                message_field.focus()
                message_field.update()
                field_message.disabled = True
                field_message.update()
                time.sleep(1)
                index = len(chat.controls)-1
                chat.controls[index].controls[1].controls[0].controls[2].value = "❌   file not send!"
                chat.controls[index].controls[1].controls[0].controls[2].color = ft.colors.RED
                page.update()
                time.sleep(0.4)
                field_message.disabled = False
                field_message.update()
        

        file_picker = ft.FilePicker(on_result=file_pick)

        message_field = ft.TextField(expand=True,label="Write a message...",on_submit=send,max_lines=2,max_length=700)
        global field_message
        field_message = ft.Row(
            controls=
            [
                message_field,
                ft.IconButton(icon=ft.icons.FILE_OPEN,icon_size=40,on_click=file_picker.pick_files),
                ft.IconButton(icon=ft.icons.SEND_ROUNDED,icon_size=40,on_click=send)
            ],
            vertical_alignment=ft.CrossAxisAlignment.START
        )

        page.add(ft.Container(
            expand=True,
            content=ft.Row(
                expand=True,
                controls={
                    ft.Column(
                        controls=[
                            ft.Text(""),
                            chat
                        ]
                    )
                }
            ),
            border=ft.border.all(1,ft.colors.BLUE_GREY_900),
            border_radius=7
        ),field_message,file_picker,file_path_save)
        page.update()

    def HOST():
        page.clean()
        page.appbar = None

        def submit(name,ip,port,password):
            try:
                scanner = name != "" and ip !="" and str(type(int(port))) == "<class 'int'>"
            except:
                scanner = False
            if scanner == True:
                try:
                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server.connect((ip, int(port)))
                    server.send(str(enc(password,password)).encode())
                    pass_res_ack = server.recv(1024)
                    if pass_res_ack.decode() == "yes!":
                        server.close()
                        CLIENT(name,ip,int(port),password)
                    else:
                        server.close()
                        raise Exception("password is not true!")
                except:
                    ROLS_ERROR.visible = True
                    ERROR.value = "Could not connect to the server"
                    ERROR.update()
                    ROLS_ERROR.update()
                    time.sleep(2)
                    ROLS_ERROR.visible = False
                    ERROR.value = "Please enter the correct entries!"
                    ERROR.update()
                    ROLS_ERROR.update()
            else:
                ROLS_ERROR.visible = True
                ROLS_ERROR.update()
                time.sleep(2)
                ROLS_ERROR.visible = False
                ROLS_ERROR.update()
        
        FOUNDED_SERVER = ft.DataTable(
            column_spacing=100,
            columns=[
                ft.DataColumn(ft.Text("ip")),
                ft.DataColumn(ft.Text("port"), numeric=True),
                ft.DataColumn(ft.Text("name")),
                ft.DataColumn(ft.Text("connect")),
            ],
            rows=[],
            data=[],
            expand=True
        )

        founded_list = ft.ListView(expand=True,controls=[FOUNDED_SERVER],height=150)

        def set_prompt(ip,port):
            IP.value = ip
            PORT.value = port
            IP.update()
            PORT.update()
            NAME.focus()
            page.window_width = 800
            page.window_height = 670
            page.update()
        
        def found_servers():
            global found_server
            found_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            found_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            found_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            found_server.bind(("0.0.0.0", 4747))

            while True:
                try:
                    data, addr = found_server.recvfrom(1024)
                    packet = eval(data)
                    if packet[0] == 4 and packet[1] != "" and packet[2] != None and packet[3] != "":
                        data_server_connect_details = ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(packet[1]))),
                                ft.DataCell(ft.Text(int(packet[2]))),
                                ft.DataCell(ft.Text(str(packet[3]))),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text("import",color=ft.colors.WHITE,size=14,weight=ft.FontWeight.W_400),
                                        alignment=ft.alignment.center,
                                        width=70,
                                        height=35,
                                        bgcolor=ft.colors.BLUE_GREY_900,
                                        border_radius=7,
                                        on_click=lambda e: set_prompt(packet[1],packet[2])
                                    )
                                ),
                            ],
                        )
                        if packet not in FOUNDED_SERVER.data:
                            FOUNDED_SERVER.rows.append(
                                data_server_connect_details
                            )
                            FOUNDED_SERVER.data.append(packet)
                            FOUNDED_SERVER.update()
                        else:
                            pass
                    elif packet[0] == 5 and packet[1] != "" and packet[2] != None and packet[3] != "":
                        if (4,packet[1],packet[2],packet[3]) in FOUNDED_SERVER.data:
                            index = FOUNDED_SERVER.data.index((4,packet[1],packet[2],packet[3]))
                            FOUNDED_SERVER.rows.pop(index)
                            FOUNDED_SERVER.data.pop(index)
                            FOUNDED_SERVER.update()
                        else:
                            pass
                except:
                    break

        found = threading.Thread(target=found_servers)
        found.start()

        IP = ft.TextField(width=616,label="ip")
        PORT = ft.TextField(hint_text="port",width=75,text_align=ft.TextAlign.CENTER)
        NAME = ft.TextField(label="enter your name",width=700)
        PASS = ft.TextField(label="enter server password",width=700,password=True,can_reveal_password=True)
        ERROR = ft.Text("Please enter the correct entries!",color=ft.colors.RED)
        ROLS_ERROR = ft.Row(spacing=10,controls=[ft.Text(),ERROR],visible=False)
        
        submit_btn = ft.Container(
            content=ft.Text("Submit",color=ft.colors.WHITE,size=17,weight=ft.FontWeight.W_400),
            alignment=ft.alignment.center,
            width=80,
            height=45,
            bgcolor=ft.colors.BLUE_GREY_900,
            border_radius=7,
            on_click=lambda e: submit(NAME.value,IP.value,PORT.value,PASS.value)
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

        BODY = ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Row(controls=[ft.Icon(ft.icons.PERSON,size=100),ft.Text("School Student Network (Client)",size=40)],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[]),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            ft.Container(
                                width=700,
                                content=founded_list,
                                border=ft.border.all(1,ft.colors.BLUE_GREY_900),
                                border_radius=7
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(controls=[]),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            NAME
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            IP,PORT
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            PASS
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        col={"sm": 40},
                        controls=[
                            ft.Row(controls=[ROLS_ERROR,ft.Text("                                                                                                                        ")])
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

        page.add(BODY,theme_btn)
        page.update()

    HOST()
    
ft.app(target=main)