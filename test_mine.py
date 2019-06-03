import unittest
import main

example = [{"name": "place", "postcode": "HP201DH"}]


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = main.app
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SERVER_NAME'] = 'localhost'
        self.client = self.app.test_client()

    def test_home_page_1(self):
        response = self.client.get('/')
        received = response.get_data(as_text=True)
        # print (received)
        self.assertTrue('name' in received)

    def test_home_page_2(self):
        response = self.client.get('/')
        received = response.get_data(as_text=True)
        self.assertFalse('name given' in received)

    def test_filled_page_1(self):
        response = self.client.post('/storeslist', data=example)
        received = response.get_data(as_text=False)
        self.assertTrue(5 == received)

    def test_filled_page_2(self):
        response = self.client.get('/storeslist', data={'name': 'Bob'})
        received = response.get_data(as_text=True)
        self.assertFalse('entering' in received)

    def test_add_coordinates(self):
        self.assertEqual(len(example), len(main.add_coordinated_beta(example)))

    def test_number_of_nearest_towns(self):
        self.a = main.make_nearest_towns_list("E58RA", 5)
        sorted_by_lat_nearest_towns = sorted(self.a, key=lambda i: i['latitude'], reverse=True)
        self.assertEqual(len(sorted_by_lat_nearest_towns), 3)

    def test_home_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_stores_list_status(self):
        response = self.client.post('/storeslist')
        self.assertEqual(response.status_code, 200)


suite = unittest.TestLoader().loadTestsFromTestCase(FlaskClientTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
