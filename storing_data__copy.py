import pickle
from collections import defaultdict
from redis import Redis
from telegram.ext import DictPersistence, BasePersistence
from telegram.ext.utils.types import ConversationDict, BD, CD, UD
from typing import Optional, Tuple, DefaultDict
from exceptions import StoringDataError


class FishShopPersistence(DictPersistence):
    def __init__(
        self,
        reddisdb: Redis,
        on_flush: bool = False,
        store_user_data: bool = False,
        store_chat_data: bool = False,
        store_bot_data: bool = False,
        store_callback_data: bool = False
    ):
        super().__init__(store_user_data, store_chat_data, store_bot_data, store_callback_data)
        self.reddisdb = reddisdb
        self.on_flush = on_flush
        self.conversations = None
        self.on_flush = False

    def load_redis(self) -> None:
        try:
            data_bytes = self.reddisdb.get('TelegramBotPersistence')
            if data_bytes:
                data = pickle.loads(data_bytes)
                self.user_data = defaultdict(dict, data['user_data'])
                self.chat_data = defaultdict(dict, data['chat_data'])
                # For backwards compatibility with files not containing bot data
                self.bot_data = data.get('bot_data', {})
                self.conversations = data['conversations']
            else:
                self.conversations = dict()
                self.user_data = defaultdict(dict)
                self.chat_data = defaultdict(dict)
                self.bot_data = {}
        except TypeError as exc:
            raise StoringDataError(
                f"Something went wrong unpickling from Redis, exception is:\n{exc}"
                )

    def dump_redis(self) -> None:
        data = {
            'conversations': self.conversations,
            'user_data': self.user_data,
            'chat_data': self.chat_data,
            'bot_data': self.bot_data,
        }
        data_bytes = pickle.dumps(data)
        self.reddisdb.set('TelegramBotPersistence', data_bytes)

    def get_conversations(self, name: str) -> ConversationDict:
        '''Returns the conversations from the pickle on Redis if it exsists or an empty dict.'''
        if self.conversations:
            pass
        else:
            self.load_redis()
        return self.conversations.get(name, {}).copy()

    def update_conversation(self, name: str, key: Tuple[int, ...], new_state: Optional[object]) -> None:
        '''Will update the conversations for the given handler and depending on :attr:`on_flush` save the pickle on Redis.'''
        if not self.conversations:
            self.conversations = dict()
        if self.conversations.setdefault(name, {}).get(key) == new_state:
            return
        self.conversations[name][key] = new_state
        if not self.on_flush:
            self.dump_redis()
