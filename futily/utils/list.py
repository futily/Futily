def filter_unique_dict(items, dict_key):
    """
    Filter a list of dicts by their unique key
    :param items:
    :param dict_key:
    :return:
    """
    seen = set()
    seen_add = seen.add

    return [x for x in items if not (x[dict_key] in seen or seen_add(x[dict_key]))]


def find_dict_by_value(lst, key, value):
    for dic in lst:
        if dic[key] == value:
            return dic

    return ValueError('No dicts found')
