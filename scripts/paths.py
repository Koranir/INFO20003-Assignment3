page_depth = 0


def set_page_depth(depth):
    global page_depth
    page_depth = depth


def page_path(path):
    if path.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return path

    return "../" * page_depth + path.lstrip("/")


def asset_path(path):
    return page_path(f"assets/{path.lstrip('/')}")


def slugify(name):
    return name.lower().replace(" ", "-")


def author_assets_path(name):
    return asset_path(f"authors/{slugify(name)}")


def book_assets_path(name):
    return asset_path(f"books/{slugify(name)}")


def author_assets_fs_path(name):
    return f"assets/authors/{slugify(name)}"


def book_assets_fs_path(name):
    return f"assets/books/{slugify(name)}"


def portrait_path(name):
    return f"{author_assets_path(name)}/portrait.jpg"


def portrait_fs_path(name):
    return f"{author_assets_fs_path(name)}/portrait.jpg"


def cover_path(name):
    return f"{book_assets_path(name)}/cover.jpg"


def cover_fs_path(name):
    return f"{book_assets_fs_path(name)}/cover.jpg"


def product_page_path(name):
    return page_path(f"products/{slugify(name)}.html")


def author_page_path(name):
    return page_path(f"authors/{slugify(name)}.html")
