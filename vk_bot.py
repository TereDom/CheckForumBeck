import vk_api
from data import db_session
from data.__all_models import User
import random


def bot(status, recipient=None):
    vk_session = vk_api.VkApi(
        token='38eaceba8f2e4284f487793011452e4d7cd637cffbb11605b451d3cf71b1fdf2628793ef25cd0b4f8a0ad')
    vk = vk_session.get_api()

    db_session.global_init('db/DataBase.sqlite')
    session = db_session.create_session()
    messages = {'wiki_change': 'В раздел WIKI длбавлена новая запись', 'new_record': 'На форум добавлена новая запись',
                'new_comment': 'Под Вашей записью оставлен новый комментарий',
                'delete_news': 'Ваша запись удалена модератором сайта'}

    if status == "new_comment" or status == "delete_news":
        recipients = [recipient]
    else:
        recipients = session.query(User)
    for elem in recipients:
        if len(str(elem.vk_id)):
            try:
                vk.messages.send(user_id=vk.users.get(user_ids=[elem.vk_id])[0]['id'],
                                 message=f'{messages[status]} \n http://checkbecksite.herokuapp.com/forum',
                                 random_id=random.randint(0, 2 ** 64))
            except:
                pass


if __name__ == '__main__':
    bot('new_record')
