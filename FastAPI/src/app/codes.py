from enum import Enum
from http.client import FORBIDDEN


class ErrorCode(Enum):
	BAD_REQUEST = 400
	UNAUTHORIZED = 401
	FORBIDDEN = 403