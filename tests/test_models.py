import os
import unittest
from mock import patch, Mock, MagicMock

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

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    def test_employee_model_verifyPasswordIfFalse(self):
        # create test non-admin user
        employee = Employee(username="test_user", email="test@mail.ru", first_name="firstname", last_name="lastname",
                            password="test2016")

        self.assertFalse(employee.verify_password("test2017"))

    def test_employee_model_verifyPasswordIfTrue(self):
        # create test non-admin user
        employee = Employee(username="test_user", email="test@mail.ru", first_name="firstname", last_name="lastname",
                            password="test2016")

        self.assertTrue(employee.verify_password("test2016"))

    def test_employee_model_ifEmpty(self):
        self.assertEqual(Employee.query.count(), 0)

    def test_employee_model_ifAdd(self):
        # create test non-admin user
        employee = Employee(username="test_user", email="test@mail.ru", first_name="firstname", last_name="lastname",  password="test2016")

        # save users to database
        db.session.add(employee)
        db.session.commit()
        chEmployee = Employee.query.filter_by(username='test_user').first()

        self.assertEqual(Employee.query.count(), 1)
        self.assertEqual(employee, chEmployee)

    def test_employee_model_ifAddAdmin(self):
        # create test admin user
        admin = Employee(username="admin", password="admin2016", is_admin=True)

        # save users to database
        db.session.add(admin)
        db.session.commit()

        chAdmin = Employee.query.filter_by(username='admin').first()
        self.assertEqual(Employee.query.count(), 1)
        self.assertEqual(admin, chAdmin)

    def test_employee_model_ifAddMany(self):
        # create test admin user
        admin = Employee(username="admin", password="admin2016", is_admin=True)
        # create test non-admin user
        employee1 = Employee(username="test_user_1", password="test2016")
        # create test non-admin user
        employee2 = Employee(username="test_user_2", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.commit()

        chAdmin = Employee.query.filter_by(username='admin').first()
        chEmployee1 = Employee.query.filter_by(username='test_user_1').first()
        chEmployee2 = Employee.query.filter_by(username='test_user_2').first()

        self.assertEqual(Employee.query.count(), 3)
        self.assertEqual(admin, chAdmin)
        self.assertEqual(employee1, chEmployee1)
        self.assertEqual(employee2, chEmployee2)

    def test_employee_model_ifDelete(self):
        # create test non-admin user
        employee = Employee(username="test_user", password="test2016")

        # save users to database
        db.session.add(employee)
        db.session.commit()
        db.session.delete(employee)
        db.session.commit()

        self.assertEqual(Employee.query.count(), 0)

    def test_employee_model_ifDeleteAdmin(self):
        # create test admin user
        admin = Employee(username="admin", password="admin2016", is_admin=True)
        # create test non-admin user
        employee1 = Employee(username="test_user_1", password="test2016")
        # create test non-admin user
        employee2 = Employee(username="test_user_2", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.commit()

        db.session.delete(admin)

        chEmployee1 = Employee.query.filter_by(username='test_user_1').first()
        chEmployee2 = Employee.query.filter_by(username='test_user_2').first()

        self.assertEqual(Employee.query.count(), 2)
        self.assertEqual(employee1, chEmployee1)
        self.assertEqual(employee2, chEmployee2)

    def test_employee_model_ifDeleteMany(self):
        # create test admin user
        admin = Employee(username="admin", password="admin2016", is_admin=True)
        # create test non-admin user
        employee1 = Employee(username="test_user_1", password="test2016")
        # create test non-admin user
        employee2 = Employee(username="test_user_2", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.commit()

        db.session.delete(admin)
        db.session.delete(employee2)
        db.session.commit()

        chEmployee1 = Employee.query.filter_by(username='test_user_1').first()

        self.assertEqual(Employee.query.count(), 1)
        self.assertEqual(employee1, chEmployee1)

    def test_employee_model_ifDeleteAll(self):
        # create test admin user
        admin = Employee(username="admin", password="admin2016", is_admin=True)
        # create test non-admin user
        employee1 = Employee(username="test_user_1", password="test2016")
        # create test non-admin user
        employee2 = Employee(username="test_user_2", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.commit()

        db.session.delete(admin)
        db.session.delete(employee1)
        db.session.delete(employee2)

        self.assertEqual(Employee.query.count(), 0)

    def test_department_model_ifEmpty(self):
        self.assertEqual(Department.query.count(), 0)

    def test_department_model_ifAdd(self):
        # create test department
        department = Department(name="IT", description="The IT Department")

        # save department to database
        db.session.add(department)
        db.session.commit()

        chDepartment = Department.query.filter_by(name='IT').first()

        self.assertEqual(Department.query.count(), 1)
        self.assertEqual(department, chDepartment)

    def test_department_model_ifAddMany(self):
        # create test department
        department1 = Department(name="IT1", description="The IT1 Department")
        department2 = Department(name="IT2", description="The IT2 Department")

        # save department to database
        db.session.add(department1)
        db.session.add(department2)
        db.session.commit()

        chDepartment1 = Department.query.filter_by(name='IT1').first()
        chDepartment2 = Department.query.filter_by(name='IT2').first()

        self.assertEqual(Department.query.count(), 2)
        self.assertEqual(department1, chDepartment1)
        self.assertEqual(department2, chDepartment2)

    def test_department_model_ifDelete(self):
        # create test department
        department1 = Department(name="IT1", description="The IT1 Department")
        department2 = Department(name="IT2", description="The IT2 Department")

        # save department to database
        db.session.add(department1)
        db.session.add(department2)
        db.session.commit()

        db.session.delete(department2)

        chDepartment1 = Department.query.filter_by(name='IT1').first()

        self.assertEqual(Department.query.count(), 1)
        self.assertEqual(department1, chDepartment1)

    def test_role_model_ifEmpty(self):
        self.assertEqual(Role.query.count(), 0)

    def test_role_model_ifAdd(self):
        # create test role
        role = Role(name="CEO", description="Run the whole company")

        # save role to database
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)

    def test_role_model_ifAddMany(self):
        role1 = Role(name="CEO1", description="Run the whole company")
        role2 = Role(name="CEO2", description="Run the whole company")
        role3 = Role(name="CEO3", description="Run the whole company")

        # save role to database
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.commit()

        chRole1 = Role.query.filter_by(name='CEO1').first()
        chRole2 = Role.query.filter_by(name='CEO2').first()
        chRole3 = Role.query.filter_by(name='CEO3').first()

        self.assertEqual(Role.query.count(), 3)
        self.assertEqual(role1, chRole1)
        self.assertEqual(role2, chRole2)
        self.assertEqual(role3, chRole3)

    def test_role_model_ifDelete(self):
        role1 = Role(name="CEO1", description="Run the whole company")
        role2 = Role(name="CEO2", description="Run the whole company")
        role3 = Role(name="CEO3", description="Run the whole company")

        # save role to database
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.commit()

        db.session.delete(role2)
        db.session.commit()

        chRole1 = Role.query.filter_by(name='CEO1').first()
        chRole3 = Role.query.filter_by(name='CEO3').first()

        self.assertEqual(Role.query.count(), 2)
        self.assertEqual(role1, chRole1)
        self.assertEqual(role3, chRole3)


if __name__ == '__main__':
    unittest.main()
