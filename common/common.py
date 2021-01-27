from setting import baoninhbinh
from cache import cache


class NewsCommon:
    @staticmethod
    @cache.memoize(timeout=60)
    def get_all_cates():
        print('get_all_cates')
        return baoninhbinh.query_table('SELECT id,title,slug FROM category  WHERE locked=0 ORDER BY priority LIMIT 100;')

    @staticmethod
    @cache.memoize(timeout=60)
    def get_all_widgets():
        return baoninhbinh.query_table('SELECT * FROM widget ORDER BY priority ASC LIMIT 100;')
