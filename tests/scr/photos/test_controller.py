import unittest
from pathlib import Path
from scr.photos.controller import PhotosController
from unittest.mock import MagicMock, patch


class TestPhotosController(unittest.TestCase):
    """
    Unit tests for the PhotosController class, validating its functionalities including photo generation,
    handling API calls, and file saving capabilities under various scenarios.
    """

    @patch("scr.photos.controller.os.environ.get", return_value=None)
    def test_generate_photos_missing_api_key(self, mock_environ_get):
        with self.assertRaises(EnvironmentError) as context:
            controller = PhotosController()
            controller.generate_photos("test query")
        self.assertEqual(
            str(context.exception),
            "GOOGLE_SEARCH_KEY environment variable is not set"
        )

    @patch("scr.photos.controller.os.environ.get", side_effect=["mocked_search_key", None])
    def test_generate_photos_missing_search_engine_id(self, mock_environ_get):
        with self.assertRaises(EnvironmentError) as context:
            controller = PhotosController()
            controller.generate_photos("test query")
        self.assertEqual(
            str(context.exception),
            "SEARCH_ENGINE_ID environment variable is not set"
        )

    @patch("scr.photos.controller.requests.get")
    @patch("scr.photos.controller.os.environ.get", side_effect=["mocked_search_key", "mocked_search_engine_id"])
    def test_generate_photos_api_call(self, mock_environ_get, mock_requests_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [{"link": "http://example.com/photo1.jpg"}]
        }
        mock_response.status_code = 200
        mock_response.content = b"image_data"  # Adding actual byte content to avoid TypeError
        mock_requests_get.return_value = mock_response

        controller = PhotosController()
        with patch("scr.photos.controller.Path.open", new_callable=MagicMock) as mock_open:
            with patch("scr.photos.controller.Path.mkdir") as mock_mkdir:
                controller.generate_photos("test query")

                # Assert that the API was called with correct parameters
                mock_requests_get.assert_any_call(
                    'https://www.googleapis.com/customsearch/v1',
                    params={
                        'q': 'test query',
                        'key': 'mocked_search_key',
                        'cx': 'mocked_search_engine_id',
                        'searchType': 'image',
                        'gl': 'MX',
                    }
                )
                # Assert directory creation
                mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch("scr.photos.controller.requests.get")
    @patch("scr.photos.controller.os.environ.get", side_effect=["mocked_search_key", "mocked_search_engine_id"])
    def test_generate_photos_saves_images(self, mock_environ_get, mock_requests_get):
        mock_search_response = MagicMock()
        mock_search_response.json.return_value = {
            "items": [{"link": "http://example.com/photo1.jpg"}]
        }
        mock_search_response.status_code = 200

        mock_image_response = MagicMock()
        mock_image_response.content = b"image_data"
        mock_image_response.status_code = 200

        mock_requests_get.side_effect = [mock_search_response, mock_image_response]

        controller = PhotosController()
        with patch("scr.photos.controller.Path.open", new_callable=MagicMock) as mock_open:
            with patch("scr.photos.controller.Path.mkdir") as mock_mkdir:
                with patch("scr.photos.controller.Path") as mock_path:
                    mock_path.return_value = Path("data/photos/photo_1.jpg")
                    mock_mkdir.return_value = None  # Ensure mkdir is called for the directory
                    mock_path("data/photos").mkdir(parents=True, exist_ok=True)  # Mock directory creation
                    controller.generate_photos("test query")
                    # Assert that the image data was written to the file
                    mock_open.assert_called_once_with(Path("data/photos/photo_1.jpg"), "wb")
                    mock_open().write.assert_called_once_with(b"image_data")

    @patch("scr.photos.controller.requests.get", side_effect=Exception("Network error"))
    @patch("scr.photos.controller.os.environ.get", side_effect=["mocked_search_key", "mocked_search_engine_id"])
    def test_generate_photos_handles_network_errors(self, mock_environ_get, mock_requests_get):
        controller = PhotosController()
        with self.assertRaises(Exception) as context:
            controller.generate_photos("test query")
        self.assertEqual(str(context.exception), "Network error")
