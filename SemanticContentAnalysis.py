from collections import Counter

from pydub import AudioSegment
import whisper
from pathlib import Path
import json
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    sentiment = "Positive" if sentiment_scores["compound"] > 0 else "Negative" if sentiment_scores["compound"] < 0 else "Neutral"
    return sentiment

def averageSentencesLength(text):
    sentences = text.split('.')
    total = 0
    for sentence in sentences:
        total += len(sentence.split())
    return total / len(sentences)

def averageWordLength(text):
    words = text.split()
    total = 0
    for word in words:
        total += len(word)
    return total / len(words)

def frequentWords(text):
    words = text.split()
    return Counter(words).most_common(10)

def lexicalDiversityScore(text):
    words = text.split()
    return (len(set(words)) / len(words))*100

def calculate_overall_score(statistics):
    weights = {
        "Sentiment": 15,
        "Total Words": 10,
        "Average Word Length": 15,
        "Average Sentence Length": 20,
        "Frequent Words": 10,
        "Lexical Diversity Score": 15,
    }

    sentiment_score = 100 if statistics["Sentiment"] == "Positive" else 0
    total_words_score = min((statistics["Total Words"] / 200) * 100, 100)  #  500 words is a perfect score
    avg_word_length_score = min((statistics["Average Word Length"] / 5) * 100, 100)  #  5 is a perfect score
    avg_sentence_length_score = min((statistics["Average Sentence Length"] / 15) * 100, 100)  #  30 is a perfect score
    frequent_words_score = sum([count for _, count in statistics["Frequent Words"]]) / 10  #  the highest count is 10
    lexical_diversity_score = min(statistics["Lexical Diversity Score"], 50)

    overall_score = (
        weights["Sentiment"] * sentiment_score +
        weights["Total Words"] * total_words_score +
        weights["Average Word Length"] * avg_word_length_score +
        weights["Average Sentence Length"] * avg_sentence_length_score +
        weights["Frequent Words"] * frequent_words_score +
        weights["Lexical Diversity Score"] * lexical_diversity_score
    ) / sum(weights.values())

    return round(overall_score, 2)

def get_statistics(file):
    audio_transcribe = AudioSegment.from_wav(file)
    audio_transcribe = audio_transcribe.set_channels(1)
    audio_transcribe = audio_transcribe.set_frame_rate(16000)
    audio_transcribe.export("audio_transcribe.wav", format="wav")

    model = whisper.load_model('base')
    path = Path('audio_transcribe.wav')
    result = model.transcribe(str(path), language='en', verbose=False)

    with open('transcribe.txt', 'w') as file:
        file.write(result['text'])

    text=result['text']

    sentiment = analyze_sentiment(text)
    average_word_length = int(averageWordLength(text))
    average_sentence_length = int(averageSentencesLength(text))
    frequent_words = frequentWords(text)
    lexical_diversity_score = lexicalDiversityScore(text)



    dict_content = {
        "Sentiment": sentiment,
        "Total Words": len(text.split()),
        "Average Word Length": average_word_length,
        "Average Sentence Length": average_sentence_length,
        "Frequent Words": frequent_words,
        "Lexical Diversity Score": int(lexical_diversity_score),
        "Transcript": text,
    }
    calculate_overall_score(dict_content)
    dict_content["Overall Score"] = int(calculate_overall_score(dict_content))
    return dict_content
