package TagTables::XMP;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

# XMP tags need only be specified if a conversion or name change is necessary
%TagTables::XMP::Main = (
    TableType         => 'XMP',
    # I'll leave these parameters alone since I don't know what the Photoshop values mean
    Contrast          => {},
    Saturation        => {},
    Sharpness         => {},
    li                => { # what's up with this name?  I'm guessing this is ISO - PH
        Name => 'ISO',
    },
    WhiteBalance      => {}, # already converted to ASCII
    ExposureBiasValue => {
        Name      => 'ExposureCompensation',
        PrintConv => 'TagTables::Exif::ConvertFraction($val)',
    },
);


# fill out XMP table with entries from main table if they don't exist
foreach (keys %TagTables::Exif::Main) {
    my $tagInfo = $TagTables::Exif::Main{$_};
    # just take first entry in table info array
    my $name;
    if (ref $tagInfo) {
        ref($tagInfo) eq 'ARRAY' and $tagInfo = $$tagInfo[0];
        $name = $$tagInfo{'Name'};
    }
    else {
        $name = $tagInfo;
    }
    next if $TagTables::XMP::Main{$name};
    $TagTables::XMP::Main{$name} = $tagInfo;
}

1; #end
