import requests
import json
import random
import datetime

# post words
words = 'make, with, from, up, about, into, over, after, the, and, that, it, not, he, you, this, but, his, they, ' \
        'her, she, or, an, will, their, them, there, then, some, so, see, said, should, could, would, can, cant, ' \
        'must, my, mine, me, more, may, be, by, been, being, do, does, did, done, doing, down, during, each, even, ' \
        'every, for, from, here, had, has, have, having, how, however, if, in, into, is, its, myself, not, no, now, ' \
        'of, on, once, only, other, our, ours, out, off, over, really, very, quite, rather, same, some, something, ' \
        'such, than, that, the, their, theirs, them, themselves, then, there, these, they, this, those, through, to, ' \
        'too, until, under, up, very, was, way, we, well, were, what, when, where, which, while, who, whom, whose, ' \
        'why, will, with, within, without, yet, you, your, yours, yourself, yourselves'


# Read configuration from file
with open('config.json', 'r') as f:
    config = json.load(f)


# Set up base URL and JWT token header
BASE_URL = 'http://localhost:8000/api/'
headers = {'Authorization': 'Bearer '}

posts_list = []

# User register
try:
    for i in range(config['number_of_users']):
        user_data = {
            'username': f'user{i}',
            'password': 'PASS12345678word',
            'email': f'user{i}@test.com'
        }
        response = requests.post(BASE_URL + 'register/', data=user_data)
        token = response.json()['access']
        headers['Authorization'] = f'Bearer {token}'

        # Create random number of posts
        num_posts = random.randint(1, config['max_posts_per_user'])
        for j in range(num_posts):
            random_words = random.sample(words.split(', '), k=5)
            post_data = {
                "title": f"User {i} post {j}",
                "text": f"...{' '.join(random_words)}..."
            }
            response = requests.post(BASE_URL + 'create_post/', data=post_data, headers=headers)
            print(response.text)
            post_id = response.json()['id']
            posts_list.append(post_id)
except Exception as e:
    print(e, 'Please delete all bot users to start again')

# User login
for i in range(config['number_of_users']):
    user_data = {
        'username': f'user{i}',
        'password': 'PASS12345678word',
    }
    response = requests.post(BASE_URL + 'login/', data=user_data)
    token = response.json()['access']
    headers['Authorization'] = f'Bearer {token}'

    # Randomly like posts
    num_likes = random.randint(1, config['max_likes_per_user'])
    for k in range(num_likes):
        post_id = random.choice(posts_list)
        response = requests.post(BASE_URL + f'like_post/{post_id}/', headers=headers)

# Get analytics
params = {
    'date_from': '2023-04-01',
    'date_to': '2023-04-31'
}
response = requests.get(BASE_URL + 'analytics/', params=params, headers=headers)
analytics = response.json()

summed_analytics = {}
for key, value in analytics['likes_by_date'].items():
    date = datetime.datetime.fromtimestamp(float(key))
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    if date_str in summed_analytics:
        summed_analytics[date_str] += value
    else:
        summed_analytics[date_str] = value

print('All likes:', summed_analytics)


