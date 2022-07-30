# Spatial Data using FastAPI


## Setup

### Repository on local machine

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
~ docker login # Add credentials to prompt
~ cd FastAPI
~ docker-compose -p spatial_data up -d --build
```

### URL

```text
> http://localhost:8002/docs
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

### Sample Input

```json
{
  "admin": "Wakanda",
  "iso_a3": "WKA",
  "geom": {
        	"type": "Polygon", 
	        "coordinates": [ [ 
				[ -69.996937628999916, 12.577582098000036 ], 
				[ -69.936390753999945, 12.531724351000051 ], 
				[ -69.924672003999945, 12.519232489000046 ], 
				[ -69.915760870999918, 12.497015692000076 ], 
				[ -69.880197719999842, 12.453558661000045 ], 
				[ -69.876820441999939, 12.427394924000097 ], 
				[ -69.888091600999928, 12.417669989000046 ], 
				[ -69.908802863999938, 12.417792059000107 ], 
				[ -69.930531378999888, 12.425970770000035 ], 
				[ -69.945139126999919, 12.44037506700009 ], 
				[ -69.924672003999945, 12.44037506700009 ], 
				[ -69.924672003999945, 12.447211005000014 ], 
				[ -69.958566860999923, 12.463202216000099 ], 
				[ -70.027658657999922, 12.522935289000088 ], 
				[ -70.048085089999887, 12.531154690000079 ], 
				[ -70.058094855999883, 12.537176825000088 ], 
				[ -70.062408006999874, 12.546820380000057 ], 
				[ -70.060373501999948, 12.556952216000113 ], 
				[ -70.051096157999893, 12.574042059000064 ], 
				[ -70.048736131999931, 12.583726304000024 ], 
				[ -70.052642381999931, 12.600002346000053 ], 
				[ -70.059641079999921, 12.614243882000054 ], 
				[ -70.061105923999975, 12.625392971000068 ], 
				[ -70.048736131999931, 12.632147528000104 ], 
				[ -70.00715084499987, 12.5855166690001 ], 
				[ -69.996937628999916, 12.577582098000036 ] 
			] ]
		}
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

