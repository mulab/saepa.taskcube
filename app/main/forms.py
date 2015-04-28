from flask.ext.wtf import Form
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from  wtforms.validators import Email


class UserForm(Form):
    name = StringField('姓名：', validators=[DataRequired()])
    email = StringField('邮箱：', validators=[Email()])
    mobile = StringField('手机：', validators=[DataRequired()])
    submit = SubmitField('提交')
