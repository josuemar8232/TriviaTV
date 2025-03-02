from scr.audio.controller import AudioController
from scr.script.controller import ScriptController


def main():
    """
    Main function to generate script content and convert it into audio.
    """
    # Instantiate controllers
    script_controller = ScriptController()
    audio_controller = AudioController()

    # Prompt for content generation
    prompt = "Lista solo opciones sin comentarios, de 3 bebidas populares en México."
    generated_text = script_controller.generate_content(prompt)

    # Split the generated text into individual options
    options = generated_text.split("\n")

    # Remove asterisk (*) at the beginning of each option, strip whitespace, and filter out empty values
    options_array = [option.lstrip("*").strip() for option in options if option.strip()]

    # Generate audio from the content and Save the audio to a file
    for option in options_array:
        audio_stream = audio_controller.generate_audio(option)
        audio_controller.save_audio_to_file(audio_stream, option)

if __name__ == "__main__":
    main()
