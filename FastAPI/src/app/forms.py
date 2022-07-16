from typing import List
from fastapi import Request
from django.contrib.gis.geos import MultiPolygon, Polygon


class CountryCreateForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: List = []
