#!/usr/bin/env python3

print('''<!doctype html>
<style>
p {
    margin: 0;
}
p:first-child::after, p:last-child::after {
    /* We can't know whether this is the true value because we didn't test both
     * sides.  The true value is probably outside the range. */
    text-decoration: line-through;
    color: red;
}
div {
    height: 1.25em;
    overflow: hidden;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}
</style>

<meta name="viewport" content="initial-scale=1">
<h1>Media types</h1>''')

media_types = ('all', 'aural', 'braille', 'handheld', 'print', 'projection',
    'screen', 'tty', 'tv', 'embossed', 'tactile')
print('<style>')
for type in media_types:
    print('@media {0} {{ #{0}::after {{ content: "{0}"; }} }}'.format(type))
print('</style>')
for type in media_types:
    print('<p id="{0}">'.format(type))

print('<h1>Media features</h1>')
def show_feature(feature, range, unit):
    print('<h2>{feature}</h2>'.format(feature=feature))
    queries = ['min-{feature}:{number}{unit}'.format(
        feature=feature, number=number, unit=unit) for number in range]
    queries = [(q, q.replace(':', '-')) for q in queries]
    print('<style>')
    for q in queries:
        print('''@media ({0}) {{
    #{1}::after {{
        height: 1.25em;
        content: "{0}";
    }}
}}'''.format(*q))
    print('</style>')
    print('<div>')
    for q in reversed(queries):
        print('<p id="{1}">'.format(*q))
    print('<p>????</p>')
    print('</div>')

show_feature('resolution', range(80, 200), 'dpi')
show_feature('width', range(200, 4000), 'px')
show_feature('height', range(200, 4000), 'px')
show_feature('device-width', range(100, 2000), 'px')
show_feature('device-height', range(200, 2000), 'px')
show_feature('color', range(1, 16), '')
show_feature('color-index', range(1, 16), '')

