#!/usr/bin/env python

from xml.dom.minidom import parseString

from lulu.common import (
    match1,
    print_info,
    get_content,
    download_rtmp_url,
    playlist_not_supported,
)
from lulu.util.strings import unescape_html


__all__ = ['mtv81_download']
site_info = 'MTV 81 mtv81.com'


def mtv81_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)
    title = unescape_html(
        '|'.join(match1(html, r'<title>(.*?)</title>').split('|')[:-2])
    )

    # mgid%3Auma%3Avideo%3Amtv81.com%3A897974
    vid = match1(html, r'getTheVideo\("(.*?)"')
    xml = parseString(get_content(
        'http://intl.esperanto.mtvi.com/www/xml/media/mediaGen.jhtml?uri={}&'
        'flashPlayer=LNX%2013,0,0,206&geo=CN&sid=123456'.format(vid)
    ))

    url = sorted(
        map(lambda x: x.firstChild.nodeValue, xml.getElementsByTagName("src")),
        key=lambda x: int(match1(x, r'_(\d+?)_'))
    )[-1]

    mediatype, ext, size = 'mp4', 'mp4', 0
    print_info(site_info, title, mediatype, size)
    # rtmpdump  -r 'rtmpe://cp30865.edgefcs.net/ondemand/mtviestor/_!/intlod/MTVInternational/MBUS/GeoLocals/00JP/VIAMTVI/PYC/201304/7122HVAQ4/00JPVIAMTVIPYC7122HVAQ4_640x_360_1200_m30.mp4' -o "title.mp4" --swfVfy http://media.mtvnservices.com/player/prime/mediaplayerprime.1.10.8.swf  # noqa

    # because rtmpdump is unstable,may try serveral times
    if not info_only:
        download_rtmp_url(
            url=url, title=title, ext=ext, params={
                '--swfVfy': (
                    'http://media.mtvnservices.com/player/prime/mediaplayer'
                    'prime.1.10.8.swf'
                )
            }, output_dir=output_dir
        )


download = mtv81_download
download_playlist = playlist_not_supported(site_info)
