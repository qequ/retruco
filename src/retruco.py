import tkinter as tk


class Retruco(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Retruco")
        self.rowconfigure(0, minsize=600, weight=1)
        self.columnconfigure(1, minsize=800, weight=1)

        self.ucp_instructions = tk.Text(self)
        self.ucp_instructions.config(state=tk.NORMAL)
        self.ucp_instructions.insert(
            tk.END, "DEFINICION DE PROGRAMA\n")
        self.ucp_instructions.config(state=tk.DISABLED)

        self.stack_set_instruction = tk.Text(self)
        self.stack_set_instruction.config(state=tk.NORMAL)
        self.stack_set_instruction.insert(
            tk.END, "UCP EJECUTE CON LAS SIGUIENTES CARTAS:\n")
        self.stack_set_instruction.config(state=tk.DISABLED)

        # main buttons for operations
        self.fr_buttons = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.btn_take = tk.Button(self.fr_buttons, text="TOMAR", command=lambda: select_stack(self,
                                                                                              "Seleccione pila de la que Tomar carta", 0))
        self.btn_deposit = tk.Button(
            self.fr_buttons, text="DEPOSITAR", command=lambda: select_stack(self, "Seleccione pila en la que Depositar", 1))
        self.btn_invert = tk.Button(
            self.fr_buttons, text="INVERTIR", command=lambda: add_opcode(self, 2, None))
        self.btn_if = tk.Button(
            self.fr_buttons, text="SI", command=lambda: 1)
        self.btn_else = tk.Button(
            self.fr_buttons, text="SINO", command=lambda: 1)
        self.btn_endif = tk.Button(
            self.fr_buttons, text="NADA MAS", command=lambda: 1)
        self.btn_while = tk.Button(
            self.fr_buttons, text="MIENTRAS", command=lambda: 1)
        self.btn_endwhile = tk.Button(
            self.fr_buttons, text="REPITA", command=lambda: 1)
        self.btn_add_stack = tk.Button(
            self.fr_buttons, text="AÑADIR PILA", command=lambda: add_stack(self))
        self.btn_add_card = tk.Button(
            self.fr_buttons, text="AÑADIR CARTA", command=lambda: add_card(self))

        # packing buttons
        self.btn_take.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_deposit.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.btn_invert.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_if.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.btn_else.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.btn_endif.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
        self.btn_while.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        self.btn_endwhile.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
        self.btn_add_stack.grid(row=8,  column=0, sticky="ew", padx=5, pady=20)
        self.btn_add_card.grid(row=9,  column=0, sticky="ew", padx=5)

        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.ucp_instructions.grid(row=0, column=1, sticky="nsew")
        self.stack_set_instruction.grid(row=0, column=2, sticky="nsew")

        # data structures for the virtual machine
        self.opcodes = []
        self.stacks_opcodes = []
        self.stacks_names = []

        def select_stack(self, message, type_op):
            new_window = tk.Toplevel(self)
            new_window.geometry("255x120")

            if self.stacks_names == []:
                message = "No hay pilas actualmente"
                msg_lbl = tk.Label(master=new_window, text=message)
                msg_lbl.pack()
            else:
                msg_lbl = tk.Label(master=new_window, text=message)

                stack_var = tk.StringVar(new_window)
                stack_var.set(self.stacks_names[0])
                stacks_op = tk.OptionMenu(
                    new_window, stack_var, *self.stacks_names)

                btn_ok = tk.Button(new_window, text="Confirmar",
                                   command=lambda: add_opcode(self, type_op, stack_var.get()))

                msg_lbl.pack()
                stacks_op.pack()
                btn_ok.pack()

        def add_opcode(self, type_op, stack_name):
            if type_op == 0:
                self.opcodes.append(
                    "0" + str(self.stacks_names.index(stack_name)))
                # add to the editor (ucp_instructions) the instruction "TOME UNA CARTA DE LA PILA {stack_name}"
                self.ucp_instructions.config(state=tk.NORMAL)
                self.ucp_instructions.insert(
                    tk.END, "TOME UNA CARTA DE LA PILA {}\n".format(stack_name))
                self.ucp_instructions.config(state=tk.DISABLED)
            elif type_op == 1:
                self.opcodes.append(
                    "1" + str(self.stacks_names.index(stack_name)))
                # add to the editor (ucp_instructions) the instruction "DEPOSITE LA CARTA EN LA PILA {stack_name}"
                self.ucp_instructions.config(state=tk.NORMAL)
                self.ucp_instructions.insert(
                    tk.END, "DEPOSITE LA CARTA EN LA PILA {}\n".format(stack_name))
                self.ucp_instructions.config(state=tk.DISABLED)

            elif type_op == 2:
                self.opcodes.append("2")
                self.ucp_instructions.config(state=tk.NORMAL)
                self.ucp_instructions.insert(
                    tk.END, "INVIERTA LA CARTA\n")
                self.ucp_instructions.config(state=tk.DISABLED)

            print(self.opcodes)

        def add_card(self):
            new_window = tk.Toplevel(self)
            new_window.geometry("400x125")

            if self.stacks_names == []:
                msg_lbl = tk.Label(
                    master=new_window, text="No hay pilas actualmente\nCree una nueva")
                msg_lbl.pack()
            else:
                lbl_status = tk.Label(master=new_window, text="")

                lbl_instruction = tk.Label(
                    master=new_window, text="Seleccione Pila y Carta que añadir")

                frame_options = tk.Frame(master=new_window)

                stack_var = tk.StringVar(frame_options)
                stack_var.set(self.stacks_names[0])
                stacks_op = tk.OptionMenu(
                    frame_options, stack_var, *self.stacks_names)

                card_values = [str(i) for i in range(1, 8)] + \
                    [str(i) for i in range(10, 13)]
                card_types = ["ESPADA", "ORO", "BASTO", "COPA"]

                position = ["BOCA ARRIBA", "BOCA ABAJO"]

                value_var = tk.StringVar(frame_options)
                value_var.set(card_values[0])
                value_op = tk.OptionMenu(
                    frame_options, value_var, *card_values)

                type_var = tk.StringVar(frame_options)
                type_var.set(card_types[0])
                type_op = tk.OptionMenu(frame_options, type_var, *card_types)

                pos_var = tk.StringVar(frame_options)
                pos_var.set(position[0])
                pos_op = tk.OptionMenu(frame_options, pos_var, *position)

                btn_ok = tk.Button(new_window, text="Confirmar",
                                   command=lambda: add_stack_opcode(self, stack_var.get(),
                                                                    value_var.get(),
                                                                    type_var.get(), pos_var.get(), lbl_status))

                stacks_op.grid(row=0, column=0, padx=5, pady=5)
                value_op.grid(row=0, column=1,  padx=5, pady=5)
                type_op.grid(row=0, column=2,  padx=5, pady=5)
                pos_op.grid(row=0, column=3,  padx=5, pady=5)

                lbl_instruction.pack()
                frame_options.pack()
                lbl_status.pack()
                btn_ok.pack()

        def add_stack_opcode(self, stack_name, value_card, type_card, pos_card, lbl):
            print(stack_name, type(value_card), type_card, pos_card)

            # check first if the card is being used in other stack
            opcodes_to_check = list(
                filter(lambda s: not s.isnumeric(), self.stacks_opcodes))

            for opc in opcodes_to_check:
                for i in range(len(opc)):
                    if opc[i] in ["O", "E", "C", "B"]:
                        palo_index = i
                        break

                c = opc[palo_index: -1]

                if c == type_card[0] + value_card:
                    # the card is already in some stack
                    lbl.config(text="La carta ya está en una pila")
                    return

            # if it reached here it means its a new opcode to set the stack
            if "ARRIBA" in pos_card:
                pos = "U"
            else:
                pos = "D"

            opcode = str(self.stacks_names.index(
                stack_name)) + type_card[0] + value_card + pos
            lbl.config(
                text="La carta se añadió a la Pila {}".format(stack_name))
            self.stacks_opcodes.append(opcode)
            print(self.stacks_opcodes)
            self.stack_set_instruction.config(state=tk.NORMAL)
            self.stack_set_instruction.insert(tk.END, "AÑADA {} DE {} {} A '{}'\n".format(
                value_card, type_card, pos_card, stack_name))
            self.stack_set_instruction.config(state=tk.DISABLED)

        def add_stack(self):
            new_window = tk.Toplevel(self)
            new_window.geometry("255x120")

            stack_name_entry = tk.Entry(master=new_window, width=50)
            lbl_instruction = tk.Label(
                master=new_window, text="Ingrese nombre de Nueva Pila")
            lbl_status = tk.Label(
                master=new_window, text="")

            btn_action = tk.Button(master=new_window, text="Confirmar",  command=lambda: create_new_stack(
                self, stack_name_entry.get(), lbl_status))

            lbl_instruction.pack()
            lbl_status.pack()
            stack_name_entry.pack()
            btn_action.pack()

        def create_new_stack(self, name_stack, lbl):
            if name_stack in self.stacks_names:
                # change lbl status
                lbl.config(text="Esa Pila ya existe")
                return

            self.stacks_names.append(name_stack)
            lbl.config(text="Pila Creada")
            self.stacks_opcodes.append(
                str(self.stacks_names.index(name_stack)))
            self.stack_set_instruction.config(state=tk.NORMAL)
            self.stack_set_instruction.insert(
                tk.END, "CREE LA PILA {}\n".format(name_stack))
            self.stack_set_instruction.config(state=tk.DISABLED)


rt = Retruco()
rt.mainloop()
