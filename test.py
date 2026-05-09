WHITE = "\033[47;30m"
NC = "\033[0m"


def flags(walls: int) -> dict[str, bool]:
    flag0 = bool(walls & 0b0001)
    flag1 = bool(walls & 0b0010)
    flag2 = bool(walls & 0b0100)
    flag3 = bool(walls & 0b1000)

    return {
        "flag0": flag0,
        "flag1": flag1,
        "flag2": flag2,
        "flag3": flag3
    }


def draw_cell(flags: dict[str, bool]) -> None:
    if flags["flag0"]:
        print(f"{WHITE}     {NC}")
    else:
        print(f"{WHITE} {NC}   {WHITE} {NC}")

    if flags["flag1"] and flags["flag3"]:
        print(f"{WHITE} {NC}   {WHITE} {NC}")
        print(f"{WHITE} {NC}   {WHITE} {NC}")
    elif flags["flag1"] and not flags["flag3"]:
        print(f"    {WHITE} {NC}")
        print(f"    {WHITE} {NC}")
    elif not flags["flag1"] and flags["flag3"]:
        print(f"{WHITE} {NC}   ")
        print(f"{WHITE} {NC}   ")
    elif not flags["flag1"] and not flags["flag3"]:
        print("   ")
        print("   ")

    if flags["flag2"]:
        print(f"{WHITE}     {NC}")
    else:
        print(f"{WHITE} {NC}   {WHITE} {NC}")


# Tests:
    # 15 ok
    # 14 ok
    # 13 ok
    # 12 ok
    # 11 ok
    # 10 ok
    # 9  ok
    # 8  ok
    # 7  ok
    # 6  ok
    # 5  ok
    # 4  ok
    # 3  ok
    # 2  ok
    # 1  ok
def main() -> None:
    walls = 1
    bits = flags(walls)
    draw_cell(bits)


if __name__ == "__main__":
    main()
