from random import randrange as rand
from random import randint
from math import sin, cos, pi
import pygame as py

py.init()
done = 0

py.display.set_caption("Rain")
win = py.display.set_mode((500, 400))

font = py.font.SysFont("courier", 16)
clock = py.time.Clock()
platform_colors = (64, 64, 64), (96, 96, 96)

def iso(x, y, z):
	return x * 2 - y * 2 + 200, x + y - z * 2 + 200

class Drip:
	def __init__(self):
		self.x = rand(100)
		self.y = rand(100)
		self.z = 300
		self.speed = 1

	def fall(self):
		self.z -= self.speed
		
		if self.speed < 8:
			if rand(75 - self.speed // 5) == 0:
				self.speed += 1

		return self.z <= 0

	def draw(self):
		x, y = iso(self.x, self.y, self.z)
		py.draw.rect(win, (0, 127, 255), (x, y, 2, 2))

	@property
	def splash(self):
		return self.x, self.y, self.speed
	

class Splash:
	def __init__(self, x, y, radius):
		self.x = x
		self.y = y
		self.r = radius
		self.s = 0

	def pour(self):
		self.s += 1
		return self.s == self.r

	def draw(self):
		py.draw.polygon(win, (0, 127, 255), (
			iso(self.x - self.s, self.y - self.s, 0),
			iso(self.x - self.s, self.y + self.s, 0),
			iso(self.x + self.s, self.y + self.s, 0),
			iso(self.x + self.s, self.y - self.s, 0)
		))

class Rain:
	platform = py.Surface((400, 400))
	platform.fill((16, 16, 16))

	splashes = []
	drips = []
	dps = 0

	for x in range(10):
		for y in range(10):
			c = platform_colors[(x ^ y) & 1]
			py.draw.polygon(platform, c, (
				iso(x * 10, y * 10, 0),
				iso(x * 10, y * 10 + 10, 0),
				iso(x * 10 + 10, y * 10 + 10, 0),
				iso(x * 10 + 10, y * 10, 0)
			))

	@classmethod
	def incDPS(cls, boost):
		cls.dps += boost
		if cls.dps > 1000:
			cls.dps = 1000

	@classmethod
	def decDPS(cls, boost):
		cls.dps -= boost
		if cls.dps < 0:
			cls.dps = 0

	@classmethod
	def generate(cls):
		for i in range(cls.dps):
			cls.drips.append(Drip())

	@classmethod
	def fall(cls):
		poplist = []
		index = 0

		for drip in cls.drips:
			if drip.fall():
				cls.splashes.append(Splash(*drip.splash))
				poplist.append(index)

			index += 1

		for index in poplist[::-1]:
			cls.drips.pop(index)

	@classmethod
	def splash(cls):
		poplist = []
		index = 0

		for splash in cls.splashes:
			if splash.pour():
				poplist.append(index)
			index += 1

		for index in poplist[::-1]:
			cls.splashes.pop(index)

	@classmethod
	def draw(cls):
		for splash in cls.splashes:
			splash.draw()

		for drip in cls.drips:
			drip.draw()

dripTimer = 0
splashTimer = 0

while 1:
	keys = py.key.get_pressed()

	if keys[py.K_z]:
		boost = 100
	elif keys[py.K_x]:
		boost = 10
	else:
		boost = 1

	for evt in py.event.get():
		if evt.type == py.QUIT:
			done = 1
			break
		if evt.type == py.KEYDOWN:
			if evt.key == py.K_UP:
				Rain.incDPS(boost)
			elif evt.key == py.K_DOWN:
				Rain.decDPS(boost)

	if done:
		break

	if dripTimer:
		dripTimer -= 1
	else:
		dripTimer = 60
		Rain.generate()

	Rain.fall()

	if splashTimer:
		splashTimer -= 1
	else:
		splashTimer = 4
		Rain.splash()

	win.fill((24, 24, 24))
	win.blit(Rain.platform, (0, 0))
	Rain.draw()

	text = font.render("DPS: %s" % Rain.dps, 1, (255, 255, 255))
	win.blit(text, (500 - text.get_width(), 0))

	py.display.flip()
	clock.tick(60)

py.quit()