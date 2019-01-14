import os

from dostoevsky.tokenization import UDBaselineTokenizer
from dostoevsky.word_vectors import SocialNetworkWordVectores
from dostoevsky.models import SocialNetworkModel
from dostoevsky.data import DataDownloader, DATA_BASE_PATH, AVAILABLE_FILES


MODEL = None


def init_dostoevsky():
    global MODEL

    downloader = DataDownloader()
    for filename in ['vk-embeddings', 'cnn-social-network-model']:
        source, destination = AVAILABLE_FILES[filename]
        destination_path = os.path.join(DATA_BASE_PATH, destination)
        if os.path.exists(destination_path):
            continue
        downloader.download(source=source, destination=destination)

    tokenizer = UDBaselineTokenizer()
    word_vectors_container = SocialNetworkWordVectores()

    MODEL = SocialNetworkModel(
        tokenizer=tokenizer,
        word_vectors_container=word_vectors_container,
        lemmatize=False,
    )


def sentiment_analysis(message):
    result = MODEL.predict([message])[0]
    if result == 'negative':
        return -1.
    elif result == 'positive':
        return 1.
    else:
        return 0.
