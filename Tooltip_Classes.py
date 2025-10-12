import tkinter as tk

class ToolTip:    # I got the code for this Tooltip class from ChatGPT (it works for tkinter widgets)
    def __init__(self, widget, text="Tooltip text"):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.move_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert") or (0, 0, 0, 0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20

        # Create a top-level window for the tooltip
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove window decorations
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Helvetica", 10)
        )
        label.pack(ipadx=5, ipady=3)

    def move_tooltip(self, event):
        if self.tooltip_window:
            x = event.x_root + 20
            y = event.y_root + 10
            self.tooltip_window.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class ToolTip_For_Canvas_Items:    # I got the code for this second Tooltip class from ChatGPT (it works for canvas items)
    def __init__(self, canvas, item, text): # I modified the code to add a yellow background for each tooltip
        self.canvas = canvas
        self.item = item
        self.text = text
        self.tooltip = None
        self.rect_id = None

        # Bind mouse events to the line
        canvas.tag_bind(item, "<Enter>", self.show_tooltip)
        canvas.tag_bind(item, "<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip is None:
            x, y = event.x + 10, event.y + 3
            self.tooltip = self.canvas.create_text(
                x, y, text=self.text, anchor="nw",
                fill="black", font=("Helvetica", 10),
                tags="tooltip")

			# Get the bounding box of the text
            bbox = self.canvas.bbox(self.tooltip)  # returns (x1, y1, x2, y2)

			# Create a yellow rectangle behind it (for background color)
            self.rect_id = self.canvas.create_rectangle(bbox, fill="#ffffe0", outline="black")

			# Move the text on top of the rectangle
            self.canvas.tag_lower(self.rect_id, self.tooltip)
            
    def hide_tooltip(self, event):
        if self.tooltip:
            self.canvas.delete(self.tooltip)
            self.canvas.delete(self.rect_id)  # remove the rectangle
            self.tooltip = None