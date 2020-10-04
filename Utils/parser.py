import requests


def load(uri: str):
    try:
        req = requests.get(uri)
    except Exception:
        return

    if req.status_code != 200:
        return

    lines = req.text.split('\n')
    channels = []

    # Checking if it is m3u file
    if lines[0][:7] != '#EXTM3U':
        return None

    group_title = ""
    channel = {'title': "", 'uri': "", 'group_title': 0}
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

            # Current group
            if parts[0] == '#EXTGRP':
                group_title = parts[1].strip()
            # New channel
            elif parts[0] == '#EXTINF':
                params, channel['title'] = parts[1].split(',', 1)

                # Adding default group
                channel['group_title'] = group_title

                # Splitting params and removing length (-1)
                params = params.split(' ')[1:]
                filled = True

                for param in params:
                    param = param.split('=', 1)
                    if param[0] == 'group-title':
                        channel['group_title'] = param[1][1:-1]

        # URI of channel
        elif filled:
            channel['uri'] = line
            channels.append(channel)
            channel = {}
            filled = False

    return channels
