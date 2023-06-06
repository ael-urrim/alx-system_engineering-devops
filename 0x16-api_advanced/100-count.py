
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
#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests


def count_words(subreddit, word_list, instances={}, after="", count=0):
    """Prints counts of given words found in hot posts of a given subreddit.
    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        instances (obj): Key/value pairs of words/counts.
        after (str): The parameter for the next page of the API results.
        count (int): The parameter of results matched thus far.
    """
    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    try:
        results = response.json()
        if response.status_code == 404:
            raise Exception
    except Exception:
        print("")
        return

    results = results.get("data")
    after = results.get("after")
    count += results.get("dist")
    for c in results.get("children"):
        title = c.get("data").get("title").lower().split()
        for word in word_list:
            if word.lower() in title:
                times = len([t for t in title if t == word.lower()])
                if instances.get(word) is None:
                    instances[word] = times
                else:
                    instances[word] += times

    if after is None:
        if len(instances) == 0:
            print("")
            return
        instances = sorted(instances.items(), key=lambda kv: (-kv[1], kv[0]))
        [print("{}: {}".format(k, v)) for k, v in instances]
    else:
        count_words(subreddit, word_list, instances, after, count)
