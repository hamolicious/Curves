from math import radians
import pygame
from vector import Vec2d, Color
from curves import Point
from curves.helper_functions import clamp

class CubicBezier:
	def __init__(self, p1, p2, p3, p4) -> None:
		self.p1 = Point(p1)
		self.p2 = Point(p2)
		self.p3 = Point(p3)
		self.p4 = Point(p4)

		self.resolution = 100

		self.color = Color(255)

		self.__lines = []

		self.update()

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

	def calculate_normal(self, direction: Vec2d):
		direction.rotate(radians(90))
		direction.normalise()
		return direction

	def update(self, t_range=[0, 1]):
		t_range = Vec2d(t_range)
		t_range.mult(self.resolution)

		self.__lines = []
		line = []

		for t_int in range(int(t_range[0]), int(t_range[1])+1):
			t = t_int / self.resolution

			p = self.calculate_point(t)
			d = self.calculate_direction(t)
			n = self.calculate_normal(d)

			line.append(p.get_int())

			if len(line) == 2:
				line.remove(line[0])

			self.__lines.append(line[0])

	def display(self, screen, line_thickness=3):
		if len(self.__lines) < 2 : return
		pygame.draw.lines(screen, self.color.get(), False, self.__lines, line_thickness)

	def display_controll_points(self, screen):
		self.p1.display(screen)
		self.p2.display(screen)
		self.p3.display(screen)
		self.p4.display(screen)

