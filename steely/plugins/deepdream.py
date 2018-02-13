'''
http://i0.kym-cdn.com/photos/images/original/001/042/049/5ef.jpg
'''
import requests
from steely import config

__author__ = 'CianLR'
COMMAND = '..'
API_URL = "https://api.deepai.org/api/deepdream"

def get_dream(url):
    return requests.post(
        API_URL,
        data = {'content': url},
        headers = {'api-key': config.DEEP_API_KEY},
    ).json()

def grab_image(message):
    for a in message.attachments:
        # TODO: Something less stupid than below
        if a.__class__.__name__ == 'ImageAttachment':
            return a
    return None

def dream(bot, message, image_send, text_send):
    image = grab_image(message)
    if image is None:
        return text_send("Last message doesn't contain an image")
    image_url = bot.fetchImageUrl(image.uid)
    dream = get_dream(image_url)
    if 'output_url' not in dream:
        return text_send("Some API error occured: {}".format(str(dream)))
    return image_send(dream['output_url'])


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    image_send = lambda url: bot.sendRemoteImage(url,
                                                 thread_id=thread_id,
                                                 thread_type=thread_type)
    text_send = lambda text: bot.sendMessage(text,
                                             thread_id=thread_id,
                                             thread_type=thread_type)
    dream(bot, message, image_send, text_send)


if __name__ == '__main__':
    harold = ('https://static.independent.co.uk/'
              's3fs-public/thumbnails/image/2017/07/11/11/harold-0.jpg')
    print(get_dream(harold))
