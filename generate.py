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
  with open('projects.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      template_data = {}
      for i, item in enumerate(FIELDS):
        template_data[item] = row[i]
      html = template.render(template_data)
      with open('gen/%s.html' % createUniqueName(template_data['project_title']), 'w') as g:
        g.write(html)
        g.close()

if __name__ == '__main__':
  Main()