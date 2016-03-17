#!/usr/bin/env python

class GenLm(object):
	"""docstring for GenLm"""
	def __init__(self):
		super(GenLm, self).__init__()
		self.head = ["I want", "I will take"]
		self.conj = ["and", "with"]
		self.food = ["noodles", "peanuts", "hamburger", "fries"]
		self.drink = ["orange juice", "water"]

	def gen(self):
		for head in self.head:
			for conj in self.conj:
				for food in self.food:
					print head + " " + conj + " " + food

			for drink in self.drink:
				print head + " " + drink
			

if __name__=="__main__":
    main = GenLm().gen()