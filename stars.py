import math
import geometry
import parse
from geometry import Point, NORTH

rad_per_sec = 0.06562904269775921 / 20


class Star:

    def __init__(self, p, color, m, constellation, letter):
        self.p = p
        self.constellation = constellation
        self.color = color
        self.m = m
        self.letter = letter
        self.r = 2

    def __lt__(self, other):
        return self.m < other.m

    @property
    def x(self):
        return self.p.x

    @property
    def y(self):
        return self.p.y

    def rotate(self, angle):
        return self.with_coord(geometry.rotate_about_north(self.p, angle))

    def with_coord(self, p):
        return Star(p, self.color, self.m, self.constellation, self.letter)

    def get_new_coord(self, v, r, u):
        if not self.p.in_sphere_strictly(v, r):
            return None
        return self.with_coord(geometry.get_new_coord(self.p, v, r, u))


class StarrySky:

    def __init__(self, direction, top, stars, width=500, height=500):
        self._direction = direction
        self._top = top
        self.stars = stars
        self.size = Point(width, height)
        self.cacheanswer = None
        self.angle = 0
        self.zoom(0)

    direction = property()
    top = property()

    @direction.getter
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value.with_len(1)
        self.top = self.top

    @top.getter
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        w = value * self.direction
        value = self.direction * w
        self._top = value.with_len(1)

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.x

    def get_stars(self):
        if self.cache:
            return self.cache
        self.cache = []
        for star in self.stars:
            s = star.rotate(self.angle)
            s = s.get_new_coord(self.direction, self.r, self.top)
            if s and self.is_bright(star):
                self.cache.append(self.scale(s))
        self.modify_brightness()
        return self.cache

    def is_bright(self, star):
        return star.m + 5 * self.r < 7

    def modify_brightness(self):
        self.cache.sort()
        cnt = len(self.cache) // 3
        for star, i in zip(self.cache, range(cnt)):
            star.r += 1

    def scale(self, star):
        center = self.center()
        star.p *= min(center.x, center.y)
        star.p += center
        return star

    def get_nearest_star(self, p):
        s = None
        for star in self.get_stars():
            if not s or star.p.dist2(p) < s.p.dist2(p):
                s = star
        return s

    def in_pole(self):
        return geometry.equal(abs(self.direction.z), 1)

    def get_north(self):
        return geometry.get_new_coord(
            NORTH, self.direction, self.r, self.top).with_len(
                geometry.signum(NORTH % self.direction))

    def get_labels(self):
        labels = [self.get_north()]
        for i in range(3):
            labels.append(labels[i].rotate90(NORTH))
        center = self.center()
        return [v * (min(center.x, center.y) - 10) + center for v in labels]

    def inc_angle(self):
        self.angle += rad_per_sec
        self.angle %= math.pi * 2
        self.cache = None

    def set_angle(self, time):
        time /= 1000
        self.angle = time * rad_per_sec * 20 / 15 / 60 % (math.pi * 2)
        self.cache = None

    def center(self):
        return self.size / 2

    def resize(self, size):
        self.size = size
        self.cache = None

    def rotate_screen(self, v, u):
        v -= self.center()
        u -= self.center()
        self.top = self.top.rotate(-v.get_angle_2d(u), self.direction)
        self.cache = None

    def zoom_function(self, x):
        return 1 / (1 + math.e ** -x) * math.sqrt(2)

    def zoom(self, value):
        value /= 7000
        self.r = self.zoom_function(value)
        self.cache = None

    def rotate_camera(self, dx, dy):
        dx = 2 * self.r * -dx
        dy = 2 * self.r * -dy
        self._direction, self._top = geometry.rotate(
            self.direction, self.top, dx, dy)
        self.direction = self.direction
        self.cache = None
        return map(lambda x: (x * 180 / math.pi) % 360,
                   geometry.get_angles(self.direction))

    def change_direction(self, theta, phi):
        theta = parse.convert_str_to_angle(theta)
        phi = parse.convert_str_to_angle(phi)
        theta = 90 - theta
        p = geometry.spherical_to_decart(phi, theta)

        w = self.top * self.direction

        angle = self.top.in_basis(w, self.top).get_angle_2d(
            self.direction.ort().with_len(1).in_basis(w, self.top))

        self._direction, self._top = p.with_len(1), p.ort().with_len(1)

        self._top = self._top.rotate(angle, self._direction)

        self.direction = self.direction
        self.cache = None
