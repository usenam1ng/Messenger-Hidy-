import rsa
import datetime
import customtkinter as CTk
from PIL import Image
import json
import socket
import os
import hashlib
import viginere
import time
import threading

global login_check
login_check = False

global ping_ans
ping_ans = ""

global name_text_dict
name_text_dict = {}

global logn
logn = ""

global lets_ping
lets_ping = ""

class ServerRequestSender:
    def __init__(self):
        def send_server_request():
            global ping_ans
            global logn
            global name_text_dict
            host="127.0.0.1"
            port=6575
            while True:
                if logn != "" and lets_ping != "":
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        try:
                            message = '~ping~ + ' + logn
                            s.connect((host, port))
                            print("Connection done!")
                            s.sendall(message.encode())
                            resp = s.recv(1024).decode()
                            ans = resp.split('+')
                            if ans[0] != "":
                                #name_text_dict[ans[0]] = (ans[0] + '---' + ans[1])
                                pass
                        except Exception as e:
                            print(f"Error occurred: {e}")

                    time.sleep(100)

        request_thread = threading.Thread(target=send_server_request)
        request_thread.daemon = True
        request_thread.start()


class App(CTk.CTk):
    def __init__(self):
        print("Interface loaded!")
        super().__init__()
        global realtime_user
        realtime_user = ""

        global password
        password = ""

        global userto
        userto = ""

        self.server_request_sender = ServerRequestSender()


        def sha256(input_string):
            sha256_hash = hashlib.sha256()
            sha256_hash.update(input_string.encode('utf-8'))
            return sha256_hash.hexdigest()


        def send_tcp_message(message, host="127.0.0.1", port=6575):
            # Создаем сокет
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Устанавливаем соединение с сервером
                s.connect((host, port))
                print("Connection done!")
                # Отправляем сообщение
                s.sendall(message.encode())
                #(f"Сообщение '{message}' отправлено успешно на {host}:{port}")

                response = s.recv(1024).decode()
                print(f"Получен ответ от сервера: {response}")
                
                return response
            

        def key_gen(parameter):
            if os.path.exists('keys.json'):
                if parameter == 0:
                    with open('keys.json', 'r') as file:
                        (e, n), (d, n) = json.load(file)
                    return (e, n), (d, n)
                elif parameter == 1:
                    print("RSA process!")
                    (e, n), (d, n) = rsa.generate_keypair()
                    print("RSA done!")
                    with open('keys.json', 'w', encoding='utf-8') as file:
                        json.dump(((e, n), (d, n)), file, ensure_ascii=False, indent=4)
                    return (e, n), (d, n)
            else:
                print("RSA process!")
                (e, n), (d, n) = rsa.generate_keypair()
                print("RSA done!")
                with open('keys.json', 'w', encoding='utf-8') as file:
                    json.dump(((e, n), (d, n)), file, ensure_ascii=False, indent=4)
                return (e, n), (d, n)


        def ToplevelWindow():
            new_window = CTk.CTkToplevel(self)
            new_window.geometry("400x300")
            new_window.title("Login")

            my_image = CTk.CTkImage(light_image=Image.open("7516814.png"),
                                    dark_image=Image.open("7516814.png"),
                                    size=(100, 100))
            new_window.label = CTk.CTkLabel(new_window, image=my_image, text="", )
            new_window.label.pack(padx=20, pady=20)


            def login():
                global login_check
                global realtime_user
                global logn
                global password
                global lets_ping
                logn = new_window.user.get()
                logn = logn.lower()
                password = new_window.password.get()
                password = password.lower()
                password = sha256(password)

                (e, n), (d, n) = key_gen(0)
                openkey = str(e) + ":" + str(n)
                
                print("key`s generated!")

                resp = send_tcp_message(logn + "~" + password + "~" + openkey)

                if resp == "User created successfully" or resp == "Login successful":
                    new_window.destroy()
                    lets_ping = "1"
                    load_data(logn)
                    return
                elif resp == "Bad password":
                    new_window.destroy()
                    ToplevelWindow()

            new_window.user = CTk.CTkEntry(master=new_window, width=200, height=30)
            new_window.user.place(x=100, y=150)

            new_window.password = CTk.CTkEntry(master=new_window, width=200, height=30)
            new_window.password.place(x=100, y=200)
            
            new_window.login = CTk.CTkButton(master=new_window, width=50, height=30, fg_color="#5e00ff", text_color="white", text="register/login", command=login)
            new_window.login.place(x=150, y=250)


        def send_To_Server(message):
            global userto
            global logn
            openkey = send_tcp_message(logn + '`' + ' ')
            keys = openkey.split(':')
            message = rsa.decryption((int(keys[0]), int(keys[1])), message)
            mes = ""
            for i in message:
                mes += str(i) + ','
            ifls = send_tcp_message(userto + '+' + logn + '+' + mes)
            if ifls:
                pass


        def sendtext():
            global userto
            global name_text_dict
            global password 
            message = self.textbox.get()
            current_time = datetime.datetime.now()
            message_text = f"{current_time} - {message}\n"

            send_To_Server(message_text)

            text_label = CTk.CTkLabel(master=self.chat_frame, text=message_text, justify=CTk.LEFT)
            text_label.pack(anchor=CTk.W)
            message = self.textbox.delete(first_index=0, last_index=10000)

            if userto.lower() in name_text_dict.keys():
                st = name_text_dict.get(userto)
                st += message_text
                name_text_dict[userto.lower()] = st
            else:
                name_text_dict[userto.lower()] = message_text

            save_data()

        def text_add(message):
            text_label = CTk.CTkLabel(master=self.chat_frame, text=message, justify=CTk.LEFT)
            text_label.pack(anchor=CTk.W)
            message = self.textbox.delete(first_index=0, last_index=10000)


        def new_user_add():
            global name_text_dict
            global realtime_user
            new_usr_window = CTk.CTkInputDialog(text="Type a usename", title="Test")
            username = new_usr_window.get_input()
            if username not in name_text_dict.keys():
                ifls = send_tcp_message(username.lower() + "`" + " ")
                if ifls != "bad_user":
                    name_text_dict[username] = ""
                    button = CTk.CTkButton(master=self.chater_frame, width=190, height=30, text=username.lower(), fg_color="#5e00ff", text_color="white", command=lambda: switch_dialog(username))
                    button.pack()
                    switch_dialog(username)
                else:
                    new_usr_window.destroy()
                    return


        def old_user_add(username):
            global name_text_dict
            global realtime_user
            name_text_dict[username] = ""
            button = CTk.CTkButton(master=self.chater_frame, width=190, height=30, text=username, fg_color="#5e00ff", text_color="white", command=lambda: switch_dialog(username))
            button.pack()
            switch_dialog(username)


        def switch_dialog(username):
            global name_text_dict
            global realtime_user
            global userto
            userto = username
            self.chat_frame.place_forget()

            print(f"{username} in {name_text_dict.keys()} == {username in name_text_dict.keys()}")
            if username in name_text_dict.keys() and name_text_dict.get(username) != "":
                print("Trying to replace")
                self.chat_frame.place_forget()

                new_dialog_frame = CTk.CTkScrollableFrame(master=self, width=630, height=490, fg_color="white")
                new_dialog_frame.place(x=350, y=10)

                self.chat_frame = new_dialog_frame
                self.chat_frame.tkraise()
                self.chat_frame.place()
                st = name_text_dict.get(username)
                st_arr = st.split("\n")
                for message in st_arr:
                    text_label = CTk.CTkLabel(master=self.chat_frame, text=message, justify=CTk.LEFT)
                    text_label.pack(anchor=CTk.W)
                    message = self.textbox.delete(first_index=0, last_index=10000)
                print("DONE :)")
            else:
                new_dialog_frame = CTk.CTkScrollableFrame(master=self, width=630, height=490, fg_color="white")
                new_dialog_frame.place(x=350, y=10)
                #debug_output()
                self.chat_frame = new_dialog_frame
                self.chat_frame.tkraise()
                self.chat_frame.place()

            realtime_user = username

            print(f"user switched to: {username}")
            

        def save_data():
            global logn
            global name_text_dict
            global password
            for_save_dict = {}
            for i in name_text_dict.keys():
                x = name_text_dict.get(i)
                x = x.split('\n')
                st = ""
                for j in x:
                    if j != '':
                        a = j.split('-')
                        a_enc = viginere.vig_encrypt(a[3], password)
                        st += a[0] + '-' + a[1] + '-' + a[2] + '-' + a_enc + "\n"
                for_save_dict[i] = st

            with open(str(logn)+'.json', 'w') as file:
                json.dump(for_save_dict, file, ensure_ascii=False, indent=4)


        def load_data(usr):
            global password
            global name_text_dict
            with open(str(usr)+'.json', 'r') as file:
                loaded_dict = json.load(file)
            for i in loaded_dict.keys():
                old_user_add(i)
                st = loaded_dict.get(i)
                st_arr = st.split("\n")
                for j in st_arr:
                    a = j.split('-')
                    if len(a) >= 2:
                        a_dec = viginere.vig_decrypt(a[3], password)
                        mes = a[0] + '-' + a[1] + '-' + a[2] + '-' + a_dec
                        name_text_dict[i] = mes
                        text_add(mes)


        self.geometry("1000x600")
        self.title("messenger")
        self.resizable(False, False)

        self.chat_frame = CTk.CTkScrollableFrame(master=self, width=630, height=490, fg_color="white")
        self.chat_frame.place(x=350, y=10)

        self.textbox = CTk.CTkEntry(master=self, width=590, height=30)
        self.textbox.place(x=350, y=520)
        
        self.sendbutton = CTk.CTkButton(master=self, width=30, height=30, fg_color="#5e00ff", text_color="white", text="send", command=sendtext)
        self.sendbutton.place(x=950, y=520)

        self.setbutton = CTk.CTkButton(master=self, width=40, height=30, fg_color="#5e00ff", text_color="white", text="settings")
        self.setbutton.place(x=10, y=10)

        self.newchat = CTk.CTkButton(master=self, width=30, height=30, fg_color="#5e00ff", text_color="white", text="+", command=new_user_add)
        self.newchat.place(x=80, y=10)

        self.chater_frame = CTk.CTkScrollableFrame(master=self, width=200, height=490, fg_color="white")
        self.chater_frame.place(x=10, y=50)

        ToplevelWindow()



if __name__ == "__main__":
    app = App()
    app.mainloop()
