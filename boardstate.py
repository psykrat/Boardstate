import tkinter as tk
from tkinter import simpledialog, messagebox
from functools import partial

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
MID_X = CANVAS_WIDTH // 2
MID_Y = CANVAS_HEIGHT // 2
BUTTON_Y_TOP = 10
BUTTON_Y_BOTTOM = 560
BUTTON_X_LEFT = 10
BUTTON_X_RIGHT = 760

class CreatureDialog(simpledialog.Dialog):
    
    def body(self, master):
        tk.Label(master, text="Enter value (x/x):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.value_entry = tk.Entry(master)
        self.value_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(master, text="Enter creature description:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.desc_entry = tk.Entry(master)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        return self.value_entry

    def apply(self):
        self.result = (self.value_entry.get(), self.desc_entry.get())

class MTGBoardState(tk.Tk):
    
    def __init__(self):
        super().__init__()
        # Get screen width and height
        self.SCREEN_WIDTH = self.winfo_screenwidth()
        self.SCREEN_HEIGHT = self.winfo_screenheight()
        self.MID_X = self.SCREEN_WIDTH // 2
        self.MID_Y = self.SCREEN_HEIGHT // 2
        self.BUTTON_Y_TOP = 10
        self.BUTTON_Y_BOTTOM = self.SCREEN_HEIGHT - 40
        self.BUTTON_X_LEFT = 10
        self.BUTTON_X_RIGHT = self.SCREEN_WIDTH - 40
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.creature_count = 0

        self.setup_window()
        self.setup_canvas()
        self.setup_buttons()

    def setup_window(self):
        self.title("MTG Board State")

    def setup_canvas(self):
        default_bg = self.cget("bg")
        self.canvas = tk.Canvas(self, bg=default_bg, width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT)
        self.canvas.pack()
        self.canvas.create_line(self.MID_X, 0, self.MID_X, self.SCREEN_HEIGHT, fill="black", width=2)
        self.canvas.create_line(0, self.MID_Y, self.SCREEN_WIDTH, self.MID_Y, fill="black", width=2)
        self.corners = {
            "Top Left": [],
            "Top Right": [],
            "Bottom Left": [],
            "Bottom Right": []
        }
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.dragging)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<Button-3>", self.generic_right_click)

    def setup_buttons(self):
        self.add_buttons = {
            "Top Left": tk.Button(self, text="+", command=lambda: self.add_creature("Top Left")),
            "Top Right": tk.Button(self, text="+", command=lambda: self.add_creature("Top Right")),
            "Bottom Left": tk.Button(self, text="+", command=lambda: self.add_creature("Bottom Left")),
            "Bottom Right": tk.Button(self, text="+", command=lambda: self.add_creature("Bottom Right")),
        }
        for position, button in self.add_buttons.items():
            x = self.BUTTON_X_LEFT if "Left" in position else self.BUTTON_X_RIGHT
            y = self.BUTTON_Y_TOP if "Top" in position else self.BUTTON_Y_BOTTOM
            button.place(x=x, y=y)

    def generic_right_click(self, event):
        x, y = event.x, event.y

    def add_creature(self, position):
        dialog = CreatureDialog(self)
        if dialog.result:
            value, creature_desc = dialog.result
            if self.validate_input(value):
                if "Left" in position:
                    x = self.BUTTON_X_LEFT + 50 + len(self.corners[position]) * 70
                else:
                    x = self.BUTTON_X_RIGHT - 50 - len(self.corners[position]) * 70
                
                prev_y = self.BUTTON_Y_TOP + 50 if "Top" in position else self.BUTTON_Y_BOTTOM - 50
                total_height = sum([frame.winfo_height() for frame in self.corners[position]])
                y = prev_y + total_height

                self.display_creature(value, creature_desc, x, y, position)
            else:
                messagebox.showerror("Error", "Please input valid integers in the format x/x.")

    def validate_input(self, value):
        if "/" in value:
            x_val, y_val = value.split('/')
            return x_val.isdigit() and y_val.isdigit()
        return False

    def display_creature(self, value, desc, x, y, position):
        self.creature_count += 1
        creature_tag = f"creature_{self.creature_count}"
        drag_tag = f"drag_{self.creature_count}"
        self.canvas.create_text(x, y, text=value, font=("Arial", 24), anchor=tk.CENTER, tags=(creature_tag, 'draggable', drag_tag))
        self.canvas.create_text(x, y + 30, text=desc, font=("Arial", 14), anchor=tk.CENTER, tags=(creature_tag, 'draggable', drag_tag))
        
        callback = partial(self.on_right_click, creature_tag)
        self.canvas.tag_bind(creature_tag, "<Button-3>", callback)

    def on_right_click(self, creature_tag, event):
        self.show_context_menu(event, creature_tag)

    def show_context_menu(self, event, creature_tag):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Modify Value", command=lambda: self.modify_creature_value(creature_tag))
        context_menu.add_command(label="Modify Description", command=lambda: self.modify_creature_description(creature_tag))  # New command
        context_menu.add_command(label="Delete", command=lambda: self.delete_creature(creature_tag))
        
        context_menu.post(event.x_root, event.y_root)

    def modify_creature_value(self, creature_tag):
        value = simpledialog.askstring("Input", "Enter the new value (format x/x):", parent=self)
        if value and self.validate_input(value):
            value_id = self.canvas.find_withtag(creature_tag)[0]
            self.canvas.itemconfig(value_id, text=value)

    def modify_creature_description(self, creature_tag):
        description = simpledialog.askstring("Input", "Enter the new description:", parent=self)
        if description:
            description_id = self.canvas.find_withtag(creature_tag)[1]
            self.canvas.itemconfig(description_id, text=description)

    def delete_creature(self, creature_tag):
        self.canvas.delete(creature_tag)

    def start_drag(self, event):
        items = self.canvas.find_withtag(tk.CURRENT)
        if items and 'draggable' in self.canvas.gettags(items[0]):
            self.drag_data["item"] = items[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def dragging(self, event):
        item = self.drag_data["item"]
        if item:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            tags = self.canvas.gettags(item)
            drag_tag = next((tag for tag in tags if "drag_" in tag), None)
            
            if drag_tag:
                items_to_move = self.canvas.find_withtag(drag_tag)
                for item_id in items_to_move:
                    self.canvas.move(item_id, dx, dy)
            
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def end_drag(self, event):
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def update_value(self, event, label_id):
        value = simpledialog.askstring("Input", "Enter the new value (format x/x):", parent=self)
        if value and self.validate_input(value):
            self.canvas.itemconfig(label_id, text=value)

if __name__ == "__main__":
    app = MTGBoardState()
    app.mainloop()
