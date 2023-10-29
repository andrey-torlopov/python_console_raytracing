from math import cos, sin

from utils import sign, step


class Point:

    def __init__(self, x: float, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"
    # Определение оператора сложения

    def __add__(self, other: 'Point') -> 'Point':
        if isinstance(other, (int | float)):  # Если other - это число
            return Point(self.x + other, self.y + other, self.z + other)
        elif isinstance(other, Point):  # Если other - это другой объект Point
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise ValueError("Unsupported type for multiplication")

    # Определение оператора вычитания
    def __sub__(self, other: 'Point') -> 'Point':
        # return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, (int | float)):  # Если other - это число
            return Point(self.x - other, self.y - other, self.z - other)
        elif isinstance(other, Point):  # Если other - это другой объект Point
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise ValueError("Unsupported type for multiplication")

     # Определение оператора умножения
    def __mul__(self, other) -> 'Point':
        if isinstance(other, (int | float)):  # Если other - это число
            return Point(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Point):  # Если other - это другой объект Point
            return Point(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            raise ValueError("Unsupported type for multiplication")

    # Определение оператора деления

    def __truediv__(self, other) -> 'Point':
        if isinstance(other, (int | float)):  # Если other - это число
            if other == 0:
                return Point(0, 0, 0)  # Если деление на ноль, возвращаем Point(0, 0, 0)
            return Point(self.x / other, self.y / other, self.z / other)
        elif isinstance(other, Point):  # Если other - это другой объект Point
            # Если координата other равна нулю, возвращаем 0 для соответствующей координаты
            x = self.x / other.x if other.x != 0 else 0
            y = self.y / other.y if other.y != 0 else 0
            z = self.z / other.z if other.z != 0 else 0
            return Point(x, y, z)
        else:
            raise ValueError("Unsupported type for division")

    @property
    def distance_to_center(self) -> float:
        return (self.x*self.x + self.y*self.y + self.z * self.z) ** 0.5

    def to_unit_vector(self) -> 'Point':
        '''
        Нормализуем в единичный вектор с сохранением направления.
        '''
        x = self.x / self.distance_to_center if self.distance_to_center != 0 else 0
        y = self.y / self.distance_to_center if self.distance_to_center != 0 else 0
        z = self.z / self.distance_to_center if self.distance_to_center != 0 else 0
        return Point(x, y, z)

    def dot(self, other: 'Point') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def abs(self) -> 'Point':
        return Point(abs(self.x), abs(self.y), abs(self.z))

    def sign(self) -> 'Point':
        return Point(sign(self.x), sign(self.y), sign(self.z))

    def step(self, edge: 'Point') -> 'Point':
        return Point(
            step(edge.x, self.x),
            step(edge.y, self.y),
            step(edge.z, self.z)
        )

    def reflect(self, normal: 'Point') -> 'Point':
        return self - normal * 2 * self.dot(normal)

    # Возможно методы поворота надо будет поправить и саму точку менять.
    def rotateX(self, angle: float) -> 'Point':
        b = Point(self.x, self.y, self.z)
        b.z = self.z * cos(angle) - self.y * sin(angle)
        b.y = self.z * sin(angle) + self.y * cos(angle)
        return b

    def rotateY(self, angle: float) -> 'Point':
        b = Point(self.x, self.y, self.z)
        b.x = self.x * cos(angle) - self.z * sin(angle)
        b.z = self.x * sin(angle) + self.z * cos(angle)
        return b

    def rotateZ(self, angle: float) -> 'Point':
        b = Point(self.x, self.y, self.z)
        b.x = self.x * cos(angle) - self.y * sin(angle)
        b.y = self.x * sin(angle) + self.y * cos(angle)
        return b

    # Сформировать объект сферы
    def sphere(self, other: 'Point', r: float) -> 'Point':
        b = self.dot(other)
        c = self.dot(self) - r * r
        h = b * b - c
        if h < 0.0:
            return Point(-1.0)
        h = h ** 0.5
        return Point(-b - h, -b + h)

    def box(self, other: 'Point', box_size: 'Point', out_normal: 'Point'):
        m = Point(1.0) / other
        n = m * self
        k = m.abs() * box_size
        t1 = n * (-1) - k
        t2 = n * (-1) + k
        tN = max(max(t1.x, t1.y), t1.z)
        tF = min(min(t2.x, t2.y), t2.z)
        if tN > tF or tF < 0.0:
            return Point(-1.0)
        yzx = Point(t1.y, t1.z, t1.x)
        zxy = Point(t1.z, t1.x, t1.y)
        out_normal = other.sign() * (-1) * yzx.step(t1) * zxy.step(t1)
        return Point(tN, tF)

    def plane(self, other: 'Point', p: 'Point', w: float) -> float:
        return -(self.dot(p) + w) / other.dot(p)
