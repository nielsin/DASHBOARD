# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from math import sin, cos, pi
import numpy as np
import random

class Dashboard(object):
	"""docstring for Dashboard"""

	def __init__(self):
		self.make_empty()
		self.clear_current_dash()

	def make_empty(self):
		size=(600,250)
		
		# Create image
		self.empty_dash = Image.new('L', size, color=0)

		# Create draw object
		draw = ImageDraw.Draw(self.empty_dash)

		# circle_box
		tl = (30, 30)		# top left corner
		br = (220, 220)		# bottom right corner

		# Directions
		h_mid = (br[0] + tl[0]) / 2
		v_mid = (br[1] + tl[1]) / 2
		n = (h_mid, tl[1]-10)
		s = (h_mid, br[1]+10)
		w = (tl[0]-10, v_mid)
		e = (br[0]+10, v_mid)

		# Save wind wind_direction parameters
		self.wind_center = (h_mid, v_mid)
		self.wind_radius = (br[0] - tl[0]) / 2
		self.wind_bounding_box = [tl, br]

		# Draw cross
		width = 2
		draw.line((n,s), fill=256, width=width)
		draw.line((w,e), fill=256, width=width)

		# Draw circle
		draw.ellipse([tl, br], fill=0, outline=256)

	def clear_current_dash(self):
		self.current_dash = self.empty_dash.copy()

	def set_wind(self, speed, direction):
		self.wind_direction = direction
		self.wind_speed = speed

	def draw_wind_arrow(self):

		arrow_len = self.wind_radius*0.9
		rad_wind_direction = self.wind_direction*pi/180

		# Arrow tip
		u = self.wind_center[0] + int(sin(rad_wind_direction)*arrow_len)
		v = self.wind_center[1] - int(cos(rad_wind_direction)*arrow_len)

		# Arrow wings
		wing_len = arrow_len * 0.85
		l_wing_wind_direction = (self.wind_direction-5)*pi/180
		r_wing_wind_direction = (self.wind_direction+5)*pi/180

		lu = self.wind_center[0] + int(sin(l_wing_wind_direction)*wing_len)
		lv = self.wind_center[1] - int(cos(l_wing_wind_direction)*wing_len)

		ru = self.wind_center[0] + int(sin(r_wing_wind_direction)*wing_len)
		rv = self.wind_center[1] - int(cos(r_wing_wind_direction)*wing_len)

		# Create draw object
		draw = ImageDraw.Draw(self.current_dash)

		# Draw arrow line
		draw.line([self.wind_center, (u,v)], fill=256, width=2)

		# Draw arrow heads
		draw.line([(lu,lv), (u,v)], fill=256, width=2)
		draw.line([(ru,rv), (u,v)], fill=256, width=2)

	def draw_wind_std_dev(self, values):
		rad_values = values*np.pi/180
		u = np.sin(rad_values)
		v = np.cos(rad_values)

		u_mean = np.mean(u)
		v_mean = np.mean(v)

		mean = int(np.arctan(u_mean/v_mean)*180/pi)

		if v_mean<0:
			mean += 180

		if u_mean<0 and v_mean>0:
			mean += 360

		u_std = np.std(u)
		v_std = np.std(v)

		std = int(np.arctan(u_std/v_std)*180/pi)

		# Create draw object
		draw = ImageDraw.Draw(self.current_dash)

		# Draw pie
		start = mean-std-90
		end = mean+std-90
		b = self.wind_bounding_box
		draw.pieslice((b[0][0]+5, b[0][1]+5 ,b[1][0]-5 ,b[1][1]-5), start, end, fill=30, outline=None)

	def make_test_wind_values(self, num=100):
		speed = np.zeros(num)
		direction = np.zeros(num)

		speed[0] = random.randint(0,30)
		direction[0] = random.randint(0,359)

		for n in range(num-1):
			speed[n+1] = random.randint(-2,2) + speed[n]
			direction[n+1] = random.randint(-5,5) + direction[n]

			if direction[n+1] > 359:
				direction[n+1] -= 360

			elif direction[n+1] < 0:
				direction[n+1] += 360

			if speed[n+1] > 30:
				speed[n+1] = 30

			elif speed[n+1] < 0:
				speed[n+1] = 0

		return speed, direction


if __name__ == '__main__':
	d = Dashboard()

	

	speed, direction = d.make_test_wind_values()

	d.draw_wind_std_dev(direction)

	d.set_wind(speed=10, direction=direction[-1])

	d.draw_wind_arrow()

	


	#d.empty_dash.show()
	d.current_dash.show()