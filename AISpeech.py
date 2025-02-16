import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import threading

class AISpeech:
    def __init__(self):
        load_dotenv()  # .env ファイルを読み込む

        # Azureの音声認識設定
        speech_config = speechsdk.SpeechConfig(
            subscription=os.environ.get("SPEECH_KEY"),
            region=os.environ.get("SPEECH_REGION"),
        )

        # 言語を設定
        speech_config.speech_recognition_language = "ja-JP"

        # 音声認識インスタンスを作成
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config
        )

        # 結果を格納するための変数
        self.recognized_text = ""
        self.recognizing_text = ""

        # コールバック関数を登録
        self.speech_recognizer.recognized.connect(self.recognized_callback)
        self.speech_recognizer.recognizing.connect(self.recognizing_callback)
        

        # 音声認識が終了した際に呼ばれるコールバック
        self.speech_recognizer.canceled.connect(self.canceled_callback)

    def recognizing_callback(self,evt):
        """
        継続中の音声認識結果を取得(確定前のテキスト)
        """
        if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            self.recognizing_text = evt.result.text
            print(f"Recognizing: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")           

    def recognized_callback(self, evt):
        """
        確定した音声認識結果を取得（確定後のテキスト）
        """
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            self.recognized_text = evt.result.text
            print(f"Recognized: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")

    def canceled_callback(self, evt):
        """
        音声認識がキャンセルされたときの処理
        """
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Speech Recognition canceled: {evt.error_details}")
    
    def start_recognition(self):
        """
        音声認識を開始
        """
        print("音声認識を開始します（終了するには Ctrl+C を押してください）")
        self.speech_recognizer.start_continuous_recognition()

    def stop_recognition(self):
        """
        音声認識を停止
        """
        print("音声認識を停止します")
        self.speech_recognizer.stop_continuous_recognition()

    def get_recognized_text(self):
        """
        外部から認識されたテキストを取得
        """
        return self.recognized_text
    
    def get_recognizing_text(self):
        """
        外部から認識中のテキストを取得
        """
        return self.recognizing_text   
