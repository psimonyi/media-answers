#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

media_types = [
    # Media Queries level 4 defined:
    'all', 'print', 'screen', 'speech',
    # MQ4 deprecated:
    'tty', 'tv', 'projection', 'handheld', 'braille', 'embossed', 'aural',
    # Not mentioned in MQ4:
    'tactile',
]

media_features = [
    # Media Queries level 4 defined:
    ('width', range(200, 4000), 'px'),
    ('height', range(200, 4000), 'px'),
    #'aspect-ratio'
    ('orientation', ['portrait', 'landscape']),
    ('resolution', range(80, 200), 'dpi'),
    ('resolution', range(1, 4,), 'dppx'),
    ('scan', ['interlace', 'progressive']),
    ('grid', [0, 1]),
    ('update-frequency', ['none', 'slow', 'normal']),
    ('overflow-block', ['none', 'scroll', 'optional-paged', 'paged']),
    ('overflow-inline', ['none', 'scroll']),
    ('color', range(0, 16)),
    ('color-index', range(0, 256)),
    ('monochrome', range(0, 16)),
    ('inverted-colors', ['none', 'inverted']),
    ('pointer', ['none', 'coarse', 'fine']),
    ('hover', ['none', 'on-demand', 'hover']),
    ('any-pointer', ['none', 'coarse', 'fine']),
    ('any-hover', ['none', 'on-demand', 'hover']),
    ('light-level', ['dim', 'normal', 'washed']),
    ('scripting', ['enabled', 'initial-only', 'none']),
    # MQ4 deprecated:
    ('device-width', range(200, 4000), 'px'),
    ('device-height', range(200, 4000), 'px'),
    #'device-aspect-ratio
]

def main():
    print('''<!doctype html>
<title>Media Query Answers</title>
<style>
p {{ display: none; }}
</style>
<meta name="viewport" content="initial-scale=1">

<h1>Media Query Answers</h1>

<h2>Media types</h2>
{types}

<h2>Media features</h2>
{features}
'''.format(types=types(),
           features='\n'.join(feature(*f) for f in media_features)))

def types():
    styles = []
    tests = []
    for type in media_types:
        styles.append('@media {type} {{ #{type} {{ display: block; }} }}'
                .format(type=type))
        tests.append('<p id="{type}">{type}</p>'
                .format(type=type))
    return '''
<style>
{styles}
</style>
{tests}'''.format(styles='\n'.join(styles), tests='\n'.join(tests))

def feature(name, values, unit=''):
    styles = []
    tests = []
    for value in values:
        styles.append(('@media ({name}: {value}{unit}) {{'
                '#{name}-{value}{unit} {{ display: block; }} }}').format(
                    name=name, value=value, unit=unit))
        tests.append('<p id="{name}-{value}{unit}">{value}{unit}</p>'.format(
                    name=name, value=value, unit=unit))
    return '''
<h3>{name}</h3>
<style>
{styles}
</style>
{tests}'''.format(name=name, styles='\n'.join(styles), tests='\n'.join(tests))

if __name__ == '__main__':
    main()
