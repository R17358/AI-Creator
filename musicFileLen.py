from mutagen import File

def get_audio_length(file_path):
    audio = File(file_path)  # Load any audio file format
    if audio and audio.info:
        duration = audio.info.length  # Get duration in seconds
        # minutes = int(duration // 60)  # Convert to minutes
        # seconds = int(duration % 60)  # Get remaining seconds
        # return f"{minutes}:{seconds:02d}"  # Format as MM:SS
        return duration
    else:
        return "Could not retrieve duration"

# # Example usage
# file_path = "song.mp3"  # Replace with your file path
# print(get_audio_length(file_path))
