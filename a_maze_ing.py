from src import parser, RED, NC
import sys


def main() -> None:
    try:
        config = parser(sys.argv)
        print(config)
    except Exception as err:
        print(RED, err, NC)


if __name__ == "__main__":
    main()
