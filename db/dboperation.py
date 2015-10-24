#/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

import aiomysql
import asyncio

global __pool

#create connection pools
@asyncio.coroutine
def create_pools(loop, pool_size=5, **kw):
	global __pool
	try:
		__pool = yield from aiomysql.create_pool(
			maxsize = pool_size,
			minsize = pool_size,
			loop = loop,
			**kw
		)
	except Exception as e:
		raise e

@asyncio.coroutine
def select(sql, args, size=None):
	global __pool
	with (yield from __pool) as conn:
		try:
			cur = yield from conn.cursor(aiomysql.DictCursor)
			yield from cur.execute(sql.replace('?', '%s'), args or ())
			if size:
				rs = yield from cur.fetchmany(size)
			else:
				rs = yield from cur.fetchall()
			yield from cur.close()
			return rs
		except Exception as e:
			raise e
		finally:
			conn.close()

@asyncio.coroutine
def execute(sql, args):
	global __pool
	with (yield from __pool) as conn:
		try:
			cur = yield from conn.cursor(aiomysql.DictCursor)
			yield from cur.execute(sql.replace('?', '%s'), args)
			affected = cur.rowcount
			yield from cur.close()
			if affected != 0:
				yield from conn.commit()
			else:
				yield from conn.rollback()
			return affected
		except Exception as e:
			yield from conn.rollback()
			raise e
		finally:
			conn.close()

