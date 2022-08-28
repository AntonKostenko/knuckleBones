import math
import arcade

import constants as c


class Dice(arcade.Sprite):
    def __init__(self, value, scale=c.DICE_SCALE):
        self.value = value
        self.image_file_name = f'images/dice/Side_{self.value}_Pips.png'

        # Max speed
        self.speed = None

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")

    def move_sprite(self, position):
        # Only move if needed
        if self.position == position:
            return

        self.center_x += self.change_x
        self.center_y += self.change_y

        start_x = self.center_x
        start_y = self.center_y

        # Calculate the angle between the start points
        # and end points. This is the angle the dice will travel.
        x_diff = position[0] - start_x
        y_diff = position[1] - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the dice travels.
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        # If we are close, lock in the position so the dice does not vibrate
        if abs(self.center_x - position[0]) < abs(self.change_x):
            self.center_x = position[0]
            self.change_x = 0
        if abs(self.center_y - position[1]) < abs(self.change_y):
            self.center_y = position[1]
            self.change_y = 0
