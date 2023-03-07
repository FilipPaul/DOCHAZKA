#ifndef _WEBSOCKETCALLBACK_H
#define _WEBSOCKETCALLBACK_H
#include "Arduino.h"
#include "WebSocketsServer.h"
#include "globals.h"


void SendJSONMessage(const char JSON_string[], uint8_t num);
void WebSocketCallback(uint8_t num,      // Number of clients connected
                    WStype_t type,    // type of message, error, text, disconnected, connetcted status etc..
                    uint8_t *payload, // raw data
                    size_t length);   // length of payload
#endif
