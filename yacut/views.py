from flask import flash, redirect, render_template
from flask_api import status

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        url = form.original_link.data
        custom = form.custom_id.data
        if custom:
            if URLMap.query.filter_by(short=custom).first() is not None:
                flash(f'Имя {custom} уже занято!')
                return render_template('index.html', form=form), status.HTTP_400_BAD_REQUEST
            else:
                urlmap = URLMap(
                    original=url,
                    short=custom,
                )
                db.session.add(urlmap)
                db.session.commit()
                flash('Ваша новая ссылка готова:')
                return render_template('index.html', form=form, short=custom), status.HTTP_201_CREATED
        else:
            short, code = get_unique_short_id(url)
            if URLMap.query.filter_by(original=url).first() is not None and custom:
                flash(f'Для адреса {url} уже есть короткая ссылка')
                return render_template('index.html', form=form, short=short, code=status.HTTP_400_BAD_REQUEST)
            if code == status.HTTP_201_CREATED:
                urlmap = URLMap(
                    original=url,
                    short=short,
                )
                db.session.add(urlmap)
                db.session.commit()
                flash('Ваша новая ссылка готова:')
                return render_template('index.html', form=form, short=short), code
            elif code == status.HTTP_200_OK:
                flash('Ваша ссылка:')
                return render_template('index.html', form=form, short=short)
    return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET', ])
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original, code=status.HTTP_302_FOUND)
