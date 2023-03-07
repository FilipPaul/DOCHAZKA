#ifndef _MY_MAIN_PROGRAM_FUNCTIONS_H
#define _MY_MAIN_PROGRAM_FUNCTIONS_H
#include "globals.h"

void setState(uint8_t *state_variable, uint8_t enum_state, uint8_t update_display);
void UpdateAllTimes();
uint8_t compareRFIDwithSD(uint8_t TagID[], uint8_t ID_size);
void customPrint(uint8_t id);
uint8_t scanButtonMatrix(char pressed_btn[], uint8_t btn_array[], const char* btn_states[],uint8_t arrSize);
void get_JSON_MainPageStatus_string(String *JSON_string_output);
uint16_t getTotalNumberOfEmployes(char paths_string_array[ARRAYSIZE_1][ARRAYSIZE_2]);
#endif