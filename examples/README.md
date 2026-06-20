# Ejemplos de TIMBA

Programas de ejemplo para el interprete Retruco. Ejecutalos con:

```
retruco examples/hello.timba
```

o, sin instalar, desde la raiz del repositorio:

```
python -m retruco examples/hello.timba
```

| Archivo | Que muestra |
| --- | --- |
| `hello.timba` | El programa minimo: tomar una carta de una pila. |
| `move_stack.timba` | Ciclo `MIENTRAS` con `TOME`/`DEPOSITE` para mover una pila. |
| `invert_cards.timba` | La instruccion `INVIERTA LA CARTA` (dar vuelta cartas). |
| `split_by_palo.timba` | `SI` / `SINO` / `NADA MAS` con una condicion de palo. |
| `sort.timba` | Ordenamiento por insercion (valores unicos). |
| `sort_duplicates.timba` | Igual que `sort.timba` pero con valores repetidos (usa `MENOR` estricto). |
