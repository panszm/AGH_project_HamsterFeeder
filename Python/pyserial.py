import bt_api


bt_serial = bt_api.BTConn('COM9')
while True:
    print(bt_serial.get_pressure())
    steps_to_rotate = int(input("Input steps to rotate: "))
    bt_serial.rotate_stepper(steps_to_rotate)
    