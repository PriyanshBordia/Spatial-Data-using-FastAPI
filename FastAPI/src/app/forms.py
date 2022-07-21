from typing import List

from django.contrib.gis.geos import MultiPolygon, Polygon

from fastapi import Request


class CountryCreateForm:
	def __init__(self, request: Request) -> None:
		self.request: Request = request
		self.errors: List = []