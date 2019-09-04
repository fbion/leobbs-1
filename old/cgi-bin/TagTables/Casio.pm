package TagTables::Casio;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

%TagTables::Casio::Main = (
    0x0001 => {
        Name      => 'RecordingMode',
        PrintConv => {
            1 => 'SingleShutter',
            2 => 'Panorama',
            3 => 'Night scene',
            4 => 'Portrait',
            5 => 'Landscape',
        },
    },
    0x0002 => {
        Name      => 'Quality',
        PrintConv => { 1 => 'Economy', 2 => 'Normal', 3 => 'Fine' },
    },
    0x0003 => {
        Name      => 'FocusMode',
        PrintConv => {
            2 => 'Macro',
            3 => 'Auto',
            4 => 'Manual',
            5 => 'Infinity',
        },
    },
    0x0004 => {
        Name      => 'FlashMode',
        PrintConv => { 1 => 'Auto', 2 => 'On', 3 => 'Off', 4 => 'Red-eye reduction' },
    },
    0x0005 => {
        Name      => 'FlashIntensity',
        PrintConv => { 11 => 'Weak', 13 => 'Normal', 15 => 'Strong' },
    },
    0x0006 => 'ObjectDistance',
    0x0007 => {
        Name      => 'WhiteBalance',
        PrintConv => {
            1   => 'Auto',
            2   => 'Tungsten',
            3   => 'Daylight',
            4   => 'Fluorescent',
            5   => 'Shade',
            129 => 'Manual',
        },
    },
    0x000a => {
        Name      => 'DigitalZoom',
        PrintConv => { 65536 => 'Off', 65537 => '2X' },
    },
    0x000b => {
        Name      => 'Sharpness',
        PrintConv => { 0 => 'Normal', 1 => 'Soft', 2 => 'Hard' },
    },
    0x000c => {
        Name      => 'Contrast',
        PrintConv => { 0 => 'Normal', 1 => 'Low', 2 => 'High' },
    },
    0x000d => {
        Name      => 'Saturation',
        PrintConv => { 0 => 'Normal', 1 => 'Low', 2 => 'High' },
    },
    0x0014 => {
        Name      => 'CCDSensitivity',
        PrintConv => {
            64  => 'Normal',
            125 => '+1.0',
            250 => '+2.0',
            244 => '+3.0',
            80  => 'Normal',
            100 => 'High',
        },
    },
);

1; # end
