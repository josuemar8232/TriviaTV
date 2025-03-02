import unittest
from scr.script.controller import ScriptController
from unittest.mock import patch, MagicMock


class TestScriptController(unittest.TestCase):
    """
    Unit test class for validating the functionality of ScriptController's generate_content method.
    Tests ensure proper handling of inputs, responses, and exceptions.
    """

    @patch("scr.script.controller.genai.Client")
    def test_generate_content_valid_prompt(self, mock_client):
        """Test generate_content with a valid prompt."""
        mock_response = MagicMock()
        mock_response.text = "Generated content."
        mock_client_instance = mock_client.return_value
        mock_client_instance.models.generate_content.return_value = mock_response

        with patch.dict("os.environ", {"GOOGLE_KEY": "dummy_key"}):
            controller = ScriptController()
            prompt = "Describe the benefits of machine learning in 3 words."
            result = controller.generate_content(prompt)

            mock_client.assert_called_once_with(api_key="dummy_key")  # Ensures API key usage
            mock_client_instance.models.generate_content.assert_called_once_with(
                model="gemini-2.0-flash-lite",
                contents=prompt,
            )
            self.assertEqual(result, "Generated content.")

    @patch("scr.script.controller.genai.Client")
    def test_generate_content_empty_prompt(self, mock_client):
        """Test generate_content raises ValueError for an empty prompt."""
        mock_client_instance = mock_client.return_value
        with patch.dict("os.environ", {"GOOGLE_KEY": "dummy_key"}):
            controller = ScriptController()
            with self.assertRaises(ValueError) as context:
                controller.generate_content("")
            self.assertEqual(str(context.exception), "Prompt cannot be empty")
        mock_client_instance.models.generate_content.assert_not_called()

    @patch("scr.script.controller.genai.Client")
    def test_generate_content_no_google_key(self, mock_client):
        """Test generate_content raises EnvironmentError if GOOGLE_KEY is not set."""
        mock_client_instance = mock_client.return_value
        with patch.dict("os.environ", {"GOOGLE_KEY": ""}):
            controller = ScriptController()
            with self.assertRaises(EnvironmentError):
                controller.generate_content("This is a test prompt.")
        mock_client_instance.models.generate_content.assert_not_called()

    @patch("scr.script.controller.genai.Client")
    def test_generate_content_api_error(self, mock_client):
        """Test generate_content raises exception if API call fails."""
        mock_client_instance = mock_client.return_value
        mock_client_instance.models.generate_content.side_effect = Exception("API Error")

        controller = ScriptController()
        with self.assertRaises(Exception):
            controller.generate_content("This is a test prompt.")
