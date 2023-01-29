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
max_tokens_list = ["256", "2000", "8000"]
picture_size = ["256x256", "512x512", "1024x1024"]
mode = ["Light", "Dark", "System"]
scaling = ["80%", "90%", "100%", "110%", "120%"]


class OpenAIGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.title('OpenAI GUI')
        self.geometry("1100x700")
        self.resizable(True, True)

        self._create_widgets()
        self._configure_layout()
        self._create_logger()

    def _create_widgets(self):
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)

        # create tabview
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.add("Text models")
        self.tabview.add("Dall-E")

        self.prompt_entry = ctk.CTkEntry(
            self.tabview.tab('Text models'), width=250, height=100, placeholder_text="Enter your statement or question:")

        self.dalle_prompt = ctk.StringVar()
        self.dalle_impression = ctk.CTkEntry(self.tabview.tab(
            'Dall-E'), width=500, height=100, placeholder_text="Enter image suggestion:", textvariable=self.dalle_prompt)
        self.text_in = ctk.StringVar()
        self.textbox = ctk.CTkEntry(
            self.tabview.tab('Text models'), width=500, height=300, textvariable=self.text_in, justify='left', state="disabled")
        # GUI LABEL
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="OpenAI GUI", font=ctk.CTkFont(size=20, weight="bold"))

        self.modellabel = ctk.CTkLabel(
            self.sidebar_frame, text="Models:", font=("Arial", 13, 'bold'))

        self.model_var = ctk.StringVar(value="text-davinci-003")
        self.model_selector = ctk.CTkComboBox(
            self.sidebar_frame, variable=self.model_var, values=models)

        self.tokenlabel = ctk.CTkLabel(
            self.sidebar_frame, text="Max tokens:", font=("Arial", 13, 'bold'))

        self.max_tokens_var = ctk.StringVar(value="256")
        self.max_tokens_selector = ctk.CTkComboBox(
            self.sidebar_frame, variable=self.max_tokens_var, values=max_tokens_list)

        self.dalle_label = ctk.CTkLabel(
            self.sidebar_frame, text="Dall-E", font=("Arial", 17, 'bold'))
        self.sizelabel = ctk.CTkLabel(
            self.sidebar_frame, text="Picture size:", font=("Arial", 13, 'bold'))

        self.set_picture_size_var = ctk.StringVar(value="256x256")
        self.set_picture_selector = ctk.CTkComboBox(
            self.sidebar_frame, variable=self.set_picture_size_var, values=picture_size)

        self.generate_button = ctk.CTkButton(
            self.tabview.tab('Text models'), text="Generate answer", command=self.generate_response)
        self.create_image = ctk.CTkButton(self.tabview.tab(
            'Dall-E'), text="Create image", command=self.generate_image)
        self.open_log = ctk.CTkButton(
            self.tabview.tab('Text models'), text="Open file", command=self.open_file)
        self.clear_button = ctk.CTkButton(
            self.sidebar_frame, text="Clear prompt", command=self.clear_prompt)
        self.quit_button = ctk.CTkButton(
            self.sidebar_frame, text="Quit app", command=self.quit_app, fg_color='Red')

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

        self.generate_button.bind("<Return>", self.generate_response)
        self.clear_button.bind("<Delete>", self.clear_prompt)
        self.quit_button.bind("<Escape>", self.quit_app)

    def _configure_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.logo_label.grid(row=0, column=0, padx=20, pady=20, sticky='n')
        # Tab view
        self.tabview.tab("Text models").grid_columnconfigure(
            1, weight=5)  # configure grid of individual tabs
        self.tabview.tab("Dall-E").grid_columnconfigure(1, weight=5)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="n")
        # Sidebar
        self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        self.modellabel.grid(row=1, column=0)
        self.model_selector.grid(row=2, column=0)
        self.tokenlabel.grid(row=3, column=0)
        self.max_tokens_selector.grid(
            row=4, column=0)
        self.dalle_label.grid(row=5, column=0)
        self.sizelabel.grid(row=6, column=0)
        self.set_picture_selector.grid(row=7, column=0, sticky="n")
        self.scaling_optionemenu.grid(row=12, column=0, sticky="n")
        self.appearance_mode_optionemenu.grid(
            row=10, column=0)
        # Main bar
        self.prompt_entry.grid(row=0, column=2, padx=(
            20, 5), pady=(25, 10),  sticky="new")
        self.textbox.grid(row=1, column=2, padx=(
            20, 5), pady=(25, 10), sticky="nsew")
        self.generate_button.grid(row=5, column=2, padx=20, pady=10)
        self.dalle_impression.grid(row=0, column=2, padx=20, pady=10)
        self.create_image.grid(row=5, column=2, padx=20, pady=10)
        self.open_log.grid(row=6, column=2, padx=20, pady=10)
        self.clear_button.grid(row=13, column=0, padx=20, pady=10)
        self.quit_button.grid(row=14, column=0, padx=20, pady=10)

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
    def generate_image(self):
        tk.messagebox.showinfo('Creating and saving image...')
        prompt_ins = self.dalle_prompt.get()
        response = openai.Image.create(
            prompt=prompt_ins,
            n=1,
            size=self.set_picture_size_var.get()
        )
        image_url = response['data'][0]['url']
        webUrl = urllib.request.urlopen(image_url)
        img = Image.open(webUrl)
        file_name = os.path.basename('DallE')[:255] + '.png'
        img.show()
        img.save(file_name)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def open_file(self):
        os.startfile('answers.txt', 'open')

    def clear_prompt(self):
        self.prompt_entry.delete(0, tk.END)
        self.textbox.delete(0, tk.END)
        self.dalle_prompt.delete(0, tk.END)

    def quit_app(self):
        self.destroy()


if __name__ == '__main__':
    app = OpenAIGUI()
    app.mainloop()
