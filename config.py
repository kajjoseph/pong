# -- Colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# -- Game constants

WIDTH = 575
HEIGHT = 500
FPS = 30
FONT = 'couriernew'
SMALL_FONT = (FONT, 32)  # (fontname, size)
LARGE_FONT = (FONT, 64)  # (fontname, size)
MAX_SCORE = 5
RESET_DELAY = 1 #  Delay after scoring in seconds

# -- Paddle defaults

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10


PLAYER1_X = 50
PLAYER1_Y = int((WIDTH / 2)) - int((PADDLE_HEIGHT / 2))

PLAYER2_X = WIDTH - 50
PLAYER2_Y = int((WIDTH / 2)) - int((PADDLE_HEIGHT / 2))

# -- CPU variables

CPU_PADDLE_SPEED = 8
BALL_CHECK_INTERVAL = 15 #  How often CPU references ball position in frames

# -- Ball defaults

BALL_SIZE = 30
BALL_X = int(WIDTH/2)  # X position at start and after reset
BALL_Y = int(HEIGHT/2) # Y position at start and after reset
BALL_X_SPEED = 4 # Starting speed
BALL_Y_SPEED = 4 # Starting speed
BALL_MAX_SPEED = 8
