#ifndef _SDCARDCOMMANDS_H
#define _SDCARDCOMMANDS_H
#include "globals.h"
#include <time.h> 

#define SD_CS 13
#define SDSPEED 4000000


void SD_listDir(fs::FS &fs, const char * dirname, uint8_t levels);
void SD_removeDir(fs::FS &fs, const char * path);
uint8_t SD_readFile(fs::FS &fs, const char * path);
void SD_writeFile(fs::FS &fs, const char * path, const char * message);
void SD_appendFile(fs::FS &fs, const char * path, const char * message);
void SD_renameFile(fs::FS &fs, const char * path1, const char * path2);
void SD_deleteFile(fs::FS &fs, const char * path);
void SD_createDir(fs::FS &fs, const char * path);
void SD_init();
#endif

