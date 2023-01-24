import tkinter
import tkinter.messagebox
import customtkinter as ctk
import logging
import openai
from tkinter import StringVar
from PIL import Image
from api_key import key
from imgnsound import noacc, engine, voices

# Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("dark-blue")


class OpenAIGUI(ctk.CTk):
    def openAi(self):
        command = self.prompt_in.get()
        self.prompt_in.set(command)
        completion = openai.Completion.create(engine="text-davinci-003", prompt=command,
                                              temperature=0,
                                              max_tokens=4000,
                                              top_p=1.0,
                                              frequency_penalty=0.0,
                                              presence_penalty=0.0
                                              )
        result = completion.choices[0].text
        length = ((result).join(result)).count(result) + 1
        # Creating an object
        logger = logging.getLogger()
        logging.basicConfig(filename='answers.txt', level=logging.INFO)
        if length < 150:
            logger.info(result)
            ctk.CTkTextbox.showinfo("Answer", result)
        else:
            logger.info(result)
            ctk.CTkTextbox.showinfo("Answer", result)

    def clr(self):
        self.prompt_in.set('')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def __init__(self):
        super().__init__()
        self.title('OpenAI GUI')
        self.geometry("1100x580")
        self.resizable(False, False)

        # GUI FRAME
        entryframe = ctk.CTkFrame(self, width=140, corner_radius=0)
        entryframe.grid(sticky="NSEW")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # GUI LABEL
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="OpenAI GUI", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.prompt_in = StringVar()
        self.delabel = ctk.CTkLabel(self.sidebar_frame, text="Enter to Speak; Esc to Quit; Delete to Delete text", font=("Arial", 9, 'bold'))
        self.delabel.grid(row=3, column=0, sticky="NSEW")

        # create textbox
        self.txt_input = ctk.CTkEntry(self, placeholder_text="Enter your question or statement:", validatecommand=self.prompt_in)
        self.txt_input.grid(row=0, column=1,padx=(20, 5), pady=(20, 10), sticky="nsew")

        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=2, column=1, padx=(20, 5), pady=(20, 10), sticky="nsew")

        # Appearance
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Scaling
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # GUI FUNCTIONALITY
        self.but_choice = ctk.CTkButton(self, text="Speak", command=self.openAi, font=("Arial", 15, 'bold'))
        self.but_clear = ctk.CTkButton(self, text='Clear', command=self.clr, font=("Arial", 15, 'bold'))

        # GUI DESIGN
        self.but_choice.grid(row=6, column=1, padx=(20, 5),pady=(20, 10), sticky="NSWE")
        self.but_clear.grid(row=6, column=2, padx=(20, 5),pady=(20, 10), sticky="NSWE")

        # CLOSE WINDOW
        """self.ctk.bind("<Return>", self.entertorun)
        self.ctk.bind("<Delete>", self.deletetoquit)
        self.ctk.bind('<Escape>', lambda e: close_me(e))"""

        def close_me(e):
            ctk.destroy()


if __name__ == '__main__':
    # DEFINE WINDOW
    app = OpenAIGUI()
    # INITIATE WINDOW
    app.mainloop()
else:
    print('Client exit!')
