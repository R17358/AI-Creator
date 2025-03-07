import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(file_path):
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(file_path)
    wav_path = "converted_audio.wav"
    audio.export(wav_path, format="wav")
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
        
        try:
            print("Transcribing...")
            text = recognizer.recognize_google(audio_data, language='en-in')
            print("Transcription Complete!")
            
            # Save transcription to a text file
            with open("lyrics.txt", "w", encoding="utf-8") as f:
                f.write(text)
            
            print("Lyrics saved to lyrics.txt")
        
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
        except sr.RequestError:
            print("Could not request results, check your internet connection")

# Example Usage
transcribe_audio("sample_song.mp3")
