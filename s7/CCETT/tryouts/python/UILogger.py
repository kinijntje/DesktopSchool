import tkinter as tk
import threading
import keyboard
import speech_recognition as sr

class MyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hacker Voice and Keyboard Logger")
        self.root.configure(bg="#000000")  # Set background color to black

        self.start_button = tk.Button(root, text="Start Logging", command=self.start_logging, bg="#00FF00", fg="#000000", font=("Courier", 14, "bold"), relief=tk.FLAT)
        self.start_button.grid(row=0, column=0, pady=10)

        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_logging, bg="#FF0000", fg="#000000", font=("Courier", 14, "bold"), relief=tk.FLAT)
        self.stop_button.grid(row=0, column=1, pady=10)

        self.keyboard_output_label = tk.Label(root, text="Keyboard Output:", bg="#000000", fg="#00FF00", font=("Courier", 12, "bold"))
        self.keyboard_output_label.grid(row=1, column=0, columnspan=2)

        self.keyboard_output_text = tk.Text(root, height=10, width=50, bg="#000000", fg="#00FF00", font=("Courier", 10))
        self.keyboard_output_text.grid(row=2, column=0, columnspan=2)

        self.voice_output_label = tk.Label(root, text="Voice Output:", bg="#000000", fg="#00FF00", font=("Courier", 12, "bold"))
        self.voice_output_label.grid(row=3, column=0, columnspan=2)

        self.voice_output_text = tk.Text(root, height=10, width=50, bg="#000000", fg="#00FF00", font=("Courier", 10))
        self.voice_output_text.grid(row=4, column=0, columnspan=2)

        self.keyboard_thread = None
        self.voice_thread = None
        self.exit_flag = True

        self.canvas = tk.Canvas(root, width=20, height=20, bg="#000000", highlightthickness=0)
        self.status_circle = self.canvas.create_oval(0, 0, 20, 20, fill="#00FF00")  # Create the circle
        self.canvas.grid(row=0, column=2, sticky=tk.NE, padx=10, pady=10)  # Place the canvas in the top right corner

        self.draw_status_circle()
        

    def start_logging(self):
        self.exit_flag = False
        keyboard_thread = threading.Thread(target=self.start_keyboard_logging)
        keyboard_thread.start()

        self.voice_thread = threading.Thread(target=self.voice_logging)
        self.voice_thread.start()
        
        self.update_status_circle()

    def stop_logging(self):
        self.exit_flag = True
        keyboard.unhook_all()
        
        self.update_status_circle()
        
    def start_keyboard_logging(self):
        keyboard.hook(self.keyboard_logging)

    def keyboard_logging(self, keyboard_event):
        global exit_flag
        if keyboard_event.event_type == keyboard.KEY_DOWN:
            key = keyboard_event.name
            print(f"Key '{key}' pressed")
            self.keyboard_output_text.insert(tk.END, f"Keyboard Input: {key}\n")
            self.keyboard_output_text.see(tk.END)

    def voice_logging(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            while not self.exit_flag:
                try:
                    audio = r.listen(source)
                    text = r.recognize_google(audio)
                    self.voice_output_text.insert(tk.END, f"Voice Input: {text}\n")
                    self.voice_output_text.see(tk.END)  # Scroll to the end of the text
                except sr.UnknownValueError:
                    pass  # Ignore unrecognized audio
                except Exception as e:
                    print("Error:", str(e))
               
    def draw_status_circle(self):
        color = "#00FF00" if not self.exit_flag else "#FF0000"
        self.canvas.itemconfig(self.status_circle, fill=color)

    def update_status_circle(self):
        color = "red" if self.exit_flag else "green"
        self.canvas.itemconfig(self.status_circle, fill=color)

root = tk.Tk()
root.geometry("450x500")  # Set initial window size
root.resizable(True, True)  # Enable window resizing
gui = MyGUI(root)
root.mainloop()
