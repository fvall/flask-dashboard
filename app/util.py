import re
import os
from itertools import chain

loc = os.path.dirname(os.path.abspath(__file__))


def css_variables():

    with open(os.path.join(loc, 'static', 'styles.css'), "r") as f:
        css = f.read()

    var = re.search(r':root\s?\n?{[\w\s\n)(:#;-]*}', css)
    if var is None:
        raise ValueError("Cannot extract css variables")

    var = var.group()
    var = [v.strip() for v in var.split("\n") if v.strip().startswith("--")]
    var = [v.split(";") for v in var]
    var = [v.strip() for v in chain.from_iterable(var) if v.strip().startswith("--")]

    output = dict()
    for v in var:
        key, val = v.split(":")
        key = key[2:].replace("-", "_").strip()
        val = val.strip()
        output[key] = val

    return output
