# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from math import sin, cos, pi

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

		# Save wind bearing parameters
		self.wind_center = (h_mid, v_mid)
		self.wind_radius = (br[0] - tl[0]) / 2

		# Draw cross
		width = 2
		draw.line((n,s), fill=256, width=width)
		draw.line((w,e), fill=256, width=width)

		# Draw circle
		draw.ellipse([tl, br], fill=0, outline=256)

	def clear_current_dash(self):
		self.current_dash = self.empty_dash.copy()

	def draw_wind(self, bearing):
		arrow_len = self.wind_radius*0.9
		rad_bearing = bearing*pi/180

		# Arrow tip
		u = self.wind_center[0] + int(sin(rad_bearing)*arrow_len)
		v = self.wind_center[1] - int(cos(rad_bearing)*arrow_len)

		# Arrow wings
		wing_len = arrow_len * 0.85
		l_wing_bearing = (bearing-5)*pi/180
		r_wing_bearing = (bearing+5)*pi/180

		lu = self.wind_center[0] + int(sin(l_wing_bearing)*wing_len)
		lv = self.wind_center[1] - int(cos(l_wing_bearing)*wing_len)

		ru = self.wind_center[0] + int(sin(r_wing_bearing)*wing_len)
		rv = self.wind_center[1] - int(cos(r_wing_bearing)*wing_len)

		# Create draw object
		draw = ImageDraw.Draw(self.current_dash)

		# Draw arrow line
		draw.line([self.wind_center, (u,v)], fill=256, width=2)

		# Draw arrow heads
		draw.line([(lu,lv), (u,v)], fill=256, width=2)
		draw.line([(ru,rv), (u,v)], fill=256, width=2)


if __name__ == '__main__':
	d = Dashboard()


	d.draw_wind(90)

	print d.wind_center
	print d.wind_radius

	#d.empty_dash.show()
	#d.current_dash.show()