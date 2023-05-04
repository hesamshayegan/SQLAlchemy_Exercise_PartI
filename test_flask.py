from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="TestFirstName",
                    last_name="TestLastName",
                    image_url="https://icons.iconarchive.com/icons/aha-soft/free-3d-glossy-interface/64/accept-icon.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            # make a fake request
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')

            res = client.get(res.location)
            html = res.get_data(as_text=True)
            self.assertIn('TestFirstName', html)
    

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first-name": "TestBugs", "last-name": "TestBunnyY",
                 "image-url": "https://icons.iconarchive.com/icons/sykonist/looney-tunes/256/Bugs-Bunny-Carrot-icon.png"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestBugs", html)


    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2> TestFirstName TestLastName </h2>', html)


    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first-name": "TestWileE", "last-name": "Coyote",
                 "image-url": "https://icons.iconarchive.com/icons/sykonist/looney-tunes/256/Wile-E-Coyote-icon.png"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestWileE", html)        
