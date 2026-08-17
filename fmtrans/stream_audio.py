import sys
from pytubefix import YouTube

def main():
    # Check if a URL was provided as a command-line argument
    if len(sys.argv) < 2:
        # Print error to stderr so it doesn't corrupt the stdout stream
        print("Error: Please provide a YouTube URL.", file=sys.stderr)
        print("Usage: python stream_audio.py <URL>", file=sys.stderr)
        sys.exit(1)
        
    url = sys.argv[1]
    
    try:
        # Fetch the video and get the audio stream
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if not audio_stream:
            print("Error: No audio stream found for this video.", file=sys.stderr)
            sys.exit(1)
            
        # Stream the bytes directly to standard output's binary buffer
        audio_stream.stream_to_buffer(sys.stdout.buffer)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
