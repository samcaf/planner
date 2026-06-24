import re
from dataclasses import dataclass, field


@dataclass
class Title:
    text: str

@dataclass
class Task:
    text: str
    state: str = "todo"   # todo | done | moved | maybe | cancelled | empty
    duration: str | None = None
    raw_text: str = ""

@dataclass
class Gap:
    state: str
    size: str = "small"
    duration: str = None


@dataclass
class Block:
    kind: str  # project | list | note
    title: str = ""
    color: str = "gray"
    items: list[Task] = field(default_factory=list)
    content: list[str] = field(default_factory=list)


def parse_pln(text: str):
    blocks = []
    current = None

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("@title"):
            title = line.replace("@title", "").strip()
            current = Block(kind="title", title=title)
            blocks.append(current)

        elif line.startswith("@project"):
            title = ""
            color = "gray"

            m = re.match(r"@project\s+(.*?)(\s+color=(\w+))?$", line)
            if m is not None:
                title = m.group(1)
                color = m.group(3) or "gray"

            current = Block(kind="project", title=title, color=color)
            blocks.append(current)

        elif line.startswith("@list"):
            title = line.replace("@list", "").strip()
            current = Block(kind="list", title=title)
            blocks.append(current)

        elif line.startswith("@note"):
            current = Block(kind="note")
            blocks.append(current)

        elif line.startswith("@end"):
            current = None

        elif current:
            if current.kind in ("project", "list"):
                current.items.append(parse_item(line))

            elif current.kind == "note":
                current.content.append(line)

    return blocks


STATE_MAP = {
    "- [ ]": "todo",
    "- [x]": "done",
    "- [M]": "moved",
    "- [?]": "maybe",
    "- [~]": "cancelled",
    "@gap": "gap",
    "@sep": "sep",
}


def parse_item(line: str) -> Task:
    raw = line.strip()

    state = None
    text = line

    for symbol, mapped in STATE_MAP.items():
        if line.startswith(f"{symbol}"):
            state = mapped
            text = line.replace(f"{symbol}", "", 1).strip()
            break

    duration = None

    for tag in re.findall(r"@\w+", text):
        if tag in ["@short", "@med", "@long"]:
            duration = tag[1:]

    text = re.sub(r"@\w+", "", text).strip()

    if state in ['gap', 'sep']:
        return Gap(state=state, size='small', duration=duration)

    return Task(
        text=text,
        state=state,
        duration=duration,
        raw_text=raw
    )
