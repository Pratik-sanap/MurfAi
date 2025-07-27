# AI Voice Generator (Flet & Murf.ai)

> Made with ❤️ from Pratik Sanap

A simple desktop application built with Python and Flet to generate AI voice from text using the Murf.ai API.

![Application Screenshot](assets/Screenshot.png)

## Features

*   Multi-line text input for text-to-speech conversion.
*   Select voices from a dynamically updated list of available **US English (en-US)** and **UK English (en-UK)** voices from Murf.ai.
*   Choose appropriate moods/styles for the selected voice.
*   Adjust the pitch of the generated speech.
*   Generate and open a dialog to **save the audio file (MP3)** to a user-selected location.
*   Update the Murf.ai **API Key** through a dedicated settings dialog.
*   Automatically **persists the API Key** in an `api_key.py` file for subsequent runs.
*   Displays the current API Key status (set or not set).
*   User-friendly interface built with Flet.
## Prerequisites

*   **Python 3.11+**
*   **pip** (Python package installer)
*   A **Murf.ai** account and a valid **API Key**. You can obtain your API Key from your Murf.ai account dashboard.

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone 
    cd AIVoice-MurfAI
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
   Run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key:**
    *   Add the following line to `api_key.py`, replacing `"YOUR_MURFAI_API_KEY"` with your actual Murf.ai API Key:
        ```python
        API_KEY = "YOUR_MURFAI_API_KEY"
        ```

## Usage

1.  **Run the Application:**
    Open your terminal or command prompt in the project's root directory (with the virtual environment activated, if used) and run:
    ```bash
    python main.py
    ```
    *(Or `python3 main.py` depending on your system configuration)*

2.  **Using the Interface:**
    *   Enter the text you want to convert in the large text area.
    *   Select a Voice and Mood from the dropdown menus.
    *   Adjust the Pitch slider if desired.
    *   Click the **"Generate and Save Audio"** button.
    *   A file dialog will appear; choose a location and filename to save the MP3 file.
    *   The audio file will play automatically after saving.

## Packaging for Windows

You can package this application into a standalone Windows executable (`.exe`) using Flet's built-in packaging tool (which utilizes PyInstaller). This allows users to run the application without needing Python or installing dependencies.

**Prerequisites:**

*   Ensure the application runs correctly using `python main.py`.
*   Have an icon file ready, preferably in `.ico` format for best results on Windows (e.g., `assets/favicon.ico`).

**Steps:**

1.  Open your **Terminal**, **Command Prompt**, or **PowerShell**.
2.  Navigate (`cd`) to the root directory of your project (where `main.py` is located).
3.  **Activate your virtual environment** (if you are using one):
    ```bash
    # Windows Command Prompt / PowerShell
    .\venv\Scripts\activate
    ```
4.  Run the `flet pack` command. Use the command that worked successfully for you:
    ```bash
    flet pack main.py --name "AIVoiceGenerator" --icon "assets/favicon.ico" --add-data "assets;assets" --add-data "api_key.py;."
    ```
    *   `main.py`: Your main application script.
    *   `--name "AIVoiceGenerator"`: Sets the name of the executable and the output folder.
    *   `--icon "assets/favicon.ico"`: Specifies the icon file for the `.exe`.
    *   `--add-data "assets;assets"`: Bundles the entire `assets` folder into the package, making `assets/favicon.ico` (for the window icon) accessible.
    *   `--add-data "api_key.py;."`: Bundles the `api_key.py` file into the root directory of the package, allowing the application to read it on startup and potentially overwrite it.

5.  **Wait for the process to complete.** This might take several minutes. Ignore warnings unless there are specific errors.

6.  **Find the Result:** Once finished, you'll find the packaged application inside the `dist` directory, within a sub-folder named after your `--name` argument (e.g., `dist/AIVoiceGenerator`).

**Running the Packaged App:**

*   Navigate into the `dist/AIVoiceGenerator` folder.
*   Double-click the `AIVoiceGenerator.exe` file to run the application.
*   You can copy the entire `AIVoiceGenerator` folder to another Windows machine (even one without Python installed) and run the `.exe` from there.


## Technology Stack

*   **[Flet](https://flet.dev/)**: Build cross-platform Flutter frontends in Python.
*   **[Murf Python Library](https://github.com/murf-ai/)**: Python client for the Murf.ai API.
*   **[Requests](https://requests.readthedocs.io/en/latest/)**: Python library for making HTTP requests (used for downloading the audio file).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details (You should create a `LICENSE` file containing the MIT license text).

---