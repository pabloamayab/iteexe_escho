# ===========================================================================
# eXe
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================

"""
Useful Python functions
"""

import logging
import os
import os.path
import sys

log = logging.getLogger(__name__)

# ===========================================================================

#----------------------------------------------------------------------------
def deltree(path):
    """
    Will recursively delete all the files under the given path
    Redundant with Python 2.3's os.walk
    dare you to run deltree("/") !!! :-P
    """
    if os.path.isdir(path):
        children = os.listdir(path)
        for child in children:
            deltree(os.path.join(path, child))
        os.rmdir(path)

    elif os.path.isfile(path):
        os.remove(path)
    # if it's not a directory or a file, we just leave it alone

#----------------------------------------------------------------------------
def functionId(nFramesUp=1):
    """ 
    Create a string naming the function n frames up on the stack.
    http://www.nedbatchelder.com/blog/200410.html
    """
    co = sys._getframe(nFramesUp+1).f_code
    return "%s (%s @ %d)" % (co.co_name, co.co_filename, co.co_firstlineno)


#----------------------------------------------------------------------------
def get_all_files(path):
    """ 
    Recursively return all the files under a given path
    """
    if path[-1] == ':':
        path = path + '\\'
    
    try:
        for i in os.listdir(path):
            path = os.path.join(path, i)
            if os.path.isdir(path):
                for ii in get_all_files(path):
                    yield ii
            else:
                yield path
    except:
        pass
      
# ===========================================================================
