from src.parser import parser, RED, NC
import sys


def main() -> None:
    try:
        config = parser(sys.argv)
        print(config)
    except Exception as err:
        print(RED, err, NC)
        sys.exit


if __name__ == "__main__":
    main()
