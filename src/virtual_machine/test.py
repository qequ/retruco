import unittest
from vm import VirtualMachine
from cards import Card, Position


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
            "0E1",
            "0B1",
            "0C1",
            "0O1",
            "1E2",
            "1B2"
        ]
        opcodes_list = []

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        self.assertTrue(vm.decode_logical_condition("P1N"))
        self.assertEqual(vm.error_code, 0)

    def test_2(self):
        stack_set_up = [
            "0E1",
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
            "0E1",
            "0B1",
            "1E2",
            "1B2"
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
            "0E1",
            "0B7",
            "1E2",
            "1B2"
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
            "0E1",
            "0B7",
            "1E2",
            "1B2"
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
            "0E1",
            "0B7",
            "1E2",
            "1B2"
        ]
        opcodes_list = ["00", "2"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        vm.execute_instruction()
        self.assertTrue(vm.eval_condition("CEF&CEE|CE12|CEB&P0N"))

    def test_7(self):
        stack_set_up = [
            "0E1",
            "0B7",
            "1E2",
            "1B2"
        ]
        opcodes_list = ["7P0N", "00", "2", "11", "8"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        self.assertEqual(vm.stacks[0], [])
        self.assertEqual(vm.error_code, 0)

    def test_8(self):
        stack_set_up = [
            "0E1",
            "0B7",
            "0C1",
            "0O2",
            "1E2",
            "1B2",
            "2"
        ]
        opcodes_list = ["00", "7CNB&P0N", "12", "00", "8", "2"]
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        vm.show_machine_status()
        self.assertEqual(len(vm.stacks[0]), 1)
        self.assertEqual(vm.hand.type, "B")
        self.assertEqual(vm.hand.value, 7)
        self.assertEqual(vm.error_code, 0)

    def test_8(self):
        stack_set_up = [
            "0E1",
            "0C1",
            "0O2",
            "1E2",
            "1B2",
            "2"
        ]
        opcodes_list = ["00", "7CNB&P0N", "12", "00", "8", "2"]
        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        vm.show_machine_status()
        self.assertEqual(len(vm.stacks[0]), 0)
        self.assertEqual(vm.hand.type, "E")
        self.assertEqual(vm.hand.value, 1)

        self.assertEqual(vm.error_code, 0)


if __name__ == '__main__':
    unittest.main()
