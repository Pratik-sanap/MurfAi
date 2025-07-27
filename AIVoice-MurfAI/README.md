# AIVoice-MurfAI

AIVoice-MurfAI is a Python application that utilizes the Murf API to generate audio from text using various voice options. The application features a user-friendly interface built with Flet, allowing users to easily input text, select voices and moods, and save the generated audio files.

## Features

- Load and manage API keys securely.
- Fetch and display available voices from the Murf API.
- Generate audio from user-provided text with customizable voice and mood options.
- Save generated audio files in MP3 format.

## Requirements

To run this project, you need to have Python installed along with the required packages. You can install the necessary dependencies using the following command:

```
pip install -r requirements.txt
```

## Setup

1. Clone the repository to your local machine:

   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```
   cd AIVoice-MurfAI
   ```

3. Create a file named `api_key.py` in the project root and add your Murf API key:

   ```python
   API_KEY = "your_api_key"
   ```

4. Run the application:

   ```
   python main.py
   ```

## Usage

- Open the application and enter the text you want to convert to audio.
- Select the desired voice and mood from the dropdown menus.
- Adjust the pitch using the slider.
- Click the "Generate and Save Audio" button to create and save the audio file.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.