# AIVoice-MurfAI

AIVoice-MurfAI is a Python application that utilizes the Murf API to generate audio from text input. The application features a user-friendly interface built with the Flet library, allowing users to select voices, moods, and adjust pitch for audio generation.

## Features

- Load and manage API keys securely.
- Fetch and display available English voices from the Murf API.
- Generate audio from user-provided text with customizable voice and mood settings.
- Save generated audio files in MP3 format.

## Requirements

To run this application, you need to have Python installed along with the required libraries. You can install the necessary dependencies using the following command:

```
pip install -r requirements.txt
```

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/AIVoice-MurfAI.git
   ```

2. Navigate to the project directory:

   ```
   cd AIVoice-MurfAI
   ```

3. Create a file named `api_key.py` in the project directory and add your Murf API key:

   ```python
   API_KEY = "your_api_key_here"
   ```

4. Run the application:

   ```
   python main.py
   ```

## Usage

- Open the application and enter your text in the provided text field.
- Select your desired voice and mood from the dropdown menus.
- Adjust the pitch using the slider.
- Click the "Generate and Save Audio" button to create and save your audio file.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.