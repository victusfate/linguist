import os
import sys
import json
import numpy as np
from sys import platform

from rsyslog_cee import log

from bandolier import message_queue
from bandolier import data_tools
from bandolier.s3util import S3

import consul
import requests


log.set_service_name('linguist')
log.reset()



# ==============================================================================
# == Main Thread Data Processing ===============================================
# ==============================================================================


AWS_REGION               = 'us-east-1'
AWS_BUCKET               = 'welcome.local'
AWS_BUCKET_INTERNAL      = None
CONFIG                   = {}
AWS_PROFILE              = None
ENVIRONMENT              = 'd2'
REDIS_HOST               = None

s3                       = None
CONSUL_HOST              = None

def setConfig(env=None):
  global CONSUL_HOST, CONFIG, ENVIRONMENT
  global AWS_REGION, AWS_BUCKET, AWS_BUCKET_INTERNAL, REDIS_HOST
  global AWS_PROFILE
  try:
    CONSUL_HOST = os.getenv('CONSUL_HOST')
    print('CONSUL_HOST',CONSUL_HOST)
    c = consul.Consul(host=CONSUL_HOST)
    consul_url = 'http://' + CONSUL_HOST + ':8500/v1/kv/?keys'
    # print('consul_url',consul_url)
    keys = requests.get(consul_url)
    keys = keys.json()
    # print('keys',keys)
    consul_list = []
    for key in keys:
      consul_tuple = c.kv.get(key,None)
      consul_list.append(consul_tuple[1])
    # print('consul_list',consul_list)
    CONFIG = data_tools.consul_to_nested_dict(consul_list)
    # print('CONFIG',CONFIG)
  except Exception as e:
    print('linguist.constants consul exception',e)

  if not CONFIG and env:
    dirname = os.path.dirname(__file__)
    CONFIG_PATH = os.path.join(dirname, 'bin/config_' +  env + '.json')
    with open(CONFIG_PATH) as config_file:
      CONFIG = json.load(config_file)

  if 'environment' in CONFIG:
    ENVIRONMENT = CONFIG['environment']

  if 'aws' in CONFIG and 'region' in CONFIG['aws']:
    AWS_REGION = CONFIG['aws']['region']

  if 'aws' in CONFIG and 's3' in CONFIG['aws'] and 'buckets' in CONFIG['aws']['s3'] and 'primary' in CONFIG['aws']['s3']['buckets']:
    AWS_BUCKET = CONFIG['aws']['s3']['buckets']['primary']

  if 'aws' in CONFIG and 's3' in CONFIG['aws'] and 'buckets' in CONFIG['aws']['s3'] and 'internal' in CONFIG['aws']['s3']['buckets']:
    AWS_BUCKET_INTERNAL = CONFIG['aws']['s3']['buckets']['internal']

  def fabio_ip():
    if os.getenv('NOMAD_HOST_IP_linguist'):
      return os.getenv('NOMAD_HOST_IP_linguist')
    if os.getenv('DOMAIN_FABIO'):
      return os.getenv('DOMAIN_FABIO')
    return 'localhost'

  if os.getenv('CACHE_REDIS_HOST'):
    REDIS_HOST = os.getenv('CACHE_REDIS_HOST')
  else:
    REDIS_HOST = fabio_ip()

  print('REDIS_HOST',REDIS_HOST)

  if platform == 'darwin':
    AWS_PROFILE = 'welco'

setConfig()


# shared s3 interface
print('AWS_BUCKET',AWS_BUCKET,'AWS_REGION',AWS_REGION)
if AWS_BUCKET and AWS_REGION:
  s3 = S3(bucket_name=AWS_BUCKET,profile_name=AWS_PROFILE,region_name=AWS_REGION)

print('s3',s3)



