import os
import webcheck
import unittest
import tempfile
import json


class WebcheckTestCase(unittest.TestCase):
	
	TEST_URL = "http://google.com"

	def setUp(self):
		self.db_fd, webcheck.app.config['DATABASE'] = tempfile.mkstemp()
		webcheck.app.config['TESTING'] = True
		self.app = webcheck.app.test_client()
		webcheck.dbservice.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(webcheck.app.config['DATABASE'])
		
	def add_site(self, url_name):
		return self.app.post("/add", data = json.dumps({'url': url_name}), headers = {"content-type": "application/json"})

	def edit_site(self, site_id, url_name):
		return self.app.put("/edit/" + str(site_id), data = json.dumps({'url': url_name}), headers = {"content-type": "application/json"})	
		
	def delete_site(self, site_id):
		return self.app.delete("/delete/" + str(site_id))
		
	def test_empty_db(self):
		return_html = self.app.get('/')

		assert "No sites so far..." in return_html.data
		
	def test_add_site(self):
		return_json = json.loads(self.add_site(self.TEST_URL).data)	
		return_html = self.app.get('/')

		self.assertEqual(self.TEST_URL, return_json['url'])
		self.assertEqual("Unknown", return_json['status_code'])
		self.assertEqual("Not checked yet", return_json['last_check'])

		assert self.TEST_URL in return_html.data
		assert "Unknown" in return_html.data
		assert "Not checked yet" in return_html.data
		assert "Edit" in return_html.data
		assert "Delete" in return_html.data		

	def test_add_delete_site(self):
		return_json = json.loads(self.add_site(self.TEST_URL).data)	
		return_html = self.app.get('/')
		
		assert self.TEST_URL in return_html.data
	 
		return_json = json.loads(self.delete_site(return_json['id']).data)
		return_html = self.app.get('/')

		self.assertEqual(0, return_json["sites_number"])
	
		assert "No sites so far..." in return_html.data
		
	def test_add_edit_site(self):
		return_json = json.loads(self.add_site(self.TEST_URL).data)	
		return_html = self.app.get('/')

		assert self.TEST_URL in return_html.data

		new_url = "http://wikipedia.org"
		self.edit_site(return_json['id'], new_url)
		return_html = self.app.get('/')
		
		assert new_url in return_html.data
		
	def test_add_get_site(self):
		return_json = json.loads(self.add_site(self.TEST_URL).data)	
		return_html = self.app.get('/')

		assert self.TEST_URL in return_html.data
		
		return_html = self.app.get("/site/" + str(return_json['id']))
		
		assert self.TEST_URL in return_html.data
		assert "Unknown" in return_html.data
		assert "Not checked yet" in return_html.data
		assert "Edit" in return_html.data
		assert "Delete" in return_html.data	


if __name__ == '__main__':
	unittest.main()





