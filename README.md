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
~ ogr2ogr -f "PostgreSQL" PG:"dbname=[db_name] user=[username] password=[password]" countries.geojson -nln polygon
```

#### ALIAS
- image_name = spatial-data
- tag_name = unique name given to 
- username = PostgreSQL account username
- password = PostgreSQL account password


### Notes

- When and where to use `def` and `async`.
