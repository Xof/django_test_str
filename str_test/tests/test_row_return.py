from django.test import TestCase

from django.db import connection as django_connection
import psycopg2

class StrTestCase(TestCase):
    def setUp(self):
        self.psycopg2_connection = psycopg2.connect('dbname=str_test user=str_test')
        self.django_connection = django_connection
        
        with self.psycopg2_connection.cursor() as c:
            c.execute("""
                      drop table if exists test
                      """)
            c.execute("""
                      create table test(pk bigint primary key, blob jsonb)
                      """)
            c.execute("""
                      insert into test(pk, blob) values(1, '[1, 2, {"a": 3}]')
                      """)
            c.execute("""
                      insert into test(pk, blob) values(2, '{"a": 3}')
                      """)
        
        self.psycopg2_connection.commit()

    def test_django_list(self):
        with self.django_connection.cursor() as c:
            for pk, expected_type in ((1, list), (2, dict)):
                c.execute("""
                          select * from test where pk=%(pk)s
                          """, {'pk': pk})
                row = c.fetchone()
                self.assertEqual(type(row[1]), expected_type)
    
    def test_psycopg2_list(self):
        with self.psycopg2_connection.cursor() as c:
            for pk, expected_type in ((1, list), (2, dict)):
                c.execute("""
                          select * from test where pk=%(pk)s
                          """, {'pk': pk})
                row = c.fetchone()
                self.assertEqual(type(row[1]), expected_type)