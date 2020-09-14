#!/usr/bin/python

#
#                   C
#                   |
#                   |
#                   |
#                   |
#   A---------------C'-----------B
#
#   l = |AB|        d = |C'B|               h = |CC'|
#   m - mass[kg]    r - wheel radius[m]     tbf - max braking torque front[Nm]
#   u - friction coefficient                tbb - max braking torque back[Nm]
#   srf - static reaction front             srb - static reaction back
#   drf - dynamic reaction front            drb - dynamic reaction back

from matplotlib import pyplot as plt
import numpy as np
import math
import csv
import os

class Simulation():
	def __init__(self, filepath, status):
		self.filepath, self.work_dir = '', ''
		self.name = []
		self.l = []
		self.h = []
		self.r = []
		self.tbf = []
		self.tbb = []
		self.rbf = []
		self.rbb = []
		self.u = []
		self.m = []
		self.v = []
		self.incline = []
		self.weight = []
		self.bff = []
		self.bfb = []
		self.d, self.t, self.a, self.s, self.avg_a = 0, 0, 0, 0, 0
		self.i = 0
		if status == 'g':
			self.work_dir = os.path.join(filepath,'..')
			with open(filepath, 'r') as input_data:
				csv_r = csv.reader(input_data, delimiter = ',')
				for row in csv_r:
					self.name.append(row[0])
					self.l.append(float(row[1]))
					self.h.append(float(row[2]))
					self.r.append(float(row[3]))
					self.tbf.append(float(row[4]))
					self.tbb.append(float(row[5]))
					self.rbf.append(float(row[6]))
					self.rbb.append(float(row[7]))
					self.u.append(float(row[8]))
					self.m.append(float(row[9]))
					self.v.append(float(row[10]))
					self.incline.append(float(row[11]))
					self.weight.append(float(row[9]) * 9.81)
					self.bff.append(float(row[4]) / float(row[6]))
					self.bfb.append(float(row[5]) / float(row[7]))
		elif status == 'r':
			self.filepath = filepath
	
	def static_reaction_fr(self):
		return (self.weight[self.i] * self.d) / self.l[self.i]

	def static_reaction_rr(self):
		return self.weight[self.i] - self.static_reaction_fr()
	
	def dynamic_reaction_fr(self, *args):
		return (self.weight[self.i] * self.d + self.m[self.i] * self.a * self.h[self.i]) / self.l[self.i]

	def dynamic_reaction_rr(self):
		return self.weight[self.i] - self.dynamic_reaction_fr()

	def max_potential_braking_force_fr(self):
		return self.dynamic_reaction_fr() * self.u[self.i]
	
	def max_potential_braking_force_rr(self):
		return self.dynamic_reaction_rr() * self.u[self.i] 

	def max_real_braking_force_fr(self): 
		out =  self.max_potential_braking_force_fr()
		if out >= (self.bfb[self.i] / 0.09):
			return self.bfb[self.i] / 0.09
		elif out <= 0:
			return 0
		else:
			return out
	
	def max_real_braking_force_rr(self):
		out = self.max_potential_braking_force_rr()
		if out >= (self.bff[self.i]):
			return self.bff[self.i] 
		elif out <= 0:
			return 0
		else:
			return out

	def max_real_braking_force_net(self):
		return self.max_real_braking_force_fr() + self. max_real_braking_force_rr()	

	def deceleration(self):
		return self.max_real_braking_force_net() / self.m


	def load_front(self, bf):
		if self.d < 0:
			return (self.weight[self.i] * abs(self.d) + bf * self.h[self.i]) / (abs(self.d) + self.l[self.i])
		else:
			return (self.weight[self.i] * self.d + bf * self.h[self.i]) / self.l[self.i]

	def load_rear(self, bf):	# bf - braking force	
		return self.weight[self.i] - self.load_front(bf)

	def max_braking_force_net(self):
		bf = self.bff[self.i] + self.bfb[self.i]
		max_braking = self.weight[self.i] * self.u[self.i]
		if self.load_rear(bf) < 0:
			if self.d >= 0:
				bf = ((self.weight[self.i] / self.l[self.i]) - self.weight[self.i] * self.d) / self.h[self.i]
			elif self.d < 0:
				bf = self.weight[self.i] * self.u[self.i]
				if bf > self.bfb[self.i]:
					return self.bfb[self.i]
		return bf

	def generate_directory(self):
		params = 'l = '+str(self.l[self.i])+'\nh = '+str(self.h[self.i])+'\nr = '+str(self.r[self.i])+'\ntbf = '+str(self.bff[self.i])+'\ntbb = '+str(self.bfb[self.i])+'\nu = '+str(self.u[self.i])+'\nm = '+str(self.m[self.i])
		self.work_dir = os.path.join(self.filepath, self.name[self.i])
		os.mkdir(self.work_dir)
		path = os.path.join(self.work_dir, 'info')
		os.mkdir(path)

		with open(path + '/params.txt', 'w') as f:
			f.write(params)
		
		path = os.path.join(self.work_dir, 'data')
		os.mkdir(path)

		print('directory ', path, 'created')

	def conspect(self):
		conspect_path = self.work_dir + '/info/' + self.name[self.i] + '.csv'
		with open(conspect_path, 'a') as f:
			csv_wr = csv.writer(f, delimiter = ',')
			csv_wr.writerow(["{0:.2f}".format(self.d)] + ["{0:.2f}".format(self.t)] + ["{0:.2f}".format(self.s)] + ["{0:.2f}".format(self.avg_a)])

	def generate_data(self):
		for v_w in self.v:
			ff, fb, fn = 0, 0, 0
			self.generate_directory()
			v = v_w
			self.d = self.l[self.i] * (-0.25)
			while self.d < self.l[self.i] - 0.2:
				path = os.path.join(self.work_dir, 'data', str('{0:.2f}'.format(self.d)) + '.csv')
				with open(path, 'w') as f:
					csv_wr = csv.writer(f, delimiter = ',')
					while v > 0:
						ff = self.max_real_braking_force_fr()
						fr = self.max_real_braking_force_rr()
						fn = self.max_braking_force_net()
						self.a = fn / self.m[self.i]
						if self.a <= 0:
							break
						v -= self.a * 0.1
						self.s += v * 0.1 + abs(0.5 * self.a * 0.01)
						self.t += 0.1
						csv_wr.writerow(["{0:.2f}".format(self.t)]+["{0:.2f}".format(self.a)]+
							["{0:.2f}".format(v)]+["{0:.2f}".format(self.s)]+["{0:.2f}".format(fn)]+
							["{0:.2f}".format(ff)]+["{0:.2f}".format(fr)])
				if self.a <= 0:
					break
				self.avg_a = v_w / self.t
				self.conspect()
				self.d += 0.01
				v = v_w
				self.a, self.t, self.s, self.avg_a = 0, 0, 0, 0
			self.i += 1
	
	def arr_size(self):
		arg_size = 0
		for n in self.name:	
			path = n + '/info/' + n + '.csv'
			with open(path, 'r') as f:
				row_count = sum(1 for row in csv.reader(f, delimiter = ','))
				if row_count > arg_size:
					arg_size = row_count
		return arg_size

	def plot_conspects(self, *args):
		files = []
		arr_height = self.arr_size()
		arr_width = 1
		file_count, arg_count = 0, 0 
		arg_stat = np.zeros(3)
		for a in args:
			if a == 'a' :
				arr_width += 1
				arg_stat[0] = 1
				arg_count += 1
			elif a == 't':
				arr_width += 1
				arg_stat[1] = 1
				arg_count += 1
			elif a == 's':
				arr_width += 1
				arg_stat[2] = 1
				arg_count += 1
			else:
				files.append(a)
				file_count += 1
		arr_width *= file_count
		data = np.zeros([arr_height, arr_width], dtype = float)

		for f in files:
			k, i = 0, 0
			path = f + '/info/' + f + '.csv'
			with open(path, 'r') as fl:
				csv_r = csv.reader(fl, delimiter = ',')
				for row in csv_r:
					print(row)
					j = k
					print(j)
					if arg_stat[0] == 1:
						j += 1
						print(j)
						data[i,j] = float(row[3])
					if arg_stat[1] == 1:
						j += 1
						data[i,j] = float(row[1])
					if arg_stat[2] == 1:	
						j += 1
						data[i,j] = float(row[2])
					data[i,0] = float(row[0])
					i += 1
			k = i * arg_count
			print(data)
			plt.plot(data[:,0], data[:,1])	
		plt.show()

if __name__ == "__main__":
	sim = Simulation('sample_csv.csv', 'g')
	#sim.generate_data()
	sim.plot_conspects('a', 'my_bike', 'bike_2')
