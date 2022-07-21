from django.contrib.gis.geos import MultiPolygon, Polygon

from spatial_data.countries.models import Country


def get_cleaned_data(data):
    cleaned_data = []
    for row in data:
        properties = row["properties"]
        geometry = row["geometry"]
        admin = properties.get("ADMIN")
        iso_a3 = properties.get("ISO_A3")
        if geometry.get("type") == "Polygon":
            points = [geometry.get("coordinates")]
        elif geometry.get("type") == "MultiPolygon":
            points = geometry.get("coordinates")
        else:
            print(f"Error: {admin} ")
        geom = MultiPolygon([Polygon(point[0]) for point in points])
        cleaned_data.append(Country(admin=admin, iso_a3=iso_a3, geom=geom))
    return cleaned_data
