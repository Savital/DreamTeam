import os
import unittest

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Department, Employee, Role


class TestBase(TestCase):

    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        if os.getenv('CIRCLECI'):
            database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
        else:
            database_uri = 'mysql://dt_admin:12345678@localhost/dreamteam_test'
        app.config.update(
            # Specify the test database
            SQLALCHEMY_DATABASE_URI=database_uri
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = Employee(username="admin", password="admin2016", is_admin=True)

        # create test non-admin user
        employee = Employee(username="test_user", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        """
        Test 403 error page
        """
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        """
        Test 404 error page
        """
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        """
        Test 500 error page
        """
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)


if __name__ == '__main__':
    unittest.main()
