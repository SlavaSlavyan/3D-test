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
        return None, z

    f = 0.5 * height / math.tan(math.radians(fov) / 2)

    px = (x * f) / z + width / 2
    py = (-y * f) / z + height / 2

    return (int(px), int(py)), z

def main():
    running = True

    while running:
        clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
            if any(depth_list[i] is None or depth_list[i] <= 0 for i in poly):
                continue
            avg_depth = sum([depth_list[i] for i in poly]) / 3
            polygons_depth.append((avg_depth, poly))

        polygons_depth.sort(key=lambda x: x[0], reverse=True)

        for _, poly in polygons_depth:
            point_list = [projected_vertices[i] for i in poly]
            pygame.draw.polygon(screen, GRAY, point_list)
            pygame.draw.polygon(screen, WHITE, point_list, 1)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
