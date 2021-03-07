# purificador

Codigo desarrollado para leer sensores DHT22 y TSL2561. 
Se utilizan repositorios de Adafruit, los cuales facilitan la interaccion con los sensores.

Se adiciona led en el pin GPIO21 para tener precente el momento en el que se esta tomando la data.
La data se sube a Thingspeak, en el cual toca crear cuenta y canal, y modificar el Key en el codigo para que concuerde.

El sensor DHT22 esta conectado en mi Raspberry al pin GPIO4, si no va a conetarse en este, se debe modificar el pin donde esta detallado en el codigo.
El sensor TSL2561, es conectado por I2C, para lo que se usan los puertos GPIO2 y GPIO3 el puerto 2 es para coneccion SDA y el puerto 3 para coneccion SCL.

Importante acctiar la deteccion de puertos I2C en la configuracion del Raspberry Pi.
