import pygame
import math
import sys

# Инициализация Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Cube with Camera and FOV")

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
camera_position = [0, 0, 0]
camera_pitch = 0
camera_yaw = 0
fov = 90

def rotate_point(x, y, z, pitch, yaw):
    # Вращение точки вокруг оси X (pitch)
    cosy = math.cos(pitch)
    siny = math.sin(pitch)
    y2 = y * cosy - z * siny
    z2 = y * siny + z * cosy

    # Вращение вокруг оси Y (yaw)
    cosx = math.cos(yaw)
    sinx = math.sin(yaw)
    x2 = x * cosx + z2 * sinx
    z3 = -x * sinx + z2 * cosx

    return x2, y2, z3

def project_point(point, camera_pos, pitch, yaw, fov, width, height):
    x = point[0] - camera_pos[0]
    y = point[1] - camera_pos[1]
    z = point[2] - camera_pos[2]

    x, y, z = rotate_point(x, y, z, pitch, yaw)

    if z <= 0:
        # Точка за камерой - проекция невозможна
        return None, z

    f = 0.5 * height / math.tan(math.radians(fov) / 2)

    px = (x * f) / z + width / 2
    py = (-y * f) / z + height / 2

    return (int(px), int(py)), z

def normalize(v):
    length = math.sqrt(sum([coord**2 for coord in v]))
    if length == 0:
        return [0,0,0]
    return [coord/length for coord in v]

def cross(a,b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    ]

def main():
    global camera_pitch, camera_yaw, camera_position

    running = True

    move_speed = 0.1

    while running:
        clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    camera_pitch += 0.1
                elif event.key == pygame.K_DOWN:
                    camera_pitch -= 0.1
                elif event.key == pygame.K_LEFT:
                    camera_yaw -= 0.1
                elif event.key == pygame.K_RIGHT:
                    camera_yaw += 0.1

        keys = pygame.key.get_pressed()
        # Вектор взгляда камеры с учетом pitch и yaw
        forward = [
            math.cos(camera_pitch) * math.sin(camera_yaw),
            math.sin(camera_pitch),
            math.cos(camera_pitch) * math.cos(camera_yaw)
        ]
        forward = normalize(forward)

        # Вектор "вправо" - ортогонален вектору forward и вертикальному вектору up = (0,1,0)
        up = [0,1,0]
        right = cross(forward, up)
        right = normalize(right)

        if keys[pygame.K_w]:
            camera_position[0] += forward[0] * move_speed
            camera_position[1] += forward[1] * move_speed
            camera_position[2] += forward[2] * move_speed
        if keys[pygame.K_s]:
            camera_position[0] -= forward[0] * move_speed
            camera_position[1] -= forward[1] * move_speed
            camera_position[2] -= forward[2] * move_speed
        if keys[pygame.K_d]:
            camera_position[0] -= right[0] * move_speed
            camera_position[1] -= right[1] * move_speed
            camera_position[2] -= right[2] * move_speed
        if keys[pygame.K_a]:
            camera_position[0] += right[0] * move_speed
            camera_position[1] += right[1] * move_speed
            camera_position[2] += right[2] * move_speed

        # Проецируем вершины, пропуская точки за камерой
        projected_vertices = []
        depth_list = []

        for v in vertices:
            proj, depth = project_point(v, camera_position, camera_pitch, camera_yaw, fov, WIDTH, HEIGHT)
            projected_vertices.append(proj)
            depth_list.append(depth)

        # Сортируем полигоны по глубине и фильтруем полигоны с вершинами за камерой
        polygons_depth = []
        for poly in polygons:
            # Проверяем что все вершины видимы (z > 0)
            if any(depth_list[i] is None or depth_list[i] <= 0 for i in poly):
                continue
            avg_depth = sum([depth_list[i] for i in poly]) / 3
            polygons_depth.append((avg_depth, poly))

        polygons_depth.sort(key=lambda x: x[0], reverse=True)

        for _, poly in polygons_depth:
            # Все вершины проецированы
            point_list = [projected_vertices[i] for i in poly]
            pygame.draw.polygon(screen, GRAY, point_list)
            pygame.draw.polygon(screen, WHITE, point_list, 1)

        # Отображение информации
        font = pygame.font.SysFont(None, 24)
        instructions = [
            "Arrow keys: rotate camera pitch/yaw",
            "WASD: move camera",
            f"Pitch: {camera_pitch:.2f} rad",
            f"Yaw: {camera_yaw:.2f} rad",
            "Camera Pos: [{:.2f}, {:.2f}, {:.2f}]".format(*camera_position),
            f"FOV: {fov} deg"
        ]
        for i, text in enumerate(instructions):
            rendered = font.render(text, True, WHITE)
            screen.blit(rendered, (10, 10 + i * 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

