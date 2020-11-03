function out = maximum_real_deceleration(distance, height, length, mass, friction_coefficient)
    max_braking_force = 9.81 .* mass .* friction_coefficient;
    deceleration = maximum_theoretical_deceleration(distance, height, mass, 0.8);
    force_rear = force_dynamic_rear(distance, height, length, mass, max_braking_force)
    out = max_braking_force ./ 85 + distance .* 0;
end
