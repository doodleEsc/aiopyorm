#/usr/bin/env python
# -*- coding: UTF-8 -*-

from fields.fields import *

class ModelMetaClass(type):
	def __new__(cls, name, bases, attrs):
		if name == 'Model':
			#super(ModelMetaClass, cls).__new__(cls, name, bases, attrs)
			type.__new__(cls, name, bases, attrs)

		tableName = attrs.get('__tableName__', None) or name
		mappings = dict() #所有参数的映射关系
		fields = [] #除主键外的所有参数
		primaryKey = None
		#将定义的列映射到mappings里面
		for k, v in attrs.items():
			if isinstance(v,Field):
				mappings[k] = v
				if v.primary_key:
					if primaryKey:
						raise RuntimeError('Duplicate primary key')
					primaryKey = k
				else:
					fields.append(k)

		#清空参数字典，以便从新构造参数字典
		for k in mappings.keys():
			attrs.pop(k)

		#普通参数字符串列表，用来构造SQL语句
		no_pri_field = list(map(lambda f: '%s' %f, fields))

		attrs['__mapping__'] = mappings
		attrs['__fields__'] = fields
		attrs['__table__'] = tableName
		attrs['__primaryKey__'] = primaryKey

		#构造基本SQL语句
		attrs['__select__'] = 'SELECT %s,%s FROM %s' %(primaryKey, ','.join(no_pri_field), tableName)
		attrs['__insert__'] = 'INSERT INTO %s (%s,%s) VALUES (%s)' %(tableName, ','.join(no_pri_field), primaryKey, _getValueString(len(no_pri_field) + 1))
		attrs['__update__'] = 'UPDATE %s SET %s WHERE %s=?' %(tableName, ','.join(list(map(lambda f: '%s=?' %f, no_pri_field))), primaryKey)
		attrs['__delete__'] = 'DELETE FROM %s WHERE %s=?' %(tableName,primaryKey)

		#return super(ModelMetaClass,cls).__new__(cls, name, bases, attrs)
		return type.__new__(cls, name, bases, attrs)


def _getValueString(length):
	strList = []
	for i in range(0,length):
		strList.append('?')
	return ','.join(strList)