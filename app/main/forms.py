from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    """
    定义帖子的表单
    """
    title = StringField(label='标题', validators=[DataRequired()])
    body = PageDownField(label='正文', validators=[DataRequired()])
    submit = SubmitField(label='发表')


class CommentForm(FlaskForm):
    """
    帖子评论表单
    """
    body = PageDownField(label='评论', validators=[DataRequired()])
    submit = SubmitField(label='发表')














