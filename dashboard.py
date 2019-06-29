from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators, SelectField, IntegerField
from github import Github
import os




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

    g = Github(os.environ["GITHUB_TOKEN"])

    org = g.get_organization(str(org))


    sort_function = sort_metrics[sort_by]

    repos = sort_function(org.get_repos(), lim=int(limit))

    return render_template('view.html', repos=repos, sort_by=sort_by)


def get_org(org):
    g = Github(os.environ["GITHUB_TOKEN"])

    org = g.get_organization(str(org))

    return org

def get_org_repos(org_name):
    g = Github(os.environ["GITHUB_TOKEN"])

    org = g.get_organization(str(org_name))

    return list(org.get_repos())

def sort_by_stars(repos, lim=10):
    # (Generator[repos] -> List[repos])
    return sorted(repos, key=lambda x: x.stargazers_count, reverse=True)[:lim]

def sort_by_forks(repos, lim=10):
    # (Generator[repos] -> List[repos])
    return sorted(repos, key=lambda x: x.forks_count, reverse=True)[:lim]

def sort_by_contributors(repos, lim=10):
    # (Generator[repos] -> List[repos])

    # get list of contributors then count it.
    return sorted(repos, key=get_num_contributors, reverse=True)[:lim]

def get_num_contributors(repo):
    return repo.get_contributors().totalCount


class SearchForm(Form):

    sorts = ['Stars', 'Forks', 'Contributors']

    org = StringField('Organization', [validators.Length(min=0, max=30)])
    sort_by = SelectField('Sort By', choices = [(val, val) for val in sorts])
    limit = IntegerField('Limit', [validators.NumberRange(min=0)])

sort_metrics = {
    'Stars': sort_by_stars,
    'Forks': sort_by_forks,
    'Contributors': sort_by_contributors
}