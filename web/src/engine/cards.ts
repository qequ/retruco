export enum Position {
  FACE_UP = 1,
  FACE_DOWN = 2,
}

export type Palo = "O" | "B" | "E" | "C";

export class Card {
  value: number;
  type: string;
  position: Position;

  constructor(value: number, type: string, position: Position = Position.FACE_UP) {
    this.value = value;
    this.type = type;
    this.position = position;
  }

  swapPosition(): void {
    this.position =
      this.position === Position.FACE_DOWN ? Position.FACE_UP : Position.FACE_DOWN;
  }
}
