import cocos
from cocos import scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.scenes import *
from cocos.sprite import Sprite
from cocos.actions import *
from pyglet.window.key import symbol_string
import time

class InputLayer(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self, x=320, y=240, is_trippy=False):
        super(InputLayer, self).__init__(46, 204, 113, 1000)


        self.sprite = Sprite('assets/85857.png')
        self.sprite.position = x, y
        self.sprite.opacity = 0
        self.add(self.sprite)
        self.sprite.do(FadeIn(2))

        self.schedule_interval(self.movement, 0.1)
        self.left_move = False
        self.right_move = False


    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "LEFT":
            self.left_move = True

        elif symbol_string(key) == "RIGHT":
            self.right_move = True


        elif symbol_string(key) == "SPACE":
            coordinates = self.sprite.position

    """ move sprite in the appropriate direction as long as left/right key is held"""
    def movement(self, dt):

        move_left = MoveBy((-20, 0), .1)

        if self.left_move == True:
            self.sprite.do(move_left)

        elif self.right_move == True:
            self.sprite.do(Reverse(move_left)) 


    def on_key_release(self, key, modifiers):

        self.left_move = False
        self.right_move = False


director.init()
director.run(scene.Scene(InputLayer()))
