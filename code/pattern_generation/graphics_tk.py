from tkinter import Canvas, Tk
from PIL import Image, ImageDraw


class EinsteinCanvas(Canvas):
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)
        self.scalar = 1

    def set_scalar(self, scalar):
        self.scalar = scalar

    def draw_polygon(self, vertices, fill="blue"):
        coordinates = []
        for vec in vertices:
            coordinates.append(vec.x*self.scalar + self.winfo_reqwidth()/2)
            coordinates.append(vec.y*self.scalar + self.winfo_reqheight()/2)

        self.create_polygon(coordinates, fill=fill, width=2, outline="black")


class EinsteinImage:
    """Pillow-backed drawing helper that mirrors the small Canvas API used
    by the project (set_scalar, draw_polygon).

    Usage:
        img = EinsteinImage(width, height, bg="white", scalar=20)
        img.draw_polygon(vertices, fill="red")
        img.save("out.png")
    """

    def __init__(self, width, height, bg=(255, 255, 255), scalar=1):
        self.width = width
        self.height = height
        self.scalar = scalar
        self.img = Image.new("RGB", (width, height), bg)
        self.draw = ImageDraw.Draw(self.img)

    def set_scalar(self, scalar):
        self.scalar = scalar

    def draw_polygon(self, vertices, fill="blue"):
        coords = []
        cx = self.width / 2
        cy = self.height / 2
        for vec in vertices:
            coords.append((vec.x * self.scalar + cx, vec.y * self.scalar + cy))

        # Accept several fill formats used in the project:
        #  - color name string, e.g. 'blue'
        #  - RGB tuple, e.g. (255,200,100)
        #  - list like [name, (r,g,b)]
        if isinstance(fill, (list, tuple)):
            if len(fill) == 0:
                fill_val = None
            elif isinstance(fill[0], str):
                # [name, (r,g,b)] or (name, ...)
                fill_val = fill[0]
            elif all(isinstance(c, int) for c in fill):
                # RGB tuple
                fill_val = tuple(fill)
            elif len(fill) > 1 and isinstance(fill[1], (list, tuple)) and all(isinstance(c, int) for c in fill[1]):
                fill_val = tuple(fill[1])
            else:
                fill_val = str(fill[0])
        else:
            fill_val = fill

        self.draw.polygon(coords, fill=fill_val, outline="black")

    def save(self, filename):
        try:
            self.img.save(filename)
            print("Saved successfully:", filename)
        except Exception as e:
            print("SAVE FAILED:", e)

    def get_image(self):
        return self.img


def draw_tiles(tiles, width=500, height=500, scalar=20, filename="./einstein_pattern.jpg", show_window=False):
    if filename:
        img = EinsteinImage(width, height, bg="white", scalar=scalar)
        for tile in tiles:
            img.draw_polygon(tile[0], fill=tile[1][1])

        img.save(filename)
    if show_window:
        root = Tk()
        canvas = EinsteinCanvas(root, width=width, height=height)
        canvas.set_scalar(scalar)

        for tile in tiles:
            canvas.draw_polygon(tile[0], fill=tile[1][0])

        canvas.pack()
        root.mainloop()
    return filename
