from sanic import Sanic
from sanic.response import json as sanic_json
import json
import time
import requests
from linguist import constants
import redis
import asyncio
import os
import psutil
import urllib.parse

from os import path
from pathlib import Path

from rsyslog_cee import log
from rsyslog_cee.logger import Logger,LoggerOptions

from linguist.transformers import Transformers

PORT = 5050

tStart = time.time()

app = Sanic("Linguist")
cache = redis.Redis(host=constants.REDIS_HOST, port=6379, db=0)   

def reset_logger():
  oNewLogger = Logger(
        LoggerOptions(
            service='linguist.welco.me', # The App Name for Syslog
            console= True,        # we log to console here
            syslog=  False        # Output logs to syslog
        )
    )
  log.set_logger(oNewLogger)
reset_logger()
log.info('deployment start',tStart)

@app.route('/')
async def index(request):
  return sanic_json({'message': 'yup'})

@app.route('/health')
async def health(request):    
  pid = os.getpid()
  process = psutil.Process(pid)
  memory_bytes = process.memory_info().rss  # in bytes 
  logs = {
    'service': 'Linguist',
    'purpose': 'Linguist',
    'process': pid,
    'memory': memory_bytes 
  }
  return sanic_json(logs)

@app.route('/ner/<text>',methods=['GET'])
async def ner_get(request,text=None):
  reset_logger()
  text = urllib.parse.unquote(text,'utf-8')
  results = Transformers.ner(text)
  log.oLogger.summary('server.ner_get.Summary')
  return sanic_json(results)

@app.route('/ner',methods=['POST'])
async def ner_post(request):
  reset_logger()
  text = request.json.get('text')
  results = Transformers.ner(text)
  log.oLogger.summary('server.ner_post.Summary')
  return sanic_json(results)

@app.route('/pos/<text>',methods=['GET'])
async def pos_get(request,text=None):
  reset_logger()
  text = urllib.parse.unquote(text,'utf-8')
  results = Transformers.pos(text)
  log.oLogger.summary('server.ner_get.Summary')
  return sanic_json(results)

@app.route('/pos',methods=['POST'])
async def pos_post(request):
  reset_logger()
  text = request.json.get('text')
  results = Transformers.pos(text)
  log.oLogger.summary('server.ner_post.Summary')
  return sanic_json(results)

@app.route('/spacy_seg/<text>',methods=['GET'])
async def spacy_seg_get(request,text=None):
  reset_logger()
  text = urllib.parse.unquote(text,'utf-8')
  results = Transformers.seg(text)
  log.oLogger.summary('server.spacy_seg_get.Summary')
  return sanic_json(results)

@app.route('/spacy_seg',methods=['POST'])
async def spacy_seg_post(request,text=None):
  reset_logger()
  text = request.json.get('text')
  results = Transformers.seg(text)
  log.oLogger.summary('server.spacy_seg_post.Summary')
  return sanic_json(results)

@app.route('/ner_pos/<text>',methods=['GET'])
async def ner_pos_get(request,text=None):
  reset_logger()
  text = urllib.parse.unquote(text,'utf-8')
  result = Transformers.ner_pos(text)
  log.oLogger.summary('server.ner_pos_get.Summary')
  return sanic_json(result)

@app.route('/ner_pos',methods=['POST'])
async def ner_pos_post(request,text=None):
  reset_logger()
  text = request.json.get('text')
  result = Transformers.ner_pos(text)
  log.oLogger.summary('server.ner_pos_post.Summary')
  return sanic_json(result)

@app.route('/ner_pos_lines',methods=['POST'])
async def ner_pos_post(request,text=None):
  reset_logger()
  lines = request.json.get('lines')
  result = Transformers.ner_pos_lines(lines)
  log.oLogger.summary('server.ner_pos_lines.Summary')
  return sanic_json(result)

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=PORT)
