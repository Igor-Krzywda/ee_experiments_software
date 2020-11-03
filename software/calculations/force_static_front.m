function out = force_static_front(distance, length, mass)
    g = 9.81;
    out = (mass * g * distance) / length;
end
