ampy --port /dev/ttyACM0 run ShakeDice.py && raspistill -w 100 -h 100 -o test.jpg -rot 270 && python pi_infer.py
