import re

from django_webtest import WebTest

class TestConstituencyDetailView(WebTest):

    def test_constituencies_page(self):
        # Just a smoke test to check that the page loads:
        response = self.app.get('/constituencies')
        aberdeen_north = response.html.find(
            'a', text=re.compile(r'York Outer')
        )
        self.assertTrue(aberdeen_north)
