import arcade

from typing import List

import constants as c
import game
import menu


class SettingsView(arcade.View):
    def __init__(self, color_scheme):
        super().__init__()

        self.color_scheme = color_scheme
        self.menu_buttons = None

    def on_show_view(self):
        arcade.set_background_color(self.color_scheme[4])

        self.menu_buttons: arcade.SpriteList = arcade.SpriteList()

        # Create the buttons in the page
        for i in range(len(c.INSTRUCTION_BUTTON_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.MENU_BUTTON_WIDTH, c.MENU_BUTTON_HEIGHT,
                                                            self.color_scheme[3])
            button.position = c.INSTRUCTION_BUTTON_START + i * c.MENU_BUTTON_X_SPACING, c.SCREEN_HEIGHT / 4
            button.properties['name'] = c.INSTRUCTION_BUTTON_NAMES[i]
            self.menu_buttons.append(button)

    def on_draw(self):
        self.clear()

        self.menu_buttons.draw()

        arcade.draw_text("Settings", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 0.75,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")

        for i in range(len(c.INSTRUCTION_BUTTON_NAMES)):
            arcade.draw_text(c.INSTRUCTION_BUTTON_NAMES[i],
                             self.menu_buttons[i].center_x, self.menu_buttons[i].center_y,
                             self.color_scheme[4], font_size=20, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        tile_location: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.menu_buttons)
        if tile_location:
            if tile_location[0].properties['name'] == c.INSTRUCTION_BUTTON_NAMES[0]:
                game_view = game.KnuckleBones(self.color_scheme)
                game_view.setup()
                self.window.show_view(game_view)
            elif tile_location[0].properties['name'] == c.SETTINGS_BUTTON_NAMES[0]:
                main_menu_view = menu.MenuView(self.color_scheme)
                self.window.show_view(main_menu_view)
