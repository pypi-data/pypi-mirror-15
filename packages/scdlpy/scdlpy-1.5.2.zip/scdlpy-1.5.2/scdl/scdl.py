#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""scdl allow you to download music from soundcloud

Usage:
    scdl -l <track_url> [-a | -f | -t | -p][-c][-o <offset>]\
[--hidewarnings][--debug | --error][--path <path>][--addtofile][--onlymp3]
[--hide-progress]
    scdl me (-s | -a | -f | -t | -p)[-c][-o <offset>]\
[--hidewarnings][--debug | --error][--path <path>][--addtofile][--onlymp3]
[--hide-progress]
    scdl -h | --help
    scdl --version


Options:
    -h --help          Show this screen
    --version          Show version
    me                 Use the user profile from the auth_token
    -l [url]           URL can be track/playlist/user
    -s                 Download the stream of a user (token needed)
    -a                 Download all tracks of a user (including repost)
    -t                 Download all uploads of a user
    -f                 Download all favorites of a user
    -p                 Download all playlists of a user
    -c                 Continue if a music already exist
    -o [offset]        Begin with a custom offset
    --path [path]      Use a custom path for this time
    --hidewarnings     Hide Warnings. (use with precaution)
    --addtofile        Add the artist name to the filename if it isn't in the filename already
    --onlymp3          Download only the mp3 file even if the track is Downloadable
    --error            Only print debug information (Error/Warning)
    --debug            Print every information and
    --hide-progress    Hide the wget progress bar
"""

import logging
import os
import signal
import sys
import time
import warnings
import math
import shutil
import requests
import re
import tempfile

import configparser
import mutagen
from docopt import docopt
from clint.textui import progress

from scdl import __version__
from scdl import client, utils

logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger('requests').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addFilter(utils.ColorizeFilter())
logger.newline = print

arguments = None
token = ''
path = ''
offset = 0
scdl_client_id = '95a4c0ef214f2a4a0852142807b54b35'
alternative_client_id = 'a3e059563d7fd3372b49b37f00a00bcf'

url = {
    'favorites': ('https://api.soundcloud.com/users/{0}/favorites?'
                  'limit=200&offset={1}'),
    'tracks': ('https://api.soundcloud.com/users/{0}/tracks?'
               'limit=200&offset={1}'),
    'all': ('https://api-v2.soundcloud.com/profile/soundcloud:users:{0}?'
            'limit=200&offset={1}'),
    'playlists': ('https://api.soundcloud.com/users/{0}/playlists?'
                  'limit=200&offset={1}'),
    'resolve': ('https://api.soundcloud.com/resolve?url={0}'),
    'user': ('https://api.soundcloud.com/users/{0}'),
    'me': ('https://api.soundcloud.com/me?oauth_token={0}')
}

client = client.Client()


def main():
    """
    Main function, call parse_url
    """
    signal.signal(signal.SIGINT, signal_handler)
    global offset
    global arguments

    # import conf file
    get_config()

    # Parse argument
    arguments = docopt(__doc__, version=__version__)

    if arguments['--debug']:
        logger.level = logging.DEBUG
    elif arguments['--error']:
        logger.level = logging.ERROR

    logger.info('Soundcloud Downloader by DarkArtek')
    logger.debug(arguments)

    if arguments['-o'] is not None:
        try:
            offset = int(arguments['-o']) - 1
        except:
            logger.error('Offset should be an integer...')
            sys.exit()
        logger.debug('offset: %d', offset)

    if arguments['--hidewarnings']:
        warnings.filterwarnings('ignore')

    if arguments['--path'] is not None:
        if os.path.exists(arguments['--path']):
            os.chdir(arguments['--path'])
        else:
            logger.error('Invalid path in arguments...')
            sys.exit()
    logger.debug('Downloading to '+os.getcwd()+'...')

    logger.newline()
    if arguments['-l']:
        parse_url(arguments['-l'])
    elif arguments['me']:
        if arguments['-f']:
            download(who_am_i(), 'favorites', 'likes')
        elif arguments['-t']:
            download(who_am_i(), 'tracks', 'uploaded tracks')
        elif arguments['-a']:
            download(who_am_i(), 'all', 'tracks and reposts')
        elif arguments['-p']:
            download(who_am_i(), 'playlists', 'playlists')


def get_config():
    """
    read the path where to store music
    """
    global token
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.config/scdl/scdl.cfg'))
    try:
        token = config['scdl']['auth_token']
        path = config['scdl']['path']
    except:
        logger.error('Are you sure scdl.cfg is in $HOME/.config/scdl/ ?')
        sys.exit()
    if os.path.exists(path):
        os.chdir(path)
    else:
        logger.error('Invalid path in scdl.cfg...')
        sys.exit()


def get_item(track_url, client_id=scdl_client_id):
    """
    Fetches metadata for an track or playlist
    """
    try:
        item_url = url['resolve'].format(track_url)
        item_url = '{0}&client_id={1}'.format(item_url, client_id)
        logger.debug(item_url)

        r = requests.get(item_url)
        if r.status_code == 403:
            return get_item(track_url, alternative_client_id)

        item = r.json()
        no_tracks = item['kind'] == 'playlist' and not item['tracks']
        if no_tracks and client_id != alternative_client_id:
            return get_item(track_url, alternative_client_id)
    except Exception:
        if client_id == alternative_client_id:
            logger.error('Get item failed...')
            return
        logger.error('Error resolving url, retrying...')
        time.sleep(5)
        try:
            return get_item(track_url, alternative_client_id)
        except Exception as e:
            logger.error('Could not resolve url {0}'.format(track_url))
            logger.exception(e)
            sys.exit(0)
    return item


def parse_url(track_url):
    """
    Detects if the URL is a track or playlists, and parses the track(s)
    to the track downloader
    """
    global arguments
    item = get_item(track_url)
    logger.debug(item)
    if not item:
        return
    elif item['kind'] == 'track':
        logger.info('Found a track')
        download_track(item)
    elif item['kind'] == 'playlist':
        logger.info('Found a playlist')
        download_playlist(item)
    elif item['kind'] == 'user':
        logger.info('Found a user profile')
        if arguments['-f']:
            download(item, 'favorites', 'likes')
        elif arguments['-t']:
            download(item, 'tracks', 'uploaded tracks')
        elif arguments['-a']:
            download(item, 'all', 'tracks and reposts')
        elif arguments['-p']:
            download(item, 'playlists', 'playlists')
        else:
            logger.error('Please provide a download type...')
    else:
        logger.error('Unknown item type')


def who_am_i():
    """
    display to who the current token correspond, check if the token is valid
    """
    me = url['me'].format(token)
    me = '{0}&client_id={1}'.format(me, scdl_client_id)
    r = requests.get(me)
    current_user = r.json()
    logger.debug(me)

    if r.status_code == 401:
        logger.error('Invalid token...')
        sys.exit(0)
    logger.info('Hello {0}!'.format(current_user['username']))
    logger.newline()
    return current_user


def download(user, dl_type, name):
    """
    Download all items of a user
    """
    username = user['username']
    user_id = user['id']
    logger.info(
        'Retrieving all the {0} of user {1}...'.format(name, username)
    )
    dl_url = url[dl_type].format(user_id, offset)
    resources = client.get_collection(dl_url)
    total = len(resources)
    logger.info('Retrieved {0} {1}'.format(total, name))
    for counter, item in enumerate(resources, 1):
        try:
            logger.debug(item)
            logger.info('{0} n°{1} of {2}'.format(
                name.capitalize(), counter + offset, total)
            )
            if name == 'tracks and reposts':
                item_name = ''
                if item['type'] == 'track-repost':
                    item_name = 'track'
                else:
                    item_name = item['type']
                uri = item[item_name]['uri']
                parse_url(uri)
            elif name == 'playlists':
                download_playlist(item)
            else:
                download_track(item)
        except Exception as e:
            logger.exception(e)
    logger.info('Downloaded all {0} {1} of user {2}!'.format(
        total, name, username)
    )


def download_playlist(playlist):
    """
    Download a playlist
    """
    global offset
    invalid_chars = '\/:*?|<>"'
    playlist_name = playlist['title'].encode('utf-8', 'ignore')
    playlist_name = playlist_name.decode(sys.stdout.encoding)
    playlist_name = ''.join(c for c in playlist_name if c not in invalid_chars)

    if not os.path.exists(playlist_name):
        os.makedirs(playlist_name)
    os.chdir(playlist_name)

    with open(playlist_name + '.m3u', 'w+') as playlist_file:
        playlist_file.write('#EXTM3U' + os.linesep)
        for counter, track_raw in enumerate(playlist['tracks'], 1):
            if offset > 0:
                offset -= 1
                continue
            logger.debug(track_raw)
            logger.info('Track n°{0}'.format(counter))
            download_track(track_raw, playlist['title'], playlist_file)
    os.chdir('..')


def download_my_stream():
    """
    DONT WORK FOR NOW
    Download the stream of the current user
    """
    # TODO
    # Use Token


def download_all_of_a_page(tracks):
    """
    NOT RECOMMENDED
    Download all song of a page
    """
    logger.error(
        'NOTE: This will only download the songs of the page.(49 max)'
    )
    logger.error('I recommend you to provide a user link and a download type.')
    for counter, track in enumerate(tracks, 1):
        logger.newline()
        logger.info('Track n°{0}'.format(counter))
        download_track(track)


def download_track(track, playlist_name=None, playlist_file=None):
    """
    Downloads a track
    """
    global arguments

    title = track['title']
    title = title.encode('utf-8', 'ignore').decode(sys.stdout.encoding)
    if track['streamable']:
        url = '{0}?client_id={1}'.format(track['stream_url'], scdl_client_id)
    else:
        logger.error('{0} is not streamable...'.format(title))
        logger.newline()
        return
    logger.info('Downloading {0}'.format(title))

    # filename
    if track['downloadable'] and not arguments['--onlymp3']:
        logger.info('Downloading the original file.')
        download_url = track['download_url']
        url = '{0}?client_id={1}'.format(download_url, scdl_client_id)
        r = requests.get(url, stream=True)
        d = r.headers['content-disposition']
        filename = re.findall("filename=(.+)", d)[0][1:-1]
    else:
        invalid_chars = '\/:*?|<>"'
        username = track['user']['username']
        if username not in title and arguments['--addtofile']:
            title = '{0} - {1}'.format(username, title)
        title = ''.join(c for c in title if c not in invalid_chars)
        filename = title + '.mp3'

    logger.debug("filename : {0}".format(filename))
    # Add the track to the generated m3u playlist file
    if playlist_file:
        duration = math.floor(track['duration'] / 1000)
        playlist_file.write(
            '#EXTINF:{0},{1}{3}{2}{3}'.format(
                duration, title, filename, os.linesep
            )
        )

    # Download
    if not os.path.isfile(filename):
        logger.debug(url)
        r = requests.get(url, stream=True)
        if r.status_code == 401:
            url = url[:-32] + alternative_client_id
            logger.debug(url)
            r = requests.get(url, stream=True)
        temp = tempfile.NamedTemporaryFile(delete=False)
        with temp as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(
                r.iter_content(chunk_size=1024),
                expected_size=(total_length/1024) + 1,
                hide=True if arguments["--hide-progress"] else False
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()
        shutil.move(temp.name, os.path.join(os.getcwd(), filename))
        if '.mp3' in filename:
            try:
                settags(track, filename, playlist_name)
            except Exception as e:
                logger.error('Error trying to set the tags...')
                logger.debug(e)
        else:
            logger.error("This type of audio doesn't support tagging...")
    else:
        if arguments['-c']:
            logger.info('{0} already Downloaded'.format(title))
            logger.newline()
            return
        else:
            logger.newline()
            logger.error('Music already exists ! (exiting)')
            sys.exit(0)

    logger.newline()
    logger.info('{0} Downloaded.'.format(filename))
    logger.newline()


def settags(track, filename, album=None):
    """
    Set the tags to the mp3
    """
    logger.info('Settings tags...')
    artwork_url = track['artwork_url']
    user = track['user']
    if not artwork_url:
        artwork_url = user['avatar_url']
    artwork_url = artwork_url.replace('large', 't500x500')
    response = requests.get(artwork_url, stream=True)
    with tempfile.NamedTemporaryFile() as out_file:
        shutil.copyfileobj(response.raw, out_file)
        out_file.seek(0)

        audio = mutagen.File(filename)
        audio['TIT2'] = mutagen.id3.TIT2(encoding=3, text=track['title'])
        audio['TPE1'] = mutagen.id3.TPE1(encoding=3, text=user['username'])
        audio['TCON'] = mutagen.id3.TCON(encoding=3, text=track['genre'])
        if album:
            audio['TALB'] = mutagen.id3.TALB(encoding=3, text=album)
        if artwork_url:
            audio['APIC'] = mutagen.id3.APIC(
                encoding=3, mime='image/jpeg', type=3, desc='Cover',
                data=out_file.read()
                )
        else:
            logger.error('Artwork can not be set.')
    audio.save()


def signal_handler(signal, frame):
    """
    Handle Keyboardinterrupt
    """
    logger.newline()
    logger.info('Good bye!')
    sys.exit(0)

if __name__ == '__main__':
    main()
