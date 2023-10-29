from point import Point
from utils import clamp


class Scene:
    '''
    stdscr - содержит набор символов который мы задали вначале и можем 
    по x-y теперь рисовать элементы (если они корректно заданы в массиве)
    '''

    def __init__(self, stdscr, height: int, width: int) -> None:
        self.stdscr = stdscr
        self.height = height
        self.width = width
        self.screen_aspect = width / height
        self.letter_aspect = 58 / 126  # 1 / 2
        self.gradient = " .:!/r(l1Z4H9W8$@"
        self.gradient_size = len(self.gradient)  # возможно надо будет 2 вычесть

    def draw(self, x: int, y: int, char: str) -> None:
        self.stdscr.addch(y, x, char)

    def get_char(self, distance_to_center: float, radius: float) -> str:
        normalized_distance = 1 - distance_to_center / radius
        char_index = int(normalized_distance * self.gradient_size)
        char_index = clamp(char_index, 0, self.gradient_size - 1)
        return self.gradient[char_index]

    def get_char_by_index(self, index) -> str:
        char_index = clamp(index, 0, self.gradient_size - 1)
        return self.gradient[char_index]

    def scale_to_unit_range(self, point: 'Point') -> 'Point':
        '''
        нормализуем относительно экрана. Чтобы точка вписывалась в квадрат [-1, 1]
        '''
        x = 2.0 * point.x / float(self.width) - 1
        y = 2.0 * point.y / float(self.height) - 1
        return Point(x, y)
