#!/usr/bin/python3
# -*- coding:utf-8 -*
#
# Copyright (C) 2017 Antoine Tenart <antoine.tenart@free-electrons.com>
#
# This file is licensed under the terms of the GNU General Public
# License version 2. This program is licensed "as is" without any
# warranty of any kind, whether express or implied.

from datetime import datetime, timedelta, timezone
import dateutil.parser
from jinja2 import Template

class Render:
    __tpl = '''<html>
<head>
    <title>{{title}}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <style>
html { margin: auto; width: 85%; }
    </style>
</head>
<body>
    <h1><small>{{title}}</small></h1>
{{content}}
</body>
</html>'''

    def __init__(self, c, s):
        self.__cfg = c
        self.__store = s

    def summary(self):
        table = ''
        t = datetime.now(timezone.utc) - timedelta(days=1)
        failed = list(filter(lambda x: dateutil.parser.parse(x['published']) > t,
                             self.__store.get_status('FAIL')))
        for t in failed:
            tree = "%s/%s" % (t['tree'], t['branch'])
            log = 'https://storage.kernelci.org/%s/%s/%s/%s/%s/lab-%s/boot-%s.html'\
                  % (t['tree'], t['branch'], t['version'], t['arch'],
                     t['config'], t['lab'], t['kci_board'])
            table += '''<tr>
<td>%s</td><td>%s</td><td>%s</td><td>%s</td>
<td><a href="%s">Boot</a></td><td><a style="color:red;" href="%s">%s</a></td>
</tr>''' % (t['board'], tree, t['version'], t['config'], log, t['link'],
            t['status'])

        content = '''<table class="table table-condensed table-hover">
<thead>
<tr><th>Baord</th><th>Tree</th><th>Version</th><th>Config</th>
<th>Boot log</th><th>Status</th></tr>
</thead>
<tbody>%s</tbody>
</table>''' % table
        with open('summary.html', 'w') as f:
            f.write(Template(self.__tpl).render(title='KCI summary',
                    content=content))
