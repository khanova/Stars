#!/usr/bin/env python3
import unittest
import sys
import os
import geometry
import parse
import stars
import global_vars
from geometry import Point


class Tests(unittest.TestCase):

    def test_get_h(self):
        x = geometry.get_h(1, 23)
        self.assertAlmostEqual(x, 11.5)

    def test_get_radius(self):
        r = geometry.get_radius(2 ** 0.5)
        self.assertAlmostEqual(r, 1)

    def test_get_new_vector_len(self):
        x = geometry.get_new_vector_len(Point(1, 0, 0), Point(1, 1, 0), 1)
        self.assertAlmostEqual(x, 2 ** 0.5)

    def test_get_new_vector_len_sqrt2(self):
        x = geometry.get_new_vector_len(
            Point(1, 0, 0), Point(1, 1, 0), 2 ** 0.5)
        self.assertAlmostEqual(x, 2)

    def test_get_new_coord(self):
        p = geometry.get_new_coord(
            Point(1, 1, 0), Point(1, 0, 0), 1, Point(0, 1, 0))
        self.assertAlmostEqual(p.x, 0)
        self.assertAlmostEqual(p.y, 0.57735026918)
        self.assertAlmostEqual(p.z, 0)

    def test_spherical_to_decart_north_poles(self):
        p = geometry.spherical_to_decart(0, 0)
        self.assertAlmostEqual(p.x, 0)
        self.assertAlmostEqual(p.y, 0)
        self.assertAlmostEqual(p.z, 1)

    def test_spherical_to_decart_south_poles(self):
        p = geometry.spherical_to_decart(0, 180)
        self.assertAlmostEqual(p.x, 0)
        self.assertAlmostEqual(p.y, 0)
        self.assertAlmostEqual(p.z, -1)

    def test_spherical_to_decart_equathor_east(self):
        p = geometry.spherical_to_decart(0, 90)
        self.assertAlmostEqual(p.x, 1)
        self.assertAlmostEqual(p.y, 0)
        self.assertAlmostEqual(p.z, 0)

    def test_spherical_to_decart_equathor_west(self):
        p = geometry.spherical_to_decart(180, 90)
        self.assertAlmostEqual(p.x, -1)
        self.assertAlmostEqual(p.y, 0)
        self.assertAlmostEqual(p.z, 0)

    def test_spherical_to_decart_equathor_other(self):
        p = geometry.spherical_to_decart(90, 90)
        self.assertAlmostEqual(p.x, 0)
        self.assertAlmostEqual(p.y, 1)
        self.assertAlmostEqual(p.z, 0)

    def test_spherical_to_decart_equathor_simple(self):
        p = geometry.spherical_to_decart(270, 90)
        self.assertAlmostEqual(p.x, 0)
        self.assertAlmostEqual(p.y, -1)
        self.assertAlmostEqual(p.z, 0)

    def test_rotation(self):
        p, q = geometry.rotate(Point(1, 0, 0), Point(0, 1, 0), 1, 1)
        self.assertAlmostEqual(p.x, 0.25)
        self.assertAlmostEqual(q.y, 0.5)
        self.assertAlmostEqual(q.z, 0.75)

    def test_in_sphere(self):
        p = Point(0, 0, 1)
        self.assertTrue(p.in_sphere(Point(0, 0, 0), 1))

    def test_not_in_sphere(self):
        p = Point(0, 0, 1)
        self.assertFalse(p.in_sphere(Point(0, 0, 0), 0.9))

    def test_dist(self):
        p = Point(0, 0, 0)
        l = p.dist(Point(0, 0, 10))
        self.assertAlmostEqual(l, 10)

    def test_dist2_2d(self):
        p = Point(0, 0, 0)
        l = p.dist2(Point(0, 10, 10))
        self.assertAlmostEqual(l, 200)

    def test_dist2_3d(self):
        p = Point(0, 0, 0)
        l = p.dist2(Point(1, 10, 10))
        self.assertAlmostEqual(l, 201)

    def test_parse_line_constellation(self):
        s = parse.parse_line(
            '161 19:22:50.9 +26:15:45  59.78   5.32  V 5.18   B6III\
              -0.001 -0.010       -012 182255   3    ', 'abc')
        self.assertEqual(s.constellation, 'abc')

    def test_parse_line_color(self):
        s = parse.parse_line(
            '161 19:22:50.9 +26:15:45  59.78   5.32  V 5.18   B6III\
              -0.001 -0.010       -012 182255   3    ', 'abc')
        self.assertEqual(s.color, 'B')

    def test_parse_line_letter(self):
        s = parse.parse_line(
            '161 19:22:50.9 +26:15:45  59.78   5.32  V 5.18   B6III\
              -0.001 -0.010       -012 182255   3Lam ', 'abc')
        self.assertEqual(s.letter, 'λ')

    def test_inint_sky(self):
        sky = stars.StarrySky(Point(1, 0, 0), Point(0, 1, 0), [])
        self.assertAlmostEqual(sky.top % sky.direction, 0)

    def test_is_bright(self):
        sky = stars.StarrySky(Point(1, 0, 0), Point(0, 1, 0), [])
        s = stars.Star(Point(0, 0), 'A', 1, 'and', None)
        self.assertTrue(sky.is_bright(s))

    def test_is_not_bright(self):
        sky = stars.StarrySky(Point(1, 0, 0), Point(0, 1, 0), [])
        s = stars.Star(Point(0, 0), 'A', 5, 'and', None)
        self.assertFalse(sky.is_bright(s))

    def test_brightness(self):
        s0 = stars.Star(Point(1, 0, 0), 'A', 1, 'and', None)
        s1 = stars.Star(Point(1, 0, 0), 'A', 3, 'and', None)
        s2 = stars.Star(Point(1, 0, 0), 'A', 3, 'and', None)
        sky = stars.StarrySky(Point(1, 0, 0), Point(0, 1, 0), [s0, s1, s2])
        st = sky.get_stars()
        self.assertTrue(st[0].m == 1)

    def test_brightness_radius(self):
        s0 = stars.Star(Point(1, 0, 0), 'A', 1, 'and', None)
        s1 = stars.Star(Point(1, 0, 0), 'A', 3, 'and', None)
        s2 = stars.Star(Point(1, 0, 0), 'A', 3, 'and', None)
        sky = stars.StarrySky(Point(1, 0, 0), Point(0, 1, 0), [s0, s1, s2])
        st = sky.get_stars()
        self.assertFalse(st[0].r == st[1].r)

    def test_zoom(self):
        sky = stars.StarrySky(Point(1, 0, 0), Point(0, 1, 0), [])
        sky.zoom(6000)
        self.assertAlmostEqual(sky.r, 0.992867539)

    def test_scale(self):
        sky = stars.StarrySky(Point(1, 0, 0), Point(0, 1, 0), [])
        sky.resize(Point(100, 100))
        s0 = stars.Star(Point(0, 0, 0), 'A', 1, 'and', None)
        sky.scale(s0)
        self.assertAlmostEqual(s0.x, 50)
        self.assertAlmostEqual(s0.y, 50)

    def test_rotate_camera(self):
        sky = stars.StarrySky(Point(1, 0, 0), Point(0, 1, 0), [])
        sky.rotate_camera(0.1, 0.1)
        self.assertAlmostEqual(sky.top % sky.direction, 0)
        self.assertAlmostEqual(sky.top.length(), 1)
        self.assertAlmostEqual(sky.direction.length(), 1)

    def test_parse_time(self):
        self.assertEqual(parse.parse_time('1.1.2001 12:30'), 31667400000)

    def test_check_angle(self):
        self.assertTrue(parse.check_angle((170, 50, 59), 180))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
