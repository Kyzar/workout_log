import os
import app
import unittest
import tempfile

class AppTestCase(unittest.TestCase):

  # called before every test
  def setUp(self):
    self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    app.app.config['USERNAME'] = 'admin'
    app.app.config['PASSWORD'] = 'default'
    self.app = app.app.test_client()
    app.init_db()

  # called after every test
  def tearDown(self):
    os.close(self.db_fd)
    os.unlink(app.app.config['DATABASE'])

  def login(self, username, password):
    return self.app.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

  def logout(self):
    return self.app.get('/logout', follow_redirects=True)


  #-------------- BEGIN TESTS --------------#

  def test_empty_db(self):
    rv = self.app.get('/')
    assert 'No entries here so far' in rv.data

  # tc 1: logging in and out with correct credentials
  # tc 2: logging in with invalid username and password
  def test_login_logout(self):
    rv = self.login('admin', 'default')
    print rv.data
    assert 'You were logged in' in rv.data
    rv = self.logout()
    assert 'You were logged out' in rv.data

    rv = self.login('adminx', 'default')
    assert 'Invalid username' in rv.data
    rv = self.login('admin', 'defaultx')
    assert 'Invalid password' in rv.data

if __name__ == '__main__':
    unittest.main()