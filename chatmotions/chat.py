import asyncio
import logging

import iso8601

from chatmotions.sentiment import sentiment_analysis

log = logging.getLogger(__name__)

CHATS = {}


class Chat:
    POSITIVE_THRESHOLD = 0.25
    NEGATIVE_THRESHOLD = -0.25

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._last_message_timestamp = None
        self._chat_polarity = 0

    def message_posted(
        self, author, message, timestamp, **kwargs
    ):
        try:
            timestamp = iso8601.parse_date(timestamp)
        except iso8601.ParseError:
            log.exception('Timestamp could not be parsed: {}'.format(timestamp))
            return

        polarity = sentiment_analysis(message)
        log.info('Message {} received. Polarity is {}'.format(message, polarity))
        self.recalc_polarity(polarity, timestamp)

        self._last_message_timestamp = timestamp

    def recalc_polarity(self, polarity, timestamp):
        alpha = 0.15
        self._chat_polarity = (1 - alpha) * self._chat_polarity + alpha * polarity
        log.info('New polarity for {}: {}'.format(self.chat_id, self._chat_polarity))

    def reset_polarity(self):
        self._chat_polarity = 0.

    def should_respond(self):
        if self._chat_polarity > self.POSITIVE_THRESHOLD:
            return 1
        if self._chat_polarity < self.NEGATIVE_THRESHOLD:
            return -1
        return 0


def get_chat(chat_id):
    if chat_id not in CHATS:
        CHATS[chat_id] = Chat(chat_id)

    return CHATS[chat_id]
