import tkinter as tk

class ErrorWindow():
	def __init__(self, TF_instance):
		self.rootErrorWindow = None
		self.TF_instance = TF_instance

	def showErrorWindow(self, text):

		err_window_width = self.TF_instance.scale_x(720)
		err_window_height = self.TF_instance.scale_y(160)
		self.rootErrorWindow = tk.Tk()
		self.rootErrorWindow.title("Input error")
		self.rootErrorWindow.geometry(str(err_window_width) + "x" + str(err_window_height))
		self.rootErrorWindow.resizable(False, False)

		root_errwindow = self.rootErrorWindow.winfo_toplevel()
		#root_errwindow.overrideredirect(1)  # get rid of the title bar of the main window

		# Set the err window position
		err_x_pos = int(self.TF_instance.this_screen_width / 2) - int(err_window_width / 2) 
		err_y_pos = int(self.TF_instance.this_screen_height / 2) - int(err_window_height / 2)
		self.rootErrorWindow.geometry(f"+{err_x_pos}+{err_y_pos}")  # position the app window centered on the screen

		  # Create canvas
		red = self.TF_instance.rgb_to_hex((255, 0, 0))
		err_canvas = tk.Canvas(self.rootErrorWindow, width=err_window_width, height=err_window_height, bg=red)
		err_canvas.pack()

		def close_window():
			self.rootErrorWindow.destroy()   # closes the red error window

		err_msg = ""
		if len(text) > 0:
			err_msg = "[" + text + "] is not a valid number."
		else:
			err_msg = "You must type in an angle value in degrees before proceeding"

		err_canvas.create_text(int(err_window_width / 2), self.TF_instance.scale_y(25), text=err_msg, font=("Helvetica", self.TF_instance.scale_x(16)))

		err_msg_2 = "Touch (or click) the close button in this red window and then try again."

		err_canvas.create_text(int(err_window_width / 2), self.TF_instance.scale_y(60), text=err_msg_2, font=("Helvetica", self.TF_instance.scale_x(16)))

		close_button = tk.Button(self.rootErrorWindow, text = 'Close', command = close_window, font = ('Helvetica', self.TF_instance.button_font_size))
		close_button.place(x=int(err_window_width / 2) - self.TF_instance.scale_x(25), y=int(err_window_height * 5 / 8))
