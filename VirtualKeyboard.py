import tkinter as tk

class VirtualKeyboard():      # I got the code for this class from ChatGPT and then modified it for my purposes

        #    Virtual keyboard widget that can type into an existing Entry widget. (used for input)

    def __init__(self, kb_x, kb_y, width, app_canvas):
        self.width = width
        self.fill = "white"
        self.color = "black"
        self.font = ('Helvetica', 8)
        self.app_canvas = app_canvas
        self.kb_x = kb_x
        self.kb_y = kb_y

    def __repr__(self):
        return "VirtualKeyboard({}, {})".format(self.anchor, self.width)

    def _draw(self, this_screen_width, width_threshold):
        frm = tk.Frame(self.app_canvas, takefocus = 0, bg = 'dark gray')
        self.frm = frm
        self.show_kb_frame(this_screen_width, width_threshold)
        self.create_keyboard(frm)
        return #canvas.create_window(x,y,window=frm)

    def create_keyboard(self, frm):
   
        # Keyboard layout
        numeric_keys =["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".","-", "Enter","Backspace"]

        full_keyboard = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m", ",", ".", "?"],
            ["Space", "Clear"]
        ]

        # Build the keyboard
        for key in numeric_keys:
            action = lambda x=key: self.press_key(x)
            btn = tk.Button(
                    frm,   # was row_frame, not frm
                    text=key,
                    bg = 'white',
                    takefocus = 0,
                    width=5 if key not in ["Space", "Backspace", "Clear", "Enter"] else 8,
                    height=1,
                    font = ('Helvetica', 10),
                    command=action
                )
            btn.pack(side=tk.LEFT, padx=3)

    def press_key(self, key):

        focused_widget = self.app_canvas.focus_get()  #  get the object that currently has the focus

        if isinstance(focused_widget, tk.Entry):
            if key == "Backspace":
                current_text = focused_widget.get()
                focused_widget.delete(0, tk.END)
                focused_widget.insert(0, current_text[:-1])
            elif key == "Space":
                focused_widget.insert(tk.END, " ")
            elif key == "Clear":
                focused_widget.delete(0, tk.END)
            elif key == 'Enter':
                focused_widget.event_generate("<Return>")
            else:
                focused_widget.insert(tk.END, key)   # a good key was pressed (0-9 or decimal point)

    def hide_kb_frame(self):
        self.frm.pack_forget()

    def show_kb_frame(self, this_screen_width, width_threshold):
        local_kb_x = None
        if this_screen_width > width_threshold:
           local_kb_x = self.kb_x
        else:
           local_kb_x = 3  # for tiny keyboards, we have to hardcode a small amount
        self.frm.place(x=local_kb_x, y=self.kb_y)