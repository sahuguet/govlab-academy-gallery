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
      all_projects.append({ 'name': template_data['project_title'], 'link': "%s.html" % projectUniqueName})
    f.close()
  template = env.get_template('all_projects.html')
  print >> sys.stderr, len(all_projects)
  with open('gen/index.html', 'w') as g:
    g.write(template.render({'projects': all_projects}))
    g.close()
if __name__ == '__main__':
  Main()