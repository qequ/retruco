import unittest
from vm import VirtualMachine


class TestLogicDecoder(unittest.TestCase):

    def test_1(self):
        stack_set_up = [
            "01E",
            "01B",
            "01C",
            "01O",
            "12E",
            "12B"
        ]
        opcodes_list = []

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        self.assertTrue(vm.decode_logical_condition("P1N"))
        self.assertEqual(vm.error_code, 0)

    def test_2(self):
        stack_set_up = [
            "01E",
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
            "01E",
            "01B",
            "12E",
            "12B"
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
            "01E",
            "07B",
            "12E",
            "12B"
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
            "01E",
            "07B",
            "12E",
            "12B"
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
            "01E",
            "07B",
            "12E",
            "12B"
        ]
        opcodes_list = ["00", "2"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.load_stacks()
        vm.execute_instruction()
        self.assertTrue(vm.eval_condition("CEF&CEE|CE12|CEB&P0N"))

    def test_7(self):
        stack_set_up = [
            "01E",
            "07B",
            "12E",
            "12B"
        ]
        opcodes_list = ["7P0N", "00", "2", "11", "8"]

        vm = VirtualMachine(opcodes_list, stack_set_up)
        vm.run()
        self.assertEqual(vm.stacks[0], [])


if __name__ == '__main__':
    unittest.main()
