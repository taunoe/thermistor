#include <Arduino.h>
/********************************************************************
 * Tauno Erik
 * 11.10.2020 
 * https://taunoerik.art/
 * https://github.com/taunoe/thermistor
 * 
 * TODO:
 *  - replase delays with millis()
 ********************************************************************/

/******************************************************************** 
 * 7-segment LED:
 *  |--A--|
 *  F     B
 *  |--G--|
 *  E     C
 *  |--D--|   
 *          dp
 *         
 *  GF+AB
 *    #
 *  ED+Csp
 *
 *  
 *  0 - High! (Common anode!)
 *  1 - Low
 ********************************************************************/

// Enable debug info Serial print
#define DEBUG
#ifdef DEBUG
  #define DEBUG_PRINT(x)  Serial.print(x)
  #define DEBUG_PRINTLN(x)  Serial.println(x)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
#endif

/* Pins */
const int LATCH_PIN = 8;
const int DATA_PIN = 11;
const int CLOCK_PIN = 12;
const int THERMISTOR_PIN = A0;

const int INTERVAL = 500; // delay

/********************************************************************/

// https://protosupplies.com/product/thermistor-temp-sensor-module/
// https://www.thinksrs.com/downloads/programs/therm%20calc/ntccalibrator/ntccalculator.html

namespace sensor{

  /* 
   * Function to read and calculate tempearure.
   * Algoritm: Beta model equation
   */
  float read_beta(int pin = THERMISTOR_PIN) {
    
    const double RESISTOR   = 9820.0;  // Measured value of on-board divider resistor
    const double BETA       = 4346.83; //4242.0; // Beta value (from datasheet or calculated)
    const double ROOM_TEMP  = 296.15;  //=23C, 19,6C=292.75;   // room ambient temperature in Kelvin
    const double THERMISTOR = 9670.0;  // Measured value of thermistor at room temp
           
    int raw_reading = analogRead(pin);  // ADC measurement
    // Thermistor current resistance value:
    double thermistor = RESISTOR * ( (1023.0 / raw_reading) - 1);
    double kelvin = (BETA * ROOM_TEMP) / (BETA + 
                    (ROOM_TEMP * log(thermistor / THERMISTOR)));
    double celsius = kelvin - 273.15;
    return celsius;
  }

  /*
   * Function to read and calculate tempearure.
   * Algoritm: Steinhart-hart equation 
   */
  float read(int pin = THERMISTOR_PIN) {
    // Steinhart-hart coeficients:
    const float c1 = 0.001129148;       // 0.001129148
    const float c2 = 0.000234125;       // 0.000234125
    const float c3 = 0.0000000876741;   // 0.0000000876741
    const float resistor = 10000.0;     // On board resistor 10K

    int raw_reading = analogRead(pin);  // ADC measurement
    // Resistance on thermistor:
    float thermistor = resistor * (1023.0 / (float)raw_reading - 1.0);
    float logR2 = log(thermistor);
    float kelvin = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
    float celcius = kelvin - 273.15;
    //float farenheit = (celcius * 9.0)/ 5.0 + 32.0; 
    return celcius;
  }

} // sensor namespace end



/********************************************************************/
namespace display {

  /* Defined numbers */
  uint8_t numbers[10][2] = {
    {0b00000111, 0b00001110}, // 0
    {0b00000001, 0b00000010}, // 1
    {0b00001011, 0b00001100}, // 2
    {0b00001011, 0b00000110}, // 3
    {0b00001101, 0b00000010}, // 4
    {0b00001110, 0b00000110}, // 5
    {0b00001110, 0b00001110}, // 6
    {0b00000011, 0b00000010}, // 7
    {0b00001111, 0b00001110}, // 8
    {0b00001111, 0b00000110}  // 9
  };

  // Error message
  uint8_t error[2] = {0b10101010, 0b01000100 };

  /*
   * Function to shift number out.
   * Input is array.
   * Example array: int zero[2] = { 0b00000111, 0b00001110};
   * Usage: shift_to_7seg(zero);
   */
  void shift_to_7seg(uint8_t *num) {
 
    digitalWrite(LATCH_PIN, LOW);
    for (size_t i = 0; i < 2; i++) {
      // MSBFIRST - Most Significant Bit First
      // LSBFIRST - Least Significant Bit First
      shiftOut(DATA_PIN, CLOCK_PIN, LSBFIRST, ~(num[i]));
    }
    digitalWrite(LATCH_PIN, HIGH);
  }


  /*
   * Helper function for animations
   */
  void shift_frame( uint8_t a, uint8_t b){
    uint8_t pattern[2] = { a, b};
    shift_to_7seg(pattern);
  }

  /*
   * Function to display animation: triibud.
   * Param int speed == delay time. Higher == slower 
   */
  void animation_triibud(int speed = 40){
    uint8_t pattern[2] = { 0b00000001, 0b00000010};
    //DEBUG_PRINT(pattern[0]);DEBUG_PRINT(", ");DEBUG_PRINTLN(pattern[1]);
    for (uint8_t i = 0; i < 4; i++)
    {
      shift_to_7seg(pattern);
      pattern[0] = pattern[0] << 2;
      pattern[1] = pattern[1] << 2;
      delay(speed);
    }
      shift_frame(0b00010000, 0b00100000);
      delay(speed);
 
      shift_frame(0b00000100, 0b00001000);
      delay(speed);

      shift_frame(0b00000001, 0b00000010);
      delay(speed);
  }

  /*
   * Function to display animation:  
   */
  void animation_snake(int speed = 30){
    shift_frame(0b00000000, 0b00000001);
    delay(speed);
    shift_frame(0b00000000, 0b00000100);
    delay(speed);
    shift_frame(0b00000000, 0b00001000);
    delay(speed);
    shift_frame(0b00001000, 0b00000000);
    delay(speed);
    shift_frame(0b00000001, 0b00000000);
    delay(speed);
    shift_frame(0b00000010, 0b00000000);
    delay(speed);
    shift_frame(0b00000100, 0b00000000);
    delay(speed);
    shift_frame(0b00001000, 0b00000000);
    delay(speed);
    shift_frame(0b00000000, 0b00000010);
    delay(speed);
    shift_frame(0b00000000, 0b00000100);
    delay(speed);
    shift_frame(0b00000000, 0b00010000);
    delay(speed);
    shift_frame(0b00000000, 0b00100000);
    delay(speed);
    shift_frame(0b10000000, 0b00000000);
    delay(speed);
    shift_frame(0b01000000, 0b00000000);
    delay(speed);
    shift_frame(0b00100000, 0b00000000);
    delay(speed);
    shift_frame(0b10000000, 0b00000000);
    delay(speed);
    shift_frame(0b00000000, 0b10000000);
    delay(speed);
    shift_frame(0b00000000, 0b01000000);
    delay(speed);
    shift_frame(0b00000000, 0b00010000);
    delay(speed);
    shift_frame(0b00000000, 0b00000100);
    delay(speed);
    shift_frame(0b00000000, 0b00000001);
    delay(speed);
  }



  /* To store number what is on display */
  uint8_t old_num = 0;

  /*
   * Fuction to display number.
   * Input number 0 - 99
   * Shifts out number only when it is changed
   */
  void write_number(uint8_t num) {

    // When we convert decimal number (10-99) to binary we store it here
    uint8_t new_number[2] = {0}; 

    // We shift it out only when a number has changed.
    if (num != old_num) {
      //animation_triibud();
      animation_snake();
      // If number is 0-9:
      if (num < 10) {
        shift_to_7seg(numbers[num]);
      }
      // If number is 10-99:
      else if (num > 9 and num < 100) {
        // Spli the number.
        // e.g if we have 58
        // then 5 and 8
        uint8_t tens = (num/10) % 10;
        uint8_t ones = num % 10;

        // combine two binaries
        for (uint8_t i = 0; i < 2; i++) {
          new_number[i] = numbers[tens][i]<<4 | numbers[ones][i];
        }
        shift_to_7seg(new_number);
      }
      // If number is higher than 99:
      else {
        shift_to_7seg(error);
      }

    }
    old_num = num;
  }


} // display namespace end



/********************************************************************/


void setup() {
  Serial.begin(9600);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  // TODO: animation
}

void loop() {

  float temp = sensor::read();
  float temp_beta = sensor::read_beta();

  DEBUG_PRINT("Steinhart: "); 
  DEBUG_PRINT(temp);

  DEBUG_PRINT(" Beta method: "); 
  DEBUG_PRINT(temp_beta);

  float average = (temp+temp_beta)/2;

  DEBUG_PRINT(" Average: "); 
  DEBUG_PRINT(average);
  DEBUG_PRINTLN(" C");  

  display::write_number((int)average); // Convert float to int. so our func. can use it

  delay(INTERVAL);
  
}