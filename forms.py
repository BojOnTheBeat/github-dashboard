from wtforms import Form, StringField, validators, SelectField, IntegerField
from sort_metrics import SORT_METRICS


class SearchForm(Form):
    org = StringField('Organization', [validators.Length(min=0, max=30)])
    sort_by = SelectField('Sort By', choices = [(val, val) for val in SORT_METRICS])
    limit = IntegerField('Limit', [validators.NumberRange(min=0)])