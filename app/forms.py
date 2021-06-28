from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm

class ShopForm(FlaskForm):
    shopName = StringField(
        'Enter shop name',
        [
            validators.DataRequired(message="Shop name must be given"),
            validators.Length(min=1, max=99, message="Shop name must have 1-99 characters")
        ])
    submit = SubmitField('Extract')
