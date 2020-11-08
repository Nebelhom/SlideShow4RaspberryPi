#!/usr/bin/env python

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class RootWidget(BoxLayout):
    """
    Description
    """

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        self.current_touch = None

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print("Double Hello!")
        else:
            print("Single Hello!")

class TestApp(App):

    def build(self):
        root = RootWidget()
        return root


if __name__ == '__main__':
    TestApp().run()
