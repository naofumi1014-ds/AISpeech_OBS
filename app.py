import asyncio
import websockets
from AISpeech import AISpeech

async def create_caption(websocket):
    ai_speech = AISpeech()
    
    # 音声認識を開始
    ai_speech.start_recognition()

    try:
        while True:
            # 認識されたテキストを取得
            # recognized_text = ai_speech.get_recognized_text()
            recognized_text = ai_speech.get_recognizing_text()

            # もし認識されたテキストがあれば、それを字幕として送信
            if recognized_text:
                await websocket.send(f"大沢：{recognized_text}")
            else:
                # テキストが認識されていない場合は、タイマーのようなものを送る
                await websocket.send(f"大沢：字幕テスト")

    except asyncio.CancelledError:
        # 音声認識を停止
        ai_speech.stop_recognition()
        print("音声認識を停止しました")

async def main():
    async with websockets.serve(create_caption, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
