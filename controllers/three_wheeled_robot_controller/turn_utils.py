import math
import time

velocity = 4.0



def initialize_turn(rear_motor, right_motor2, left_motor2, right_motor1, left_motor1):
    # Общие параметры для поворота
    global turn_speed, turn_duration
    turn_speed = 2.0  # Скорость поворота
    turn_duration = 3.2  # Длительность поворота для 90 градусов

    # Инициализация моторов
    rear_motor.setPosition(float('inf'))
    right_motor2.setPosition(float('inf'))
    left_motor2.setPosition(float('inf'))

    print("Поворотные параметры и моторы инициализированы.")

# Функция для поворота на 90 градусов
def turn_90_degrees(robot, timestep, rear_motor, right_motor2, left_motor2, right_motor1, left_motor1, direction='right'):
    # Поворот передних колёс
    if direction == 'right':
        right_motor1.setPosition(math.pi / 2)  # Поворачиваем вправо
        left_motor1.setPosition(math.pi / 2)  # Поворачиваем влево
        rear_motor.setVelocity(4.0)
    elif direction == 'left':
        right_motor1.setPosition(-math.pi / 2)  # Поворачиваем влево
        left_motor1.setPosition(-math.pi / 2)  # Поворачиваем вправо
        rear_motor.setVelocity(4.0)

    # Вращение заднего колеса для поворота
    rear_motor.setVelocity(0.0)
    right_motor2.setVelocity(turn_speed)
    left_motor2.setVelocity(-turn_speed)

    # Засекаем время для поворота
    start_time = robot.getTime()
    while robot.step(timestep) != -1:
        current_time = robot.getTime()
        if current_time - start_time >= turn_duration:  # Проверяем, сколько прошло времени
            break

    # Полная остановка после поворота
    rear_motor.setVelocity(0.0)
    right_motor2.setVelocity(0.0)
    left_motor2.setVelocity(0.0)
    right_motor1.setPosition(0.0)
    left_motor1.setPosition(0.0)
    print(f"Поворот на 90 градусов {direction} завершён.")

    # Даем команду двигаться назад еще 2 секунды
    # Движение назад
    rear_motor.setVelocity(0.0)  # Отрицательная скорость для движения назад
    right_motor2.setVelocity(0.0)
    left_motor2.setVelocity(0.0)

    # Засекаем время для движения назад
    back_start_time = robot.getTime()
    while robot.step(timestep) != -1:
        if robot.getTime() - back_start_time >= 2:  # 2 секунды назад
            break

    # Останавливаем робота
    rear_motor.setVelocity(0.0)
    right_motor2.setVelocity(0.0)
    left_motor2.setVelocity(0.0)
    print("Робот остановился после движения назад.")
