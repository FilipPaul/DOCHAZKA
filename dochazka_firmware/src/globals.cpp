#include "globals.h"
uint8_t btn_array[] = {PIN_PRICHOD,PIN_ODCHOD,PIN_ODCHOD_OBED,PIN_ODCHOD_PRAC_CESTA,PIN_ODCHOD_DOKTOR};
const char *btn_states[] ={"Prichod","Odchod","Doktor" ,"Prac. Cesta", "Obed"};
uint8_t total_number_of_employes;
uint8_t number_of_present_employes;
uint32_t global_last_log_ID;
volatile uint8_t get_time_flag = 0;
volatile uint32_t one_second_tick = 0;
volatile uint32_t ms_tick = 0;
char paths[ARRAYSIZE_1][ARRAYSIZE_2];
uint8_t slider_value;
char global_date_time[20] = "00.00.0000 00:00:00";
hw_timer_t * timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;
LiquidCrystal_I2C lcd(0x27,2,1,0,4,5,6,7);  // Set the LCD I2C address
String JSON_string_output = "";
DynamicJsonDocument doc(6144);
empl_data EMPLOY;
AsyncWebServer myAsyncServer(80);
RTC_DS3231 rtc;
SPIClass spiSD(HSPI);
WebSocketsServer MyWebSocket = WebSocketsServer(1337);
MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance
char init_file_string[] = "--------------------------------------------------"
        "NEMAZAT!!!! V tomto souboru jsou uloženy logy. Tento řádek je automaticky generován a slouží pro inicializaci programu - NEMAZAT!!!!!!"
        "---------------------------------------------------------------------------\n";
