# -*- coding: utf-8 -*-

'''
Prerequisites:

Pillow - PIL fork
http://pillow.readthedocs.org
'''

from PIL import Image, ImageDraw, ImageFont
from math import sin, cos, pi
import numpy as np
import random

class Dashboard(object):
	"""
	Simple class for calculating and displaying wind data

	Keyword arguments:
	history 		seconds of history used in calculations
	array_order		are new record added to the start or end of array
						'new_last'
						'new_first'
	in_wind_dir		are the input wind direction values
						'origin'
						'heading'
	out_wind_dir	are the output wind direction displayed as
						'origin'
						'heading'
	calibartion   	calibrate wind arrow housing to some direction
	"""

	def __init__(self, history=120, array_order='new_last', in_wind_dir='heading', out_wind_dir='heading', calibartion=0):
		# Save arguments
		self.history = history
		self.array_order = array_order
		self.in_wind_dir = in_wind_dir
		self.out_wind_dir = out_wind_dir
		self.calibartion = int(calibartion)

		# Initialize class
		self._make_empty()
		self._clear_current_dash()

	# Fonts
	Ubuntu_R = ImageFont.truetype("fonts/Ubuntu-R.ttf", 15)
	Ubuntu_L = ImageFont.truetype("fonts/Ubuntu-L.ttf", 15)
	Ubuntu_M = ImageFont.truetype("fonts/Ubuntu-M.ttf", 15)
	Ubuntu_B = ImageFont.truetype("fonts/Ubuntu-B.ttf", 15)
	WIND_FONT = ImageFont.truetype("fonts/Ubuntu-B.ttf", 50)
	MS_FONT = ImageFont.truetype("fonts/Ubuntu-R.ttf", 30)

	def generate(self, speed_array, direction_array, array_timespan, saveloc='wind.png'):
		self._clear_current_dash()

		self._set_wind_arrays(speed_array, direction_array, array_timespan)			# Different lengths...

		self._print_wind_values()

		self._draw_wind_std_dev()				
		self._draw_wind_arrow()

		self._draw_wind_speed_history()			# Not implemented

		# Save figure
		self.current_dash.save(saveloc)

	def _clear_current_dash(self):
		self.current_dash = self.empty_dash.copy()

	def _set_wind_arrays(self, speed, direction, timespan):

		# Flip arrays to new first
		if self.array_order == 'new_last':
			speed = speed[::-1]
			direction = direction[::-1]

		self.current_speed = speed[0]
		self.current_direction = direction[0]

		# Make direction a positive number [0,359]
		if self.in_wind_dir != self.out_wind_dir:
			self.current_direction -= 180
			if self.current_direction < 0:
				self.current_direction += 360

		# Clip arrays if they are too long
		if timespan > self.history:
			new_len = len(speed)*self.history/timespan
			speed = speed[:new_len]
			new_len = len(direction)*self.history/timespan
			direction = direction[:new_len]
			timespan = self.history

		self.wind_timespan = timespan
		self.wind_direction = direction
		self.wind_speed = speed

	def _make_empty(self, wind_history_ticks=5):
		size=(600,250)
		
		# Create image
		self.empty_dash = Image.new('L', size, color=0)

		# circle_box
		tl = (30, 30)		# top left corner
		br = (220, 220)		# bottom right corner

		# Directions
		h_mid = (br[0] + tl[0]) / 2
		v_mid = (br[1] + tl[1]) / 2
		#n = (h_mid, tl[1]-10)
		#s = (h_mid, br[1]+10)
		#w = (tl[0]-10, v_mid)
		#e = (br[0]+10, v_mid)

		# Save wind wind_direction parameters
		self.wind_dir_center = (h_mid, v_mid)
		self.wind_dir_radius = (br[0] - tl[0]) / 2
		self.wind_dir_bounding_box = [tl, br]

		# Create draw object
		draw = ImageDraw.Draw(self.empty_dash)

		'''
		# Draw cross
		width = 2
		draw.line((n,s), fill=256, width=width)
		draw.line((w,e), fill=256, width=width)
		
		# Direction letters
		draw.text((h_mid-10, tl[1]-26), u'N 0\u00B0', fill=256, font=self.Ubuntu_R)
		draw.text((h_mid-15, br[1]+10), u'S 180\u00B0', fill=256, font=self.Ubuntu_R)
		draw.text((tl[0]-25,v_mid-15), u'W', fill=256, font=self.Ubuntu_R)
		draw.text((tl[0]-30,v_mid), u'270\u00B0', fill=256, font=self.Ubuntu_R)
		draw.text((br[0]+11,v_mid-15), u'E', fill=256, font=self.Ubuntu_R)
		draw.text((br[0]+5,v_mid), u'90\u00B0', fill=256, font=self.Ubuntu_R)
		'''

		# Draw cardinal
		cardinals = ['N', 'E', 'S', 'W']
		for a in range(4):
			# Radial coordinates
			rad_dir = (a*90-self.calibartion)*pi/180

			tick_len = 7

			u = self.wind_dir_center[0] + int(sin(rad_dir)*(self.wind_dir_radius+tick_len))
			v = self.wind_dir_center[1] - int(cos(rad_dir)*(self.wind_dir_radius+tick_len))

			# Draw tick line
			draw.line([self.wind_dir_center, (u,v)], fill=256, width=3)

			# Draw text
			ut = self.wind_dir_center[0] + int(sin(rad_dir)*(self.wind_dir_radius+tick_len+9))
			vt = self.wind_dir_center[1] - int(cos(rad_dir)*(self.wind_dir_radius+tick_len+9))

			draw.text((ut-5,vt-7), cardinals[a], fill=256, font=self.Ubuntu_R)

		# Draw circle
		draw.ellipse([tl, br], fill=0, outline=256)

		# Some text
		#draw.text((3,3), u'Wind', fill=256, font=self.Ubuntu_R)
		#draw.text((3,18), u'Heading', fill=256, font=self.Ubuntu_R)
		draw.text((3,3), u'Up=%s\u00B0' % (self.calibartion), fill=256, font=self.Ubuntu_R)

		# Bounding box for wind speed
		tl = (330, 120)		# top left corner
		br = (570, 220)		# bottom right corner

		# Save parameters
		self.wind_speed_bounding_box = [tl, br]

		# Lines around speed history area
		draw.line((tl, (br[0],tl[1])), fill=256, width=0)
		draw.line(((tl[0],br[1]), br), fill=256, width=0)

		# Wind history
		tick_size = 5

		tick_start = (tl[0],br[1])
		tick_end = br
		tick_line_len = tick_end[0] - tick_start[0]

		for a in range(wind_history_ticks):
			h_off = a*tick_line_len/(wind_history_ticks-1)
			x = tick_start[0]+h_off
			y1 = tick_start[1]
			y2 = y1+tick_size
			xy = ((x,y1),(x,y2))
			draw.line(xy, fill=256, width=0)

			text_str = str(a*self.history/(wind_history_ticks-1))

			draw.text((x-5,y2+3), text_str, fill=256, font=self.Ubuntu_R)

		# Write some annotation
		text_str = 'Speed history last %s seconds' % self.history
		draw.text((tl[0],tl[1]-20), text_str, fill=256, font=self.Ubuntu_R)
		draw.text((tl[0]-40,br[1]+8), 'Age', fill=256, font=self.Ubuntu_R)
		
		# Draw line between speed and direction
		draw.line(((380,10),(380,75)), fill=256, width=0)

		# Info text above speed and direction
		if self.out_wind_dir == 'origin':
			draw.text((260,5), u'Origin', fill=256, font=self.Ubuntu_R)
		else:
			draw.text((260,5), u'Heading', fill=256, font=self.Ubuntu_R)

		draw.text((400,5), u'Speed', fill=256, font=self.Ubuntu_R)

		# Sigma info
		draw.text((3,210), u'Gray pie', fill=80, font=self.Ubuntu_R)
		draw.text((3,230), u'1\u03C3 (68%)', fill=80, font=self.Ubuntu_R)

	def _draw_wind_speed_history(self):

		# Wind speed bounding box
		tl = self.wind_speed_bounding_box[0]
		br = self.wind_speed_bounding_box[1]

		# Create draw object
		draw = ImageDraw.Draw(self.current_dash)

		# Write statistics
		spacing = 28
		offset = 85
		max_val = self.wind_speed.max()
		min_val = self.wind_speed.min()

		draw.text((tl[0]-offset,tl[1]+spacing*0), 'Max: %3.1f' % (max_val), fill=256, font=self.Ubuntu_R)
		draw.text((tl[0]-offset,tl[1]+spacing*1), 'Mean: %3.1f' % (self.wind_speed.mean()), fill=256, font=self.Ubuntu_R)
		draw.text((tl[0]-offset,tl[1]+spacing*2), u'1\u03C3: %3.1f' % (self.wind_speed.std()), fill=256, font=self.Ubuntu_R)
		draw.text((tl[0]-offset,tl[1]+spacing*3), 'Min: %3.1f' % (min_val), fill=256, font=self.Ubuntu_R)

		bins = 20
		x_array = np.linspace(0, self.wind_timespan, len(self.wind_speed))
		x_print = np.linspace(0, self.history, bins)

		hist_vals = np.interp(x_print, x_array, self.wind_speed)

		val_bins = bins * self.wind_timespan / self.history

		u_range = (br[0] - tl[0]) + 9
		v_range = (br[1] - tl[1]) - 4
		v_min = br[1] - 2
		v_val = max_val - min_val

		for b in range(bins):
			u = ((b*u_range/bins) + tl[0]) + 2

			y_max = (hist_vals[b] - min_val) / v_val * v_range

			if b <= val_bins:
				draw.line([(u,v_min), (u,v_min-y_max)], fill=100, width=5)
			
	def _print_wind_values(self):
		# Create draw object
		draw = ImageDraw.Draw(self.current_dash)

		# Direction
		dir_str = u'%3.0f\u00B0' % int(self.current_direction)
		draw.text((260,20), dir_str, fill=256, font=self.WIND_FONT, allign='right')

		# Speed
		spd_str = u'%4.1f' % self.current_speed
		draw.text((400,20), spd_str, fill=256, font=self.WIND_FONT, allign='right')
		draw.text((500,40), 'm/s', fill=256, font=self.MS_FONT)

	def _draw_wind_arrow(self, arrow_width=3):
		# Set direction to heading
		if self.in_wind_dir == 'origin':
			direction = self.current_direction-180
		else:
			direction = self.current_direction

		direction -= self.calibartion

		arrow_len = self.wind_dir_radius*0.9
		rad_wind_direction = direction*pi/180

		# Arrow tip
		u = self.wind_dir_center[0] + int(sin(rad_wind_direction)*arrow_len)
		v = self.wind_dir_center[1] - int(cos(rad_wind_direction)*arrow_len)

		# Arrow wings
		wing_len = arrow_len * 0.85
		l_wing_wind_direction = (direction-5)*pi/180
		r_wing_wind_direction = (direction+5)*pi/180

		lu = self.wind_dir_center[0] + int(sin(l_wing_wind_direction)*wing_len)
		lv = self.wind_dir_center[1] - int(cos(l_wing_wind_direction)*wing_len)

		ru = self.wind_dir_center[0] + int(sin(r_wing_wind_direction)*wing_len)
		rv = self.wind_dir_center[1] - int(cos(r_wing_wind_direction)*wing_len)

		# Create draw object
		draw = ImageDraw.Draw(self.current_dash)

		# Draw arrow line
		draw.line([self.wind_dir_center, (u,v)], fill=256, width=arrow_width)

		# Draw arrow heads
		draw.line([(lu,lv), (u,v)], fill=256, width=arrow_width)
		draw.line([(ru,rv), (u,v)], fill=256, width=arrow_width)

	def _draw_wind_std_dev(self):
		# Set direction to heading
		if self.in_wind_dir == 'origin':
			values = self.wind_direction-180
		else:
			values = self.wind_direction

		values -= self.calibartion

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
		b = self.wind_dir_bounding_box
		draw.pieslice((b[0][0]+5, b[0][1]+5 ,b[1][0]-5 ,b[1][1]-5), start, end, fill=30, outline=None)

if __name__ == '__main__':
	d = Dashboard(calibartion=70)

	num=500

	speed = np.zeros(num)
	direction = np.zeros(num)

	speed[0] = random.randint(0,30)
	direction[0] = random.randint(0,359)

	for n in range(num-1):
		speed[n+1] = random.choice((-1,1))*random.random() + speed[n]
		direction[n+1] = random.randint(-3,3) + direction[n]

		if direction[n+1] > 359:
			direction[n+1] -= 360

		elif direction[n+1] < 0:
			direction[n+1] += 360

		if speed[n+1] > 30:
			speed[n+1] = 30

		elif speed[n+1] < 0:
			speed[n+1] = 0

		outfile = 'test/frame_%s.png' % (n)

		d.generate(speed, direction, n+1, saveloc=outfile)

	#d.empty_dash.show()
	#d.current_dash.show()

	#d.current_dash.save('hei.png')
