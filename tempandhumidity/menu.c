#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>         
#include <lcd.h>               
#include <time.h>
#include <math.h>
#include <mysql/mysql.h>



//USE WIRINGPI PIN NUMBERS
#define LCD_RS  25               //Register select pin
#define LCD_E   24               //Enable Pin
#define LCD_D4  23               //Data pin 4
#define LCD_D5  22               //Data pin 5
#define LCD_D6  21               //Data pin 6
#define LCD_D7  14               //Data pin 7

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


    while(TRUE){

        int year,day,month,hour,minute,second;
        int year2,day2,month2,hour2,minute2,second2;
        int choice;
        int option;

        printf("Temperature and Humidity Database");

         // User choice
        printf("What would like you to analyze today? 1. Max, 2. Min, or 3. Average: ");
        scanf("%d", &choice);
        printf("Enter time range of the collected data: ex. 2022-05-26 15:10:27 to 2022-05-26 16:34:27\n");
        printf("Date: ");
        scanf("%d-%d-%d %d:%d:%d to %d-%d-%d %d:%d:%d",&year,&month,&day,&hour,&minute,&second,&year2,&month2,&day2,&hour2,&minute2,&second2);
        
        printf("1.Temperature or 2.Humidity: ");
        scanf("%d", &option);



        // setting up query
        char query[200] = "";

        switch(choice)
        {
            case 1:
                if (option == 1){
                    sprintf(query, "select time,temperature from thlog2 where temperature = (SELECT MAX(temperature) FROM thlog2 WHERE time BETWEEN '%d-%d-%d %d:%d:%d' AND '%d-%d-%d %d:%d:%d')",year,month,day,hour,minute,second,year2,month2,day2,hour2,minute2,second2);
                    
                }
                if (option == 2){
                    sprintf(query, "select time,humidity from thlog2 where humidity = (SELECT MAX(humidity) FROM thlog2 WHERE time BETWEEN '%d-%d-%d %d:%d:%d' AND '%d-%d-%d %d:%d:%d')",year,month,day,hour,minute,second,year2,month2,day2,hour2,minute2,second2);
                    
                }
                break;
        
            case 2:
                if (option == 1){
                    sprintf(query, "select time,temperature from thlog2 where temperature = (SELECT MIN(temperature) FROM thlog2 WHERE time BETWEEN '%d-%d-%d %d:%d:%d' AND '%d-%d-%d %d:%d:%d')",year,month,day,hour,minute,second,year2,month2,day2,hour2,minute2,second2);
                    
                }
                if (option == 2){
                    sprintf(query, "select time,humidity from thlog2 where humidity = (SELECT MIN(humidity) FROM thlog2 WHERE time BETWEEN '%d-%d-%d %d:%d:%d' AND '%d-%d-%d %d:%d:%d')",year,month,day,hour,minute,second,year2,month2,day2,hour2,minute2,second2);
                    
                }
                break;
        
            case 3:
                if (option == 1){
                    sprintf(query, "select AVG(temperature) FROM thlog2 WHERE time BETWEEN '%d-%d-%d %d:%d:%d' AND '%d-%d-%d %d:%d:%d'",year,month,day,hour,minute,second,year2,month2,day2,hour2,minute2,second2);
                   
                }
                if (option == 2){
                    sprintf(query, "select AVG(humidity) FROM thlog2 WHERE time BETWEEN '%d-%d-%d %d:%d:%d' AND '%d-%d-%d %d:%d:%d'",year,month,day,hour,minute,second,year2,month2,day2,hour2,minute2,second2);
                    
                }
                break;
                
            default :
                printf("Invalid Input.\n");
        }
        
        // prints results from switch
        if (mysql_query(conn, query)){
            fprintf(stderr, "%s\n", mysql_error(conn));
            exit(1);
        }
        
        res = mysql_use_result(conn);

        /* output table name */
        if (choice == 3){
            while ((row = mysql_fetch_row(res)) != NULL){
            printf("%s\n", row[0]);
            sleep(1);
            }
        }
        else{
            while ((row = mysql_fetch_row(res)) != NULL){
            printf("%s %s\n", row[1], row[0]);
            sleep(1);
            }
        }
    
    }

    return 0;
}