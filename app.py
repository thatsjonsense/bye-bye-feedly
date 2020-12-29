# -*- coding: utf-8 -*-

import io
import json
import requests
import time


# Add your feedly API credentials
user_id = ''
access_token = ''


def get_saved_items(user_id, access_token, continuation = None):
    headers = {'Authorization' : 'OAuth ' + access_token}
    url = 'https://cloud.feedly.com/v3/streams/contents?streamId=user/' + user_id + '/tag/global.saved&count=10000'
    if continuation:
      url += '&continuation=' + continuation

    print('Requesting saved items')
    r = requests.get(url, headers = headers)

    if r.status_code == 200:
      r.encoding = 'UTF-8'
      items = r.json()['items']
      print(len(items))
      if (r.json().get('continuation')):
        print(r.json()['continuation'])
        return items + get_saved_items(user_id, access_token, r.json()['continuation'])
      else:
        return items

    else:
        print('Error: Saved items couldn’t be fetched')
        print('Status code: ' + str(r.status_code))
        print(r.json())
        exit(1)

filename = 'feedly-saved-' + time.strftime("%Y%m%d-%H%M%S") + '.json'
items = get_saved_items(user_id, access_token)
with io.open(filename, 'a', encoding='UTF-8') as output_file:
  try:
    print(len(items), 'total items')
    json.dump(items, output_file, separators=(',',':'), indent=2)
    print('Success: Created ' + filename)
  except ValueError as error:
    print(error)