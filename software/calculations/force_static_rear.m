function out = force_static_rear(distance, length, mass)
    g = 9.81;
    out = (mass * g) - force_static_front(distance, length, mass);
end
