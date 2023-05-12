from kivymd.app import MDApp
from kivy.lang import Builder
import cv2
KV = '''
MDFloatLayout:
    Camera:
        id: camera
        resolution: (640, 640)
        play: True
    MDIconButton:
        icon: "camera"
        pos_hint: {"center_x": .50, "center_y": .05}
        md_bg_color: 0, 0, 0, 1
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        on_press: camera.export_to_png('selfie.png')
'''


class CameraClick(MDApp):
    def build(self):
        return Builder.load_string(KV)



CameraClick().run()
