export interface Example {
  name: string;
  label: string;
  source: string;
}

export const EXAMPLES: Example[] = [
  {
    name: "split_by_palo",
    label: "Separar por palo (SI/SINO)",
    source: `# Separa las cartas: las de OROS van a una pila, el resto a otra.
UCP EJECUTE CON LAS SIGUIENTES CARTAS
LA PILA MAZO TIENE 1 DE OROS BOCA ARRIBA -
                   2 DE ESPADAS BOCA ARRIBA -
                   3 DE OROS BOCA ARRIBA -
                   4 DE COPAS BOCA ARRIBA,
LA PILA MONEDAS NO TIENE CARTAS,
LA PILA RESTO NO TIENE CARTAS;

DEFINICION DE PROGRAMA
MIENTRAS LA PILA MAZO NO ESTA VACIA
    TOME UNA CARTA DE LA PILA MAZO
    SI LA CARTA ES OROS
        DEPOSITE LA CARTA EN PILA MONEDAS
    SINO
        DEPOSITE LA CARTA EN PILA RESTO
    NADA MAS
REPITA
`,
  },
  {
    name: "move_stack",
    label: "Mover una pila (MIENTRAS)",
    source: `# Mueve todas las cartas de ORIGEN a DESTINO (invirtiendo el orden).
UCP EJECUTE CON LAS SIGUIENTES CARTAS
LA PILA ORIGEN TIENE 1 DE OROS BOCA ARRIBA -
                     2 DE OROS BOCA ARRIBA -
                     3 DE OROS BOCA ARRIBA,
LA PILA DESTINO NO TIENE CARTAS;

DEFINICION DE PROGRAMA
MIENTRAS LA PILA ORIGEN NO ESTA VACIA
    TOME UNA CARTA DE LA PILA ORIGEN
    DEPOSITE LA CARTA EN PILA DESTINO
REPITA
`,
  },
  {
    name: "invert_cards",
    label: "Dar vuelta cartas (INVIERTA)",
    source: `# Da vuelta todas las cartas (de BOCA ABAJO a BOCA ARRIBA).
UCP EJECUTE CON LAS SIGUIENTES CARTAS
LA PILA MAZO TIENE 4 DE COPAS BOCA ABAJO -
                   5 DE COPAS BOCA ABAJO -
                   6 DE COPAS BOCA ABAJO,
LA PILA RESULTADO NO TIENE CARTAS;

DEFINICION DE PROGRAMA
MIENTRAS LA PILA MAZO NO ESTA VACIA
    TOME UNA CARTA DE LA PILA MAZO
    INVIERTA LA CARTA
    DEPOSITE LA CARTA EN PILA RESULTADO
REPITA
`,
  },
];
