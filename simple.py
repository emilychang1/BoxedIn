# Alright!
# It's time for us to string everything we learned in the basics tutorial together

# Let's start with all of the inputs we need
import cocos
from cocos import scene
from cocos.layer import Layer, ColorLayer
from cocos.director import director
from cocos.scenes import *
from cocos.sprite import Sprite
from cocos.actions import *
from pyglet.window.key import symbol_string




# Let's be fancy and make this a color layer AND an event handler
class InputLayer(cocos.layer.ColorLayer):
    is_event_handler = True
    key_held = False

    def __init__(self, x=320, y=240, is_trippy=False):
        super(InputLayer, self).__init__(46, 204, 113, 1000)


        # Now we need a little guy to manipulate
        self.sprite = Sprite('assets/85857.png')
        self.sprite.position = x, y
        self.sprite.opacity = 0
        self.add(self.sprite)
        self.sprite.do(FadeIn(2))

        # You should be bored seeing this same code over and over again
        # Here's something different though
        # Now I create an audio object and store it within self, based on whether or not it's trippy
  


        # We don't need anything else here, let's just let our sprite be moved in the event handlers

    # So now we can overload some default event handlers
    # We'll let the user move in any direction on the screen with the arrow keys
    # We'll only be doing keyboard input for this program
    def on_key_press(self, key, modifiers):
        # If you don't know what these next couple lines do, go check the previous tutorials
        move_left = MoveBy((-50, 0), .5)
        move_up = MoveBy((0, 50), .5)

    
        if symbol_string(key) == "LEFT":
            self.sprite.do(move_left)


        # Or maybe if they want to move right?
        elif symbol_string(key) == "RIGHT":
            self.sprite.do(Reverse(move_left)) 

        # That's it for movements!
        # Now let's look at transitioning to a new scene
        # Let's make the game all trippy when they hit space
        elif symbol_string(key) == "SPACE":
            # I need to stop the music before we transition to the next scene so that two songs aren't playing at once
            # self.bg_music.stop()

            # If you were paying attention, you would've noticed I take three parameters in the init function
            # I get the X and Y coordinates of the sprite to figure out where to place it when the scenes transition
            coordinates = self.sprite.position
            # You should try printing the X and Y coordinates yourself to see the type of object that it returns

        key_held = True

        self.schedule_interval(self.movement, key)

        print("why")

    def movement(self, key):

        print("ok")
        while (key_held == True):
            print("hey")
            move_left = MoveBy((-50, 0), .5)
            move_up = MoveBy((0, 50), .5)
            # Check if they want to go left, and then actually make the sprite go left
            if symbol_string(key) == "LEFT":
                self.sprite.do(move_left)

            # Or maybe if they want to move right?
            elif symbol_string(key) == "RIGHT":
                self.sprite.do(Reverse(move_left)) 




    def on_key_release(self, key, modifiers):

        key_held = False


        

# And finally we do our usual initialization and run the scene
# mixer.init()
director.init()
director.run(scene.Scene(InputLayer()))
