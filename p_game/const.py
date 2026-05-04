EASY   = 0
NORMAL = 1
HARD   = 2

# ==========

T_BOX    = 0
T_VISION = 1
T_PLAYER = 2
T_ELEMS  = 3

# ==========

IS_HERE     = 1
IS_TOP      = 8
IS_BOT      = -7
IS_NOT_HERE = 0

# ==========

DONT_SEE = 0
SEE_TOP  = 10
SEE_BOT  = -9
SEE      = 1

# ==========

N_ROW = 6
N_COL = 8

# ==========

CAVERN = 0
C1     = 1
C2     = 2
N_HOLE = 4
HOLE   = 8

N_WUMP   = 16
WUMPUS   = 32
BAT      = 64
PLAYER   = 128
TRIG_BAT = 256

ADD_TRIG_BAT = TRIG_BAT - BAT

# ==========

# C1
#   ↳
# ↰

# C2
# ↲
#   ↱

# ==========

# 0  = no game → start
# 1  = playing
# 2  = one bat is trigger
# 3  = walked on a triggered bat
# -1 = Win with the arc
# -2 = dead by wumpus
# -3 = dead by hole