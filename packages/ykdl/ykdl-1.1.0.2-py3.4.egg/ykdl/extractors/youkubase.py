#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..extractor import VideoExtractor
from .youkujs import *
from ..util.html import get_content

from ykdl.compact import urlencode

import json
from random import randint

class YoukuBase(VideoExtractor):

    def get_custom_sign(self):
        custom_api = 'https://api.youku.com/players/custom.json?client_id={}&video_id={}&vext=null&embsig=undefined&styleid=undefined'.format(self.client_id, self.vid)
        html = get_content(custom_api)
        data = json.loads(html)
        self.playsign = data['playsign']

    def get_custom_stream(self):
        custom_api = 'http://play.youku.com/partner/get.json?vid={}&ct={}&sign={}&ran={}'.format(self.vid, self.ct, self.playsign, randint(1,9999))
        html = get_content(custom_api)
        data = json.loads(html)['data']
        self.stream_data = data['stream']
        self.ep = data['security']['encrypt_string']
        self.ip = data['security']['ip']

    def prepare(self):

        self.setup()
        self.streams_parameter = {}
        for stream in self.stream_data:
            stream_id = stream['stream_type']
            if not stream_id in self.stream_types:
                self.streams_parameter[stream_id] = {
                    'fileid': stream['stream_fileid'],
                    'segs': stream['segs']
                }
                self.streams[stream_id] = {
                    'container': stream_type_to_container[stream_code_to_type[stream_id]],
                    'video_profile': stream_code_to_profiles[stream_id],
                    'size': stream['size']
                }
                self.stream_types.append(stream_id)

        self.stream_types = sorted(self.stream_types, key = supported_stream_code.index)

    def extract(self):
        if not self.param.info:
            stream_id = self.param.format or self.stream_types[0]
            self. extract_single(stream_id)
        else:
            for stream_id in self.stream_types:
                self. extract_single(stream_id)

    def extract_single(self, stream_id):
        sid, token = init(self.ep)
        segs = self.streams_parameter[stream_id]['segs']
        streamfileid = self.streams_parameter[stream_id]['fileid']
        urls = []
        no = 0
        for seg in segs:
            k = seg['key']
            assert k != -1
            fileId = getFileid(streamfileid, no)
            ep  = create_ep(sid, fileId, token)
            q = urlencode(dict(
                ctype = self.ct,
                ev    = 1,
                K     = k,
                ep    = ep,
                oip   = str(self.ip),
                token = token,
                yxon  = 1,
                myp   = 0,
                ymovie= 1,
                ts    = seg['total_milliseconds_audio'][:-3],
                hd    = stream_type_to_hd[stream_code_to_type[stream_id]],
                special = 'true',
                yyp   = 2
            ))
            nu = '%02x' % no
            u = 'http://k.youku.com/player/getFlvPath/sid/{sid}_{nu}' \
                '/st/{container}/fileid/{fileid}?{q}'.format(
                sid       = sid,
                nu        = nu,
                container = self.streams[stream_id]['container'],
                fileid    = fileId,
                q         = q
            )
            no += 1
            url = json.loads(get_content(u))[0]['server']
            urls.append(url)

        self.streams[stream_id]['src'] = urls
        if not self.streams[stream_id]['src'] and self.password_protected:
            log.e('[Failed] Wrong password.')

