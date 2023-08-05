# Copyright 2007-2014 VPAC
#
# This file is part of python-alogger.
#
# python-alogger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-alogger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-alogger  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
import os.path

from .base import Base
from . import examples


class TestSlurm(Base, unittest.TestCase):
    file_prefix = "slurm"
    log_type = "SLURM"

    def get_cfg(self):
        directory = os.path.abspath(os.path.split(examples.__file__)[0])
        path = os.path.join(directory, self.file_prefix)

        return {
            'sacct_path': path,
            'jobid_postfix': '-m',
        }
