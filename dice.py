import arcade
import math
import random

from typing import Tuple

import constants as c


class Dice(arcade.Sprite):
    def __init__(self, value, scale=c.DICE_SCALE):
        self.value = value
        self.image_file_name = f'images/dice/Side_{self.value}_Pips.png'

        # Time before dice roll animation stops
        self.total_roll_time = 0.75

        # Max speed
        self.speed = None

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")

    def move_dice(self, destination_position: Tuple) -> None:
        """
        animates moving a die from its current position to the
        destination_position passed in
        """
        # Only move if needed
        if self.position == destination_position:
            return

        self.center_x += self.change_x
        self.center_y += self.change_y

        start_x: float = self.center_x
        start_y: float = self.center_y

        # Calculate the angle between the start points
        # and end points. This is the angle the dice will travel.
        x_diff: float = destination_position[0] - start_x
        y_diff: float = destination_position[1] - start_y
        angle: float = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the dice travels.
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        # If we are close, lock in the position so the dice does not vibrate
        if abs(self.center_x - destination_position[0]) < abs(self.change_x):
            self.center_x = destination_position[0]
            self.change_x = 0
        if abs(self.center_y - destination_position[1]) < abs(self.change_y):
            self.center_y = destination_position[1]
            self.change_y = 0

    def shrink_dice(self) -> bool:
        """
        Reduces the scale of a die and destroy it once it is small.
        Used to animate a die being attacked by the opposite player
        Returns True if a die was killed, so we can recalculate the score
        """
        self.color = c.ATTACKED_DICE_COLOR
        if self.scale < 0.2:
            self.kill()
            return True

        self.scale -= 0.05

    def roll_dice_animation(self, delta_time) -> None:
        """
        Dice roll animation.
        "Rolls" the current dice by randomly setting the self.center_x and self.center_y
        and loading different dice textures until the total_roll_time is 0
        """
        if self.total_roll_time <= 0:
            self.set_texture(0)
            return

        self.total_roll_time -= delta_time

        self.center_x += random.randint(-3, 3)
        self.center_y += random.randint(-3, 3)
        for x in range(6):
            self.append_texture(arcade.load_texture(f'images/dice/Side_{x + 1}_Pips.png'))

        if self.center_x % 2 == 0:
            self.set_texture(random.randint(0, 6))
