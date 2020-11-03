function out = max_braking_force(mass, friction_coefficient)
    out = mass .* friction_coefficient .* 9.81;
end
