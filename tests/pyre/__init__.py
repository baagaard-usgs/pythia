# ======================================================================
#
# Brad T. Aagaard, U.S. Geological Survey
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2017 University of California, Davis
#
# See COPYING for license information.
#
# ======================================================================
#

import test_units
import test_inventory
import test_schedulers

def test_cases():
    tests = []
    for mod in [test_units, test_inventory, test_schedulers]:
        tests += mod.test_classes()
    return tests


# End of file