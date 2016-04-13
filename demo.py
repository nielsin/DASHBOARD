# -*- coding: utf-8 -*-

import random
from dash import Dashboard
import os
import numpy as np

# Output paramaters
outfolder = 'demo'
html_file = 'demo.html'

# Make output folder
try:
	os.mkdir('demo')
except:
	pass

# Demo parameters
num_frames = 180
calibartion_angle = 0
timespan = 120
wind_display = 'heading'
#wind_display = 'origin'
source = r'https://github.com/nielsin/DASHBOARD'
info_text = r'''
Simple class for calculating statistics and displaying wind data.
'''

# Create frames
d = Dashboard(calibartion=calibartion_angle, out_wind_dir=wind_display, history=timespan)

speed = []
direction = []

speed.append(random.randint(0,30))
direction.append(random.randint(0,359))
#direction.append(1)

outfile = os.path.join(outfolder,'frame_0.png')

speed_array = np.array(speed)
direction_array = np.array(direction)

d.generate(speed_array, direction_array, 1, saveloc=outfile)

for n in range(num_frames-1):
	speed.append(random.choice((-1,1))*random.random() + speed[n])
	direction.append(random.randint(-10,10) + direction[n])

	if direction[n+1] > 359:
		direction[n+1] -= 360

	elif direction[n+1] < 0:
		direction[n+1] += 360

	if speed[n+1] > 30:
		speed[n+1] = 30

	elif speed[n+1] < 0:
		speed[n+1] = 0

	outfile = os.path.join(outfolder,'frame_%s.png' % (n+1))

	speed_array = np.array(speed)
	direction_array = np.array(direction)

	d.generate(speed_array, direction_array, n+1, saveloc=outfile)

html_text = '''<html>
	<head>
		<title>Wind dashboard demo</title>
		<script lang="javascript">
		
			var count = 0;

			function frameCount() {

				document.getElementById("bilde").src = "frame_" + count + ".png?" + new Date().getTime();	

				count += 1;

				var text = "Frame: " + count;
				document.getElementById("text").innerHTML = text;

				if(count > %s)
					count = 0;
			}

			var upd_interval = 1 * 1000;

			setInterval(frameCount, upd_interval);
		</script>
	</head>
	<body>
		<img id="bilde" src="frame_0.png" />
		<br>
		<div id="text"></div>
		Demo will reset after %s frames
		<br>
		<br>
		Wind display mode: %s
		<br>
		Calibartion angle: %s
		<br>
		<br>
		%s
		<br>
		<br>
		Source code: <a href="%s">%s</a>

		<script>
			frameCount();
		</script>
	</body>
</html>
''' % (num_frames, num_frames, wind_display, calibartion_angle, info_text, source, source)

html_path = os.path.join(outfolder, html_file)
with open(html_path, 'w') as outfile:
	outfile.write(html_text)