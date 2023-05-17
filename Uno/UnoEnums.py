from enum import Enum

Color = Enum('Color', ['RED', 'GREEN', 'YELLOW', 'BLUE', 'BLACK'])
Value = Enum('Value', [*[f'N{str(i)}' for i in range(10)], 'SKIP', 'REV', 'DRAW2', 'WILD', 'WILD4'])