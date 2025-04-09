import asyncio
import websockets
from AISpeech import AISpeech

class SpeechWebSocketServer:
    def __init__(self):
        self.ai_speech = AISpeech()
        self.latest_recognizing_text = ""  # 認識中のテキスト
        self.latest_recognized_text = ""   # 確定したテキスト

    async def create_caption(self, websocket):
        self.ai_speech.start_recognition()

        try:
            while True:
                recognizing_text = self.ai_speech.get_recognizing_text()
                recognized_text = self.ai_speech.get_recognized_text()

                # 認識中のテキストが更新されたら送信
                if recognizing_text and recognizing_text != self.latest_recognizing_text:
                    self.latest_recognizing_text = recognizing_text
                    await websocket.send(f"大沢：{recognizing_text}")  # 認識中メッセージ

                # 確定したテキストが更新されたら送信（認識中の表示を置き換える）
                if recognized_text and recognized_text != self.latest_recognized_text:
                    self.latest_recognized_text = recognized_text
                    await websocket.send(f"大沢：{recognized_text}")  # 確定メッセージ

                await asyncio.sleep(0.1)  # 負荷を抑えるためのスリープ

        except asyncio.CancelledError:
            self.ai_speech.stop_recognition()
            print("音声認識を停止しました")

async def main():
    server = SpeechWebSocketServer()
    async with websockets.serve(server.create_caption, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
