from operator import index

from scr.audio.controller import AudioController
from scr.photos.controller import PhotosController
from scr.script.controller import ScriptController


def main():
    """
    Main function to generate script content and convert it into audio.
    """
    # Instantiate controllers
    script_controller = ScriptController()
    audio_controller = AudioController()
    photos_controller = PhotosController()

    # Prompt for content generation
    user_input = input("Enter a topic (e.g., drinks, dishes, places): ")
    prompt = f"""
      I need you to list Google Image search prompts for a trivia game, NO ADDED COMMENTS. Please use the following template for each prompt: [Category] [Specific Subject/Object/Action] [Visual Descriptor] [Optional: Time Period/Style/Modifier] photo/image.

For each of the following trivia categories, provide one Google Image search prompt using the template:

{user_input.replace(',', '\n')}

Please fill in each part of the template with relevant and specific terms for each category.
      """
    generated_text = script_controller.generate_content(prompt)

    # Split the generated text into individual options
    options = generated_text.split("\n")

    # Remove asterisk (*) at the beginning of each option, strip whitespace, and filter out empty values
    options_array = [option.lstrip("*").strip() for option in options if option.strip()]

    # Generate audio from the content and Save the audio to a file
    for index, option in enumerate(options_array):
        # audio_stream = audio_controller.generate_audio(option)
        # audio_controller.save_audio_to_file(audio_stream, option)
        photos_controller.generate_photos(option, user_input.split(',')[index])


if __name__ == "__main__":
    main()
