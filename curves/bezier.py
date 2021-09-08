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

	def update(self, mouse_pos, mouse_press):
		self.p1.update(mouse_pos, mouse_press)
		self.p2.update(mouse_pos, mouse_press)
		self.p3.update(mouse_pos, mouse_press)
		self.p4.update(mouse_pos, mouse_press)

	def calculate_points(self):
		points = []

		for t_int in range(0, self.resolution + 1):
			t = t_int / self.resolution

			p = Vec2d.zero()
			p.add(self.p1.pos * (-t**3 + 3 * t**2 - 3 * t + 1))
			p.add(self.p2.pos * (3 * t**3 - 6 * t**2 + 3 * t))
			p.add(self.p3.pos * (-3 * t**3 + 3 * t**2))
			p.add(self.p4.pos * (t**3))

			points.append(p)

		return points

	def create_lines(self, points):
		lines = []

		for i in range(0, len(points)-1):
			lines.append([p.get_int() for p in points[i:i+1]][0])

		return lines

	def display(self, screen, draw_lines=True, draw_line_points=False, draw_controll_points=False):
		points = self.calculate_points()
		lines = self.create_lines(points)

		if draw_lines:
			pygame.draw.lines(screen, Color(255, 0, 0).get(), False, lines)

		if draw_line_points:
			for p in points:
				pygame.draw.circle(screen, Color(0, 255, 0).get(), p.get_int(), 3)

		if not draw_controll_points : return
		self.p1.display(screen)
		self.p2.display(screen)
		self.p3.display(screen)
		self.p4.display(screen)


