import pygame
import math
import sys

# Инициализация Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Cube")

clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Куб - вершины в локальных координатах (x, y, z)
vertices = [
    (-1, -1, -1), # 0
    (-1, -1,  1), # 1
    (-1,  1, -1), # 2
    (-1,  1,  1), # 3
    (1, -1, -1),  # 4
    (1, -1,  1),  # 5
    (1,  1, -1),  # 6
    (1,  1,  1),  # 7
]

# Полигоны - стороны куба (треугольники)
polygons = [
    (0, 1, 3), (0, 3, 2),  # левая сторона
    (4, 6, 7), (4, 7, 5),  # правая сторона
    (0, 4, 5), (0, 5, 1),  # низ
    (2, 3, 7), (2, 7, 6),  # верх
    (1, 5, 7), (1, 7, 3),  # перед
    (0, 2, 6), (0, 6, 4),  # задняя
]

# Камера
camera_position = [0, 0, -5]  # Отодвинули назад, чтобы видеть куб сразу
camera_pitch = 0.0
camera_yaw = 0.0
camera_roll = 0.0
fov = 90

camera_input = False

MOUSE_SENSITIVITY = 0.005
MOVE_SPEED = 0.1
ROLL_SPEED = 0.03

def rotate_point(x, y, z, pitch, yaw, roll):
    # Вращение вокруг оси Y (yaw)
    cosy = math.cos(yaw)
    siny = math.sin(yaw)
    x1 = x * cosy + z * siny
    z1 = -x * siny + z * cosy

    # Вращение вокруг оси X (pitch)
    cosp = math.cos(pitch)
    sinp = math.sin(pitch)
    y1 = y * cosp - z1 * sinp
    z2 = y * sinp + z1 * cosp

    # Вращение вокруг оси Z (roll)
    cosr = math.cos(roll)
    sinr = math.sin(roll)
    x2 = x1 * cosr - y1 * sinr
    y2 = x1 * sinr + y1 * cosr

    return x2, y2, z2

def project_point(point, camera_pos, pitch, yaw, roll, fov, width, height):
    x = point[0] - camera_pos[0]
    y = point[1] - camera_pos[1]
    z = point[2] - camera_pos[2]

    x, y, z = rotate_point(x, y, z, pitch, yaw, roll)

    if z <= 0:
        return None, z

    f = 0.5 * height / math.tan(math.radians(fov) / 2)

    px = (x * f) / z + width / 2
    py = (-y * f) / z + height / 2

    return (int(px), int(py)), z

def clamp(value, minv, maxv):
    return max(minv, min(value, maxv))

def main():
    global camera_input, camera_pitch, camera_position, camera_yaw, camera_roll, fov

    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)

    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # delta time в секундах
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    camera_input = not camera_input
                    pygame.event.set_grab(camera_input)
                    pygame.mouse.set_visible(not camera_input)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # прокрутка колесика вверх
                    fov = max(10, fov - 1)  # Заzoom in (уменьшаем FOV)
                elif event.button == 5:  # прокрутка колесика вниз
                    fov = min(150, fov + 1)  # Заzoom out (увеличиваем FOV)

        keys = pygame.key.get_pressed()

        # Рассчитываем вектор взгляда камеры (направление вперед)
        sin_yaw = math.sin(camera_yaw)
        cos_yaw = math.cos(camera_yaw)
        sin_pitch = math.sin(camera_pitch)
        cos_pitch = math.cos(camera_pitch)

        forward = [
            cos_pitch * sin_yaw,
            -sin_pitch,
            cos_pitch * cos_yaw
        ]

        # Вектор "вправо" как кросс продукт мировой оси Y (0,1,0) и forward
        right = [
            cos_yaw,
            0,
            -sin_yaw
        ]

        # Вверх - мировая ось Y
        up = [0,1,0]

        # Управление движением камеры
        if keys[pygame.K_w]:
            camera_position[0] += forward[0] * MOVE_SPEED
            camera_position[1] += forward[1] * MOVE_SPEED
            camera_position[2] += forward[2] * MOVE_SPEED

        if keys[pygame.K_s]:
            camera_position[0] -= forward[0] * MOVE_SPEED
            camera_position[1] -= forward[1] * MOVE_SPEED
            camera_position[2] -= forward[2] * MOVE_SPEED

        if keys[pygame.K_a]:
            camera_position[0] -= right[0] * MOVE_SPEED
            camera_position[1] -= right[1] * MOVE_SPEED
            camera_position[2] -= right[2] * MOVE_SPEED

        if keys[pygame.K_d]:
            camera_position[0] += right[0] * MOVE_SPEED
            camera_position[1] += right[1] * MOVE_SPEED
            camera_position[2] += right[2] * MOVE_SPEED

        if keys[pygame.K_SPACE]:  # вверх
            camera_position[1] += MOVE_SPEED

        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:  # вниз
            camera_position[1] -= MOVE_SPEED

        # Управление поворотом ролл (наклон головы) через Q/E
        if keys[pygame.K_q]:
            camera_roll -= ROLL_SPEED
        if keys[pygame.K_e]:
            camera_roll += ROLL_SPEED

        # Управление обзором мышью при активном режиме camera_input
        if camera_input:
            mx, my = pygame.mouse.get_rel()
            camera_yaw += mx * MOUSE_SENSITIVITY
            camera_pitch += -my * MOUSE_SENSITIVITY
            camera_pitch = clamp(camera_pitch, -math.pi/2 + 0.01, math.pi/2 - 0.01)

        # Проецируем вершины, пропуская точки за камерой
        projected_vertices = []
        depth_list = []

        for v in vertices:
            proj, depth = project_point(v, camera_position, camera_pitch, camera_yaw, camera_roll, fov, WIDTH, HEIGHT)
            projected_vertices.append(proj)
            depth_list.append(depth)

        # Сортируем полигоны по глубине и фильтруем полигоны с вершинами за камерой
        polygons_depth = []
        for poly in polygons:
            if any(depth_list[i] is None or depth_list[i] <= 0 for i in poly):
                continue
            avg_depth = sum([depth_list[i] for i in poly]) / 3
            polygons_depth.append((avg_depth, poly))

        polygons_depth.sort(key=lambda x: x[0], reverse=True)

        for _, poly in polygons_depth:
            point_list = [projected_vertices[i] for i in poly]
            try:
                pygame.draw.polygon(screen, GRAY, point_list)
                pygame.draw.polygon(screen, WHITE, point_list, 1)
            except:
                pass

        # Отображение информации
        font = pygame.font.SysFont(None, 24)
        instructions = [
            f"Pitch: {camera_pitch:.2f} rad",
            f"Yaw: {camera_yaw:.2f} rad",
            f"Roll: {camera_roll:.2f} rad",
            "Camera Pos: [{:.2f}, {:.2f}, {:.2f}]".format(*camera_position),
            f"FOV: {fov} deg",
        ]
        for i, text in enumerate(instructions):
            rendered = font.render(str(text), True, WHITE)
            screen.blit(rendered, (10, 10 + i * 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

