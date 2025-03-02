import os
from google import genai


class ScriptController:
    """
    Handles operations related to script content generation.

    This class provides mechanisms to generate textual content programmatically based on the input
    provided. It interacts with an external generative AI service to leverage language model
    capabilities. The primary purpose of this class is to serve as a utility for content-generation
    tasks, ensuring seamless API communication and simplified usage for the caller.

    :ivar some_attribute: Description of some attribute relevant to the class.
    :type some_attribute: str
    """

    def generate_content(self, prompt) -> str:
        """
        Generates content based on a given prompt using a specified model. This method utilizes
        the Gemini model hosted by the GenAI service to produce contextually relevant
        textual content. The function takes a prompt as input, interacts with the external
        API, and retrieves the generated content as the response. The function assumes
        an active API key is provided in the environment variable `GOOGLE_KEY`.

        :param prompt: Text input that the function uses as a basis for generating content.
        :type prompt: str
        :return: Generated content based on the given prompt.
        :rtype: str
        :raises ValueError: If the prompt is empty or None.
        :raises EnvironmentError: If the required `GOOGLE_KEY` environment variable is not set.
        :raises APIError: If an error occurs during the generation request to the external API.
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")

        google_key = os.environ.get("GOOGLE_KEY")
        if not google_key:
            raise EnvironmentError("GOOGLE_KEY environment variable is not set")

        client = genai.Client(api_key=google_key)

        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
        )

        return response.text
