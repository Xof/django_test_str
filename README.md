# Test case for a bug in Django (#36832 in Trac)

Back to at least Django 4.0, there is a bug in the database interface under
specific conditions:

1. PostgreSQL.
2. The cursor is created from the `django.connection` object.
3. The data type being returned is JSON.
4. The top-level structure in the JSON blog is a list, rather than an object.

In that situation, `cursor.execute` returns a `str` rather than a Python `list`

This test case should be self-contained, although you do need a local PostgreSQL
database. The only dependency besides Django is `psycopg2`.

To run the test, use:

```bash
./manage.py test --keepdb
```
