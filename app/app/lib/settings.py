import os
from aiohttp import web
from gino import Gino


DB_URL = 'postgres://castom_user:castom_pass@127.0.0.1:5432/advertisement'

# инициализируем приложение
app = web.Application()
# инициализируем базу
db = Gino()
