import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
import openai
import logging
import os
import sys
import requests
import urllib.request
from PIL import Image
from io import BytesIO
from api_key import key

models = ["text-davinci-003", "text-davinci-002",
          "text-curie-001", "text-babbage-001", "text-ada-001"]
max_tokens_list = [256, 2000, 8000]
picture_size = ["256x256", "512x512", "1024x1024"]
mode = ["Light", "Dark", "System"]
scaling = ["80%", "90%", "100%", "110%", "120%"]


class OpenAIGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.title('OpenAI GUI')
        self.geometry("1100x580")
        self.resizable(True, True)

        self._create_widgets()
        self._configure_layout()
        self._create_logger()

    def _create_widgets(self):
        self.prompt_entry = ctk.CTkEntry(
            self, width=250, height=100, placeholder_text="Enter your statement or question:")

        self.text_in = tk.StringVar()
        self.textbox = ctk.CTkEntry(
            self, width=250, height=400, textvariable=self.text_in, state='normal', justify='left', exportselection=True)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)

        # GUI LABEL
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="OpenAI GUI", font=ctk.CTkFont(size=20, weight="bold"))

        self.modellabel = ctk.CTkLabel(
            self.sidebar_frame, text="Models:", font=("Arial", 13, 'bold'))

        self.dalle_prompt = tk.StringVar()
        self.model_var = tk.StringVar()
        self.model_var.set("text-davinci-003")
        self.model_selector = tk.OptionMenu(
            self.sidebar_frame, self.model_var, *models)
        self.model_selector.config(
            font=("Arial", 12), fg="White", bg="#004C99", highlightbackground="#404040", highlightcolor="#404040", activebackground="#004C99", disabledforeground="#404040", anchor="w")

        self.tokenlabel = ctk.CTkLabel(
            self.sidebar_frame, text="Max tokens:", font=("Arial", 13, 'bold'))

        self.max_tokens_var = tk.StringVar()
        self.max_tokens_var.set("256")
        self.max_tokens_selector = tk.OptionMenu(
            self.sidebar_frame, self.max_tokens_var, *max_tokens_list)
        self.max_tokens_selector.config(
            font=("Arial", 12), fg="White", bg="#004C99", highlightbackground="#404040", highlightcolor="#404040", activebackground="#004C99", disabledforeground="#404040", anchor="w")

        self.dalle_label = ctk.CTkLabel(
            self.sidebar_frame, text="Dall-E", font=("Arial", 17, 'bold'))
        self.sizelabel = ctk.CTkLabel(
            self.sidebar_frame, text="Picture size:", font=("Arial", 13, 'bold'))

        self.set_picture_size_var = tk.StringVar()
        self.set_picture_size_var.set("256x256")
        self.set_picture_selector = tk.OptionMenu(
            self.sidebar_frame, self.set_picture_size_var, *picture_size)
        self.set_picture_selector.config(
            font=("Arial", 12), fg="White", bg="#004C99", highlightbackground="#404040", highlightcolor="#404040", activebackground="#004C99", disabledforeground="#404040", anchor="w")

        self.set_picture_selector.config(font=("Arial", 12), fg="White", bg="#004C99", highlightbackground="#404040",
                                         highlightcolor="#404040", activebackground="#004C99", disabledforeground="#404040")

        self.generate_button = ctk.CTkButton(
            self, text="Generate answer", fg_color="#004C99", bg_color="#004C99", command=self.generate_response, font=("Arial", 13))
        self.clear_button = ctk.CTkButton(
            self, text="Clear prompt", fg_color="#004C99", bg_color="#004C99", command=self.clear_prompt, font=("Arial", 13))
        self.quit_button = ctk.CTkButton(
            self, text="Quit app", fg_color="#004C99", bg_color="#004C99", command=self.quit_app, font=("Arial", 12))

        # Window customization
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=mode, command=self.change_appearance_mode_event)

        self.scaling_label = ctk.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=scaling, command=self.change_scaling_event)
        # create tabview
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(
            20, 0), pady=(20, 0), sticky="n")
        # ADD TAB FOCUS
        self.tabview.add("Text models")
        self.tabview.add("Dall-E")
        self.tabview.tab("Text models").grid_columnconfigure(
            0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Dall-E").grid_columnconfigure(0, weight=1)

        self.generate_button.bind("<Return>", self.generate_response)
        self.clear_button.bind("<Delete>", self.clear_prompt)
        self.quit_button.bind("<Escape>", self.quit_app)

    def _configure_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Sidebar
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.modellabel.grid(row=1, column=0, sticky="n")
        self.model_selector.grid(row=2, column=0, sticky="n")
        self.tokenlabel.grid(row=3, column=0, sticky="n")
        self.max_tokens_selector.grid(
            row=4, column=0, sticky="n")
        self.dalle_label.grid(row=5, column=0, sticky="n")
        self.sizelabel.grid(row=6, column=0, sticky="n")
        self.set_picture_selector.grid(row=7, column=0, sticky="n")
        self.scaling_optionemenu.grid(row=12, column=0, sticky="n")
        self.appearance_mode_optionemenu.grid(
            row=10, column=0, sticky="n")
        # Main bar
        self.prompt_entry.grid(row=0, column=1, padx=(
            20, 5), pady=(25, 10),  sticky="new")
        self.textbox.grid(row=1, column=1, padx=(
            20, 5), pady=(25, 10), sticky="nsew")
        self.generate_button.grid(row=6, column=1, padx=(
            20, 5), pady=(20, 10), sticky="nsew")
        self.clear_button.grid(row=6, column=0, padx=(
            20, 5), pady=(20, 10), sticky="nsew")
        self.quit_button.grid(row=6, column=2, padx=(
            20, 5), pady=(20, 10), sticky="nsew")

    def _create_logger(self):
        self.logger = logging.getLogger()
        logging.basicConfig(filename='answers.txt', level=logging.INFO)

    def generate_response(self):
        command = self.prompt_entry.get()
        completion = openai.Completion.create(engine=self.model_var.get(), prompt=command,
                                              temperature=0,
                                              max_tokens=int(
            self.max_tokens_var.get())
        )
        result = completion.choices[0].text
        self.logger.info(result)
        self.text_in.set(result)
        # tk.messagebox.showinfo("Answer", result)

    # ADD DALLE VARIATION AND IMAGE CREATION
    def generate_image(self, set_picture_size_var):
        tk.messagebox.showinfo('Creating and saving image...')
        prompt_ins = self.dalle_prompt.get()
        response = openai.Image.create(
            prompt=prompt_ins,
            n=1,
            size=set_picture_size_var.get()
        )
        image_url = response['data'][0]['url']
        webUrl = urllib.request.urlopen(image_url)
        img = Image.open(webUrl)
        file_name = os.path.basename(prompt_ins)[:255] + '.png'
        img.show()
        img.save(file_name)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def clear_prompt(self):
        self.prompt_entry.delete(0, tk.END)
        self.textbox.delete(0, tk.END)

    def quit_app(self):
        self.destroy()


if __name__ == '__main__':
    app = OpenAIGUI()
    app.mainloop()
