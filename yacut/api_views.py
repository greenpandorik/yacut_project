from flask import jsonify, request
from http import HTTPStatus as status

from . import app, db
from .utils import check_symbols, check_uniq_link, get_unique_short_id
from .error_handlers import InvalidAPIUsage
from .models import URLMap

MAX_LENGHT = 16


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    custom_id = data.get("custom_id")
    if custom_id:
        if not check_symbols(custom_id) or len(custom_id) > MAX_LENGHT:
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки")
        if check_uniq_link(custom_id):
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
        data['short_link'] = custom_id
    else:
        data['short_link'] = get_unique_short_id()
    if 'url' not in data or data.get('url') is None:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!', status.BAD_REQUEST)
    new_link = URLMap()
    new_link.from_dict(data)
    db.session.add(new_link)
    db.session.commit()
    return jsonify(new_link.to_dict()), status.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', status.NOT_FOUND)
    return jsonify({'url': url.original}), status.OK
