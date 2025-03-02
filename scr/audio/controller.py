import os
from typing import Iterator
from pathlib import Path

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from playsound import playsound


class AudioController:
    """
    Manages audio generation and saving functions leveraging ElevenLabs services.

    This class facilitates the generation of audio content using ElevenLabs'
    text-to-speech services and supports saving the generated audio to a local
    file system. Designed for efficient handling of streamed audio and file
    management.

    :ivar client: Instance of ElevenLabs client used for text-to-speech processing.
    :type client: ElevenLabs
    """

    def generate_audio(self, script) -> Iterator[bytes]:
        if not script:
            raise ValueError("script cannot be empty")

        eleven_labs_key = os.environ.get("ELEVEN_LABS_KEY")
        if not eleven_labs_key:
            raise EnvironmentError("ELEVEN_LABS_KEY environment variable is not set")
        client = ElevenLabs(
            api_key=eleven_labs_key
        )

        response = client.text_to_speech.convert_as_stream(
            text=script,
            voice_id="22VndfJPBU7AZORAZZTT",
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                speed=1.08,
                stability=0.15,
                similarity_boost=0.53,
                style=0.80,
                use_speaker_boost=True
            )
        )

        return response

    def save_audio_to_file(self, audio, file_name: str) -> None:
        # Constants for directory paths
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        audio_file_path = project_root / "data" / "audios"

        # Ensure the directory exists
        audio_file_path.mkdir(parents=True, exist_ok=True)

        # Define the full file path with .mp3 extension
        file_path = audio_file_path / f"{file_name}.mp3"

        # Save the audio bytes to the file
        with open(file_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
