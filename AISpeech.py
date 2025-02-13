import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import pyaudio

class AISpeech:
    def __init__(self):
        load_dotenv()  # .env ファイルを読み込む

        # Azureの音声認識設定
        speech_config = speechsdk.SpeechConfig(
            subscription=os.environ.get("SPEECH_KEY"),
            region=os.environ.get("SPEECH_REGION"),
        )
        speech_config.speech_recognition_language = "ja-JP"

        p = pyaudio.PyAudio()

        print("Available Audio Input Devices:")
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:  # 入力デバイスのみ表示
                print(f"Index {i}: {device_info['name']}")

        p.terminate()

        # マイク入力の設定
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        print(audio_config)

        # 音声認識インスタンスを作成
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )

        # コールバック関数を登録
        self.speech_recognizer.recognizing.connect(self.recognizing_callback)
        self.speech_recognizer.recognized.connect(self.recognized_callback)

    def recognizing_callback(self, evt):
        """
        途中の音声認識結果をリアルタイムで取得（未確定のテキスト）
        """
        print(f"Recognizing: {evt.result.text}")

    def recognized_callback(self, evt):
        """
        確定した音声認識結果を取得（確定後のテキスト）
        """
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Recognized: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")

    def start_recognition(self):
        """
        音声認識を開始し、リアルタイムで結果を出力
        """
        print("音声認識を開始します（終了するには Ctrl+C を押してください）")
        self.speech_recognizer.start_continuous_recognition()

    def stop_recognition(self):
        """
        音声認識を停止
        """
        print("音声認識を停止します")
        self.speech_recognizer.stop_continuous_recognition()
