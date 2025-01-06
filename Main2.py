import tkinter as tk
from tkinter import simpledialog
import math
import random
import time
AvgTime= []
points = []
radius = 1
max_points = 0
point_size = 2
precomputed_centers = {}
cursor_size = 1
def add_point(event):
    x, y = event.x, event.y
    points.append((x, y))
    canvas.create_oval(x - point_size, y - point_size, x + point_size, y + point_size, fill="white")
def activate_circle(event):
    x, y = event.x, event.y
    canvas.delete("circle")
    global max_points, precomputed_centers, AvgTime
    start_time = time.time()
    count = 0
    for px, py in points:
        dist = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
        dist2 = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
        if dist <= radius or dist2 <= radius:
            count = count + 1
    if count > max_points:
        max_points = count
        precomputed_centers = {(x, y): count}
    elif count == max_points:
        precomputed_centers[(x, y)] = count
    end_time = time.time()
    Runtime = end_time - start_time
    AvgTime.append(Runtime)
    color = "green" if (x,y) in precomputed_centers  else "red"
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=color, tags="circle", width=2)
    max_points_label.config(text=f"Max Points: {max_points}")
def generate_points():
    num_points = simpledialog.askinteger("Generate Points", "Enter the number of points to generate:")
    if num_points is not None and num_points > 0:
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        for _ in range(num_points):
            x = random.randint(0, canvas_width)
            y = random.randint(0, canvas_height)
            points.append((x, y))
            canvas.create_oval(x - point_size, y - point_size, x + point_size, y + point_size, fill="white")

def set_radius():
    global radius
    radius = simpledialog.askfloat("Input Radius", "Enter circle radius:")
    if radius is not None:
        radius_label.config(text=f"Radius: {radius}")
def clear_canvas():
    global points, max_points, precomputed_centers
    points = []
    max_points = 0
    precomputed_centers = {}
    canvas.delete("all")
    radius_label.config(text="Radius: 0")
    max_points_label.config(text="Max Points: 0")
def quit_app():
    root.destroy()
def activate_functionality(new_functionality):
    global active_functionality
    active_functionality = new_functionality
    canvas.unbind("<Button-1>")
    canvas.unbind("<Motion>")
    if active_functionality == "add_points":
        canvas.bind("<Button-1>", add_point)
    elif active_functionality == "activate_circle":
        canvas.bind("<Motion>", activate_circle)
    add_points_btn.config(state="normal" if active_functionality != "add_points" else "disabled")
    activate_circle_btn.config(state="normal" if active_functionality != "activate_circle" else "disabled")
    clear_canvas_btn.config(state="normal" if active_functionality != "clear_canvas" else "disabled")
    radius_btn.config(state="normal")
    quit_btn.config(state="normal")
root = tk.Tk()
root.title("Facility location")
root.geometry("1280x720")
canvas = tk.Canvas(root, width=1280, height=720, bg="black")
canvas.pack()
control_frame = tk.Frame(root, bg="black")
control_frame.pack(side=tk.BOTTOM, fill=tk.X)
add_points_btn = tk.Button(control_frame, text="Add Points", command=lambda: activate_functionality("add_points"))
add_points_btn.pack(side=tk.LEFT)
generate_points_btn = tk.Button(control_frame, text="Generate Points", command=generate_points)
generate_points_btn.pack(side=tk.LEFT)
activate_circle_btn = tk.Button(control_frame, text="Activate Circle",
                                 command=lambda: activate_functionality("activate_circle"))
activate_circle_btn.pack(side=tk.LEFT)
clear_canvas_btn = tk.Button(control_frame, text="Clear Canvas", command=clear_canvas)
clear_canvas_btn.pack(side=tk.LEFT)
radius_btn = tk.Button(control_frame, text="Set Radius", command=set_radius)
radius_btn.pack(side=tk.LEFT)
radius_label = tk.Label(control_frame, text="Radius: 0", bg="black", fg="white")
radius_label.pack(side=tk.LEFT)
max_points_label = tk.Label(control_frame, text="Max Points: 0", bg="black", fg="white")
max_points_label.pack(side=tk.LEFT)
quit_btn = tk.Button(control_frame, text="Quit", command=quit_app)
quit_btn.pack(side=tk.RIGHT)
root.mainloop()
average= sum(AvgTime)/len(AvgTime)
print(f"Average runtime: {average}")