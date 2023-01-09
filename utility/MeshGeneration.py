from math import atan, degrees
import struct
from tkinter import filedialog, messagebox


class Point:
    def __init__(self):
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.Gx = 0.0
        self.Gy = 0.0
        self.Gz = 0.0


def generate_mesh():
    # Polynomial Coefficients
    a = -1.0e-5
    b = 5.0e-3
    c = 6.0e-2
    d = 1.0e+2

    def y(x):
        return (a * pow(x, 3)) + (b * pow(x, 2)) + (c * pow(x, 1)) + d

    def gz(p: Point):
        slope = 0
        coefficients = [d, c, b, a]
        intercept = coefficients[0]
        x = p.X

        for j, coefficient in enumerate(coefficients):
            if j != 0:
                slope = slope + (coefficient * j * pow(x, j - 1))
                intercept = intercept + (coefficient * pow(x, j))

        return degrees(atan(slope))

    # Mesh Generation Parameters
    x_start = 0.0
    x_stop = 500.0
    x_resolution = 0.01
    z_start = 150.0
    z_stop = 200.0
    z_resolution = 5.0

    # Calculate Polynomial
    first_line: [Point] = []
    x_calc = x_start
    y_calc = y(x_calc)
    z_calc = z_start
    travel = 0.0
    last_x = x_calc
    last_y = y_calc

    while x_calc <= x_stop:
        y_calc = y(x_calc)
        travel = travel + pow(pow(x_calc - last_x, 2) + pow(y_calc - last_y, 2), 0.5)

        if (travel >= z_resolution) or (x_calc == x_start):
            travel = 0.0
            current_point = Point()
            current_point.X = x_calc
            current_point.Y = y_calc
            current_point.Z = z_calc
            first_line.append(current_point)

        last_x = x_calc
        last_y = y_calc
        x_calc = x_calc + x_resolution

    # Copy First Line In Z Direction
    mesh_points: [Point] = []
    current_line = first_line
    scan_dimension = len(first_line)
    index_dimension = 0

    while z_calc <= z_stop:
        for point in current_line:
            current_point = Point()
            current_point.X = point.X
            current_point.Y = point.Y
            current_point.Z = point.Z
            mesh_points.append(current_point)
        index_dimension = index_dimension + 1
        z_calc = z_calc + z_resolution

        for i in range(len(current_line)):
            current_line[i].Z = z_calc

    # Calculate Normals
    for point in mesh_points:
        point.Gz = gz(point)

    # Create Mesh File
    mesh_file = filedialog.asksaveasfilename(filetypes=[("Mesh File", "*.mesh")], defaultextension=".mesh")
    if ".mesh" not in mesh_file:
        messagebox.showerror(
            title="File Error",
            message="Mesh File Invalid"
        )
        return
    mesh = open(mesh_file, "wb")

    # Write Parameters
    mesh.write(struct.pack('f', float(scan_dimension)))
    mesh.write(struct.pack('f', float(index_dimension)))
    mesh.write(struct.pack('f', z_resolution))
    mesh.write(struct.pack('f', 0.0))
    mesh.write(struct.pack('f', 0.0))
    mesh.write(struct.pack('f', 0.0))
    mesh.write(struct.pack('f', 0.0))
    mesh.write(struct.pack('f', 0.0))

    # Write Points
    for point in mesh_points:
        mesh.write(struct.pack('f', float(point.X)))
        mesh.write(struct.pack('f', float(point.Y)))
        mesh.write(struct.pack('f', float(point.Z)))
        mesh.write(struct.pack('f', float(point.Gx)))
        mesh.write(struct.pack('f', float(point.Gy)))
        mesh.write(struct.pack('f', float(point.Gz)))
        mesh.write(struct.pack('b', True))

    mesh.close()

    print(scan_dimension, index_dimension)
