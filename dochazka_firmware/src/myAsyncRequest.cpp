#include "myAsyncRequest.h"
#include "SD.h"
#include "my_main_program_functions.h"

void onIndexRequest(AsyncWebServerRequest *request)
{
  IPAddress remote_IP = request->client()->remoteIP();
  // Serial.println("["+ remote_IP.toString() + "] HTTP GET request of " + request->url());
  request->send(SD, "/index.html", "text/html");
}

// CSS styling
void onCssRequest(AsyncWebServerRequest *request)
{
  IPAddress remote_IP = request->client()->remoteIP();
  // Serial.println("["+ remote_IP.toString() + "] HTTP GET request of " + request->url());
  request->send(SD, "/styles.css", "text/css");
}
void onJavaRequest(AsyncWebServerRequest *request)
{
  IPAddress remote_IP = request->client()->remoteIP();
  // Serial.println("["+ remote_IP.toString() + "] HTTP GET request of " + request->url());
  request->send(SD, "/app.js", "text/css");
}
// 404 error
void onPageNotFoundRequest(AsyncWebServerRequest *request)
{
  IPAddress remote_IP = request->client()->remoteIP();
  // Serial.println("["+ remote_IP.toString() + "] HTTP GET request of " + request->url());
  request->send(404, "text/plain", "Not found");
}


void UpdateSoundPath(AsyncWebServerRequest *request){
    IPAddress remote_IP = request->client()->remoteIP();
    // Serial.println("["+ remote_IP.toString() + "] HTTP GET request of " + request->url());
    char buffer[200];
    sprintf(buffer,"/sounds/%s",EMPLOY.sound);
    request->send(SD, buffer, "mp3");
}