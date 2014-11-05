#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import yaml
import csv
import re

import codecs
import locale
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = 'templates'

def createUniqueName(title):
  text = title.lower()
  text = re.sub(r'\s+', '-', text)
  return re.sub(r'[^a-zA-Z\\-]','', text)

def Main():
  env = Environment(loader=FileSystemLoader(TEMPLATES_DIR),
      extensions=['jinja2.ext.with_'])


  for page in ['about', 'offerings', 'index', 'resources']:
    template = env.get_template('%s.html' % page)
    html = template.render()
    with open('gen/%s.html' % page, 'w') as f:
      f.write(html.encode('utf8'))
      f.close()

  # START Gallery 
  template = env.get_template('project.html')

  FIELDS = ['name', 'project_title', 'team_name',
  'truonex_link', 'problem', 'why_compelling', 'summary',
  'tags', 'status', 'affiliation', 'country', 'class_of', 'online']
  all_projects = []
  with open('projects.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      template_data = {}
      for i, item in enumerate(FIELDS):
        template_data[item] = row[i]
      if template_data['project_title'] == "":
        continue
      html = template.render(template_data)
      projectUniqueName = createUniqueName(template_data['project_title'])
      with open('gen/%s.html' % projectUniqueName, 'w') as g:
        g.write(html)
        g.close()
      template_data['link'] = "%s.html" % projectUniqueName
      all_projects.append(template_data)
    f.close()

  template = env.get_template('all_projects.html')
  print >> sys.stderr, len(all_projects)
  with open('gen/gallery.html', 'w') as g:
    g.write(template.render({'projects': all_projects}))
    g.close()
  # Gallery END

if __name__ == '__main__':
  Main()