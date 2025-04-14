import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import simpledialog

# Global constants
HOST = '127.0.0.1'
PORT = 5001

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tkinter GUI class
class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        # Asking users about their usernames
        self.username = simpledialog.askstring("Username", "Enter your username:", parent=master)
        if not self.username:
            messagebox.showerror("Username Error", "Username cannot be empty.")
            master.destroy()
            return

        # Text area for displaying messages
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input field for typing messages
        self.input_field = tk.Entry(master)
        self.input_field.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.input_field.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=(0, 10))

        # Connect to server
        try:
            client_socket.connect((HOST, PORT))
            client_socket.send(self.username.encode())
        except socket.error as err:
            messagebox.showerror("Connection Error", str(err))
            master.destroy()
            return

        # Start a background thread to listen for messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = client_socket.recv(2048).decode()
                self.show_message(message)
            except socket.error:
                break

    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if message:
            try:
                client_socket.send(f'{self.username}: {message}'.encode())
                self.show_message(f"You: {message}")
                self.input_field.delete(0, tk.END)
            except socket.error as err:
                self.show_message(f"[ERROR] {str(err)}")

    def show_message(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

# Launch the GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatClientGUI(root)
    root.mainloop()
