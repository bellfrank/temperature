#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>         
#include <lcd.h>               
#include <time.h>
#include <math.h>



//USE WIRINGPI PIN NUMBERS
#define LCD_RS  25               //Register select pin
#define LCD_E   24               //Enable Pin
#define LCD_D4  23               //Data pin 4
#define LCD_D5  22               //Data pin 5
#define LCD_D6  21               //Data pin 6
#define LCD_D7  14               //Data pin 7

// Function prototypes
void set_timer(void);
void dht11_dat(double *temp, double *humid);

int main()
{
    double temperature;
    double humidity;
    dht11_dat(&temperature, &humidity);
    printf("%lf\n", temperature);
    printf("%lf\n", humidity);

    return 0;
}


// Generates temperature and humidity
void dht11_dat(double *temp, double *humid)
{
    // simulated measurements from a DHT11 sensor
    time_t rawtime;
    struct tm * timeinfo;
    time( &rawtime );
    timeinfo = localtime( &rawtime );
    double t = timeinfo->tm_hour + timeinfo->tm_min/60.0;

    srand(time(NULL));
    int r = rand();
    double noise = (double) r / RAND_MAX - 0.5; // noise is [-0.5, 0.5]

    *temp = 60 - 20*cos(3.14*t/12) + 2*noise;
    *humid = 70 + 20*cos(3.14*t/12) + 5*noise;
}

// current time
void set_timer(void){
    int lcd;
    wiringPiSetup();
    lcd = lcdInit (2, 16, 4, LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7, 0, 0, 0, 0);
    while(1){
        time_t timer;
        char buffer_date[26];
        char buffer_time[26];
        struct tm* tm_info;
        time(&timer);
        tm_info = localtime(&timer);
        strftime(buffer_date, 26, "Date: %m:%d:%Y", tm_info);
        strftime(buffer_time, 26, "Time: %H:%M:%S", tm_info);
        lcdPosition(lcd, 0, 0);
        lcdPuts(lcd, buffer_date);
        lcdPosition(lcd, 0, 1);
        lcdPuts(lcd, buffer_time);
    }
}