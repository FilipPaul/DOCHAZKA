#include "my_main_program_functions.h"
#include "SD.h"
#include "SDcardCommands.h"
#include "myRTCfunc.h"

void setState(uint8_t *state_variable, uint8_t enum_state, uint8_t update_display){
  *state_variable = enum_state;
  digitalWrite(GREEN_LED, LOW);
  if(update_display){
    switch (enum_state)
    {
    case STATE_PRESS_BUTTON:
      lcd.setCursor(0,2);
      lcd.print("Stisknete tlacitko  ");
      lcd.setCursor(0,3);
      lcd.printf("Pritomno: %2u/%2u     ",number_of_present_employes,total_number_of_employes);
      digitalWrite(RED_LED, LOW);
      digitalWrite(BUZZER, LOW);

      break;
    case STATE_INSERT_RFID_TAG:
        lcd.setCursor(0,2);
        lcd.print("Prilozte cip        ");
        lcd.setCursor(0,3);
        lcd.print("                    ");
        lcd.setCursor(0,3);
        lcd.print(EMPLOY.state);
      break;
    
    case STATE_SAVE_DATA:
    break;

    case STATE_SDCARD_ERROR:
        lcd.setCursor(0,2);
        lcd.print("SD karta neodpovida ");
        lcd.setCursor(0,3);
        lcd.print("                    ");
    break;
    
    default:
      break;
    }

  }
}

void UpdateAllTimes(){
    char buffer[50];
    char date_format[] = "DD.MM.YYYY";
    DateTime currnt_date_time = rtc.now();
    sprintf(buffer,"datum: %s  ",currnt_date_time.toString(date_format));
    lcd.setCursor(0,0);
    lcd.print(buffer);
    char time_format[] = "hh:mm:ss";
    sprintf(buffer,"cas: %s   ",currnt_date_time.toString(time_format));
    lcd.setCursor(0,1);
    lcd.print(buffer);
    char date_time_format[] = "DD.MM.YYYY hh:mm:ss";
    strcpy(global_date_time,currnt_date_time.toString(date_time_format));
    sprintf(buffer,"CURRENT_TIME*%s*",global_date_time);
    MyWebSocket.broadcastTXT(buffer);
}

uint16_t getTotalNumberOfEmployes(char paths_string_array[ARRAYSIZE_1][ARRAYSIZE_2]){
  static uint16_t result = 0;

  if (!SD.exists("/tags.txt")){
      Serial.println("FILE DOESNT EXIST !!");
      return 0;
    }

  File file = SD.open("/tags.txt");
  if(!file){
      Serial.println("Failed to open file for reading");
      return 0;
  }

  result = 0;
  while(file.available()){

      static char line[260];
      static char *command;
      static char first_name[] = "init_value_long_enought_to_store_name_a";
      static char second_name[] = "init_value_long_enought_to_store_name_a";
      file.readBytesUntil('\n',line,260);
      command = strtok((char *)line, ";");
      command = strtok(NULL,";");
      strcpy(first_name,command);
      command = strtok(NULL,";");
      strcpy(second_name,command);
      char buffer[ARRAYSIZE_1];
      strcpy(buffer,"EMPTY THIS STRING");
      sprintf(buffer,"/%s_%s.txt",first_name,second_name);
      strcpy(paths_string_array[result],buffer);
      result++;
      } 
  
  file.close();
  return result;
}

void get_JSON_MainPageStatus_string(String *JSON_string_output){
    //JSON STRING
    doc.clear();
    *JSON_string_output = "";
    JsonObject json_slider_obj = doc.createNestedObject("slider");
    JsonObject json_date_time_obj = doc.createNestedObject("date_time");
    JsonObject json_connected_client_obj = doc.createNestedObject("connected_client");
    JsonArray json_employ_array = doc.createNestedArray("employees");
    JsonObject json_employ_obj = json_employ_array.createNestedObject();
    json_employ_array.clear();
    json_connected_client_obj["local_IP"] = "THIS IP";
    json_connected_client_obj["number"] = 2;

    json_date_time_obj["date"] = "01.02.1920";
    json_date_time_obj["time"] = "12:12";

    json_slider_obj["value"] = slider_value;

    uint16_t num_of_lines;
    num_of_lines = getTotalNumberOfEmployes(paths);
    number_of_present_employes = 0;
    total_number_of_employes = num_of_lines;
    for (uint16_t i = 0; i < num_of_lines; i++)
    {
      if (!SD.exists(paths[i])){
        SD_writeFile(SD,paths[i],init_file_string);
        char path[ARRAYSIZE_2];
        strcpy(path,paths[i]);
        Serial.println(path);
        Serial.println(paths[i]);
        myAsyncServer.on(path, HTTP_GET,  [path] (AsyncWebServerRequest *request) {
            IPAddress remote_IP = request->client()->remoteIP();
            Serial.println("PATH IN FUN");
            Serial.println(path);
            request->send(SD, path, "text/html");
        }
        );


      }
      File file = SD.open(paths[i]);
      if(!file){
          Serial.println("Failed to open file for reading");
          return;
      }

      if( file.size() < 270 ){
        char *command;
        command = strtok((char *)paths[i], "_");//logID
        char *p = &command[1];
        json_employ_obj["first_name"] =  p;
        command = strtok(NULL,"");
        command[strlen(command) - 4] = '\0';
        json_employ_obj["second_name"] = command;
        json_employ_obj["date_time"] = "UNKNOWN";
        json_employ_obj["state"] = "UNKNOWN";
        json_employ_array.add(json_employ_obj);
        continue;
      }

      char line[270];
      while(file.available()){
        file.readBytesUntil('\n',line,270);//last line
      }
      file.close();
      char *command;
      command = strtok((char *)line, ";");//logID
      command = strtok(NULL,";");//logID_value
      json_employ_obj["log_ID"] =  command;
      command = strtok(NULL,";"); //Jmeno
      command = strtok(NULL,";"); //Jmeno value
      json_employ_obj["first_name"] =  command;
      command = strtok(NULL,";"); //Prijmeni
      command = strtok(NULL,";"); //Prijmeni Value
      json_employ_obj["second_name"] = command;
      command = strtok(NULL,";"); //TAG
      command = strtok(NULL,";"); //TAGVALUE
      json_employ_obj["TAG"] = command;
      command = strtok(NULL,";"); //STAV
      command = strtok(NULL,";"); //STAV_VALUE
      json_employ_obj["state"] = command;
      if(strcmp(command,"Prichod")== 0){
        number_of_present_employes++;
      }
      command = strtok(NULL,";"); //SAVED_TIME
      command = strtok(NULL,";"); //SAVED_TIME_value
      json_employ_obj["date_time"] = command;     
      json_employ_array.add(json_employ_obj);
    }
    serializeJsonPretty(doc,*JSON_string_output);
}

uint8_t compareRFIDwithSD(uint8_t TagID[], uint8_t ID_size){

  //RESET employ Class
  EMPLOY.TAG_size = 10;
  for (uint8_t i = 0; i < EMPLOY.TAG_size; i++)
  {
    EMPLOY.TAG_ID[i] = 0xff;
  }
  strcpy(EMPLOY.TAG_ID_string, "UNKNOWN");
  strcpy(EMPLOY.First_name, "UNKNOWN");
  strcpy(EMPLOY.Second_name, "UNKNOWN");

  char help_str[8];
  char id_string[20];
  strcpy(id_string,"");//init result string

  for (size_t i = 0; i < ID_size ; i++){
    //make string from byte array

    EMPLOY.TAG_ID[i] = TagID[i];
    if (i == ID_size -1){ //remove last space
      sprintf(help_str,"%02X", TagID[i]);
    }
    else{
      sprintf(help_str,"%02X ", TagID[i]);
    }

    strcat(id_string, help_str);
  }
  //Compare string from bytearray with SAVED IDS ate SD CARD
  File file = SD.open("/tags.txt");
  if(!file){
      Serial.println("Failed to open file for reading");
      return 0;
    }

    //Serial.print("Read from file: ");
    while(file.available()){
        char line[150];
        file.readBytesUntil('\n',line,150);
        char *command;
        command = strtok((char *)line, ";");
        if(!strcmp(command,id_string)){
          command = strtok(NULL,";");
          strcpy(EMPLOY.First_name,command);
          command = strtok(NULL,";");
          strcpy(EMPLOY.Second_name, command);
          strcpy(EMPLOY.TAG_ID_string ,id_string);
          command = strtok(NULL,";");
          strcpy(EMPLOY.sound, command);

          file.close();
          return 1;
        }
    }
    file.close();
  return 0;
}

void customPrint(uint8_t id)
{
  Serial.printf("Scanned number %u", id);
}

uint8_t scanButtonMatrix(char pressed_btn[],uint8_t btn_array[], const char* btn_states[],uint8_t arrSize)
{
    strcpy(pressed_btn,"");
    for (uint8_t i = 0; i < arrSize; i++)
    {
        if (0 == digitalRead(btn_array[i])){
        //Serial.printf("PRESSED Button PIN: %u DIGITAL READ: %u ; HAS state %s\n", btn_array[i], digitalRead(btn_array[i]),btn_states[i]);
        strcpy(pressed_btn, btn_states[i]);
        return 1;
    }
  }
  //Serial.println("Nothing pressed!");
  return 0;
}

