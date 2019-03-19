#!/bin/python
from alex import alex

def switch(value):
	if(value == 2):
		alex.counter += 1
	else:
		print("default")


