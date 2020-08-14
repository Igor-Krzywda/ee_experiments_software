cmpl-w:
	arduino-cli compile --fqbn arduino:avr:uno weight_distribution_unit --verbose
upld-w:
	arduino-cli upload --port /dev/ttyACM0 --fqbn arduino:avr:uno weight_distribution_unit --verbose
acc-w:
	arduino-cli compile --fqbn arduino:avr:uno accelerometer_unit --verbose
upld-w:
	arduino-cli upload --port /dev/ttyACM0 --fqbn arduino:avr:uno accelerometer_unit --verbose
