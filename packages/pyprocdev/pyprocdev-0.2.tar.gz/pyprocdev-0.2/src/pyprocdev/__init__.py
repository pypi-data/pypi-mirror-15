# Copyright (C) 2016 Anne Mulhern
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Anne Mulhern <mulhern@cs.wisc.edu>

"""
The public interface of pyprocdev.

- Constants:
    * DeviceTypes.BLOCK
    * DeviceTypes.CHARACTER

- Errors:
    ProcDevError

- Main Class:
    ProcDev
"""

from ._constants import DeviceTypes
from ._errors import ProcDevError
from ._pyprocdev import ProcDev
from ._version import __version__
