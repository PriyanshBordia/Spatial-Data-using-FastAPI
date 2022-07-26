import base64
import sys


def main() -> str:

    if len(sys.argv) != 3:
        return "~ python encode.py [username] [password]"

    base = str(sys.argv[1]) + ":" + str(sys.argv[2])
    return base64.b64encode(base.encode("utf-8")).decode("utf-8")


if __name__ == "__main__":
    print(main())
