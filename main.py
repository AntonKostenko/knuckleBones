import arcade

import constants as c
import menu


def main():
    window: arcade.Window = arcade.Window(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)
    menu_view: menu.MenuView = menu.MenuView()
    menu_view.setup()
    window.show_view(menu_view)
    window.run()


if __name__ == '__main__':
    main()
