1;

l = 1.1;        %length of the bike
l_f = 0.72;     %length of the fork
h_0 = 71.5;     %head angle 

l_s = 0.43;     %seattube length
s_0 = 73;       %seattube angle
offset = 0.2;   %centre of mass offset

h_c = 0.9;      %croutch height

m = 85;         %mass of the rider + the bike
m_1 = 100;
m_2 = 60;
u = 0.8;        %friction coefficient
u_1 = 0.6;
u_2 = 0.3;



range_h = effective_horizontal_range(l, l_f, h_0);
h_min = minimum_ride_height(l_s, s_0, offset);
h_ped = pedalling_ride_height(h_c, offset);
f_max = max_braking_force(m, u);

h_avg = (h_min + h_ped) ./ 2;
h_max = (h_ped + 0.2);

d = [0 : 0.01 : range_h];    %range of movement of the cyclist

hold on;
plot(d, maximum_theoretical_deceleration(d, h_min, l, m, u), "-k");
plot(d, maximum_real_deceleration(d, h_min, l, m, u), "-r");
plot(d, maximum_real_deceleration(d, h_avg, l, m_1, u), "-b");
plot(d, maximum_real_deceleration(d, h_max, l, m_2, u), "-m");
legend("maximum deceleration", "85kg", "100kg", "60kg");
xlabel("distance from rear axle [m]");
ylabel("maximum deceleration [^m/_{s^2}]");
grid on;
hold off;
