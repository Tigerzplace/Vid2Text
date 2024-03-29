# Vid2Text

Vid2Text is a tool to extract audio from videos and transcribe it into text using Google Cloud Speech-To-Text API.

## Requirements

- ffmpeg
- Google Cloud Speech-To-Text API service account credentials

## Installation

Clone this repository:

```
git clone https://github.com/Tigerzplace/Vid2Text.git
```

Install ffmpeg and create a service account in Google Cloud Speech-To-Text.

To install ffmpeg, follow the instructions given [here](https://www.wikihow.com/Install-FFmpeg-on-Windows).

To create service account credentials, follow the instructions given [here](https://cloud.google.com/speech-to-text/docs/before-you-begin). If you want to follow up a video tutorial, you can get the whole method [here]: (https://youtu.be/DtlJH6MgBso?t=94).  Download the JSON file and save it in the same directory as `key.json`.

## Usage

To transcribe the audio from a video, run the following command:

```
python vid2text.py <video-file>
```

This will create a text file with the same name as the video file in the same directory. The default language code for the audio is `en-US`.

To specify a language code for the audio, use the `-l` or `--language` flag:

```
python vid2text.py <video-file> -l <language-code>
```

The language code should be a [supported language code](https://cloud.google.com/speech-to-text/docs/languages) for the Google Cloud Speech-To-Text API.


If you don't want to use the Google Cloud Speech-To-Text API, you can use the [VTT-Snap](https://github.com/Tigerzplace/VTT-Snap) tool which is using offline method but not as accurate as the Google Cloud Speech-To-Text API.

## Credits

[Ñasir Ali](https://fb.com/tiger6117).
 [Tigerzplace](https://tigerzplace.com).

