import arcade
import random

from typing import List, Tuple

import constants as c
from dice import Dice


class KnuckleBones(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(c.BACKGROUND_COLOR)

        self.current_turn = None
        self.goes_first_name = None
        self.first_turn = None

        self.player_one_score = None
        self.player_one_column_scores = None
        self.player_two_score = None
        self.player_two_column_scores = None

        # Newest Dice Sprite for each player
        self.player_one_current_dice = None
        self.player_two_current_dice = None

        # List of sprite lists containing player 1's active dice
        self.player_one_dice_list_group = None

        # List of sprite lists containing player 2's active dice
        self.player_two_dice_list_group = None

        # List of sprites that hold the dice trays for both players
        self.dice_trays = None

        # List of sprite lists that make up player 1's tile board
        self.player_one_tile_group = None

        # List of sprite lists that make up player 2's tile board
        self.player_two_tile_group = None

        # Temp vars used to update player's dice and scores
        self.current_dice = None
        self.tile_group = None
        self.dice_list = None
        self.opposite_dice_list = None
        self.opposite_tile_group = None

        self.temp_dice_list = None
        self.temp_sprite_destination = None
        self.temp_column_index = None

        # Used to stop mouse spamming which can cause animation issues
        self.mouse_debounce_timer = None

        # Flag for setting easy AI
        self.vs_ai_easy = None
        # Flag for setting hard AI
        self.vs_ai_hard = None

        # Amount of time before AU performs turn
        self.ai_timer = None

        self.player_one_dicts = None
        self.player_two_dicts = None

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

        # List of sprite lists that make up player 2's tile board
        self.player_two_tile_group: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                               arcade.SpriteList(),
                                                               arcade.SpriteList()]

        # Temp vars used to update player's dice and scores
        self.current_dice: arcade.Sprite = arcade.Sprite()
        self.tile_group: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                    arcade.SpriteList(),
                                                    arcade.SpriteList()]
        self.dice_list: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                   arcade.SpriteList(),
                                                   arcade.SpriteList()]
        self.opposite_dice_list: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                            arcade.SpriteList(),
                                                            arcade.SpriteList()]
        self.opposite_tile_group: List[arcade.SpriteList] = [arcade.SpriteList(),
                                                             arcade.SpriteList(),
                                                             arcade.SpriteList()]

        self.temp_dice_list: List = []
        self.temp_sprite_destination: Tuple = ()
        self.temp_column_index: int = 0

        # Debounce timer to stop some animation issues when spamming the mouse
        self.mouse_debounce_timer: float = 0

        # Time the AI waits before performing turn
        self.ai_timer: float = 0

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

        self.current_turn = self.roll_dice() % 2 == 0
        self.first_turn: bool = True
        self.goes_first()
        self.create_dice()

        # Flag for setting easy AI
        self.vs_ai_easy: bool = False
        # Flag for setting hard AI
        self.vs_ai_hard = True

        self.player_one_dicts = [{}, {}, {}]
        self.player_two_dicts = [{}, {}, {}]

    def on_draw(self):
        self.clear()

        self.dice_trays.draw()

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

        # Draws the current dice sprite for each player
        self.player_one_current_dice.draw()
        self.player_two_current_dice.draw()

        # Draws the player names
        arcade.draw_text(c.PLAYER_ONE, c.BOTTOM_TRAY_X, c.BOTTOM_TRAY_Y + c.DICE_TRAY_HEIGHT / 2 + 55, font_size=20,
                         anchor_x='center', anchor_y='center')
        arcade.draw_text(c.PLAYER_TWO, c.TOP_TRAY_X, c.TOP_TRAY_Y - c.DICE_TRAY_HEIGHT / 2 - 55, font_size=20,
                         anchor_x='center', anchor_y='center')

        if self.first_turn:
            arcade.draw_text(self.goes_first_name + ' goes first', c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 10,
                             font_size=40, anchor_x='center', anchor_y='center')

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

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        self.mouse_debounce_timer += delta_time
        self.ai_timer += delta_time

        if self.current_turn:
            self.player_one_current_dice.roll_dice_animation(delta_time)
        else:
            self.player_two_current_dice.roll_dice_animation(delta_time)

        if self.vs_ai_easy:
            self.perform_easy_ai_turn()
        elif self.vs_ai_hard:
            self.perform_hard_ai_turn()

        self.move_current_dice_to_position()
        if self.filter_dice():
            self.calculate_score()
        self.set_multiplier_colors()
        self.move_remaining_dice_to_position()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            self.setup()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.mouse_debounce_timer > 1:
            if self.vs_ai_easy or self.vs_ai_hard:
                if self.current_turn:
                    self.perform_turn(x, y)
            else:
                self.perform_turn(x, y)

    def set_turn_values(self) -> None:
        self.temp_sprite_destination = ()
        if self.current_turn:
            self.current_dice = self.player_one_current_dice
            self.tile_group = self.player_one_tile_group
            self.dice_list = self.player_one_dice_list_group

            self.opposite_dice_list = self.player_two_dice_list_group
            self.opposite_tile_group = self.player_two_tile_group
        else:
            self.current_dice = self.player_two_current_dice
            self.tile_group = self.player_two_tile_group
            self.dice_list = self.player_two_dice_list_group

            self.opposite_dice_list = self.player_one_dice_list_group
            self.opposite_tile_group = self.player_one_tile_group

    def goes_first(self) -> None:
        """
        Used to determine which player name to display.
        """
        if self.current_turn:
            self.goes_first_name = c.PLAYER_ONE
        else:
            self.goes_first_name = c.PLAYER_TWO

    @staticmethod
    def roll_dice() -> int:
        """
        :return: a random number between 1 and 6. Used to determine turn, and for setting dice values.
        """
        return random.randint(1, 6)

    def create_dice(self) -> None:
        """
        Creates a new Dice object and places it on the current turn player's mat
        """
        dice: Dice = Dice(self.roll_dice())
        dice.speed = 35
        if self.current_turn:
            dice.position = c.BOTTOM_TRAY_X, c.BOTTOM_TRAY_Y
            self.player_one_current_dice = dice
        else:
            dice.position = c.TOP_TRAY_X, c.TOP_TRAY_Y
            self.player_two_current_dice = dice

    def set_multiplier_colors(self) -> None:
        """
        Modifies the color of the dice if the column has multiple dice with the same value.
        """
        if not self.temp_sprite_destination:
            return
        if self.current_dice.center_x == self.temp_sprite_destination[0]:
            dice_count: dict[int, int] = self.get_dice_value_count(self.dice_list[self.temp_column_index])
            # If the column is full of dice of the same value, set the dice color to the 3x modifier color
            if 3 in dice_count.values():
                for dice in self.dice_list[self.temp_column_index]:
                    dice.color = c.THREE_X_MOD_COLOR
            # If the column has 2 dice of the same value, set their color to the 2x modifier color
            elif 2 in dice_count.values():
                for dice in self.dice_list[self.temp_column_index]:
                    if dice_count[dice.value] == 2:
                        dice.color = c.TWO_X_MOD_COLOR

    def perform_turn(self, x: int, y: int) -> None:
        """
        The workhorse method of the game logic. Places the current dice, calls methods to filter dice and update score
        :param x: x coordinate of mouse click
        :param y: y coordinate of mouse click
        """
        self.set_turn_values()

        for column_index in range(len(self.tile_group)):
            tile_location: List[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.tile_group[column_index])
            # If the column has an open spot for the dice, place dice in the lowest/highest open spot.
            if len(tile_location) > 0 and len(self.dice_list[column_index]) < 3:
                self.first_turn = False

                self.finish_turn(column_index)

                if self.vs_ai_easy or self.vs_ai_hard:
                    self.mouse_debounce_timer = -2
                else:
                    self.mouse_debounce_timer = 0

    def perform_easy_ai_turn(self) -> None:
        """
        The logic used for an "easy" AI opponent.
        The AI checks what columns have an open spot and randomly selects one of them.
        """
        if self.current_turn or self.ai_timer < 2 or self.is_board_full():
            return
        self.set_turn_values()
        self.first_turn = False

        column_has_spot: List[int] = []
        for index in range(len(self.tile_group)):
            if len(self.dice_list[index]) < 3:
                column_has_spot.append(index)
        random_index: int = random.choice(column_has_spot)

        self.finish_turn(random_index)
        self.mouse_debounce_timer = 0

    def finish_turn(self, column_index: int) -> None:
        """
        Performs the functions needed at the end of each turn
        """
        # Used to move current dice in the update() call
        self.temp_sprite_destination = self.tile_group[column_index][len(self.dice_list[column_index])].position

        # Grab index to use in various methods
        self.temp_column_index = column_index
        self.dice_list[column_index].append(self.current_dice)

        if not self.is_board_full():
            self.current_turn = not self.current_turn
            self.create_dice()
        self.calculate_score()
        self.ai_timer = 0

    def get_non_full_column(self) -> List[int]:
        """
        Returns a list of column indexes containing an open spot for a die.
        """
        column_has_spot: List[int] = []
        for index in range(len(self.tile_group)):
            if len(self.dice_list[index]) < 3:
                column_has_spot.append(index)
        return column_has_spot

    @staticmethod
    def pick_best_column(tier_list: List[int], empty_column: List[int], column_has_spot: List[int]) -> int:
        """
        Pick the best option the AI has.
        Returns the index of the best column.
        """
        # Go through the tier list and pick the best option.
        for move_options in tier_list:
            if move_options != -1:
                return move_options
        # If nothing in the tier list, pick a random empty column
        if tier_list.count(-1) == 9 and empty_column:
            return random.choice(empty_column)
        # If no empty column, pick a random column containing an open spot
        else:
            return random.choice(column_has_spot)

    def perform_hard_ai_turn(self) -> None:
        """
        The logic used for a "hard" AI opponent.
        The AI checks what columns have an open spot and selects the best spot.
        """
        if self.current_turn or self.ai_timer < 2 or self.is_board_full():
            return
        self.set_turn_values()
        self.first_turn = False

        column_has_spot = self.get_non_full_column()
        tier_list = [-1] * 7
        empty_column = []

        for open_index in column_has_spot:
            self.fill_in_tier_list(open_index, tier_list)
            # Check if a column is empty
            if len(self.player_two_dicts[open_index]) == 0:
                empty_column.append(open_index)

        best_column = self.pick_best_column(tier_list, empty_column, column_has_spot)

        self.finish_turn(best_column)
        self.mouse_debounce_timer = 0

    def fill_in_tier_list(self, index: int, tier_list: List[int]) -> List[int]:
        """
        The main AI brains. Creates a tier list of options for the AI to use.
        """
        if self.player_two_current_dice.value in self.player_two_dicts[index]:
            # Check if AI can get a 3x multiplier
            if self.player_two_dicts[index][self.player_two_current_dice.value] == 2:
                tier_list[0] = index
            # Check if AI can destroy an opponent dice without filling up AI's column
            if self.player_two_current_dice.value in self.player_one_dicts[index] and \
                    self.player_two_dicts[index][self.player_two_current_dice.value] < 2:
                tier_list[4] = index
        if self.player_two_current_dice.value in self.player_one_dicts[index]:
            # Check if AI can destroy opponent's 3x multiplier
            if self.player_one_dicts[index][self.player_two_current_dice.value] == 3:
                tier_list[2] = index
            # Check if AI can destroy opponent's 2x multiplier
            if self.player_one_dicts[index][self.player_two_current_dice.value] == 2:
                tier_list[3] = index
        # Check if AI can get a 2x multiplier on a die 4 or greater
        if self.player_two_current_dice.value in self.player_two_dicts[index] and \
                self.player_two_current_dice.value > 3:
            tier_list[1] = index
        # Check if AI can destroy an opponent's dice
        if self.player_two_current_dice.value in self.player_one_dicts[index]:
            tier_list[5] = index
        # Check if AI can get a 2x multiplier
        if self.player_two_current_dice.value in self.player_two_dicts[index]:
            tier_list[6] = index
        return tier_list

    def calculate_score(self) -> None:
        """
        Updates the column scores and total score for each player. If a player has more than 1 dice with the same value
        in a column, the dice value is multiplied by the number of dice with that value.
        eg.: column = [4, 3, 4]. column score = 19 (4 * 2 * 2 + 3 * 1 * 1)
        eg.: column = [1, 1, 1]. column score =  9 (1 * 3 * 3)
        """
        for index, (player_one_column, player_two_column) in enumerate(
                zip(self.player_one_dice_list_group, self.player_two_dice_list_group)):
            self.player_one_column_scores[index] = 0
            self.player_two_column_scores[index] = 0

            player_one_dict: dict[int, int] = self.get_dice_value_count(player_one_column)
            player_two_dict: dict[int, int] = self.get_dice_value_count(player_two_column)
            self.player_one_dicts[index] = player_one_dict
            self.player_two_dicts[index] = player_two_dict

            for key in player_one_dict:
                self.player_one_column_scores[index] += key * player_one_dict[key] * player_one_dict[key]
            for key in player_two_dict:
                self.player_two_column_scores[index] += key * player_two_dict[key] * player_two_dict[key]

        self.player_one_score = sum(self.player_one_column_scores)
        self.player_two_score = sum(self.player_two_column_scores)

    @staticmethod
    def get_dice_value_count(player_column: arcade.SpriteList) -> dict[int, int]:
        """
        Counts the dice occurrence in a column. Used later to determine a score multiplier
        :param player_column: the column in the player dice group
        :return: a dictionary with the number of dice occurrences for the column
        """
        player_dict: dict[int, int] = {}

        for dice in player_column:
            if dice.value in player_dict:
                player_dict[dice.value] += 1
            else:
                player_dict[dice.value] = 1
        return player_dict

    def filter_dice(self) -> bool:
        """
        Takes a SpriteList opposite of the current dice column and animates removing
        dice containing the value of the current dice. Begins the animation when the current dice
        gets to its destination.
        Used to update dice when the player attacks.
        Returns True if a die was destroyed, so we can recalculate the score
        """
        for dice in self.opposite_dice_list[self.temp_column_index]:
            if dice.value == self.current_dice.value and self.current_dice.center_x == \
                    self.opposite_dice_list[self.temp_column_index][0].center_x:
                return dice.shrink_dice()

    def move_current_dice_to_position(self) -> None:
        """
        Animate the dice moving from the start position to the position on the board
        """
        if isinstance(self.current_dice, Dice) and self.temp_sprite_destination != ():
            self.current_dice.move_dice(self.temp_sprite_destination)

    def move_remaining_dice_to_position(self) -> None:
        """
        Once dice are removed in filter_dice(), we need to reposition the remaining dice to the top/bottom of the board
        """
        if 0 < len(self.opposite_dice_list[self.temp_column_index]) < 3:
            remaining_dice: Dice
            for dice_index, remaining_dice in enumerate(self.opposite_dice_list[self.temp_column_index]):
                remaining_dice.speed = 20
                remaining_dice.move_dice(self.opposite_tile_group[self.temp_column_index][dice_index].position)

    def is_board_full(self) -> bool:
        """
        Checks if a board is full. Used to end the game
        :return: True if either dice count is 9
        """
        player_one_dice_count: int = 0
        player_two_dice_count: int = 0
        for p1_column, p2_column in zip(self.player_one_dice_list_group, self.player_two_dice_list_group):
            player_one_dice_count += len(p1_column)
            player_two_dice_count += len(p2_column)
        return player_one_dice_count == 9 or player_two_dice_count == 9

    def winner_text(self) -> str:
        if self.player_one_score > self.player_two_score:
            winner: str = c.PLAYER_ONE
        else:
            winner: str = c.PLAYER_TWO
        return f'{winner} is the winner!'
