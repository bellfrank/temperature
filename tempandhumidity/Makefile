temp: main.c
	gcc -B -Wall -g -I/usr/include/mariadb -I/usr/include/mariadb/mysql  -c /home/pi/Desktop/temperature/tempandhumidity/main.c -o obj/Debug/main.o
	gcc  -o bin/Debug/tempandhumidity obj/Debug/main.o -lm -L/usr/lib/arm-linux-gnueabihf/ -lmariadb /usr/lib/libwiringPi.so /usr/lib/libwiringPiDev.so
	./bin/Debug/tempandhumidity

menu: menu.c
	gcc -B -Wall -g -I/usr/include/mariadb -I/usr/include/mariadb/mysql  -c /home/pi/Desktop/temperature/tempandhumidity/menu.c -o obj/Debug/menu.o
	gcc  -o bin/Debug/tempandhumidity obj/Debug/menu.o -lm -L/usr/lib/arm-linux-gnueabihf/ -lmariadb /usr/lib/libwiringPi.so /usr/lib/libwiringPiDev.so
	./bin/Debug/tempandhumidity