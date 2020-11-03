function out = force_dynamic_front(distance, height, length, mass, braking_force)
   g = 9.81;
   out = (mass * g * distance + braking_force * height) / length;
end
