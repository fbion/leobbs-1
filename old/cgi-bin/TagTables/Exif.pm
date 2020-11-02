package TagTables::Exif;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

#------------------------------------------------------------------------------
# File:         Exif.pm
#
# Description:  Definitions for EXIF tags
#
# Revisions:    11/25/2003 - P. Harvey Created
#------------------------------------------------------------------------------

# main EXIF tag table
%TagTables::Exif::Main = (
    0x1    => {
        Name         => 'InteropIndex',
        Description  => 'Interoperability Index',
        SubDirectory => {
            Start    => '$dirBase',
            OffsetPt => '$valuePtr',
        },
    },
    0x2    => {
        Name        => 'InteropVersion',
        Description => 'Interoperability Version',
    },
    0x100  => {
        Name        => 'ImageWidth',
        Description => 'Width of Image',
    },
    0x101  => {
        Name        => 'ImageHeight',
        Description => 'Height of Image',
    },
    0x102  => 'BitsPerSample',
    0x103  => {
        Name      => 'Compression',
        PrintConv => {
            1     => 'Uncompressed',
            2     => 'CCITT 1D',
            3     => 'Group 3 Fax',
            4     => 'Group 4 Fax',
            5     => 'LZW',
            6     => 'JPEG',
            32773 => 'PackBits',
        },
    },
    0x106  => {
        Name      => 'PhotometricInterpretation',
        PrintConv => {
            0 => 'WhiteIsZero',
            1 => 'BlackIsZero',
            2 => 'RGB',
            3 => 'RGB Palette',
            4 => 'Tansparency mask',
            5 => 'CMYK',
            6 => 'YCbCr',
            8 => 'CIELab',
        },
    },
    0x10a  => 'FillOrder',
    0x10d  => 'DocumentName',
    0x10e  => 'ImageDescription',
    0x10f  => {
        Name      => 'Make',
        ValueConv => '($::cameraMake = $val) =~ s/\0.*//, $val',
    },
    0x110  => {
        Name        => 'Model',
        Description => 'Camera Model Name',
        # truncate string at null terminator if it exists
        ValueConv   => '($::cameraModel = $val) =~ s/\0.*//, $val',
    },
    0x111  => 'StripOffsets',
    0x112  => {
        Name      => 'Orientation',
        PrintConv => {
            1 => 'Horizontal (normal)',
            2 => 'Mirrored horizontal',
            3 => 'Rotated 180',
            4 => 'Mirrored vertical',
            5 => 'Mirrored horizontal then rotated 90 CCW',
            6 => 'Rotated 90 CW',
            7 => 'Mirrored horizontal then rotated 90 CW',
            8 => 'Rotated 90 CCW',
        },
    },
    0x115  => 'SamplesPerPixel',
    0x116  => 'RowsPerStrip',
    0x117  => 'StripByteCounts',
    0x11a  => 'XResolution',
    0x11b  => 'YResolution',
    0x11c  => {
        Name      => 'PlanarConfiguration',
        PrintConv => {
            1 => 'Chunky',
            2 => 'Planar',
        },
    },
    0x128  => {
        Name      => 'ResolutionUnit',
        PrintConv => {
            1 => 'None',
            2 => 'inches',
            3 => 'cm',
        },
    },
    0x12d  => 'TransferFunction',
    0x131  => 'Software',
    0x132  => {
        Name        => 'ModifyDate',
        Description => 'Date/Time of last modification',
        PrintConv   => 'ExifTool::ConvertExifDate($val)',
    },
    0x13b  => 'Artist',
    0x13e  => 'WhitePoint',
    0x13f  => 'PrimaryChromaticities',
    0x156  => 'TransferRange',
    0x200  => 'JPEGProc',
    0x201  => {
        Name      => 'ThumbnailOffset',
        # save the offset for later use
        ValueConv => '$::thumb_offset = $val',
    },
    0x202  => {
        Name      => 'ThumbnailLength',
        # save the thumbnail data
        ValueConv => '$::thumb_data=substr($$dataPt,$::thumb_offset,$val), $val',
    },
    0x211  => 'YCbCrCoefficients',
    0x212  => {
        Name      => 'YCbCrSubSampling',
        PrintConv => {
            1 => 'YCbCr4:2:2',
            2 => 'YCbCr4:2:0',
        },
    },
    0x213  => {
        Name      => 'YCbCrPositioning',
        PrintConv => {
            1 => 'Centered',
            2 => 'Co-sited',
        },
    },
    0x214  => 'ReferenceBlackWhite',
    0x2bc  => {
        Name         => 'ApplicationNotes',
        # this could be an XMP block
        SubDirectory => {
            TagTable => 'TagTables::XMP::Main',
            Start    => '$valuePtr',
        },
    },
    0x1000 => 'RelatedImageFileFormat',
    0x1001 => 'RelatedImageWidth',
    0x1002 => 'RelatedImageLength',
    0x828d => 'CFARepeatPatternDim',
    0x828e => 'CFAPattern2',
    0x828f => 'BatteryLevel',
    0x8298 => 'Copyright',
    0x829a => {
        Name        => 'ExposureTime',
        Description => 'Tv(Shutter Speed)',
        PrintConv   => 'TagTables::Exif::PrintExposureTime($val)',
    },
    0x829d => {
        Name        => 'FNumber',
        Description => 'Av(Aperture Value)',
        PrintConv   => 'sprintf("%.1f",$val)',
    },
    # this is too big to display
    #    0x83bb => {
    #        Name => 'IPTC/NAA',
    #    },
    0x8769 => {
        Name         => 'ExifOffset',
        SubDirectory => {
            Start    => '$dirBase',
            OffsetPt => '$valuePtr',
        },
    },
    # don't want to print all this because it is a big table
    #    0x8773 => {
    #        Name => 'InterColorProfile',
    #    },
    0x8822 => {
        Name      => 'ExposureProgram',
        PrintConv => {
            1 => 'Manual',
            2 => 'Program AE',
            3 => 'Aperture-priority AE',
            4 => 'Shutter speed priority AE',
            5 => 'Creative (Slow speed)',
            6 => 'Action (High speed)',
            7 => 'Portrait',
            8 => 'Landscape',
        },
    },
    0x8824 => 'SpectralSensitivity',
    0x8825 => {
        Name         => 'GPSInfo',
        SubDirectory => {
            TagTable => 'TagTables::GPS::Main',
            Start    => '$dirBase',
            OffsetPt => '$valuePtr',
        },
    },
    0x8827 => {
        Name        => 'ISO',
        Description => 'ISO Speed',
    },
    0x8828 => 'OECF',
    0x9000 => 'ExifVersion',
    0x9003 => {
        Name        => 'DateTimeOriginal',
        Description => 'Shooting Date/Time',
        PrintConv   => 'ExifTool::ConvertExifDate($val)',
    },
    0x9004 => {
        Name        => 'CreateDate',
        Description => 'Date/Time of digitization',
        PrintConv   => 'ExifTool::ConvertExifDate($val)',
    },
    0x9101 => {
        Name      => 'ComponentsConfiguration',
        PrintConv => '$_=$val;tr/\x01-\x06/YbrRGB/;s/b/Cb/g;s/r/Cr/g;return $_',
    },
    0x9102 => 'CompressedBitsPerPixel',
    0x9201 => {
        Name      => 'ShutterSpeedValue',
        ValueConv => 'abs($val)<100 ? 1/(2**$val) : 0',
        PrintConv => 'TagTables::Exif::PrintExposureTime($val)',
    },
    0x9202 => {
        Name      => 'ApertureValue',
        ValueConv => 'sqrt(2) ** $val',
        PrintConv => 'sprintf("%.1f",$val)',
    },
    0x9203 => 'BrightnessValue',
    0x9204 => {
        Name      => 'ExposureCompensation',
        PrintConv => 'TagTables::Exif::ConvertFraction($val)',
    },
    0x9205 => {
        Name      => 'MaxApertureValue',
        ValueConv => 'sqrt(2) ** $val',
        PrintConv => 'sprintf("%.1f",$val)',
    },
    0x9206 => {
        Name      => 'SubjectDistance',
        PrintConv => '"$val m"',
    },
    0x9207 => {
        Name      => 'MeteringMode',
        PrintConv => {
            0   => 'Unknown',
            1   => 'Average',
            2   => 'Center-weighted average',
            3   => 'Spot',
            4   => 'Multi-spot',
            5   => 'Multi-segment',
            6   => 'Partial',
            255 => 'Other',
        },
    },
    0x9208 => {
        Name      => 'LightSource',
        PrintConv => {
            0   => 'Unknown',
            1   => 'Daylight',
            2   => 'Fluorescent',
            3   => 'Tungsten',
            10  => 'Flash',
            17  => 'Standard light A',
            18  => 'Standard light B',
            19  => 'Standard light C',
            20  => 'D55',
            21  => 'D65',
            22  => 'D75',
            23  => 'D50',
            24  => 'ISO Studio tungsten',
            255 => 'Other',
        },
    },
    0x9209 => {
        Name      => 'Flash',
        PrintConv => {
            0x00 => 'No Flash',
            0x01 => 'Fired',
            0x05 => 'Fired, Return not detected',
            0x07 => 'Fired, Return detected',
            0x09 => 'On',
            0x0d => 'On, Return not detected',
            0x0f => 'On, Return detected',
            0x10 => 'Off',
            0x18 => 'Auto, Did not fire',
            0x19 => 'Auto, Fired',
            0x1d => 'Auto, Fired, Return not detected',
            0x1f => 'Auto, Fired, Return detected',
            0x20 => 'No flash function',
            0x41 => 'Fired, Red-eye reduction',
            0x45 => 'Fired, Red-eye reduction, Return not detected',
            0x47 => 'Fired, Red-eye reduction, Return detected',
            0x49 => 'On, Red-eye reduction',
            0x4d => 'On, Red-eye reduction, Return not detected',
            0x4f => 'On, Red-eye reduction, Return detected',
            0x59 => 'Auto, Fired, Red-eye reduction',
            0x5d => 'Auto, Fired, Red-eye reduction, Return not detected',
            0x5f => 'Auto, Fired, Red-eye reduction, Return detected',
        },
    },
    0x920a => {
        Name      => 'FocalLength',
        PrintConv => 'sprintf("%.1fmm",$val)',
    },
    #----------------------------------------------------------------------------
    # decide which MakerNotes to use (based on camera make/orm_model)
    #
    0x927c => [ # square brackets for a conditional list
        {
            Condition    => '$::cameraMake =~ /^Canon/',
            Name         => 'MakerNoteCanon',
            SubDirectory => {
                TagTable => 'TagTables::Canon::Main',
                Start    => '$valuePtr',
            },
        },
        {
            # The Fuji programmers really botched this one up,
            # but with a bit of work we can still read this directory
            Condition    => '$::cameraMake =~ /^FUJIFILM/',
            Name         => 'MakerNoteFujiFilm',
            SubDirectory => {
                TagTable  => 'TagTables::FujiFilm::Main',
                Start     => '$valuePtr',
                # there is an 8-byte maker tag (FUJIFILM) we must skip over
                OffsetPt  => '$valuePtr+8',
                ByteOrder => 'LittleEndian',
                # the pointers are relative to the subdirectory start
                # (before adding the offsetPt).  Weird - PH
                Base      => '$start',
            },
        },
        {
            Condition    => '$::cameraMake =~ /^PENTAX/',
            Name         => 'MakerNotePentax',
            SubDirectory => {
                TagTable  => 'TagTables::Pentax::Main',
                Start     => '$valuePtr+6',
                ByteOrder => 'BigEndian',
            },
        },
        {
            Condition    => '$::cameraMake =~ /^OLYMPUS/',
            Name         => 'MakerNoteOlympus',
            SubDirectory => {
                TagTable => 'TagTables::Olympus::Main',
                Start    => '$valuePtr+8',
            },
        },
        {
            Condition    => '$::cameraMake=~/^NIKON/ and $::cameraModel=~/^(E700|E800|E900|E900S|E910|E950)$/',
            Name         => 'MakerNoteNikon1',
            SubDirectory => {
                TagTable => 'TagTables::Nikon::nikon1_tags',
                Start    => '$valuePtr+8',
            },
        },
        {
            Condition    => '$::cameraMake=~/^NIKON/',
            Name         => 'MakerNoteNikon2',
            SubDirectory => {
                TagTable => 'TagTables::Nikon::nikon2_tags',
                Start    => '$valuePtr',
            },
        },
        {
            Condition    => '$::cameraMake=~/^CASIO/',
            Name         => 'MakerNoteCasio',
            SubDirectory => {
                TagTable => 'TagTables::Casio::Main',
                Start    => '$valuePtr',
            },
        },
        {
            Name => 'MakerNoteUnknown',
        },
    ],
    #----------------------------------------------------------------------------
    0x9286 => 'UserComment',
    0x9290 => 'SubSecTime',
    0x9291 => 'SubSecTimeOriginal',
    0x9292 => 'SubSecTimeDigitized',
    0xa000 => 'FlashPixVersion',
    0xa001 => {
        Name      => 'ColorSpace',
        PrintConv => {
            1      => 'sRGB',
            2      => 'Adobe RGB',
            0xffff => 'Uncalibrated',
        },
    },
    0xa002 => 'ExifImageWidth',
    0xa003 => 'ExifImageLength',
    0xa004 => 'RelatedSoundFile',
    0xa005 => 'InteroperabilityOffset',
    0xa20b => 'FlashEnergy',
    0xa20c => 'SpatialFrequencyResponse',
    0xa20e => 'FocalPlaneXResolution',
    0xa20f => 'FocalPlaneYResolution',
    0xa210 => {
        Name      => 'FocalPlaneResolutionUnit',
        ValueConv => {
            1 => '25.4',
            2 => '25.4',
            3 => '10',
            4 => '1',
            5 => '0.001',
        },
        PrintConv => {
            25.4  => 'inches',
            10    => 'cm',
            1     => 'mm',
            0.001 => 'um',
        },
    },
    0xa214 => 'SubjectLocation',
    0xa215 => 'ExposureIndex',
    0xa217 => {
        Name      => 'SensingMethod',
        PrintConv => {
            1 => 'Not defined',
            2 => 'One-chip color area',
            3 => 'Two-chip color area',
            4 => 'Three-chip color area',
            5 => 'Color sequential area',
            7 => 'Trilinear',
            8 => 'Color sequential linear',
        },
    },
    0xa300 => {
        Name      => 'FileSource',
        PrintConv => { 3 => 'Digital Camera', },
    },
    0xa301 => {
        Name      => 'SceneType',
        PrintConv => { 1 => 'Directly photographed', },
    },
    0xa302 => 'CFAPattern',
    0xa401 => {
        Name      => 'CustomRendered',
        PrintConv => {
            0 => 'Normal',
            1 => 'Custom',
        },
    },
    0xa402 => {
        Name      => 'ExposureMode',
        PrintConv => {
            0 => 'Auto',
            1 => 'Manual',
            2 => 'Auto bracket',
        },
    },
    0xa403 => {
        Name      => 'WhiteBalance',
        Condition => 'not defined($oldVal)', # don't override maker WhiteBalance
        PrintConv => {
            0 => 'Auto',
            1 => 'Manual',
        },
    },
    0xa404 => 'DigitalZoomRatio',
    0xa405 => 'FocalLengthIn35mmFormat',
    0xa406 => {
        Name      => 'SceneCaptureType',
        PrintConv => {
            0 => 'Standard',
            1 => 'Landscape',
            2 => 'Portrait',
            3 => 'Night',
        },
    },
    0xa407 => {
        Name      => 'GainControl',
        PrintConv => {
            0 => 'None',
            1 => 'Low gain up',
            2 => 'High gain up',
            3 => 'Low gain down',
            4 => 'High gain down',
        },
    },
    0xa408 => {
        Name      => 'Contrast',
        PrintConv => 'TagTables::Exif::PrintParameter($val)',
    },
    0xa409 => {
        Name      => 'Saturation',
        PrintConv => 'TagTables::Exif::PrintParameter($val)',
    },
    0xa40a => {
        Name      => 'Sharpness',
        PrintConv => 'TagTables::Exif::PrintParameter($val)',
    },
    0xa40b => 'DeviceSettingDescription',
    0xa40c => {
        Name      => 'SubjectDistanceRange',
        PrintConv => {
            1 => 'Macro',
            2 => 'Close',
            3 => 'Distant',
        },
    },
    0xa420 => 'ImageUniqueID',
);

# the Composite tags are evaluated last, and are used
# to calculate values based on the other tags
# (the main script looks for the special 'Composite' hash)
%TagTables::Exif::Composite = (
    ImageSize        => {
        Require   => {
            0 => 'ImageWidth',
            1 => 'ImageHeight',
        },
        ValueConv => '"$val[0]x$val[1]"',
    },
    # pick the best shutter speed value
    ShutterSpeed     => {
        Description => 'Tv(Shutter Speed)',
        Desire      => {
            0 => 'ExposureTime',
            1 => 'ShutterSpeedValue',
            2 => 'BulbDuration',
        },
        ValueConv   => '$val[2] ? $val[2] : (defined($val[0]) ? $val[0] : $val[1])',
        PrintConv   => 'TagTables::Exif::PrintExposureTime($val)',
    },
    Aperture         => {
        Description => 'Av(Aperture Value)',
        Desire      => {
            0 => 'FNumber',
            1 => 'ApertureValue',
        },
        ValueConv   => '$val[0] ? $val[0] : $val[1]',
        PrintConv   => 'sprintf("%.1f",$val)',
    },
    FocalLength35efl => {
        Description => 'Focal Length',
        Require     => {
            0 => 'FocalLength',
        },
        Desire      => {
            1 => 'ScaleFactor35efl',
        },
        ValueConv   => '$val[0] * ($val[1] ? $val[1] : 1)',
        PrintConv   => '$val[1] ? sprintf("%.1fmm (35mm equivalent: %.1fmm)", $val[0], $val) : sprintf("%.1fmm", $val)',
    },
    ThumbnailImage   => {
        Require   => {
            0 => 'ThumbnailOffset',
            1 => 'ThumbnailLength',
        },
        ValueConv => '$::thumb_data',
        PrintConv => '"(Thumbnail image)"',
    },
    ScaleFactor35efl => {
        Description => 'Scale Factor to 35mm Equivalent',
        Desire      => {
            0  => 'FocalLength',
            1  => 'FocalLengthIn35mmFormat',
            2  => 'FocalPlaneResolutionUnit',
            3  => 'FocalPlaneXResolution',
            4  => 'FocalPlaneYResolution',
            5  => 'CanonImageWidthAsShot',
            6  => 'CanonImageHeightAsShot',
            7  => 'ExifImageWidth',
            8  => 'ExifImageLength',
            9  => 'ImageWidth',
            10 => 'ImageHeight',
        },
        ValueConv   => 'TagTables::Exif::CalcScaleFactor35efl(@val)',
        PrintConv   => 'sprintf("%.1f", $val)',
    },
);

# this is a special table used to define command-line shortcuts
%TagTables::Exif::Shortcuts = (
    Common => [ 'FileName',
        'FileSize',
        'Model',
        'DateTimeOriginal',
        'ImageSize',
        'Quality',
        'FocalLength',
        'ShutterSpeed',
        'Aperture',
        'ISO',
        'WhiteBalance',
        'Flash',
    ],
    Canon  => [ 'FileName',
        'Model',
        'DateTimeOriginal',
        'ShootingMode',
        'ShutterSpeed',
        'Aperture',
        'MeteringMode',
        'ExposureCompensation',
        'ISO',
        'Lens',
        'FocalLength',
        'ImageSize',
        'Quality',
        'FlashOn',
        'FlashType',
        'ConditionalFEC',
        'RedEyeReduction',
        'ShutterCurtainHack',
        'WhiteBalance',
        'FocusMode',
        'Contrast',
        'Sharpness',
        'Saturation',
        'ColorTone',
        'FileSize',
        'FileNumber',
        'DriveMode',
        'OwnerName',
        'SerialNumber',
    ],
);

#------------------------------------------------------------------------------
# Calculate scale factor for 35mm effective focal length
# Inputs: 0) Focal length
#         1) Focal length in 35mm format
#         2) focal plane resolution units (in mm)
#         3/4) Focal plane X/Y resolution
#         5/6,7/8...) Image width/height in order of precidence (first valid pair is used)
# Returns: 35mm conversion factor (or undefined if it can't be calculated)
sub CalcScaleFactor35efl {
    my $focal = shift;
    my $foc35 = shift;

    return $foc35 / $focal if $focal and $foc35;

    my $units = shift || return undef;
    my $x_res = shift || return undef;
    my $y_res = shift || return undef;
    my ($w, $h);
    for (;;) {
        @_ < 2 and return undef;
        $w = shift;
        $h = shift;
        last if $w and $h;
    }
    # calculate focal plane size in mm
    $w *= $units / $x_res;
    $h *= $units / $y_res;
    return sqrt(36 * 36 + 24 * 24) / sqrt($w * $w + $h * $h);
}

#------------------------------------------------------------------------------
# Convert exposure compensation fraction
#
sub ConvertFraction($) {
    my $val = shift;
    my $str;
    if (defined $val) {
        $val *= 1.00001; # avoid round-off errors
        if (not $val) {
            $str = '0';
        }
        elsif (int($val) / $val > 0.999) {
            $str = sprintf("%+d", int($val));
        }
        elsif ((int($val * 2)) / ($val * 2) > 0.999) {
            $str = sprintf("%+d/2", int($val * 2));
        }
        elsif ((int($val * 3)) / ($val * 3) > 0.999) {
            $str = sprintf("%+d/3", int($val * 3));
        }
        else {
            $str = sprintf("%.3g", $val);
        }
    }
    return $str;
}

#------------------------------------------------------------------------------
# Print parameter value (with sign, or 'Normal' for zero)
sub PrintParameter($) {
    my $val = shift;
    if ($val > 0) {
        $val = "+$val";
    }
    elsif ($val == 0) {
        $val = 'Normal';
    }
    return $val;
}

#------------------------------------------------------------------------------
# Print exposure time as a fraction
sub PrintExposureTime($) {
    my $secs = shift;
    if ($secs < 0.25001) {
        return sprintf("1/%d", int(0.5 + 1 / $secs));
    }
    $_ = sprintf("%.1f", $secs);
    s/\.0$//;
    return $_;
}


1; # end
