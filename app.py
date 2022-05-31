from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, Property
from kivy.core.window import Window

from digitizer import Digitizer

IMAGE_PATH = 'ecg.jpg'
GRID_SIZE_PX = 8  # BETA
digitizer = Digitizer()
digitizer.load_by_path(IMAGE_PATH)


class Container(BoxLayout):
    image = StringProperty(defaultvalue=IMAGE_PATH)

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 13:  # Enter
            if self.touchscreen.point_a is not None and self.touchscreen.point_b is not None:
                if self.touchscreen.abs_point_a[0] < self.touchscreen.abs_point_b[0]:
                    x = round(self.touchscreen.abs_point_a[0])
                else:
                    x = round(self.touchscreen.abs_point_b[0])
                if self.touchscreen.abs_point_a[1] < self.touchscreen.abs_point_b[1]:
                    y = round(self.touchscreen.abs_point_a[1])
                else:
                    y = round(self.touchscreen.abs_point_b[1])
                w = round(abs(self.touchscreen.abs_point_a[0] - self.touchscreen.abs_point_b[0]))
                h = round(abs(self.touchscreen.abs_point_a[1] - self.touchscreen.abs_point_b[1]))
                digitizer4cropped = Digitizer()
                digitizer4cropped.load(digitizer.crop(x, y, w, h))
                *curve, grid = digitizer4cropped.find_curve(grid_size=GRID_SIZE_PX, show=True)


class TouchableImage(Image):
    container_size = Property(None)
    point_a = Property(None, allownone=True)
    point_b = Property(None, allownone=True)
    abs_point_a = Property(None, allownone=True)
    abs_point_b = Property(None, allownone=True)
    change_point = StringProperty('a')

    def on_touch_down(self, touch):
        scale = self.container_size[0] / digitizer.image_width
        if digitizer.image_height * scale > self.container_size[1]:
            scale = self.container_size[1] / digitizer.image_height
            abs_mouse_x = touch.pos[0] - self.container_size[0] / 2 + digitizer.image_width * scale / 2
            abs_mouse_y = touch.pos[1]
        else:
            abs_mouse_x = touch.pos[0]
            abs_mouse_y = touch.pos[1] - self.container_size[1] / 2 + digitizer.image_height * scale / 2

        if 0 <= abs_mouse_x < digitizer.image_width * scale and 0 <= abs_mouse_y < digitizer.image_height * scale:

            if self.change_point == 'a':
                self.point_a = touch.pos
                self.abs_point_a = abs_mouse_x / scale, abs_mouse_y / scale
                self.change_point = 'b'
            elif self.change_point == 'b':
                self.point_b = touch.pos
                self.abs_point_b = abs_mouse_x / scale, abs_mouse_y / scale
                self.change_point = 'a'

            if self.point_a is not None and self.point_b is not None:
                if self.point_a[0] < self.point_b[0]:
                    rec_x = self.point_a[0]
                else:
                    rec_x = self.point_b[0]
                if self.point_a[1] < self.point_b[1]:
                    rec_y = self.point_a[1]
                else:
                    rec_y = self.point_b[1]
                rec_w = abs(self.point_a[0] - self.point_b[0])
                rec_h = abs(self.point_a[1] - self.point_b[1])

                self.canvas.after.clear()
                with self.canvas.after:
                    Color(1, 0, 0, 0.25, mode='rgba')
                    Rectangle(pos=(rec_x, rec_y), size=(rec_w, rec_h))
        else:
            self.point_a = None
            self.point_b = None
            self.abs_point_a = None
            self.abs_point_b = None
            self.canvas.after.clear()


class DigitizerApp(App):

    def build(self):
        container = Container()
        return container


if __name__ == '__main__':
    DigitizerApp().run()
