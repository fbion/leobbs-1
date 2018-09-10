package TagTables::Canon;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

#------------------------------------------------------------------------------
# File:         Canon.pm
#
# Description:  Definitions for Canon EXIF Maker notes
#
# Revisions:    11/25/2003 - P. Harvey Created
#               12/03/2003 - P. Harvey Figured out lots more tags and added
#                            CanonPictureInfo
#------------------------------------------------------------------------------

# Canon EXIF Maker Notes
%TagTables::Canon::Main = (
    0x1  => {
        Name         => 'CanonCameraSettings',
        SubDirectory => {
            Validate => 'TagTables::Canon::Validate($dirData,$subdirStart,$size)',
            TagTable => 'TagTables::Canon::CameraSettings',
            Start    => '$valuePtr',
        },
    },
    0x4  => {
        Name         => 'CanonShotInfo',
        SubDirectory => {
            Validate => 'TagTables::Canon::Validate($dirData,$subdirStart,$size)',
            TagTable => 'TagTables::Canon::ShotInfo',
            Start    => '$valuePtr',
        },
    },
    0x6  => 'CanonImageType',
    0x7  => 'CanonFirmwareVersion',
    0x8  => {
        Name      => 'FileNumber',
        PrintConv => '$_=$val,s/(\d+)(\d{4})/$1-$2/,$_',
    },
    0x9  => {
        Name        => 'OwnerName',
        Description => "Owner's Name",
    },
    0xa  => {
        Name         => 'Canon1DSettings',
        SubDirectory => {
            Validate => 'TagTables::Canon::Validate($dirData,$subdirStart,$size)',
            TagTable => 'TagTables::Canon::Canon1DSettings',
            Start    => '$valuePtr',
        },
    },
    0xc  => [ # square brackets for a conditional list
        {
            Condition   => '$::cameraModel =~ /(300D|REBEL|10D)/',
            Name        => 'SerialNumber',
            Description => 'Camera Body No.',
            PrintConv   => 'sprintf("%.10d",$val)',
        },
        {
            # no condition (all other models)
            Name        => 'SerialNumber',
            Description => 'Camera Body No.',
            PrintConv   => 'sprintf("%x-%.5d",$val>>16,$val&0xffff)',
        },
    ],
    0xe  => 'CanonFileLength',
    0xf  => [
        {
            Condition    => '$::cameraModel =~ /10D/',
            Name         => 'CanonCustomFunctions10D',
            SubDirectory => {
                Validate => 'TagTables::Canon::Validate($dirData,$subdirStart,$size)',
                TagTable => 'TagTables::CanonCustom::Functions10D',
                Start    => '$valuePtr',
            },
        },
        {
            # assume everything else is a D30/D60
            Name         => 'CanonCustomFunctions',
            SubDirectory => {
                Validate => 'TagTables::Canon::Validate($dirData,$subdirStart,$size)',
                TagTable => 'TagTables::CanonCustom::Functions',
                Start    => '$valuePtr',
            },
        },
    ],
    0x12 => {
        Name         => 'CanonPictureInfo',
        SubDirectory => {
            # the first word seems to be always 7, not the size as in other blocks
            Validate => 'TagTables::Canon::Validate($dirData,$subdirStart,7)',
            TagTable => 'TagTables::Canon::PictureInfo',
            Start    => '$valuePtr',
        },
    },
    0x90 => {
        Name         => 'CanonCustomFunctions1D',
        SubDirectory => {
            Validate => 'TagTables::Canon::Validate($dirData,$subdirStart,$size)',
            TagTable => 'TagTables::CanonCustom::Functions1D',
            Start    => '$valuePtr',
        },
    },
    0xa0 => 'CanonA0Tag',
    0xb6 => {
        Name         => 'PreviewImageInfo',
        SubDirectory => {
            # Note: first word if this block is the total number of words, not bytes!
            Validate => 'TagTables::Canon::Validate($dirData,$subdirStart,$size/2)',
            TagTable => 'TagTables::Canon::PreviewImageInfo',
            Start    => '$valuePtr',
        },
    },
);

# Canon camera settings (EXIF tag 0x01)
# BinaryData (keys are indices into the Short array)
%TagTables::Canon::CameraSettings = (
    TableType => 'BinaryData',
    1         => {
        Name      => 'MacroMode',
        PrintConv => {
            0 => 'Unknown',
            1 => 'Macro',
            2 => 'Normal',
        },
    },
    2         => {
        Name      => 'Self-timer',
        ValueConv => '$val / 10',
    },
    3         => {
        Name        => 'Quality',
        Description => 'Image Quality',
        PrintConv   => {
            2 => 'Normal',
            3 => 'Fine',
            4 => 'RAW',
            5 => 'Superfine',
        },
    },
    4         => {
        Name      => 'CanonFlashMode',
        PrintConv => {
            0  => 'Off',
            1  => 'Auto',
            2  => 'On',
            3  => 'Red-eye reduction',
            4  => 'Slow-sync',
            5  => 'Red-eye reduction (Auto)',
            6  => 'Red-eye reduction (On)',
            16 => 'External flash', # not set in D30 or 300D
        },
    },
    5         => {
        Name      => 'ContinuousDrive',
        PrintConv => {
            0 => 'Single',
            1 => 'Continuous',
        },
    },
    7         => {
        Name      => 'FocusMode',
        PrintConv => {
            0 => 'One-shot AF',
            1 => 'AI Servo AF',
            2 => 'AI Focus AF',
            3 => 'Manual Focus',
            4 => 'Single',
            5 => 'Continuous',
            6 => 'Manual Focus',
        },
    },
    10        => {
        Name      => 'CanonImageSize',
        PrintConv => {
            0 => 'Large',
            1 => 'Medium',
            2 => 'Small',
        },
    },
    11        => {
        Name      => 'EasyMode',
        PrintConv => {
            0  => 'Full auto',
            1  => 'Manual',
            2  => 'Landscape',
            3  => 'Fast shutter',
            4  => 'Slow shutter',
            5  => 'Night',
            6  => 'Black & White',
            7  => 'Sepia',
            8  => 'Portrait',
            9  => 'Sports',
            10 => 'Macro',
            11 => 'Pan focus',
        },
    },
    12        => {
        Name      => 'DigitalZoom',
        PrintConv => {
            -1 => 'Unknown',
            0  => 'None',
            1  => 'x2',
            2  => 'x4',
            3  => 'Other', # value obtained from 2*#37/#36
        },
    },
    13        => {
        Name      => 'Contrast',
        PrintConv => 'TagTables::Exif::PrintParameter($val)',
    },
    14        => {
        Name      => 'Saturation',
        PrintConv => 'TagTables::Exif::PrintParameter($val)',
    },
    15        => {
        Name      => 'Sharpness',
        PrintConv => 'TagTables::Exif::PrintParameter($val)',
    },
    16        => {
        Name      => 'CameraISO',
        PrintConv => {
            0  => 'Use shot ISO instead',
            15 => 'Auto',
            16 => '50',
            17 => '100',
            18 => '200',
            19 => '400',
        },
    },
    17        => {
        Name      => 'MeteringMode',
        PrintConv => {
            1 => 'Spot',
            3 => 'Evaluative',
            4 => 'Partial',
            5 => 'Center-weighted averaging',
        },
    },
    18        => {
        # this is always 2 for the 300D - PH
        Name      => 'FocusType',
        PrintConv => {
            0 => 'Manual',
            1 => 'Auto (1)',
            2 => 'Auto (2)',
            3 => 'Macro Mode',
            7 => 'Infinity Mode',
            8 => 'Locked (Pan Mode)',
        },
    },
    19        => {
        Name      => 'AFPoint',
        PrintConv => {
            0      => 'None (MF)',
            0x3000 => 'None (MF)',
            0x3001 => 'Auto-selected',
            0x3002 => 'Right',
            0x3003 => 'Center',
            0x3004 => 'Left',
            0x4001 => 'Auto AF point selection',
            0x2005 => 'Manual AF point selection',
        },
    },
    20        => {
        Name      => 'CanonExposureMode',
        PrintConv => {
            0 => 'Easy',
            1 => 'Program AE',
            2 => 'Shutter Speed Priority AE',
            3 => 'Aperture-Priority AE',
            4 => 'Manual',
            5 => 'Depth-of-field AE',
        },
    },
    23        => 'LongFocal',
    24        => 'ShortFocal',
    25        => 'FocalUnits',
    28        => {
        Name      => 'FlashActivity',
        PrintConv => '$val==-1 ? undef() : $val',
    },
    29        => {
        Name      => 'FlashBits',
        PrintConv => q[TagTables::Canon::DecodeBits($val,
                        {
                            3 => 'On',
                            4 => 'FP sync enabled',
                            7 => '2nd-curtain sync used',
                            11 => 'FP sync used',
                            13 => 'Internal flash',
                            14 => 'External E-TTL',
                        })
                    ],
    },
    32        => {
        Name      => 'FocusContinuous',
        PrintConv => {
            -1 => 'Unknown',
            0  => 'Single',
            1  => 'Continuous',
        },
    },
    36        => 'ZoomedResolution',
    37        => 'ZoomedResolutionBase',
    42        => {
        Name      => 'ColorTone',
        PrintConv => 'TagTables::Exif::PrintParameter($val)',
    },
);

# Canon shot information (EXIF tag 0x04)
# BinaryData (keys are indices into the Short array)
%TagTables::Canon::ShotInfo = (
    TableType => 'BinaryData',
    2         => {
        Name        => 'ISO',
        Description => 'ISO Speed',
        # lookup tables can't predict new values, so calculate ISO instead - PH
        ValueConv   => 'exp(TagTables::Canon::CanonEv($val)*log(2))*100/32',
        PrintConv   => 'sprintf("%.0f",$val)',
    },
    6         => {
        Name      => 'ExposureCompensation',
        ValueConv => 'TagTables::Canon::CanonEv($val)',
        PrintConv => 'TagTables::Exif::ConvertFraction($val)',
    },
    7         => {
        Name      => 'WhiteBalance',
        PrintConv => {
            0 => 'Auto',
            1 => 'Daylight',
            2 => 'Cloudy',
            3 => 'Tungsten',
            4 => 'Fluorescent',
            5 => 'Flash',
            6 => 'Custom',
            7 => 'Black & White',
            8 => 'Shade',
            9 => 'Manual temperature',
        },
    },
    9         => {
        Name        => 'SequenceNumber',
        Description => 'Sequence number in continuous burst',
    },
    15        => {
        Name        => 'FlashExposureComp',
        Description => 'Flash Exposure Compensation',
        ValueConv   => 'TagTables::Canon::CanonEv($val);',
        PrintConv   => 'TagTables::Exif::ConvertFraction($val)',
    },
    16        => {
        Name      => 'AutoExposureBracketing',
        PrintConv => {
            0  => 'Off',
            -1 => 'On',
        },
    },
    17        => {
        Name      => 'AEBBracketValue',
        ValueConv => 'TagTables::Canon::CanonEv($val)',
        PrintConv => 'TagTables::Exif::ConvertFraction($val)',
    },
    19        => {
        Name      => 'FocusDistanceUpper',
        ValueConv => '$val * 0.01',
    },
    20        => {
        Name      => 'FocusDistanceLower',
        ValueConv => '$val * 0.01',
    },
    21        => {
        Name        => 'FNumber',
        Description => 'Av(Aperture Value)',
        # approximate big translation table by simple calculation - PH
        ValueConv   => '$val ? exp(TagTables::Canon::CanonEv($val)*log(2)/2) : undef()',
        PrintConv   => 'sprintf("%.2g",$val);',
    },
    22        => {
        Name        => 'ExposureTime',
        Description => 'Tv(Shutter Speed)',
        # approximate big translation table by simple calculation - PH
        ValueConv   => '$val ? exp(-TagTables::Canon::CanonEv($val)*log(2)) : undef()',
        PrintConv   => 'TagTables::Exif::PrintExposureTime($val);',
    },
    24        => {
        Name      => 'BulbDuration',
        Format    => 'Long',
        ValueConv => '$val / 10',
    },
    29        => {
        Name      => 'Self-timer2',
        ValueConv => '$val / 10',
    },
);

# picture information (EXIF tag 0x12)
%TagTables::Canon::PictureInfo = (
    TableType => 'BinaryData',
    2         => 'CanonImageWidth',
    3         => 'CanonImageHeight',
    4         => 'CanonImageWidthAsShot',
    5         => 'CanonImageHeightAsShot',
    22        => {
        Name        => 'AFPointsUsed',
        Description => 'AF Points Used',
        # this works for my Rebel -- bits 6-0 correspond to focus points 1-7 respectively - PH
        PrintConv   => 'TagTables::Canon::PrintAFPoints($val)',
    },
);

# The 300D writes a 1536x1024 preview image that is accessed
# through this information - decoded by PH 12/14/03
%TagTables::Canon::PreviewImageInfo = (
    TableType => 'BinaryData',
    Format    => 'ULong',
    # the size of the preview block in 2-byte increments
    #    0 => {
    #        Name => 'PreviewImageInfoWords',
    #    },
    # this value is always 2
    #    1 => {
    #        Name => 'PreviewImageUnknown',
    #    },
    2         => 'PreviewImageLength',
    3         => 'PreviewImageWidth',
    4         => 'PreviewImageHeight',
    5         => 'PreviewImageStart',
    6         => {
        Name      => 'PreviewFocalPlaneXResolution',
        Format    => 'LongRational',
        PrintConv => 'sprintf("%.1f",$val)'
    },
    8         => {
        Name      => 'PreviewFocalPlaneYResolution',
        Format    => 'LongRational',
        PrintConv => 'sprintf("%.1f",$val)'
    },
    # the following 2 values look like they are really 4 shorts
    # taking the values of 1,4,4 and 2 respectively - don't know what they are though
    #    10 => {
    #        Name => 'PreviewImageUnknown1',
    #        PrintConv => 'sprintf("0x%x",$val)',
    #    },
    #    11 => {
    #        Name => 'PreviewImageUnknown2',
    #        PrintConv => 'sprintf("0x%x",$val)',
    #    },
);

%TagTables::Canon::Canon1DSettings = (
    TableType => 'BinaryData',
    9         => 'ColorTemperature',
    10        => 'ColorMatrix',
);

# canon composite tags
# (the main script looks for the special 'Composite' hash)
%TagTables::Canon::Composite = (
    DriveMode          => {
        Require   => {
            0 => 'ContinuousDrive',
            1 => 'Self-timer',
        },
        ValueConv => '$val[0] ? 0 : ($val[1] ? 1 : 2)',
        PrintConv => {
            0 => 'Continuous shooting',
            1 => 'Self-timer Operation',
            2 => 'Single-frame shooting',
        },
    },
    Lens               => {
        Require   => {
            0 => 'ShortFocal',
            1 => 'LongFocal',
            2 => 'FocalUnits',
        },
        ValueConv => '$val[0] / $val[2]',
        PrintConv => 'TagTables::Canon::PrintFocalRange(@val)',
    },
    Lens35efl          => {
        Description => 'Lens',
        Require     => {
            0 => 'ShortFocal',
            1 => 'LongFocal',
            2 => 'FocalUnits',
            4 => 'Lens',
        },
        Desire      => {
            3 => 'ScaleFactor35efl',
        },
        ValueConv   => '$val[4] * ($val[3] ? $val[3] : 1)',
        PrintConv   => '$valPrint[4] . ($val[3] ? sprintf(" (35mm equivalent: %s)",TagTables::Canon::PrintFocalRange(@val)) : "")',
    },
    ShootingMode       => {
        Require   => {
            0 => 'CanonExposureMode',
            1 => 'EasyMode',
        },
        ValueConv => '$val[0] ? $val[0] : $val[1] + 10',
        PrintConv => '$val[0] ? $valPrint[0] : $valPrint[1]',
    },
    FlashType          => {
        Require   => {
            0 => 'FlashBits',
        },
        ValueConv => '$val[0] ? ($val[0]&(1<<14)? 1 : 0) : undef()',
        PrintConv => {
            0 => 'Built-In Flash',
            1 => 'External',
        },
    },
    RedEyeReduction    => {
        Require   => {
            0 => 'CanonFlashMode',
            1 => 'FlashBits',
        },
        ValueConv => '$val[1] ? (($val[0]==3 or $val[0]==4 or $val[0]==6) ? 1 : 0) : undef()',
        PrintConv => {
            0 => 'Off',
            1 => 'On',
        },
    },
    # fudge to display simple Flash On/Off for Canon cameras only
    FlashOn            => {
        Description => 'Flash',
        Desire      => {
            0 => 'FlashBits',
            1 => 'Flash',
        },
        ValueConv   => 'TagTables::Canon::FlashOn(@val)',
        PrintConv   => {
            0 => 'Off',
            1 => 'On',
        },
    },
    # same as FlashExposureComp, but undefined if no flash
    ConditionalFEC     => {
        Description => 'Flash Exposure Compensation',
        Require     => {
            0 => 'FlashExposureComp',
            1 => 'FlashBits',
        },
        ValueConv   => '$val[1] ? $val[0] : undef()',
        PrintConv   => '$valPrint[0]',
    },
    # hack to assume 1st curtain unless we see otherwise
    ShutterCurtainHack => {
        Description => 'Shutter Curtain Sync',
        Desire      => {
            0 => 'ShutterCurtainSync',
        },
        Require     => {
            1 => 'FlashBits',
        },
        ValueConv   => '$val[1] ? (defined($val[0]) ? $val[0] : 0) : undef()',
        PrintConv   => {
            0 => '1st-curtain sync',
            1 => '2nd-curtain sync',
        },
    },
    PreviewImage       => {
        Require   => {
            0 => 'PreviewImageStart',
            1 => 'PreviewImageLength',
            2 => 'CanonFileLength',
        },
        ValueConv => 'ExifTool::ExtractBinary($val[0]+12,$val[1],"PreviewImage")',
        PrintConv => '"(Preview image, use -b option to extract binary)"',
    },
    PreviewImageSize   => {
        Require   => {
            0 => 'PreviewImageWidth',
            1 => 'PreviewImageHeight',
        },
        ValueConv => '"$val[0]x$val[1]"',
    },
);

#------------------------------------------------------------------------------
# Validate first word of Canon binary data
# Inputs: 0) data pointer, 1) offset, 2) value
# Returns: true if data value is the same
sub Validate($$$) {
    my ($dataPt, $offset, $val) = @_;
    # the first 16-bit value is the length of the data in words
    my $dataVal = ExifTool::Get16u($dataPt, $offset);
    return $val == $dataVal;
}

#------------------------------------------------------------------------------
# Print range of focal lengths
# Inputs: 0) short focal, 1) long focal, 2) focal units, 3) optional scaling factor
sub PrintFocalRange(@) {
    my ($short, $long, $units, $scale) = @_;

    $scale and $units /= $scale; # correct for 35efl scaling factor if given
    if ($short == $long) {
        return sprintf("%.1fmm", $short / $units);
    }
    else {
        return sprintf("%.1f - %.1fmm", $short / $units, $long / $units);
    }
}

#------------------------------------------------------------------------------
# Print auto focus points
# Inputs: 0) value to convert
sub PrintAFPoints($) {
    my $val = shift;
    my @p;
    $val & 1 << (7 - $_) and push(@p, $_) foreach (1 .. 7);
    return sprintf("%d (%s)", scalar @p, join(",", @p));
}

#------------------------------------------------------------------------------
# Decide whether flash was on or off
sub FlashOn(@) {
    my @val = @_;

    if (defined $val[0]) {
        return $val[0] ? 1 : 0;
    }
    if (defined $val[1]) {
        return $val[1] & 0x07 ? 1 : 0;
    }
    return undef;
}

#------------------------------------------------------------------------------
# Convert Canon hex-based EV (modulo 0x20) to real number
# Inputs: 0) value to convert
# ie) 0x00 -> 0
#     0x0c -> 0.33333
#     0x10 -> 0.5
#     0x14 -> 0.66666
#     0x20 -> 1   ...  etc
sub CanonEv($) {
    my $val = shift;
    my $sign;
    # temporarily make the number positive
    if ($val < 0) {
        $val = -$val;
        $sign = -1;
    }
    else {
        $sign = 1;
    }
    my $frac = $val & 0x1f;
    $val -= $frac; # remove fraction
    # Convert 1/3 and 2/3 codes
    if ($frac == 0x0c) {
        $frac = 0x20 / 3;
    }
    elsif ($frac == 0x14) {
        $frac = 0x40 / 3;
    }
    return $sign * ($val + $frac) / 0x20;
}

#------------------------------------------------------------------------------
# Decode bit mask
# Inputs: 0) value to decode, 
#         1) Reference to hash for decoding
sub DecodeBits($$) {
    my $bits = shift;
    my $lookup = shift;
    my $outStr = '';
    for (my $i = 0; $i < 32; ++$i) {
        next unless $bits & (1 << $i);
        $outStr .= ', ' if $outStr;
        if ($$lookup{$i}) {
            $outStr .= $$lookup{$i};
        }
        else {
            $outStr .= "[$i]";
        }
    }
    return $outStr || '(none)';
}

1; # end
