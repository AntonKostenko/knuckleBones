import arcade

from typing import List

SCREEN_WIDTH: int = 1024
SCREEN_HEIGHT: int = 768
SCREEN_TITLE: str = 'Knuckle Bones'
BACKGROUND_COLOR: arcade.Color = arcade.color.JET

DICE_SCALE: float = 0.7
DICE_DIMENSIONS: float = 100 * DICE_SCALE

TILE_PERCENT_OVERSIZE: float = 1.25
TILE_DIMENSIONS: int = int(DICE_DIMENSIONS * TILE_PERCENT_OVERSIZE)

VERTICAL_MARGIN_PERCENT: float = 0.07
HORIZONTAL_MARGIN_PERCENT: float = 0.07
TILE_X_SPACING: float = TILE_DIMENSIONS + TILE_DIMENSIONS * HORIZONTAL_MARGIN_PERCENT
TILE_Y_SPACING: float = TILE_DIMENSIONS + TILE_DIMENSIONS * VERTICAL_MARGIN_PERCENT
TILE_COLOR: arcade.Color = arcade.color.DARK_OLIVE_GREEN
TILE_COLOR_LIST: List[arcade.Color] = [arcade.color.DARK_OLIVE_GREEN,
                                       arcade.color.DARK_SEA_GREEN,
                                       arcade.color.AERO_BLUE]

BOARD_X_START: float = SCREEN_WIDTH / 2 - TILE_X_SPACING

TOP_BOARD_Y: float = VERTICAL_MARGIN_PERCENT * TILE_DIMENSIONS + SCREEN_HEIGHT - TILE_DIMENSIONS * 3
BOTTOM_BOARD_Y: float = VERTICAL_MARGIN_PERCENT * TILE_DIMENSIONS + TILE_DIMENSIONS * 3

DICE_TRAY_WIDTH: int = 250
DICE_TRAY_HEIGHT: int = 150

TOP_TRAY_X: int = SCREEN_WIDTH - 175
TOP_TRAY_Y: int = SCREEN_HEIGHT - TILE_DIMENSIONS - TILE_DIMENSIONS

BOTTOM_TRAY_X: int = 175
BOTTOM_TRAY_Y: int = TILE_DIMENSIONS + TILE_DIMENSIONS

PLAYER_ONE: str = 'Player 1'
PLAYER_TWO: str = 'Player 2'

ATTACKED_DICE_COLOR = arcade.color.CARMINE_PINK
THREE_X_MOD_COLOR = arcade.color.BALL_BLUE
TWO_X_MOD_COLOR = arcade.color.AFRICAN_VIOLET

MENU_BUTTON_WIDTH: int = 200
MENU_BUTTON_HEIGHT: int = 115

MENU_BUTTON_X_SPACING: float = MENU_BUTTON_WIDTH + MENU_BUTTON_WIDTH * HORIZONTAL_MARGIN_PERCENT
MENU_BUTTON_START: float = SCREEN_WIDTH / 2 - MENU_BUTTON_X_SPACING
MENU_BUTTON_NAMES: List[str] = ['Play', 'Instructions', 'Settings']
MENU_SUB_TEXT: str = 'A dice game of risk and reward'

INSTRUCTION_BUTTON_SPACING: float = MENU_BUTTON_WIDTH / 2 - MENU_BUTTON_WIDTH * HORIZONTAL_MARGIN_PERCENT / 2
INSTRUCTION_BUTTON_START: float = SCREEN_WIDTH / 2 - INSTRUCTION_BUTTON_SPACING
INSTRUCTION_BUTTON_NAMES: List[str] = ['Play', 'Back']
INSTRUCTIONS_SUB_TEXT: str = 'Your score is calculated by adding all your dice together.'

INSTRUCTIONS_LEFT_MAT_X: float = SCREEN_WIDTH / 3 - 50
INSTRUCTIONS_RIGHT_MAT_X: float = SCREEN_WIDTH * (2 / 3) + 50
INSTRUCTION_MAT_Y: float = SCREEN_HEIGHT * 0.6

MATCH_DICE_X_START = SCREEN_WIDTH / 3 - DICE_DIMENSIONS - DICE_DIMENSIONS * 0.25
DESTROY_DICE_X_START = SCREEN_WIDTH * (2 / 3) + DICE_DIMENSIONS / 2


MATCH_DICE_RULE_TEXT: str = 'When dice of the same number are placed in the same column, multiply their value.'
DESTROY_OPPONENT_RULE_TEXT: str = 'Destroy your opponent\'s dice by matching yours to theirs.'

SETTINGS_BUTTON_START: float = SCREEN_WIDTH / 2
SETTINGS_BUTTON_NAMES: List[str] = ['Back']
