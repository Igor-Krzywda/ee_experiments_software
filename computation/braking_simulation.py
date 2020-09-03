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

class Bicycle:
	def __init__(self, l, h, r, tbf, tbb, rbf, rbb, u, m):
		self.l = l
		self.h = h
		self.r = r
		self.bff = tbf / rbf
		self.bfb = tbb / rbb
		self.u = u
		self.m = m
		self.a = 0
		self.d = 0
		self.weight = m * 9.81

	def static_reaction_fr(self):
		return (self.weight * self.d) / self.l

	def static_reaction_rr(self):
		return self.weight - self.static_reaction_fr()
	
	def dynamic_reaction_fr(self, *args):
		return (self.weight * self.d + self.m * self.a * self.h) / self.l

	def dynamic_reaction_rr(self):
		return self.weight - self.dynamic_reaction_fr()

	def max_potential_braking_force_fr(self):
		return self.dynamic_reaction_fr() * self.u
	
	def max_potential_braking_force_rr(self):
		return self.dynamic_reaction_rr() * self.u 

	def max_real_braking_force_fr(self): 
		out =  self.max_potential_braking_force_fr()
		if out >= (self.bfb / 0.09):
			return self.bfb / 0.09
		elif out <= 0:
			return 0
		else:
			return out
	
	def max_real_braking_force_rr(self):
		out = self.max_potential_braking_force_rr()
		if out >= (self.bff):
			return self.bff 
		elif out <= 0:
			return 0
		else:
			return out

	def max_real_braking_force_net(self):
		return self.max_real_braking_force_fr() + self. max_real_braking_force_rr()	

	def deceleration(self):
		return self.max_real_braking_force_net() / self.m

class Simulation(Bicycle):
	def __init__(self, l, h, r, tbf, tbb, rbb, rbf, u, m, v, incline, filepath):
		Bicycle.__init__(self, l, h, r, tbf, tbb, rbb, rbf, u, m)
		self.v = v
		self.incline = incline
		self.filepath = filepath

	def load_front(self, bf):
		return (self.weight * self.d + bf * self.h) / self.l

	def load_rear(self, bf):	# bf - braking force	
		return self.weight - self.load_front(bf)

	def max_braking_force_net(self):
		bf = self.bff + self.bfb
		max_braking = self.weight * self.u
		if self.load_rear(bf) < 0:
			print(bf, self.load_rear(bf), self.load_front(bf))
			bf -= 1		# optimize 
		print(bf, self.load_rear(bf))
		return bf

	def generate_directory(self):
		dir_count = 0
		directory = 'sim_' + str(dir_count)
		params = 'l = '+str(self.l)+'\nh = '+str(self.h)+'\nr = '+str(self.r)+'\ntbf = '+str(self.bff)+'\ntbb = '+str(self.bfb)+'\nu = '+str(self.u)+'\nm = '+str(self.m)
		for subdir, dirs, files in os.walk(self.filepath):
				directory = 'sim_' + str(dir_count)
				for i in dirs:
					if i == directory:
						dir_count += 1
		path = os.path.join(self.filepath, directory)
		os.mkdir(path)
		path = os.path.join(self.filepath, directory, 'info')
		os.mkdir(path)

		with open(path + '/params.txt', 'w') as f:
			f.write(params)
		
		path = os.path.join(self.filepath, directory, 'data')
		os.mkdir(path)

		print('directory ', path, 'created')
		return path

	def generate_data(self):
		data_path = self.generate_directory()
		v = self.v
		self.a = 5
		t = ff = fr = fn = 0
		while self.d < self.l:
			path = os.path.join(data_path, str('{0:.2f}'.format(self.d)) + '.csv')
			with open(path, 'w') as f:
				csv_wr = csv.writer(f, delimiter = ',')
				csv_wr.writerow(['t'] + ['a'] + ['v'] + ['s'] + ['F_n'] + ['F_f'] +['F_r'])
				while v > 0:
					ff = self.max_real_braking_force_fr()
					fr = self.max_real_braking_force_rr()
					fn = self.max_braking_force_net()
					self.a = fn / self.m
					v -= self.a * 0.1
					s = abs(0.5 * self.a * 0.01)
					t += 0.1
					# ADDITIONAL LOGIC FOR REAR WHEEL LIFT-OFF
					# ONE STEP AHEAD -> ITERATION -> GETTING BEST RESULT -> C++?
					csv_wr.writerow(["{0:.2f}".format(t)]+["{0:.2f}".format(self.a)]+["{0:.2f}".format(v)]+["{0:.2f}".format(s)]+["{0:.2f}".format(fn)]+["{0:.2f}".format(ff)]+["{0:.2f}".format(fr)])
			self.d += 0.01
			t = 0
			self.a = 0
			v = self.v
	
if __name__ == "__main__":
	sim = Simulation(1.1, 0.8, 0.36, 69.9, 62.3, 0.09, 0.08, 0.8, 85, 50, 0, '/home/ikrz/extended_essay/simulations/')
	sim.generate_data()
