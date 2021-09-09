from math import radians
from vector import Vec2d
from curves.bezier import CubicBezier
import pygame
from time import time

#region pygame init
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion

curve = CubicBezier([32, 571], [45, 27], [552, 561], [574, 24])

# generate road
right_points = []
left_points = []
road_width = 50

for t_int in range(0, curve.resolution+1):
	t = t_int / curve.resolution

	direction = curve.calculate_direction(t)
	left_point = curve.calculate_normal(direction)
	position = curve.calculate_point(t)

	left_point.mult(road_width/2)
	right_point = left_point.copy()
	right_point.rotate(radians(180))

	right_point.add(position)
	left_point.add(position)

	right_points.append(right_point.get_int())
	left_points.append(left_point.get_int())

points = right_points + left_points[::-1]


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
	frame_start_time = time()
	screen.fill(0)
	mouse_pos   = Vec2d(pygame.mouse.get_pos())
	mouse_press = pygame.mouse.get_pressed()
	key_press   = pygame.key.get_pressed()

	curve.display_controll_points(screen)
	curve.display(screen, line_thickness=5)

	pygame.draw.polygon(screen, [255, 0, 0], points, 0)

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')
