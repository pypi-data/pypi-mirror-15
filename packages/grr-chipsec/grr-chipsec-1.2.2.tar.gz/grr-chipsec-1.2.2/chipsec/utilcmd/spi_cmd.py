#!/usr/local/bin/python
#CHIPSEC: Platform Security Assessment Framework
#Copyright (c) 2010-2015, Intel Corporation
# 
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; Version 2.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#Contact information:
#chipsec@intel.com
#



"""
CHIPSEC includes functionality for reading and writing the SPI flash. When an image file is created from reading the SPI flash, this image can be parsed to reveal sections, files, variables, etc.

.. warning:: Particular care must be taken when using the spi write and spi erase functions. These could make your system unbootable.

A basic forensic operation might be to dump the entire SPI flash to a file. This is accomplished as follows:

``# python chipsec_util.py spi dump rom.bin``

The file rom.bin will contain the full binary of the SPI flash. It can then be parsed using the decode util command.
"""

__version__ = '1.0'

import time

from chipsec.command    import BaseCommand
from chipsec.hal.spi    import *
from chipsec.helper.oshelper import helper


# SPI Flash Controller
class SPICommand(BaseCommand):
    """
    >>> chipsec_util spi info|dump|read|write|erase|disable-wp [flash_address] [length] [file]

    Examples:

    >>> chipsec_util spi info
    >>> chipsec_util spi dump rom.bin
    >>> chipsec_util spi read 0x700000 0x100000 bios.bin
    >>> chipsec_util spi write 0x0 flash_descriptor.bin
    >>> chipsec_util spi disable-wp
    """
    def requires_driver(self):
        if len(self.argv) < 1 or helper().is_linux():
            return False
        return True

    def run(self):
        if 1 > len(self.argv):
            print SPICommand.__doc__
            return

        try:
            _spi = SPI( self.cs )
        except SpiRuntimeError, msg:
            print msg
            return

        spi_op = self.argv[0]

        t = time.time()

        if ( 'erase' == spi_op ):
            spi_fla = int(self.argv[1],16)
            self.logger.log( "[CHIPSEC] Erasing SPI Flash block at FLA = 0x%X" % spi_fla )
            #if not _spi.disable_BIOS_write_protection():
            #    self.logger.error( "Could not disable SPI Flash protection. Still trying.." )

            ok = _spi.erase_spi_block( spi_fla )
            if ok: self.logger.log_result( "SPI Flash erase done" )
            else:  self.logger.warn( "SPI Flash erase returned error (turn on VERBOSE)" )
        elif ( 'write' == spi_op and 3 == len(self.argv) ):
            spi_fla = int(self.argv[1],16)
            filename = self.argv[2]
            self.logger.log( "[CHIPSEC] Writing to SPI Flash at FLA = 0x%X from '%.64s'" % (spi_fla, filename) )
            #if not _spi.disable_BIOS_write_protection():
            #    self.logger.error( "Could not disable SPI Flash protection. Still trying.." )

            ok = _spi.write_spi_from_file( spi_fla, filename )
            if ok: self.logger.log_result( "SPI Flash write done" )
            else:  self.logger.warn( "SPI Flash write returned error (turn on VERBOSE)" )
        elif ( 'read' == spi_op ):
            spi_fla = int(self.argv[1],16)
            length = int(self.argv[2],16)
            self.logger.log( "[CHIPSEC] Reading 0x%x bytes from SPI Flash starting at FLA = 0x%X" % (length, spi_fla) )
            out_file = None
            if 4 == len(self.argv):
                out_file = self.argv[3]
            buf = _spi.read_spi_to_file( spi_fla, length, out_file )
            if (buf is None): self.logger.error( "SPI Flash read didn't return any data (turn on VERBOSE)" )
            else: self.logger.log_result( "SPI Flash read done" )
        elif ( 'info' == spi_op ):
            self.logger.log( "[CHIPSEC] SPI Flash Info\n" )
            ok = _spi.display_SPI_map()
        elif ( 'dump' == spi_op ):
            out_file = 'rom.bin'
            if 2 == len(self.argv):
                out_file = self.argv[1]
            self.logger.log( "[CHIPSEC] Dumping entire SPI Flash to '%s'" % out_file )
            # @TODO: don't assume SPI Flash always ends with BIOS region
            (base,limit,freg) = _spi.get_SPI_region( BIOS )
            spi_size = limit + 1
            self.logger.log( "[CHIPSEC] BIOS Region: Base = 0x%08X, Limit = 0x%08X" % (base,limit) )
            self.logger.log( "[CHIPSEC] Dumping 0x%08X bytes (to the end of BIOS region)" % spi_size )
            buf = _spi.read_spi_to_file( 0, spi_size, out_file )
            if (buf is None): self.logger.error( "Dumping SPI Flash didn't return any data (turn on VERBOSE)" )
            else: self.logger.log_result( "Done dumping SPI Flash" )

        elif ( 'disable-wp' == spi_op ):
            self.logger.log( "[CHIPSEC] Trying to disable BIOS write protection.." )
            #
            # This write protection only matters for BIOS range in SPI flash memory
            #
            if _spi.disable_BIOS_write_protection():
                self.logger.log_good( "BIOS region write protection is disabled in SPI flash" )
            else:
                self.logger.log_bad( "Couldn't disable BIOS region write protection in SPI flash" )
        else:
            print SPICommand.__doc__
            return

        self.logger.log( "[CHIPSEC] (spi %s) time elapsed %.3f" % (spi_op, time.time()-t) )

commands = { 'spi': SPICommand }
