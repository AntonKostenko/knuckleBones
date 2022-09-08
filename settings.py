import arcade

from typing import List

import constants as c
import game
import menu


def update_mode_colors(mode_sprite_list, mode_sprite_list_selected, player_mode):
    for index, button in enumerate(mode_sprite_list):
        if button.properties['name'] == player_mode:
            button.visible = False
            mode_sprite_list_selected[index].visible = True
        else:
            button.visible = True
            mode_sprite_list_selected[index].visible = False


class SettingsView(arcade.View):
    def __init__(self, color_scheme, p1_mode, p2_mode):
        super().__init__()

        self.color_scheme = color_scheme
        # Flags for setting AI difficulty
        self.p1_mode = p1_mode
        self.p2_mode = p2_mode

        self.menu_buttons = None

        self.p1_mode_buttons = None
        self.p2_mode_buttons = None
        self.p1_mode_buttons_selected = None
        self.p2_mode_buttons_selected = None

        self.p1_pressed = None

    def on_show_view(self):
        arcade.set_background_color(self.color_scheme[4])

        self.menu_buttons: arcade.SpriteList = arcade.SpriteList()

        self.p1_mode_buttons: arcade.SpriteList = arcade.SpriteList()
        self.p2_mode_buttons: arcade.SpriteList = arcade.SpriteList()
        self.p1_mode_buttons_selected: arcade.SpriteList = arcade.SpriteList()
        self.p2_mode_buttons_selected: arcade.SpriteList = arcade.SpriteList()

        # Create the meu buttons in the page
        for i in range(len(c.INSTRUCTION_BUTTON_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.MENU_BUTTON_WIDTH, c.MENU_BUTTON_HEIGHT,
                                                            self.color_scheme[3])
            button.position = c.INSTRUCTION_BUTTON_START + i * c.MENU_BUTTON_X_SPACING, c.SCREEN_HEIGHT / 4
            button.properties['name'] = c.INSTRUCTION_BUTTON_NAMES[i]
            self.menu_buttons.append(button)

        # Create play mode buttons
        for i in range(len(c.SETTINGS_MODE_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.TILE_DIMENSIONS, c.TILE_DIMENSIONS // 2,
                                                            self.color_scheme[3])
            button.position = c.INSTRUCTION_BUTTON_START + i * c.TILE_X_SPACING, c.SCREEN_HEIGHT * 0.7
            button.properties['name'] = c.SETTINGS_MODE_NAMES[i]
            self.p1_mode_buttons.append(button)
        for i in range(len(c.SETTINGS_MODE_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.TILE_DIMENSIONS, c.TILE_DIMENSIONS // 2,
                                                            self.color_scheme[3])
            button.position = c.INSTRUCTION_BUTTON_START + i * c.TILE_X_SPACING,\
                c.SCREEN_HEIGHT * 0.7 - c.TILE_DIMENSIONS * 0.6
            button.properties['name'] = c.SETTINGS_MODE_NAMES[i]
            self.p2_mode_buttons.append(button)

        for i in range(len(c.SETTINGS_MODE_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.TILE_DIMENSIONS, c.TILE_DIMENSIONS // 2,
                                                            self.color_scheme[1])
            button.position = c.INSTRUCTION_BUTTON_START + i * c.TILE_X_SPACING, c.SCREEN_HEIGHT * 0.7
            button.properties['name'] = c.SETTINGS_MODE_NAMES[i]
            button.visible = False
            self.p1_mode_buttons_selected.append(button)
        for i in range(len(c.SETTINGS_MODE_NAMES)):
            button: arcade.Sprite = arcade.SpriteSolidColor(c.TILE_DIMENSIONS, c.TILE_DIMENSIONS // 2,
                                                            self.color_scheme[1])
            button.position = c.INSTRUCTION_BUTTON_START + i * c.TILE_X_SPACING,\
                c.SCREEN_HEIGHT * 0.7 - c.TILE_DIMENSIONS * 0.6
            button.properties['name'] = c.SETTINGS_MODE_NAMES[i]
            button.visible = False
            self.p2_mode_buttons_selected.append(button)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Settings", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT * 0.85,
                         arcade.color.WHITE, font_size=50, anchor_x="center", anchor_y="center")

        self.menu_buttons.draw()

        for i in range(len(c.INSTRUCTION_BUTTON_NAMES)):
            arcade.draw_text(c.INSTRUCTION_BUTTON_NAMES[i],
                             self.menu_buttons[i].center_x, self.menu_buttons[i].center_y,
                             self.color_scheme[4], font_size=20, anchor_x="center", anchor_y="center")

        self.p1_mode_buttons.draw()
        self.p2_mode_buttons.draw()
        self.p1_mode_buttons_selected.draw()
        self.p2_mode_buttons_selected.draw()

        arcade.draw_text(c.PLAYER_ONE, self.p1_mode_buttons[0].center_x - 100, self.p1_mode_buttons[0].center_y,
                             arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")
        arcade.draw_text(c.PLAYER_TWO, self.p2_mode_buttons[0].center_x - 100, self.p2_mode_buttons[0].center_y,
                         arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

        for i in range(len(c.SETTINGS_MODE_NAMES)):
            arcade.draw_text(c.SETTINGS_MODE_NAMES[i],
                             self.p1_mode_buttons[i].center_x, self.p1_mode_buttons[i].center_y,
                             self.color_scheme[4], font_size=17, anchor_x="center", anchor_y="center")

        for i in range(len(c.SETTINGS_MODE_NAMES)):
            arcade.draw_text(c.SETTINGS_MODE_NAMES[i],
                             self.p2_mode_buttons[i].center_x, self.p2_mode_buttons[i].center_y,
                             self.color_scheme[4], font_size=17, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time: float):
        update_mode_colors(self.p1_mode_buttons, self.p1_mode_buttons_selected, self.p1_mode)
        update_mode_colors(self.p2_mode_buttons, self.p2_mode_buttons_selected, self.p2_mode)

    def on_mouse_press(self, x, y, button, modifiers):
        tile_location: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.menu_buttons)
        p1_pressed: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.p1_mode_buttons)
        p2_pressed: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.p2_mode_buttons)
        if tile_location:
            if tile_location[0].properties['name'] == c.INSTRUCTION_BUTTON_NAMES[0]:
                game_view = game.KnuckleBones(self.color_scheme, self.p1_mode, self.p2_mode)
                game_view.setup()
                self.window.show_view(game_view)
            elif tile_location[0].properties['name'] == c.SETTINGS_BUTTON_NAMES[0]:
                main_menu_view = menu.MenuView(self.color_scheme, self.p1_mode, self.p2_mode)
                self.window.show_view(main_menu_view)
        if p1_pressed:
            self.p1_mode = p1_pressed[0].properties['name']
        elif p2_pressed:
            self.p2_mode = p2_pressed[0].properties['name']
