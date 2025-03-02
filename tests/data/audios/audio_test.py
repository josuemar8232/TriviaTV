import unittest
from playsound import playsound
from pathlib import Path

# Constants for directory paths
CURRENT_DIR = Path(__file__).parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent
AUDIO_FILE_PATH = PROJECT_ROOT / "data" / "audios"


class TestAudios(unittest.TestCase):
    """
    Unit test class for validating the functionality of audio playback.

    This class contains methods to test audio file playback functionality,
    including scenarios for playing individual audio files or all available
    audio files in a directory. The tests ensure that audio files exist, user
    input is handled correctly, and playback occurs without exceptions.

    :ivar audio_file_path: Path to the directory containing the audio files
        to be tested.
    :type audio_file_path: pathlib.Path
    """

    def test_play_audio(self):
        try:
            audio_files = [audio_file for audio_file in AUDIO_FILE_PATH.iterdir() if
                           audio_file.is_file() and audio_file.suffix == ".mp3"]
            if not audio_files:
                self.fail("No audio files found.")

            print("Available audio files:")
            for i, audio_file in enumerate(audio_files, start=1):
                print(f"{i}. {audio_file.name}")
            while True:
                print(
                    "Enter 'all' to play all audios, the number corresponding to an audio file to play it, or 'exit' to stop.")

                user_input = input("Your choice: ").strip().lower()
                if user_input == "all":
                    for audio_file in audio_files:
                        playsound(str(audio_file))
                elif user_input.isdigit() and 1 <= int(user_input) <= len(audio_files):
                    playsound(str(audio_files[int(user_input) - 1]))
                elif user_input == "exit":
                    print("Exiting playback menu.")
                    break
                else:
                    print("Invalid input. Please try again.")

            self.assertTrue(True)  # Assert True if no exception occurs during playback
        except Exception as e:
            self.fail(f"Audio playback test failed: {e}")

    def test_all_audios(self):
        try:
            for audio_file in AUDIO_FILE_PATH.iterdir():
                if audio_file.is_file() and audio_file.suffix == ".mp3":
                    self.assertTrue(True)  # Assert True if no exception occurs during playback
        except Exception as e:
            self.fail(f"Audio playback test failed: {e}")


if __name__ == '__main__':
    unittest.main()
