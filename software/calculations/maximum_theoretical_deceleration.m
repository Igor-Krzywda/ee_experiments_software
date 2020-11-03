function out = maximum_theoretical_deceleration(d, height, length, mass, friction_coefficient)
    R = length - d;
    max_force = -1 .* force_from_angular_acceleration(0.01, mass, d, R, height);
    out = max_force ./ mass;
end
