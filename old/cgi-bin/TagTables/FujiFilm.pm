package TagTables::FujiFilm;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

#------------------------------------------------------------------------------
# File:         FujiFilm.pm
#
# Description:  Definitions for FujiFilm EXIF Maker Notes
#
# Revisions:    11/25/2003  - P. Harvey Created
#------------------------------------------------------------------------------

%TagTables::FujiFilm::Main = (
    0x0    => 'Version',
    0x1000 => 'Quality',
    0x1001 => {
        Name      => 'Sharpness',
        ValueConv => '$val - 2',
        PrintConv => 'TagTables::Exif::PrintParameter($val)',
    },
    0x1002 => {
        Name      => 'WhiteBalance',
        PrintConv => {
            0    => 'Auto',
            256  => 'Daylight',
            512  => 'Cloudy',
            768  => 'DaylightColor-fluorescent',
            769  => 'DaywhiteColor-fluorescent',
            770  => 'White-fluorescent',
            1024 => 'Incandescent',
            3840 => 'Custom',
        },
    },
    0x1003 => {
        Name      => 'Saturation',
        PrintConv => {
            0   => 'Normal',
            256 => 'High',
            512 => 'Low',
        },
    },
    0x1004 => {
        Name      => 'Contrast',
        PrintConv => {
            0   => 'Normal',
            256 => 'High',
            512 => 'Low',
        },
    },
    0x1010 => {
        Name      => 'FujiFlashMode',
        PrintConv => {
            0 => 'Auto',
            1 => 'On',
            2 => 'Off',
            3 => 'Red-eye reduction',
        },
    },
    0x1011 => 'FlashStrength',
    0x1020 => {
        Name      => 'Macro',
        PrintConv => {
            0 => 'Off',
            1 => 'On',
        },
    },
    0x1021 => {
        Name      => 'FocusMode',
        PrintConv => {
            0 => 'Auto',
            1 => 'Manual',
        },
    },
    0x1030 => {
        Name      => 'SlowSync',
        PrintConv => {
            0 => 'Off',
            1 => 'On',
        },
    },
    0x1031 => {
        Name      => 'PictureMode',
        PrintConv => {
            0   => 'Auto',
            1   => 'Portrait',
            2   => 'Landscape',
            4   => 'Sports',
            5   => 'Night',
            6   => 'Program AE',
            256 => 'Aperture-priority AE',
            512 => 'Shutter speed priority AE',
            768 => 'Manual',
        },
    },
    0x1100 => {
        Name      => 'AutoBracketing',
        PrintConv => {
            0 => 'Off',
            1 => 'On',
        },
    },
    0x1300 => {
        Name      => 'BlurWarning',
        PrintConv => {
            0 => 'None',
            1 => 'Blur Warning',
        },
    },
    0x1301 => {
        Name      => 'FocusWarning',
        PrintConv => {
            0 => 'Good',
            1 => 'Out of focus',
        },
    },
    0x1302 => {
        Name      => 'ExposureWarning',
        PrintConv => {
            0 => 'Good',
            1 => 'Bad exposure',
        },
    },
);

1; # end
