import flet as ft
import requests
import os
import pathlib
from murf import Murf
import sys 

API_KEY = "" # Initialize as empty string
client = None

def load_api_key_from_file():
    """Read API Key from api_key.py file at the same level as the executable."""
    try:
        if getattr(sys, 'frozen', False):
            base_path = pathlib.Path(sys.executable).parent
        else:
            base_path = pathlib.Path(__file__).parent

        api_key_file_path = base_path / "api_key.py"
        print(f"Looking for API Key file at: {api_key_file_path}") 

        if api_key_file_path.is_file():
            with open(api_key_file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("API_KEY") and "=" in line:
                        parts = line.split("=", 1) 
                        key_value = parts[1].strip()
                        if (key_value.startswith('"') and key_value.endswith('"')) or \
                           (key_value.startswith("'") and key_value.endswith("'")):
                            return key_value[1:-1] 
                        else:
                            return key_value 
            print("Found api_key.py file but did not find line 'API_KEY = ...'")
            return "" 
        else:
            print(f"Could not find file {api_key_file_path}")
            return "" 
    except Exception as e:
        print(f"Error reading api_key.py file: {e}")
        return "" 

def initialize_murf_client(api_key):
    global client
    if not api_key:
        print("API Key is empty, cannot initialize Murf client.")
        client = None
        return False, "API Key is empty."
    try:
        print(f"Trying to initialize Murf client with key: ...{api_key[-4:]}") # Only log last 4 chars for verification
        client = Murf(api_key=api_key)
        print("Murf client initialized successfully.")
        return True, "Initialization successful."
    except Exception as e:
        print(f"Error initializing Murf Client: {e}")
        client = None
        return False, f"API Error: {e}"

print("Loading API Key...")
API_KEY = load_api_key_from_file() 
initialize_murf_client(API_KEY) 

# --- AUTOMATICALLY FETCH AND FILTER ENGLISH VOICES ---
VOICE_MOODS = {} 

if client: 
    try:
        voices = client.text_to_speech.get_voices()
        count_en = 0
        for voice in voices:
            # Check if voice_id starts with 'en-' (case insensitive)
            if voice.voice_id and (voice.voice_id.lower().startswith("en-us-") or voice.voice_id.lower().startswith("en-uk-")):
                display_name = voice.display_name 
                voice_id = voice.voice_id
                moods = voice.available_styles if isinstance(voice.available_styles, list) else []
                if not moods:
                    moods = ['default'] 

                VOICE_MOODS[display_name] = {
                    "voice_id": voice_id,
                    "moods": moods
                }
                count_en += 1

        VOICE_MOODS = dict(sorted(VOICE_MOODS.items()))

    except Exception as e:
        print(f"Error fetching or processing voices from Murf API: {e}")
        print("Using default or empty voices list.")
else:
    print("Murf client not initialized. Cannot fetch voices list.")
    VOICE_MOODS = {}

if not VOICE_MOODS:
     print("WARNING: No voices loaded into VOICE_MOODS.")

def main(page: ft.Page):
    page.title = "AI Voice Generator - Vo Nguyen Giap High School"
    page.window_icon = "assets/icon.png"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.symmetric(horizontal=40, vertical=20)
    page.bgcolor = "#1E1E2F"

    _audio_url_to_save = None

    def save_file_result(e: ft.FilePickerResultEvent):
        nonlocal _audio_url_to_save 
        if not e.path:
            print("User cancelled file save.")
            page.snack_bar = ft.SnackBar(content=ft.Text("File save cancelled."))
            page.snack_bar.open = True
            _audio_url_to_save = None 
            page.update() 
            return

        if not _audio_url_to_save:
            print("Error: No audio URL to save.")
            page.snack_bar = ft.SnackBar(content=ft.Text("Internal error: Audio URL not found."), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        save_path_str = e.path
        if not save_path_str.lower().endswith(".mp3"):
            save_path_str += ".mp3"

        save_path = pathlib.Path(save_path_str)
        print(f"Saving file to: {save_path}")
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Saving to {save_path.name}..."))
        page.snack_bar.open = True
        page.update() 

        try:
            response = requests.get(_audio_url_to_save, stream=True, timeout=60) 
            response.raise_for_status() 

            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print("Audio Saved As:", save_path)
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Saved successfully to {save_path.name}!"), bgcolor=ft.colors.GREEN)
            page.snack_bar.open = True

            current_audio = next((ctl for ctl in page.overlay if isinstance(ctl, ft.Audio)), None)
            if current_audio:
                page.overlay.remove(current_audio)

            audio_src = save_path.resolve().as_uri()
            print(f"Playing audio from: {audio_src}")
            page.overlay.append(ft.Audio(src=audio_src, autoplay=True))
            page.update()

        except requests.exceptions.Timeout:
            error_msg = "Error: Timeout while downloading audio."
            print(error_msg)
            page.snack_bar = ft.SnackBar(content=ft.Text(error_msg), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
        except requests.exceptions.RequestException as req_e:
            error_msg = f"Network error while downloading audio: {req_e}"
            print(error_msg)
            page.snack_bar = ft.SnackBar(content=ft.Text(error_msg), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
        except IOError as io_e:
            error_msg = f"I/O error while saving file: {io_e}"
            print(error_msg)
            page.snack_bar = ft.SnackBar(content=ft.Text(error_msg), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            error_msg = f"Unknown error while saving/playing: {ex}"
            print(error_msg)
            page.snack_bar = ft.SnackBar(content=ft.Text(error_msg), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
        finally:
             _audio_url_to_save = None

    file_picker = ft.FilePicker(on_result=save_file_result)
    if file_picker not in page.overlay:
         page.overlay.append(file_picker)

    title = ft.Text(
    spans=[
        ft.TextSpan(
            "Made with ",
            ft.TextStyle(
                size=36, 
                weight=ft.FontWeight.BOLD, 
                color="#FFD700", 
            ),
        ),
        ft.TextSpan(
            "❤️", 
            ft.TextStyle(
                size=36, 
                weight=ft.FontWeight.BOLD, 
                color=ft.colors.RED,
            ),
        ),
        ft.TextSpan(
            " from Pratik Sanap",
            ft.TextStyle(
                size=36, 
                weight=ft.FontWeight.BOLD, 
                color="#FFD700",
            ),
        ),
    ],
    text_align=ft.TextAlign.CENTER 
    )
    # Show current API Key status
    api_status_text = ft.Text(
        f"API Key: {'Set' if client else 'Not set'}",
        color=ft.colors.GREEN if client else ft.colors.RED,
        italic=True,
        size=12
    )

    api_key_input_dialog = ft.TextField(
        label="Enter new Murf.ai API Key",
        password=True,
        can_reveal_password=True,
        bgcolor="#3e3e4f", 
        color="#ffffff",
        border_color="#FFD700",
        border_radius=10
    )

    def update_api_key(e):
        new_key = api_key_input_dialog.value.strip()
        if not new_key:
            page.snack_bar = ft.SnackBar(content=ft.Text("API Key cannot be empty!"), bgcolor=ft.colors.ORANGE)
            page.snack_bar.open = True
            page.update()
            return

        success, message = initialize_murf_client(new_key)

        if success:
            page.snack_bar = ft.SnackBar(content=ft.Text("API Key updated successfully!"), bgcolor=ft.colors.GREEN)
            api_status_text.value = "API Key: Set"
            api_status_text.color = ft.colors.GREEN
            global API_KEY
            API_KEY = new_key
            # Save to api_key.py for next time
            try:
                with open("api_key.py", "w") as f:
                    f.write(f'API_KEY = "{new_key}"\n')
            except IOError as io_err:
                print(f"Could not save API Key to file: {io_err}")
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error updating API Key: {message}"), bgcolor=ft.colors.RED)
            api_status_text.value = "API Key: Setup error"
            api_status_text.color = ft.colors.RED

        page.snack_bar.open = True
        page.close(api_key_dialog)
        page.update()

    def close_dialog(e):
        page.close(api_key_dialog)
        page.update()

    api_key_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Update API Key", weight=ft.FontWeight.BOLD),
        content=ft.Column(
            [
                api_key_input_dialog,
                ft.Text("Get your API Key from your Murf.ai account.", size=12, italic=True, color=ft.colors.GREY_500)
            ], tight=True, spacing=10
        ),
        actions=[
            ft.TextButton("Save", on_click=update_api_key, style=ft.ButtonStyle(color=ft.colors.GREEN)),
            ft.TextButton("Cancel", on_click=close_dialog, style=ft.ButtonStyle(color=ft.colors.RED)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="#2A2A3B",
        shape=ft.RoundedRectangleBorder(radius=15)
    )

    def open_api_key_dialog(e):
        api_key_input_dialog.value = "" # Clear old value before opening
        page.open(api_key_dialog) # Open dialog
        page.update()

    settings_button = ft.IconButton(
        ft.icons.SETTINGS_OUTLINED,
        tooltip="Change API Key",
        icon_color="#FFD700",
        on_click=open_api_key_dialog
    )

    text_input = ft.TextField(
        label="Enter your text here...",
        width=350,
        bgcolor="#2A2A3B",
        color="#ffffff",
        border_radius=15,
        border_color="#FFD700",
        multiline=True,
        min_lines=3,
        max_lines=4,
        shift_enter=False
    )
    voice_selection = ft.Dropdown( 
        label="Choose Voice",
        options=[ft.dropdown.Option(voice) for voice in VOICE_MOODS.keys()],
        width=350,
        bgcolor="#ffffff",
        border_color="#FFD700",
        color="#ffffff",
        value="Miles"
    )
    mood_selection = ft.Dropdown( 
        label="Choose Mood",
        width=350,
        bgcolor="#ffffff",
        border_color="#FFD700",
        color="#ffffff",
    )
    def update_moods(e=None): 
        selected_voice = voice_selection.value
        available_moods = VOICE_MOODS.get(selected_voice, {}).get("moods", [])
        mood_selection.options = [ft.dropdown.Option(mood) for mood in available_moods]
        mood_selection.value = available_moods[0] if available_moods else None
        page.update() 
    voice_selection.on_change = update_moods
    update_moods()

    voice_speed = ft.Slider( 
        min=-30, max=30, value=0, divisions=12, label="{value}% Pitch",
        active_color="#FFD700", inactive_color="#44445a"
    )
    progress_ring = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=3)
    status_text = ft.Text("", color="#FFD700", size=12)

    def generate_audio():
        if client is None:
            print("Error: Murf client not initialized or API Key invalid.")
            page.snack_bar = ft.SnackBar(content=ft.Text("Error: API Key not set or invalid. Please check settings."), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
            return None 

        progress_ring.visible = True
        status_text.value = "Generating audio..."
        btn_enter.disabled = True
        page.update()

        selected_voice = voice_selection.value
        voice_id = VOICE_MOODS.get(selected_voice,{}).get("voice_id")
        text = text_input.value.strip()
        selected_mood = mood_selection.value
        pitch_value = int(voice_speed.value)

        audio_url = None

        if not text:
            print("ERROR, you need some text...")
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter some text!"), bgcolor=ft.colors.ORANGE)
            page.snack_bar.open = True
        elif not selected_mood:
             print("ERROR, you need to select a mood...")
             page.snack_bar = ft.SnackBar(content=ft.Text("Please select a mood!"), bgcolor=ft.colors.ORANGE)
             page.snack_bar.open = True
        elif not voice_id:
             print("ERROR, voice ID not found...")
             page.snack_bar = ft.SnackBar(content=ft.Text("Error: Voice ID not found."), bgcolor=ft.colors.RED)
             page.snack_bar.open = True
        else:
            print(f"Generating audio with Voice: {selected_voice}, Mood: {selected_mood}, Pitch: {pitch_value}")
            try:
                response = client.text_to_speech.generate(
                    format="MP3",
                    sample_rate=48000,
                    channel_type="STEREO",
                    text=text,
                    voice_id=voice_id,
                    style=selected_mood,
                    pitch=pitch_value
                )
                print("API Response received.")
                if hasattr(response, "audio_file") and response.audio_file:
                    print(f"Audio URL: {response.audio_file}")
                    audio_url = response.audio_file
                    status_text.value = "Audio generated successfully!"
                else:
                    error_detail = getattr(response, 'message', 'No audio_file returned.')
                    print(f"Error from Murf API or audio_file not found: {error_detail}")
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"API Error: {error_detail}"), bgcolor=ft.colors.RED)
                    page.snack_bar.open = True

            except Exception as e:
                error_msg = f"Error calling Murf API: {e}"
                print(error_msg)
                page.snack_bar = ft.SnackBar(content=ft.Text(error_msg), bgcolor=ft.colors.RED)
                page.snack_bar.open = True

        progress_ring.visible = False
        btn_enter.disabled = False
        page.update()
        return audio_url

    def generate_and_show_save_dialog(e):
        nonlocal _audio_url_to_save
        audio_url = generate_audio()
        if audio_url:
            _audio_url_to_save = audio_url
            print("Received audio URL, opening save file dialog...")
            status_text.value = "Please choose where to save the file..."
            page.update()
            file_picker.save_file(
                dialog_title="Save audio file",
                file_name="generated_audio.mp3",
                allowed_extensions=["mp3"]
            )
        else:
            print("Could not generate audio URL, cannot open save dialog.")
            status_text.value = "Audio generation failed."
            page.update()

    btn_enter = ft.ElevatedButton(
        "Generate and Save Audio",
        bgcolor="#FFD700",
        color="#1E1E2F",
        on_click=generate_and_show_save_dialog,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
        height=50
    )

    input_container = ft.Container(
        content=ft.Column(
            [
                text_input,
                voice_selection,
                mood_selection,
                ft.Text("Adjust Pitch", size=18, weight=ft.FontWeight.BOLD, color="#FFD700"),
                voice_speed,
                ft.Row(
                    [btn_enter, progress_ring, status_text],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                )
            ],
            spacing=15,
        ),
        padding=20,
        border_radius=20,
        bgcolor="#2A2A3B",
        shadow=ft.BoxShadow(blur_radius=12, spread_radius=2, color=ft.colors.with_opacity(0.5, "#FFD700"))
    )

    page.add(
        ft.Row(
            [title, ft.Container(expand=True), settings_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),

        ft.Column(
            controls=[
                api_status_text,
                ft.Divider(
                    height=10, color=ft.colors.with_opacity(0.5, "#FFD700")),
                input_container,
            ],
            expand=True,           
            scroll=ft.ScrollMode.AUTO  
        )
    )
    page.update()

# Run the App
if __name__ == "__main__":
    ft.app(target=main, assets_dir=".")