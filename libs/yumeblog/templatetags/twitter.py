#
# http://www.djangosnippets.org/snippets/593/
# author: Author: gmacgregor
# 
from django.template import Library, Node, TemplateSyntaxError
from django.conf import settings
import twitter

register = Library()

class TwitterStatusNode(Node):
	def __init__(self, tweet, tweet_time, tweet_url):
		self.tweet = tweet
		self.tweet_time = tweet_time
		self.tweet_url = tweet_url
	
	def render(self, context):
		try:
			api = twitter.Api()
			most_recent_status = api.GetUserTimeline(settings.TWITTER_USERNAME)[0]
			context[self.tweet] = most_recent_status.text
			context[self.tweet_time] = most_recent_status.relative_created_at
			context[self.tweet_url] = "http://twitter.com/%s/statuses/%s" % (settings.TWITTER_USERNAME, most_recent_status.id)
		except:
			context[self.tweet] = "Ack! Looks like Twitter's codes are broken!"
			context[self.tweet_time] = ""
			context[self.tweet_url] = ""
		return ''

@register.tag(name='get_twitter_status')
def twitter_status(parser, token):
	"""
	Call this tag with: 
		get_twitter_status as tweet_var tweet_time_var tweet_url_var
	"""
	bits = token.split_contents()
	if len(bits) != 5:
		raise TemplateSyntaxError, "%s takes 4 arguments" % bits[0]
	if bits[1] != "as":
		raise TemplateSyntaxError, "First argument for %s should be 'as'" % bits[0]
	return TwitterStatusNode(bits[2], bits[3], bits[4])

######################################################
# Alternative to the above tag
######################################################

class TwitterStatusNode(Node):
	def __init__(self, tweet):
		self.tweet = tweet
	
	def render(self, context):
		try:
			api = twitter.Api()
			most_recent_status = api.GetUserTimeline(settings.TWITTER_USERNAME)[0]
			context[self.tweet] = {
				"status": "%s" % most_recent_status.text,
				"url": "http://twitter.com/%s/statuses/%s" % (settings.TWITTER_USERNAME, most_recent_status.id),
				"time": "%s" % most_recent_status.relative_created_at,
			}			
		except:
			context[self.tweet] = {
				"status": "Ack! Looks like Twitter's codes are broken!",
				"url": "",
				"time": "",
			}			
		return ''

@register.tag(name='get_twitter_status')
def twitter_status(parser, token):
	"""
	Call this tag with: 
		get_twitter_status as tweet
	"""
	bits = token.split_contents()
	if len(bits) != 3:
			raise TemplateSyntaxError, "%s takes 2 arguments" % bits[0]	
	if bits[1] != "as":
		raise TemplateSyntaxError, "First argument for %s should be 'as'" % bits[0]
	return TwitterStatusNode(bits[2])
