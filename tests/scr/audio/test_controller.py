import unittest
from pathlib import Path
from scr.audio.controller import AudioController
from unittest.mock import MagicMock, patch


class TestAudioController(unittest.TestCase):
    """
    Unit tests for the AudioController class, validating its functionalities including audio generation and saving.

    These tests ensure the proper behavior of the AudioController methods under various scenarios, including
    valid inputs, empty inputs, handling of required configurations, and file saving capabilities.

    """

    @patch("scr.audio.controller.os.environ.get", return_value="mocked_api_key")
    @patch("scr.audio.controller.ElevenLabs")
    def test_generate_audio_valid_script(self, mock_elevenlabs, mock_environ_get):
        """
        Test that generate_audio works with a valid script input.
        """
        audio_stream = [b"audio_chunk1", b"audio_chunk2"]
        client_instance = MagicMock()
        voice_settings_mock = MagicMock()
        client_instance.text_to_speech.convert_as_stream.return_value = iter(audio_stream)
        mock_elevenlabs.return_value = client_instance

        controller = AudioController()
        with patch("scr.audio.controller.VoiceSettings", return_value=voice_settings_mock):
            result = list(controller.generate_audio("This is a test script."))

        # Assert that the client was initialized
        mock_environ_get.assert_called_once_with("ELEVEN_LABS_KEY")
        mock_elevenlabs.assert_called_once_with(api_key="mocked_api_key")
        client_instance.text_to_speech.convert_as_stream.assert_called_once_with(
            text="This is a test script.",
            voice_id="22VndfJPBU7AZORAZZTT",
            model_id="eleven_multilingual_v2",
            voice_settings=voice_settings_mock
        )
        self.assertEqual(result, audio_stream)

    @patch("scr.audio.controller.os.environ.get", return_value="mocked_api_key")
    def test_generate_audio_empty_script(self, mock_environ_get):
        """
        Test that generate_audio raises ValueError when script is empty.
        """
        controller = AudioController()

        with self.assertRaises(ValueError) as context:
            controller.generate_audio("")

        self.assertEqual(str(context.exception), "script cannot be empty")

    @patch("scr.audio.controller.os.environ.get", return_value=None)
    def test_generate_audio_missing_api_key(self, mock_environ_get):
        """
        Test that generate_audio raises EnvironmentError when ELEVEN_LABS_KEY is not set.
        """
        controller = AudioController()

        with self.assertRaises(EnvironmentError) as context:
            controller.generate_audio("This is a test script.")

        self.assertEqual(str(context.exception), "ELEVEN_LABS_KEY environment variable is not set")

    @patch("scr.audio.controller.Path.mkdir")
    @patch("builtins.open", new_callable=MagicMock)
    def test_save_audio_to_file_valid_input(self, mock_open, mock_mkdir):
        """
        Test saving a valid audio stream to a file.
        """
        audio_chunks = [b"chunk1", b"chunk2", b"chunk3"]
        file_name = "test_audio"
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        controller = AudioController()
        controller.save_audio_to_file(audio_chunks, file_name)

        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        audio_file_path = project_root / "data" / "audios"

        mock_mkdir.assert_called_once()
        mock_open.assert_called_once_with(Path(audio_file_path / "test_audio.mp3"), "wb")
        mock_file.write.assert_any_call(b"chunk1")
        mock_file.write.assert_any_call(b"chunk2")
        mock_file.write.assert_any_call(b"chunk3")

    @patch("scr.audio.controller.Path.mkdir")
    @patch("builtins.open", new_callable=MagicMock)
    def test_save_audio_to_file_no_audio_chunks(self, mock_open, mock_mkdir):
        """
        Test saving audio to a file when the audio iterator is empty.
        """
        audio_chunks = []
        file_name = "empty_audio"
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        controller = AudioController()
        controller.save_audio_to_file(audio_chunks, file_name)

        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        audio_file_path = project_root / "data" / "audios"

        mock_mkdir.assert_called_once()
        mock_open.assert_called_once_with(Path(audio_file_path / "empty_audio.mp3"), "wb")
        mock_file.write.assert_not_called()

    @patch("scr.audio.controller.Path.mkdir")
    @patch("builtins.open", new_callable=MagicMock)
    def test_save_audio_to_file_directory_creation(self, mock_open, mock_mkdir):
        """
        Test that the method ensures the directory is created if it does not exist.
        """
        audio_chunks = [b"chunk1"]
        file_name = "new_directory_test"
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        controller = AudioController()
        controller.save_audio_to_file(audio_chunks, file_name)

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
