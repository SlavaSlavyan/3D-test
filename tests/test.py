import pygame
import math
import sys

# Настройки экрана
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CUBE_COLOR = (0, 255, 0)

# Настройки камеры
CAMERA_POS = [0.0, 0.0, -5.0]  # стартовая позиция камеры
CAMERA_ANGLE = [0.0, 0.0, 0.0]  # pitch, yaw, roll (градусы)

MOVE_SPEED = 0.1
ROTATE_SPEED = 2.0


def rotation_matrix(pitch, yaw, roll):
    """Создать матрицу поворота из углов (в градусах) pitch, yaw, roll."""
    # Переводим углы в радианы
    pitch = math.radians(pitch)
    yaw = math.radians(yaw)
    roll = math.radians(roll)

    # Матрица поворота вокруг X (pitch)
    Rx = [
        [1, 0, 0],
        [0, math.cos(pitch), -math.sin(pitch)],
        [0, math.sin(pitch), math.cos(pitch)]
    ]

    # Матрица поворота вокруг Y (yaw)
    Ry = [
        [math.cos(yaw), 0, math.sin(yaw)],
        [0, 1, 0],
        [-math.sin(yaw), 0, math.cos(yaw)]
    ]

    # Матрица поворота вокруг Z (roll)
    Rz = [
        [math.cos(roll), -math.sin(roll), 0],
        [math.sin(roll), math.cos(roll), 0],
        [0, 0, 1]
    ]

    # Итоговая матрица = Rz * Ry * Rx (roll, затем yaw, затем pitch)
    Rzy = matrix_multiply(Rz, Ry)
    R = matrix_multiply(Rzy, Rx)
    return R


def matrix_multiply(A, B):
    """Умножение 3x3 матриц A и B."""
    result = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            s = 0
            for k in range(3):
                s += A[i][k]*B[k][j]
            result[i][j] = s
    return result


def vector_matrix_multiply(vec, mat):
    """Умножить вектор (x,y,z) на матрицу 3x3."""
    x = vec[0]*mat[0][0] + vec[1]*mat[0][1] + vec[2]*mat[0][2]
    y = vec[0]*mat[1][0] + vec[1]*mat[1][1] + vec[2]*mat[1][2]
    z = vec[0]*mat[2][0] + vec[1]*mat[2][1] + vec[2]*mat[2][2]
    return (x, y, z)


def transform_point(point, camera_pos, camera_rot_mat):
    """Трансформировать точку из мировых координат в координаты камеры."""
    # Сдвинуть точку относительно камеры
    x = point[0] - camera_pos[0]
    y = point[1] - camera_pos[1]
    z = point[2] - camera_pos[2]
    translated = (x, y, z)

    # Повернуть точку в обратную сторону (инверсия поворота камеры)
    # Для инвертирования матрицы поворота используем транспонирование (для ортонормальной матрицы)
    R_inv = [
        [camera_rot_mat[0][0], camera_rot_mat[1][0], camera_rot_mat[2][0]],
        [camera_rot_mat[0][1], camera_rot_mat[1][1], camera_rot_mat[2][1]],
        [camera_rot_mat[0][2], camera_rot_mat[1][2], camera_rot_mat[2][2]]
    ]
    rotated = vector_matrix_multiply(translated, R_inv)
    return rotated


def project_point(point, width, height, fov, viewer_distance):
    """Перспективная проекция 3D точки на 2D плоскость"""
    x, y, z = point
    if z <= 0.1:
        return None
    factor = fov / (viewer_distance + z)
    x_proj = x * factor + width / 2
    y_proj = -y * factor + height / 2
    return (int(x_proj), int(y_proj))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Cube Projection with Full Camera Rotation")
    clock = pygame.time.Clock()

    cube_vertices = [
        (-1, -1, -1),
        (-1, -1,  1),
        (-1,  1, -1),
        (-1,  1,  1),
        (1, -1, -1),
        (1, -1,  1),
        (1,  1, -1),
        (1,  1,  1),
    ]

    edges = [
        (0, 1), (0, 2), (0, 4),
        (1, 3), (1, 5),
        (2, 3), (2, 6),
        (3, 7),
        (4, 5), (4, 6),
        (5, 7),
        (6, 7)
    ]

    fov = 256
    viewer_distance = 4

    camera_pos = CAMERA_POS[:]
    camera_angle = CAMERA_ANGLE[:]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Клавиши для наклонов камеры (pitch и roll)
        if keys[pygame.K_UP]:
            camera_angle[0] += ROTATE_SPEED  # pitch вверх
            if camera_angle[0] > 89:
                camera_angle[0] = 89
        if keys[pygame.K_DOWN]:
            camera_angle[0] -= ROTATE_SPEED  # pitch вниз
            if camera_angle[0] < -89:
                camera_angle[0] = -89
        if keys[pygame.K_q]:
            camera_angle[2] += ROTATE_SPEED  # roll против часовой
        if keys[pygame.K_e]:
            camera_angle[2] -= ROTATE_SPEED  # roll по часовой

        # Клавиши для поворота камеры вокруг вертикальной оси (yaw)
        if keys[pygame.K_LEFT]:
            camera_angle[1] += ROTATE_SPEED  # yaw влево
        if keys[pygame.K_RIGHT]:
            camera_angle[1] -= ROTATE_SPEED  # yaw вправо

        # Получаем матрицу поворота камеры по pitch, yaw, roll
        rot_mat = rotation_matrix(camera_angle[0], camera_angle[1], camera_angle[2])

        # Векторы направления (локальные оси)
        forward = vector_matrix_multiply((0, 0, 1), rot_mat)
        right = vector_matrix_multiply((1, 0, 0), rot_mat)
        up = vector_matrix_multiply((0, 1, 0), rot_mat)

        # Движение камеры относительно направления (WASD)
        move_vec = [0, 0, 0]
        if keys[pygame.K_w]:
            move_vec[0] += MOVE_SPEED  # вперед (локальная ось Z)
        if keys[pygame.K_s]:
            move_vec[0] -= MOVE_SPEED  # назад
        if keys[pygame.K_d]:
            move_vec[2] += MOVE_SPEED  # вправо (локальная ось X)
        if keys[pygame.K_a]:
            move_vec[2] -= MOVE_SPEED  # влево
        if keys[pygame.K_r]:
            move_vec[1] += MOVE_SPEED  # вверх (локальная ось Y)
        if keys[pygame.K_f]:
            move_vec[1] -= MOVE_SPEED  # вниз

        # Применяем движение к позиции камеры
        camera_pos[0] += forward[0] * move_vec[0] + up[0] * move_vec[1] + right[0] * move_vec[2]
        camera_pos[1] += forward[1] * move_vec[0] + up[1] * move_vec[1] + right[1] * move_vec[2]
        camera_pos[2] += forward[2] * move_vec[0] + up[2] * move_vec[1] + right[2] * move_vec[2]

        screen.fill(BLACK)

        projected_points = []
        for vertex in cube_vertices:
            transformed = transform_point(vertex, camera_pos, rot_mat)
            projected = project_point(transformed, WIDTH, HEIGHT, fov, viewer_distance)
            projected_points.append(projected)

        for edge in edges:
            start, end = edge
            p1 = projected_points[start]
            p2 = projected_points[end]
            if p1 is not None and p2 is not None:
                pygame.draw.line(screen, CUBE_COLOR, p1, p2, 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

