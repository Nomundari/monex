# !/usr/bin/python/env
# -*- coding: utf-8 -*-

import session

class AuthMiddleware(object):

	def process_request(self, request):
		request.user = None
		try:
			user = session.get(request, 'user')
			if user:
				request.user = user
			else:
				request.user = manager
		except:
			pass


	#def template_response(self, request, response):
