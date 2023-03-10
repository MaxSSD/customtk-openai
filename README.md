# customtk-openai
*This is a GUI application built using the tkinter library in Python and the customtkinter library, which is a custom tkinter library built by the developers. It uses the OpenAI API to generate responses based on the user input.*

# TBD
* Fix tabs
* Scrollbar in textbox.
* Save chat history.
* Chatbot db.

# Screenshot
![Capture4](https://user-images.githubusercontent.com/86234226/215324460-2f557892-0c45-43d5-a08c-068bb440cbf5.PNG)

![Capture5](https://user-images.githubusercontent.com/86234226/215324315-859a2368-b9ce-4e27-ae92-69b3d5c7ee29.PNG)

# Features
* The application has a sidebar that contains options to select the OpenAI model, maximum tokens, appearance mode, and UI scaling.
* It also contains a prompt entry field where the user can enter the statement or question, and a textbox where the generated response will be displayed.
* The application also has a Generate button that sends the prompt to the OpenAI API and displays the response in the textbox.
* The Clear button clears the prompt entry field and the Quit button closes the application.
# Dependencies
* tkinter
* tkinter.messagebox
* customtkinter
* logging
* openai
* api_key.py (This file should contain the OpenAI API key, and should be in the same directory as the main script)
# Usage
1. Clone or download the repository.
2. Install the required libraries
3. Add your OpenAI API key in the api_key.py file.
4. Run the script using python openaictk.py

# Note
* The customtkinter library is not a part of the official tkinter library, and it's built by the developers. So, it may not work as expected or may not be compatible with your system.
* The api_key.py file is not included in the repository for security reasons.
* The openaictk.py file is the main script for the application.
* The customtkinter.py and customtkinter.pyc files are the custom tkinter library files.
