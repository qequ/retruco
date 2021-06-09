import unittest
from virtual_machine.vm import VirtualMachine
from virtual_machine.cards import Position


class TestLogicDecoder(unittest.TestCase):

    def test_empty_stacks(self):
        stack_set_up = [
            "0",
            "1",
            "2"
        ]
        opcodes_list = []
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        for s in vm.stacks:
            self.assertEqual(s, [])

    def test_1(self):
        stack_set_up = [
            "0E1U",
            "0B1U",
            "0C1U",
            "0O1U",
            "1E2U",
            "1B2U"
        ]
        opcodes_list = []

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        self.assertTrue(vm.decode_logical_condition("P1N"))
        self.assertEqual(vm.error_code, 0)

    def test_2(self):
        stack_set_up = [
            "0E1U",
        ]
        opcodes_list = ["00", "10"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        vm.execute_instruction()
        self.assertTrue(vm.decode_logical_condition("P0E"))
        self.assertTrue(vm.decode_logical_condition("CEE"))
        self.assertFalse(vm.decode_logical_condition("CEB"))
        self.assertFalse(vm.decode_logical_condition("CEO"))
        self.assertFalse(vm.decode_logical_condition("CEC"))
        self.assertTrue(vm.decode_logical_condition("CNB"))
        self.assertTrue(vm.decode_logical_condition("CNC"))
        self.assertTrue(vm.decode_logical_condition("CNO"))
        self.assertFalse(vm.decode_logical_condition("CEF"))
        self.assertTrue(vm.decode_logical_condition("CNF"))
        self.assertEqual(vm.error_code, 0)

        vm.execute_instruction()
        self.assertFalse(vm.decode_logical_condition("CEE"))
        self.assertEqual(vm.error_code, 3)

    def test_3(self):
        stack_set_up = [
            "0E1U",
            "0B1U",
            "1E2U",
            "1B2U"
        ]
        opcodes_list = ["00"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        vm.execute_instruction()
        self.assertTrue(vm.decode_logical_condition("CEP1"))
        self.assertFalse(vm.decode_logical_condition("CEP0"))
        self.assertEqual(vm.error_code, 0)

    def test_4(self):
        stack_set_up = [
            "0E1U",
            "0B7U",
            "1E2U",
            "1B2U"
        ]
        opcodes_list = ["00"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        vm.execute_instruction()
        self.assertTrue(vm.decode_logical_condition("CE==7"))
        self.assertTrue(vm.decode_logical_condition("CE>6"))
        self.assertTrue(vm.decode_logical_condition("CE<8"))
        self.assertTrue(vm.decode_logical_condition("CE>P1"))

        self.assertEqual(vm.error_code, 0)

    def test_5(self):
        stack_set_up = [
            "0E1U",
            "0B7U",
            "1E2U",
            "1B2U"
        ]
        opcodes_list = ["00", "2"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        vm.execute_instruction()
        vm.execute_instruction()
        self.assertFalse(vm.decode_logical_condition("CE==7"))
        self.assertEqual(vm.error_code, 5)

        self.assertFalse(vm.decode_logical_condition("CE>6"))
        self.assertEqual(vm.error_code, 5)

        self.assertFalse(vm.decode_logical_condition("CE<8"))
        self.assertEqual(vm.error_code, 5)

        self.assertFalse(vm.decode_logical_condition("CE>P1"))
        self.assertEqual(vm.error_code, 5)

    def test_6(self):
        stack_set_up = [
            "0E1U",
            "0B7U",
            "1E2U",
            "1B2U"
        ]
        opcodes_list = ["00", "2"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        vm.execute_instruction()
        self.assertTrue(vm.eval_condition("CEF&CEE|CE12|CEB&P0N"))

    def test_7(self):
        stack_set_up = [
            "0E1U",
            "0B7U",
            "1E2U",
            "1B2U"
        ]
        opcodes_list = ["7P0N", "00", "2", "11", "8"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        self.assertEqual(vm.stacks[0], [])
        self.assertEqual(vm.error_code, 0)

    def test_8(self):
        stack_set_up = [
            "0E1U",
            "0B7U",
            "0C1U",
            "0O2U",
            "1E2U",
            "1B2U",
            "2"
        ]
        opcodes_list = ["00", "7CNB&P0N", "12", "00", "8", "2"]
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        # vm.show_machine_status()
        self.assertEqual(len(vm.stacks[0]), 1)
        self.assertEqual(vm.hand.type, "B")
        self.assertEqual(vm.hand.value, 7)
        self.assertEqual(vm.error_code, 0)

    def test_9(self):
        stack_set_up = [
            "0E1U",
            "0C1U",
            "0O2U",
            "1E2U",
            "1B2U",
            "2"
        ]
        opcodes_list = ["00", "7CNB&P0N", "12", "00", "8", "2"]
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        # vm.show_machine_status()
        self.assertEqual(len(vm.stacks[0]), 0)
        self.assertEqual(vm.hand.type, "E")
        self.assertEqual(vm.hand.value, 1)

        self.assertEqual(vm.error_code, 0)

    def test_10(self):
        stack_set_up = [
            "0E1U",
            "0C1U",
            "0O2U",
            "1E2U",
            "1B2U",
            "2E12U"
        ]
        opcodes_list = ["3P2N", "02", "10", "4", "00", "11", "5"]
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        # vm.show_machine_status()

        self.assertEqual(vm.error_code, 0)

    def test_11(self):
        stack_set_up = [
            "0E1U",
            "0C1U",
            "0E7U",
            "1",
            "2"
        ]
        opcodes_list = ["7P0N", "00", "3CEE", "12", "4", "11", "5", "8"]
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        # vm.show_machine_status()

        self.assertEqual(vm.error_code, 0)

    def test_12(self):
        stack_set_up = [
            "0E1U",
            "0C1U",
            "0E7U",
            "1",
            "2"
        ]
        opcodes_list = ["3P1N", "01", "12", "4",
                        "7P0N", "00", "2", "12", "8", "5"]
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        # vm.show_machine_status()

        self.assertEqual(vm.stacks[0], [])
        self.assertEqual(vm.error_code, 0)

    def test_13(self):
        stack_set_up = [
            "0E1D",
            "0C1D",
            "0E7D",
            "1",
        ]
        opcodes_list = ["7P0N", "00", "2", "11", "8", "7P1N", "01", "10", "8"
                        ]
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.show_machine_status()
        # print("-------------")
        vm.run()
        vm.show_machine_status()

        for c in vm.stacks[0]:
            self.assertEqual(c.position, Position.FACE_UP)
        self.assertEqual(vm.stacks[1], [])
        self.assertEqual(vm.error_code, 0)

    def test_14(self):
        stack_set_up = ['0', '0E1U', '0O1U', '0B1D', '0C1D', '1', '1E2U']

        opcodes_list = ['01', '2', '10']

        vm = VirtualMachine(opcodes_list, stack_set_up)
        # vm.show_machine_status()
        # print("-------------")
        vm.run()
        # vm.show_machine_status()

        self.assertEqual(vm.stacks[1], [])
        self.assertEqual(vm.error_code, 0)


if __name__ == '__main__':
    unittest.main()
