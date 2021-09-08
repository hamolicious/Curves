import pygame
from vector import Vec2d, Color

class Point:
	def __init__(self, pos, **kwargs) -> None:
		self.pos = Vec2d(pos)

		self.radius = kwargs.get('radius', 8)
		self.color = Color(kwargs.get('color', 255))

	def display(self, screen):
		pygame.draw.circle(screen, self.color.get(), self.pos.get_int(), self.radius)



