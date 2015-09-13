# -*- encoding=utf-8 -*-
import turtle
from sympy import *
import time
from math import sqrt
from sympy.core.numbers import Float as symFloat
P0 = 40
RADIUS = 10
Kr = 1


def test_draw():
    obstacle = Polygon(Point(-50, -50), Point(-50, 0), Point(0, 20), Point(30, 0), Point(30, -50))
    obstacle_list = list()
    obstacle_list.append(obstacle)
    obstacle = Polygon(*[Point(-50, -50), Point(-50, 0), Point(0, 20), Point(30, 0), Point(30, -50)])
    obstacle = obstacle.translate(100, 100)

    print obstacle.vertices
    draw(obstacle.vertices, True)
    draw(obstacle_list[0].vertices, True)
    path = [Point(0, -100), Point(-100, -100), Point(-100, 30), Point(20, 30), Point(20, 20), Point(50, 20)]
    draw(path)


def test_calculate_f1():
    line = [Point(-50, -50), Point(-50, 0), Point(50, 40)]
    draw(line)
    l1 = Line(line[0], line[1])
    l2 = Line(line[1], line[2])
    f1 = calculate_f1(*line)
    print f1
    draw([line[1], line[1] + f1*100])
    time.sleep(10)


def test_calculate_f2():
    obstacle = Polygon(Point(-50, -50), Point(-50, 0), Point(0, 20), Point(30, 0), Point(30, -50))
    obstacle_list = list()
    obstacle_list.append(obstacle)
    obstacle = obstacle.translate(100, 100)
    obstacle_list.append(obstacle)
    path = [Point(0, -80), Point(-70, -60), Point(-80, 30), Point(40, 30), Point(40, 20), Point(70, 20)]
    f2_list = list()
    f2_list.append(Point(0, 0))

    for i in range(len(path)-2):
        f2_list.append(calculate_f2(path[i+1], obstacle_list))
    for ob in obstacle_list:
        draw(ob.vertices, True)
    draw(path)
    for i in range(len(path)-1):
        print path[i], f2_list[i]
        draw([path[i], path[i] + f2_list[i]])
    time.sleep(10)


def calculate_f2(point, obstacle_tuple):
    p = calculate_bubble_max_size_in_p(point, obstacle_tuple)
    if p >= P0:
        return Point(0, 0)
    else:
        h = p
        x = 0.2
        y = 0.2
        new_x = calculate_bubble_max_size_in_p(Point(point.x - h*x, point.y), obstacle_tuple) - \
                    calculate_bubble_max_size_in_p(Point(point.x + h*x, point.y), obstacle_tuple)
        new_y = calculate_bubble_max_size_in_p(Point(point.x, point.y - h*y), obstacle_tuple) - \
                    calculate_bubble_max_size_in_p(Point(point.x, point.y + h*y), obstacle_tuple)
        pian_dao = Point(new_x, new_y) / (2.0 * h)
        Fr = pian_dao * Kr * (p-P0)
        Fr = Fr.evalf()
        print Fr
        return Fr


def calculate_bubble_max_size_in_p(point, obstacle_tuple):
    t_dis_list = list([P0])
    for obstacle in obstacle_tuple:
        for side in obstacle.sides:
            t_dis = side.distance(point)
            t_dis_list.append(t_dis.evalf())
    return min(t_dis_list)


def unit_length(start, direction):
    t_length = Point.distance(start, direction)
    t_length = t_length.evalf()
    return Point((direction.x-start.x)*1.0/t_length, (direction.y-start.y)*1.0/t_length)


def calculate_f1(start_p, mid_p, end_p):
    u_line1 = unit_length(mid_p, start_p)
    u_line2 = unit_length(mid_p, end_p)
    return Point(u_line1.x+u_line2.x, u_line1.y+u_line2.y)


def draw(point_tuple, close=False):

    start = point_tuple[0]
    basic_mul = 2
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.up()
    pen.setpos(start.x*basic_mul, start.y*basic_mul)

    pen.down()
    pen.speed(5)
    for p in point_tuple:
        pen.setpos(p.x*basic_mul, p.y*basic_mul)
        pen.dot(10, 'red')
    if close is True:
        pen.setpos(start.x*basic_mul, start.y*basic_mul)
    return pen


def divide_line_into_mul_point(start, end, length=20):
    t_length = start.distance(end).evalf()
    num_p = t_length / length + 0.5
    direction = ((end - start) / num_p).evalf()
    result_list = list()
    for i in range(num_p):
        result_list.append(start + direction * i)
    result_list.append(end)
    return result_list


def main():
    obstacle = Polygon(Point(-50, -50), Point(-50, 0), Point(0, 20), Point(30, 0), Point(30, -50))
    obstacle_list = list()
    obstacle_list.append(obstacle)
    obstacle = obstacle.translate(100, 100)
    obstacle_list.append(obstacle)
    path = [Point(0, -80), Point(-70, -60), Point(-80, 30), Point(40, 30), Point(40, 20), Point(70, 20)]
    new_path = list()
    for i in range(len(path)-1):
        new_path += divide_line_into_mul_point(path[i], path[i+1])
    i = 0
    while i < len(new_path) - 1:
        if new_path[i] == new_path[i+1]:
            del new_path[i+1]
        else:
            new_path[i] = new_path[i].evalf()
            i += 1

    for ob in obstacle_list:
        draw(ob.vertices, True)


    pen1 = draw(new_path)
    f2_list = list([Point(0, 0)])
    f1_list = list([Point(0, 0)])
    for _ in range(5):
        f2_list = list([Point(0, 0)])
        f1_list = list([Point(0, 0)])
        for i in range(len(new_path)-2):
            f1_list.append(calculate_f1(new_path[i], new_path[i+1], new_path[i+2],))
            f2_list.append(calculate_f2(new_path[i+1], obstacle_list))
        f1_list.append(Point(0, 0))
        f2_list.append(Point(0, 0))

        f_total = [f1_list[i]*5+f2_list[i] for i in range(len(f1_list))]
        # 优化力的计算
        f_opti = [Point(0, 0)]
        for i in range(len(f_total)-2):
            dis = Point.distance(new_path[i], new_path[i+2]).evalf()
            u = Point(new_path[i+2]-new_path[i]).evalf()
            dian_cheng = f_total[i+1].x * u.x + f_total[i+1].y + u.y
            f_opti.append(f_total[i+1] - f_total[i+1] * dian_cheng / dis / dis)
        f_opti.append(Point(0, 0))
        new_path = [new_path[i]+f_opti[i] for i in range(len(f1_list))]
        pen2 = draw(new_path)
        pen1.clear()
        pen1 = pen2
    time.sleep(100)


if __name__ == '__main__':
    main()




