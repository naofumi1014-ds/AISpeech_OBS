import azure.cognitiveservices.speech as speechsdk
import time
from dotenv import load_dotenv
import os
import pyaudio

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
load_dotenv()  # .env ファイルを読み込む

p = pyaudio.PyAudio()

print("Available Audio Input Devices:")
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info["maxInputChannels"] > 0:  # 入力デバイスのみ表示
        print(f"Index {i}: {device_info['name']}")

p.terminate()

# Azureの音声認識設定
speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY"),
    region=os.environ.get("SPEECH_REGION"),
)
speech_config.speech_recognition_language = "ja-JP"
# Creates a recognizer with the given settings
audio_config = speechsdk.audio.AudioConfig(device_name="マイク配列 (デジタルマイク向けインテル® スマート・サウンド")
# audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,audio_config=audio_config)

print("Say something...")

def recognized(evt):
    print('「{}」'.format(evt.result.text))
    # do something

def start(evt):
    print('SESSION STARTED: {}'.format(evt))

def stop(evt):
    print('SESSION STOPPED {}'.format(evt))

speech_recognizer.recognized.connect(recognized)
speech_recognizer.session_started.connect(start)
speech_recognizer.session_stopped.connect(stop)

try:
    speech_recognizer.start_continuous_recognition()
    time.sleep(60)
except KeyboardInterrupt:
    print("bye.")
    speech_recognizer.recognized.disconnect_all()
    speech_recognizer.session_started.disconnect_all()
    speech_recognizer.session_stopped.disconnect_all()
