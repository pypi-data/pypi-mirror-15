#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time
import os

FNULL = open(os.devnull, 'w')

songRunning = False
class Data:
	def __init__(self, com="", msg="", sp="False"):
		self.command = com
		self.message = msg
		self.speak = sp
	def interact(self,duration):
		subprocess.Popen(["notify-send","Dragonfire", self.message])
		if self.command != "":
			time.sleep(duration)
			subprocess.Popen(self.command, stdout=FNULL, stderr=FNULL)
		#if self.speak == True:
		#	self.say(self.message)
		#else:
	def say(self,message):
		#if songRunning == True:
		#	subprocess.Popen(["rhythmbox-client","--pause"])
		if len(message) < 10000:
			print "Dragonfire: " + message.upper()
		print "_______________________________________________________________\n"
		proc = subprocess.Popen(["festival","--tts"], stdin=subprocess.PIPE, stdout=FNULL, stderr=FNULL)
		proc.stdin.write(message)
		proc.stdin.close()
		#proc.wait()
		#if songRunning == True:
		#	subprocess.Popen(["rhythmbox-client","--play"])
	def espeak(self,message):
		subprocess.Popen(["espeak","-v","en-uk-north",message])
