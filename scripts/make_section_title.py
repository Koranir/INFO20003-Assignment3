import dominate.tags as d
from paths import asset_path


def make_section_title(text, asset=None):
    attrs = {"cls": "section-title"}

    if asset:
        attrs["style"] = f"--styled-asset-path: url('../{asset_path(asset)}')"

    return d.h2(text, **attrs)
