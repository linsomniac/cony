# -*- coding: utf-8 -*-
import os.path
import urllib
from bottle import redirect

def cmd_tr(term):
    """Translates the text using Google Translate."""
    if len(term.decode('utf-8')) < len(term):
        direction = 'ru|en'
    else:
        direction = 'en|ru'
    redirect('http://translate.google.com/#%s|%s' % (direction, term))

def cmd_save_word(term):
    """Saves word and it's translation into the ~/.words

    This file could be used to import words into
    the FlashCards ToGo.
    """

    template = """
    <p>Translation "{{ word }}" was saved to ~/.words</p>
    %rebase layout title='Translation saved'
    """

    with open(os.path.expanduser('~/.words'), 'a+') as f:
        f.write(term)
        f.write('\n')
    return dict(template=template, word=term)

def cmd_wo(term):
    """Searches word translations at the http://slovari.yandex.ru.

    This command requires `simplejson` module to be installed.
    """
    import simplejson
    variants = []

    template = """
    <ul>
        %for v in variants:
            <li><a href="/?s=save_word+{{ v['en'].replace(' ', '+') }}%3B+{{ v['ru'].replace(' ', '+').replace(',', '%2C') }}">{{ v['en'] }}</a> — {{ v['ru'] }}</li>
        %end
    </ul>
    %rebase layout title='Word translation'
    """


    for i in reversed(range((len(term) + 1) / 2, len(term) + 1)):
        url = 'http://suggest-slovari.yandex.ru/suggest-lingvo?v=2&lang=en&part=%s' % term[:i]
        data = urllib.urlopen(url).read()
        data = simplejson.loads(data)
        if data[0]:
            for trans, link in zip(*data[1:]):
                en, ru = trans.split(' - ', 1)
                variants.append(dict(en=en, ru=ru, link=link))
            if len(variants) > 5:
                break

    return dict(template=template, variants=variants)
