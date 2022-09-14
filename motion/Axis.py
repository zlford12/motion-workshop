from motion.AxisData import AxisData
from motion.AxisLimits import AxisLimits


class Axis:
    def __init__(self):
        self.axis_limits = AxisLimits()
        self.axis_data = AxisData()
