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
curve.resolution = 100

t = 0
delta_t = 0.3

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

	t += delta_t * delta_time
	if t > 1:
		t = 1
		delta_t *= -1
	if t < 0:
		t = 0
		delta_t *= -1

	curve.update(t_range=[0, t])
	curve.display(screen, line_thickness=5)

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')
