import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
import logging
import openai
from api_key import key

models = ["text-davinci-003", "text-davinci-002",
          "text-curie-001", "text-babbage-001", "text-ada-001"]
max_tokens_list = [256, 2000, 8000]
mode = ["Light", "Dark", "System"]
scaling = ["80%", "90%", "100%", "110%", "120%"]


class OpenAIGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.title('OpenAI GUI')
        self.geometry("1100x580")
        self.resizable(False, False)

        self._create_widgets()
        self._configure_layout()
        self._create_logger()

    def _create_widgets(self):
        self.prompt_entry = tk.Entry(self, name="enter statement or question")

        self.textbox = ctk.CTkTextbox(self, width=250)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)

        # GUI LABEL
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="OpenAI GUI", font=ctk.CTkFont(size=20, weight="bold"))

        self.modellabel = ctk.CTkLabel(self.sidebar_frame, text="Models:", font=("Arial", 13, 'bold'))

        self.model_var = tk.StringVar()
        self.model_var.set("text-davinci-003")
        self.model_selector = tk.OptionMenu(self.sidebar_frame, self.model_var, *models)

        self.tokenlabel = ctk.CTkLabel(self.sidebar_frame, text="Max tokens:", font=("Arial", 13, 'bold'))

        self.max_tokens_var = tk.StringVar()
        self.max_tokens_var.set("256")
        self.max_tokens_selector = tk.OptionMenu(self.sidebar_frame, self.max_tokens_var, *max_tokens_list)

        self.generate_button = tk.Button(self, text="Generate", command=self.generate_response)
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_prompt)
        self.quit_button = tk.Button(self, text="Quit", command=self.quit_app)

        # Window customization
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=mode, command=self.change_appearance_mode_event)

        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=scaling, command=self.change_scaling_event)

    def _configure_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
				self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Sidebar
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.modellabel.grid(row=1, column=0, sticky="N")
        self.model_selector.grid(row=2, column=0, padx=20,pady=(10, 10))
        self.tokenlabel.grid(row=3, column=0, sticky="N")
        self.max_tokens_selector.grid(row=4, column=0, padx=20,pady=(10, 10), sticky="N")
        self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 10))
        # Main bar
        self.prompt_entry.grid(row=0, column=1,padx=(20, 5), pady=(20, 10), sticky="nsew")
				self.textbox.grid(row=2, column=1, padx=(20, 5), pady=(20, 10), sticky="nsew")
				self.generate_button.grid(row=6, column=1, padx=(20, 5),pady=(20, 10), sticky="NSWE")
        self.clear_button.grid()
        self.quit_button.grid(row=6, column=2, padx=(20, 5),pady=(20, 10), sticky="NSWE")

    def _create_logger(self):
        self.logger = logging.getLogger()
        logging.basicConfig(filename='answers.txt', level=logging.INFO)

    def generate_response(self):
        command = self.prompt_entry.get()
        completion = openai.Completion.create(engine=self.model_var.get(), prompt=command,
                                              temperature=0,
                                              max_tokens=int(self.max_tokens_var.get())
        )
        result = completion.choices[0].text
        self.logger.info(result)
        tk.messagebox.showinfo("Answer", result)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def clear_prompt(self):
        self.prompt_entry.delete(0, tk.END)

    def quit_app(self):
        self.destroy()

if __name__ == '__main__':
    app = OpenAIGUI()
    app.mainloop()