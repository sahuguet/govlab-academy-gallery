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
  env.filters['skolem'] = lambda x: x.lower().replace(' ', '_').replace('"','')


  for page in ['offerings', 'index', 'resources']:
    template = env.get_template('%s.html' % page)
    html = template.render()
    with open('gen/%s.html' % page, 'w') as f:
      f.write(html.encode('utf8'))
      f.close()

  # START Gallery 
  template = env.get_template('project.html')

  TOPICS = [ 'topic%d' % k for k in range(1, 10)]
  TYPES  = [ 'type%d' % k for k in range(1, 10)]
  DIMS   = [ 'dim%d' % k for k in range(1, 10)]


  import random

  FIELDS = ['name', 'project_title', 'team_name',
  'truonex_link', 'problem', 'why_compelling', 'summary',
  'tags', 'status', 'affiliation', 'country', 'class_of', 'online']
  all_projects = []
  count = 0
  with open('projects.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      template_data = {}
      for i, item in enumerate(FIELDS):
        template_data[item] = row[i]
      if template_data['project_title'] == "":
        continue
      template_data['id'] = count
      count = count + 1
      template_data['topic'] = random.choice(TOPICS)
      template_data['type'] = random.choice(TYPES)
      template_data['dim'] = random.choice(DIMS)
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
    g.write(template.render({'projects': all_projects}, topics=TOPICS, types=TYPES, dims=DIMS))
    g.close()
  # Gallery END

  # Doing the /about page
  template = env.get_template('about.html')
  with open('people.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='|')
    people = []
    all_clusters = set()
    for row in reader:
      (name, clusters) = row
      clusters = map(lambda x:x.strip(), clusters.split(','))
      for c in clusters: all_clusters.add(c)
      people.append({'name': name, 'clusters': clusters})
    f.close()
    people = sorted(people, key=lambda x:x['name'])
  with open('gen/about.html', 'w') as g:
    g.write(template.render({ 'people': people, 'all_clusters': all_clusters }))
    g.close()

if __name__ == '__main__':
  Main()