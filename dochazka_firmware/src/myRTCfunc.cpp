#include "myRTCfunc.h"

void showDate(const char* txt, const DateTime& dt) {
    Serial.print(txt);
    Serial.print(' ');
    Serial.print(dt.year(), DEC);
    Serial.print('/');
    Serial.print(dt.month(), DEC);
    Serial.print('/');
    Serial.print(dt.day(), DEC);
    Serial.print(' ');
    Serial.print(dt.hour(), DEC);
    Serial.print(':');
    Serial.print(dt.minute(), DEC);
    Serial.print(':');
    Serial.print(dt.second(), DEC);

    Serial.print(" = ");
    Serial.print(dt.unixtime());
    Serial.print("s / ");
    Serial.print(dt.unixtime() / 86400L);
    Serial.print("d since 1970");

    Serial.println();
}

void showTimeSpan(const char* txt, const TimeSpan& ts) {
    Serial.print(txt);
    Serial.print(" ");
    Serial.print(ts.days(), DEC);
    Serial.print(" days ");
    Serial.print(ts.hours(), DEC);
    Serial.print(" hours ");
    Serial.print(ts.minutes(), DEC);
    Serial.print(" minutes ");
    Serial.print(ts.seconds(), DEC);
    Serial.print(" seconds (");
    Serial.print(ts.totalseconds(), DEC);
    Serial.print(" total seconds)");
    Serial.println();
}