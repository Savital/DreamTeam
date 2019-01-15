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


class TestIntegration(TestBase):

    def test_employee_model_assignDepartment(self):
        pass

    def test_employee_model_assignRole(self):
        pass

if __name__ == '__main__':
    unittest.main()
