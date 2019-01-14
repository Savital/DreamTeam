# Настройка проекта

```bash
$ mysql -u root

mysql> CREATE USER 'dt_admin'@'localhost' IDENTIFIED BY 'dt2016';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE DATABASE dreamteam_db;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON dreamteam_db . * TO 'dt_admin'@'localhost';
Query OK, 0 rows affected (0.00 sec)

$ export FLASK_CONFIG=development
$ export FLASK_APP=run.py
$ flask run

$ flask db init
$ flask db migrate
$ flask db upgrade

$ mysql -u root

mysql> use dreamteam_db;

mysql> show tables;

$ flask shell
>>> from app.models import Employee
>>> from app import db
>>> admin = Employee(email="admin@admin.com",username="admin",password="admin2016",is_admin=True)
>>> db.session.add(admin)
>>> db.session.commit()

$ mysql -u root

mysql> CREATE DATABASE dreamteam_test;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON dreamteam_test . * TO 'dt_admin'@'localhost';
Query OK, 0 rows affected (0.00 sec)

$ python tests.py

nose2 --with-coverage

```