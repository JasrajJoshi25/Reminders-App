import customtkinter as ctk
from tkinter import filedialog
import os
import webbrowser
import urllib.parse

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

PROGRESS_FILE = "assignment_progress.txt"

class AssignmentTracker(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Assignment Reminder System")
        self.geometry("600x700")
        self.resizable(False, False)

        self.students = {}
        self.checkboxes = {}

        self.title_label = ctk.CTkLabel(
            self,
            text="Assignment Submission Tracker",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(pady=15)

        self.upload_button = ctk.CTkButton(
            self,
            text="Upload Student File",
            command=self.upload_file,
            height=40
        )
        self.upload_button.pack(pady=10)

        # STUDENT LIST
        self.student_frame = ctk.CTkScrollableFrame(self, width=520, height=350)
        self.student_frame.pack(pady=10)

        # BUTTON FRAME
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="Save Progress",
            command=self.save_progress,
            width=130,
            hover_color="#29b229bd"
        )
        self.save_button.grid(row=0, column=0, padx=8)

        self.generate_button = ctk.CTkButton(
            self.button_frame,
            text="Generate Reminder",
            command=self.generate_reminder,
            width=150,
            hover_color="#29b229bd"
        )
        self.generate_button.grid(row=0, column=1, padx=8)

        # NEW RESET BUTTON
        self.reset_button = ctk.CTkButton(
            self.button_frame,
            text="Reset",
            command=self.reset_checkboxes,
            width=100,
            fg_color="#8B0000"
        )
        self.reset_button.grid(row=0, column=2, padx=8)

        # NEW SEND MESSAGE BUTTON
        self.send_button = ctk.CTkButton(
            self.button_frame,
            text="Send MSG",
            command=self.send_message,
            width=120,
            fg_color="#006400"
        )
        self.send_button.grid(row=0, column=3, padx=8)

        self.message_box = ctk.CTkTextbox(self, width=520, height=150)
        self.message_box.pack(pady=10)

        self.load_progress_if_exists()

    def load_progress_if_exists(self):

        if os.path.exists(PROGRESS_FILE):

            with open(PROGRESS_FILE, "r") as file:
                lines = file.readlines()

            for widget in self.student_frame.winfo_children():
                widget.destroy()

            for line in lines:

                name, status = line.strip().split(",")

                var = ctk.BooleanVar(value=bool(int(status)))

                checkbox = ctk.CTkCheckBox(
                    self.student_frame,
                    text=name,
                    variable=var
                )

                checkbox.pack(anchor="w", pady=5, padx=10)

                self.checkboxes[name] = var

    def upload_file(self):

        file_path = filedialog.askopenfilename(
            title="Select Student List",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            return

        with open(file_path, "r") as file:
            students = [line.strip() for line in file.readlines()]

        for widget in self.student_frame.winfo_children():
            widget.destroy()

        self.checkboxes.clear()

        for student in students:

            var = ctk.BooleanVar()

            checkbox = ctk.CTkCheckBox(
                self.student_frame,
                text=student,
                variable=var
            )

            checkbox.pack(anchor="w", pady=5, padx=10)

            self.checkboxes[student] = var

    def save_progress(self):

        with open(PROGRESS_FILE, "w") as file:

            for name, var in self.checkboxes.items():

                status = 1 if var.get() else 0

                file.write(f"{name},{status}\n")

        self.message_box.delete("0.0", "end")
        self.message_box.insert("0.0", "Progress saved successfully.")

    def generate_reminder(self):

        pending_students = []

        for name, var in self.checkboxes.items():

            if not var.get():
                pending_students.append(name)

        if not pending_students:

            message = "All students have submitted the assignment."

        else:

            message = "Reminder:\n\nThe following students have not submitted the Python assignment:\n\n"

            for student in pending_students:
                message += f"- {student}\n"

        self.message_box.delete("0.0", "end")
        self.message_box.insert("0.0", message)

    # RESET FUNCTION
    def reset_checkboxes(self):

        for var in self.checkboxes.values():
            var.set(False)

        self.message_box.delete("0.0", "end")
        self.message_box.insert("0.0", "All checkboxes have been reset.")

    # SEND MESSAGE FUNCTION
    def send_message(self):

        message = self.message_box.get("0.0", "end").strip()

        if not message:
            return

        encoded_message = urllib.parse.quote(message)

        whatsapp_url = f"https://web.whatsapp.com/send?text={encoded_message}"

        webbrowser.open(whatsapp_url)


app = AssignmentTracker()
app.mainloop()