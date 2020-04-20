# Manbase API Server

## Class Diagram

![Class Diagram](img/README.png)

## Server Connection Info

### SSH

- Server: manbase-api.williswcy.com
- Account: root
- Password: eqh49-v3bnb
- Location: ~/manbase-api
- Start the testing server by -

```
cd manbase-api
. venv/bin/activate
flask run --host 0.0.0.0
```

- Note that we will need to use a production WSGI server later.

### MySQL

- Server Host: manbase-api.williswcy.com
- Account: charlescly / lancetpk / williswcy
- Password: Same as the account name
- Note: Please update your password with the following SQL command -

```sql
UPDATE mysql.user SET Password = PASSWORD('{your_new_password}') WHERE user = '{your_account}';
```

- Start the MySQL prompt with `mysql`, or connect remotely.
- Note the `public` (currently) has `SELECT`, `UPDATE` and `INSERT` prviledges on all tables of `manbasdb`.
- The password of `public` is `b05qv-x4xca`.
