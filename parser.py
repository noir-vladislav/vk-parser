import requests
import json
import os
import time


token = '' #Enter u token
version = 5.92
count = 100

owner_ids = [
    {'owner_id': '-47220519', 'Название города': 'Иркутск'},
    {'owner_id': '-59717127', 'Название города': 'Красноярск'},
    {'owner_id': '-185731622', 'Название города': 'Якутск'},
    {'owner_id': '-64949021', 'Название города': 'Москва'},
    {'owner_id': '-72816921', 'Название города': 'Владивосток'},
    {'owner_id': '-67083068', 'Название города': 'CПБ'},
    {'owner_id': '-113706151', 'Название города': 'Грозный'},
]

for owner_id in owner_ids:

    all_posts = []
    offset = 0

    while offset<=1500:

        response = requests.get('https://api.vk.com/method/wall.get',
                params={
                    'access_token':token,
                    'v': version,
                    'owner_id':owner_id['owner_id'],
                    'count': count,
                    'offset': offset
                }
            )

        posts = response.json()['response']['items']
        offset += count

        print(offset)

        for post in posts:
            all_posts.append({
                'owner_id': post['owner_id'],
                'id': post['id'],
                'text': post['text']
            })
        

        if response.json()['response']['count'] < offset:
            break

        time.sleep(0.5)

    all_comments = []

    for post in all_posts:

        offset = 0

        while True:

            response = requests.get('https://api.vk.com/method/wall.getComments',
                params={
                    'access_token':token,
                    'owner_id': post['owner_id'],
                    'count': count,
                    'offset': offset,
                    'post_id': post['id'],
                    'v': version,
                }
            )

            if response.json()['response']['count'] != 0:

                comments = response.json()['response']['items']

                for comment in comments:
                    all_comments.append({
                        'owner_id': post['owner_id'],
                        'post_id': post['id'],
                        'id': comment['id'],
                        'text': comment['text']
                    })
            
            time.sleep(0.5)

            print(response.json()['response'][ 'count'])

            offset += count

            if response.json()['response'][ 'count'] < offset:
                break

    os.mkdir(owner_id['Название города'])

    if len(all_posts) != 0:
        with open(owner_id['Название города'] + '/output_posts.txt', 'w', encoding='utf-8') as file:
            for post in all_posts:
                file.write(post['text'].replace('\n', ' ') + ' ')

    if len(all_comments) != 0:
        with open(owner_id['Название города'] + '/output_comments.txt', 'w', encoding='utf-8') as file:
            for comment in all_comments:
                file.write(comment['text'].replace('\n', '') + ' ')

        
    








