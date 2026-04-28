import dominate.tags as d
import yaml
from paths import cover_path, portrait_path


@d.section
def make_featured(title, feature):
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


def make_all_featured():
    featured = yaml.full_load(open("sources/featured.yaml", "r"))

    [make_featured(title, feature) for title, feature in featured.items()]
