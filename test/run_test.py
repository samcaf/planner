from lib.parser import parse_pln
from lib.render import render


def main():
    with open("test/test.pln", "r") as f:
        text = f.read()

    blocks = parse_pln(text)

    html = render(blocks, "Test Day")

    with open("test/dashboard.html", "w") as f:
        f.write(html)

    print("Generated test/dashboard.html")


if __name__ == "__main__":
    main()
