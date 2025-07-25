import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Cube with Camera Control")

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
DEBUG_BG = (30, 30, 30)
DEBUG_TEXT_COLOR = (200, 200, 200)

# Font for debug text
font = pygame.font.SysFont("consolas", 14)

# Cube vertices (x, y, z)
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

# Cube faces (each face is a list of indices to vertices)
cube_faces = [
    (0, 1, 3, 2),  # left
    (4, 6, 7, 5),  # right
    (0, 4, 5, 1),  # bottom
    (2, 3, 7, 6),  # top
    (0, 2, 6, 4),  # back
    (1, 5, 7, 3),  # front
]

# Face colors
face_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
]

# Camera class that stores position and rotation (yaw, pitch, roll)
class Camera:
    def __init__(self, pos=(0, 0, -5), yaw=0, pitch=0, roll=0):
        self.x, self.y, self.z = pos
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def get_rotation_matrix(self):
        # Convert degrees to radians
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        roll_rad = math.radians(self.roll)

        # Rotation matrices around each axis
        cy = math.cos(yaw_rad)
        sy = math.sin(yaw_rad)
        cp = math.cos(pitch_rad)
        sp = math.sin(pitch_rad)
        cr = math.cos(roll_rad)
        sr = math.sin(roll_rad)

        # Combined rotation matrix R = Rroll * Rpitch * Ryaw
        # Roll
        Rr = [
            [cr, -sr, 0],
            [sr, cr,  0],
            [0,  0,   1]
        ]
        # Pitch
        Rp = [
            [1,  0,   0],
            [0,  cp, -sp],
            [0,  sp,  cp]
        ]
        # Yaw
        Ry = [
            [cy, 0, sy],
            [0,  1, 0],
            [-sy,0, cy]
        ]

        # Multiply matrices: R = Rr * Rp * Ry
        def mat_mult(A, B):
            result = [[0,0,0],[0,0,0],[0,0,0]]
            for i in range(3):
                for j in range(3):
                    result[i][j] = A[i][0]*B[0][j] + A[i][1]*B[1][j] + A[i][2]*B[2][j]
            return result

        RpRy = mat_mult(Rp, Ry)
        R = mat_mult(Rr, RpRy)
        return R

    def rotate_point(self, point):
        # Rotate point according to camera rotation
        R = self.get_rotation_matrix()

        x = point[0]
        y = point[1]
        z = point[2]

        xr = R[0][0]*x + R[0][1]*y + R[0][2]*z
        yr = R[1][0]*x + R[1][1]*y + R[1][2]*z
        zr = R[2][0]*x + R[2][1]*y + R[2][2]*z

        return (xr, yr, zr)

    def world_to_camera(self, point):
        # Translate world point relative to camera position
        px = point[0] - self.x
        py = point[1] - self.y
        pz = point[2] - self.z

        # Rotate according to camera rotation
        return self.rotate_point((px, py, pz))

    def move(self, dx, dy, dz):
        self.x += dx
        self.y += dy
        self.z += dz


# Projection function (perspective)
def project(point):
    # Simple perspective projection
    fov = 90
    aspect_ratio = WIDTH / HEIGHT
    near = 0.1
    far = 1000

    fov_rad = 1 / math.tan(math.radians(fov) / 2)

    x, y, z = point

    if z == 0:
        z = 0.0001  # To prevent division by zero

    px = (x * fov_rad / aspect_ratio) / (z if z != 0 else 1)
    py = (y * fov_rad) / (z if z != 0 else 1)

    # Convert to screen coordinates
    screen_x = int((px + 1) * WIDTH / 2)
    screen_y = int((1 - py) * HEIGHT / 2)  # y is inverted on the screen

    return screen_x, screen_y


# Normalize a vector
def normalize(v):
    length = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    if length == 0:
        return (0, 0, 0)
    return (v[0]/length, v[1]/length, v[2]/length)

# Cross product of two vectors
def cross(v1, v2):
    return (v1[1]*v2[2] - v1[2]*v2[1],
            v1[2]*v2[0] - v1[0]*v2[2],
            v1[0]*v2[1] - v1[1]*v2[0])

# Vector addition
def vec_add(v1, v2):
    return (v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2])

# Vector subtraction
def vec_sub(v1, v2):
    return (v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2])

# Vector scale
def vec_scale(v, s):
    return (v[0]*s, v[1]*s, v[2]*s)

# Get camera direction vectors for movement relative to yaw and pitch (ignoring roll for movement)
def get_camera_direction_vectors(camera):
    yaw_rad = math.radians(camera.yaw)
    pitch_rad = math.radians(camera.pitch)

    # Forward vector (camera look vector ignoring roll)
    forward = (math.sin(yaw_rad)*math.cos(pitch_rad), -math.sin(pitch_rad), math.cos(yaw_rad)*math.cos(pitch_rad))
    forward = normalize(forward)

    # Right vector (perpendicular to forward, ignoring y)
    up_vector = (0, 1, 0)
    right = cross(forward, up_vector)
    right = normalize(right)

    # Recompute forward vector to be perpendicular to right and up
    forward = cross(up_vector, right)
    forward = normalize(forward)

    return forward, right

def main():
    clock = pygame.time.Clock()
    camera = Camera()

    running = True

    move_speed = 0.1
    rot_speed = 2

    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Camera rotation control
        if keys[pygame.K_RIGHT]:
            camera.yaw -= rot_speed
        if keys[pygame.K_LEFT]:
            camera.yaw += rot_speed
        if keys[pygame.K_UP]:
            camera.pitch -= rot_speed
            if camera.pitch < -89:
                camera.pitch = -89
        if keys[pygame.K_DOWN]:
            camera.pitch += rot_speed
            if camera.pitch > 89:
                camera.pitch = 89

        if keys[pygame.K_q]:
            camera.roll -= rot_speed
        if keys[pygame.K_e]:
            camera.roll += rot_speed

        # Movement relative to camera direction (x and z only)
        forward, right = get_camera_direction_vectors(camera)

        move_vec = (0.0, 0.0, 0.0)

        if keys[pygame.K_w]:
            camera.x -= math.sin(camera.yaw/180*math.pi) / 20
            camera.z += math.cos(camera.yaw/180*math.pi) / 20
        if keys[pygame.K_s]:
            camera.x += math.sin(camera.yaw/180*math.pi) / 20
            camera.z -= math.cos(camera.yaw/180*math.pi) / 20
        if keys[pygame.K_a]:
            camera.x -= math.cos(camera.yaw/180*math.pi) / 20
            camera.z -= math.sin(camera.yaw/180*math.pi) / 20
        if keys[pygame.K_d]:
            camera.x += math.cos(camera.yaw/180*math.pi) / 20
            camera.z += math.sin(camera.yaw/180*math.pi) / 20

        # Vertical movement
        if keys[pygame.K_SPACE]:
            move_vec = vec_add(move_vec, (0, move_speed, 0))
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            move_vec = vec_add(move_vec, (0, -move_speed, 0))

        # Apply movement
        camera.move(move_vec[0], move_vec[1], move_vec[2])

        # Clear screen
        screen.fill(BLACK)

        # Draw cube
        # Transform cube vertices to camera space and project to 2D
        projected_vertices = []
        for vertex in cube_vertices:
            # World to camera space
            cam_point = camera.world_to_camera(vertex)
            # Cull points behind camera (simple)
            if cam_point[2] <= 0:
                projected_vertices.append(None)
            else:
                p = project(cam_point)
                projected_vertices.append(p)

        # Draw faces with simple painter's algorithm (sort faces by avg depth)
        face_depth = []
        for i, face in enumerate(cube_faces):
            z_max = float('-inf')  # Start with the smallest possible value
            valid = True
            for idx in face:
                if projected_vertices[idx] is None:
                    valid = False
                    break
                world_v = camera.world_to_camera(cube_vertices[idx])
                z_max = max(z_max, world_v[2])  # Use the maximum z value
            if not valid:
                continue
            face_depth.append((z_max, i))  # Store the max z value for sorting

        face_depth.sort(reverse=True)  # Sort by max z value

        for _, i in face_depth:
            face = cube_faces[i]
            point_list = [projected_vertices[idx] for idx in face]
            if None in point_list:
                continue
            pygame.draw.polygon(screen, face_colors[i], point_list)
            pygame.draw.polygon(screen, BLACK, point_list, 1)  # black border


        # Draw debug info box
        debug_rect = pygame.Rect(WIDTH - 220, 10, 210, 100)
        pygame.draw.rect(screen, DEBUG_BG, debug_rect)
        pygame.draw.rect(screen, GRAY, debug_rect, 1)

        debug_lines = [
            f"Camera Position:",
            f"x: {camera.x:.2f}",
            f"y: {camera.y:.2f}",
            f"z: {camera.z:.2f}",
            f"Yaw: {camera.yaw:.1f}",
            f"Pitch: {camera.pitch:.1f}",
            f"Roll: {camera.roll:.1f}",
            "Controls:",
            "WASD - Move (relative to camera)",
            "Space - Up, Shift - Down",
            "Arrows - Yaw/Pitch",
            "Q/E - Roll",
        ]

        for i, line in enumerate(debug_lines):
            text_surface = font.render(line, True, DEBUG_TEXT_COLOR)
            screen.blit(text_surface, (WIDTH - 210, 15 + i*12))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

