from django.test import Client, TestCase


class AnalyzerApiTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health(self):
        r = self.client.get("/api/health/")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("status", data)

    def test_coverage(self):
        r = self.client.get("/api/suggest/coverage/?count=5")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("suggestions", data)
