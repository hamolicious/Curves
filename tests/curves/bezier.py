from math import radians
import pygame
from vector import Vec2d, Color
from curves.points import Point

class CubicBezier:
	def __init__(self, p1, p2, p3, p4) -> None:
		self.p1 = Point(p1)
		self.p2 = Point(p2)
		self.p3 = Point(p3)
		self.p4 = Point(p4)

		self.resolution = 100

		self.color = Color(255)

		self.__points = []

	def update(self, mouse_pos, mouse_press):
		pass

	def calculate_point(self, t):
		p = Vec2d.zero()
		p.add(self.p1.pos * (-t**3 + 3 * t**2 - 3 * t + 1))
		p.add(self.p2.pos * (3 * t**3 - 6 * t**2 + 3 * t))
		p.add(self.p3.pos * (-3 * t**3 + 3 * t**2))
		p.add(self.p4.pos * (t**3))

		return p

	def calculate_direction(self, t):
		p = Vec2d.zero()
		p.add(self.p1.pos * (-t**2 + 6 * t - 3))
		p.add(self.p2.pos * (9 * t**2 - 12 * t + 3))
		p.add(self.p3.pos * (-9 * t**2 + 6 * t))
		p.add(self.p4.pos * (3 * t**2))
		p.normalise()

		return p

	def calculate_normal(self, direction: Vec2d):
		direction.rotate(radians(90))
		direction.normalise()
		return direction

	def calculate_acc(self, t):
		p = Vec2d.zero()
		p.add(self.p1.pos * (-6 * t + 6))
		p.add(self.p2.pos * (18 * t - 12))
		p.add(self.p3.pos * (18 * t + 6))
		p.add(self.p4.pos * (6 * t))
		p.normalise()

		return p

	def calculate_jerk(self, t):
		p = Vec2d.zero()
		p.add(self.p1.pos * (-6))
		p.add(self.p2.pos * (18))
		p.add(self.p3.pos * (-18))
		p.add(self.p4.pos * (6))
		p.normalise()

		return p

	def display(self, screen, draw_lines=True, draw_line_points=False, draw_controll_points=False):
		points = []
		line = []
		for t_int in range(0, self.resolution+1):
			t = t_int / self.resolution

			p = self.calculate_point(t)
			d = self.calculate_direction(t)
			n = self.calculate_normal(d)

			points.append(p)
			line.append(p)

			if draw_lines and len(line) == 2:
				pygame.draw.line(screen, self.color.get(), line[0].get_int(), line[1].get_int(), 1)

				pygame.draw.line(screen, Color(0, 0  , 255).get(), line[1].get_int(), (line[1] + n).get_int(), 1)
				pygame.draw.line(screen, Color(0, 255, 255).get(), line[1].get_int(), (line[1] + d).get_int(), 1)

			if draw_line_points:
				pygame.draw.circle(screen, Color(0, 255, 0).get(), p.get_int(), 3)

			if len(line) == 2:
				line.remove(line[0])

		if not draw_controll_points : return
		self.p1.display(screen)
		self.p2.display(screen)
		self.p3.display(screen)
		self.p4.display(screen)


