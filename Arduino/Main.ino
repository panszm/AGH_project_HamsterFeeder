#include "BluetoothSerial.h"
#include "Stepper.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
const int stepsPerRevolution = 2037;
const int feedStep = stepsPerRevolution / 6;
Stepper myStepper = Stepper(stepsPerRevolution, 32, 33, 25, 26);
int res;
int feedCount;

void setup()
{
  analogReadResolution(10);
  myStepper.setSpeed(10);
  Serial.begin(115200);
  SerialBT.begin("PetFeeder");
  Serial.println("The device started, now you can pair it with bluetooth!");
}

void loop()
{
   if (SerialBT.available())
   {
     char command = SerialBT.read();
     Serial.println(command);
     switch (command)
     {
     case 's':
       res = analogRead(34) >> 2;
       SerialBT.write(res);
       Serial.println(res);
       break;
     default:
       feedCount = command;
       Serial.println(command);
       myStepper.step(feedStep * feedCount);
       SerialBT.write(0);
     }
   }
  delay(1000);
}
