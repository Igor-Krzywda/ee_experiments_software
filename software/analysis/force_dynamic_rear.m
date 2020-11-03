function out = force_dynamic_rear(distance, height, length, mass, braking_force)
    g = 9.81;
    out = mass * g - force_dynamic_front(distance, height, length, mass, braking_force);
end
