#/usr/bin/env python
# -*- coding: UTF-8 -*-

import time, uuid
import asyncio

from fields.fields import *
from models.model import Model
from db.dboperation import create_pools
from config.config import config


def next_id():
	return '%015d%s000' %(int(time.time()*1000), uuid.uuid4().hex)

class User(Model):
	id = StringField(ddl='VARCHAR(50)',primary_key=True, default=next_id())
	name = StringField(ddl='VARCHAR(50)')
	email = StringField(ddl='VARCHAR(50)')

#main function
def main(loop,**kw):
	yield from create_pools(loop = loop, pool_size=5, **kw)
	s = yield from User.findAll()
	x = s[0]
	yield from x.remove()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(loop,**config))
	