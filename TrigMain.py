""" 
This is the Python code for the Visual Trigonometry Fundamentals program.  
You can use trigmain.bat (on a Windows platform) to start the program or start it any other way that works for you.
The program is free. 
If you make any useful changes, let me know so I can consider incorporating them into my version.
If you discover any bugs, let me know.  I have only tested (so far) on a Windows machine.  I'll be interested in learning whether it works on Linux and Macs.
Python 3.13.7 was used for development.

I can be reached at danch1@verizon.net      Dan Chandler
"""
import tkinter as tk
#from tkinter import ttk
from tkinter import Canvas
import math
import os  # we need os to get exit()

import sys           # used for function get_screen_size
import subprocess    # used for function get_screen_size
import re            # used for function get_screen_size
import ctypes        # used for function get_screen_size

import Tooltip_Classes
import VirtualKeyboard
import ErrWindow

class Unit_Circle():

	def __init__(self):
		self.radius = None
		self.center_x = None
		self.center_y = None
		self.lineH_id = None
		self.lineS_id = None
		self.lineC_id = None

	def Unit_Circle_setup(self, TF_instance):

		self.radius = TF_instance.scale_x(175)
		self.center_x = TF_instance.scale_x(240)
		self.center_y = TF_instance.scale_y(520)

		if (TF_instance.firstCycle):

			TF_instance.app_canvas.create_text(self.center_x, self.center_y - self.radius - TF_instance.scale_y(50), text="Unit Circle       Radius = 1",
										font=("Helvetica", TF_instance.primary_font_size, "bold"))

			circ = self.create_circle(self.center_x, self.center_y, self.radius, TF_instance.app_canvas, outline=TF_instance.rgb_to_hex((0, 255, 255)), fill='white', width = 2)
			tooltip_str = "Trig Definitions:\n\n" + "sin(θ) = opposite / hypotenuse\n" + "cos(θ) = adjacent / hypotenuse\n" + "tan(θ) = opposite / adjacent\n\n" + "and also, tan(θ) = sin(θ) / cos(θ)"
			Tooltip_Classes.ToolTip_For_Canvas_Items(TF_instance.app_canvas, circ, tooltip_str) 

			# Draw the x axis in light gray
			x1 = self.center_x-self.radius
			y1 = self.center_y
			x2 = self.center_x+self.radius
			y2 = self.center_y
			TF_instance.app_canvas.create_line(x1, y1, x2, y2, fill =TF_instance.rgb_to_hex(TF_instance.medium_gray_color), width = 1)

			# Draw the y axis in light gray
			x1 = self.center_x
			y1 = self.center_y-self.radius
			x2 = self.center_x
			y2 = self.center_y+self.radius
			TF_instance.app_canvas.create_line(x1, y1, x2, y2, fill =TF_instance.rgb_to_hex(TF_instance.medium_gray_color), width = 1)

			x = self.center_x
			y = self.center_y - self.radius - TF_instance.scale_y(14)
			TF_instance.app_canvas.create_text(x, y, text = "1", font=("Helvetica", TF_instance.small_font_size))

			x = self.center_x
			y = self.center_y + self.radius + TF_instance.scale_y(14)
			TF_instance.app_canvas.create_text(x, y, text = "-1", font=("Helvetica", TF_instance.small_font_size))

			x = self.center_x - self.radius - TF_instance.scale_x(14)
			y = self.center_y
			TF_instance.app_canvas.create_text(x, y, text = "-1", font=("Helvetica", TF_instance.small_font_size))

			x = self.center_x + self.radius + TF_instance.scale_x(14)
			y = self.center_y
			TF_instance.app_canvas.create_text(x, y, text = "1", font=("Helvetica", TF_instance.small_font_size))

	def Unit_Circle_draw_triangle(self, sinOfAngle, cosOfAngle, TF_instance): 

		if (TF_instance.firstCycle):
			self.Unit_Circle_setup(TF_instance)
		else:
			TF_instance.app_canvas.delete(self.lineH_id)  # remove the last hypotenuse line that we drew
			TF_instance.app_canvas.delete(self.lineS_id)  # remove the last sin line that we drew
			TF_instance.app_canvas.delete(self.lineC_id)  # remove the last cos line that we drew

		line_width = 2

		# Draw the hypotenuse in gray
		x1 = self.center_x
		y1 = self.center_y
		x2 = self.center_x+(cosOfAngle*self.radius)
		y2 = self.center_y-(sinOfAngle*self.radius)
		self.lineH_id = TF_instance.app_canvas.create_line(x1, y1, x2, y2, fill = TF_instance.rgb_to_hex((154, 154, 154)), width = line_width)  # gray

		# Draw the sin in red
		x1 = self.center_x + (cosOfAngle*self.radius)
		y1 = self.center_y
		x2 = self.center_x+(cosOfAngle*self.radius)
		y2 = self.center_y-(sinOfAngle*self.radius)
		self.lineS_id = TF_instance.app_canvas.create_line(x1, y1, x2, y2, fill = TF_instance.rgb_to_hex((255, 0, 0)), width = line_width)  # red

		# Draw the cos in dark blue
		x1 = self.center_x
		y1 = self.center_y
		x2 = self.center_x+(cosOfAngle*self.radius)
		y2 = self.center_y
		self.lineC_id = TF_instance.app_canvas.create_line(x1, y1, x2, y2, fill = TF_instance.rgb_to_hex((0, 0, 255)), width = line_width)  # dark blue

	def create_circle(self, center_x, center_y, radius, canvas, **kwargs):
		return canvas.create_oval(center_x-radius, center_y-radius, center_x+radius, center_y+radius, **kwargs)

class setup_run:
	def __init__(self):
		self.bump_up_button = None
		self.bump_down_button = None
		self.quit_button = None
		self.go_button = None
		self.bump_value_entry = None
		self.keyboard = None
		self.TF_instance = None
		self.version = "1.0"

	def create_Widgets(self, TF_instance): # the widgets made in this function only need to be created once at the beginning of the run
		self.TF_instance = TF_instance
		control_line_y = TF_instance.app_height - TF_instance.scale_y(105)

		self.quit_button = tk.Button(TF_instance.root, text = 'Exit', command = self.button_clicked_quit, 
						  font = ('Helvetica', TF_instance.button_font_size), takefocus=0)
		quit_x = TF_instance.app_width - TF_instance.scale_x(90)
		self.quit_button.place(x=quit_x, y=control_line_y)
		self.quit_button.bind("<<ButtonClickedQuit>>", self.handle_custom_event_quit)  # function handle_custom_event_quit proccesses event <<ButtonClickedQuit>>
		Tooltip_Classes.ToolTip(self.quit_button, "This will terminate the program")

		self.bump_up_button = tk.Button(TF_instance.root, text = 'Bump +', command = self.button_clicked_up, 
								  font = ('Helvetica', TF_instance.button_font_size), takefocus=0)
		TF_instance.app_canvas.update_idletasks() # call this to get accurate window_width value
		up_x = quit_x - TF_instance.scale_x(150)
		self.bump_up_button.place(x=up_x, y=control_line_y)
		self.bump_up_button.config(state="disabled")
		self.bump_up_button.bind("<<ButtonClickedUp>>", self.handle_custom_event_up)  # function handle_custom_event_up proccesses event <<ButtonClickedUp>>

		TF_instance.app_canvas.create_text(TF_instance.app_width - TF_instance.scale_x(70), TF_instance.scale_y(15),
								text = "Ver " + self.version, font=("Helvetica", TF_instance.small_font_size), 
								fill=TF_instance.rgb_to_hex(TF_instance.light_gray_color))

		def update_bump_tool_tips():
			if str(TF_instance.bump_delta) == "1.0":
				deg = " degree"
			else:
				deg = " degrees"
			bump_up_tip_str = "Increase the angle value by " + str(TF_instance.bump_delta) + deg + "\nand show the new results"
			Tooltip_Classes.ToolTip(self.bump_up_button, bump_up_tip_str)
			bump_down_tip_str = "Reduce the angle value by " + str(TF_instance.bump_delta) + " degrees\nand show the new results"
			Tooltip_Classes.ToolTip(self.bump_down_button, bump_down_tip_str)
		
		def get_bump_entry_input(event):
			# This function is called when the Enter key is pressed in the bump entry widget.
			# It retrieves the value from the entry and stores it in a variable.
			entered_text = self.bump_value_entry.get()
			try:
				TF_instance.bump_delta = float(entered_text)
				update_bump_tool_tips()
				if TF_instance.this_screen_width > TF_instance.width_threshold:
					TF_instance.app_canvas.itemconfigure(ghost_label_bump, text=entered_text)

				self.bump_value_entry.config(fg="black")   # change the color of the bump entry text back to black (as Amy Winehouse would say)
			except ValueError:
				ErrorWindow_instance = ErrWindow.ErrorWindow(self.TF_instance)
				ErrorWindow_instance.showErrorWindow(entered_text)

		bump_entry_text = tk.StringVar()
		initial_bump_value = str(TF_instance.bump_delta)
		bump_entry_text.set(initial_bump_value)

		def on_focus_in(event):
			self.bump_value_entry.config(fg="red") # set color of text to red when user sets focus on bump entry input field

		self.bump_value_entry = tk.Entry(TF_instance.root, width=10, textvariable=bump_entry_text, bg='white',  fg='black', 
						font=("Helvetica", TF_instance.entry_font_size), takefocus = 0)
		self.bump_value_entry.bind("<Return>", get_bump_entry_input)
		self.bump_value_entry.bind("<FocusIn>", on_focus_in)
		bump_value_x = up_x - TF_instance.scale_x(195)
		self.bump_value_entry.place(x=bump_value_x, y=control_line_y, height = 30)
		Tooltip_Classes.ToolTip(self.bump_value_entry, "This value is the amount in degrees that a Bump+ or Bump- will add or subtract to the angle value.\nYou can change this value by typing a new value and pressing the Enter key.")

		if TF_instance.this_screen_width > TF_instance.width_threshold:
			ghost_label_bump =TF_instance.app_canvas.create_text(bump_value_x + TF_instance.scale_x(15),control_line_y + TF_instance.scale_y(40),
								text=initial_bump_value, font=("Helvetica", TF_instance.small_font_size), 
								fill=TF_instance.rgb_to_hex(TF_instance.light_gray_color))
			# Attach tooltip to the ghost value
			Tooltip_Classes.ToolTip_For_Canvas_Items(TF_instance.app_canvas, ghost_label_bump, "Shows which bump delta is currently in effect")

		self.bump_down_button = tk.Button(TF_instance.root, text = 'Bump -', command = self.button_clicked_down, 
									font = ('Helvetica', TF_instance.button_font_size), takefocus=0)
		down_x = bump_value_x - TF_instance.scale_x(150)
		self.bump_down_button.place(x=down_x, y=control_line_y)
		self.bump_down_button.config(state="disabled")
		self.bump_down_button.bind("<<ButtonClickedDown>>",self.handle_custom_event_down)  # function handle_custom_event_down proccessrd event <<ButtonClickeddown>>
		update_bump_tool_tips()

		TF_instance.input_box_L_x = TF_instance.scale_x(190)
		TF_instance.input_box_R_x = TF_instance.input_box_L_x + TF_instance.scale_x(100)
		entry_tooltip_text = "Enter one angle value in degrees to process a single angle.\nEnter two angle values to process a range of angles."

		TF_instance.input_box_left = tk.Entry(TF_instance.root, width=TF_instance.scale_x(12), bg='white',  fg='black', font=("Helvetica", 
											TF_instance.entry_font_size), takefocus=1)
		TF_instance.input_box_left.place(x=TF_instance.input_box_L_x - TF_instance.scale_x(94), y=TF_instance.scale_y(TF_instance.input_box_location_y) + TF_instance.scale_y(14), 
								   height = TF_instance.scale_y(25))
		TF_instance.input_box_left.focus_set()
		Tooltip_Classes.ToolTip(TF_instance.input_box_left, entry_tooltip_text)

		TF_instance.input_box_right = tk.Entry(TF_instance.root, width=TF_instance.scale_x(12), bg='white',  fg='black', 
										 font=("Helvetica", TF_instance.entry_font_size), takefocus=1)
		TF_instance.input_box_right.place(x=TF_instance.input_box_R_x - TF_instance.scale_x(50), 
									y=TF_instance.scale_y(TF_instance.input_box_location_y) + TF_instance.scale_y(14), height = TF_instance.scale_y(25))
		Tooltip_Classes.ToolTip(TF_instance.input_box_right, entry_tooltip_text)

		inText_right_id = TF_instance.app_canvas.create_text(TF_instance.scale_x(-2000), TF_instance.scale_y(200), text="", font=("Helvetica", 8), 
												fill=TF_instance.rgb_to_hex(TF_instance.light_gray_color))
		TF_instance.inText_right = TF_instance.app_canvas.itemcget(inText_right_id, "text") # itemcget retrieves the text that was written to the canvas

		self.go_button = tk.Button(TF_instance.root, text = 'Go', command = self.button_clicked_go, font = ('Helvetica', 
																								 TF_instance.button_font_size), takefocus=1)
		go_x = TF_instance.input_box_R_x + TF_instance.input_box_right.winfo_width() + TF_instance.scale_x(90)
		self.go_button.place(x=go_x, y=TF_instance.scale_y(TF_instance.input_box_location_y) + TF_instance.scale_y(12), height = TF_instance.scale_y(29))
		self.go_button.bind("<<ButtonClickedGo>>", TF_instance.handle_custom_event_go)  # function handle_custom_event_go proccesses event <<ButtonClickedGo>>
		Tooltip_Classes.ToolTip(self.go_button, "Click here after inputting angle value(s) to plot")

		self.keyboard = VirtualKeyboard.VirtualKeyboard(TF_instance.scale_x(215), control_line_y + TF_instance.scale_y(65), 100, TF_instance.app_canvas)
		self.keyboard._draw(TF_instance.this_screen_width, TF_instance.width_threshold)

		inText_left_id = TF_instance.app_canvas.create_text(TF_instance.scale_x(-2000), TF_instance.scale_y(200), text="", font=("Helvetica", 8), 
											   fill=TF_instance.rgb_to_hex(TF_instance.light_gray_color))
		TF_instance.inText_left = TF_instance.app_canvas.itemcget(inText_left_id, "text") # itemcget retrieves the text that was written to the canvas

		local_font_size = None
		if TF_instance.this_screen_width > TF_instance.width_threshold:
			local_font_size = TF_instance.primary_font_size
		else:
			local_font_size = TF_instance.small_font_size
		TF_instance.app_canvas.create_text(TF_instance.scale_x(TF_instance.text_x), TF_instance.scale_y(TF_instance.label_location1_y),
								text="Enter angle in degrees,", font=("Helvetica", local_font_size))
		TF_instance.app_canvas.create_text(TF_instance.scale_x(TF_instance.text_x), TF_instance.scale_y(TF_instance.label_location2_y),
								text="then touch (or click on) the Go button.", font=("Helvetica", local_font_size))
		TF_instance.app_canvas.create_text(TF_instance.scale_x(TF_instance.text_x), TF_instance.scale_y(TF_instance.label_location3_y),
								text="Or you can enter two angles,", font=("Helvetica", local_font_size))
		TF_instance.app_canvas.create_text(TF_instance.scale_x(TF_instance.text_x), TF_instance.scale_y(TF_instance.label_location4_y),
								text="then touch the Go button.", font=("Helvetica", local_font_size))
		
	def button_clicked_up(self):
		# print ("bump up button was clicked")
		self.bump_up_button.event_generate("<<ButtonClickedUp>>")

	def button_clicked_down(self):
		# print ("bump down button was clicked")		
		self.bump_down_button.event_generate("<<ButtonClickedDown>>")

	def button_clicked_quit(self):
		# print ("quit button was clicked")
		self.quit_button.event_generate("<<ButtonClickedQuit>>")

	def button_clicked_go(self):
		self.go_button.event_generate("<<ButtonClickedGo>>")
		#print("Go button clicked, generating event <<ButtonClickedGo>>.")	

	def handle_custom_event_up(self, event):
		#print("Custom event: bump plus button was clicked")
		self.bump_up_button.config(state="disabled")    # disable the two bump buttons
		self.bump_down_button.config(state="disabled")
		self.TF_instance.process_bump('up')
		self.TF_instance.show_bump_buttons()     # restore the bump buttons

	def handle_custom_event_down(self, event):
		# print("Custom event: bump minus button was clicked")
		self.bump_up_button.config(state="disabled")    # disable the two bump buttons
		self.bump_down_button.config(state="disabled")
		self.TF_instance.process_bump('down')
		self.TF_instance.show_bump_buttons()     # restore the bump buttons

	def handle_custom_event_quit(self, event):
		# print("Custom event: quit button was clicked")
		os._exit(0)
		#exit()	

class TrigFundamentals:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Visual Trigonometry Fundamentals")
		self.app_width = None
		self.app_height = None
		self.root.resizable(False, False)
		self.input_box_left = None
		self.input_box_right = None
		self.inText_left = None
		self.inText_right = None
		self.ghost_label_bump = None
		self.bump_delta = 15.0
		self.ghost_label_left_id = None
		self.ghost_label_right_id = None
		self.small_font_size = 11
		self.primary_font_size = 14
		self.button_font_size = 14
		self.entry_font_size = 14
		self.input_box_L_x = None
		self.input_box_R_x = None
		self.light_gray_color = (160, 160, 160) # a light gray
		self.medium_gray_color = (211, 211, 211) # a medium gray
		self.last_run_type_str = 'none_yet'
		self.last_angle_deg_left = 0.0
		self.last_angle_deg_right = 0.0
		self.last_angle_deg = 0.0
		self.sin_line_id = None
		self.text_sin_id = None
		self.cos_line_id = None
		self.text_cos_id = None
		self.tan_line_id = None
		self.text_tan_id = None
		self.text_angle_deg_id = None
		self.text_angle_rad_id = None
		self.firstCycle = True # this variable is used to control some one-time-only drawing operations
		self.setup_instance = None
		self.UC_instance = None
		self.scale_factor_x = None
		self.scale_factor_y = None
		self.this_screen_height = None
		self.this_screen_width = None
		self.width_threshold = None
		self.label_location1_y = None
		self.label_location2_y = None
		self.label_location3_y = None
		self.label_location4_y = None
		self.input_box_location_y = None
		self.angle_values_location_y = None
		self.text_x = None
		self.x_left = None
		self.sin_cos_box_height = None
		self.tan_box_height = None
		self.box_width = None
		self.UpperLeft_x_sin = None
		self.upperLeft_x_cos = None
		self.UpperLeft_x_tan = None
		self.Rounding_Num_Digits = 10  # this is the number of digits to which we round sin, cos, tan, and angle_rad values before displaying them
		self.app_canvas = None

	#==========
	def scale_x(self, inVal):
		# Adjust the input value to account for non-nominal screen width
		return int(inVal * self.scale_factor_x)

	def scale_y(self, inVal):
		# Adjust the input value to account for non-nominal screen height
		return int(inVal * self.scale_factor_y)

	def get_screen_size(self):
			if sys.platform.startswith("win"):
				user32 = ctypes.windll.user32
				return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

			elif sys.platform.startswith("linux"):
				try:
					output = subprocess.check_output("xrandr | grep '*'", shell=True).decode()
					resolution = re.search(r'(\d+)x(\d+)', output).groups()
					return int(resolution[0]), int(resolution[1])
				except Exception:
					raise RuntimeError("Could not determine screen size on Linux (is xrandr installed?).")

			elif sys.platform == "darwin":
				try:
					output = subprocess.check_output(
						"system_profiler SPDisplaysDataType | grep Resolution", shell=True
					).decode()
					resolution = re.search(r'(\d+)\s*x\s*(\d+)', output).groups()
					return int(resolution[0]), int(resolution[1])
				except Exception:
					raise RuntimeError("Could not determine screen size on macOS.")

			else:
				raise NotImplementedError(f"Unsupported platform: {sys.platform}")
			
	def screen_calculations(self):

		build_resolution = "auto_detect"			 # auto_detect or low_end_handheld or low_end_laptop

		if build_resolution == "auto_detect":
			self.this_screen_width, self.this_screen_height = self.get_screen_size()
		elif build_resolution == "low_end_handheld":
			self.this_screen_width = 1280  # Use this to test worst resolution handheld  (1280 by 800)  # low end tablet
			self.this_screen_height = 800  # Use this to test worst resolution handheld  (1280 by 800)  # low end tablet
		elif build_resolution == "low_end_laptop":
			self.this_screen_width = 1366  # Use this to test worst resolution laptop  # low end laptop
			self.this_screen_height = 768  # Use this to test worst resolution laptop  # low end laptop

		self.width_threshold = 1366 + 1  # use this to decide in code when to omit features (like ghost labels) due to undesirable crowded screen on low-end devices

		print ("screen width = ", self.this_screen_width, "screen height = ", self.this_screen_height)

		#  Nominal resolution was used to develop the program and to decide the most eye-pleasing placement of widgets (no crowding, easy=to-see plots)
		nominal_screen_width = 1920   # this is the resolution used to develop the program
		nominal_screen_height = 1080  # this is the resolution used to develop the program

		self.scale_factor_x = self.this_screen_width / nominal_screen_width
		self.scale_factor_y = self.this_screen_height / nominal_screen_height
		print ("scale_factor_x = ", self.scale_factor_x, "   scale_factor_y = ", self.scale_factor_y)

		self.app_width  = self.scale_x(1260)
		self.app_height = self.scale_y(780)
		print ("app width = ", self.app_width, "app height = ", self.app_height)
		self.root.geometry(str(self.app_width) + "x" + str(self.app_height))
		#==========

		root_window = self.root.winfo_toplevel()
		#root_window.overrideredirect(1)  # get rid of the title bar of the main window
		
		# Set the new window position
		app_x_pos = int(self.this_screen_width / 2) - int(self.app_width / 2) 
		app_y_pos = self.scale_y(30)
		self.root.geometry(f"+{app_x_pos}+{app_y_pos}")  # position the app window centered on the screen
        
        # Create canvas
		aquaBlue = self.rgb_to_hex((0, 255, 255))
		self.app_canvas = tk.Canvas(self.root, width=self.app_width, height=self.app_height, bg=aquaBlue)
		self.app_canvas.pack()
     
		self.setup_instance = setup_run()
		self.UC_instance = Unit_Circle()

		self.graphMinInDegrees = -360.0
		self.graphMaxInDegrees = 720.0
		self.graphSpan = self.graphMaxInDegrees - self.graphMinInDegrees
		self.line_height = 20
		self.label_location1_y = 40
		self.label_location2_y = 65
		self.label_location3_y = 90
		self.label_location4_y = 115
		self.input_box_location_y = self.label_location4_y + 5
		self.angle_values_location_y = self.input_box_location_y + 60

		self.x_left = 40
		self.text_x = 235
		self.sin_cos_box_height = 100
		self.tan_box_height = 270  # tan gets a taller box than sin and cos 
		self.box_width = 660
		self.UpperLeft_x_sin = 580
		self.UpperLeft_x_cos = self.UpperLeft_x_sin 
		self.UpperLeft_x_tan = self.UpperLeft_x_sin 

		self.UpperLeft_y_sin = 50
		self.UpperLeft_y_cos = self.UpperLeft_y_sin + self.sin_cos_box_height + 50
		self.UpperLeft_y_tan = self.UpperLeft_y_cos + self.sin_cos_box_height + 50
		#self.firstCycle = True  # this variable is used to control some one-time-only drawing operations

	def x_annotation(self, angle_left, x_right, angle_right, y_position_annotation):
		# this method puts the annotation on the x axis that is below the tangent box

		thisAngle_deg = angle_left
		angle_span = angle_right - angle_left
		pixel_span = self.scale_x(x_right) - self.scale_x(self.x_left)
		while thisAngle_deg <= angle_right:
			x_position_annotation = self.scale_x(self.UpperLeft_x_tan) +(pixel_span / angle_span)*(thisAngle_deg-self.graphMinInDegrees)
			modValue = thisAngle_deg % 90.0
			if modValue == 0.0 :
				thisAnno = str(int(thisAngle_deg))
				x = x_position_annotation
				y = self.scale_y(y_position_annotation)
				self.app_canvas.create_text(x, y, text = thisAnno, font=("Helvetica", self.small_font_size))

			thisAngle_deg += 1.0

	def DrawSinPoint(self, Angle_deg):
		thisAngle_rad = Angle_deg * math.pi / 180.0
		thisSin = math.sin(thisAngle_rad)
		x_position = self.scale_x(self.UpperLeft_x_sin)+(self.scale_x(self.box_width) / self.graphSpan)*(Angle_deg-self.graphMinInDegrees)
		y_position = self.scale_y(self.UpperLeft_y_sin)+(self.scale_y(self.sin_cos_box_height) / 2.0) - thisSin * (self.scale_y(self.sin_cos_box_height)/2.0)
		point_color = self.rgb_to_hex((255, 0, 0))
		self.app_canvas.create_rectangle(x_position,y_position,x_position+1,y_position+1, outline=point_color, fill=point_color)  # this line draws a single point

	def DrawCosPoint(self, Angle_deg):
		thisAngle_rad = Angle_deg * math.pi / 180.0
		thisCos = math.cos(thisAngle_rad)
		x_position = self.scale_x(self.UpperLeft_x_cos)+(self.scale_x(self.box_width) / self.graphSpan)*(Angle_deg-self.graphMinInDegrees)
		y_position = self.scale_y(self.UpperLeft_y_cos)+(self.scale_y(self.sin_cos_box_height) / 2.0) - thisCos * (self.scale_y(self.sin_cos_box_height)/2.0)
		point_color = self.rgb_to_hex((0, 0, 255))  # dark blue
		self.app_canvas.create_rectangle(x_position,y_position,x_position+1,y_position+1, outline=point_color, fill=point_color)  # this line draws a single point

	def DrawTanPoint(self, Angle_deg):
		thisAngle_rad = Angle_deg * math.pi / 180.0
		thisTan = math.tan(thisAngle_rad)
		x_position = self.scale_x(self.UpperLeft_x_tan)+(self.scale_x(self.box_width) / self.graphSpan)*(Angle_deg-self.graphMinInDegrees)
		y_position = self.scale_y(self.UpperLeft_y_tan) +(self.scale_y(self.tan_box_height) / 2.0) - (thisTan * (self.scale_y(self.tan_box_height)/self.scale_y(15)))
		if y_position >= self.scale_y(self.UpperLeft_y_tan) and y_position <= (self.scale_y(self.UpperLeft_y_tan) + self.scale_y(self.tan_box_height)):
			self.app_canvas.create_rectangle(x_position,y_position,x_position+1,y_position+1)  # this line draws a single point

	def SinBox(self, angle_deg, last_angle_deg, sinOfAngle):
		sinBoxColor = self.rgb_to_hex((255, 255, 255)) # white
		if( self.firstCycle ): 
			
			self.app_canvas.create_rectangle(
    			self.scale_x(self.UpperLeft_x_sin), self.scale_y(self.UpperLeft_y_sin), # x1, y1
    			self.scale_x(self.UpperLeft_x_sin)+self.scale_x(self.box_width), self.scale_y(self.UpperLeft_y_sin)+self.scale_y(self.sin_cos_box_height),  # x2, y2
    			outline=sinBoxColor,    # border color
    			fill=sinBoxColor,       # inside color
    			width=3   )             # border thickness

			# Annotate the y axis
			x = self.scale_x(self.UpperLeft_x_sin)-self.scale_x(20)
			y = self.scale_y(self.UpperLeft_y_sin)
			sin_y_anno_top_id =self.app_canvas.create_text(x, y, text = "1", font=("Helvetica", self.small_font_size))

			x = self.scale_x(self.UpperLeft_x_sin)-self.scale_x(20)
			y = self.scale_y(self.UpperLeft_y_sin)+self.scale_y(self.sin_cos_box_height)
			sin_y_anno_bottom_id =self.app_canvas.create_text(x, y, text = "-1", font=("Helvetica", self.small_font_size))

			x = self.scale_x(self.UpperLeft_x_sin)-self.scale_x(20)
			y = self.scale_y(self.UpperLeft_y_sin)+(0.5*self.scale_y(self.sin_cos_box_height))
			sin_y_anno_zero_id =self.app_canvas.create_text(x, y, text = "0", font=("Helvetica", self.small_font_size))

			# draw a horizontal gray line at y = 0
			x1 = self.scale_x(self.UpperLeft_x_sin)
			y1 = self.scale_y(self.UpperLeft_y_sin)+(0.5*self.scale_y(self.sin_cos_box_height))
			x2 = self.scale_x(self.UpperLeft_x_sin)+self.scale_x(self.box_width)
			y2 = self.scale_y(self.UpperLeft_y_sin)+(0.5*self.scale_y(self.sin_cos_box_height))
			x_axis_zero_id = self.app_canvas.create_line(x1, y1, x2, y2, fill =self.rgb_to_hex(self.medium_gray_color), width = 1)
			    
			# draw the entire sin function from graphMinInDegrees to graphMaxInDegrees
			thisAngle_deg = self.graphMinInDegrees
			while thisAngle_deg <= self.graphMaxInDegrees:
				self.DrawSinPoint(thisAngle_deg)
				thisAngle_deg += 1.0

		else: 
			if last_angle_deg >= self.graphMinInDegrees and last_angle_deg <= self.graphMaxInDegrees:
				self.app_canvas.delete(self.sin_line_id)  # remove the last red sin line that we drew
			self.app_canvas.delete(self.text_sin_id)  # remove the text that was written during the previous cycle

		if angle_deg >= self.graphMinInDegrees and angle_deg <= self.graphMaxInDegrees:
			# draw a vertical red line to show the sin of the angle that the user selected
			requestedColor = self.rgb_to_hex((255, 0, 0)) # red
			self.sin_line_id = self.verticalLine(angle_deg, self.scale_x(self.UpperLeft_x_sin), self.scale_y(self.UpperLeft_y_sin), self.scale_x(self.box_width), 
								      self.scale_y(self.sin_cos_box_height), requestedColor)
			
		# Force some special cases to be rounded values
		if angle_deg == 30.0 or angle_deg == 150.0 or angle_deg == 390.0 or angle_deg == 510.0 or angle_deg == -210.0 or angle_deg == -330.0:
			sin_str = "sine = 0.5"
		elif angle_deg == 210.0 or angle_deg == 330.0 or angle_deg == 570.0 or angle_deg == -30.0 or angle_deg == -150.0 or angle_deg == -390.0:
			sin_str = "sine = -0.5"
		elif (angle_deg % 180.0 == 0.0):
			sin_str = "sine = 0.0"
		else:
			sin_str = "sine = " + str(sinOfAngle)

		self.text_sin_id = self.app_canvas.create_text(self.scale_x(self.UpperLeft_x_sin)+(self.scale_x(self.box_width)/2.0), 
						self.scale_y(self.UpperLeft_y_sin)-self.scale_y(20), 	text=sin_str, font=("Helvetica", self.primary_font_size, "bold"), 
						fill=self.rgb_to_hex((255, 0, 0))) #  red

	def CosBox(self, angle_deg, last_angle_deg, cosOfAngle):
		cosBoxColor = self.rgb_to_hex((255, 255, 255)) # white
		if( self.firstCycle ):

			self.app_canvas.create_rectangle(
    			self.scale_x(self.UpperLeft_x_cos), self.scale_y(self.UpperLeft_y_cos), # x1, y1
    			self.scale_x(self.UpperLeft_x_cos)+self.scale_x(self.box_width), self.scale_y(self.UpperLeft_y_cos)+self.scale_y(self.sin_cos_box_height),  # x2, y2
    			outline=cosBoxColor,    # border color
    			fill=cosBoxColor,   # inside color
    			width=3   )          # border thickness

			# Annotate the y axis
			x = self.scale_x(self.UpperLeft_x_cos)-self.scale_x(20)
			y = self.scale_y(self.UpperLeft_y_cos)
			self.app_canvas.create_text(x, y, text = "1", font=("Helvetica", self.small_font_size))

			x = self.scale_x(self.UpperLeft_x_cos)-self.scale_x(20)
			y = self.scale_y(self.UpperLeft_y_cos)+self.scale_y(self.sin_cos_box_height)
			self.app_canvas.create_text(x, y, text = "-1", font=("Helvetica", self.small_font_size))

			x = self.scale_x(self.UpperLeft_x_cos)-self.scale_x(20)
			y = self.scale_y(self.UpperLeft_y_cos)+(0.5*self.scale_y(self.sin_cos_box_height))
			self.app_canvas.create_text(x, y, text = "0", font=("Helvetica", self.small_font_size))

			# draw a horizontal gray line at y = 0
			x1 = self.scale_x(self.UpperLeft_x_cos)
			y1 = self.scale_y(self.UpperLeft_y_cos)+(0.5*self.scale_y(self.sin_cos_box_height))
			x2 = self.scale_x(self.UpperLeft_x_cos)+self.scale_x(self.box_width)
			y2 = self.scale_y(self.UpperLeft_y_cos)+(0.5*self.scale_y(self.sin_cos_box_height))
			self.app_canvas.create_line(x1, y1, x2, y2, fill =self.rgb_to_hex(self.medium_gray_color), width = 1)

			# draw the entire cos function from graphMinInDegrees to graphMaxInDegrees
			thisAngle_deg = self.graphMinInDegrees
			while thisAngle_deg <= self.graphMaxInDegrees:
				self.DrawCosPoint(thisAngle_deg)
				thisAngle_deg += 1.0

		else:
			if last_angle_deg >= self.graphMinInDegrees and last_angle_deg <= self.graphMaxInDegrees:
				self.app_canvas.delete(self.cos_line_id)  # remove the last blue cos line that we drew
			self.app_canvas.delete(self.text_cos_id)  # remove the text that was written during the previous cycle

		if angle_deg >= self.graphMinInDegrees and angle_deg <= self.graphMaxInDegrees:
			# draw a vertical dark blue line to show the cos of the angle that the user selected
			requestedColor = self.rgb_to_hex((0, 0, 255)) # red
			self.cos_line_id = self.verticalLine(angle_deg, self.scale_x(self.UpperLeft_x_cos), self.scale_y(self.UpperLeft_y_cos), self.scale_x(self.box_width), 
										self.scale_y(self.sin_cos_box_height), requestedColor)

		# Force some special cases to be rounded values
		if(angle_deg == 60.0 or angle_deg == -60.0):
			cos_str = "cosine = 0.5"
		elif (angle_deg % 180.0 == 90.0):
			cos_str = "cosine = 0.0"
		else:
			cos_str = "cosine = " + str(cosOfAngle)

		self.text_cos_id = self.app_canvas.create_text(self.scale_x(self.UpperLeft_x_cos)+(self.scale_x(self.box_width)/2.0), 
						self.scale_y(self.UpperLeft_y_cos)-self.scale_y(20), 	text=cos_str, font=("Helvetica", self.primary_font_size, "bold"), 
						fill=self.rgb_to_hex((0, 0, 255))) #  red

	def TanBox(self, angle_deg, last_angle_deg, tanOfAngle):
		tanBoxColor = self.rgb_to_hex((255, 255, 255)) # white
		if( self.firstCycle ):
		
			self.app_canvas.create_rectangle(
    			self.scale_x(self.UpperLeft_x_tan), self.scale_y(self.UpperLeft_y_tan), # x1, y1
    			self.scale_x(self.UpperLeft_x_tan)+self.scale_x(self.box_width), self.scale_y(self.UpperLeft_y_tan)+self.scale_y(self.tan_box_height),  # x2, y2
    			outline=tanBoxColor,    # border color
    			fill=tanBoxColor,   # inside color
    			width=2   )          # border thickness

			# Annotate the y axis
			x = self.scale_x(self.UpperLeft_x_tan)-self.scale_x(31)
			y = self.scale_y(self.UpperLeft_y_tan)
			tan_y_anno_top_id =self.app_canvas.create_text(x, y, text = "7.35", font=("Helvetica", self.small_font_size))
			x = self.scale_x(self.UpperLeft_x_tan)-self.scale_x(31)
			y = self.scale_y(self.UpperLeft_y_tan)+self.scale_y(self.tan_box_height)
			tan_y_anno_bottom_id =self.app_canvas.create_text(x, y, text = "-7.35", font=("Helvetica", self.small_font_size))
			x = self.scale_x(self.UpperLeft_x_tan)-self.scale_x(31)
			y = self.scale_y(self.UpperLeft_y_tan)+(0.5*self.scale_y(self.tan_box_height))
			tan_y_anno_bottom_id =self.app_canvas.create_text(x, y, text = "0", font=("Helvetica", self.small_font_size))

			# draw a horizontal gray line at y = 0
			x1 = self.scale_x(self.UpperLeft_x_tan)
			y1 = self.scale_y(self.UpperLeft_y_tan)+(0.5*self.scale_y(self.tan_box_height))
			x2 = self.scale_x(self.UpperLeft_x_tan)+self.scale_x(self.box_width)
			y2 = self.scale_y(self.UpperLeft_y_tan)+(0.5*self.scale_y(self.tan_box_height))
			x_axis_zero_id = self.app_canvas.create_line(x1, y1, x2, y2, fill =self.rgb_to_hex(self.medium_gray_color), width = 1)

			# draw the entire tan function from graphMinInDegrees to graphMaxInDegrees
			thisAngle_deg = self.graphMinInDegrees
			while thisAngle_deg <= self.graphMaxInDegrees:
				self.DrawTanPoint(thisAngle_deg)
				thisAngle_deg += 0.1

		else: 
			if last_angle_deg >= self.graphMinInDegrees and last_angle_deg <= self.graphMaxInDegrees:
				self.app_canvas.delete(self.tan_line_id)  # remove the last black vertical line that we drew
			self.app_canvas.delete(self.text_tan_id)  # remove the text that was written during the previous cycle
			
		if angle_deg >= self.graphMinInDegrees and angle_deg <= self.graphMaxInDegrees:
			# draw a vertical black line to show the tan of the angle that the user selected
			requestedColor = self.rgb_to_hex((0, 0, 0)) # black
			self.tan_line_id = self.verticalLine(angle_deg, self.scale_x(self.UpperLeft_x_tan), self.scale_y(self.UpperLeft_y_tan), 
								   self.scale_x(self.box_width), self.scale_y(self.tan_box_height), requestedColor)

		# Force some special cases to be rounded values
		if (angle_deg % 180.0 == 0.0):
			tan_str = "tangent = 0.0"
		elif(angle_deg % 180.0 == 90.0):
			tan_str = "tangent = Undefined"
		elif (angle_deg == -315.0 or angle_deg == -135.0 or angle_deg == 45.0 or angle_deg == 225.0 or angle_deg == 405.0 or angle_deg == 585.0):	
			tan_str = "tangent = 1.0"
		elif (angle_deg == -225.0 or angle_deg == -45.0 or angle_deg == 135.0 or angle_deg == 315.0 or angle_deg == 495.0 or angle_deg == 675.0):	
			tan_str = "tangent = -1.0"
		else:
			tan_str = "tangent = " + str(tanOfAngle)

		self.text_tan_id = self.app_canvas.create_text(self.scale_x(self.UpperLeft_x_tan)+(self.scale_x(self.box_width)/2.0), 
				self.scale_y(self.UpperLeft_y_tan)-self.scale_y(20), 	text=tan_str, font=("Helvetica", self.primary_font_size, "bold"))
				
	def verticalLine(self, angle_deg_requested, UpperLeft_x, UpperLeft_y, width, height, requestedColor):
		# draw a vertical line to show the function value at the requested angle

		x_position = UpperLeft_x+(width / self.graphSpan)*(angle_deg_requested-self.graphMinInDegrees)
		x1 = x_position
		y1 =  UpperLeft_y
		x2 = x_position
		y2 = UpperLeft_y+height
		line_id = self.app_canvas.create_line(x1, y1, x2, y2, fill = requestedColor, width = 1)
		return line_id
		
	def WriteAngleValues(self, text_y, angle_deg, angle_rad):

		angle_rad_round = round(angle_rad, self.Rounding_Num_Digits)

		angle_deg_str = 'angle in degrees = ' + str(angle_deg)
		angle_rad_str = 'angle in radians = ' + str(angle_rad_round)

		if(not self.firstCycle): 
			self.app_canvas.delete(self.text_angle_deg_id)  # Erase the text that was written during the previous cycle
			self.app_canvas.delete(self.text_angle_rad_id)  # Erase the text that was written during the previous cycle

		local_font_size = None
		if self.this_screen_width > self.width_threshold:
			local_font_size = self.primary_font_size
		else:
			local_font_size = self.small_font_size #   # for tiny keyboards, we have to use a small font

		self.text_angle_deg_id = self.app_canvas.create_text(self.scale_x(self.text_x), self.scale_y(text_y)+self.scale_y(43), text=angle_deg_str, 
												  font=("Helvetica", self.primary_font_size, "bold"))

		self.text_angle_rad_id = self.app_canvas.create_text(self.scale_x(self.text_x), self.scale_y(text_y)+self.scale_y(48)+self.scale_y(self.line_height), text=angle_rad_str, 
												  font=("Helvetica", local_font_size))	

	def process_range(self, run_type_str, angle_deg_left_float, angle_deg_right_float):
		angle = angle_deg_left_float
		self.process_one_angle(run_type_str, angle)
		if angle_deg_left_float < angle_deg_right_float:
			while angle+self.bump_delta <= angle_deg_right_float:
				angle += self.bump_delta
				self.process_one_angle(run_type_str, angle)
				self.app_canvas.update()
		else:
			while angle-self.bump_delta >= angle_deg_right_float:
				angle -= self.bump_delta
				self.process_one_angle(run_type_str, angle)
				self.app_canvas.update()

	def process_one_angle(self, run_type_str, angle_deg):

		x_right = self.x_left + self.box_width
		y_position_annotation = self.UpperLeft_y_tan + self.tan_box_height + 30
				
		if self.last_run_type_str == 'none_yet':
			self.last_angle_deg = self.last_angle_deg_left
		elif self.last_run_type_str == 'single_left':
			self.last_angle_deg = self.last_angle_deg_left
		elif self.last_run_type_str == 'single_right':
			last_angle_deg = self.last_angle_deg_right
		elif self.last_run_type_str == 'range':
			self.last_angle_deg = self.last_angle_deg_left
				
		self.last_run_type_str = run_type_str
		
		angle_rad = angle_deg * math.pi / 180.0
				
		if run_type_str == 'single_left' or run_type_str == 'single_right':
			self.draw_one_angle (angle_deg, angle_rad, self.last_angle_deg)
		elif run_type_str == 'range':
			self.draw_one_angle (angle_deg, angle_rad, self.last_angle_deg)

		if run_type_str == 'single_left':
			self.last_angle_deg_left = angle_deg
		elif run_type_str == 'single_right':
			last_angle_deg_right = angle_deg
		elif run_type_str == 'range':
			self.last_angle_deg_left = angle_deg

		self.last_angle_deg = angle_deg

		if self.firstCycle:
			self.x_annotation(self.graphMinInDegrees, x_right, self.graphMaxInDegrees, y_position_annotation)
		self.firstCycle = False	
								
	def draw_one_angle(self, angle_deg, angle_rad, last_angle_deg):

		sinOfAngle = round(math.sin(angle_rad), self.Rounding_Num_Digits)  #  Too many digits can be distracting to the user, so round
		cosOfAngle = round(math.cos(angle_rad), self.Rounding_Num_Digits)
		tanOfAngle = round(math.tan(angle_rad), self.Rounding_Num_Digits)

		self.WriteAngleValues(self.scale_y(self.angle_values_location_y), angle_deg, angle_rad)

		self.SinBox(angle_deg, last_angle_deg, sinOfAngle)

		self.CosBox(angle_deg, last_angle_deg, cosOfAngle)

		self.TanBox(angle_deg, last_angle_deg, tanOfAngle)

		self.UC_instance.Unit_Circle_draw_triangle(sinOfAngle, cosOfAngle, self)

	def process_bump(self, direction):  #direction = up or down
		if direction == 'up':
			new_angle = self.last_angle_deg + self.bump_delta
		elif direction == 'down':
			new_angle = self.last_angle_deg - self.bump_delta
		self.process_one_angle('single_left', new_angle)
		
	def get_inputs(self):

			text_left_str = self.input_box_left.get()
			text_right_str = self.input_box_right.get()

			self.inText_left = text_left_str
			self.inText_right = text_right_str
			
			angle_deg_left_float = 0.0
			angle_deg_right_float = 0.0
			
			status_int = self.test_inputs ( text_left_str, text_right_str )
			run_type_str = 'none_yet'
			
			if status_int == 1:    #left input is good and right input is good
				run_type_str = 'range'
				angle_deg_left_float = float(text_left_str)
				angle_deg_right_float = float(text_right_str)
			elif status_int == 2: #if left input is good and right input is blank
				run_type_str = 'single_left'
				angle_deg_left_float = float(text_left_str)
			elif status_int == 3:   #right input is good and left input is blank
				run_type_str = 'single_right'
				angle_deg_right_float = float(text_right_str)
			elif status_int == 4:   #both inputs are blank
				run_type_str = 'no_run'
				ErrorWindow_instance = ErrWindow.ErrorWindow(self)
				ErrorWindow_instance.showErrorWindow(text_left_str)
			elif status_int == 5:   #left input is invalid
				run_type_str = 'no_run'
				ErrorWindow_instance = ErrWindow.ErrorWindow(self)
				ErrorWindow_instance.showErrorWindow(text_left_str)
			elif status_int == 6:   #right input is invalid
				run_type_str = 'no_run'
				ErrorWindow_instance = ErrWindow.ErrorWindow(self)
				ErrorWindow_instance.showErrorWindow(text_right_str)
				
			self.input_box_left.delete(0, tk.END) # clear text so that user can input another one if desired
			text_left_str = ""               # clear text so that user can input another one if desired

			self.input_box_right.delete(0, tk.END) # clear text so that user can input another one if desired
			text_right_str = ""               # clear text so that user can input another one if desired     

			return run_type_str, angle_deg_left_float, angle_deg_right_float
				
	def test_inputs ( self, text_left_str, text_right_str ):
	#  returns 1 if left input is good and right input is good
	#          2 if left input is good and right input is blank
	#          3 if right input is good and left input is blank
	#          4 if both inputs are blank
	#          5 if left number is invalid
	#          6 if right number is invalid

		status_left_str = 'none_yet'
		status_right_str = 'none_yet'
		
		if text_left_str == '':
			status_left_str = 'blank'
		if text_right_str == '':
			status_right_str = 'blank'

		if status_left_str != 'blank':
			try:
				test_x = float(text_left_str)
				status_left_str = 'good_number'
			except ValueError:
				status_left_str = 'bad_number'
				
		if status_right_str != 'blank':
			try:
				test_x = float(text_right_str)
				status_right_str = 'good_number'
			except ValueError:
				status_right_str = 'bad_number'
			
		ret_value_int = 0       
		if status_left_str == 'good_number' and status_right_str == 'good_number':
			ret_value_int = 1
		elif status_left_str == 'good_number' and status_right_str == 'blank':
			ret_value_int = 2
		elif status_left_str == 'blank' and status_right_str == 'good_number':
			ret_value_int = 3
		elif status_left_str == 'blank' and status_right_str == 'blank':
			ret_value_int = 4
		elif status_left_str == 'bad_number':
			ret_value_int = 5
		elif status_right_str == 'bad_number':
			ret_value_int = 6
			
		return ret_value_int

	def show_bump_buttons(self):
		self.setup_instance.bump_up_button.config(state="normal")     # restore the two bump buttons
		self.setup_instance.bump_down_button.config(state="normal")

	def rgb_to_hex(self, rgb):
		# Convert (R, G, B) tuple to hex string.
		return "#%02x%02x%02x" % rgb
			
	def handle_custom_event_go(self, event):  # this function defines what will be done when the user presses the Go button
		
			run_type_str, angle_deg_left_float, angle_deg_right_float = self.get_inputs()

			if self.this_screen_width > self.width_threshold:
				# The ghost labels let the user see what they typed after they type a selection
				self.app_canvas.delete(self.ghost_label_left_id)  # remove the previous value for this label
				self.app_canvas.delete(self.ghost_label_right_id)  # remove the previous value for this label

				self.ghost_label_left_id =self.app_canvas.create_text(self.input_box_L_x - self.scale_x(60), self.scale_y(self.input_box_location_y) + self.scale_y(49),
										text = self.inText_left, font=("Helvetica", self.small_font_size), fill=self.rgb_to_hex(self.light_gray_color))
				self.ghost_label_right_id =self.app_canvas.create_text(self.input_box_R_x - self.scale_x(20), self.scale_y(self.input_box_location_y) + self.scale_y(49),
										text = self.inText_right, font=("Helvetica", self.small_font_size), fill=self.rgb_to_hex(self.light_gray_color))
				# Attach tooltip to the ghost values
				Tooltip_Classes.ToolTip_For_Canvas_Items(self.app_canvas, self.ghost_label_left_id, "This is the last angle value you typed above")
				Tooltip_Classes.ToolTip_For_Canvas_Items(self.app_canvas, self.ghost_label_right_id, "This is the last angle value you typed above")
		
			self.input_box_left.focus_set() 

			if run_type_str == 'single_left':
				self.process_one_angle(run_type_str, angle_deg_left_float)
				self.show_bump_buttons()     # restore the bump buttons
			elif run_type_str == 'single_right':
				self.process_one_angle(run_type_str, angle_deg_right_float)
				self.show_bump_buttons()
			elif run_type_str == 'range':
				self.setup_instance.bump_up_button.config(state="disabled")    # disable the bump buttons
				self.setup_instance.bump_down_button.config(state="disabled")
				self.process_range(run_type_str, angle_deg_left_float, angle_deg_right_float)
				self.show_bump_buttons()

	def run(self):

		self.root.mainloop()		

	
# Create and run the program.   This program is event driven.  See event <<ButtonClickedGo>>)
if __name__ == "__main__":
    TF = TrigFundamentals()
    TF.screen_calculations() # uses device resolution to scale the app window and widgets
    TF.setup_instance.create_Widgets(TF) # place the widgets opn the screen
	# The screen is now populated, the program is now waiting for the user to do something
    TF.run()