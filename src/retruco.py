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
            self.fr_buttons, text="SI", command=lambda: form_proposition(self, 3))
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
        self.proposition = ""

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

        def update_proposition(self, append_string):
            self.proposition += append_string
            print(self.proposition)

        def form_proposition(self, type_op):
            new_window = tk.Toplevel(self)
            new_window.geometry("800x600")
            self.proposition = ""
            print("reset propos: {}".format(self.proposition))

            e1 = ["ESTÁ", "NO ESTÁ"]
            e2 = ["ES", "NO ES"]
            palos = ["ORO", "BASTO", "ESPADA", "COPA"]
            numeric_comp = ["!=", "=", "<", ">", "<=", ">="]
            card_values = [str(i) for i in range(1, 8)] + \
                [str(i) for i in range(10, 13)]

            # lists of propositions

            # frame of stacks propositions
            frm_pila = tk.Frame(master=new_window)
            if len(self.stacks_names) != 0:
                msg1 = tk.Label(master=frm_pila, text="LA PILA")
                msg2 = tk.Label(master=frm_pila, text="VACIA")
                e1_var = tk.StringVar(frm_pila)
                e1_var.set(e1[0])
                op_menu1 = tk.OptionMenu(frm_pila, e1_var, *e1)
                stack_var = tk.StringVar(frm_pila)
                stack_var.set(self.stacks_names[0])
                stacks_op = tk.OptionMenu(
                    frm_pila, stack_var, *self.stacks_names)
                btn1 = tk.Button(master=frm_pila, command=lambda: update_proposition(self,
                                                                                     "P" + str(self.stacks_names.index(stack_var.get())) + e1_var.get()[0]),
                                 text="Agregar")

                msg1.grid(row=0, column=0)
                stacks_op.grid(row=0, column=1)
                op_menu1.grid(row=0, column=2)
                msg2.grid(row=0, column=3)
                btn1.grid(row=0, column=4)
            else:
                l1 = tk.Label(master=frm_pila,
                              text="No hay pilas con las que formar una proposición")
                l1.pack()

            # position of the card proposition
            frm_pos_card = tk.Frame(master=new_window)
            msg1 = tk.Label(master=frm_pos_card, text="LA CARTA")
            msg2 = tk.Label(master=frm_pos_card, text="BOCA ABAJO")
            e1_var_card_pos = tk.StringVar(frm_pos_card)
            e1_var_card_pos.set(e1[0])
            op_menu1_pos_card = tk.OptionMenu(
                frm_pos_card, e1_var_card_pos, *e1)
            btn1_cp = tk.Button(master=frm_pos_card, command=lambda: update_proposition(self,
                                                                                        "C" +
                                                                                        e1_var_card_pos.get()[
                                                                                            0]+"F",
                                                                                        ),
                                text="Agregar")

            msg1.grid(row=0, column=0)
            op_menu1_pos_card.grid(row=0, column=1)
            msg2.grid(row=0, column=2)
            btn1_cp.grid(row=0, column=3, pady=5)

            # proposition about card's palo
            frm_palo = tk.Frame(master=new_window)
            msg1 = tk.Label(master=frm_palo, text="LA CARTA")
            msg2 = tk.Label(master=frm_palo, text="DEL PALO")
            e2_var_card_palo = tk.StringVar(frm_palo)
            e2_var_card_palo.set(e2[0])
            op_menu2_palo_card = tk.OptionMenu(
                frm_palo, e2_var_card_palo, *e2)
            palos_var = tk.StringVar(master=frm_palo)
            palos_var.set(palos[0])
            op_menu_palos = tk.OptionMenu(frm_palo, palos_var, *palos)
            btn1_palo_c = tk.Button(master=frm_palo, command=lambda: update_proposition(self,
                                                                                        "C"+e2_var_card_palo.get()[0]+palos_var.get()[0]),
                                    text="Agregar")

            msg1.grid(row=0, column=0)
            op_menu2_palo_card.grid(row=0, column=1)
            msg2.grid(row=0, column=2)
            op_menu_palos.grid(row=0, column=3)
            btn1_palo_c.grid(row=0, column=4, pady=5)

            # proposition about card's palo compared with the top of stack

            frm_palo_stack = tk.Frame(master=new_window)

            if len(self.stacks_names) != 0:
                msg1 = tk.Label(master=frm_palo_stack, text="LA CARTA")
                msg2 = tk.Label(master=frm_palo_stack,
                                text="DE IGUAL PALO QUE TOPE DE PILA")

                e2_palo_stack_var = tk.StringVar(master=frm_palo_stack)
                e2_palo_stack_var.set(e2[0])
                op_menu_e2_stack_palo = tk.OptionMenu(
                    frm_palo_stack, e2_palo_stack_var, *e2)

                stack_palo_var = tk.StringVar(master=frm_palo_stack)
                stack_palo_var.set(self.stacks_names[0])
                op_menu_stacks_names_palo = tk.OptionMenu(
                    frm_palo_stack, stack_palo_var, *self.stacks_names)

                btn_palo_stack = tk.Button(
                    master=frm_palo_stack,
                    command=lambda: update_proposition(
                        self, "C"+e2_palo_stack_var.get()[0]+"P" + str(self.stacks_names.index(stack_palo_var.get()))),
                    text="Agregar")

                msg1.grid(row=0, column=0)
                op_menu_e2_stack_palo.grid(row=0, column=1)
                msg2.grid(row=0, column=2)
                op_menu_stacks_names_palo.grid(row=0, column=3)
                btn_palo_stack.grid(row=0, column=4, pady=5)
            else:
                l2 = tk.Label(
                    master=frm_palo_stack, text="No hay pilas con las que formar una proposición")
                l2.pack()

            # propositions about comparing the card value with a number
            frm_value = tk.Frame(master=new_window)

            msg1 = tk.Label(master=frm_value, text="LA CARTA")
            msg2 = tk.Label(master=frm_value, text="DE VALOR")

            e2_value_var = tk.StringVar(master=frm_value)
            e2_value_var.set(e2[0])
            op_menu_e2_value = tk.OptionMenu(
                frm_value, e2_value_var, *e2)

            num_comp_var = tk.StringVar(master=frm_value)
            num_comp_var.set(numeric_comp[0])
            op_menu_num_comp_value = tk.OptionMenu(
                frm_value, num_comp_var, *numeric_comp)

            num_var = tk.StringVar(master=new_window)
            num_var.set(card_values[0])
            op_menu_number_values = tk.OptionMenu(
                frm_value, num_var, *card_values)

            btn_value = tk.Button(
                master=frm_value,
                command=lambda: update_proposition(self,
                                                   "C"+e2_value_var.get()[0]+num_comp_var.get()+num_var.get()),
                text="Agregar")

            msg1.grid(row=0, column=0)
            op_menu_e2_value.grid(row=0, column=1)
            msg2.grid(row=0, column=2)
            op_menu_num_comp_value.grid(row=0, column=3)
            op_menu_number_values.grid(row=0, column=4)
            btn_value.grid(row=0, column=5)

            # proposition about card's value with the top of a stack
            frm_stack_value = tk.Frame(master=new_window)

            msg1 = tk.Label(master=frm_stack_value, text="LA CARTA")
            msg2 = tk.Label(master=frm_stack_value,
                            text="QUE VALOR QUE TOPE DE PILA")

            e2_stack_value_var = tk.StringVar(master=frm_stack_value)
            e2_stack_value_var.set(e2[0])
            op_menu_e2_stack_value = tk.OptionMenu(
                frm_stack_value, e2_stack_value_var, *e2)

            num_comp_stack_value_var = tk.StringVar(master=frm_stack_value)
            num_comp_stack_value_var.set(numeric_comp[0])
            op_menu_num_comp_stack_value = tk.OptionMenu(
                frm_stack_value, num_comp_stack_value_var, *numeric_comp)

            stack_names_stack_value_var = tk.StringVar(master=frm_stack_value)
            stack_names_stack_value_var.set(self.stacks_names[0])
            op_menu_stack_names_stack_value = tk.OptionMenu(
                frm_stack_value, stack_names_stack_value_var, *self.stacks_names)

            btn_stack_value = tk.Button(
                master=frm_stack_value,
                command=lambda: update_proposition(self, "C"+e2_stack_value_var.get()[0]+num_comp_stack_value_var.get(
                )+"P"+str(self.stacks_names.index(stack_names_stack_value_var.get()))),
                text="Agregar")

            msg1.grid(row=0, column=0)
            op_menu_e2_stack_value.grid(row=0, column=1)
            op_menu_num_comp_stack_value.grid(row=0, column=2)
            msg2.grid(row=0, column=3)
            op_menu_stack_names_stack_value.grid(row=0, column=4)
            btn_stack_value.grid(row=0, column=5)

            # packing all the frames of template propositions
            frm_pila.pack()
            frm_pos_card.pack()
            frm_palo.pack()
            frm_palo_stack.pack()
            frm_value.pack()
            frm_stack_value.pack()

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
