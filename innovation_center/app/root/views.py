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
    print(paginate.page)
    return render_template('base.html', articles=articles, pagination=paginate)