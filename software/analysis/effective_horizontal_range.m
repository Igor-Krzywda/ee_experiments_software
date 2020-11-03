function out = effective_horizontal_range(bike_length, fork_length, head_angle)
    out = bike_length .- (fork_length * cos(head_angle .* pi ./ 180));
end
