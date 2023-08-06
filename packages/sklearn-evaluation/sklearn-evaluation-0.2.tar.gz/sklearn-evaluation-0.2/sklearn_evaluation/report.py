try:
    from cStringIO import StringIO  # py2
except ImportError:
    from io import StringIO  # py3


import base64
import os
import re
from datetime import datetime
from . import table

import matplotlib

try:
    import mistune
except:
    raise ImportError('You need to install mistune to use the report module')


def generate(evaluator, template, path=None, style='default'):
    # extra tags that can also be used in the report but are not evaluator
    # attributes

    date_utc = '{} UTC'.format(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    _extra_tags = {
        'date_utc':  date_utc,
        'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
    }

    # check if template is a path to a file
    # if yes, load the file
    if template.endswith('.md'):
        with open(template, 'r') as f:
            template = f.read()

    # strip lines in template
    lines = [l.strip() for l in template.splitlines()]
    template = reduce(lambda x, y: x+'\n'+y, lines)
    # get list of tags from template
    tags = parse_tags(template)

    # remove tags that are _extra_tags since they are not attributes
    # and the next function will fail
    tags = filter(lambda t: t not in _extra_tags.keys(), tags)

    # get attributes from evaluator using the tags
    attrs = getattr_from_list(evaluator, tags)

    # convert axes objects to HTML with base64,
    # Table to html
    for k, v in attrs.items():
        if isinstance(v, matplotlib.axes.Axes):
            attrs[k] = figure2html(v.get_figure())
        if isinstance(v, table.Table):
            attrs[k] = v.html

    # add key-value pairs to the attrs dict from the extra_tags
    attrs.update(_extra_tags)

    # replace tags with values
    report = template.format(**attrs)

    # compile to html and add style
    report = to_html(report, style)

    if path is not None:
        report_file = open(path, 'w')
        report_file.write(report)
        report_file.close()
    else:
        return report


def to_html(template, style_name):
    # Read md template and compile to html
    markdown = mistune.Markdown()
    html = markdown(template)

    # Add css
    pkg = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(pkg, 'styles', '{}.css'.format(style_name))
    f = open(filepath, 'r')
    css = f.read()
    html = '<style>'+css+'</style>'+html
    return html


def figure2html(fig):
    return base64_2_html(figure2base64(fig))


def base64_2_html(img):
    return '<img src="data:image/png;base64,'+img+'"></img>'


def figure2base64(fig):
    io = StringIO()
    fig.savefig(io, format='png')
    fig_base64 = base64.encodestring(io.getvalue())
    return fig_base64


def prettify_list(l):
    l = [str(idx+1)+'. '+str(el) for idx, el in enumerate(l)]
    return reduce(lambda x, y: x+'<br>'+y, l)


def prettify_dict(d):
    return prettify_list([key+': '+str(d[key]) for key in d.keys()])


def parse_tags(s):
    """
        Return a list of tags (e.g. {tag_a}, {tag_b}) found in string s
    """
    return re.findall('{(\w+)\}*', s)


def getattr_from_list(obj, attr_names):
    return {attr: getattr(obj, attr) for attr in attr_names}
