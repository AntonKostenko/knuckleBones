import arcade

from typing import List

import constants as c
from dice import Dice
import game
import instructions
import settings


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.menu_dice = None
        self.menu_buttons = None

    def on_show_view(self):
        arcade.set_background_color(c.BACKGROUND_COLOR)

        self.menu_dice: arcade.SpriteList = arcade.SpriteList()
        self.menu_buttons: arcade.SpriteList = arcade.SpriteList()

        for i in range(3):
            dice: Dice = Dice(6, scale=0.4)
            dice.position = c.SCREEN_WIDTH / 2 - dice.width + dice.width * i, c.SCREEN_HEIGHT * 0.66 + 70
            self.menu_dice.append(dice)

        for i in range(3):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.MENU_BUTTON_WIDTH, c.MENU_BUTTON_HEIGHT,
                                                            c.TILE_COLOR_LIST[i])
            button.position = c.MENU_BUTTON_START + i * c.MENU_BUTTON_X_SPACING, c.SCREEN_HEIGHT / 3
            button.properties['name'] = c.MENU_BUTTON_NAMES[i]
            self.menu_buttons.append(button)

    def on_draw(self):
        self.clear()

        for dice in self.menu_dice:
            dice.draw()

        for button in self.menu_buttons:
            button.draw()

        arcade.draw_text("KNUCKLEBONES", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 0.66,
                         arcade.color.WHITE, font_size=80, anchor_x="center", anchor_y="center")
        arcade.draw_text(c.MENU_SUB_TEXT, c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 0.66 - 100,
                         arcade.color.WHITE, font_size=30, anchor_x="center", anchor_y="center")

        for i in range(len(c.MENU_BUTTON_NAMES)):
            arcade.draw_text(c.MENU_BUTTON_NAMES[i], self.menu_buttons[i].center_x, self.menu_buttons[i].center_y,
                             c.BACKGROUND_COLOR, font_size=20, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        tile_location: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.menu_buttons)
        if tile_location:
            if tile_location[0].properties['name'] == c.MENU_BUTTON_NAMES[0]:
                game_view = game.KnuckleBones()
                self.window.show_view(game_view)
                game_view.setup()
            elif tile_location[0].properties['name'] == c.MENU_BUTTON_NAMES[1]:
                instructions_view = instructions.InstructionView()
                self.window.show_view(instructions_view)
            elif tile_location[0].properties['name'] == c.MENU_BUTTON_NAMES[2]:
                settings_view = settings.SettingsView()
                self.window.show_view(settings_view)
