import os
import numpy as np
import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv


def continuous_recognition_streaming_with_overwrite():
    load_dotenv()  # これにより .env ファイルが読み込まれます
    texts = []

    # 環境変数からキーとリージョンを取得
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("SPEECH_KEY"),
        region=os.environ.get("SPEECH_REGION"),
    )
    # 認識言語の設定 (日本語)
    speech_config.speech_recognition_language = "ja-JP"

    # デフォルトマイクから音声を取得するための AudioConfig
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # SpeechRecognizer のインスタンスを作成
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # 前回の partial 結果を保持しておく（表示上書き用）
    last_partial_text = ""

    # ========================================================================
    #                  イベントハンドラ(コールバック)の設定
    # ========================================================================

    # 1) 認識途中の結果(Partial result)が得られるたびに呼び出される
    def recognizing_callback(evt: speechsdk.SpeechRecognitionEventArgs):
        """
        evt.result.reason == speechsdk.ResultReason.RecognizingSpeech の場合に、
        evt.result.text に途中認識のテキストが入ります。
        """
        nonlocal last_partial_text

        if evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            partial_text = evt.result.text

            # 前回のpartial_textの長さを取得（上書き用のスペースに利用）
            max_len = max(len(partial_text), len(last_partial_text))

            # 行頭に戻る前に、行を一度スペースでクリアしておく
            # （前回のpartial_textのほうが長かった場合に残りが表示されないようにするため）
            print(" " * max_len, end="\r", flush=True)

            # 新しい partial_text を同じ行で出力
            print(f"Partial: {partial_text}", end="\r", flush=True)

            # 次回比較のために最新の partial_text を保持
            last_partial_text = partial_text
            return partial_text

    # 2) 認識が確定した結果(Final result)が得られたときに呼び出される
    def recognized_callback(evt: speechsdk.SpeechRecognitionEventArgs):
        """
        evt.result.reason == speechsdk.ResultReason.RecognizedSpeech の場合に、
        evt.result.text に最終確定した認識結果が入ります。
        """
        nonlocal last_partial_text

        result = evt.result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # 最終結果が確定したので、partial表示を消してから改行して確定結果を出力
            max_len = max(len(result.text), len(last_partial_text))
            print(" " * max_len, end="\r", flush=True)
            print(f"Recognized: {result.text}")
            texts.append(result.text)

            # partial 表示をクリア
            last_partial_text = ""
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("\nNo speech could be recognized.")

    # 3) エラーやキャンセルが発生した場合に呼び出される
    def canceled_callback(evt: speechsdk.SpeechRecognitionCanceledEventArgs):
        print(f"\nSpeech Recognition canceled: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {evt.error_details}")
            print("Did you set the speech resource key and region values?")

    # 4) セッションが停止した（終了した）ときに呼び出される
    def session_stopped_callback(evt: speechsdk.SessionEventArgs):
        print("\nSession stopped: {}".format(evt))

    # ========================================================================
    #              上記コールバックを、それぞれのイベントに紐付ける
    # ========================================================================
    # 認識途中の結果 (partial)
    speech_recognizer.recognizing.connect(recognizing_callback)
    # 認識が確定した結果 (final)
    speech_recognizer.recognized.connect(recognized_callback)
    # キャンセル(エラー)イベント
    speech_recognizer.canceled.connect(canceled_callback)
    # セッション停止イベント
    speech_recognizer.session_stopped.connect(session_stopped_callback)

    # 連続認識を開始
    print("ストリーミング形式の連続認識を開始します。Ctrl+C で終了します。")
    speech_recognizer.start_continuous_recognition_async().get()

    try:
        # 連続認識中はメインスレッドが終了しないようにループで待機
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nCtrl+C が押されました。連続認識を停止します。")

    # 連続認識を停止
    speech_recognizer.stop_continuous_recognition_async().get()
    print("連続認識を停止しました。")
    for text in texts:
        print(text)
    np.save("./data/texts", texts)


if __name__ == "__main__":
    continuous_recognition_streaming_with_overwrite()
