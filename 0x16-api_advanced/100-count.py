
#!/usr/bin/python3
"""
A recursive function that queries the Reddit API and prints a sorted
count of give keyword
"""
import requests


def count_words(subreddit, word_list, hot_list=[], params={'limit': 100}):
    url = 'https://www.reddit.com/r/' + subreddit + '/hot.json'
    headers = {'User-Agent': '0x16-api_advanced:alx'}
    res = requests.get(url,
                       headers=headers, params=params, allow_redirects=False)
    if res.status_code == requests.codes.ok:
        data = res.json()['data']
        hot_posts = data['children']
        if len(hot_posts) > 0:
            hot_list += [item['data']['title'].lower() for item in hot_posts]
            if data['after'] is not None:
                params['after'] = data['after']
                return count_words(subreddit, word_list,
                                   hot_list=hot_list, params=params)
        words_count = {}
        for target_word in word_list:
            target_word = target_word.lower()
            if target_word not in words_count:
                words_count[target_word] = 0
            for title in hot_list:
                for word in title.split():
                    if word == target_word:
                        words_count[target_word] += 1
        for word in words_count.keys():
            print(word + ': ' + str(words_count[word]))
    return None
