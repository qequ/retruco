# Retruco

![Retroco_logo](/src/logo/timba.png)

A virtual machine and interpreter for the [TIMBA](http://dirinfo.unsl.edu.ar/servicios/abm/assets/uploads/materiales/ddafb-timba-2018.pdf) language.


Un intérprete para el lenguaje de programación [TIMBA](http://dirinfo.unsl.edu.ar/servicios/abm/assets/uploads/materiales/ddafb-timba-2018.pdf)

# Prerequisites

1. Python3
2. Tkinter (if you want to use the gui)

To install Tkinter;
```
pip install tk
```

# Usage 

```
python retruco.py
```

# Example programs

## Hello Timba
The language can't handle strings so the most basic program is taking a card from a stack;

```
UCP EJECUTE CON LAS SIGUIENTES CARTAS
LA PILA HOLATIMBA TIENE 1 DE ESPADAS BOCA ARRIBA;

DEFINICION DE PROGRAMA
TOME UNA CARTA DE LA PILA HOLATIMBA

```

## Sorting a stack

```
UCP EJECUTE CON LAS SIGUIENTES CARTAS
LA PILA INPUT TIENE       10 DE BASTOS BOCA ARRIBA -
                          7 DE BASTOS BOCA ARRIBA -
                          1 DE ESPADAS BOCA ARRIBA -
                          5 DE OROS BOCA ARRIBA -
                          11 DE COPAS BOCA ARRIBA -
                          2 DE COPAS BOCA ARRIBA -
                          6 DE ESPADAS BOCA ARRIBA,

LA PILA TMPSTACK NO TIENE CARTAS,
LA PILA AUXILIAR NO TIENE CARTAS,
LA PILA AUXILIAR2 NO TIENE CARTAS;


DEFINICION DE PROGRAMA
MIENTRAS LA PILA INPUT NO ESTA VACIA

    TOME UNA CARTA DE LA PILA INPUT

    MIENTRAS LA PILA TMPSTACK NO ESTA VACIA
        SI LA CARTA ES DE MENOR O IGUAL VALOR QUE TOPE DE PILA TMPSTACK
            # TOMAR EL TOPE DE PILA DE TMPSTACK Y PONERLO EN STACK DE INPUT
            # ANTES DEPOSITAR LA CARTA TMP EN AUXILIAR
            DEPOSITE LA CARTA EN PILA AUXILIAR

            TOME UNA CARTA DE PILA TMPSTACK
            DEPOSITE LA CARTA EN PILA INPUT
            TOME UNA CARTA DE PILA AUXILIAR


        SINO
            # NO HAY BREAK ASI QUE HAY QUE SACAR TODAS LAS CARTAS DE TMPSTACK ASI SE ROMPE EL WHILE

            #depositamos tmp en auxiliar 
            DEPOSITE LA CARTA EN PILA AUXILIAR

            MIENTRAS LA PILA TMPSTACK NO ESTA VACIA
                TOME UNA CARTA DE PILA TMPSTACK
                DEPOSITE LA CARTA EN PILA AUXILIAR2
            REPITA

            # recuperamos temp
            TOME UNA CARTA DE PILA AUXILIAR
        NADA MAS

    REPITA

    DEPOSITE LA CARTA EN PILA AUXILIAR

    # caso de romper el while antes
    SI LA PILA TMPSTACK ESTA VACIA Y LA PILA AUXILIAR2 NO ESTA VACIA
        MIENTRAS LA PILA AUXILIAR2 NO ESTA VACIA
            TOME UNA CARTA DE PILA AUXILIAR2
            DEPOSITE LA CARTA EN PILA TMPSTACK
        REPITA
    SINO
    NADA MAS

    TOME UNA CARTA DE PILA AUXILIAR
    DEPOSITE LA CARTA EN PILA TMPSTACK

REPITA

```

# TODO
- [ ] A setup script

# License
MIT License Copyright (c) 2021 Alvaro Frias
