import tornado.websocket
import json
import config as conf
import time


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        try:
            # data = json.loads(message)
            time.sleep(3)
            print(message)
            self.write_message(message)
        except json.decoder.JSONDecodeError as e:
            self.write_message('参数有误！')
        finally:
            pass    
    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True        