from . import root
from flask import render_template, request, current_app as app
from ..models import NewsArticle

@root.route('/')
def home():
    page = int(request.args.get('page', 1))
    paginate = NewsArticle.query.order_by(NewsArticle.time_written).paginate(
        page, per_page=app.config['RESULTS_PER_PAGE']
    )
    articles = paginate.items
    return render_template('base.html', articles=articles, pagination=paginate)


@root.route('/article/<int:article_id>')
def get_article(article_id):
	article = NewsArticle.query.get_or_404(article_id)
	return render_template('article/article.html', article=article)