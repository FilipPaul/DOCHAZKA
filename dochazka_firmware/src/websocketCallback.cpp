  #include "websocketCallback.h"
  void WebSocketCallback(uint8_t num,      // Number of clients connected
                       WStype_t type,    // type of message, error, text, disconnected, connetcted status etc..
                       uint8_t *payload, // raw data
                       size_t length)    // length of payload
{
  char buffer[300];
  // function body:
  // Figure out the type of WebSocket event
  switch (type)
  {
  // client disconnected
  case WStype_DISCONNECTED:
    // Serial.printf("[%u] Disconnected\n",num);
    break;
  // new client connected
  case WStype_CONNECTED:
  {
    // Serial.printf("[%u] Connected\n",num);
    IPAddress myIP = MyWebSocket.remoteIP(num);
    sprintf(buffer,"IP*%s*",MyWebSocket.remoteIP(num).toString().c_str());
    MyWebSocket.sendTXT(num,buffer);
    
    sprintf(buffer,"CLIENT_NUMBER*%u*",num);
    MyWebSocket.sendTXT(num,buffer);

    sprintf(buffer,"SLIDERVALUE*%u*NOT_YOUR_NUMBER*",slider_value);
    MyWebSocket.sendTXT(num, buffer);

    //get_JSON_MainPageStatus_string(&JSON_string_output);
    //MyWebSocket.sendTXT(num,JSON_string_output);
    // Serial.printf("[%u] New client connected at IP: %s\n",num,myIP.toString().c_str());
    break;
  }

  // Echo text message back to the client
  case WStype_TEXT:
  {

    char *command;
    command = strtok((char *)payload, "*");
    Serial.printf("tokanized command: %s\n", command);
    if (strcasecmp(command, "SLIDER") == 0)
    {
      command = strtok(NULL, "*");
      slider_value = atoi(command);
      sprintf(buffer,"SLIDERVALUE*%u*%u*",slider_value,num);

      
      MyWebSocket.broadcastTXT(buffer);
    }

    else if (strcasecmp(command, "GIMMEIP") == 0)
    {
      sprintf(buffer,"IP*%s*",MyWebSocket.remoteIP(num).toString().c_str());
      MyWebSocket.sendTXT(num,buffer);
    }

    else if (strcasecmp(command, "GIMMENUM") == 0)
    {
      sprintf(buffer,"CLIENT_NUMBER*%u*",num);
      MyWebSocket.sendTXT(num,buffer);
    }
    else if (strcasecmp(command, "GIMMELASTLOGID") == 0)
    {
      sprintf(buffer,"LASTLOGID*%u*",global_last_log_ID);
      MyWebSocket.sendTXT(num,buffer);
    }

        else if (strcasecmp(command, "GIMMEEMPLOYEECOUNT") == 0)
    {
      sprintf(buffer,"EMPLOYEECOUNT*%2u*%2u*",number_of_present_employes,total_number_of_employes);
      MyWebSocket.sendTXT(num,buffer);
    }

    else if (strcasecmp(command, "GIMMEJSONDATA") == 0)
    {
      get_JSON_MainPageStatus_string(&JSON_string_output);
      MyWebSocket.sendTXT(num,JSON_string_output);
    }


    else if (strcasecmp(command, "GIMMETIME") == 0)
    {
      sprintf(buffer,"CURRENT_TIME*%s*", global_date_time);
      MyWebSocket.sendTXT(num,buffer);
    }

    else if (strcasecmp(command, "RESTART") == 0)
    {
      sprintf(buffer,"RESTART*");
      MyWebSocket.sendTXT(num,buffer);
      ESP.restart();
    }
  
  

    else if (strcasecmp(command, "DELETE") == 0)
    {
      command = strtok(NULL, "*");
      SD_deleteFile(SD,command);
    }
    
    else if (strcasecmp(command, "DELETEALLLOGS") == 0)
    {
      uint16_t num_of_emp;
      num_of_emp = getTotalNumberOfEmployes(paths);
      for (uint16_t i = 0; i < num_of_emp; i++)
      {
        SD_deleteFile(SD,paths[i]);
      }
      get_JSON_MainPageStatus_string(&JSON_string_output);
      MyWebSocket.broadcastTXT(JSON_string_output);
      
    }

    else if (strcasecmp(command, "CREATE") == 0)
    {
      command = strtok(NULL, "*");
      SD_writeFile(SD,command,init_file_string);
    }

    else if (strcasecmp(command, "READ") == 0)
    {
      command = strtok(NULL, "*");
      SD_readFile(SD,command);
    }

      else if (strcasecmp(command, "SETTIME") == 0)
    {
      uint16_t year;
      uint8_t month;
      uint8_t day;
      uint8_t hour;
      uint8_t min;
      uint8_t sec;
      command = strtok(NULL, "*");
      year = atoi(command);
      command = strtok(NULL, "*");
      month = atoi(command);
      command = strtok(NULL, "*");
      day = atoi(command);
      command = strtok(NULL, "*");
      hour = atoi(command);
      command = strtok(NULL, "*");
      min = atoi(command);
      command = strtok(NULL, "*");
      sec = atoi(command);
      rtc.adjust(DateTime(year, month, day, hour, min, sec));
    }

    else
    {
      Serial.printf("Unkown Message: %s", payload);
      MyWebSocket.sendTXT(num, "Received unknown message:");
      MyWebSocket.sendTXT(num, payload);
    }

    break;
  }

  case WStype_ERROR:
  case WStype_BIN:
  case WStype_FRAGMENT_TEXT_START:
  case WStype_FRAGMENT_BIN_START:
  case WStype_FRAGMENT:
  case WStype_FRAGMENT_FIN:
  case WStype_PING:
  case WStype_PONG:
  default:
    ////Serial.printf("Received type: %s",type);
    break;
  }
}