# encoding: utf-8

from __future__ import division, print_function, unicode_literals
import objc
import sys, os, re
import math

from GlyphsApp import *
from GlyphsApp.plugins import *

class ShowComponentsCompatibility (ReporterPlugin):
	@objc.python_method
	def settings(self):
		self.menuName = "Components Compatibility"

	@objc.python_method
	def checkComponents(self, Layer):

		currentLayer = Layer
		thisGlyph = currentLayer.parent
		thisFont = thisGlyph.parent

		HandleSize = self.getHandleSize()
		scale = self.getScale()
		zoomedHandleSize = HandleSize / scale

		initPos = -30
		step = 24
		xHeight = thisFont.selectedFontMaster.xHeight
		angle = thisFont.selectedFontMaster.italicAngle
		offset = math.tan(math.radians(angle)) * xHeight/2

		lista = []

		for thisMaster in thisFont.masters: 
			thisMasterId = thisMaster.id
			masterIndex = thisFont.masters.index(thisMaster)
			frontLayers = thisGlyph.layers[thisFont.masters[masterIndex].id]
			
			for thisComponent in frontLayers.components:
				lista.append(str(thisComponent.name))
			
		fontColor1 = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, 0.7)
		fontColor2 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 0.45 )

		for currentComponent in currentLayer.components:
		
			name = currentComponent.name
			posX = currentComponent.position.x
			posY = currentComponent.position.y
			
			if lista.count(currentComponent.name) != len(thisFont.masters):
				self.drawTextAtPoint(u"%s" % name, (10 - offset, initPos), 14.0, fontColor1)
			else:
				self.drawTextAtPoint(u"%s" % name, (10 - offset, initPos), 14.0, fontColor2)

			initPos = initPos - step

	@objc.python_method
	def background(self, Layer):
		try:
			NSColor.colorWithCalibratedRed_green_blue_alpha_(0.0, 0.5, 0.3, 0.5).set()
			self.checkComponents(Layer)
		except Exception as e:
			import traceback
			print(traceback.format_exc())
