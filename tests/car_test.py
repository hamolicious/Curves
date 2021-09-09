from math import radians
from vector import Vec2d
from curves import CubicBezier
import pygame
from time import time
from random import randint

#region pygame init
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion

# curve = CubicBezier([32, 571], [45, 27], [552, 561], [574, 24])
buffer = 100
curve = CubicBezier([buffer, buffer], [buffer, size[1]-buffer], [size[0]-buffer, size[1]-buffer], [size[0]-buffer, buffer])
curve.resolution = 100

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

# create cars
class Car:
	def __init__(self, speed=0.1) -> None:
		self.speed = speed + (randint(0, 10) / 100)
		self.pos = randint(0, 100) / 100 # [0, 1] range (t)

		self.verts = [
			Vec2d(-1, -0.5),
			Vec2d( 1, -0.5),
			Vec2d( 1,  0.5),
			Vec2d(-1,  0.5),
		]
		self.size = 10

	def update(self, delta_time):
		self.pos += self.speed * delta_time

		if self.pos >= 1:
			self.pos = 0

	def display(self, screen, curve: CubicBezier):
		new_verts = [i * self.size for i in self.verts]
		pos = curve.calculate_point(self.pos)
		vel = curve.calculate_direction(self.pos)
		rot = vel.get_heading_angle()

		verts = []
		for v in new_verts:
			v.rotate(-(rot - radians(90)))
			v.add(pos)
			verts.append(v.get_int())

		pygame.draw.polygon(screen, [255, 255, 255], verts, 0)

		#NOTE uncomment to display direction lines
		# p = Vec2d()
		# for v in verts:
		# 	p.add(v)
		# p.div(len(verts))

		# vel.mult(50)
		# pygame.draw.line(screen, [51, 51, 51], p.get_int(), (p + vel).get_int())

cars = [Car() for _ in range(10)]

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

	curve.display(screen, line_thickness=5)
	pygame.draw.polygon(screen, [255, 0, 0], points, 0)

	for car in cars:
		car.update(delta_time)
		car.display(screen, curve)

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')
