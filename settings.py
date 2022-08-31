import arcade

from typing import List

import constants as c
import main_menu


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()

        self.menu_buttons = None

    def on_show_view(self):
        arcade.set_background_color(c.BACKGROUND_COLOR)

    def setup(self):
        self.menu_buttons: arcade.SpriteList = arcade.SpriteList()

        for i in range(len(c.SETTINGS_BUTTON_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.MENU_BUTTON_WIDTH, c.MENU_BUTTON_HEIGHT,
                                                            c.TILE_COLOR_LIST[i])
            button.position = c.SETTINGS_BUTTON_START + i * c.MENU_BUTTON_X_SPACING, c.SCREEN_HEIGHT / 3
            button.properties['name'] = c.SETTINGS_BUTTON_NAMES[i]
            self.menu_buttons.append(button)

    def on_draw(self):
        self.clear()

        for button in self.menu_buttons:
            button.draw()

        arcade.draw_text("Settings", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 0.75,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")

        for i in range(len(c.SETTINGS_BUTTON_NAMES)):
            arcade.draw_text(c.SETTINGS_BUTTON_NAMES[i],
                             self.menu_buttons[i].center_x, self.menu_buttons[i].center_y,
                             c.BACKGROUND_COLOR, font_size=20, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        tile_location: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.menu_buttons)
        if tile_location:
            if tile_location[0].properties['name'] == c.SETTINGS_BUTTON_NAMES[0]:
                main_menu_view = main_menu.MenuView()
                self.window.show_view(main_menu_view)
                main_menu_view.setup()
