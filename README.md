# Spatial Data using FastAPI


## Setup

### Repository on local machine:

```shell
~ gh repo clone PriyanshBordia/Spatial-Data-using-FastAPI
~ cd Spatial-Data-using-FastAPI
```

### Env vars

```shell
~ export SECRET_KEY=""
~ export DEBUG=True
~ export DB_NAME=[DB_NAME]
~ export DB_USERNAME=[DB_USERNAME]
~ export DB_PASSWORD=[DB_PASSWORD]
~ export DB_PORT=5432
~ export DB_HOST=[DB_HOST]
```

### Creating Virtual Env

```shell
~ python3 -m venv venv
~ source venv/bin/activate
~ pip install -r requirements.txt
```

### Docker Steps

```shell
~ docker login # Add credentials to promp
~ cd FastAPI
~ docker-compose -p spatial_data up -d --build

```

### Push image to Hub

```shell
~ docker build -t [image_name] .
~ docker tag [image_name]:[tag_name] [docker_username]:[repo]
~ docker push [docker_username]/[repo]
```

### Populate data to db

```shell
~ ogr2ogr -f "PostgreSQL" PG:"dbname=[db_name] user=[username] password=[password]" countries.geojson -nln data/geo-countries/archive/spatial_data
```

#### Sample Input 

```json
{
  "admin": "Wakanda",
  "iso_a3": "WKA",
  "geom": "[[[[0.0, 0.0]]]]"
}
{
  "admin": "Atlantis",
  "iso_a3": "ATL",
  "geom": "[[[[0.0, 0.0]]]]"
}
```

### Test

```shell
~ cd FastAPI
~ pytest src/tests/tests.py
```

#### ALIAS

- image_name = spatial-data
- tag_name = unique name given to an build
- username = PostgreSQL account username
- password = PostgreSQL account password


#### References

- [FastAPI](https://www.fastapitutorial.com/)
- [PostGIS](http://postgis.net/)
- [Docker](https://testdriven.io/blog/fastapi-crud/)
- [GitHub](https://github.com/nofoobar/JobBoard-Fastapi/blob/main/backend/tests/conftest.py)

