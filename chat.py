from customtkinter import *
from socket import *
import threading

HOST = '192.168.0.111'
PORT = 8080

class MainWindow(CTk):

    def __init__(self):
        super().__init__()

        self.geometry("900x600")
        self.title("Chat")
        self.minsize(700, 500)

        set_appearance_mode("dark")
        set_default_color_theme("blue")

        self.frame = CTkFrame(
            self,
            corner_radius=0,
            fg_color="#111827"
        )

        self.frame.pack_propagate(False)

        self.frame.configure(width=0)
        self.frame.place(x=0, y=0)

        self.is_show_menu = False
        self.frame_width = 0
        self.menu_show_speed = 20

        self.label = CTkLabel(
            self.frame,
            text='PROFILE',
            font=("Arial", 22, "bold")
        )

        self.label.pack(pady=(40, 20))

        self.entry = CTkEntry(
            self.frame,
            height=40,
            corner_radius=10,
            placeholder_text="Enter your name"
        )

        self.entry.pack(
            padx=15,
            fill="x"
        )

        self.label_theme = CTkOptionMenu(
            self.frame,
            values=['Light', 'Dark'],
            command=self.change_theme,
            height=35
        )

        self.bg_menu = CTkOptionMenu(
            self.frame,
            values=["Blue", "Green", "Purple", "Black"],
            command=self.change_background,
            height=35
        )

        self.bg_menu.pack(
            side='bottom',
            pady=10,
            padx=15,
            fill="x"
        )

        self.label_theme.pack(
            side='bottom',
            pady=20,
            padx=15,
            fill="x"
        )

        self.theme = None

        self.btn = CTkButton(
            self,
            text='->',
            command=self.toggle_show_menu,
            width=40,
            height=40,
            corner_radius=10,
            fg_color="#2563EB"
        )

        self.btn.place(x=10, y=10)

        self.chat_text = CTkTextbox(
            self,
            state='disabled',
            corner_radius=0,
            font=("Consolas", 15),
            fg_color="#0F172A",
            text_color="white",
            border_width=0
        )

        self.chat_text.place(x=0, y=0)

        self.btn.lift()

        self.message_entry = CTkEntry(
            self,
            placeholder_text="Type your message...",
            height=45,
            corner_radius=12,
            font=("Arial", 14)
        )

        self.message_entry.place(x=0, y=230)

        self.send_btn = CTkButton(
            self,
            text='Send',
            width=80,
            height=45,
            corner_radius=12,
            font=("Arial", 14, "bold"),
            command=self.send_message,
            fg_color="#2563EB"
        )

        self.send_btn.place(
            x=150,
            y=230
        )

        self.username = "Admin"

        try:

            self.sock = socket(AF_INET, SOCK_STREAM)

            self.sock.connect((HOST, PORT))

            hello = f"TEXT@{self.username}@SYSTEM {self.username} joined\n"

            self.sock.send(hello.encode())

            threading.Thread(
                target=self.recv_message,
                daemon=True
            ).start()

        except Exception as e:

            self.add_message(
                f"Couldn't join the server: {e}\n"
            )

        self.change_background("Blue")
        
        self.adaptive_ui()

    def change_theme(self, value):

        if value == 'Dark':
            set_appearance_mode('dark')

        elif value == 'Light':
            set_appearance_mode('light')

    def change_background(self, value):

        if value == "Blue":

            window_color = "#0F172A"
            menu_color = "#111827"
            chat_color = "#0F172A"

            button_color = "#2563EB"

        elif value == "Green":

            window_color = "#052E16"
            menu_color = "#14532D"
            chat_color = "#064E3B"

            button_color = "#22C55E"

        elif value == "Purple":

            window_color = "#2E1065"
            menu_color = "#3B0764"
            chat_color = "#4C1D95"

            button_color = "#8B5CF6"

        elif value == "Black":

            window_color = "#000000"
            menu_color = "#111111"
            chat_color = "#0A0A0A"

            button_color = "#444444"

        self.configure(
            fg_color=window_color
        )

        self.frame.configure(
            fg_color=menu_color
        )

        self.chat_text.configure(
            fg_color=chat_color
        )

        self.message_entry.configure(
            fg_color=menu_color
        )

        self.send_btn.configure(
            fg_color=button_color
        )

        self.btn.configure(
            fg_color=button_color
        )

    def toggle_show_menu(self):

        if self.is_show_menu:

            self.is_show_menu = False
            self.close_menu()

        else:

            self.is_show_menu = True
            self.show_menu()

    def show_menu(self):

        if self.frame_width < 220:

            self.frame_width += self.menu_show_speed

            self.frame.configure(
                width=self.frame_width,
                height=self.winfo_height()
            )

        if self.is_show_menu:

            self.after(
                20,
                self.show_menu
            )

    def close_menu(self):

        if self.frame_width > 0:

            self.frame_width -= self.menu_show_speed

            self.frame.configure(
                width=self.frame_width,
                height=self.winfo_height()
            )

        if not self.is_show_menu:

            self.after(
                20,
                self.close_menu
            )

    def adaptive_ui(self):

        self.chat_text.configure(
            width=self.winfo_width() - self.frame.winfo_width(),
            height=self.winfo_height() - 70
        )

        self.chat_text.place(
            x=self.frame.winfo_width(),
            y=60
        )

        self.btn.lift()

        self.message_entry.configure(
            width=self.winfo_width()
            - self.frame.winfo_width()
            - self.send_btn.winfo_width()
            - 20
        )

        self.message_entry.place(
            x=self.frame.winfo_width() + 10,
            y=self.winfo_height() - 55
        )

        self.send_btn.place(
            x=self.winfo_width()
            - self.send_btn.winfo_width()
            - 10,

            y=self.winfo_height()
            - self.send_btn.winfo_height()
            - 10
        )

        self.after(
            100,
            self.adaptive_ui
        )

    def send_message(self):

        self.username = self.entry.get()

        if self.username == '':
            self.username = "Admin"

        message = self.message_entry.get()

        if message:

            self.add_message(
                f"{self.username}: {message}"
            )

            data = f"TEXT@{self.username}@{message}\n"

            try:
                self.sock.sendall(data.encode())

            except:
                pass

        self.message_entry.delete(0, END)

    def add_message(self, text):

        self.chat_text.configure(state='normal')

        self.chat_text.insert(
            END,
            text + "\n"
        )

        self.chat_text.see(END)

        self.chat_text.configure(state='disabled')

    def recv_message(self):

        buffer = ''

        while True:

            try:

                chunk = self.sock.recv(4096)

                if not chunk:
                    break

                buffer += chunk.decode()

                while '\n' in buffer:

                    line, buffer = buffer.split('\n', 1)

                    self.handle_line(line.strip())

            except:
                break

        self.sock.close()

    def handle_line(self, line):

        if not line:
            return

        parts = line.split("@", 3)

        message_type = parts[0]

        if message_type == "TEXT":

            if len(parts) == 3:

                author = parts[1]
                message = parts[2]

                self.add_message(
                    f"{author}: {message}"
                )

        elif message_type == "IMAGE":

            if len(parts) == 4:

                author = parts[1]
                file_name = parts[2]

                self.add_message(
                    f"{author}: has send an image: {file_name}"
                )

        else:

            self.add_message(line)

main = MainWindow() 
main.mainloop()