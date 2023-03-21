
from pynput import mouse, keyboard

class 记录器:
    def __init__(self):
        self.正在记录 = False
        self.输入事件 = []

    def on_move(self, x, y):#on_move=self.on_move, 
        if self.正在记录:
            self.输入事件.append(('移动', x, y))

    def on_click(self, x, y, button, pressed):
        if self.正在记录:
            action = '按下' if pressed else '释放'
            self.输入事件.append(('点击', x, y, button, action))

    def on_scroll(self, x, y, dx, dy):
        if self.正在记录:
            self.输入事件.append(('滚动', x, y, dx, dy))

    def on_press(self, key):
        if self.正在记录:
            try:
                char = key.char
            except AttributeError:
                char = None
            self.输入事件.append(('按下', key, char))

    def on_release(self, key):
        if self.正在记录:
            try:
                char = key.char
            except AttributeError:
                char = None
            self.输入事件.append(('释放', key, char))

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f12:
                if not self.正在记录:
                    print("开始记录")
                    self.输入事件.clear()
                    self.正在记录 = True
                else:
                    print("停止记录")
                    print(self.输入事件)
                    self.正在记录 = False
        except AttributeError:
            pass

    def 开始(self):
        with mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll) as m_listener, keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as k_listener, keyboard.Listener(on_press=self.on_key_press) as f_listener:
            m_listener.join()
            k_listener.join()
            f_listener.join()

if __name__ == '__main__':
    记录器 = 记录器()
    记录器.开始()
