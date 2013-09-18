#-*- coding: latin1 -*-

W_WIDTH = 640
W_HEIGHT = 480
BLOCK_SIZE = 30

TOP_MARGIN = 75
LEFT_MARGIN = 20

#
NUM_LINES = ((W_HEIGHT - TOP_MARGIN * 2) / BLOCK_SIZE) * 2 + 1
NUM_COLUM = ((W_WIDTH - LEFT_MARGIN * 2) / BLOCK_SIZE) + 1

#Colors
C_WHITE = (255, 255, 255, 255*0.9)
C_GRAY 	= (255, 255, 255, 255*0.1)
C_P1 	= (200, 0, 255, 255*0.7)
C_P2 	= (12, 147, 232, 255*0.7)
C_P3 	= (232, 90, 12, 255*0.7)
C_P4 	= (20, 255, 0, 255*0.7)

PORT = 8888

colorDefine = {1 : C_P1, 2 : C_P2, 3 : C_P3, 4 : C_P4}

