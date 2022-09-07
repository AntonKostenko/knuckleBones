import arcade

from typing import List

import constants as c
from dice import Dice
import game
import menu


class InstructionView(arcade.View):
    def __init__(self, color_scheme):
        super().__init__()
        self.color_scheme = color_scheme
        self.menu_buttons = None

        self.dice_mats = None

        self.match_dice = None
        self.destroy_dice = None

    def on_show_view(self):
        arcade.set_background_color(self.color_scheme[4])

        self.menu_buttons: arcade.SpriteList = arcade.SpriteList()

        self.dice_mats: arcade.SpriteList = arcade.SpriteList()

        self.match_dice: arcade.SpriteList = arcade.SpriteList()
        self.destroy_dice: arcade.SpriteList = arcade.SpriteList()

        # Create some "mats" under the dice
        left_mat: arcade.Sprite = arcade.SpriteSolidColor(120, 120, self.color_scheme[2])
        left_mat.position = c.INSTRUCTIONS_LEFT_MAT_X, c.INSTRUCTION_MAT_Y
        self.dice_mats.append(left_mat)

        right_mat: arcade.Sprite = arcade.SpriteSolidColor(120, 120, self.color_scheme[2])
        right_mat.position = c.INSTRUCTIONS_RIGHT_MAT_X, c.INSTRUCTION_MAT_Y
        self.dice_mats.append(right_mat)

        # Create the dice used in the "multiply" rule
        mult_dice_one: Dice = Dice(6)
        mult_dice_one.position = c.INSTRUCTIONS_LEFT_MAT_X - c.DICE_DIMENSIONS / 2,\
            c.INSTRUCTION_MAT_Y + c.DICE_DIMENSIONS / 2
        mult_dice_one.color = self.color_scheme[1]
        self.match_dice.append(mult_dice_one)

        mult_dice_two: Dice = Dice(6)
        mult_dice_two.position = c.INSTRUCTIONS_LEFT_MAT_X + c.DICE_DIMENSIONS / 2, \
            c.INSTRUCTION_MAT_Y - c.DICE_DIMENSIONS / 2
        mult_dice_two.color = self.color_scheme[1]
        self.match_dice.append(mult_dice_two)

        # Create the dice used in the "destroy" rule
        destroy_dice_one: Dice = Dice(4)
        destroy_dice_one.position = c.INSTRUCTIONS_RIGHT_MAT_X, c.INSTRUCTION_MAT_Y + c.DICE_DIMENSIONS * 0.75
        destroy_dice_one.color = c.ATTACKED_DICE_COLOR
        self.destroy_dice.append(destroy_dice_one)

        destroy_dice_one: Dice = Dice(4)
        destroy_dice_one.position = c.INSTRUCTIONS_RIGHT_MAT_X, c.INSTRUCTION_MAT_Y - c.DICE_DIMENSIONS * 0.75
        self.destroy_dice.append(destroy_dice_one)

        # Create the buttons in the page
        for i in range(len(c.INSTRUCTION_BUTTON_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.MENU_BUTTON_WIDTH, c.MENU_BUTTON_HEIGHT,
                                                            self.color_scheme[3])
            button.position = c.INSTRUCTION_BUTTON_START + i * c.MENU_BUTTON_X_SPACING, c.SCREEN_HEIGHT / 4
            button.properties['name'] = c.INSTRUCTION_BUTTON_NAMES[i]
            self.menu_buttons.append(button)

    def on_draw(self):
        self.clear()

        # Draw the title and subtitle texts
        arcade.draw_text('How To Play', c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 0.9,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")
        arcade.draw_text(c.INSTRUCTIONS_SUB_TEXT, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 0.9 - 80,
                         arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

        # Draw the mats
        self.dice_mats.draw()

        arcade.draw_line(c.INSTRUCTIONS_RIGHT_MAT_X - 50, c.INSTRUCTION_MAT_Y,
                         c.INSTRUCTIONS_RIGHT_MAT_X + 50, c.INSTRUCTION_MAT_Y, self.color_scheme[4], 4)

        # Draw the dice
        self.match_dice.draw()
        self.destroy_dice.draw()

        # Draw the "Match Dice" text
        arcade.draw_text('Match Dice', c.INSTRUCTIONS_LEFT_MAT_X, c.INSTRUCTION_MAT_Y - 100,
                         arcade.color.WHITE, font_size=22, anchor_x="center", anchor_y="center")
        arcade.draw_text(c.MATCH_DICE_RULE_TEXT, c.INSTRUCTIONS_LEFT_MAT_X, c.INSTRUCTION_MAT_Y - 150, font_size=12,
                         anchor_x="center", anchor_y="center", multiline=True, width=290, align='center')

        # Draw the "Destroy Dice" text
        arcade.draw_text('Destroy Opponent', c.INSTRUCTIONS_RIGHT_MAT_X, c.INSTRUCTION_MAT_Y - 100,
                         arcade.color.WHITE, font_size=22, anchor_x="center", anchor_y="center")
        arcade.draw_text(c.DESTROY_OPPONENT_RULE_TEXT, c.INSTRUCTIONS_RIGHT_MAT_X, c.INSTRUCTION_MAT_Y - 150,
                         font_size=12, anchor_x="center", anchor_y="center", multiline=True, width=290, align='center')

        # Draw the menu buttons and their text
        self.menu_buttons.draw()

        for i in range(len(c.INSTRUCTION_BUTTON_NAMES)):
            arcade.draw_text(c.INSTRUCTION_BUTTON_NAMES[i],
                             self.menu_buttons[i].center_x, self.menu_buttons[i].center_y,
                             self.color_scheme[4], font_size=20, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # Navigate to the proper view when selecting a menu button
        tile_location: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.menu_buttons)
        if tile_location:
            if tile_location[0].properties['name'] == c.INSTRUCTION_BUTTON_NAMES[0]:
                game_view = game.KnuckleBones(self.color_scheme)
                game_view.setup()
                self.window.show_view(game_view)
            elif tile_location[0].properties['name'] == c.INSTRUCTION_BUTTON_NAMES[1]:
                main_menu_view = menu.MenuView(self.color_scheme)
                self.window.show_view(main_menu_view)
