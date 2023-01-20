import os
import argparse
import subprocess
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_args():
    parser = argparse.ArgumentParser(description='Extract audio from video and transcribe it')
    parser.add_argument('video_file', metavar='video_file', type=str, help='python vid2text.py path/to/video.mp4')
    parser.add_argument('-l', '--language', metavar='language', type=str, default='en-US', help='Language code for the audio. Default is en-US')
    return parser.parse_args()

def transcribe_audio(audio_file, language_code):
    credentials = service_account.Credentials.from_service_account_file('key.json')
    client = speech.SpeechClient(credentials=credentials)

    with open(audio_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code=language_code)

    response = client.recognize(config=config, audio=audio)
    if not response.results:
        return ""
    else:
        result = response.results[0].alternatives[0].transcript
        return result

def process_video(video_file, language_code):
    
    try:
        # Extract audio from video
        filename = os.path.splitext(video_file)[0]
        audio_file = 'audio.wav'
        subprocess.run(['ffmpeg', '-i', video_file, audio_file], check=True)

        mono_audio_file = 'mono_audio.wav'
        subprocess.run(['ffmpeg', '-i', audio_file, '-ac', '1', mono_audio_file], check=True)

        # Create chunks of audio
        subprocess.run(['ffmpeg', '-i', mono_audio_file, '-f', 'segment', '-segment_time', '50', '-c', 'copy', 'mono_audio_chunk_%03d.wav'], check=True)
      
        chunks = [f for f in os.listdir() if f.startswith('mono_audio_chunk_')]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(transcribe_audio, chunk, language_code) for chunk in chunks]
            transcripts = [future.result() for future in as_completed(futures)]

        # Write transcriptions to file
        transcript_file = filename + ".txt"
        with open(transcript_file, 'w') as file:
            file.write('\n'.join(transcripts))

    except subprocess.CalledProcessError as e:
        print(f"Error: ffmpeg command failed with exit code {e.returncode}")
    except Exception as e:
        print(e)
    finally:
        # Remove audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if os.path.exists(mono_audio_file):
            os.remove(mono_audio_file)
        # Remove audio chunks
        for chunk in chunks:
            os.remove(chunk)
        print(language_code)
        print("Finally ready!")

if __name__ == "__main__":
    args = get_args()
    process_video(args.video_file, args.language)
