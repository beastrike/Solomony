import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import pymysql.cursors
import requests
import random
id = '219675967'


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.ilroIMCZd4Vq6Zxrq3bKfnWoKz6sSL-E4QhjPOIA3yH1q1Cf9iQI9PhFeL5h4S23LybRiu4ZsJOIf5lF-GTXI12U8s8ynJ4ow8dL9dnd42rxJJyHTJWZTuKFr4j8U4tsJnm2IxRmsmZx75Ja6CoEvgBdLgSflFXsM9YGZS2b33-1pyFel0HCI4qY2oVAYC4Ss0xhrWdz_odpE8Cwzflt8g')

    longpoll = VkBotLongPoll(vk_session, id)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Спасибо, что написали нам. Мы обязательно ответим",
                             random_id=random.randint(0, 2 ** 64))

def get_connection():
    connection = pymysql.connect(host='you_host',
                                 user='you_user',
                                 password='you_password',
                                 db='you_db',
                                 charset='utf8mb4',
                                 cursorclass=mymysql.cursors.DictCursor)
    return connection

def add_to_database(function_mode, x):
    #Создаем новую сессию
    connection = getConnection()
    #Будем получать информацию от сюда
    cursor = connection.cursor()
    #Наш запрос
    sql = "INSERT INTO mode (Id_User, Mode) VALUES (%s, %s) ON DUPLICATE KEY UPDATE Mode = %s"
    #Выполняем наш запрос и вставляем свои значения
    cursor.execute(sql, (x, function_mode, function_mode))
    #Делаем коммит
    connection.commit()
    #Закрываем подключение
    connection.close()
    #Возвращаем результат
    return function_mode

def select_from_database(x):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT Mode FROM mode WHERE Id_User = %s"
    cursor.execute(sql, (x,))
    #Получаем запрашиваемые данных и заносим их в переменные
    for i in cursor:
        mode_send = i['Mode']
    #Проверяем точно ли есть такая запись
    if cursor.fetchall() == ():
        mode_send = 'Вы еще не пробовали'
    connection.close()
    return mode_send


if __name__ == '__main__':
    main()
