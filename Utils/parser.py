import requests
import shlex

EMPTY_CHANNEL = {'title': "", 'uri': "", 'group_title': ""}


def load(uri: str):
    try:
        req = requests.get(uri, timeout=5)
    except Exception:
        return None

    if req.status_code // 100 != 2:
        return None

    lines = req.text.split('\n')
    channels = []

    # Checking if it is m3u file
    if len(lines) < 1 or len(lines[0]) < 7 or lines[0][:7] != '#EXTM3U':
        return None

    channel = {**EMPTY_CHANNEL}
    filled = False

    for line in lines:
        # Empty line
        if len(line) == 0:
            continue

        # Removing \r
        if line[-1:] == '\r':
            line = line[:-1]

        # M3U8 tag
        if line[0] == '#':
            parts = line.split(':', 1)
            if len(parts) < 2 or ' ' in parts[0]:
                continue

            # Channel group
            if parts[0] == '#EXTGRP':
                channel['group_title'] = parts[1].strip()

            # New channel
            elif parts[0] == '#EXTINF':
                params, channel['title'] = parts[1].split(',', 1)
                channel['title'] = channel['title'].strip()
                if channel['title'][0] == '#':
                    channel = {**EMPTY_CHANNEL}
                    continue
                filled = True

                # Splitting params and removing length (-1)
                params = shlex.split(params)[1:]

                for param in params:
                    param = param.split('=', 1)
                    if param[0] == 'group-title':
                        channel['group_title'] = param[1]

        # URI of channel
        elif filled:
            channel['uri'] = line
            channels.append(channel)

            channel = {**EMPTY_CHANNEL}
            filled = False

    return channels


def get_chunks(raw_m3u8: str):
    chunks = []
    lines = raw_m3u8.replace('\r', '').split('\n')

    if len(lines) == 0 or lines[0] != '#EXTM3U':
        return []

    for line in lines:
        if len(line) > 1:
            if line[0] != '#':
                chunks.append(line)
    return chunks
