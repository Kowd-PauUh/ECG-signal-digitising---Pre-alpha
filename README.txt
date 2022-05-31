Version:	Pre-alpha
Requirements:	Python 3.8
		+---------------+----------+
		| Package	| Version  |
		+---------------+----------+
		| Kivy          | 2.1.0	   |
		| matplotlib 	| 3.5.2	   |
		| opencv-python	| 4.5.5.64 |
		| numpy 	| 1.22.3   |
		+---------------+----------+

To run successfully, configure the path to the ECG file 
in the IMAGE_PATH variable of app.py.

Once started, a window showing the ECG image will appear. Select two points on the image by moving the cursor and left-clicking. The area between the selected points will be coloured for better visualisation. When the area to be analysed has been selected, press Enter and the window with the digitised cardiogram will appear.

Not yet implemented:
 - curve scaling
 - data export