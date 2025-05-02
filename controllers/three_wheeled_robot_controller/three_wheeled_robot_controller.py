from controller import Robot
import time
from turn_utils import initialize_turn, turn_90_degrees 
# Инициализация робота
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Подключение устройств
rear_motor = robot.getDevice('rear_motor')  # Задний мотор
right_motor2 = robot.getDevice('right_motor2')  # Правое колесо для движения
left_motor2 = robot.getDevice('left_motor2')  # Левое колесо для движения
right_motor1 = robot.getDevice('right_motor1')  # Правое колесо для поворота
left_motor1 = robot.getDevice('left_motor1')  # Левое колесо для поворота

rear_motor.setVelocity(0.0)
right_motor2.setVelocity(0.0)
left_motor2.setVelocity(0.0)

initialize_turn(rear_motor, right_motor2, left_motor2, right_motor1, left_motor1)

velocity = 5.0  # Можно настроить на нужную скорость

# Функция для расчета времени на преодоление 1 метра
def move_one_meter():
    distance_travelled = 0.0
    start_time = robot.getTime()  # Начало отсчета времени
    rear_motor.setVelocity(velocity)
    right_motor2.setVelocity(velocity)
    left_motor2.setVelocity(velocity)
    
    while distance_travelled < 8.0:  # Пока не пройдено 1 метр
        robot.step(timestep)
        distance_travelled = velocity * (robot.getTime() - start_time)
    
    end_time = robot.getTime()  # Время, когда робот проехал 1 метр
    print(f"Время для проезда 1 метра: {end_time - start_time} секунд")
    # Остановить моторы после прохождения 1 метра
    rear_motor.setVelocity(0.0)
    right_motor2.setVelocity(0.0)
    left_motor2.setVelocity(0.0)

# Основной цикл
print("Запуск робота.")

import random

# Карта (известная заранее)
grid_map = [
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0,'B',1,'A',1, 1, 0, 0, 0],
]

# Координаты старта (A) и цели (B)
start = (9, 4)  # Координаты A
goal = (9, 2)  # Координаты B

# Параметры генетического алгоритма
POPULATION_SIZE = 100
MUTATION_RATE = 0.05
MAX_PATH_LENGTH = 20  # Реалистичное ограничение

# Возможные шаги: вправо, влево, вверх, вниз
MOVES = [(0, 1), (0, -1), (-1, 0), (1, 0)]


# Проверка допустимости позиции
def is_valid_position(x, y):
    return 0 <= x < len(grid_map) and 0 <= y < len(grid_map[0]) and grid_map[x][y] != 1


# Удаление петель из маршрута
def remove_loops(route):
    visited = set()
    x, y = start
    optimized_route = []

    for dx, dy in route:
        next_position = (x + dx, y + dy)
        if next_position in visited or not is_valid_position(next_position[0], next_position[1]):
            continue
        visited.add(next_position)
        optimized_route.append((dx, dy))
        x, y = next_position

        if next_position == goal:
            break

    return optimized_route


# Функция для оценки пути
def fitness(route):
    route = remove_loops(route)  # Удаляем петли перед оценкой
    x, y = start
    total_distance = len(route)
    penalty = 0

    for dx, dy in route:
        x += dx
        y += dy

        if not is_valid_position(x, y):
            penalty += 100
            break

        if (x, y) == goal:
            return 1000 - total_distance

    penalty += abs(goal[0] - x) + abs(goal[1] - y)
    return -penalty


# Создание начальной популяции
def initialize_population():
    population = []
    for _ in range(POPULATION_SIZE):
        route = []
        x, y = start
        while len(route) < MAX_PATH_LENGTH:
            dx, dy = random.choice(MOVES)
            if is_valid_position(x + dx, y + dy):
                x += dx
                y += dy
                route.append((dx, dy))
                if (x, y) == goal:
                    break
        population.append(route)
    return population


# Селекция: турнирный отбор
def select_parent(population):
    tournament = random.sample(population, 5)
    tournament.sort(key=fitness, reverse=True)
    return tournament[0]


# Кроссовер (одноточечный)
def crossover(parent1, parent2):
    split = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    return child1, child2


# Мутация
def mutate(route):
    for i in range(len(route)):
        if random.random() < MUTATION_RATE:
            route[i] = random.choice(MOVES)
    return route


# Проверка завершения маршрута
def is_goal_reached(route):
    x, y = start
    for dx, dy in route:
        x += dx
        y += dy
        if not is_valid_position(x, y):
            return False
        if (x, y) == goal:
            return True
    return False


# Генетический алгоритм
def genetic_algorithm():
    population = initialize_population()
    generation = 0

    while True:  # Работает до тех пор, пока не найдется решение
        generation += 1
        population = sorted(population, key=fitness, reverse=True)

        best_route = max(population, key=fitness)
        print(
            f"Поколение {generation}: Лучшая длина пути = {len(remove_loops(best_route))}, Приспособленность = {fitness(best_route)}")
        if generation  == 50 and fitness(best_route) > 0:
            print(f"Цель достигнута за {generation} поколений!")
            return remove_loops(best_route)

        if is_goal_reached(best_route):
            print(f"Цель достигнута за {generation} поколений!")
            return remove_loops(best_route)

        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])

        population = new_population


# Вывод карты без пути
def display_initial_map():
    print("\nНачальная карта:")
    for row in grid_map:
        print(" ".join(str(cell) for cell in row))


# Вывод карты с маршрутом
def display_map_with_path(route):
    map_with_path = [row[:] for row in grid_map]
    x, y = start

    for dx, dy in route:
        x += dx
        y += dy
        if not is_valid_position(x, y):
            break
        if (x, y) == goal:
            break
        map_with_path[x][y] = 'X'

    map_with_path[start[0]][start[1]] = 'A'
    map_with_path[goal[0]][goal[1]] = 'B'

    print("\nКарта с маршрутом:")
    for row in map_with_path:
        print(" ".join(str(cell) for cell in row))


# Запуск алгоритма
display_initial_map()  # Вывод начальной карты
best_path = genetic_algorithm()
print("Лучший найденный путь:", best_path)

# Вычисление конечной позиции и вывод карты с путём
final_position = (start[0], start[1])
for dx, dy in best_path:
    final_position = (final_position[0] + dx, final_position[1] + dy)
    if final_position == goal:
        break

print(f"Финишная позиция: {final_position}")
display_map_with_path(best_path)

def execute_path(path):
    previous_step = None
    looking_up = True  # Начальное направление "смотрит вверх"

    for i, step in enumerate(path):
        next_step = path[i + 1] if i + 1 < len(path) else None

        if step == (-1, 0):  # Движение вперёд
            move_one_meter()
            looking_up = True
        elif step == (0, 1):  # Поворот влево, движение, поворот вправо
            if previous_step != (0, 1):
                turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='left')
            move_one_meter()
            if previous_step != (0, 1) and next_step != (0, 1):
                turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='right')
            looking_up = False
        elif step == (0, -1):  # Поворот вправо, движение, поворот влево
            if previous_step != (0, -1):
                turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='right')
            move_one_meter()
            if previous_step != (0, -1) and next_step != (0, -1):
                turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='left')
            looking_up = False
        elif step == (1, 0):  # Движение вниз
            if previous_step != (1, 0):
                if looking_up:
                    turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='left')
                    turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='left')
                elif previous_step == (0, 1):  # Если смотрели вправо
                    turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='left')
                elif previous_step == (0, -1):  # Если смотрели влево
                    turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='right')
            move_one_meter()
            if previous_step != (1, 0) and next_step != (1, 0):
                turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='left')
                turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='left')
            looking_up = False

        previous_step = step




execute_path(best_path)
