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

    while z_calc <= z_stop:
        for point in current_line:
            current_point = Point()
            current_point.X = point.X
            current_point.Y = point.Y
            current_point.Z = point.Z
            mesh_points.append(current_point)
        z_calc = z_calc + z_resolution

        for i in range(len(current_line)):
            current_line[i].Z = z_calc

    for point in mesh_points:
        print(point.X, point.Y, point.Z)


generate_mesh()
