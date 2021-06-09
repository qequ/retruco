import tkinter as tk


class Retruco(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Retruco")
        self.rowconfigure(0, minsize=600, weight=1)
        self.columnconfigure(1, minsize=800, weight=1)

        self.ucp_instructions = tk.Text(self)
        self.ucp_instructions.config(state=tk.DISABLED)

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

        # data structures for the virtual machine
        self.opcodes = []
        self.stacks_opcodes = []
        self.stacks_names = ["A", "B", "C"]

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
            pass

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
            print(self.stacks_names)


rt = Retruco()
rt.mainloop()
