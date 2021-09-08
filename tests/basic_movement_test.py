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

buffer = 100
curve = CubicBezier([buffer, buffer], [buffer, size[1]-buffer], [size[0]-buffer, size[1]-buffer], [size[0]-buffer, buffer])
curve.resolution = 100

selected = None

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

	for p in [curve.p1, curve.p2, curve.p3, curve.p4]:
		if mouse_pos.dist(p.pos) <= p.radius**2:
			if mouse_press[0]:
				selected = p
				break

			if not mouse_press[0]:
				selected = None

	if selected is not None:
		selected.pos.set(mouse_pos)

	curve.update(mouse_pos, mouse_press)
	curve.display(screen, draw_controll_points=True, draw_line_points=True, draw_lines=True)

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')
