function out = angular_acceleration_torque(force_rear, length)
    out = force_rear .* length;
end
