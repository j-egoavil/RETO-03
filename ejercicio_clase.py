class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class Line(Point):
    def __init__(self, start: Point, end: Point ) -> None:
        super().__init__(start.x, start.y)
        self.start = start
        self.end = end

    def compute_length(self) -> float:
        length = ((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2) ** 0.5
        return length
    
    def compute_slope(self):
        # Vertical line
        if (self.end.x - self.start.x) == 0:
            return None  
        slope: float = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        return slope
    
    def compute_vertical_crossing(self):
        # Intersection with y-axis (x=0)
        slope = self.compute_slope()
        if slope is None:
            return None
        crossing = self.start.y - (slope * self.start.x)  # y = mx + b  =>  b = y - mx
        return crossing

    def compute_horizontal_crossing(self):
        # Intersection with x-axis (y=0)
        slope = self.compute_slope()
        if slope == 0:
            return None  # Horizontal line has no crossing with x-axis
        if slope is None:
            return None  # Vertical line has no crossing with x-axis
        crossing = -(self.start.y - (slope * self.start.x)) / slope  # y = mx + b  =>  x = (y - b) / m
        return crossing
    
    def __str__(self) -> str:
        slope = self.compute_slope()
        slope_str = f"{slope:.2f}"
        v_cross = self.compute_vertical_crossing()
        h_cross = self.compute_horizontal_crossing()
        return (
            f"Length: {self.compute_length():.2f}, "
            f"Slope: {slope_str}, "
            f"Vertical crossing: {v_cross}, "
            f"Horizontal crossing: {h_cross}"
        )

class Rectangle:
    def __init__(self, method: int, *args):
        if method == 1:
            # Method 1: Bottom-left + width + height
            bottom_left, width, height = args
            self.width = width
            self.height = height
            self.center = Point(bottom_left.x + width/2, bottom_left.y + height/2)

        elif method == 2:
            # Method 2: Center + width + height
            center, width, height = args
            self.width = width
            self.height = height
            self.center = center

        elif method == 3:
            # Method 3: Two opposite points
            p1, p2 = args
            self.width = abs(p2.x - p1.x)
            self.height = abs(p2.y - p1.y)
            self.center = Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)

        elif method == 4:
            # Method 4: Four lines (composition)
            l1, l2, l3, l4 = args
            lines = [l1, l2, l3, l4]

            points = []
            for line in lines:
                points.append(line.start)
                points.append(line.end)

            xs = []
            ys = []
            for p in points:
                xs.append(p.x)
                ys.append(p.y)

            min_x = min(xs)
            max_x = max(xs)
            min_y = min(ys)
            max_y = max(ys)

            self.width = max_x - min_x
            self.height = max_y - min_y
            self.center = Point((min_x + max_x) / 2, (min_y + max_y) / 2)

        else:
            return "Error: Invalid method"

    def compute_area(self):
        return self.width * self.height

    def compute_perimeter(self):
        return 2 * (self.width + self.height)

    def compute_interference_point(self, point: Point) -> bool:
        x_min = self.center.x - self.width/2
        x_max = self.center.x + self.width/2
        y_min = self.center.y - self.height/2
        y_max = self.center.y + self.height/2
        return x_min <= point.x <= x_max and y_min <= point.y <= y_max


class Square(Rectangle):
    def __init__(self, method: int, *args):
        if method == 1:
            # Method 1: Bottom-left + side
            bottom_left, side = args
            super().__init__(1, bottom_left, side, side)
        elif method == 2:
            # Method 2: Center + side
            center, side = args
            super().__init__(2, center, side, side)
        elif method == 3:
            # Method 3: Two opposite points
            p1, p2 = args
            side = max(abs(p2.x - p1.x), abs(p2.y - p1.y))
            super().__init__(2, Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), side, side)
        else:
            raise ValueError("Error: Invalid method")

#Test
p1 = Point(0, 0)
p2 = Point(4, 0)
p3 = Point(4, 3)
p4 = Point(0, 3)

# Create 4 lines that form a rectangle
l1 = Line(p1, p2)
l2 = Line(p2, p3)
l3 = Line(p3, p4)
l4 = Line(p4, p1)

print("Test Rectangle")

# Method 1: Bottom-left + width + height
rect1 = Rectangle(1, Point(0, 0), 4, 3)
print("Method 1 -> Area:", rect1.compute_area(), 
      "Perimeter:", rect1.compute_perimeter(), 
      "Center:", (rect1.center.x, rect1.center.y))

# Method 2: Center + width + height
rect2 = Rectangle(2, Point(2, 1.5), 4, 3)
print("Method 2 -> Area:", rect2.compute_area(), 
      "Perimeter:", rect2.compute_perimeter(), 
      "Center:", (rect2.center.x, rect2.center.y))

# Method 3: Two opposite points
rect3 = Rectangle(3, Point(0, 0), Point(4, 3))
print("Method 3 -> Area:", rect3.compute_area(), 
      "Perimeter:", rect3.compute_perimeter(), 
      "Center:", (rect3.center.x, rect3.center.y))

# Method 4: Four lines
rect4 = Rectangle(4, l1, l2, l3, l4)
print("Method 4 -> Area:", rect4.compute_area(), 
      "Perimeter:", rect4.compute_perimeter(), 
      "Center:", (rect4.center.x, rect4.center.y))

# Test point interference
inside = Point(2, 2)
outside = Point(5, 5)
print("Point (2,2) inside rect4?", rect4.compute_interference_point(inside))
print("Point (5,5) inside rect4?", rect4.compute_interference_point(outside))


print("\nTest Square")

# Method 1: Bottom-left + side
sq1 = Square(1, Point(0, 0), 4)
print("Square Method 1 -> Area:", sq1.compute_area(), 
      "Perimeter:", sq1.compute_perimeter(), 
      "Center:", (sq1.center.x, sq1.center.y))

# Method 2: Center + side
sq2 = Square(2, Point(2, 2), 4)
print("Square Method 2 -> Area:", sq2.compute_area(), 
      "Perimeter:", sq2.compute_perimeter(), 
      "Center:", (sq2.center.x, sq2.center.y))

# Method 3: Two opposite points (will adjust to square)
sq3 = Square(3, Point(0, 0), Point(4, 2))
print("Square Method 3 -> Area:", sq3.compute_area(), 
      "Perimeter:", sq3.compute_perimeter(), 
      "Center:", (sq3.center.x, sq3.center.y))