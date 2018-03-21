import math
import re
from math import cos, sin, atan2

eps = 1e-14  # precission
R = 1  # radius of sphere


def signum(x):
    return -1 if x < 0 else 1


def equal(a, b):
    return abs(a - b) < eps


def less(a, b):
    return a < b and not equal(a, b)


def less_or_equal(a, b):
    return a < b or equal(a, b)


def sqrt(x):
    if x <= 0:
        return 0
    return math.sqrt(x)


class Point:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.x, self.y, self.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other, self.z / other)

    def __mul__(self, other):
        if not isinstance(other, Point):
            return Point(self.x * other, self.y * other, self.z * other)
        return Point(self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def __mod__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    @staticmethod
    def create_from_QPoint(p):
        return Point(p.x(), p.y())

    def length2(self):
        return self % self

    def length(self):
        return sqrt(self.length2())

    def __len__(self):
        return self.length()

    def dist(self, other):
        return (self - other).length()

    def dist2(self, other):
        return (self - other).length2()

    def get_angle(self, other):
        return atan2((self * other).length(), self % other)

    def get_angle_2d(self, other):
        return atan2((self * other).z, self % other)

    def with_len(self, k=1):
        d = self.length()
        if equal(d, 0):
            if equal(k, 0):
                return self
            raise Exception('zero-size vector')
        return self * k / d

    def rotate90(self, norm):
        if not equal(norm.length(), 1) or not equal(norm % self, 0):
            print(equal(norm.length(), 1), equal(norm % self, 0))
            raise Exception('No axel. Can\'t rotate vector {0} arount \
             vector {1}'.format(
                str(self), str(norm)))
        return self * norm

    def rotate(self, angle, norm):
        return self.rotate_at(cos(angle), sin(angle), norm)

    def rotate_at(self, cosa, sina, norm):
        other = self.rotate90(norm)
        return self * cosa + other * sina

    def on_plane(self, a, b, c):
        return equal(0, (a - self) * (b - self) % (c - self))

    def in_sphere(self, o, r):
        return less_or_equal(self.dist2(o), r * r)

    def in_sphere_strictly(self, o, r):
        return less(self.dist2(o), r * r)

    def in_basis(self, u, v):
        return Point(self % u, self % v, 0)

    def ort(self):
        if not equal(self.x, 0):
            return Point(-self.y, self.x, 0)
        if not equal(self.y, 0):
            return Point(-self.y, self.x, 0)
        return Point(0, self.z, -self.y)

NORTH = Point(0, 0, 1)  # vector to the north


def get_h(r, d):
    cosa = (R * R + d * d - r * r) / (2 * R * d)
    return R * cosa


def get_radius(r):
    h = get_h(r, R)
    return sqrt(R * R - h * h)


def get_new_vector_len(p, q, h):
    angle = p.get_angle(q)
    return h / cos(angle)


def get_new_coord(p, v, r, u):
    h = get_h(r, R)
    w = p.with_len(get_new_vector_len(v, p, h)) - v.with_len(h)
    return w.in_basis(u * v, u) / get_radius(r)


def get_new_coord_fixed(p, v, r, u):
    h = get_h(r, R)
    w = p.with_len(get_new_vector_len(v, p, h)) - v.with_len(h)
    return w.in_basis(u * v, u).with_len(r) / get_radius(r)


def spherical_to_decart(alpha, delta):
    alpha = math.radians(alpha)
    delta = math.radians(delta)
    return Point(R * sin(delta) * cos(alpha),
                 R * sin(delta) * sin(alpha),
                 R * cos(delta))


def rotate_around(v, u, xangle, yangle):
    v = v.rotate(xangle, u)
    w = v * u
    return v.rotate(yangle, w), u.rotate(yangle, w)


def rotate(v, u, dx, dy):
    xangle = 2 * math.asin(dx / (2 * R))
    yangle = 2 * math.asin(dy / (2 * R))
    return rotate_around(v, u, xangle, yangle)


def rotate_about_north(p, angle):
    h = get_h(p.dist(NORTH), p.length()) / R * p.length()
    s = NORTH.with_len(h)
    v = p - s
    return s + v.rotate(angle, NORTH)


def get_angles(v):
    return math.acos(v.z / v.length()), math.atan2(v.y, v.x)
