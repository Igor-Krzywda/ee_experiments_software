#!/usr/bin/octave -fq

function static_wheel_loads
end function

function dynamic_wheel_loads
end function

function max_braking_torque

a = 5
g = 9.81
m = 70
l = 1.1
h = 0.8
u = 0.8
r = 0.36
tb = 62.13
tf = 69.9
x = 0:l

sff = ((l - x) * m * g) / l 	% force on front wheel (static)
sfr = m * g - sff				% force on rear wheel (static)
dff = ((l - x) * m * g + m * a * h) / l % reaction on front wheel (dyn)
dfb = m * g - dff				% reaction on rear wheel (dyn)
ptf = dff * u					% max torque on static friction (front)
ptb = dfb * u					% max torque on static friction (back)
max_braking_torque_f = ((ptf / tf) * tf) : tf 
max_braking_torque_b = ((ptb / tb) * tb) : tb

subplot(2,2,1)
plot(x,sff,x,sfr)
title("distance vs reaction on axles (no acceleration)")
legend("front wheel", "rear wheel")
xlabel("d [m]")
ylabel("F [N]")

subplot(2,2,2)
plot(x, dff, x, dfb)
title("distance vs reaction on axles (deceleration)")
legend("front wheel", "rear wheel")
xlabel("d [m]")
ylabel("T [Nm]")

subplot(2,2,3)
plot(x, max_braking_torque_f, x, max_braking_torque_b, x, max_net_braking_torque)
title("distance vs maximum torque with static friction (front wheel)")
legend("friction torque", "brake torque")
xlabel("d [m]")
ylabel("T [Nm]")

subplot(2,2,4)
plot(x, ptb, x, tb * ones(size(x)))
title("distance vs maximum torque with static friction (rear wheel)")
legend("friction torque", "brake torque")
xlabel("d [m]")
ylabel("T [Nm]")

