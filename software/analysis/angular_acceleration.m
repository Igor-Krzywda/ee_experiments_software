function out = angular_acceleration(distance, height, length, mass, braking_force)
    g = 9.81;
    R = length - distance;
    force_rear = force_dynamic_rear(distance, height, length, mass, braking_force);
    torque = angular_acceleration_torque(force_rear, length);
    moment_of_inertia = moment_of_inertia(R, mass);
    out = torque ./ moment_of_inertia;
end
