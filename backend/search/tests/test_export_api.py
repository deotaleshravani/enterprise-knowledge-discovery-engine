from django.test import SimpleTestCase
from django.urls import reverse


class ExportAPITests(SimpleTestCase):
    def test_csv_export_returns_200(self):
        response = self.client.get(reverse("export-data", kwargs={"file_format": "csv"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])

    def test_json_export_returns_200(self):
        response = self.client.get(reverse("export-data", kwargs={"file_format": "json"}))
        self.assertEqual(response.status_code, 200)
