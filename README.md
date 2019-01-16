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

Результаты оценки покрытия

```bash
app/__init__.py                                                                            39      4    90%
app/admin/__init__.py                                                                       3      0   100%
app/admin/forms.py                                                                         17      0   100%
app/admin/views.py                                                                        120     93    23%
app/auth/__init__.py                                                                        3      0   100%
app/auth/forms.py                                                                          22      4    82%
app/auth/views.py                                                                          31     18    42%
app/home/__init__.py                                                                        3      0   100%
app/home/views.py                                                                          13      4    69%
app/models.py                                                                              70      8    89%
config.py                                                                                   9      0   100%
example.py                                                                                 12     12     0%
instance/config.py                                                                          2      0   100%
run.py                                                                                      6      6     0%
test_errors.py                                                                             41      2    95%
test_func.py                                                                              327      2    99%
test_integration.py                                                                       139      2    99%
test_models.py                                                                            224      2    99%
test_views.py                                                                              67      2    97%

```