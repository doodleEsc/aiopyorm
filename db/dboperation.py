#/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

import aiomysql
import asyncio

global _pool

#create connection pools
@asyncio.coroutine
def create_pools(loop, pool_size=5, **kw):
	global _pool
	try:
		_pool = yield from aiomysql.create_pool(
			maxsize = pool_size,
			minsize = pool_size,
			loop = loop,
			**kw
		)
	except Exception as e:
		raise e

@asyncio.coroutine
def select(sql, args, size=None):
	global _pool
	try:
		with (yield from _pool) as conn:
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

@asyncio.coroutine
def execute(sql, args):
	global _pool
	try:
		with (yield from _pool) as conn:
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

