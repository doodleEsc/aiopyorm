# pyorm
This is a simple asynchronous ORM tool built  with python3.5.

###Introduction
ORM（Object Relational Mapping）looks like a virtual object database.   
Briefly，It contains most database operations    
and you don't have to write SQL statements in every database operation.

###Usage

```Python
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
```

###Dependence
*Python 3.x (take a very small change that you can it on Python 2.x)   
  [Python 3.x](https://www.python.org/downloads/release/python-350/)   

*aiomysql
```shell
pip install aiomysql
```     


If you think it is a little bit useful,please take a star!   

####Thank you!




