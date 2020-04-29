import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from data import db_session
from data.__all_models import User, WikiDB
import random


def bot(status, recipient=None):
    vk_session = vk_api.VkApi(
        token='38eaceba8f2e4284f487793011452e4d7cd637cffbb11605b451d3cf71b1fdf2628793ef25cd0b4f8a0ad')
    vk = vk_session.get_api()

    db_session.global_init('db/DataBase.sqlite')
    session = db_session.create_session()
    messages = {'wiki_change': 'В раздел WIKI длбавлена новая запись', 'new_record': 'На форум добавлена новая запись',
                'new_comment': 'Под Вашей записью оставлен новый комментарий'}

    if status == "new_comment":
        recipients = [recipient]
    else:
        recipients = session.query(User)
    print(recipients)
    for elem in recipients:
        print(elem.vk_id)
        if len(str(elem.vk_id)):
            try:
                vk.messages.send(user_id=vk.users.get(user_ids=[elem.vk_id])[0]['id'],
                                 message=f'{messages[status]} \n http://127.0.0.1:8000/forum',
                                 random_id=random.randint(0, 2 ** 64))
            except:
                pass


if __name__ == '__main__':
    bot('new_record')
