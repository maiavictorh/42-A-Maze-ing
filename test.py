from src.parser import parser
import sys


def main() -> None:
    try:
        config = parser(sys.argv)
        print(config)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
