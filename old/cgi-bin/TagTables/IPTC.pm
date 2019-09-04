package TagTables::IPTC;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

#------------------------------------------------------------------------------
# File:         IPTC.pm
#
# Description:  Definitions for IPTC information
#
# Revisions:    Jan. 08/03 - P. Harvey Created
#------------------------------------------------------------------------------

# main EXIF tag table
%TagTables::IPTC::Main = (
    0   => {
        Name      => 'IPTCRecordVersion',
        PrintConv => '"(Binary data, use -b to extract)"',
    },
    5   => 'ObjectName',
    7   => 'EditStatus',
    8   => 'EditorialUpdate',
    10  => 'Urgency',
    12  => 'SubjectReference',
    15  => 'Category',
    20  => 'SupplementalCategory',
    22  => 'FixtureIdentifier',
    25  => 'Keywords',
    26  => 'ContentLocationCode',
    27  => 'ContentLocationName',
    30  => 'ReleaseDate',
    35  => 'ReleaseTime',
    37  => 'ExpirationDate',
    38  => 'ExpirationTime',
    40  => 'SpecialInstructions',
    42  => 'ActionAdvised',
    45  => 'ReferenceService',
    47  => 'ReferenceDate',
    50  => 'ReferenceNumber',
    55  => 'DateCreated',
    60  => 'TimeCreated',
    62  => 'DigitalCreationDate',
    63  => 'DigitalCreationTime',
    65  => 'OriginatingProgram',
    70  => 'ProgramVersion',
    75  => 'ObjectCycle',
    80  => 'By-line',
    85  => 'By-lineTitle',
    90  => 'City',
    92  => 'Sub-location',
    95  => 'Province-State',
    100 => 'Country-PrimaryLocationCode',
    101 => 'Country-PrimaryLocationName',
    103 => 'OriginalTransmissionReference',
    105 => 'Headline',
    110 => 'Credit',
    115 => 'Source',
    116 => 'CopyrightNotice',
    118 => 'Contact',
    120 => 'Caption-Abstract',
    122 => 'Writer-Editor',
    125 => {
        Name      => 'RasterizedCaption',
        PrintConv => '"(Binary data, use -b to extract)"',
    },
    130 => 'ImageType',
    131 => 'ImageOrientation',
    135 => 'LanguageIdentifier',
);

#------------------------------------------------------------------------------
# get IPTC info
# Inputs: 0) reference to tag table, 1) data reference, 2) data length
# Returns: 1 on success, 0 otherwise
sub ProcessIPTC($$$) {
    my $tagTablePtr = shift;
    my $dataPt = shift;
    my $dataLen = shift;
    my $success = 0;

    # the first field starts with 0x1c, everything before is the header
    my $header;
    if ($$dataPt =~ /\x1c/) {
        $header = $`;
    }
    else {
        $header = $$dataPt;
    }
    my $pos = length($header);

    # save our IPTC header too
    $pos and ExifTool::FoundTag('IPTC_Header', $header);

    while ($pos + 5 < $dataLen) {
        my $buff = substr($$dataPt, $pos, 5);
        my ($id, $type, $tag, $len) = unpack("CCCn", $buff);
        last unless $id == 0x1c and $type == 2;
        $pos += 5; # step to after field header
        if ($pos + $len > $dataLen) {
            $ExifTool::verbose and print "Invalid IPTC entry for tag $tag (len $len)\n";
            $success = 0;
            last;
        }
        my $val = substr($$dataPt, $pos, $len);
        my $tagInfo = ExifTool::GetTagInfo($tagTablePtr, $tag);
        $tagInfo or $tagInfo = sprintf("IPTC_%d", $tag);
        ExifTool::FoundTag($tagInfo, $val);
        $success = 1;

        $pos += $len; # increment to next field
    }
    return $success;
}


1; # end
