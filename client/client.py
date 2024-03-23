import rsa
import datetime
import customtkinter as CTk

class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        def sendtext():
            message = self.textbox.get()
            current_time = datetime.datetime.now()
            message_text = f"{current_time} - {message}\n"
            text_label = CTk.CTkLabel(master=self.chat_frame, text=message_text, justify=CTk.LEFT)
            text_label.pack(anchor=CTk.W)
            message = self.textbox.delete(first_index=0, last_index=10000)

        def show_popup():
            new_usr_window = CTk.CTkInputDialog(text="Type a usename", title="Test")
            username = new_usr_window.get_input()
            button = CTk.CTkButton(master=self.chater_frame, width=190, height=30, text=username, fg_color="#5e00ff", text_color="white", command=switch_dialog)
            button.pack()

        def save_chat_history_to_file():
            chat_history = ""
            for widget in self.chat_frame.winfo_children():
                chat_history += widget.cget("text") + "\n"
            filename = "bibki1" + ".txt"
            with open(filename, "w") as file:
                file.write(chat_history)

        def switch_dialog():
            save_chat_history_to_file()
            self.chat_frame.grid_forget()
            new_dialog_frame = CTk.CTkScrollableFrame(master=self, width=630, height=490, fg_color="white")
            new_dialog_frame.place(x=350, y=10)
            self.chat_frame = new_dialog_frame    

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

        self.newchat = CTk.CTkButton(master=self, width=30, height=30, fg_color="#5e00ff", text_color="white", text="+", command=show_popup)
        self.newchat.place(x=80, y=10)

        self.chater_frame = CTk.CTkScrollableFrame(master=self, width=200, height=490, fg_color="white")
        self.chater_frame.place(x=10, y=50)




if __name__ == "__main__":
    app = App()
    app.mainloop()
