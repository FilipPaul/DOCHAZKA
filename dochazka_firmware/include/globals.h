#ifndef _GLOBALS_H
#define _GLOBALS_H
//DEFINES-------------------------------
#define SD_CS 13
#define SDSPEED 4000000

#define PIN_PRICHOD 33
#define PIN_ODCHOD 34
#define PIN_ODCHOD_OBED 35
#define PIN_ODCHOD_PRAC_CESTA 36
#define PIN_ODCHOD_DOKTOR 39

#define BUZZER 25

#define GREEN_LED 2
#define RED_LED 12

#define ARRAYSIZE_1 60
#define ARRAYSIZE_2 40

#define RST_PIN 17 // Configurable, see typical pin layout above
#define SS_PIN 5   // Configurable, see typical pin layout above
//Includes-------------------------------
#include <Arduino.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>
#include <ESPAsyncWebServer.h>
#include <RTClib.h>
#include <MFRC522.h>
#include <FS.h>
#include <SD.h>
#include <SPI.h>
#include <WebSocketsServer.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "credentials.h"

#include "myAsyncRequest.h"
#include "websocketCallback.h"
#include "my_main_program_functions.h"
#include "SDcardCommands.h"
#include "myRTCfunc.h"


struct empl_data{
  uint8_t TAG_size;
  uint8_t TAG_ID[10];
  char TAG_ID_string[20];
  char First_name[40];
  char Second_name[40];
  char state[40];
  char sound[60];
};

 enum
  {
    STATE_PRESS_BUTTON,
    STATE_INSERT_RFID_TAG,
    STATE_SAVE_DATA,
    STATE_SDCARD_ERROR
  };
extern uint32_t global_last_log_ID;
extern uint8_t total_number_of_employes;
extern uint8_t number_of_present_employes;
extern char global_date_time[20];
extern empl_data EMPLOY;
extern uint8_t btn_array[8];
extern const char *btn_states[8];
extern char paths[ARRAYSIZE_1][ARRAYSIZE_2];
extern hw_timer_t * timer;
extern portMUX_TYPE timerMux;
extern volatile uint32_t one_second_tick;
extern volatile uint32_t ms_tick;
extern volatile uint8_t get_time_flag;
extern String JSON_string_output;
extern DynamicJsonDocument doc;
extern LiquidCrystal_I2C lcd;  // Set the LCD I2C address
extern AsyncWebServer myAsyncServer;
extern RTC_DS3231 rtc;
extern SPIClass spiSD;
extern WebSocketsServer MyWebSocket;
extern MFRC522 mfrc522;
extern char init_file_string[267];
extern uint8_t slider_value;
#endif


