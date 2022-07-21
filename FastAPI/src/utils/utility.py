import geojson


def format(country: tuple) -> dict:
    try:
        return {
            "id": country[0],
            "name": country[1],
            "code": country[2],
            "coordinates": geojson.loads(country[3]).get("coordinates"),
        }
    except Exception as e:
        raise e


def success_response(data: list, message="API is fast..") -> dict:
    try:
        response = {
            "message": "",
            "meta": {
                "size": 0
            },
            "result": [],
            "success": True
        }
        response["message"] = message
        response["meta"]["size"] = len(data)
        response["result"].extend(data)
        return response
    except Exception as e:
        raise e


def error_response(error: list) -> dict:
    try:
        response = {"error": {"code": []}, "success": False}
        response["error"]["code"].extend(error)
        return response
    except Exception as e:
        raise e
