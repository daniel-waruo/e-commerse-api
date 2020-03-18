from functools import reduce

from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

from business.products.models import Product


def filter_products(kwargs):
    category_ids = kwargs.get("category_Ids")
    category_slugs = kwargs.get("categorySlugs")
    query = kwargs.get("query")

    # initial queryset object
    query_set = Product.objects.all()

    # if categoryIds and query not provided
    if not (category_ids or query or category_slugs):
        return query_set
    # TODO: remove category ids filter as it redundant after fully migrating to using slugs
    # if categoryIds filter
    if category_ids:
        query_set = query_set.filter(category_id__in=category_ids)

    # if categorySlugs filter
    if category_slugs:
        query_set = query_set.filter(category__slug__in=category_slugs)

    # if query filter according to the query
    if query:
        # get the list of search queries
        queries = map(lambda x: SearchQuery(x), query.split())
        # get the reduced search queries using the or
        queries_or = reduce(lambda a, b: a | b, queries)
        # get the search vector
        vector = SearchVector('name', weight='A') + \
                 SearchVector('description', weight='B') + \
                 SearchVector('category__name', weight='C')

        # set search rank
        rank = SearchRank(vector, queries_or)
        query_set = query_set.annotate(
            rank=rank
        ).order_by('-rank')

    # return query set
    return query_set


def filter_by_price(query_set, kwargs):
    min_price = kwargs.get("min")
    max_price = kwargs.get("max")

    # if min and max filter
    if min_price or max_price:
        query_set = query_set.filter(
            discount_price__gte=min_price,
            discount_price__lte=max_price
        )
    return query_set
