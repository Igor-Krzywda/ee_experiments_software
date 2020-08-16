#!/usr/bin/python

import sys
import csv

def partition(arr_m, arr_s, low,high):
	pivot = arr_m[high]
	i = low - 1
	for j in range(low, high):
		if arr_m[j] < pivot:
			i += 1
			arr_m[i], arr_m[j] = arr_m[j], arr_m[i]
			arr_s[i], arr_s[j] = arr_s[j], arr_s[i]
	arr_m[i + 1], arr_m[high] = arr_m[high], arr_m[i + 1]
	arr_s[i + 1], arr_s[high] = arr_s[high], arr_s[i + 1]
	return i + 1

def quick_sort(arr_m, arr_s, low, high):
	if low < high:
		pi = partition(arr_m, arr_s, low,high)
		quick_sort(arr_m, arr_s, low, pi - 1)
		quick_sort(arr_m, arr_s, pi + 1, high)

def generate_filepath(filepath):
	out = filepath[0:len(filepath) - 4]
	out +="_OUT.CSV"
	return out

def sort_results(filepath):
	distance = list()
	load = list()
	with open(filepath, newline = '\n') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			distance.append(float(row[0]))
			load.append(float(row[1]))
	quick_sort(distance,load,0,len(distance) - 1)
	with open(generate_filepath(filepath), "w") as f:
		csv_write = csv.writer(f, delimiter=',')
		csv_write.writerow(['d'] + ['F'])
		for i in range(0,len(load)):
			csv_write.writerow([distance[i]] + [load[i]])

if __name__ == "__main__":
	for arg in sys.argv[1:]:
		sort_results(arg)
