import dominate.tags as d
import yaml
from paths import cover_path, portrait_path

featured = yaml.full_load(open("sources/featured.yaml", "r"))

for title, feature in featured.items():
    article = d.article()
    with article:
        with d.div(cls="images"):
            with d.img(cls="author-portrait"):
                d.attr(
                    src=portrait_path(feature["author"]),
                    alt=f"Portrait of {feature['author']}",
                )
            with d.img(cls="cover"):
                d.attr(
                    src=cover_path(title),
                    alt=f"Cover of {title}",
                )
        with d.div(cls="details"):
            d.h3(title)
            d.address(feature["author"])

            d.p(feature["description"])

    print(article)
