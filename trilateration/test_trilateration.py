import unittest

from trilateration import trilateration, circle, point
# do not forget to use nose2 at root to run test

 
class Test_trilateration(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_circle_creation(self):
        assert False, "write test please"

    def test_point_creation(self):
        assert False, "write test please"

    def test_projection_creation(self):
        assert False, "write test please"

    def test_trilateration_creation(self):
        assert False, "write test please"


    # =============================================== FUNCTIONNAL TEST
    def test_complete_approximation(self):
        c1 = circle(point(48.84, 2.26), 300)
        c2 = circle(point(48.84, 2.30), 5)
        c3 = circle(point(48.80, 2.30), 350)

        trilat = trilateration([c1, c2, c3])
        self.assertTrue(trilat.is_approximation)
        self.assertEqual(trilat.geolocalized_device.lat, 48.826717)
        self.assertEqual(trilat.geolocalized_device.lon, 2.286731)

    def test_exact_intersection(self):
        assert False, "write test please"

    def test_area_intersection(self):
        assert False, "write test please"

    def test_two_circles_intersection(self):
        assert False, "write test please"

    
    # =============================================== ERROR CHECKING
    def test_negative_radius(self):
        assert False, "write test please"

    def test_only_one_circle(self):
        assert False, "write test please"

    def test_only_two_circles(self):
        assert False, "write test please"

    def test_four_circles(self):
        assert False, "write test please"

    def test_incorrect_latitude(self):
        assert False, "write test please"

    def test_incorrect_longitude(self):
        assert False, "write test please"

    def test_incorrect_param_type(self):
        assert False, "write test please"

if __name__ == '__main__':
    unittest.main()