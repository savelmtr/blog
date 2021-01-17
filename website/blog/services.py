def count_pages(count, per_page):
    return count // per_page + (1 if count % per_page else 0)
