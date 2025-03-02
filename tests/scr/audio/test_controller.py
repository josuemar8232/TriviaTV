import unittest
from pathlib import Path
from scr.audio.controller import AudioController
from unittest.mock import MagicMock, patch


class TestAudioController(unittest.TestCase):
    """
    Unit test class for validating the functionality of AudioController.
    Tests include verifying the save_audio_to_file method handles audio data
    correctly, ensures proper file saving behavior, and handles edge cases.
    """

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
