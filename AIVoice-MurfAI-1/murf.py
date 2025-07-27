class Murf:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.murf.ai/v1"

    def get_voices(self):
        """Fetch available voices from the Murf API."""
        response = requests.get(f"{self.base_url}/voices", headers={"Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        return response.json().get("voices", [])

    def generate_audio(self, text, voice_id, style, pitch, format="MP3", sample_rate=48000, channel_type="STEREO"):
        """Generate audio from text using the specified voice and style."""
        payload = {
            "text": text,
            "voice_id": voice_id,
            "style": style,
            "pitch": pitch,
            "format": format,
            "sample_rate": sample_rate,
            "channel_type": channel_type
        }
        response = requests.post(f"{self.base_url}/text-to-speech", json=payload, headers={"Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        return response.json()