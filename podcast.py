import os
from google.cloud import texttospeech
from pydub import AudioSegment


def synthesize_speech_for_speaker(text, voice_name, output_filename, language_code="en-US"):
    """Synthesizes speech from text for a specific voice and saves it to a file."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filename}" using voice {voice_name}')
    
    return output_filename


def create_podcast_from_script(script, output_podcast_filename="podcast_output.wav"):
    """
    Creates a podcast from a script with multiple speakers.

    Args:
        script (list): A list of dictionaries, where each dictionary has:
                       'speaker_voice': The voice name (e.g., "en-US-Studio-O")
                       'text': The text to be spoken by that speaker.
        output_podcast_filename (str): The name of the final podcast WAV file.
    """
    segment_files = []
    combined_audio = AudioSegment.empty()

    # Ensure the 'temp_audio_segments' directory exists
    temp_dir = "temp_audio_segments"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    print("Starting podcast generation...\n")

    for i, part in enumerate(script):
        speaker_voice = part.get("speaker_voice")
        text_to_speak = part.get("text")

        if not speaker_voice or not text_to_speak:
            print(f"Skipping part {i+1} due to missing voice or text.")
            continue

        segment_filename = os.path.join(temp_dir, f"segment_{i+1}_{speaker_voice.replace('-', '_')}.wav")

        print(f"Synthesizing segment {i+1} for voice {speaker_voice}...")
        synthesized_file = synthesize_speech_for_speaker(text_to_speak, speaker_voice, segment_filename)

        if synthesized_file:
            segment_files.append(synthesized_file)
            try:
                audio_segment = AudioSegment.from_wav(synthesized_file)
                # Add a short pause between segments, except for the very first one
                if i > 0:
                    combined_audio += AudioSegment.silent(duration=800) # 800 milisecond pause
                combined_audio += audio_segment
                print(f"Segment {i+1} added to podcast.")
            except Exception as e:
                print(f"Error processing audio segment {synthesized_file}: {e}")
        else:
            print(f"Failed to synthesize segment {i+1}.")
        print("-" * 30)


    if combined_audio:
        try:
            print(f"\nExporting combined podcast to {output_podcast_filename}...")
            combined_audio.export(output_podcast_filename, format="wav")
            print(f"Podcast successfully created: {output_podcast_filename}")
        except Exception as e:
            print(f"Error exporting final podcast: {e}")
    else:
        print("No audio segments were successfully processed. Podcast not created.")

    # Clean up temporary segment files
    print("\nCleaning up temporary files...")
    for f in segment_files:
        try:
            os.remove(f)
        except OSError as e:
            print(f"Error deleting file {f}: {e}")
    if os.path.exists(temp_dir) and not os.listdir(temp_dir):
        os.rmdir(temp_dir)
    print("Cleanup complete.")


if __name__ == "__main__":
    female_voice = "en-US-Chirp3-HD-Kore"
    male_voice = "en-US-Chirp3-HD-Schedar"

    podcast_script = [
        {
            "speaker_voice": female_voice,
            "text": "Welcome to 'Tech Forward', the podcast that explores the cutting edge of technology. I'm your host, Evelyn..."
        },
        {
            "speaker_voice": male_voice,
            "text": "Thanks for having me Evelyn! It's great to be here to discuss the future of AI..."
        },
        {
            "speaker_voice": female_voice,
            "text": "Today, we're diving deep into how generative AI is reshaping industries. Mark, what are your initial thoughts on its impact?"
        },
        {
            "speaker_voice": male_voice,
            "text": "Well, Evelyn, the impact is already massive. From content creation to drug discovery, generative AI is acting as a powerful catalyst for innovation!"
        },
        {
            "speaker_voice": female_voice,
            "text": "That's a fascinating perspective. We'll explore that more after a short break... Stay with us on 'Tech Forward'."
        }
    ]

    final_podcast_file = "multispeaker_podcast.wav"
    create_podcast_from_script(podcast_script, final_podcast_file)
