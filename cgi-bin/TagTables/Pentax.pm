package TagTables::Pentax;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

#------------------------------------------------------------------------------
# File:         Pentax.pm
#
# Description:  Definitions for Pentax EXIF Maker Notes
#
# Revisions:    11/25/2003  - P. Harvey Created
#------------------------------------------------------------------------------

%TagTables::Pentax::Main = (
    0x0001 => {
        Name => 'PentaxMode',
        PrintConv => {
            0 => 'Auto',
            1 => 'Night-scene',
            2 => 'Manual',
        },
    },
    0x0002 => {
        Name => 'Quality',
        PrintConv => {
            0 => 'Good',
            1 => 'Better',
            2 => 'Best',
        },
    },
    0x0003 => {
        Name => 'Focus',
        PrintConv => {
            2 => 'Custom',
            3 => 'Auto',
        },
    },
    0x0004 => {
        Name => 'Flash',
        PrintConv => {
            1 => 'Auto',
            2 => 'On',
            4 => 'Off',
            6 => 'Red-eye reduction',
        },
    },
    0x0007 => {
        Name => 'WhiteBalance',
        PrintConv => {
            0 => 'Auto',
            1 => 'Daylight',
            2 => 'Shade',
            3 => 'Tungsten',
            4 => 'Fluorescent',
            5 => 'Manual',
        },
    },
    0x000a => 'Zoom',
    0x000b => {
        Name => 'Sharpness',
        PrintConv => {
            0 => 'Normal',
            1 => 'Soft',
            2 => 'Hard',
        },
    },
    0x000c => {
        Name => 'Contrast',
        PrintConv => {
            0 => 'Normal',
            1 => 'Low',
            2 => 'High',
        },
    },
    0x000d => {
        Name => 'Saturation',
        PrintConv => {
            0 => 'Normal',
            1 => 'Low',
            2 => 'High',
        },
    },
    0x0014 => {
        Name => 'PentaxISO',
        PrintConv => {
            10 => '100',
            16 => '200',
        },
    },
    0x0017 => {
        Name => 'Color',
        PrintConv => {
            1 => 'Full',
            2 => 'Black & White',
            3 => 'Sepia',
        },
    },
    0x0e00 => 'PrintIM',
    0x1000 => 'TimeZoneCity',
    0x1001 => 'DaylightSavings',
);

1; # end
