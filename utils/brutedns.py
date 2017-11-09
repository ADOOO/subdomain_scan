#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dns.resolver
from Queue import Queue
import threading
import sys
from config import *


class BruteDns(object):
	def __init__(self, domain):
		self.domain = domain
		self.thread_count = thread_count
		self.queue = Queue
		self.result = []


	def run(self):
		self.queue = Queue()
		with open('dict/subnames.txt') as f:
		# with open('dict/test.txt') as f:
			for i in f:
				self.queue.put(i.rstrip() + '.' + self.domain)
		total = self.queue.qsize()
		threads = []
		for i in xrange(self.thread_count):
			threads.append(self.BruteRun(self.queue, total, self.result))

		for t in threads:
			t.start()
		for t in threads:
			t.join()

		return list(set(self.result))

	class BruteRun(threading.Thread):
		def __init__(self, queue, total, result):
			threading.Thread.__init__(self)
			self._queue = queue
			self.total = total
			self.result = result
			
			
		def run(self):
			while not self._queue.empty():
				sub = self._queue.get_nowait()

				try:
					self.msg()
					results = dns.resolver.query(sub, 'A') #search A
					if results.response.answer:
						# for i in results.response.answer: 
						# 	for j in i.items: 
						# 		ip = j.address
						# 		self.result.append(sub)
						# print sub
						self.result.append(sub)

				except Exception,e:
					# print e
					pass

		def msg(self):
			done_count = float(self.total - self._queue.qsize())
			all_count = float(self.total)
			found_count = len(self.result)
			msg = '\t[-]Last {} | Complete {:.2f}% | Found {}'.format(self._queue.qsize(), float((done_count / all_count)*100), found_count)
			sys.stdout.write('\r'+msg)
			sys.stdout.flush()

