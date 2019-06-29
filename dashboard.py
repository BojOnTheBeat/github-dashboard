from flask import Flask, render_template, request, redirect, url_for
from forms import SearchForm
from sort_metrics import get_sort_function_from_sort_metric, SORT_METRICS, get_repos_for_org


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)

    if request.method == 'POST' and form.validate():
        org = form.org.data
        sort_by = form.sort_by.data
        limit = form.limit.data
        return redirect(url_for('get_org', sort_by=sort_by, org=org, limit=limit))
  
    return render_template('home.html', form=form)

@app.route('/search/<sort_by>/<org>/<limit>')
def get_org(org, sort_by, limit=10):
    
    repos = get_repos_for_org(str(org))

    sort_function = get_sort_function_from_sort_metric(sort_by)

    results = sort_function(repos, lim=int(limit))

    return render_template('view.html', repos=results, sort_by=sort_by)


