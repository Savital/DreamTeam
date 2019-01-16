import os
import unittest
import time
import urllib2

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask import abort, url_for
from flask_testing import TestCase, LiveServerTestCase
from selenium import webdriver
from mock import patch, Mock, MagicMock

from config import app_config
from app import create_app, db, login_manager
from app.models import Department, Employee, Role
from app.auth.forms import LoginForm, RegistrationForm

# Set test variables for test admin user
test_admin_username = "admin"
test_admin_email = "admin@email.com"
test_admin_password = "admin2016"

# Set test variables for test employee 1
test_employee1_first_name = "Test"
test_employee1_last_name = "Employee"
test_employee1_username = "employee1"
test_employee1_email = "employee1@email.com"
test_employee1_password = "1test2016"

# Set test variables for test employee 2
test_employee2_first_name = "Test"
test_employee2_last_name = "Employee"
test_employee2_username = "employee2"
test_employee2_email = "employee2@email.com"
test_employee2_password = "2test2016"

# Set variables for test department 1
test_department1_name = "Human Resources"
test_department1_description = "Find and keep the best talent"

# Set variables for test department 2
test_department2_name = "Information Technology"
test_department2_description = "Manage all tech systems and processes"

# Set variables for test role 1
test_role1_name = "Head of Department"
test_role1_description = "Lead the entire department"

# Set variables for test role 2
test_role2_name = "Intern"
test_role2_description = "3-month learning position"

class TestBase(LiveServerTestCase):
    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        if os.getenv('CIRCLECI'):
            database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
        else:
            database_uri = 'mysql://dt_admin:12345678@localhost/dreamteam_test'
        app.config.update(
            # Specify the test database
            SQLALCHEMY_DATABASE_URI=database_uri,
            # Change the port that the liveserver listens on
            LIVESERVER_PORT=8943
        )
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        self.admin = Employee(username=test_admin_username,
                              email=test_admin_email,
                              password=test_admin_password,
                              is_admin=True)

        # create test employee user
        self.employee = Employee(username=test_employee1_username,
                                 first_name=test_employee1_first_name,
                                 last_name=test_employee1_last_name,
                                 email=test_employee1_email,
                                 password=test_employee1_password)

        # create test department
        self.department = Department(name=test_department1_name,
                                     description=test_department1_description)

        # create test role
        self.role = Role(name=test_role1_name,
                         description=test_role1_description)

        # save users to database
        db.session.add(self.admin)
        db.session.add(self.employee)
        db.session.add(self.department)
        db.session.add(self.role)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()


class TestIntegration(TestBase):
    def test_registration(self):
        self.driver.get("http://127.0.0.1:8943/register")
        self.driver.find_element_by_id("email").send_keys(test_employee2_email)
        self.driver.find_element_by_id("username").send_keys(
            test_employee2_username)
        self.driver.find_element_by_id("first_name").send_keys(
            test_employee2_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
            test_employee2_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("submit").click()

        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully registered" in success_message

        # Assert that there are now 3 employees in the database
        self.assertEqual(Employee.query.count(), 3)


    def test_registrationInvalidEmail(self):
        self.driver.get("http://127.0.0.1:8943/register")

        self.driver.find_element_by_id("email").send_keys("invalid_email")
        self.driver.find_element_by_id("username").send_keys(
            test_employee2_username)
        self.driver.find_element_by_id("first_name").send_keys(
            test_employee2_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
            test_employee2_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("submit").click()


        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Invalid email address" in error_message

    def test_registrationConfirmPassword(self):
        self.driver.get("http://127.0.0.1:8943/register")

        self.driver.find_element_by_id("email").send_keys(test_employee2_email)
        self.driver.find_element_by_id("username").send_keys(
            test_employee2_username)
        self.driver.find_element_by_id("first_name").send_keys(
            test_employee2_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
            test_employee2_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_employee2_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
            "password-won't-match")
        self.driver.find_element_by_id("submit").click()

        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Field must be equal to confirm_password" in error_message

    def test_loginEmployee(self):
        self.driver.get("http://127.0.0.1:8943/login")

        self.driver.find_element_by_id("login_link").click()

        self.driver.find_element_by_id("email").send_keys(test_employee1_email)
        self.driver.find_element_by_id("password").send_keys(
            test_employee1_password)
        self.driver.find_element_by_id("submit").click()

        assert url_for('home.dashboard') in self.driver.current_url
        username_greeting = self.driver.find_element_by_id(
            "username_greeting").text
        assert "Hi, employee1!" in username_greeting

    def test_loginAdmin(self):
        self.driver.get("http://127.0.0.1:8943/login")

        self.driver.find_element_by_id("email").send_keys(test_admin_email)
        self.driver.find_element_by_id("password").send_keys(
            test_admin_password)
        self.driver.find_element_by_id("submit").click()

        assert url_for('home.admin_dashboard') in self.driver.current_url
        username_greeting = self.driver.find_element_by_id(
            "username_greeting").text
        assert "Hi, admin!" in username_greeting

    def test_loginInvalidEmailFormat(self):
        self.driver.get("http://127.0.0.1:8943/login")

        self.driver.find_element_by_id("email").send_keys("invalid")
        self.driver.find_element_by_id("password").send_keys(
            test_employee1_password)
        self.driver.find_element_by_id("submit").click()

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Invalid email address" in error_message

    def test_loginWrongEmail(self):
        self.driver.get("http://127.0.0.1:8943/login")

        self.driver.find_element_by_id("email").send_keys(test_employee2_email)
        self.driver.find_element_by_id("password").send_keys(
            test_employee1_password)
        self.driver.find_element_by_id("submit").click()

        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Invalid email or password" in error_message

    def test_loginWrongPassword(self):
        self.driver.get("http://127.0.0.1:8943/login")

        self.driver.find_element_by_id("email").send_keys(test_employee1_email)
        self.driver.find_element_by_id("password").send_keys(
            "invalid")
        self.driver.find_element_by_id("submit").click()

        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Invalid email or password" in error_message

if __name__ == '__main__':
    unittest.main()
