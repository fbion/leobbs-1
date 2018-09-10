package TagTables::Nikon;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

%TagTables::Nikon::nikon1_tags = (
    0x0003 => 'Quality',
    0x0004 => 'ColorMode',
    0x0005 => 'ImageAdjustment',
    0x0006 => 'CCDSensitivity',
    0x0007 => 'Whitebalance',
    0x0008 => 'Focus',
    0x000A => 'DigitalZoom',
    0x000B => 'Converter',
);

%TagTables::Nikon::nikon2_tags = (
    0x0002 => 'ISOSetting',
    0x0003 => 'ColorMode',
    0x0004 => 'Quality',
    0x0005 => 'Whitebalance',
    0x0006 => 'Sharpness',
    0x0007 => 'FocusMode',
    0x0008 => 'FlashSetting',
    0x000F => 'ISOSelection',
    0x0010 => 'DataDump',
    0x0011 => 'ThumbnailImageIFD',
    0x0080 => 'ImageAdjustment',
    0x0082 => 'AuxiliaryLens',
    0x0085 => 'ManualFocusDistance',
    0x0086 => 'DigitalZoom',
    0x0088 => {
        Name      => 'AFFocusPosition',
        PrintConv => {
            pack('xCxx', 0) => 'Center',
            pack('xCxx', 1) => 'Top',
            pack('xCxx', 2) => 'Bottom',
            pack('xCxx', 3) => 'Left',
            pack('xCxx', 4) => 'Right',
        },
    },
    0x0095 => 'NoiseReduction',
);

1; # end
