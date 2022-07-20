# Spatial Data using FastAPI

```
~ python encode.py [docker_username] [docker_password]
```

### Steps

```
~ docker login # Add credentials to prompt
~ docker pull python
~ docker pull postgis/postgis
~ docker build -t [image_name] .
~ docker tag [image_name]:[tag_name] [docker_username]:[repo]
~ docker push [docker_username]/[repo]
```

### Populate data to local db

```
~ ogr2ogr -f "PostgreSQL" PG:"dbname=[db_name] user=[username] password=[password]" countries.geojson -nln spatial_data
```

#### Sample Input

{
"admin": "Wakanda",
"iso_a3": "WKA",
}
{
"admin": "Atlantis",
"iso_a3": "ATL",
"geom": "[[[[0.0, 0.0]]]]"
}

### Test

```
~ pytest src/tests/tests.py
```

#### ALIAS

- image_name = spatial-data
- tag_name = unique name given to
- username = PostgreSQL account username
- password = PostgreSQL account password

##### Notes

- When and where to use `def` and `async`.

##### References

- [FastAPI](https://www.fastapitutorial.com/)
- [PostGIS](http://postgis.net/)
- [Docker](https://testdriven.io/blog/fastapi-crud/)
- [GitHub](https://github.com/nofoobar/JobBoard-Fastapi/blob/main/backend/tests/conftest.py)
- [2](https://github.com/jordaneremieff/django-fastapi-example/blob/main/django_fastapi/project/settings.py)

##### Todo

- [x] Adding Tests
- [x] Oauth2 using JWT
- [x] Adding Checks
