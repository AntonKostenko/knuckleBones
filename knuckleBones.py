import arcade
import random
from typing import List, Optional

import constants as c


class Dice(arcade.Sprite):
    def __init__(self, value, scale=c.DICE_SCALE):
        self.value = value
        self.image_file_name = f'images/dice/Side_{self.value}_Pips.png'

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


class KnuckleBones(arcade.Window):
    player_one_score: int

    def __init__(self):
        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)

        self.current_turn: Optional[bool] = None

        arcade.set_background_color(c.BACKGROUND_COLOR)

    def setup(self):
        self.player_one_score: int = 0
        self.player_one_column_scores: List[int] = [0, 0, 0]
        self.player_two_score: int = 0
        self.player_two_column_scores: List[int] = [0, 0, 0]

        # Newest Dice Sprite for each player
        self.player_one_current_dice: arcade.Sprite = arcade.Sprite()
        self.player_two_current_dice: arcade.Sprite = arcade.Sprite()

        # List of sprite lists containing player 1's active dice
        self.player_one_dice_list_group: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                                    arcade.SpriteList(),
                                                                    arcade.SpriteList()]

        # List of sprite lists containing player 2's active dice
        self.player_two_dice_list_group: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                                    arcade.SpriteList(),
                                                                    arcade.SpriteList()]

        # List of sprites that hold the dice trays for both players
        self.dice_trays: arcade.SpriteList = arcade.SpriteList()

        # List of sprite lists that make up player 1's tile board
        self.player_one_tile_group: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                               arcade.SpriteList(),
                                                               arcade.SpriteList()]

        # List of lists used to keep score of player 1's columns
        self.player_one_dice_group: List[List[int]] = [[], [], []]

        # List of sprite lists that make up player 2's tile board
        self.player_two_tile_group: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                               arcade.SpriteList(),
                                                               arcade.SpriteList()]

        # List of lists used to keep score of player 2's columns
        self.player_two_dice_group: List[List[int]] = [[], [], []]

        # Player 1 dice tray
        bottom_tray: arcade.Sprite = arcade.SpriteSolidColor(c.DICE_TRAY_WIDTH, c.DICE_TRAY_HEIGHT, c.TILE_COLOR)
        bottom_tray.position = c.BOTTOM_TRAY_X, c.BOTTOM_TRAY_Y
        self.dice_trays.append(bottom_tray)

        # Player 2 dice tray
        top_tray: arcade.Sprite = arcade.SpriteSolidColor(c.DICE_TRAY_WIDTH, c.DICE_TRAY_HEIGHT, c.TILE_COLOR)
        top_tray.position = c.TOP_TRAY_X, c.TOP_TRAY_Y
        self.dice_trays.append(top_tray)

        # Player 1 tile columns
        for i in range(len(self.player_one_tile_group)):
            for j in range(3):
                tile: arcade.Sprite = arcade.SpriteSolidColor(c.TILE_DIMENSIONS, c.TILE_DIMENSIONS,
                                                              c.TILE_COLOR_LIST[i])
                tile.position = c.BOARD_X_START + i * c.TILE_X_SPACING, c.BOTTOM_BOARD_Y - j * c.TILE_Y_SPACING
                self.player_one_tile_group[i].append(tile)

        # Player 2 tile columns
        for i in range(len(self.player_two_tile_group)):
            for j in range(3):
                tile: arcade.Sprite = arcade.SpriteSolidColor(c.TILE_DIMENSIONS, c.TILE_DIMENSIONS,
                                                              c.TILE_COLOR_LIST[i])
                tile.position = c.BOARD_X_START + i * c.TILE_X_SPACING, c.TOP_BOARD_Y + j * c.TILE_Y_SPACING
                self.player_two_tile_group[i].append(tile)

        self.create_dice(self.goes_first())

    def on_draw(self):
        self.clear()

        self.dice_trays.draw()

        # Draws the current dice sprite for each player
        self.player_one_current_dice.draw()
        self.player_two_current_dice.draw()

        # Draws the player 1 board tiles
        for column in self.player_one_tile_group:
            column.draw()

        # Draws the player 2 board tiles
        for column in self.player_two_tile_group:
            column.draw()

        # Draws the player 1 dice sprites
        for player_one_dice_column in self.player_one_dice_list_group:
            player_one_dice_column.draw()

        # Draws the player 2 dice sprites
        for player_two_dice_column in self.player_two_dice_list_group:
            player_two_dice_column.draw()

        # Draws the player names
        arcade.draw_text(c.PLAYER_ONE, c.BOTTOM_TRAY_X, c.BOTTOM_TRAY_Y + c.DICE_TRAY_HEIGHT / 2 + 55, font_size=20,
                         anchor_x='center', anchor_y='center')
        arcade.draw_text(c.PLAYER_TWO, c.TOP_TRAY_X, c.TOP_TRAY_Y - c.DICE_TRAY_HEIGHT / 2 - 55, font_size=20,
                         anchor_x='center', anchor_y='center')

        # arcade.draw_text(goes_first + ' \'s turn', c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 10, font_size=40,
        #                  anchor_x='center')

        # Draws the total score for each player if they have points
        if self.player_one_score > 0:
            arcade.draw_text(self.player_one_score, c.BOTTOM_TRAY_X, c.BOTTOM_TRAY_Y + c.DICE_TRAY_HEIGHT / 2 + 25,
                             font_size=20,
                             anchor_x='center', anchor_y='center')

        if self.player_two_score > 0:
            arcade.draw_text(self.player_two_score, c.TOP_TRAY_X, c.TOP_TRAY_Y - c.DICE_TRAY_HEIGHT / 2 - 25,
                             font_size=20,
                             anchor_x='center', anchor_y='center')

        # Draws the column score for each player if they have points
        for index, score in enumerate(self.player_one_column_scores):
            if score > 0:
                arcade.draw_text(score, c.BOARD_X_START + index * c.TILE_X_SPACING,
                                 c.BOTTOM_BOARD_Y + c.TILE_DIMENSIONS - 20, font_size=15,
                                 anchor_x='center', anchor_y='center')

        for index, score in enumerate(self.player_two_column_scores):
            if score > 0:
                arcade.draw_text(score, c.BOARD_X_START + index * c.TILE_X_SPACING,
                                 c.TOP_BOARD_Y - c.TILE_DIMENSIONS + 20, font_size=15,
                                 anchor_x='center', anchor_y='center')

        if self.is_board_full():
            arcade.draw_text(self.winner_text(), c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 + 10,
                             font_size=40, anchor_x='center', anchor_y='center')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            self.setup()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.current_turn:
            current_dice = self.player_one_current_dice
            tile_group = self.player_one_tile_group
            dice_group = self.player_one_dice_group

            opposite_dice_group = self.player_two_dice_group
            dice_list = self.player_one_dice_list_group
            opposite_dice_list = self.player_two_dice_list_group
            opposite_tile_group = self.player_two_tile_group
        else:
            current_dice = self.player_two_current_dice
            tile_group = self.player_two_tile_group
            dice_group = self.player_two_dice_group

            opposite_dice_group = self.player_one_dice_group
            dice_list = self.player_two_dice_list_group
            opposite_dice_list = self.player_one_dice_list_group
            opposite_tile_group = self.player_one_tile_group

        self.perform_turn(x, y, tile_group, dice_group, current_dice, dice_list,
                          opposite_dice_list, opposite_dice_group, opposite_tile_group)

    @staticmethod
    def roll_dice() -> int:
        """
        :return: a random number between 1 and 6. Used to determine turn, and for setting dice values.
        """
        return random.randint(1, 6)

    def goes_first(self) -> bool:
        """
        Determines which player goes first
        :return: True - Player 1, False - Player 2
        """
        self.current_turn = self.roll_dice() % 2 == 0
        return self.current_turn

    def create_dice(self, current_turn: bool) -> None:
        """
        Creates a new Dice object and places it on the current turn player's mat
        :param current_turn: who's turn is it. Used to determine where to place the dice
        """
        dice: Dice = Dice(self.roll_dice())
        if current_turn:
            dice.position = c.BOTTOM_TRAY_X, c.BOTTOM_TRAY_Y
            self.player_one_current_dice = dice
        else:
            dice.position = c.TOP_TRAY_X, c.TOP_TRAY_Y
            self.player_two_current_dice = dice

    def perform_turn(self, x: int, y: int, tile_group: List[arcade.SpriteList], dice_group: List[List[int]],
                     current_dice: arcade.Sprite, dice_list: List[arcade.SpriteList],
                     opposite_dice_list: List[arcade.SpriteList], opposite_dice_group: List[List[int]],
                     opposite_tile_group: List[arcade.SpriteList]) -> None:
        """
        The workhorse method of the game logic. Places the current dice, calls methods to filter dice and update score
        :param x: x coordinate of mouse click
        :param y: y coordinate of mouse click
        :param tile_group: the dice_group_column of SpriteLists containing the board tiles of the current turn player
        :param dice_group: the lists containing the value of each dice of the current turn player
        :param current_dice: the latest dice sprite
        :param dice_list: the dice_group_column of SpriteLists containing all the dice of the current turn player
        :param opposite_dice_list: the dice_group_column containing all the dice of the opposite turn player
        :param opposite_dice_group: the lists containing the value of each dice of the opposite turn player
        :param opposite_tile_group: the dice_group_column containing the board tiles of the opposite turn player
        """
        for column_index in range(len(tile_group)):
            tile_location = arcade.get_sprites_at_point((x, y), tile_group[column_index])
            # If the column has an open spot for the dice, place dice in the lowest/highest open spot.
            if len(tile_location) > 0 and len(dice_group[column_index]) < 3:
                current_dice.position = tile_group[column_index][len(dice_list[column_index])].position
                dice_list[column_index].append(current_dice)
                dice_group[column_index].append(current_dice.value)

                opposite_dice_list[column_index] = self.filter_dice(opposite_dice_list[column_index],
                                                                    current_dice.value)
                opposite_dice_group[column_index] = self.remove_values_from_list(opposite_dice_group[column_index],
                                                                                 dice_list[column_index][-1].value)

                self.move_remaining_dice_to_position(opposite_dice_list[column_index],
                                                     opposite_tile_group[column_index])

                self.calculate_score()

                if not self.is_board_full():
                    self.current_turn = not self.current_turn
                    self.create_dice(self.current_turn)

                # Prints the column scores for each player. Useful for testing and debugging.
                # print(self.player_two_dice_group)
                # print(self.player_one_dice_group)
                # print()

    def calculate_score(self) -> None:
        """
        Updates the column scores and total score for each player. If a player has more than 1 dice with the same value
        in a column, the dice value is multiplied by the number of dice with that value.
        eg.: column = [4, 3, 4]. column score = 19 (4 * 2 * 2 + 3 * 1 * 1)
        eg.: column = [1, 1, 1]. column score =  9 (1 * 3 * 3)
        """
        for index, (player_one_column, player_two_column) in enumerate(
                zip(self.player_one_dice_group, self.player_two_dice_group)):
            self.player_one_column_scores[index] = 0
            self.player_two_column_scores[index] = 0

            player_one_dict = self.get_dice_count(player_one_column)
            player_two_dict = self.get_dice_count(player_two_column)

            for key in player_one_dict:
                self.player_one_column_scores[index] += key * player_one_dict[key] * player_one_dict[key]
            for key in player_two_dict:
                self.player_two_column_scores[index] += key * player_two_dict[key] * player_two_dict[key]

        self.player_one_score = sum(self.player_one_column_scores)
        self.player_two_score = sum(self.player_two_column_scores)

    @staticmethod
    def get_dice_count(player_column: List[int]) -> dict[int, int]:
        """
        Counts the dice occurrence in a column. Used later to determine a score multiplier
        :param player_column: the column in the player dice group
        :return: a dictionary with the number of dice occurrences for the column
        """
        player_dict = {}

        for dice in player_column:
            if dice in player_dict:
                player_dict[dice] += 1
            else:
                player_dict[dice] = 1
        return player_dict

    @staticmethod
    def remove_values_from_list(dice_group_column: List[int], val: int) -> List:
        """
        Takes a list on ints and filters out desired ints. Used to update values when the opposite player attacks
        :param dice_group_column: a list of integers
        :param val: the int you want removed from list
        :return: a new list without the passed in value
        """
        return [value for value in dice_group_column if value != val]

    @staticmethod
    def filter_dice(dice_list: arcade.SpriteList, value: int):
        """
        Takes a SpriteList and removes sprites containing a passed in value.
        Used to update dice when the opposite player attacks
        :param dice_list: SpriteList containing sprites
        :param value: the value that is undesired
        :return: the same SpriteList passed but no longer containing undesired sprites
        """
        # For some reason the last dice is not removed in the first pass. Running it again removes the last dice.
        for _ in range(2):
            for dice in dice_list:
                if dice.value == value:
                    dice_list.remove(dice)
        return dice_list

    def move_remaining_dice_to_position(self, dice_list: arcade.sprite_list, tile_column: arcade.sprite_list) -> None:
        """
        Once dice are removed in filter_dice(), we need to reposition the remaining dice to the top/bottom of the board
        :param dice_list: SpriteList containing the remaining dice
        :param tile_column: SpriteList containing the board tiles. Used to place dice to the tile's position
        """
        if 0 < len(dice_list) < 3:
            for dice_index, remaining_dice in enumerate(dice_list):
                remaining_dice.position = tile_column[dice_index].position

    def is_board_full(self):
        """
        Checks if a board is full. Used to end the game
        :return: True if either dice count is 9
        """
        player_one_dice_count = 0
        player_two_dice_count = 0
        for p1_column, p2_column in zip(self.player_one_dice_list_group, self.player_two_dice_list_group):
            player_one_dice_count += len(p1_column)
            player_two_dice_count += len(p2_column)
        return player_one_dice_count == 9 or player_two_dice_count == 9

    def winner_text(self):
        if self.player_one_score > self.player_two_score:
            winner = c.PLAYER_ONE
        else:
            winner = c.PLAYER_TWO
        return f'{winner} is the winner!'


def main():
    window = KnuckleBones()
    window.setup()
    window.run()


if __name__ == '__main__':
    main()
