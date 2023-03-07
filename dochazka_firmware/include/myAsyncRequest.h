#ifndef _MYASYNCREQUEST_H
#define _MYASYNCREQUEST_H
#include "globals.h"
void onIndexRequest(AsyncWebServerRequest *request);
void onCssRequest(AsyncWebServerRequest *request);
void onJavaRequest(AsyncWebServerRequest *request);
void onPageNotFoundRequest(AsyncWebServerRequest *request);
void UpdateSoundPath(AsyncWebServerRequest *request);
#endif