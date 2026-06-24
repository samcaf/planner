from datetime import datetime
import html

from lib.parser import parse_pln


def render(blocks, date_str):
    html_blocks = []

    extra_title = None

    for b in blocks:
        if b.kind == "title":
            extra_title = b.title
        if b.kind == "project":
            html_blocks.append(render_project(b))
        elif b.kind == "list":
            html_blocks.append(render_list(b))
        elif b.kind == "note":
            html_blocks.append(render_note(b))

    return f"""
<div class="header">
  <h1>{date_str}{": "+extra_title if extra_title else ""}</h1>
</div>

<div class="dashboard">
{''.join(html_blocks)}
</div>

"""


def render_project(b):
    cols = {"short": [], "med": [], "long": []}

    for t in b.items:
        if t.duration == "short":
            cols["short"].append(t)
        elif t.duration == "med":
            cols["med"].append(t)
        elif t.duration == "long":
            cols["long"].append(t)
        else:
            assert t.state in ["gap", "sep"], \
                    f"Task {t.raw_text} needs a duration"
            for k in cols:
                cols[k].append(t)

    return f"""
<div class="card {b.color}">
  <h2>{b.title}</h2>

  <div class="columns">
    <div>{render_col(cols["short"])}</div>
    <div>{render_col(cols["med"])}</div>
    <div>{render_col(cols["long"])}</div>
  </div>
</div>
"""


SYMBOLS = {
    "todo": "",
    "done": "✓",
    "moved": "M",
    "maybe": "?",
    "cancelled": "✕",
}

def format_item(item):
    symbol = SYMBOLS.get(item.state, None)

    if item.state == "gap":
        return f"""
    <div class="gap {item.size}">
    </div>
    """

    elif item.state == "sep":
        return f"""
    <div class="separator {item.size}"></div>
    """

    elif symbol is None:
       return f"""
    <div class="task">
        <span class="note">
            {html.escape(item.text)}
        </span>
    </div>
    """

    return f"""
    <div class="task {item.state}">
        <div class="box">
            {symbol}
        </div>

        <span class="task-text">
            {html.escape(item.text)}
        </span>
    </div>
    """


def render_col(items):
    return "\n".join(format_item(t) for t in items)


def render_list(b):
    return f"""
<div class="card">
<h2>{b.title}</h2>
{"".join(format_item(t) for t in b.items)}
</div>
"""


def render_note(b):
    return f"""
<div class="card note">
{" ".join(b.content)}
</div>
"""
