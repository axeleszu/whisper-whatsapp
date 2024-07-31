from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse
import whisper
import os
import requests

app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("base")

@app.route('/voice', methods=['POST'])
def voice():
    response = VoiceResponse()
    response.record(
        transcribe_callback='/transcribe',
        max_length=60
    )
    return str(response)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    recording_url = request.form['RecordingUrl']
    # Download the audio file from Twilio
    audio_file = download_audio(recording_url)
    # Transcribe the audio file using Whisper
    transcription = transcribe_audio_with_whisper(audio_file)
    return jsonify({'transcription': transcription})

def download_audio(url):
    audio_content = requests.get(url).content
    audio_file_path = 'recording.wav'
    with open(audio_file_path, 'wb') as f:
        f.write(audio_content)
    return audio_file_path

def transcribe_audio_with_whisper(file_path):
    result = model.transcribe(file_path)
    return result['text']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
