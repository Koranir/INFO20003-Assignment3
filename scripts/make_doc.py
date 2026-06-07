import dominate
import dominate.tags as d
from paths import page_path, set_page_depth


def make_doc(title, depth=0):
    set_page_depth(depth)

    doc = dominate.document(title=f"Black Pepper Publishing - {title}")
    with doc.head:
        d.meta(charset="UTF-8")
        d.meta(name="viewport", content="width=device-width, initial-scale=1.0")
        d.link(rel="stylesheet", href=page_path("style/index.css"))

        # <link rel="preconnect" href="https://fonts.googleapis.com">
        # <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        # <link href="https://fonts.googleapis.com/css2?family=Crimson+Text&display=swap" rel="stylesheet">

        d.link(rel="preconnect", href="https://fonts.googleapis.com")
        d.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True)
        d.link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,300..700;1,300..700&family=Crimson+Text:ital,wght@0,400;0,600;1,600&family=Roboto:wght@100..900&display=swap",
        )
        d.script(src=page_path("js/index.js"))
    with doc.body:
        dominate.util.raw(
            """
<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
<defs>
<filter id="embolden" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
<feOffset dx="-0.5" dy="-0.5"/>
<feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1"/>
<feColorMatrix type="matrix" values="0 0 0 0 0.0862745 0 0 0 0 0.0862745 0 0 0 0 0.0862745 0 0 0 1 0"/>
<feBlend mode="normal" in2="shape" result="effect1_innerShadow_12_6869"/>
<feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
<feOffset dx="0.75" dy="0.75"/>
<feComposite in2="hardAlpha" operator="arithmetic" k2="-1" k3="1"/>
<feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 0.909804 0 0 0 0 0.811765 0 0 0 1 0"/>
<feBlend mode="normal" in2="effect1_innerShadow_12_6869" result="effect2_innerShadow_12_6869"/>
</filter>
</defs>
</svg>
            """
        )
    return doc
