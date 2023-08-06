#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..extractor import VideoExtractor
from ..util.html import get_content, add_header
from ..util.match import match1
from ..util import log

import json

class YinYueTai(VideoExtractor):
    name = u'YinYueTai (音乐台)'
    supported_stream_types = ['sh', 'he', 'hd', 'hc' ]
    def prepare(self):

        if not self.vid:
            self.vid = match1(self.url, 'http://\w+.yinyuetai.com/video/(\d+)')

        data = json.loads(get_content('http://ext.yinyuetai.com/main/get-h-mv-info?json=true&videoId={}'.format(self.vid)))

        if data['error']:
            log.e('some error happens')

        video_data = data['videoInfo']['coreVideoInfo']

        self.title = video_data['videoName']

        for s in video_data['videoUrlModels']:
            self.stream_types.append(s['qualityLevel'])
            self.streams[s['qualityLevel']] = {'container': 'flv', 'video_profile': s['qualityLevelName'], 'src' : [s['videoUrl']], 'size': s['fileSize']}

        self.stream_types = sorted(self.stream_types, key = self.supported_stream_types.index)

    def download_playlist(self, url, param):

        playlist_id = match1(url, 'http://\w+.yinyuetai.com/playlist/(\d+)')

        playlist_data = json.loads(get_content('http://m.yinyuetai.com/mv/get-simple-playlist-info?playlistId={}'.format(playlist_id)))

        videos = playlist_data['playlistInfo']['videos']
        # TODO
        # I should directly use playlist data instead to request by vid... to be update
        for v in videos:
            vid = v['playListDetail']['videoId']
            self.download(vid, param)

site = YinYueTai()
