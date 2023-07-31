from flask import render_template

from . import app
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        url = form.original.data
        return get_unique_short_id(url)
    return render_template('index.html', form=form)
    pass
