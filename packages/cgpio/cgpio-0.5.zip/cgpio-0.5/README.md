# Linux [sysfs](https://www.kernel.org/doc/Documentation/gpio/sysfs.txt) gpio access

This library provides gpio class access via the standard linux [sysfs interface](https://www.kernel.org/doc/Documentation/gpio/sysfs.txt)

It is intended to mimick [RPIO](http://pythonhosted.org/RPIO/) as much as possible 
for all features, while also supporting additional (and better named) functionality 
to the same methods.

#based on gpio-0.1.2, you should install gpio firstly.

##using tips

t=cgpio('GPIOA9',OUT,HIGH)
t=cgpio('GPIOA9',OUT,HIGH)
t=cgpio('A9',OUT,HIGH)
t=cgpio('a9',OUT,HIGH)
t=cgpio(9,OUT,HIGH)
t.set(1)
t.set(0)


t=cgpio('GPIOA9',IN)
t.read()


