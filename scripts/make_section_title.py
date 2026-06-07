import dominate.tags as d


def make_section_title(text, asset=None):
    attrs = {"cls": "section-title"}

    if asset:
        attrs["style"] = f"--styled-asset-path: url('../assets/{asset}')"

    return d.h2(text, **attrs)
