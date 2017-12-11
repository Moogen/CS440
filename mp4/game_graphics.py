from graphics import *
import time

class PongGraphics:

	def __init__(self):
		self.scale = 500
		self.step = 0.03

		self.ball_radius = 5
		self.paddle_width = 10

	def create(self):
		self.win = GraphWin('pong', self.scale, self.scale)
		self.win.getMouse()

	def clear(self):
		for item in self.win.items[:]:
			item.undraw()
		self.win.update()

	def draw_paddle(self, paddle_x, paddle_y, paddle_height):
		paddle_x *= self.scale
		paddle_y *= self.scale
		paddle_height *= self.scale

		p1 = Point(paddle_x - self.paddle_width / 2, paddle_y)
		p2 = Point(paddle_x + self.paddle_width / 2, paddle_y + paddle_height)
		rect = Rectangle(p1, p2)
		rect.setFill('black')
		rect.draw(self.win)

	def draw_ball(self, ball_x, ball_y):
		ball_x *= self.scale
		ball_y *= self.scale
		circle = Circle(Point(ball_x, ball_y), self.ball_radius)
		circle.setFill('red')
		circle.draw(self.win)

	def wait(self):
		time.sleep(self.step)
