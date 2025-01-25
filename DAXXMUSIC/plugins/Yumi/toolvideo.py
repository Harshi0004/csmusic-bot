import os
import tempfile
from pyrogram import Client, filters
from pyrogram.types import Message
from pydub import AudioSegment
import speech_recognition as sr
import subprocess
from DAXXMUSIC import app

# --------------------------------------

def convert_video_to_text(video_path):
    try:
        # Create a temporary audio file for the conversion
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_file:
            audio = AudioSegment.from_file(video_path)
            audio.export(audio_file.name, format="wav")
        
        # Use speech recognition to convert audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file.name) as source:
            audio_data = recognizer.record(source)
        
        text = recognizer.recognize_google(audio_data)
        
        # Clean up temporary audio file
        os.remove(audio_file.name)
        
        return text
    except Exception as e:
        return f"Error during speech recognition: {str(e)}"

# ----------------------------------------------

@app.on_message(filters.command("vtxt") & filters.reply)
def convert_video_to_text_cmd(_, message: Message):
    try:
        video_path = message.reply_to_message.download("video.mp4")
        
        # Convert video to text
        text_result = convert_video_to_text(video_path)

        if text_result.startswith("Error"):
            return message.reply(text_result)  # If there's an error in conversion
        
        # Save the text result into a temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".txt") as temp_file:
            temp_file.write(text_result)
            temp_file_path = temp_file.name
        
        # Send the text file as a document
        message.reply_document(temp_file_path)
        
        # Clean up the temporary text file
        os.remove(temp_file_path)
    except Exception as e:
        message.reply(f"An error occurred: {str(e)}")

@app.on_message(filters.command("remove", prefixes="/") & filters.reply)
def remove_media(client, message: Message):
    try:
        replied_message = message.reply_to_message

        if replied_message.video:
            if len(message.command) > 1:
                command = message.command[1].lower()

                # Check if user wants to remove audio or video
                if command == "audio":
                    file_path = app.download_media(replied_message.video)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                        audio = AudioSegment.from_file(file_path)
                        audio = audio.set_channels(1)
                        audio.export(temp_audio.name, format="mp3")
                        app.send_audio(message.chat.id, temp_audio.name)
                    os.remove(file_path)
                    os.remove(temp_audio.name)
                elif command == "video":
                    file_path = app.download_media(replied_message.video)
                    output_file = tempfile.mktemp(suffix=".mp4")
                    subprocess.run(["ffmpeg", "-i", file_path, "-c", "copy", "-an", output_file], check=True)
                    app.send_video(message.chat.id, output_file)
                    os.remove(file_path)
                    os.remove(output_file)
                else:
                    app.send_message(message.chat.id, "Invalid command. Please use either /remove audio or /remove video.")
            else:
                app.send_message(message.chat.id, "Please specify whether to remove audio or video using /remove audio or /remove video.")
        else:
            app.send_message(message.chat.id, "The replied message is not a video.")
    except Exception as e:
        app.send_message(message.chat.id, f"An error occurred: {str(e)}")
