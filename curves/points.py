import pygame
from vector import Vec2d, Color

class Point:
	def __init__(self, pos, **kwargs) -> None:
		self.pos = Vec2d(pos)

		self.radius = kwargs.get('radius', 8)
		self.color = Color(kwargs.get('color', 255))

		self.__selected = False

	def update(self, mouse_pos, mouse_press):
		if mouse_pos.dist(self.pos) <= self.radius**2:
			if mouse_press[0]:
				self.__selected = True

		if self.__selected:
			self.pos.set(mouse_pos)

		if not mouse_press[0]:
			self.__selected = False

	def display(self, screen):
		pygame.draw.circle(screen, self.color.get(), self.pos.get_int(), self.radius)



