#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <lcd.h>
#include <time.h>
#include <math.h>
#include <mysql/mysql.h>
#include <wiringPi.h>


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
    MYSQL *conn;
    MYSQL_RES *res;
    MYSQL_ROW row;

    /* Server Information */
    char *server = "localhost";
    char *user = "frank";
    char *password = "password";
    char *database = "datalog";

    conn = mysql_init(NULL);

    /* Connect to database */
    if (!mysql_real_connect(conn, server, user, password, database, 0, NULL, 0)){
        fprintf(stderr, "%s\n", mysql_error(conn));
        exit(1);
    }

    int lcd;
    wiringPiSetup();
    lcd = lcdInit (2, 16, 4, LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7, 0, 0, 0, 0);

    double temperature;
    double humidity;

    while(TRUE){

        dht11_dat(&temperature, &humidity);

        printf("Temp: %.2lf\n", temperature);
        printf("Humid: %.2lf\n", humidity);

        char log_temp[16];
        char log_hum[16];

        char ch=223;
        sprintf(log_temp, "Temp: %.2lf %cF", temperature,ch);
        sprintf(log_hum, "Humd: %.2lf %%", humidity);

        lcdPosition(lcd, 0, 0);
        lcdPuts(lcd, log_temp);
        lcdPosition(lcd, 0, 1);
        lcdPuts(lcd, log_hum);
        char query[100] = "";
        sprintf(query, "insert into thlog2 (temperature, humidity, time) values (%lf, %lf, CURRENT_TIMESTAMP)", temperature, humidity);

        /* send SQL query */
        if (mysql_query(conn, query)){
            fprintf(stderr, "%s\n", mysql_error(conn));
            exit(1);
        }

        sleep(1);
    }

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
