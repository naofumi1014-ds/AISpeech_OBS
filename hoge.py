import azure.cognitiveservices.speech as speechsdk
import time
from dotenv import load_dotenv
import os
import pyaudio

load_dotenv()  # .env ファイルを読み込む



def from_mic():
    # Azureの音声認識設定
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("SPEECH_KEY"),
        region=os.environ.get("SPEECH_REGION"),
    )
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)  # デフォルトマイク使用
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # 音声認識結果が出た時に呼ばれるコールバック関数
    def recognized(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(evt.result.text))
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
        elif evt.result.reason == speechsdk.ResultReason.Canceled:
            print("Speech recognition canceled: {}".format(evt.result.cancellation_details.reason))
            print("Error details: {}".format(evt.result.cancellation_details.error_details))

    # 認識したテキストをリアルタイムで表示するためにコールバックを接続
    speech_recognizer.recognized.connect(recognized)

    print("Speak into your microphone.")
    speech_recognizer.start_continuous_recognition()

    try:
        # 音声認識結果が出るたびにリアルタイムで処理を続ける
        input("Press Enter to stop...\n")
    except KeyboardInterrupt:
        print("Interrupted")

    # 認識を停止
    speech_recognizer.stop_continuous_recognition()

from_mic()
