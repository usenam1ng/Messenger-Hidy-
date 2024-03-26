import rsa
import datetime
import customtkinter as CTk
from PIL import Image
import json
import socket

global login_check
login_check = False


class App(CTk.CTk):
    def __init__(self):
        super().__init__()
        global realtime_user
        realtime_user = ""

        global name_text_dict
        name_text_dict = {}

        def send_tcp_message(message, host="127.0.0.1", port=6575):
            # Создаем сокет
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Устанавливаем соединение с сервером
                s.connect((host, port))
                # Отправляем сообщение
                s.sendall(message.encode())
                print(f"Сообщение '{message}' отправлено успешно на {host}:{port}")

                response = s.recv(1024).decode()
                print(f"Получен ответ от сервера: {response}")
                
                return response

            

        def ToplevelWindow():
            new_window = CTk.CTkToplevel(self)
            new_window.geometry("400x300")
            new_window.title("Login")

            my_image = CTk.CTkImage(light_image=Image.open("/Users/vladislavkonukov/Desktop/RGZ/client/7516814.png"),
                                    dark_image=Image.open("/Users/vladislavkonukov/Desktop/RGZ/client/7516814.png"),
                                    size=(100, 100))
            new_window.label = CTk.CTkLabel(new_window, image=my_image, text="", )
            new_window.label.pack(padx=20, pady=20)

            def login():
                global login_check
                if login_check:
                    load_data()
                logn = new_window.user.get()
                password = new_window.password.get()

                query = logn + "+" + password

                resp = send_tcp_message(logn + "~" + password)

                if resp == "User created successfully" or resp == "Login successful":
                    new_window.destroy()
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

        def send_To_Server():
            pass

        def sendtext():
            global name_text_dict
            message = self.textbox.get()
            current_time = datetime.datetime.now()
            message_text = f"{current_time} - {message}\n"

            send_To_Server()

            text_label = CTk.CTkLabel(master=self.chat_frame, text=message_text, justify=CTk.LEFT)
            text_label.pack(anchor=CTk.W)
            message = self.textbox.delete(first_index=0, last_index=10000)
            save_data()

        def text_add(message):
            global name_text_dict
            text_label = CTk.CTkLabel(master=self.chat_frame, text=message, justify=CTk.LEFT)
            text_label.pack(anchor=CTk.W)
            message = self.textbox.delete(first_index=0, last_index=10000)

        def new_user_add():
            global name_text_dict
            global realtime_user
            new_usr_window = CTk.CTkInputDialog(text="Type a usename", title="Test")
            username = new_usr_window.get_input()
            name_text_dict[username] = None
            button = CTk.CTkButton(master=self.chater_frame, width=190, height=30, text=username, fg_color="#5e00ff", text_color="white", command=lambda: switch_dialog(username))
            button.pack()
            switch_dialog(username)

        def old_user_add(username):
            global name_text_dict
            global realtime_user
            name_text_dict[username] = None
            button = CTk.CTkButton(master=self.chater_frame, width=190, height=30, text=username, fg_color="#5e00ff", text_color="white", command=lambda: switch_dialog(username))
            button.pack()
            switch_dialog(username)
            
        def save_chat_history_to_file():
            global name_text_dict
            chat_history = ""
            for widget in self.chat_frame.winfo_children():
                chat_history += widget.cget("text") + "\n"
            filename = "bibki1" + ".txt"
            with open(filename, "w") as file:
                file.write(chat_history)

        def switch_dialog(username):
            global name_text_dict
            global realtime_user
            print(username, realtime_user)
            name_text_dict[realtime_user] = self.chat_frame
            self.chat_frame.place_forget()

            print(f"{username} in {name_text_dict.keys()} == {username in name_text_dict.keys()}")
            if username in name_text_dict.keys() and name_text_dict.get(username) != None:
                print("Trying to replace")
                self.chat_frame.place_forget()
                new_dialog_frame = name_text_dict.get(username)
                new_dialog_frame.place(x=350, y=10)
                self.chat_frame = new_dialog_frame
                self.chat_frame.tkraise()
                self.chat_frame.place()
                print("DONE :)")
            else:
                new_dialog_frame = CTk.CTkScrollableFrame(master=self, width=630, height=490, fg_color="white")
                new_dialog_frame.place(x=350, y=10)
                #debug_output()
                self.chat_frame = new_dialog_frame
                self.chat_frame.tkraise()
                self.chat_frame.place()
                name_text_dict[username] = new_dialog_frame

            realtime_user = username

            print(f"user switched to: {username}")
            
        def save_data():
            global name_text_dict
            for_save_dict = {}
            for i in name_text_dict.keys():
                 for child in name_text_dict[i].winfo_children():
                    if i in for_save_dict:
                        st = for_save_dict.get(i)
                        if "\n" in child.cget("text"):
                            st += child.cget("text")
                        else:
                            st += child.cget("text") + "\n"
                        print(st)
                        for_save_dict[i] = st
                    else:
                        for_save_dict[i] = child.cget("text")
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(for_save_dict, file, ensure_ascii=False, indent=4)


        def load_data():
            with open('data.json', 'r') as file:
                loaded_dict = json.load(file)
            for i in loaded_dict.keys():
                old_user_add(i)
                st = loaded_dict.get(i)
                st_arr = st.split("\n")
                for j in st_arr:
                    text_add(j)

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
