from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    compat_urllib_parse,
)


class XBefIE(InfoExtractor):
    _VALID_URL = r'http://(?:www\.)?xbef\.com/video/(?P<id>[0-9]+)'
    _TEST = {
        'url': 'http://xbef.com/video/5119-glamourous-lesbians-smoking-drinking-and-fucking',
        'md5': 'a478b565baff61634a98f5e5338be995',
        'info_dict': {
            'id': '5119',
            'ext': 'mp4',
            'title': 'md5:7358a9faef8b7b57acda7c04816f170e',
            'age_limit': 18,
            'thumbnail': 're:^http://.*\.jpg',
        }
    }

    def _real_extract(self, url):
        m = re.match(self._VALID_URL, url)
        video_id = m.group('id')

        webpage = self._download_webpage(url, video_id)
        title = self._html_search_regex(
            r'<h1[^>]*>(.*?)</h1>', webpage, 'title')

        config_url_enc = self._download_webpage(
            'http://xbef.com/Main/GetVideoURLEncoded/%s' % video_id, video_id,
            note='Retrieving config URL')
        config_url = compat_urllib_parse.unquote(config_url_enc)
        config = self._download_xml(
            config_url, video_id, note='Retrieving config')

        video_url = config.find('./file').text
        thumbnail = config.find('./image').text

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'thumbnail': thumbnail,
            'age_limit': 18,
        }
