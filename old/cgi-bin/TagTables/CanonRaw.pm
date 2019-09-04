#------------------------------------------------------------------------------
# File:         CanonRaw.pm
#
# Description:  Definitions for Canon CRW file information
#
# Revisions:    11/25/2003 - P. Harvey Created
#               12/02/2003 - P. Harvey Completely reworked and figured out many
#                            more tags
#               01/19/2004 - P. Harvey Added CleanRaw()
#------------------------------------------------------------------------------
package TagTables::CanonRaw;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

use ExifTool qw{SetByteOrder Get16u Get32u};

$VERSION = '1.00';

sub ProcessRawDir($$$$);

# Canon raw file tag table 
%TagTables::CanonRaw::Main = (
    0x0032 => 'CanonColorInfo1',
    0x0805 => 'CanonFileDescription',
    0x080a => {
        Name         => 'CanonRawMakeModel',
        SubDirectory => {
            TagTable => 'TagTables::CanonRaw::MakeModel',
        },
    },
    0x080b => 'CanonFirmwareVersion',
    0x0810 => 'OwnerName',
    0x0815 => 'CanonFileType',
    0x0816 => 'OriginalFileName',
    0x0817 => 'ThumbnailFileName',
    0x102a => {
        Name         => 'CanonShotInfo',
        SubDirectory => {
            TagTable => 'TagTables::Canon::ShotInfo',
        },
    },
    0x102c => 'CanonColorInfo2',
    0x102d => {
        Name         => 'CanonCameraSettings',
        SubDirectory => {
            TagTable => 'TagTables::Canon::CameraSettings',
        },
    },
    0x1031 => {
        Name         => 'RawImageSize',
        SubDirectory => {
            TagTable => 'TagTables::CanonRaw::ImageSize',
        },
    },
    0x1033 => {
        Name         => 'CanonCustomFunctions10D',
        SubDirectory => {
            TagTable => 'TagTables::CanonCustom::Functions10D',
        },
    },
    0x1038 => {
        Name         => 'CanonPictureInfo',
        SubDirectory => {
            TagTable => 'TagTables::Canon::PictureInfo',
        },
    },
    0x10a9 => {
        Name         => 'WhiteBalanceTable',
        SubDirectory => {
            TagTable => 'TagTables::CanonRaw::WhiteBalance',
        },
    },
    0x10b4 => {
        Name      => 'ColorSpace',
        ValueConv => 'Get16u(\$val,0)',
        PrintConv => {
            1      => 'sRGB',
            2      => 'Adobe RGB',
            0xffff => 'Uncalibrated',
        },
    },
    0x180e => {
        Name         => 'CanonRawDateData',
        SubDirectory => {
            TagTable => 'TagTables::CanonRaw::DateData',
        },
    },
    0x1810 => {
        Name         => 'CanonRawRotation',
        SubDirectory => {
            TagTable => 'TagTables::CanonRaw::Rotation',
        },
    },
    # no useful information to print in this (large-ish) field
    #    0x1835 => {
    #        Name => 'DecoderTable',
    #    },
    #    0x2005 => {
    #        Name => 'RawData',
    #    },
    0x2007 => {
        Name      => 'JpgFromRaw',
        PrintConv => '"(JPG in RAW file, use -b to extract binary)"',
    },
    0x5029 => {
        Name      => 'FocalLength',
        ValueConv => '$val >> 16',
        PrintConv => 'sprintf("%.1fmm",$val)',
    },
    0x580b => {
        Name        => 'SerialNumber',
        Description => 'Camera Body No.',
        PrintConv   => 'sprintf("%.10d",$val)',
    },
    0x5817 => {
        Name      => 'FileNumber',
        PrintConv => '$_=$val,s/(\d+)(\d=> {4},)/$1-$2/,$_',
    },
);

# Canon binary data blocks
%TagTables::CanonRaw::MakeModel = (
    TableType => 'BinaryData',
    Format    => 'String',
    0         => {
        Name   => 'Make',
        Format => 'String[5]',
    },
    6         => {
        Name        => 'Model',
        Format      => 'String[32]',
        Description => 'Camera Model Name',
        ValueConv   => '$_=$val,s/\0.*/\0/,$_', # remove junk at end of string
    },
);

%TagTables::CanonRaw::DateData = (
    TableType => 'BinaryData',
    0         => {
        Name        => 'DateTimeOriginal',
        Format      => 'ULong',
        Description => 'Shooting Date/Time',
        ValueConv   => 'TagTables::CanonRaw::ConvertBinaryDate($val)',
        PrintConv   => 'ExifTool::ConvertExifDate($val)',
    },
);

%TagTables::CanonRaw::ImageSize = (
    TableType => 'BinaryData',
    Format    => 'Short',
    1         => 'ImageWidth',
    2         => 'ImageHeight',
);

%TagTables::CanonRaw::Rotation = (
    TableType => 'BinaryData',
    6         => 'Rotation',
);

# these values are potentially useful to users of dcraw...
%TagTables::CanonRaw::WhiteBalance = (
    TableType => 'BinaryData',
    1         => {
        Name      => 'RedBalanceAuto',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    3         => {
        Name      => 'BlueBalanceAuto',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    5         => {
        Name      => 'RedBalanceDaylight',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    7         => {
        Name      => 'BlueBalanceDaylight',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    9         => {
        Name      => 'RedBalanceCloudy',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    11        => {
        Name      => 'BlueBalanceCloudy',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    13        => {
        Name      => 'RedBalanceTungsten',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    15        => {
        Name      => 'BlueBalanceTungsten',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    17        => {
        Name      => 'RedBalanceFluorescent',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    19        => {
        Name      => 'BlueBalanceFluorescent',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    21        => {
        Name      => 'RedBalanceFlash',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    23        => {
        Name      => 'BlueBalanceFlash',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    25        => {
        Name      => 'RedBalanceCustom',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    27        => {
        Name      => 'BlueBalanceCustom',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    29        => {
        Name      => 'RedBalanceB&W',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    31        => {
        Name      => 'BlueBalanceB&W',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    33        => {
        Name      => 'RedBalanceShade',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
    35        => {
        Name      => 'BlueBalanceShade',
        Format    => 'ShortRational',
        PrintConv => 'sprintf("%.5f",$val);',
    },
);

#------------------------------------------------------------------------------
# Convert binary date to string
# Inputs: 0) Long date value
sub ConvertBinaryDate($) {
    my $time = shift;
    my @time = gmtime($time);
    return sprintf("%4d:%.2d:%.2d %.2d:%.2d:%.2d",
        $time[5] + 1900, $time[4] + 1, $time[3],
        $time[2], $time[1], $time[0]);
}

#------------------------------------------------------------------------------
# Do the work for CleanRaw()
# Inputs: I'm not gonna tell because you shouldn't call this routine
# Notes:  This routine should be called only from CleanRaw() below
sub _doCleanRaw($$$$$$) {
    my $infile = shift;
    my $outfile = shift;
    my $in_place = shift;
    my $inref = shift;
    my $outref = shift;
    my $outJpgLen = shift;
    my ($buff, $sig, $mainDir);
    my ($jpgLen, $jpgPtr);
    my ($pk16, $pk32);

    open(RAW, $infile) or return 6;
    binmode(RAW);
    $$inref = \*RAW; # save file reference for cleanup

    read(RAW, $buff, 2) or return 1; # get byte order
    SetByteOrder($buff) or return 2;
    # set order for repacking binary data
    if ($buff eq 'MM') {
        $pk16 = 'n'; # big endian (Motorola/Network order)
        $pk32 = 'N';
    }
    else {
        $pk16 = 'v'; # little endian (Intel/Vax order)
        $pk32 = 'V'
    }
    read(RAW, $buff, 4) or return 1; # get pointer to start of first block
    read(RAW, $sig, 8) or return 1;  # get file signature
    $sig eq "HEAPCCDR" or return 3;  # validate signature
    my $blockStart = Get32u(\$buff);
    seek(RAW, 0, 2) or return 4;          # seek to end of file
    my $blockEnd = tell(RAW) or return 5; # get file size (end of main block)
    seek(RAW, $blockEnd - 4, 0) or return 4;
    read(RAW, $buff, 4) or return 1; # get offset to directory start
    my $dirStart = Get32u(\$buff) + $blockStart;
    seek(RAW, $dirStart, 0) or return 4;
    read(RAW, $buff, 2) or return 1;
    my $dirEntries = Get16u(\$buff);                   # number of directory entries
    read(RAW, $mainDir, $dirEntries * 10) or return 1; # read entire directory
    for (my $i = 0; $i < $dirEntries; ++$i) {
        my $offset = $i * 10;
        my $tag = Get16u(\$mainDir, $offset);
        next unless $tag == 0x2007; # look for JPG tag
        $jpgLen = Get32u(\$mainDir, $offset + 2);
        $jpgPtr = Get32u(\$mainDir, $offset + 6) + $blockStart;
        $$outJpgLen = $jpgLen; # we found the embedded JPG!
        last;
    }
    # nothing to do if outfile is the same as infile and no JPG data
    return 0 if $in_place and not $jpgLen;

    seek(RAW, 0, 0) or return 5; # rewind to start of input file
    open(OUT, ">$outfile") or return 10;
    binmode(OUT);
    $$outref = \*OUT; # save reference for cleanup

    if ($jpgLen) {
        # copy the RAW file, removing the JPG image
        read(RAW, $buff, $blockStart) or return 1;
        print OUT $buff or return 11;
        my $newDir = pack($pk16, $dirEntries - 1);
        for (my $i = 0; $i < $dirEntries; ++$i) {
            my $offset = $i * 10;
            my $tag = Get16u(\$mainDir, $offset);
            next if $tag == 0x2007; # don't copy JPG preview
            my $type = $tag >> 8;
            # make sure the block type is something we know how to deal with
            return 9 unless $type == 0x20 or $type == 0x28 or $type == 0x30;
            # get the data length and position
            my $len = Get32u(\$mainDir, $offset + 2);
            my $ptr = Get32u(\$mainDir, $offset + 6) + $blockStart;
            # read the data block
            seek(RAW, $ptr, 0) or return 5;
            read(RAW, $buff, $len) or return 1;
            # we must shift this pointer if it comes after the JPG
            $ptr -= $jpgLen if $ptr > $jpgPtr;
            # construct new directory entry
            $newDir .= pack($pk16, $tag) . pack($pk32, $len) .
                pack($pk32, $ptr - $blockStart);
            # write the block
            seek(OUT, $ptr, 0) or return 12;
            print OUT $buff or return 11;
        }
        # with current RAW files the main directory is at the end, but
        # do the test anyway in case this changes in the future
        $dirStart -= $jpgLen if $dirStart > $jpgPtr;
        seek(OUT, $dirStart, 0) or return 12;
        # write the main directory
        print OUT $newDir or return 11;
        $buff = pack($pk32, $dirStart - $blockStart);
        # we should already be at the end of file, but we seek there
        # anyway to be safe in case the main directory moves in future
        # versions of Canon RAW files
        seek(OUT, 0, 2) or return 12; # seek to end of file
        # write the main directory pointer (last thing in file)
        print OUT $buff or return 11;
    }
    else {
        # do a straight copy of the file
        my $len;
        while ($len = read(OUT, $buff, 65536)) {
            print OUT $buff or return 11;
        }
        return 1 unless defined $len;
    }
    return 0; # file copied OK
}

#------------------------------------------------------------------------------
# Rewrite a Canon RAW (.CRW) file, removing embedded JPG preview image
# Inputs: 0) source file name, 1) dest file name (or undef to clean in place)
# Returns: 0=failure, 1=success, >1 size of JPG removed
# Note: This is a convenience routine, not used by exiftool
sub CleanRaw($;$) {
    my $infile = shift;
    my $outfile = shift;
    my $in_place; # flag that file is being modified in place
    my $inref;    # reference to input file
    my $outref;   # reference to output file
    my $jpgLen;
    my $err;

    # generate temporary file name if changing the file in-place
    unless ($outfile and $outfile ne $infile) {
        $outfile = "$infile-CleanRaw.tmp"; # write to temporary file
        $in_place = 1;                     # set in-place flag
    }
    if (-e $outfile) {
        $err = 20; # don't overwrite existing file
    }
    else {
        $err = _doCleanRaw($infile, $outfile, $in_place, \$inref, \$outref, \$jpgLen);
    }
    # clean up any open files
    if ($inref) {
        close $inref or $err = 21;
    }
    if ($outref) {
        close $outref or $err = 22;
        if ($in_place and not $err) {
            # replace the original file only if everything went OK
            rename $outfile, $infile or $err = 23;
        }
        # erase bad (or dummy) output file
        unlink $outfile if $err;
    }
    # return success code
    if ($err) {
        warn "CleanRaw() error $err for $infile\n";
        return 0;
    }
    elsif ($jpgLen) {
        return $jpgLen;
    }
    else {
        return 1;
    }
}

#------------------------------------------------------------------------------
# Process Raw file directory
# Inputs: 0) file pointer, 1) block start position in file, 2) block size, 3) list tags to return
# Returns: 1 on success
sub ProcessRawDir($$$$) {
    my $fp = shift;
    my $blockStart = shift;
    my $blockSize = shift;
    my $requestedTags = shift;
    my $buff;

    my $rawTagTable = ExifTool::GetTagTable('TagTables::CanonRaw::Main') or return 0;

    $ExifTool::verbose > 2 and printf("Raw block: start 0x%x, size 0x%x\n", $blockStart, $blockSize);
    # 4 bytes at end of block give directory position within block
    seek($fp, $blockStart + $blockSize - 4, 0) or return 0;
    read($fp, $buff, 4) or return 0;
    my $dirOffset = ExifTool::Get32u(\$buff, 0) + $blockStart;
    seek($fp, $dirOffset, 0) or return 0;
    read($fp, $buff, 2) or return 0;
    my $entries = ExifTool::Get16u(\$buff, 0); # get number of entries in directory
    my $dirLen = 10 * $entries;
    read($fp, $buff, $dirLen) or return 0; # read the directory

    $ExifTool::verbose and printf("Raw directory at 0x%x with $entries entries:\n", $dirOffset);

    for (my $pt = 0; $pt < $dirLen; $pt += 10) {
        my $tag = ExifTool::Get16u(\$buff, $pt);
        my $size = ExifTool::Get32u(\$buff, $pt + 2);
        my $ptrVal = ExifTool::Get32u(\$buff, $pt + 6);
        my $ptr = $ptrVal + $blockStart; # all pointers relative to block start
        my $value;
        my $dumpHex;
        my $tagInfo = ExifTool::GetTagInfo($rawTagTable, $tag);

        $ExifTool::verbose > 1 and printf("Entry %d) Tag: 0x%.4x  Size: 0x%.8x  Ptr: 0x%.8x\n", $pt / 10, $tag, $size, $ptr);
        my $tagType = $tag >> 8; # tags are grouped in types by value of upper byte
        if ($tagType == 0x28 or $tagType == 0x30) {
            # this type of tag specifies a subdirectory
            $ExifTool::verbose and printf("........ Start 0x%x ........\n", $tag);
            ProcessRawDir($fp, $ptr, $size, $requestedTags);
            $ExifTool::verbose and printf("........ End 0x%x ........\n", $tag);
            next;
        }
        elsif ($tagType == 0x48 or $tagType == 0x50 or $tagType == 0x58) {
            # this type of tag stores the value in the 'size' field (weird!)
            $value = $size;
        }
        elsif ($size == 0) {
            $value = $ptrVal; # (haven't seen this, but this would make sense)
        }
        elsif ($size <= 512 or ($ExifTool::verbose > 2 and $size <= 65536)
            or ($tagInfo and ($$tagInfo{'SubDirectory'}
            or grep (/^$$tagInfo{Name}$/i, @$requestedTags)))) {
            # read value if size is small or specifically requested
            # or if this is a SubDirectory
            seek($fp, $ptr, 0) or return 0;
            unless (read($fp, $value, $size)) {
                warn sprintf("Error reading %d bytes from 0x%x\n", $size, $ptr);
                next;
            }
            $dumpHex = 1;
        }
        else {
            $value = sprintf("(%u bytes at 0x%x)", $size, $ptr);
        }
        if ($ExifTool::verbose > 1 or ($ExifTool::verbose and not defined $tagInfo)) {
            if ($dumpHex) {
                ExifTool::HexDumpTag($tag, \$value, $size);
            }
            else {
                printf("  Tag 0x%x: %s\n", $tag, ExifTool::Printable($value));
            }
        }
        next unless defined $tagInfo;

        my $subdir = $$tagInfo{'SubDirectory'};
        if ($subdir) {
            my $name = $$tagInfo{'Name'};
            my $newTagTable;
            if ($$subdir{'TagTable'}) {
                $newTagTable = ExifTool::GetTagTable($$subdir{'TagTable'});
                unless ($newTagTable) {
                    warn "Unknown tag table $$subdir{TagTable}\n";
                    next;
                }
            }
            else {
                warn "Must specify TagTable for SubDirectory $name\n";
                next;
            }
            my $subdirStart = 0;
            $$subdirStart = eval $$subdir{'Start'} if $$subdir{'Start'};
            my $dirData = \$value;
            my $subdirType = $$newTagTable{'TableType'};
            if (defined $$subdir{'Validate'} and not eval $$subdir{'Validate'}) {
                warn "Invalid $name data\n";
            }
            elsif ($subdirType) {
                $ExifTool::verbose and print "........ Start $name ........\n";
                if ($subdirType eq 'BinaryData') {
                    ExifTool::ProcessBinaryData($fp, $newTagTable, \$value, $subdirStart);
                }
                elsif ($subdirType eq 'CanonCustom') {
                    require TagTables::CanonCustom;
                    TagTables::CanonCustom::ProcessCanonCustom($newTagTable, \$value, $subdirStart, $size);
                }
                else {
                    warn "Bad SubDirectory type for RAW file: $subdirType\n";
                }
                $ExifTool::verbose and print "........ End $name ........\n";
            }
            else {
                warn "Must set TableType for $subdirType\n";
            }
        }
        else {
            ExifTool::FoundTag($tagInfo, $value);
        }
    }
    return 1;
}

#------------------------------------------------------------------------------
# get information from raw file
# Inputs: 0) file handle, 1) hash of tags to return
# Returns: 1 on success, 0 otherwise
sub RawInfo($$) {
    my $RAW = shift;
    my $requestedTags = shift;
    my $buff;

    read($RAW, $buff, 2) or return 0;
    ExifTool::SetByteOrder($buff) or return 0;
    read($RAW, $buff, 4) or return 0;
    my $hlen = ExifTool::Get32u(\$buff, 0);

    seek($RAW, 0, 2) or return 0;
    my $filesize = tell($RAW) or return 0;

    return ProcessRawDir($RAW, $hlen, $filesize - $hlen, $requestedTags);

    return 1;
}

1; # end

