from algoliasearch_django import AlgoliaIndex


class PlayerIndex(AlgoliaIndex):
    fields = ['name', 'first_name', 'last_name', 'common_name', 'english_names', 'slug', 'id', 'rating', 'color',
              'position']
    # geo_field = 'location'
    settings = {
        'searchableAttributes': ['name', 'first_name', 'last_name', 'common_name'],
        'customRanking': ['desc(rating)', 'asc(name)']
    }
    index_name = 'player_index'
