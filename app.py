import logging

from flask import Flask
from flask import render_template
from cache import cache
from common.common import NewsCommon
from setting import baoninhbinh

app = Flask(__name__)
cache.init_app(app)


@app.route('/')
@cache.cached(timeout=60 * 10)
def home():
    all_cates = NewsCommon.get_all_cates()
    widgets = NewsCommon.get_all_widgets()
    for i, cate in enumerate(all_cates):
        cate['articles'] = baoninhbinh.query_table('SELECT id,title,description,thump, slug FROM article WHERE category_id=:cid ORDER BY publish DESC LIMIT 5;', {'cid': cate['id']})
    newest = baoninhbinh.query_table('SELECT id,title,description,thump, slug FROM article ORDER BY publish DESC LIMIT 5;')
    articles = baoninhbinh.query_table('SELECT id,title,description,thump,slug FROM article ORDER BY publish DESC LIMIT 5;')
    article_news = baoninhbinh.query_table('SELECT id,title,description,slug FROM article LIMIT 8;')
    return render_template('web/home.html', cates=all_cates, newest=newest, articles=articles, article_news=article_news, widgets=widgets)


@app.route('/<category_slug>')
@cache.cached(timeout=60 * 10)
def categorys(category_slug):
    all_cates = NewsCommon.get_all_cates()
    widgets = NewsCommon.get_all_widgets()
    category = baoninhbinh.query_row('SELECT id,title,slug FROM category WHERE slug=:cate_slug LIMIT 1', {'cate_slug': category_slug})
    articles = baoninhbinh.query_table('SELECT id,title,description,thump, slug FROM article  WHERE category_id=:id ORDER BY publish DESC LIMIT 20;', {'id': category['id']})
    return render_template('web/category.html', articles=articles, cates=all_cates, widgets=widgets, category=category)


@app.route('/<_>/<int:article_id>')
@cache.cached(timeout=60 * 10)
def article_detail(_, article_id):
    all_cates = NewsCommon.get_all_cates()
    article = baoninhbinh.query_row('SELECT * FROM article WHERE id=:id LIMIT 1;', {'id': article_id})
    widgets = NewsCommon.get_all_widgets()
    return render_template('web/article.html', article=article, cates=all_cates, widgets=widgets)


@app.route('/editor')
def editor():
    return render_template('web/editor.html')


file_handler = logging.FileHandler('logging.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run()
