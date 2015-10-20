#/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import asyncio

from metaclass.modelmetaclass import ModelMetaClass
from db.dboperation import select,execute


class Model(dict,metaclass=ModelMetaClass):
	#__metaclass__ = ModelMetaClass
	def __init__(self, **kwargs):
		super(Model, self).__init__(**kwargs)
		#check the required arguments
		for k,v in self.__mapping__.items():
			if v.default is None and k not in self:
				raise ValueError("%s field should not be null" %k)
			#give the default value to object
			elif v.default is not None and k not in self:
				setattr(self, k, v.default)
		#check if dirty arguments exists
		for k in self:
			if k not in self.__mapping__:
				raise ValueError("Database table '%s' does not have '%s' field" %(self.__table__, k))

	
	def __getattr__(self, key):
		try:
			return self[key]
		except Exception as e:
			raise AttributeError('No Such attribute named %s' %key)
		

	def __setattr__(self, key, value):
		self[key] = value

	#获取到的是field
	def getValue(self,key):
		try:
			return getattr(self, key, None)
		except Exception as e:
			raise ValueError('No Such attribute named %s' %key)

	@classmethod
	@asyncio.coroutine
	def find(cls, where=None, args=None, **kw):
		sql = [cls.__select__]
		if where is not None:
			if args is None:
				raise ValueError('args should not be empty')
			if not isinstance(args, list):
				raise ValueError('args should be a list')
			if len(where.split('='))-1 != len(args):
				raise ValueError('args does not match')
			sql.append('WHERE')
			sql.append(where)
		if 'orderby' in kw.keys():
			sql.append('ORDER')
			sql.append('BY')
			sql.append(kw.get('orderby'))

		rs = yield from select(" ".join(sql),args)
		if len(rs) == 0:
			return None
		return cls(**rs[0])

	@classmethod
	@asyncio.coroutine
	def findAll(cls, where=None, args=None, **kw):
		sql = [cls.__select__]
		if where is not None:
			if args is None:
				raise ValueError('args should not be empty')
			if not isinstance(args, list):
				raise ValueError('args should be a list')
			if len(where.split('='))-1 != len(args):
				raise ValueError('args does not match')
			sql.append('WHERE')
			sql.append(where)
		if 'orderby' in kw.keys():
			sql.append('ORDER')
			sql.append('BY')
			sql.append(kw.get('orderby'))
		if 'limit' in kw.keys():
			sql.append('LIMIT')
			sql.append(kw.get('limit'))
		rs = yield from select(" ".join(sql),args)
		if len(rs) == 0:
			return None
		return [cls(**r) for r in rs]

	@asyncio.coroutine
	def save(self):
		sql = self.__insert__
		args = list(map(self.getValue, self.__fields__))
		args.append(self.getValue(self.__primaryKey__))
		rs = yield from execute(sql, args)
		if rs != 1:
			logging.warning('Entry save failed')

	@asyncio.coroutine
	def update(self):
		sql = self.__update__
		args = list(map(self.getValue, self.__fields__))
		args.append(self.getValue(self.__primaryKey__))
		rs = yield from execute(sql,args)
		if rs != 1:
			logging.warning('Entry update failed')

	@asyncio.coroutine
	def remove(self):
		sql = self.__delete__
		args = [self.getValue(self.__primaryKey__)]
		rs = yield from execute(sql, args)
		if rs!= 1:
			logging.warning('Entry remove failed')
		