#!/usr/bin/python

#
#					C
#					|
#					|
#					|
#					|
#	A---------------C'-----------B
#
#	l = |AB| 		d = |C'B|				h = |CC'|
#	m - mass[kg]	r - wheel radius[m]		tbf - max braking torque front[Nm]
#	u - friction coefficient				tbb - max braking torque back[Nm]
#	srf - static reaction front				srb - static reaction back
#	drf - dynamic reaction front			drb - dynamic reaction back

import numpy as np
import csv
from matplotlib import pyplot as plt
import math

class Bicycle:
	def __init__(self, l, h, r, tbf, tbb, u, m, a):
		self.l = l
		self.h = h
		self.r = r
		self.tbf = tbf
		self.tbb = tbb
		self.u = u
		self.m = m
		self.a = a
		self.weight = m * 9.81
		self.d = np.arange(0.01, l, 0.01)

	def plot_graph_show(self, x, y, xlabel, ylabel):
		plt.plot(x,y)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.show()

	def plot_graph_save(self, x, y, xlabel, ylabel, filename):
		plt.plot(x,y)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.savefig(filename, bbox_inches = 'tight')

	def static_reaction_fr(self, status):
		out = (self.weight * self.d) / self.l
		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'reaction on front axle [N]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'reaction on front axle [N]', 'static_reaction_front.jpg')
		elif status == 3:
			for i in out:
				print(i)

	def static_reaction_rr(self, status):
		out = self.weight - self.static_reaction_fr(0)
		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_show(self.d, out, 'distance from rear axle [m]', 'reaction on rear axle [N]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'reaction on rear axle [N]', 'static_reaction_rear.jpg')
		elif status == 3:
			for i in out:
				print(i)
	
	def dynamic_reaction_fr(self, status):
		out = (self.weight * self.d + self.m * self.a * self.h) / self.l
		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'reaction on front axle [N]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'reaction on front axle [N]', 'dynamic_reaction_front.jpg')
		elif status == 3:
			for i in out:
				print(i)

	def dynamic_reaction_rr(self, status):
		out = self.weight - self.dynamic_reaction_fr(0)
		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_show(self.d, out, 'distance from rear axle [m]', 'reaction on rear axle [N]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'reaction on rear axle [N]', 'dynamic_reaction_rear.jpg')
		elif status == 3:
			for i in out:
				print(i)

	def max_potential_braking_torque_fr(self, status):
		out = self.dynamic_reaction_fr(0) * self.u * self.r
		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_show(self.d, out, 'distance from rear axle [m]', 'max potential torque without tire-slip on front axle [Nm]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'max potential torque without tire-slip on front axle [Nm]', 'max_potential_torque_front.jpg')
		elif status == 3:
			for i in out:
				print(i)
	
	def max_potential_braking_torque_rr(self, status):
		out = self.dynamic_reaction_rr(0) * self.u * self.r
		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_show(self.d, out, 'distance from rear axle [m]', 'max potential torque without tire-slip on rear axle [Nm]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'max potential torque without tire-slip on rear axle [Nm]', 'max_potential_torque_rear.jpg')
		elif status == 3:
			for i in out:
				print(i)

	def max_real_braking_force_fr(self, status): 
		out = self.max_potential_braking_torque_fr(0)
		for i in range(0, len(out)):
			if out[i] >= self.tbf:
				out[i] = self.tbf / self.r
			elif out[i] <= 0:
				out[i] = 0
			else:
				out[i] = out[i] / self.r

		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_show(self.d, out, 'distance from rear axle [m]', 'max braking torque without tire-slip on front axle [N]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'max braking torque without tire-slip on front axle [N]', 'max_braking_torque_front.jpg')
		elif status == 3:
			for i in out:
				print(i)
	
	def max_real_braking_force_rr(self, status):
		out = self.max_potential_braking_torque_rr(0)
		for i in range(0, len(out)):
			if out[i] >= self.tbb:
				out[i] = self.tbb / self.r
			elif out[i] <= 0:
				out[i] = 0
			else:
				out[i] = out[i] / self.r

		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_show(self.d, out, 'distance from rear axle [m]', 'max braking force without tire-slip on rear axle [N]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'max braking force without tire-slip on rear axle [N]', 'max_braking_force_rear.jpg')
		elif status == 3:
			for i in out:
				print(i)

	def max_real_braking_force_net(self, status):
		out = self.max_real_braking_force_fr(0) + self. max_real_braking_force_rr(0)	
		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_show(self.d, out, 'distance from rear axle [m]', 'max braking torque without tire-slip on rear axle [N]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'max braking torque without tire-slip on rear axle [N]', 'max_braking_torque_rear.jpg')
		elif status == 3:
			for i in out:
				print(i)

	def deceleration(self, status):
		out = self.max_real_braking_force_net(0) / self.m
		if status == 0:
			return out
		elif status == 1:
			self.plot_graph_show(self.d, out, 'distance from rear axle [m]', 'deceleration [m/s^2]')
		elif status == 2:
			self.plot_graph_save(self.d, out, 'distance from rear axle [m]', 'max braking torque without tire-slip on rear axle [N]', 'max_braking_torque_rear.jpg')
		elif status == 3:
			for i in out:
				print(i)

if __name__ == "__main__":
	bike = Bicycle(1.2, 0.8, 0.36, 69.9, 62.3, 0.8, 85, 5)
	bike.max_real_braking_force_fr(1)
	bike.max_real_braking_force_rr(1)
	bike.max_real_braking_force_net(1)
	bike.deceleration(1)
