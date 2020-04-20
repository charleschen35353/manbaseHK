# Manbase API Server

## Class Diagram

![Class Diagram](img/README.png)

## Server Connection Info

### SSH

- Server: manbase-api.williswcy.com
- Account: root
- Password: eqh49-v3bnb

### MySQL

- Server Host: manbase-api.williswcy.com
- Account: charlescly / lancetpk / williswcy
- Password: Same as the account name
- Note: Please update your password with the following SQL command -

```sql
UPDATE mysql.user SET Password = PASSWORD('{your_new_password}') WHERE user = '{your_account}';
```
