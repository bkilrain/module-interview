#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-

import unittest
import modules


class ModuleCase(unittest.TestCase):

    def test_1_module_operating_at_stc(self):
        '''
        Task 1: Create a (python) module with functions that describe a
        (solar) module. Load the module coefficients for the Trina TSM PA05
        from the CSV, set the temperature (T), to 25ºC and the irradiance (S)
        to 1000 W/m^2.

        This test will pass when you calculate voltage and current matching the
        correct numerical values along the (solar) module's I/V curve.
        '''

        current = modules.calculate_module_current('TSM PA05', 1000, 25, 5)
        self.assertAlmostEquals(current, 8.345847070106313)

        current = modules.calculate_module_current('TSM PA05', 1000, 25, 25)
        self.assertAlmostEquals(current, 8.276615347828452)

        current = modules.calculate_module_current('TSM PA05', 1000, 25, 34)
        self.assertAlmostEquals(current, 5.3462926879868)

    def test_2_module_operating_at_low_irradiance_high_temperature(self):
        '''
        Task 2:  Make sure your implementation produces accurate results at
        alternative irradiance and temperature levels.

        Here we used an irradiance of 600 W/m^2, and a temperature of 45ºC on
        the same Trina module as in Task 1.
        '''

        current = modules.calculate_module_current('TSM PA05', 600, 45, 5)
        self.assertAlmostEquals(current, 5.001330819496669)

        current = modules.calculate_module_current('TSM PA05', 600, 45, 15)
        self.assertAlmostEquals(current, 4.97041290811022)

        current = modules.calculate_module_current('TSM PA05', 600, 45, 30)
        self.assertAlmostEquals(current, 4.048128130946268)

    def test_3_optimize_module_power(self):
        '''
        Task 3:  Usually, we don't just need to understand what the potential
        output of a solar module is (e.g. the I/V curve), we want to find out
        what voltage and current the module should be operating at in order to
        produce the most power.

        Write a function/method that determines the voltage and current along a
        modules I/V curve that maximizes power.  We won't tell you what the
        answer is, so also write the test that proves you found it.
        '''
        (voltage, current) = modules.calculate_max_power_point('TSM PA05', 1000, 25)

        # numerically check that this is optimal
        v_high = voltage + 1e-5
        v_low = voltage - 1e-5

        i_high = modules.calculate_module_current('TSM PA05', 1000, 25, v_high)
        i_low = modules.calculate_module_current('TSM PA05', 1000, 25, v_low)

        self.assertGreater(voltage * current, v_high * i_high)
        self.assertGreater(voltage * current, v_low * i_low)


if __name__ == "__main__":
    unittest.main()
