from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, SubmitField)
from wtforms.validators import InputRequired, Regexp


class InputForm(FlaskForm):
    link = StringField('Type YouTube video URL here',
                       validators=[InputRequired('Please enter URL'),
                                   Regexp('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', message="Enter YouTube video URL")],
                       render_kw={"placeholder": "YouTube Video URL"}
                       )
    algorithm = SelectField('Choose Your Summarization Algorithm',
                            choices=[("gensim-sum", "Text Rank Algorithm(Gensim)"),
                                     ("sumy-lsa-sum",
                                      "Latent Semantic Analysis Based(Sumy)"),
                                     ("sumy-luhn-sum", "Luhn Algorithm Based(Sumy)"),
                                     ("sumy-text-rank-sum",
                                      "Text Rank Algorithm(Sumy)")
                                     ],
                            default=1
                            )
    percentage = StringField('Enter a percentage', validators=[
                             InputRequired('Please enter some Percentage')])
    submit = SubmitField("summarize")
