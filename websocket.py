# obsに表示する字幕を生成する
from AISpeech import AISpeech
import time

ai_speech = AISpeech()
ai_speech.start_recognition()

try:
    while True:
        time.sleep(0.1)  # ループで実行を続ける（Ctrl+C で停止）
except KeyboardInterrupt:
    ai_speech.stop_recognition()