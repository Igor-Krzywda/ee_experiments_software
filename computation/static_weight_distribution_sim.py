#!/usr/bin/python

import sys
import csv
import math

def generate_data(length, weight):
	r1 = r2 = thf = thb = 0
	a = 5
	d = 0.01
	with open("out.csv", 'w', newline = '\n') as f:
		writer = csv.writer(f, delimiter = ',')
		writer.writerow(["d", "torque_b", "torque_f", "thb", "thf"])
		while d < length:
			r1 = (weight * (length - d)) / length
			r2 = weight - r1
			thb = (r1 + 70 * a) / length
			thf = weight - thb
			writer.writerow([d] + [r1] + [r2] + [thb] + [thf])
			d += 0.01

if __name__ == "__main__":
	generate_data(1.1, 686.7)
