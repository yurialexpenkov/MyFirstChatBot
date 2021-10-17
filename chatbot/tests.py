from copy import deepcopy
from random import randint
from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEvent

import settings
from bot import Bot

from freezegun import freeze_time

from generate_ticket import generate_ticket


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()
    return wrapper




class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'message':
                                {'date': 1608149295, 'from_id': 295085, 'id': 99, 'out': 0, 'peer_id': 295085,
                                 'text': '513561', 'conversation_message_id': 99, 'fwd_messages': [],
                                 'important': False,
                                 'random_id': 0, 'attachments': [], 'is_hidden': False},
                            'client_info': {'button_actions':
                                                ['text', 'vkpay', 'open_app', 'location', 'open_link',
                                                 'intent_subscribe', 'intent_unsubscribe'],
                                            'keyboard': True, 'inline_keyboard': True, 'carousel': False,
                                            'lang_id': 0}},
                 'group_id': 200948135, 'event_id': 'ce6a13de8ddb596d6e1c48b494c66a600217449c'}

    def test_run(self):
        count = 5
        obj = {'a', 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    INPUTS = [
        'Привет',
        '/help',
        '/ticket',
        'Санкт-Петербург',
        'пхукет',
        '05-12-2019',
        '1',
        '5',
        "!!!",
        'да',
        'Yuri',
        'Penkov'
    ]

    context_for_test = dict()
    context_for_test['sity_of_departyre'] = 'санкт-петербург'
    context_for_test['sity_of_arrival'] = 'пхукет'
    context_for_test['list_aircraft_flight'] = [[1, 'вариант - 05-12-2019 20:30'], [2, 'вариант - 06-12-2019 20:30'],
                                                [3, 'вариант - 07-12-2019 20:30'], [4, 'вариант - 08-12-2019 20:30'],
                                                [5, 'вариант - 09-12-2019 20:30']]
    context_for_test['selected_flight_date'] = 'вариант - 05-12-2019 20:30'
    context_for_test['comment_entry'] = '!!!'

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.DATABASE[0]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'].format(**context_for_test),
        settings.SCENARIOS['registration']['steps']['step3']['text'],
        settings.SCENARIOS['registration']['steps']['step4']['text'].format(**context_for_test),
        settings.SCENARIOS['registration']['steps']['step5']['text'].format(**context_for_test),
        settings.SCENARIOS['registration']['steps']['step6']['text'],
        settings.SCENARIOS['registration']['steps']['step7']['text'].format(**context_for_test),
        settings.SCENARIOS['registration']['steps']['step8']['text'],
        settings.SCENARIOS['registration']['steps']['step9']['text'],
        settings.SCENARIOS['registration']['steps']['step10']['text'].format(**context_for_test),
    ]

    @freeze_time("Sep 16th, 2019")
    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        for real, expec in zip(real_outputs, self.EXPECTED_OUTPUTS):
            print(real)
            print('-' * 50)
            print(expec)
            print('-' * 50)
            print(real == expec)
            print('_' * 50)
        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        ticket_file = generate_ticket('Yuri', 'Penkov', 'Санкт-Петербург', 'Пхукет', '05-12-2022')
        with open('files/ticket-example.png', 'rb') as expected_file:
            expected_file_bytes = expected_file.read()

        assert ticket_file.read() == expected_file_bytes
