#/usr/bin/env python
# -*- coding: UTF-8 -*-

class Field(object):
	def __init__(self,column_type, primary_key, default):
		#self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default

class StringField(Field):
	def __init__(self,ddl, primary_key=False, default=None):
		super(StringField, self).__init__(ddl, primary_key, default)

class IntegerField(Field):
	def __init__(self, primary_key=False, default=None):
		super(IntegerField, self).__init__('bigint', primary_key, default)

class BooleanField(Field):
	def __init__(self, default=None):
		super(BooleanField, self).__init__('boolean', False, default)

class FloatField(Field):
	def __init__(self, primary_key=False, default=None):
		super(FloatField, self).__init__('real', primary_key, default)

class TextField(Field):
	def __init__(self, default=None):
		super(TextField, self).__init__('text', False, default)