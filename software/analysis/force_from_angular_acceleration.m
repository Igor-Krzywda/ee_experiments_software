function out = force_from_angular_acceleration(angular_acceleration, mass, distance, r, height)
    g = 9.81
    out = (angular_acceleration .* mass .* r .^ 2 + mass .* g .* distance - mass .* g) ./ height; 
end
