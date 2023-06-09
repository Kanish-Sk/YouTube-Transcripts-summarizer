# Gensim Imports
from gensim.summarization.summarizer import summarize


# NLTK Imports
from nltk.tokenize import sent_tokenize

# Sumy Imports
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def gensim_summarize(text_content, percent):
    # TextRank Summarization using Gensim Library.
    # Split is false, gensim return strings joined by "\n". if true, gensim will return list
    summary = summarize(text_content, ratio=(int(percent) / 100), split=False).replace("\n", " ")

    # Returning NLTK Summarization Output
    return summary


def sumy_lsa_summarize(text_content, percent):
    # Latent Semantic Analysis is a unsupervised learning algorithm that can be used for extractive text summarization.
    # Initializing the parser
    parser = PlaintextParser.from_string(text_content, Tokenizer("english"))
    # Initialize the stemmer
    stemmer = Stemmer('english')
    # Initializing the summarizer
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')

    # Finding number of sentences and applying percentage on it: since sumy requires number of lines
    sentence_token = sent_tokenize(text_content)
    select_length = int(len(sentence_token) * (int(percent) / 100))

    # Evaluating and saving the Summary
    summary = []
    for sentence in summarizer(parser.document, sentences_count=select_length):
        summary.append(str(sentence))
    # Returning NLTK Summarization Output
    print(summary)
    return summary


def sumy_luhn_summarize(text_content, percent):
    # A naive approach based on TF-IDF and looking at the “window size” of non-important words between words of high
    # importance. It also assigns higher weights to sentences occurring near the beginning of a document.
    # Initializing the parser
    parser = PlaintextParser.from_string(text_content, Tokenizer("english"))
    # Initialize the stemmer
    stemmer = Stemmer('english')
    # Initializing the summarizer
    summarizer = LuhnSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')

    # Finding number of sentences and applying percentage on it: since sumy requires number of lines
    sentence_token = sent_tokenize(text_content)
    select_length = int(len(sentence_token) * (int(percent) / 100))

     # Evaluating and saving the Summary
    summary = []
    for sentence in summarizer(parser.document, sentences_count=select_length):
        summary.append(str(sentence))
    # Returning NLTK Summarization Output
    print(summary)
    return summary


def sumy_text_rank_summarize(text_content, percent):
    # TextRank is an unsupervised text summarization technique that uses the intuition behind the PageRank algorithm.
    # Initializing the parser
    parser = PlaintextParser.from_string(text_content, Tokenizer("english"))
    # Initialize the stemmer
    stemmer = Stemmer('english')
    # Initializing the summarizer
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')

    # Finding number of sentences and applying percentage on it: since sumy requires number of lines
    sentence_token = sent_tokenize(text_content)
    select_length = int(len(sentence_token) * (int(percent) / 100))

     # Evaluating and saving the Summary
    summary = []
    for sentence in summarizer(parser.document, sentences_count=select_length):
        summary.append(str(sentence))
    # Returning NLTK Summarization Output
    print(summary)
    return summary