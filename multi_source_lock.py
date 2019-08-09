# -*- coding=utf8 -*-

"""
游戏中经常会出现在多个地方占据同一份资源的情况，例如：
    - 某个玩家受到了两个时长不同的buff，其都会使玩家释放不了技能
	- 当时长较短的buff消失的时候，技能仍然需要处于禁用状态
	- 当所有禁用技能的buff消失的时候，技能恢复可用

其中包含的一个通用问题即：
	- 同一处位置被多次锁定，只有所有的锁都解除时才能恢复可用状态

一种可能的python实现是使用装饰器，对某个调用开关的函数加上来源指定
"""

import functools


def multi_source_lock(func):
	"""
	记录所有上锁的source，同一个source是不能重复上锁的
	"""
	lock_record = set()

	@functools.wraps(func)
	def wrapper(bool_val, **kwargs):
		source = kwargs.get('lock_source', 'common')

		# lock的时候不需要判断，只需要记录source即可
		if not bool_val:
			lock_record.add(source)
			return func(bool_val)

		# unlock的时候需要判断所有的lock是否都已经解除
		else:
			source in lock_record and lock_record.remove(source)
			if not lock_record:
				return func(bool_val)

	wrapper.lock_record = lock_record
	return wrapper


# +++++++++++++++++++ example +++++++++++++++++++

@multi_source_lock
def set_skill_enable(enabled):
	"""
	设置技能是否可用的函数
	"""
	pass


class SkillForbidDebuff(object):
	def __init__(self, no):
		self.no = no

	def on_add_state():
		set_skill_enable(False, source=self.no)

	def on_remove_state():
		set_skill_enable(True, source=self.no)

# ------------------- example --------------------
