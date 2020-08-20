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

def sort_results(filepath):
	distance = list()
	load = list()
	distance_clean = list()
	load_clean = list()
	distance_super_clean = list()
	load_super_clean = list()
	with open(filepath, newline = '\n') as f:
		reader = csv.reader(f, delimiter = ',')
		for row in reader:
			distance.append(float(row[0]))
			load.append(float(row[1]))
	quick_sort(distance,load,0,len(distance) - 1)
	filepath_raw = filepath[0:len(filepath) - 4] + "_OUT_RAW.CSV"
	with open(filepath_raw, "w") as f:
		csv_write = csv.writer(f, delimiter = ',')
		csv_write.writerow(['d'] + ['F'])
		for i in range(0,len(load)):
			csv_write.writerow([distance[i]] + [load[i]])
	clean_output(distance, load, distance_clean, load_clean)
	filepath_clean = filepath[0:len(filepath) - 4] + "_OUT_CLEAN.CSV"
	with open(filepath_clean, "w") as f:
		csv_write = csv.writer(f, delimiter = ',')
		csv_write.writerow(['d'] + ['F'])
		for i in range(0, len(distance_clean)):
			csv_write.writerow([distance_clean[i]] + [load_clean[i]])
	super_clean_output(distance_clean, load_clean, distance_super_clean, load_super_clean)
	filepath_super_clean = filepath[0:len(filepath) - 4] + "_OUT_CLEAN_SUPER.CSV"
	with open(filepath_super_clean, "w") as f:
		csv_write = csv.writer(f, delimiter = ',')
		csv_write.writerow(['d'] + ['F'])
		for i in range(0, len(distance_super_clean)):
			csv_write.writerow([distance_super_clean[i]] + [load_super_clean[i]])

def clean_output(distance, load, distance_c, load_c):
	base = distance[0]
	load_sum = load[0]
	prev_pos = 0
	for i in range(1, len(distance)):
		if distance[i] != base:
			mean = load_sum / (i - prev_pos) 
			distance_c.append(distance[prev_pos])
			load_c.append(mean)
			base = distance[i]
			load_sum = load[i]
			prev_pos = i
		else:
			load_sum += load[i]

def super_clean_output(distance, load, distance_c, load_c):
	for i in range(0, len(distance)):
		if load[i] > 1:
			distance_c.append(distance[i])
			load_c.append(load[i])

def print_contents(list1, list2):
	for i in range(0, len(list1)):
		print(list1[i], "\t|\t", list2[i], "\n")

if __name__ == "__main__":
	for arg in sys.argv[1:]:
		sort_results(arg)
