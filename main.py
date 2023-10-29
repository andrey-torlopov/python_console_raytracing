import curses
import time
from math import sin

from point import Point
from scene import Scene


def main(stdscr) -> None:
    scene = configure_screen(stdscr)
    t = 0
    light = Point(-0.5, 0.5, -1).to_unit_vector()
    spherePos = Point(0, 3, 0)

    while True:
        time.sleep(0.01)
        t += 1
        for i in range(scene.height):
            for j in range(scene.width):
                point_2d = Point(j, i)
                point_2d = scene.scale_to_unit_range(point_2d)
                point_2d.x *= scene.screen_aspect
                point_2d.x *= scene.letter_aspect
                point_2d.x += sin(t * 0.01)

                ro = Point(-6, 0, 0)  # Camera position
                rd = Point(2, point_2d.x, point_2d.y).to_unit_vector()  # Ray direction

                ro = ro.rotateY(0.25)
                ro = ro.rotateZ(t * 0.01)
                rd = rd.rotateY(0.25)
                rd = rd.rotateZ(t * 0.01)

                diff = 1

                for k in range(6):
                    minIt: float = 99_999
                    p = ro - spherePos
                    intersection = p.sphere(rd, 1)
                    n = Point(0)
                    albedo = 1

                    if intersection.x > 0:
                        itPoint = ro - spherePos + rd * intersection.x
                        minIt = intersection.x
                        n = itPoint.to_unit_vector()

                    boxN = Point(0)
                    intersection = ro.box(rd, 1, boxN)
                    if intersection.x > 0 and intersection.x < minIt:
                        minIt = intersection.x
                        n = boxN

                    intersection = ro.plane(rd, Point(0, 0, -1), 1)

                    # может надо x убрать, т.к. plane возвращает float ?
                    if intersection > 0 and intersection < minIt:
                        minIt = intersection
                        n = Point(0, 0, -1)
                        albedo = 0.5

                    if minIt < 99999:
                        diff *= (n.dot(light) * 0.5 + 0.5) * albedo
                        ro = ro + rd * (minIt - 0.01)
                        rd = rd.reflect(n)
                    else:
                        break
                # Почему 20?
                color_index = int(diff * 20)
                scene.draw(j, i, scene.get_char_by_index(color_index))

                # WORK CODE ⬇️
                # distance_to_center = point_2d.distance_to_center
                # radius = 0.6
                # if distance_to_center <= radius:
                #     char = scene.get_char(distance_to_center, radius)
                #     scene.draw(j, i, char)
                # else:
                #     scene.draw(j, i, scene.gradient[0])

        # ---
        stdscr.addstr(0, 0, " " * (scene.width - 10))  # очистка строки
        stdscr.addstr(0, 0, f"fps: {1 / 0.01}")
        stdscr.refresh()

        # stdscr.addstr(1, 0, " " * (scene.width - 10))  # очистка строки
        # stdscr.addstr(1, 0, f"point: [{point1}]  x, y: [{x}, {y}]")


def configure_screen(stdscr) -> Scene:
    # Отключение автоматического вывода символов на экран и включение режима работы с клавишами
    curses.noecho()
    curses.curs_set(False)
    curses.cbreak()
    stdscr.keypad(True)

    # Получение размеров терминала
    height, width = stdscr.getmaxyx()
    height -= 1
    canvasArray = [' ' for _ in range(height * width)]

    # Заполнение массива и вывод его на экран
    for i in range(len(canvasArray)):
        x = i // width
        y = i % width
        stdscr.addch(x, y, canvasArray[i])

    return Scene(stdscr=stdscr, height=height, width=width)


if __name__ == '__main__':
    curses.wrapper(main)
    curses.wrapper(main)
