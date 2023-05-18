from time import sleep
from datetime import datetime, timedelta
import pytz
import consts
import bt_api
import alert

bt_serial = bt_api.BTConn('COM9')

try:
    with open("pet_feeder_controller.log", "r") as file:
        last_line = file.readlines()[-1]
        last_timestamp = datetime.fromisoformat(last_line)
except:
     last_timestamp = None

log_file = open("pet_feeder_controller.log", "a")

while True:
    if last_timestamp is None or datetime.now() > last_timestamp + timedelta(hours=consts.FEEDING_INTERVAL_HOURS):
            print(f"{datetime.now().isoformat()} Feeding started")
            log_file.write(f"{datetime.now().isoformat()} Feeding started")
            log_file.flush()
            start_timestamp = datetime.now(tz=pytz.timezone("Europe/Warsaw"))

            food_left_at_start = bt_serial.get_food_left_in_grams()
            food_left = food_left_at_start
            while food_left_at_start - food_left <= consts.GRAMS_PER_FEEDING and not bt_serial.is_empty():
                 bt_serial.rotate_stepper(1)
                 food_left = bt_serial.get_food_left_in_grams()
            if bt_serial.is_empty():
                 alert.empty_warning()
            elif bt_serial.get_food_left_in_grams <= consts.ALERT_LEVEL_GRAMS:
                 alert.low_warning()
            seconds_passed = (datetime.now(tz=pytz.timezone("Europe/Warsaw")) - start_timestamp).total_seconds()
            log_file.write(f"Time passed: {seconds_passed}\n")
            log_file.write(f'{datetime.now().isoformat()}')
            print(f"Time passed: {seconds_passed}s\n")
            log_file.flush()
            
    sleep(consts.SCRIPT_INTERVAL_SECONDS)