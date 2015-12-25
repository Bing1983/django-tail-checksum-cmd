# -*- coding:utf-8 -*-
"""
## How it works

1. Find templates which bear a middle name 'raw',  i.e. [file name].raw.html
2. Search tokens in these templates, a token should look like ${'base/main.js'}
3. Find corresponding files referred by these tokens and calculating their checksums
3. Replace tokens with checksum-tailed URLs
4. For each raw template [file name].raw.html, create a new template named [file name].html to save the changes.
"""


import os
import re
import hashlib

from django.conf import settings
from django.core.management.base import BaseCommand


class HashParser(object):

    __STATIC_DIR__ = os.path.join(settings.BASE_DIR, 'static')

    def calculate_hash(self, res):
        f = open(os.path.join(self.__STATIC_DIR__, res.strip()), 'r')
        hash = hashlib.md5(f.read()).hexdigest()
        f.close()
        return hash

    def parse(self, text):
        res_list = re.findall(r'\$\{([\s\S][^\}]*)\}', text)
        for res in res_list:
            hash_tailed_url = '%s?%s' % (res, self.calculate_hash(res))
            token = '${%s}' % res
            text = text.replace(token, hash_tailed_url)
            print(u'> %s' % hash_tailed_url)
        return text


class Command(BaseCommand):

    help = ("It appends checksums to URLs of static resources in html templates. "
            "It will search templates in all installed apps "
            "(app name starts with django are excluded.) by default, "
            "use --app to specify apps in which you want to search raw templates.")

    def add_arguments(self, parser):
        parser.add_argument('--app', nargs="+", type=str, default='')

    def get_target_apps(self, options):
        if isinstance(options['app'], list):
            apps = options['app']
        else:
            # app name starts with django are excluded
            apps = [i for i in settings.INSTALLED_APPS if not i.startswith('django')]
        return apps

    def find_raw_files(self, apps):
        raw_files = []
        for app in apps:
            path = os.path.join(settings.BASE_DIR, app, u'templates')
            if os.path.isdir(path):
                raw_files.extend(self.walk_through_files(path))
        return raw_files

    def walk_through_files(self, path):
        raw_files = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.raw.html'):
                    raw_files.append(os.path.join(root, file))
        return raw_files

    def compile(self, raw_file):
        fi = open(raw_file, 'r')
        text = HashParser().parse(fi.read())
        fo = open(raw_file.replace(u'.raw.', u'.'), 'w')
        fo.write(text)
        fi.close()
        fo.close()

    def handle(self, *args, **options):
        apps = self.get_target_apps(options)
        raw_files = self.find_raw_files(apps)
        did = False
        for raw_file in raw_files:
            print(u'Compiling %s' % raw_file)
            self.compile(raw_file)
            did = True
        if did:
            print(u'Well done, all files are compiled.')
        else:
            print(u'Find no raw templates.')
