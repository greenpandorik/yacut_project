from flask import flash, redirect, render_template, request

from . import app, db
from .utils import check_uniq_link, get_unique_short_id
from .forms import Link_Form
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = Link_Form()
    if form.validate_on_submit():
        if not form.original_link.data:
            form.original_link.errors = ['Данная строка не может быть пустой!']
            return render_template("index.html", form=form)
        short_url = form.custom_id.data or get_unique_short_id()
        if check_uniq_link(short_url):
            form.custom_id.errors = [f'Имя {short_url} уже занято!']
        else:
            url_model = URLMap(
                original=form.original_link.data,
                short=short_url)
            db.session.add(url_model)
            db.session.commit()
            flash(f'Ваша новая ссылка готова: '
                  f'<a href="{request.base_url}{short_url}">'
                  f'{request.base_url}{short_url}</a>')
    return render_template("index.html", form=form)


@app.route('/<string:short_url>')
def redirect_to_url(short_url):
    url = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(url.original)
