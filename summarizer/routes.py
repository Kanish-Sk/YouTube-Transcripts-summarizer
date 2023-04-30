from summarizer.summary import gensim_summarize, sumy_lsa_summarize, sumy_luhn_summarize, sumy_text_rank_summarize
import nltk
from flask import render_template, redirect, url_for, Blueprint

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable, TooManyRequests, \
    TranscriptsDisabled, NoTranscriptAvailable
from youtube_transcript_api.formatters import TextFormatter

from summarizer.form import InputForm

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


# NLTK Imports

# Summarizer Import (Our Another File: summarizer.py)

details = {"link": None, "algorithm": None, "percentage": None}

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

# "Punkt" download before nltk tokenization
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print('Downloading punkt')
    nltk.download('punkt', quiet=True)


@pages.route("/", methods=["GET", "POST"])
def home():
    form = InputForm()

    if form.validate_on_submit():
        details["link"] = form.link.data
        details["percentage"] = form.percentage.data
        details["algorithm"] = form.algorithm.data

        return redirect(url_for('pages.summarize'))

    return render_template('home.html', title='YouTube Transcript Summarizer', form=form)


@pages.route('/summarize', methods=["GET", "POST"])
def summarize():
    parsed = details["link"].split("=")
    video_id = parsed[1]

    try:
        # Using Formatter to store and format received subtitles properly.
        formatter = TextFormatter()
        transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        formatted_text = formatter.format_transcript(
            transcript).replace("\n", " ")

        # Checking the length of sentences in formatted_text string, before summarizing it.
        num_sent_text = len(nltk.sent_tokenize(formatted_text))

        # Pre-check if the summary will have at least one line .
        select_length = int(num_sent_text * (int(details["percentage"]) / 100))

        # Summary will have at least 1 line. Proceed to summarize.
        if select_length > 0:
            # Condition satisfied for summarization, summarizing the formatted_text based on choice.
            if num_sent_text > 1:
                # Summarizing Formatted Text based upon the request's choice
                if details["algorithm"] == "gensim-sum":
                    # Gensim Library for TextRank Based Summary.
                    summary = gensim_summarize(
                        formatted_text, int(details["percentage"]))
                elif details["algorithm"] == "sumy-lsa-sum":
                    # Sumy for extractive summary using LSA.
                    summary = sumy_lsa_summarize(
                        formatted_text,  int(details["percentage"]))
                elif details["algorithm"] == "sumy-luhn-sum":
                    # Sumy Library for TF-IDF Based Summary.
                    summary = sumy_luhn_summarize(
                        formatted_text, int(details["percentage"]))
                elif details["algorithm"] == "sumy-text-rank-sum":
                    # Sumy for Text Rank Based Summary.
                    summary = sumy_text_rank_summarize(
                        formatted_text, int(details["percentage"]))
                else:
                    summary = None

                # Checking the length of sentences in summary string.

                if (details["algorithm"] == "gensim-sum"):
                    num_sent_summary = len(nltk.sent_tokenize(summary))
                    summary2 = nltk.sent_tokenize(summary)
                    summary2 = [str.capitalize() for str in summary2]

                else:
                    num_sent_summary = len(summary)
                    summary2 = summary

                # Returning Result
                response_list = {
                    # 'fetched_transcript': formatted_text,
                    'processed_summary': summary2,
                    'length_original': len(formatted_text),
                    'length_summary': len(summary),
                    'sentence_original': num_sent_text,
                    'sentence_summary': num_sent_summary
                }

                success = True
                message = "Subtitles for this video was fetched and summarized successfully."
                response = response_list

            else:
                success = False
                message = '''Subtitles are not formatted properly for this video. 
                Unable to summarize. There is a possibility that there is no punctuation in subtitles of your video.'''

        else:
            success = False
            message = f'''Number of lines in the subtitles of your video is not enough to generate a summary. 
            Number of sentences in your video: {num_sent_text}'''

            response = None

    # Catching Exceptions
    except VideoUnavailable:
        success = False
        message = "VideoUnavailable: The video is no longer available."
        response = None

    except TooManyRequests:
        success = False
        message = '''TooManyRequests: YouTube is receiving too many requests from this IP.
        Wait until the ban on server has been lifted.'''
        response = None

    except TranscriptsDisabled:
        success = False
        message = "TranscriptsDisabled: Subtitles are disabled for this video."
        response = None

    except NoTranscriptAvailable:
        success = False
        message = "NoTranscriptAvailable: No transcripts are available for this video."
        response = None

    except NoTranscriptFound:
        success = False
        message = "NoTranscriptAvailable: No transcripts were found."
        response = None

    except Exception:
        success = False
        message = '''Some error occurred.
        Contact the administrator if it is happening too frequently.'''
        response = None

    return render_template('summarize.html', success=success, message=message, response=response, title='Summarized Text')


# Error loading stopwords: <urlopen error [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond>
