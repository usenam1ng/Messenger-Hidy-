import rsa
import datetime
import customtkinter as CTk
from PIL import Image
import pickle


class ToplevelWindow(CTk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Login")

        my_image = CTk.CTkImage(light_image=Image.open("/Users/vladislavkonukov/Desktop/RGZ/client/7516814.png"),
                                  dark_image=Image.open("/Users/vladislavkonukov/Desktop/RGZ/client/7516814.png"),
                                  size=(100, 100))
        self.label = CTk.CTkLabel(self, image=my_image, text="", )
        self.label.pack(padx=20, pady=20)

        def login():
            login = self.user.get()
            password = self.password.get()

            query = login + "+" + password

            print(query)

            self.destroy()



        self.user = CTk.CTkEntry(master=self, width=200, height=30)
        self.user.place(x=100, y=150)

        self.password = CTk.CTkEntry(master=self, width=200, height=30)
        self.password.place(x=100, y=200)
        
        self.login = CTk.CTkButton(master=self, width=50, height=30, fg_color="#5e00ff", text_color="white", text="register/login", command=login)
        self.login.place(x=150, y=250)



class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        global realtime_user
        realtime_user = ""

        global name_text_dict
        name_text_dict = {}

        ToplevelWindow()


        def sendSendToServer():
            pass

        def sendtext():
            global name_text_dict
            message = self.textbox.get()
            current_time = datetime.datetime.now()
            message_text = f"{current_time} - {message}\n"

            sendSendToServer()

            text_label = CTk.CTkLabel(master=self.chat_frame, text=message_text, justify=CTk.LEFT)
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
        

        # def debug_output():
        #     global name_text_dict
        #     print("_____________________")
        #     print(f"realtime user: {realtime_user}")
        #     print(f"whole dictionary: {name_text_dict}")
        #     for i in name_text_dict.keys():
        #         print(f"<{i}>: {name_text_dict[i]}")
        #         for child in name_text_dict[i].winfo_children():
        #             print(f"child ~< {child} >~")
        #             print(f"child ~~~< {child.cget("text")} >~~~")
                
        #     print("---------------------")
            
        def seralize():
            global name_text_dict
            


        self.geometry("1000x600")
        self.title("messenger")
        self.resizable(False, False)

        self.chat_frame = CTk.CTkScrollableFrame(master=self, width=630, height=490, fg_color="white")
        self.chat_frame.place(x=350, y=10)

        self.textbox = CTk.CTkEntry(master=self, width=590, height=30)
        self.textbox.place(x=350, y=520)
        
        self.sendbutton = CTk.CTkButton(master=self, width=30, height=30, fg_color="#5e00ff", text_color="white", text="send", command=sendtext)
        self.sendbutton.place(x=950, y=520)

        self.setbutton = CTk.CTkButton(master=self, width=40, height=30, fg_color="#5e00ff", text_color="white", text="settings", command=seralize)
        self.setbutton.place(x=10, y=10)

        self.newchat = CTk.CTkButton(master=self, width=30, height=30, fg_color="#5e00ff", text_color="white", text="+", command=new_user_add)
        self.newchat.place(x=80, y=10)

        self.chater_frame = CTk.CTkScrollableFrame(master=self, width=200, height=490, fg_color="white")
        self.chater_frame.place(x=10, y=50)




if __name__ == "__main__":
    

    app = App()
    app.mainloop()
