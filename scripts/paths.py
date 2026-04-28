def author_assets_path(name):
    return f"/assets/authors/{name.lower().replace(' ', '-')}"


def book_assets_path(name):
    return f"/assets/books/{name.lower().replace(' ', '-')}"


def portrait_path(name):
    return f"{author_assets_path(name)}/portrait.jpg"


def cover_path(name):
    return f"{book_assets_path(name)}/cover.jpg"
