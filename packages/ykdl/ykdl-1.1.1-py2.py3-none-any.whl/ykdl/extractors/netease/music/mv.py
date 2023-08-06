#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from ykdl.util.html import get_content, add_header
from ykdl.extractor import VideoExtractor
from ykdl.util.match import match1

class NeteaseMv(VideoExtractor):
    name = u'Netease Mv (网易音乐Mv)'

    supported_stream_code = ['1080', '720', '480', '240']
    code_2_profile = {'1080': 'BD', '720': 'TD', '480':'HD', '240':'SD'}
    def prepare(self):
        add_header("Referer", "http://music.163.com/")
        if not self.vid:
            self.vid =  match1(self.url, 'id=(.*)')

        api_url = "http://music.163.com/api/mv/detail/?id={}&ids=[{}]&csrf_token=".format(self.vid, self.vid)
        mv = json.loads(get_content(api_url))['data']
        self.title = mv['name']
        self.artist = mv['artistName']
        for code in self.supported_stream_code:
            if code in mv['brs']:
                stream_id = self.code_2_profile[code]
                self.stream_types.append(stream_id)
                self.streams[stream_id] = {'container': 'mp4', 'video_profile': stream_id, 'src' : [mv['brs'][code]], 'size': 0}
site = NeteaseMv()
