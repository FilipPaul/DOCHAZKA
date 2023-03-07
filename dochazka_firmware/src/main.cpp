/*
PINOUT:
RFID (SPI) --> SCK(18) MISO(19) MOSI(23) SS(5) RST(17)
note SS pins in labeled SDA

SD CARD SPI --> SCK(14) MISO(16) MOSI(15) SS(13)
has broken module therefore need its own SPI BUS.. 

RTC MODULE (I2C) -->  SDA(21) SCL(22)

ENCODER: CH_A(2), CH_B(4), BTN(35)

BUTTONS: PRICHOD(27), ODCHOD(26), ODCHOD_OBED(32), ODCHOD_PRAC_CESTA(33), ODCHOD_DOKTOR(25) 
*/
#include <AsyncElegantOTA.h>
#include "globals.h"
#include <ESP32Encoder.h>
ESP32Encoder encoder;

void IRAM_ATTR onTimer() {
  ms_tick++;
  if(ms_tick % 1000 == 0){
    one_second_tick++;
    get_time_flag = 1;
  }

}


void callBackForEncoder(int8_t current_value){
  if(current_value > 0){
    Serial.println("left");
    if (slider_value > 0){
      slider_value--; 
    }
       
  }
  if(current_value < 0){
    Serial.println("right");
    if (slider_value < 255){
      slider_value++;
    }

  }
  char buffer[18];
  sprintf(buffer,"SLIDERVALUE*%u*",slider_value);
  MyWebSocket.broadcastTXT(buffer);
}

void setup()
{

  //-----------------------------BUTTONS------------------------------------------
  for (uint8_t i = 0; i < sizeof(btn_array); i++)
  {
    pinMode(btn_array[i],INPUT_PULLUP);
  }
  
    //------------------------------------------SERIAL SETTINGS----------------------------------------
  Serial.begin(115200);              // Initialize serial communications with the PC
    //------------------------------------------RTC SETTINGS ----------------------------------------
    Serial.println("OOTA UPDATED");
  if(!rtc.begin()) {
        Serial.println("Couldn't find RTC!");
        Serial.flush();
    }


  if(rtc.lostPower()) {
      // this will adjust to the date and time at compilation
      Serial.println("Power unexpected shutdown");
      //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  //we don't need the 32K Pin, so disable it
  rtc.disable32K();

  //DISABLE SQW pin
  rtc.writeSqwPinMode(DS3231_OFF);
  
  //////////////////////////-----------------"LCD---------------------"
   lcd.begin (20,4); // 16 x 2 LCD module
   lcd.setBacklightPin(3,POSITIVE); // BL, BL_POL
   lcd.setBacklight(HIGH);
   lcd.print("inicializace systemu");


  //------------------------------------------SD card system----------------------------------------
  lcd.setCursor(0,1);
  lcd.print("SD card settings"); 
  spiSD.begin(14,16,15,SD_CS);//SCK,MISO,MOSI,ss
  while(!SD.begin( SD_CS, spiSD, SDSPEED)){
    static uint8_t trial = 0;
    delay(100);
    if(++trial >20){
      Serial.println("Card Mount Failed");
      ESP.restart();
    };
  }

/*
SD_writeFile(SD, "/tags.txt", "EA 5D CB 62;Lukas;Bartosek;NONE;\n\
5A 45 BE 62;Milan;Brzy;NONE;\n\
1A 30 66 62;Pavel;Ceresnik;NONE;\n\
0A 35 A3 62;Radomil;Havlin;NONE;\n\
AA 42 C7 62;Josef;Hladky;NONE;\n\
5A F0 C1 62;Ludek;Hladky;NONE;\n\
AA 68 D0 62;Ondrej;Hutter;duhova_vila.mp3;\n\
EA 29 C6 62;Filip;Paul;imperial-march-ringtone.mp3;\n\
2A B9 CD 62;Ludek;Janderka;NONE;\n\
D9 F6 30 A4;Robert;Kazda;NONE;\n\
AA 34 9F 61;Josef;Kopriva;NONE;\n\
9A 77 9D 62;Martin;Petr;NONE;\n\
6A B7 9D 62;Lubomir;Petrik;NONE;\n\
EA 7F C2 62;Petra;Spacilova;NONE;\n\
CA 66 D5 62;Ondrej;Vainlich;NONE;\n");
*/
  
  //------------------------------------------RFID SETTINGS ----------------------------------------
  lcd.setCursor(0,1);
  lcd.print("RFID settings");
  SPI.begin(18,19,23,17);            // Init SPI bus
  mfrc522.PCD_Init();                // Init MFRC522
  delay(4);                          // Optional delay. Some board do need more time after init to be ready, see Readme
  mfrc522.PCD_DumpVersionToSerial(); // Show details of PCD - MFRC522 Card Reader details

  //------------------------------------------WIFI SETTINGS ----------------------------------------
  // Set your Static IP address
  lcd.setCursor(0,1);
  lcd.print("Connecting to Wifi");

  IPAddress local_IP(192, 168, 1, 144);
  // Set your Gateway IP address
  IPAddress gateway(192, 168, 1, 1);

  IPAddress subnet(255, 255, 255, 0);
  IPAddress primaryDNS(8, 8, 8, 8);   // optional
  IPAddress secondaryDNS(8, 8, 4, 4); // optional

  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS))
  {
    Serial.println("STA Failed to configure");
  }

  WiFi.begin(mySSID, myPASSWORD);

  ////Serial.printf("Soft AP is running at IP\n %s \n",WiFi.softAPIP().toString().c_str());
  Serial.println("connecting to the Wifi");
  lcd.setCursor(0,2);
  while (WiFi.status() != WL_CONNECTED)
  {
    static uint8_t timeout;
    delay(500);
    Serial.print(".");
    lcd.print(".");
    timeout++;
    if (timeout > 30)
    {
      Serial.println("Connection Failed.");
      WiFi.disconnect();
      WiFi.softAP("CEVOR_DOCHAZKA", "12345678");
      break;
      //ESP.restart();
    }
  }
  delay(2000);
  lcd.setCursor(0,1);
  lcd.print("                   ");

  Serial.println("Succesfully connected to the WiFi");
  Serial.println("IP addres is:");
  Serial.println(WiFi.localIP());


  //------------------------------------------SERVER SETTINGS ----------------------------------------

  lcd.setCursor(0,1);
  lcd.print("SERVER SETTINGS");
  AsyncElegantOTA.begin(&myAsyncServer); // Start ElegantOTA

  // ASING callback for async WS:
  myAsyncServer.on("/", HTTP_GET, onIndexRequest);
  myAsyncServer.on("/styles.css", HTTP_GET, onCssRequest);
  myAsyncServer.on("/app.js", HTTP_GET, onJavaRequest);
  myAsyncServer.on("/tags", HTTP_GET, []  (AsyncWebServerRequest *request) {
            IPAddress remote_IP = request->client()->remoteIP();
            request->send(SD, "/tags.txt", "text");
        });
  myAsyncServer.on("/test", HTTP_GET, []  (AsyncWebServerRequest *request) {
            IPAddress remote_IP = request->client()->remoteIP();
            request->send(SD, "/test.txt", "text");
        });
  myAsyncServer.on("/logs", HTTP_GET, []  (AsyncWebServerRequest *request) {
            IPAddress remote_IP = request->client()->remoteIP();
            request->send(SD, "/logs.txt", "text");
        });
  //myAsyncServer.on("/sound", HTTP_GET, onCssRequest);
  myAsyncServer.onNotFound(onPageNotFoundRequest);
    uint16_t num_of_lines;
    num_of_lines = getTotalNumberOfEmployes(paths);
    total_number_of_employes = num_of_lines;
    for (uint16_t i = 0; i < num_of_lines; i++)
    {
        char path[ARRAYSIZE_2];
        strcpy(path,paths[i]);
        Serial.println(path);
        Serial.println(paths[i]);
        myAsyncServer.on(path, HTTP_GET,  [path] (AsyncWebServerRequest *request) {
            IPAddress remote_IP = request->client()->remoteIP();
            Serial.println("PATH IN FUN");
            Serial.println(path);
            request->send(SD, path, "text");
        }
        );
    }

  myAsyncServer.begin();

  

  // start webserver and asign callback:
  MyWebSocket.begin();
  MyWebSocket.onEvent(WebSocketCallback);


lcd.setCursor(0,0);
lcd.print("datum: CHYBA        ");

lcd.setCursor(0,1);
lcd.print("cas:   CHYBA        ");

lcd.setCursor(0,2);
lcd.print("Stisknete tlacitko  ");

lcd.setCursor(0,3);
lcd.print("Pritomno: XX/");
lcd.print(total_number_of_employes);
lcd.print("      ");

//---------------------------------------ENCODER SETTINGS------------------------
	// Enable the weak pull up resistors
	ESP32Encoder::useInternalWeakPullResistors=UP;
	// use pin 19 and 18 for the first encoder
  encoder.attachFullQuad(27,32);
	// set starting count value after attaching
	encoder.setCount(0);

  //ENCODER button
  pinMode(26,INPUT);//this pin has no internal pullup.. external pullup needed

//PERIPH SETTINGS ---------------------------------------
pinMode(BUZZER,OUTPUT);
pinMode(GREEN_LED,OUTPUT);
pinMode(RED_LED,OUTPUT);
digitalWrite(GREEN_LED, LOW);
digitalWrite(RED_LED, LOW);
digitalWrite(BUZZER, LOW);
//-----------------------------------------------timer settings-----------------------------------------:
timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &onTimer, true);
  timerAlarmWrite(timer, 1000, true);
  timerAlarmEnable(timer);


delay(200);//time to initialize SD card,etc..
}

void loop()
{
  static uint8_t timeout_insert_tag_flag;
  static uint8_t lcd_backlight_flag = 1;
  static uint32_t one_second_compare_time = one_second_tick;
  static uint32_t ms_compare_time = ms_tick;
  static uint8_t state = STATE_PRESS_BUTTON;
  static int32_t current_encoder_value;
  static uint8_t encoder_flag;
  static uint8_t encoder_button_flag;

  current_encoder_value = encoder.getCount();
  if ( (current_encoder_value != 0) && (encoder_flag == 0) ){
    callBackForEncoder(current_encoder_value);
    encoder_flag = 1;
    ms_compare_time = ms_tick;
  }
  if( (!digitalRead(26)) && (encoder_button_flag == 0)){
      Serial.println("ENCODER BUTTON PRESED");
      slider_value = 100;
      MyWebSocket.broadcastTXT("SLIDERVALUE*100*");
      encoder_button_flag = 1;
      ms_compare_time = ms_tick;
  }

  if((encoder_button_flag == 1) && ( ms_tick > ms_compare_time +150)){
    if(digitalRead(26)){
      encoder_button_flag = 0;
    }
  }

  if((encoder_flag == 1) && ( ms_tick > ms_compare_time +80)){
    encoder.setCount(0);
    encoder_flag = 0;
  }

  MyWebSocket.loop();

  if(!SD.exists("/tags.txt") && (state != STATE_SDCARD_ERROR)){
    setState(&state,STATE_SDCARD_ERROR,1);
  }
  if(state == STATE_SDCARD_ERROR){
    SD.end();
    if(!SD.begin( SD_CS, spiSD, SDSPEED)){
      Serial.println("Card Mount Failed");
    }
    else{
      Serial.println("SD card succesfully reconnected");
      setState(&state,STATE_PRESS_BUTTON,1);
    }
      
  }

  if(get_time_flag != 0){
    UpdateAllTimes();
    get_time_flag = 0;
  }

  if ( (lcd_backlight_flag != 0 ) && (one_second_tick > one_second_compare_time+5)){
    lcd.setBacklight(LOW);
    lcd_backlight_flag = 0;
  }

  if (timeout_insert_tag_flag)
  {
    if (one_second_tick > one_second_compare_time+2)
    {
      mfrc522.PCD_Init();//reinit READER
      timeout_insert_tag_flag = 0;
      lcd_backlight_flag = 1;
      one_second_compare_time =  one_second_tick;
      Serial.println("state timeout, waiting for button press");
      setState(&state,STATE_PRESS_BUTTON,1);
    }
  }
  if (state == STATE_PRESS_BUTTON)
  {
    if (scanButtonMatrix(EMPLOY.state, btn_array, btn_states,sizeof(btn_array)))
      { 
        Serial.printf("\nstate is :%s Insert TAG\n",EMPLOY.state);
        lcd.setBacklight(HIGH);
        state = STATE_INSERT_RFID_TAG;
        timeout_insert_tag_flag = 1;
        one_second_compare_time = one_second_tick;
        setState(&state,STATE_INSERT_RFID_TAG,1);
      }
  }

  if (state == STATE_INSERT_RFID_TAG)
  {
    // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
    if ( ! mfrc522.PICC_IsNewCardPresent()) {
      return;
    }

    // Select one of the cards
    if ( ! mfrc522.PICC_ReadCardSerial()) {
      return;
    }

    mfrc522.PICC_HaltA();
    if(compareRFIDwithSD(mfrc522.uid.uidByte,mfrc522.uid.size)){
      lcd.setCursor(0,2);
      lcd.print("Probiha ukladani dat");
      lcd.setCursor(0,3);
      lcd.print("                   ");
      lcd.setCursor(0,3);
      lcd.print(EMPLOY.First_name);
      lcd.print(" ");
      lcd.print(EMPLOY.Second_name);
      timeout_insert_tag_flag = 0;
      setState(&state,STATE_SAVE_DATA,0);
    }
    else{
      lcd.setCursor(0,2);
      lcd.print("Neznamy cip        ");
      lcd.setCursor(0,3);
      lcd.print("Zkuste to znovu    ");
      Serial.println("Neznámý TAG, Prosím Načtěte tag znovu!");
      Serial.print("TAG ID: ");
      digitalWrite(RED_LED, HIGH);
      for (uint8_t i = 0; i < mfrc522.uid.size; i++)
      {
        Serial.print(mfrc522.uid.uidByte[i],HEX);
        Serial.print(" ");
      }
      Serial.println("");
      one_second_compare_time = one_second_tick;
    }
    
  }

  if (state == STATE_SAVE_DATA){


    //GET last log ID:
    static uint32_t LOG_ID = 0;
    if(!SD.exists("/logs.txt")){
      SD_writeFile(SD,"/logs.txt",init_file_string);
    }
    File file = SD.open("/logs.txt");
    if(!file){
        Serial.println("Failed to open file for reading");
        lcd.setCursor(0,2);
        lcd.print("Chyba pri ukladani  ");
        lcd.setCursor(0,3);
        lcd.print("Zkuste to znovu     ");
        digitalWrite(RED_LED, HIGH);
        setState(&state,STATE_PRESS_BUTTON,0);

        return;
    }
    if (LOG_ID== 0) {
      if (file.size()<290){
        Serial.println(file.size());
        LOG_ID = 1;
      }
      else{
        file.seek(file.size()-259);
        while(file.available()){
            char line[260];
            file.readBytesUntil('\n',line,260);
            char *command;
            command = strtok((char *)line, ";");
            if (!strcmp(command, "LOG_ID")){
              command = strtok(NULL,";");
              LOG_ID = atoi(command) + 1;
            } 
        }
      }
    }
    else{LOG_ID ++;}

    global_last_log_ID = LOG_ID;
    file.close();
    
    static char save_string[300];
    sprintf(save_string, "\nLOG_ID;%u;Jmeno;%s;Prijmeni;%s;TAG;%s;STAV;%s;SAVED_TIME;%s;EDIT;NONE;",\
      global_last_log_ID,EMPLOY.First_name, EMPLOY.Second_name ,EMPLOY.TAG_ID_string, EMPLOY.state, global_date_time);

    SD_appendFile(SD,"/logs.txt",save_string);

    static char save_path[100];
    sprintf(save_path,"/%s_%s.txt",EMPLOY.First_name,EMPLOY.Second_name);
    
    if(!SD.exists(save_path)){
      SD_writeFile(SD,save_path,init_file_string);
    }
    SD_appendFile(SD,save_path,save_string);

    //if (strcmp(EMPLOY.sound, "NONE") != 0){
    //  myAsyncServer.on("/sound", HTTP_GET,UpdateSoundPath);
    //  MyWebSocket.broadcastTXT("SOUND*");
    //}

    //MyWebSocket.broadcastTXT(JSON_string_output);
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(BUZZER, HIGH);
    //get_JSON_MainPageStatus_string(&JSON_string_output);
    delay(400);
    mfrc522.PCD_Init();//reinit READER
    lcd_backlight_flag = 1;
    one_second_compare_time = one_second_tick;
    setState(&state,STATE_PRESS_BUTTON,1);
  }    
  //delay(delay_cnt);
}
