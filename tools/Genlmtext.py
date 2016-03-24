#!/usr/bin/env python

class GenLm(object):
	"""docstring for GenLm"""
	def __init__(self):
		super(GenLm, self).__init__()
		self.head = ["go", "navigate"]
		self.conj = ["to"]
		self.food = ["noodles", "peanuts", "hamburger", "fries"]
		self.place = ["kitchen" , "living room" , "bedroom" , "hallway" , "bathroom"]
		# self.drink = ["orange juice", "water"]

	def gen(self):
		for head in self.head:
			for conj in self.conj:
				# Food
				# for food in self.food:
				# 	print head + " " + conj + " " + food

				# Place
				for place in self.place:
					print head + " " + conj + " " + place

			# Drink
			# for drink in self.drink:
			# 	print head + " " + drink
			

if __name__=="__main__":
    main = GenLm().gen()