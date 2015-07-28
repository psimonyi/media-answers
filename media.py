#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# From the Python itertools docs:
import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

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
    # It appears that, contrary to both MQ3 and MQ4, only integers are accepted
    # in front of dppx.
    ('resolution', ['1dppx', '2dppx']),
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

def feature(name, values, *args):
    if isinstance(values[0], str):
        format = format_discrete
    else:
        format = format_range
        values = pairwise(values)

    styles = []
    tests = []
    for value in values:
        cond, label = format(name, value, *args)
        id = css_id(name, label)

        styles.append(('@media {cond} {{ #{id} {{ display: block; }} }}')
                .format(cond=cond, id=id))
        tests.append('<p id="{id}">{label}</p>'
                .format(id=id, label=label))
    return '''
<h3>{name}</h3>
<style>
{styles}
</style>
{tests}'''.format(name=name, styles='\n'.join(styles), tests='\n'.join(tests))

def format_discrete(name, value):
    cond = '({name}: {value})'.format(name=name, value=value)
    label = value
    return cond, label

def format_range(name, value, unit=''):
    cond = ('(min-{name}: {min}{unit}) and (max-{name}: {max}{unit})'
            .format(name=name, min=value[0], max=value[1], unit=unit))
    label = ('{min}&ndash;{max}{unit}'
            .format(min=value[0], max=value[1], unit=unit))
    return cond, label

def css_id(name, label):
    return '{}--{}'.format(name, ''.join(x for x in label if x.isalnum()))

if __name__ == '__main__':
    main()
