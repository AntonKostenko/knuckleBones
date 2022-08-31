import arcade

from typing import List

import constants as c
from dice import Dice
import game
import main_menu


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()

        self.menu_buttons = None

        self.dice_mats = None

        self.match_dice = None
        self.destroy_dice = None

    def on_show_view(self):
        arcade.set_background_color(c.BACKGROUND_COLOR)

    def setup(self):
        self.menu_buttons: arcade.SpriteList = arcade.SpriteList()

        self.dice_mats: arcade.SpriteList = arcade.SpriteList()

        self.match_dice: arcade.SpriteList = arcade.SpriteList()
        self.destroy_dice: arcade.SpriteList = arcade.SpriteList()

        # Create some "mats" under the dice

        left_mat: arcade.Sprite = arcade.SpriteSolidColor(130, 130, c.TILE_COLOR)
        left_mat.position = c.MATCH_DICE_X_START + c.DICE_DIMENSIONS / 2 + c.DICE_DIMENSIONS * 0.1 , c.INSTRUCTION_DICE_Y_START - c.DICE_DIMENSIONS * 0.75
        self.dice_mats.append(left_mat)

        right_mat = arcade.Sprite = arcade.SpriteSolidColor(130, 130, c.TILE_COLOR)
        right_mat.position = c.DESTROY_DICE_X_START, c.INSTRUCTION_DICE_Y_START - c.DICE_DIMENSIONS * 0.75
        self.dice_mats.append(right_mat)


        # Create the dice used in the "multiply" rule
        for i in range(2):
            dice: Dice = Dice(6)
            dice.position = c.MATCH_DICE_X_START + (c.DICE_DIMENSIONS + c.DICE_DIMENSIONS * 0.1) * i,\
                            c.INSTRUCTION_DICE_Y_START - (c.DICE_DIMENSIONS + c.DICE_DIMENSIONS * 0.1) * i
            dice.color = c.TWO_X_MOD_COLOR
            self.match_dice.append(dice)

        # Create the dice used in the "destroy" rule
        for i in range(2):
            dice: Dice = Dice(6)
            dice.position = c.DESTROY_DICE_X_START, c.INSTRUCTION_DICE_Y_START - (c.DICE_DIMENSIONS +
                        c.DICE_DIMENSIONS * 0.5) * i
            dice.color = c.ATTACKED_DICE_COLOR
            self.destroy_dice.append(dice)

        # Create the buttons in the page
        for i in range(len(c.INSTRUCTION_BUTTON_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.MENU_BUTTON_WIDTH, c.MENU_BUTTON_HEIGHT,
                                                            c.TILE_COLOR_LIST[i])
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
        for mat in self.dice_mats:
            mat.draw()

        # Draw the dice
        for dice in self.match_dice:
            dice.draw()
        for dice in self.destroy_dice:
            dice.draw()

        # Draw the "Match Dice" text
        arcade.draw_text('Match Dice', c.MATCH_DICE_X_START + c.DICE_DIMENSIONS / 2,
                         c.INSTRUCTION_DICE_Y_START - c.DICE_DIMENSIONS * 2.2,
                         arcade.color.WHITE, font_size=22, anchor_x="center", anchor_y="center")
        arcade.draw_text(c.MATCH_DICE_RULE_TEXT, c.MATCH_DICE_X_START + c.DICE_DIMENSIONS / 2,
                         c.INSTRUCTION_DICE_Y_START - c.DICE_DIMENSIONS * 2.2 - 50, font_size=12,
                         anchor_x="center", anchor_y="center", multiline=True, width=290, align='center')

        # Draw the "Destroy Dice" text
        arcade.draw_text('Destroy Opponent', c.DESTROY_DICE_X_START,
                         c.INSTRUCTION_DICE_Y_START - c.DICE_DIMENSIONS * 2.2,
                         arcade.color.WHITE, font_size=22, anchor_x="center", anchor_y="center")
        arcade.draw_text(c.DESTROY_OPPONENT_RULE_TEXT, c.DESTROY_DICE_X_START,
                         c.INSTRUCTION_DICE_Y_START - c.DICE_DIMENSIONS * 2.2 - 50, font_size=12,
                         anchor_x="center", anchor_y="center", multiline=True, width=290, align='center')

        # Draw the menu buttons and their text
        for button in self.menu_buttons:
            button.draw()
        for i in range(len(c.INSTRUCTION_BUTTON_NAMES)):
            arcade.draw_text(c.INSTRUCTION_BUTTON_NAMES[i],
                             self.menu_buttons[i].center_x, self.menu_buttons[i].center_y,
                             c.BACKGROUND_COLOR, font_size=20, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # Navigate to the proper view when selecting a menu button
        tile_location: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.menu_buttons)
        if tile_location:
            if tile_location[0].properties['name'] == c.INSTRUCTION_BUTTON_NAMES[0]:
                game_view = game.KnuckleBones()
                self.window.show_view(game_view)
                game_view.setup()
            elif tile_location[0].properties['name'] == c.INSTRUCTION_BUTTON_NAMES[1]:
                main_menu_view = main_menu.MenuView()
                self.window.show_view(main_menu_view)
                main_menu_view.setup()
