# -*- encoding=utf-8 -*-
import turtle
from basic_draw_class.basic_draw import *
import time
from math import sqrt

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
        print Fr
        return Fr


def calculate_bubble_max_size_in_p(point, obstacle_tuple):
    t_dis_list = list([P0])
    for obstacle in obstacle_tuple:
        for side in obstacle.sides:
            t_dis = side.distance(point)
            t_dis_list.append(t_dis)
    return min(t_dis_list)


def unit_length(start, direction):
    return Point((direction.x-start.x), (direction.y-start.y))/start.distance(direction)


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
    for p in point_tuple:

        pen.setpos(p.x*basic_mul, p.y*basic_mul)
        pen.dot(10, 'red')
        if isinstance(p, Circle):
            pen.speed(0)
            pen.up()
            pen.forward(p.r*basic_mul)
            pen.left(90)
            pen.down()
            pen.circle(p.r*basic_mul)
            pen.up()
            pen.setpos(p.x*basic_mul, p.y*basic_mul)
            pen.down()

    if close is True:
        pen.setpos(start.x*basic_mul, start.y*basic_mul)
    return pen


def divide_line_into_mul_circle(start, end, obstacle_list):
    # input two point and return a list of circle

    t_length = start.distance(end)
    direction = ((end - start) / end.distance(start))
    m = 0.0
    result_list = list()
    start_p = start
    while m < t_length:
        r = calculate_bubble_max_size_in_p(start_p, obstacle_list)
        result_list.append(Circle(start_p, r))
        m += r
        start_p = start + direction * m
    r = calculate_bubble_max_size_in_p(end, obstacle_list)
    result_list.append(Circle(end, r))
    return result_list


def remove_too_close_point_in_path(path):
    i = 0
    while i < len(path) - 2:
        if path[i].distance(path[i+2]) < 0.8*(path[i].r+path[i+2].r):
            del path[i+1]
        else:
            i += 1
    return path


def add_point_to_path(path, obstacle_list):
    new_path = list()
    for i in range(len(path)-1):
        distance = path[i].distance(path[i+1])
        if distance < path[i].r+path[i+1].r:
            new_path.append(path[i])
            continue
        else:
            m=1
            new_path.append(path[i])
            p = path[i].p + (path[i+1].p-path[i].p)*path[i].r/distance
            new_path.append(Circle(p, calculate_bubble_max_size_in_p(p, obstacle_list)))
    new_path.append(path[-1])
    return new_path


def flush_point_in_path(path, obstacle_list):
    new_path = list()
    for p in path:
        new_path.append(Circle(p, calculate_bubble_max_size_in_p(p, obstacle_list)))
    return new_path


def remove_duplicate_point_in_path(path):
    i = 0
    while i < len(path) - 1:
        if path[i] == path[i+1]:
            del path[i+1]
        else:
            i += 1
    return path


def final_main():
    obstacle = Polygon(Point(-50, -50), Point(-50, 0), Point(0, 20), Point(30, 0), Point(30, -50))
    obstacle_list = list()
    obstacle_list.append(obstacle)
    obstacle = obstacle.translate(100, 100)
    obstacle_list.append(obstacle)
    path = [Point(0, -80), Point(-70, -60), Point(-80, 30), Point(40, 30), Point(40, 20), Point(70, 20)]
    new_path = list()
    for i in range(len(path)-1):
        new_path += divide_line_into_mul_circle(path[i], path[i+1], obstacle_list)

    new_path = remove_duplicate_point_in_path(new_path)
    new_path = remove_too_close_point_in_path(new_path)

    for ob in obstacle_list:
        draw(ob.vertices, True)
    draw(path)
    pen1 = draw(new_path)

    for _ in range(50):
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
            dis = Point.distance(new_path[i], new_path[i+2])
            u = new_path[i+2]-new_path[i]
            dian_cheng = f_total[i+1].dot(u)
            f_opti.append(f_total[i+1] - f_total[i+1] * dian_cheng / dis / dis)
        f_opti.append(Point(0, 0))

        new_path = [Circle(new_path[i]+f_opti[i], 0) for i in range(len(f1_list))]
        new_path = flush_point_in_path(new_path, obstacle_list)
        new_path = remove_duplicate_point_in_path(new_path)
        new_path = remove_too_close_point_in_path(new_path)
        new_path = add_point_to_path(new_path, obstacle_list)


        pen2 = draw(new_path)
        pen1.clear()
        pen1 = pen2
    time.sleep(100)


if __name__ == '__main__':
    final_main()




