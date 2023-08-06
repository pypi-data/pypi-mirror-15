This package provides a simple context manager for Django applications
that will output the SQL queries caused by a block of code to standard
output.

(To pre-empt a common question: Django Debug Toolbar lets you see the
queries caused by HTTP requests to your application, but often I want
to track down the queries that are used in a management command or
some other context than making requests in your browser; the
`show_queries` context manager in this package helps in those other
situations.)

If you have sqlparse installed, then the SQL will be pretty-printed to
make them easier to read, so I'd recommend that you also do:

    pip install sqlparse

### Example

```
from django_debug_queries import show_queries

...

    with show_queries():
        people = list(Person.objects.filter(date_of_birth__gt="2000-01-01") \
            .values('id', 'legal_name'))
        sessions = list(ParliamentarySession.objects.all())
```

This might output the following to standard output:

```

--===--
Number of queries: 2
  Query 0 (taking 0.003): 
    SELECT "core_person"."id",
           "core_person"."legal_name"
    FROM "core_person"
    WHERE "core_person"."date_of_birth" > '2000-01-01'
    ORDER BY "core_person"."sort_name" ASC
  Query 1 (taking 0.005): 
    SELECT "core_parliamentarysession"."id",
           "core_parliamentarysession"."created",
           "core_parliamentarysession"."updated",
           "core_parliamentarysession"."start_date",
           "core_parliamentarysession"."end_date",
           "core_parliamentarysession"."house_id",
           "core_parliamentarysession"."position_title_id",
           "core_parliamentarysession"."mapit_generation",
           "core_parliamentarysession"."name",
           "core_parliamentarysession"."slug"
    FROM "core_parliamentarysession"
    ORDER BY "core_parliamentarysession"."start_date" ASC
End of query output.
```

### Other options

Long query strings can take a long time to pretty-print using
sqlparse, so by default SQL that is longer that 2048 characters is not
formatted; you can adjust that limit with the optional
`sqlparse_character_limit` parameter, e.g.:

```
    with show_queries(sqlparse_character_limit=8192):
        ...
```

If you are using multiple databases in your Django application, you
can tell this to use a particular database with the optional
`db_alias` parameter, e.g.

```
    with show_queries(db_alias='my_other_db'):
        ...
```
