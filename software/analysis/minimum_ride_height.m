function out = minimum_ride_height(seat_tube_length, seat_tube_angle, offset)
    out = seat_tube_length .* sin(seat_tube_angle .* pi ./ 180) + offset;
end
