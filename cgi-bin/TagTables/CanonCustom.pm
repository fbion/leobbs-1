package TagTables::CanonCustom;

use strict;
use vars qw($VERSION);
use warnings;
use diagnostics;

$VERSION = '1.00';

#------------------------------------------------------------------------------
# Custom functions for the D30/D60
# CanonCustom (keys are custom function number)
%TagTables::CanonCustom::Functions = (
    TableType => 'CanonCustom',
    1         => {
        Name      => 'LongExposureNoiseReduction',
        PrintConv => {
            0 => 'Off',
            1 => 'On',
        },
    },
    2         => {
        Name      => 'Shutter/AELock',
        PrintConv => {
            0 => 'AF/AE lock',
            1 => 'AE lock/AF',
            2 => 'AF/AF lock',
            3 => 'AE+release/AE+AF  ',
        },
    },
    3         => {
        Name      => 'MirrorLockup',
        PrintConv => {
            0 => 'Disable',
            1 => 'Enable',
        },
    },
    4         => {
        Name      => 'ExposureLevelIncrements',
        PrintConv => {
            0 => '1/2 Stop',
            1 => '1/3 Stop',
        },
    },
    5         => {
        Name      => 'AFAssist',
        PrintConv => {
            0 => 'Auto',
            1 => 'Off',
        },
    },
    6         => {
        Name      => 'FlashSyncSpeedAv',
        PrintConv => {
            0 => 'Auto',
            1 => '1/200 Fixed',
        },
    },
    7         => {
        Name      => 'AEBSequence',
        PrintConv => {
            0 => '0,-,+/Enabled',
            1 => '0,-,+/Disabled',
            2 => '-,0,+/Enabled',
            3 => '-,0,+/Disabled',
        },
    },
    8         => {
        Name      => 'ShutterCurtainSync',
        PrintConv => {
            0 => '1st-curtain sync',
            1 => '2nd-curtain sync',
        },
    },
    9         => {
        Name      => 'LensAFStopButton',
        PrintConv => {
            0 => 'AF Stop',
            1 => 'Operate AF',
            2 => 'Lock AE and start timer  ',
        },
    },
    10        => {
        Name      => 'FillFlashAutoReduction',
        PrintConv => {
            0 => 'Enable',
            1 => 'Disable',
        },
    },
    11        => {
        Name      => 'MenuButtonReturn',
        PrintConv => {
            0 => 'Top',
            1 => 'Previous (volatile)',
            2 => 'Previous',
        },
    },
    12        => {
        Name      => 'SetButtonFunction',
        PrintConv => {
            0 => 'NotAssigned',
            1 => 'Change quality',
            2 => 'Change ISO speed',
            3 => 'Select parameters  ',
        },
    },
    13        => {
        Name      => 'SensorCleaning',
        PrintConv => {
            0 => 'Disable',
            1 => 'Enable',
        },
    },
    14        => {
        Name      => 'SuperimposedDisplay',
        PrintConv => {
            0 => 'On',
            1 => 'Off',
        },
    },
    15        => {
        Name        => 'ShutterReleaseNoCFCard',
        Description => 'Shutter Release w/o CF Card',
        PrintConv   => {
            0 => 'Yes',
            1 => 'No',
        },
    },
);

# custom functions for 10D
%TagTables::CanonCustom::Functions10D = (
    TableType => 'CanonCustom',
    1         => {
        Name      => 'SetButtonFunction',
        PrintConv => {
            0 => 'NotAssigned',
            1 => 'Change quality',
            2 => 'Change parameters',
            3 => 'Menu display',
            4 => 'Image replay ',
        },
    },
    2         => {
        Name        => 'ShutterReleaseNoCFCard',
        Description => 'Shutter Release w/o CF Card',
        PrintConv   => {
            0 => 'Yes',
            1 => 'No',
        },
    },
    3         => {
        Name      => 'FlashSyncSpeedAv',
        PrintConv => {
            0 => 'Auto',
            1 => '1/200 (Fixed)',
        },
    },
    4         => {
        Name      => 'Shutter/AELock',
        PrintConv => {
            0 => 'AF/AE lock',
            1 => 'AE lock/AF',
            2 => 'AF/AF lock, No AE Lock',
            3 => 'AE/AF, No AE Lock',
        },
    },
    5         => {
        Name        => 'AFAssist',
        Description => 'AF Assist/Flash Firing',
        PrintConv   => {
            0 => 'Emits/Fires',
            1 => 'Does Not Emit/Fires',
            2 => 'Only Ext. Flash Emits/Fires',
            3 => 'Emits/Does Not Fire',
        },
    },
    6         => {
        Name      => 'ExposureLevelIncrements',
        PrintConv => {
            0 => '1/2 Stop',
            1 => '1/3 Stop',
        },
    },
    7         => {
        Name      => 'AFPointRegistration',
        PrintConv => {
            0 => 'Center',
            1 => 'Bottom',
            2 => 'Right',
            3 => 'Extreme Right',
            4 => 'Automatic',
            5 => 'Extreme Left',
            6 => 'Left',
            7 => 'Top',
        },
    },
    8         => {
        Name      => 'RawAndJpgRecording',
        PrintConv => {
            0 => 'RAW+Small/Normal',
            1 => 'RAW+Small/Fine',
            2 => 'RAW+Medium/Normal',
            3 => 'RAW+Medium/Fine',
            4 => 'RAW+Large/Normal',
            5 => 'RAW+Large/Fine',
        },
    },
    9         => {
        Name      => 'AEBSequence',
        PrintConv => {
            0 => '0,-,+/Enabled',
            1 => '0,-,+/Disabled',
            2 => '-,0,+/Enabled',
            3 => '-,0,+/Disabled',
        },
    },
    10        => {
        Name      => 'SuperimposedDisplay',
        PrintConv => {
            0 => 'On',
            1 => 'Off',
        },
    },
    11        => {
        Name      => 'MenuButtonDisplayPosition',
        PrintConv => {
            0 => 'Previous (Volatile)',
            1 => 'Previous',
            2 => 'Top',
        },
    },

    12        => {
        Name      => 'MirrorLockup',
        PrintConv => {
            0 => 'Disable',
            1 => 'Enable',
        },
    },
    13        => {
        Name      => 'AssistButtonFunction',
        PrintConv => {
            0 => 'Normal',
            1 => 'Select Home Position',
            2 => 'Select HP (while pressing)',
            3 => 'Av+/- (AF point by QCD)',
            4 => 'FE lock',
        },
    },
    14        => {
        Name      => 'FillFlashAutoReduction',
        PrintConv => {
            0 => 'Enable',
            1 => 'Disable',
        },
    },
    15        => {
        Name      => 'ShutterCurtainSync',
        PrintConv => {
            0 => '1st-curtain sync',
            1 => '2nd-curtain sync',
        },
    },
    16        => {
        Name      => 'SafetyShiftInAvOrTv',
        PrintConv => {
            0 => 'Disable',
            1 => 'Enable',
        },
    },
    17        => {
        Name      => 'LensAFStopButton',
        PrintConv => {
            0 => 'AF Stop',
            1 => 'Operate AF',
            2 => 'Lock AE and start timer  ',
        },
    },
);

# custom functions for the 1D
%TagTables::CanonCustom::Functions1D = (
    TableType => 'CanonCustom',
    0         => {
        Name      => 'FocusingScreen',
        PrintConv => {
            0 => 'Ec-N, R',
            1 => 'Ec-A,B,C,CII,CIII,D,H,I,L',
        },
    },
    1         => {
        Name      => 'FinderDisplayDuringExposure',
        PrintConv => {
            0 => 'Off',
            1 => 'On',
        },
    },
    2         => {
        Name        => 'ShutterReleaseNoCFCard',
        Description => 'Shutter Release w/o CF Card',
        PrintConv   => {
            0 => 'Yes',
            1 => 'No',
        },
    },
    3         => {
        Name        => 'ISOSpeedExpansion',
        Description => 'ISO Speed Expansion',
        PrintConv   => {
            0 => 'No',
            1 => 'Yes',
        },
    },
    4         => {
        Name        => 'ShutterAELButton',
        Description => 'Shutter Button/AEL Button',
        PrintConv   => {
            0 => 'AF/AE Lock Stop',
            1 => 'AE Lock/AF',
            2 => 'AF/AF Lock, No AE Lock',
            3 => 'AE/AF, No AE Lock',
        },
    },
    5         => {
        Name        => 'ManualTv',
        Description => 'Manual Tv/Av for M',
        PrintConv   => {
            0 => 'Tv=Main/Av=Control',
            1 => 'Tv=Control/Av=Main',
            2 => 'Tv=Main/Av=Main w/o Lens',
            3 => 'Tv=Control/Av=Main w/o Lens',
        },
    },
    6         => {
        Name      => 'ExposureLevelIncrements',
        PrintConv => {
            0 => '1/3-Stop Set, 1/3-Stop Comp',
            1 => '1-Stop Set, 1/3-Stop Comp',
            2 => '1/2-Stop Set, 1/2-Stop Comp',
        },
    },
    7         => {
        Name      => 'USMLensElectronicMF',
        PrintConv => {
            0 => 'Turns On After One-Shot AF',
            1 => 'Turns Off After One-Shot AF',
            2 => 'Always Turned Off',
        },
    },
    8         => {
        Name        => 'LCDPanels',
        Description => 'Top/Back LCD Panels',
        PrintConv   => {
            0 => 'Remain. Shots/File No.',
            1 => 'ISO/Remain. Shots',
            2 => 'ISO/File No.',
            3 => 'Shots In Folder/Remain. Shots',
        },
    },
    9         => {
        Name      => 'AEBSequence',
        PrintConv => {
            0 => '0,-,+/Enabled',
            1 => '0,-,+/Disabled',
            2 => '-,0,+/Enabled',
            3 => '-,0,+/Disabled',
        },
    },
    10        => {
        Name      => 'AFPointIllumination',
        PrintConv => {
            0 => 'On',
            1 => 'Off',
            2 => 'On Without Dimming',
            3 => 'Brighter',
        },
    },
    11        => {
        Name      => 'AFPointSelection',
        PrintConv => {
            0 => 'H=AF+Main/V=AF+Command',
            1 => 'H=Comp+Main/V=Comp+Command',
            2 => 'H=Command Only/V=Assist+Main',
            3 => 'H=FEL+Main/V=FEL+Command',
        },
    },
    12        => {
        Name      => 'MirrorLockup',
        PrintConv => {
            0 => 'Disable',
            1 => 'Enable',
        },
    },
    13        => {
        Name        => 'AFPointSpotMetering',
        Description => 'No. AF points/spot metering',
        PrintConv   => {
            0 => '45/Center AF Point',
            1 => '11/Active AF Point',
            2 => '11/Center AF Point',
            3 => '9/Active AF Point',
        },
    },
    14        => {
        Name      => 'FillFlashAutoReduction',
        PrintConv => {
            0 => 'Enable',
            1 => 'Disable',
        },
    },
    15        => {
        Name      => 'ShutterCurtainSync',
        PrintConv => {
            0 => '1st-curtain sync',
            1 => '2nd-curtain sync',
        },
    },
    16        => {
        Name      => 'SafetyShiftInAvOrTv',
        PrintConv => {
            0 => 'Disable',
            1 => 'Enable',
        },
    },
    17        => {
        Name      => 'AFPointActivationArea',
        PrintConv => {
            0 => 'Single AF Point',
            1 => 'Expanded (TTL. of 7 AF Points)',
            2 => 'Automatic Expanded (Max. 13)',
        },
    },
    18        => {
        Name      => 'SwitchToRegisteredAFPoint',
        PrintConv => {
            0 => 'Assist + AF',
            1 => 'Assist',
            2 => 'Only While Pressing Assist',
        },
    },
    19        => {
        Name      => 'LensAFStopButton',
        PrintConv => {
            0 => 'AF Stop',
            1 => 'AF Start',
            2 => 'AE Lock While Metering',
            3 => 'AF Point: M->Auto/Auto->Ctr',
            4 => 'AF Mode: ONESHOT<->SERVO',
            5 => 'IS Start',
        },
    },
    20        => {
        Name      => 'AIServoTrackingSensitivity',
        PrintConv => {
            0 => 'Standard',
            1 => 'Slow',
            2 => 'Moderately Slow',
            3 => 'Moderately Fast',
            4 => 'Fast',
        },
    },
);

#------------------------------------------------------------------------------
# process Canon custom
# Inputs: 0) pointer to tag table, 1) data reference,
#         2) pointer offset, 3) bytes in directory
sub ProcessCanonCustom($$$$) {
    my $tagTablePtr = shift;
    my $dataPt = shift;
    my $offset = shift;
    my $size = shift;

    # first entry in array must be the size
    unless (ExifTool::Get16u($dataPt, $offset) == $size) {
        warn "Invalid CanonCustom data\n";
        return;
    }
    for (my $pos = 2; $pos < $size; $pos += 2) {
        my $entry = substr($$dataPt, $pos + $offset, 2);
        my $val = ExifTool::Get16u($dataPt, $offset + $pos);
        my $tag = ($val >> 8);
        $val = ($val & 0xff);
        my $tagInfo = ExifTool::GetTagInfo($tagTablePtr, $tag);
        if ($tagInfo) {
            ExifTool::FoundTag($tagInfo, $val);
        }
        else {
            $ExifTool::verbose and printf "  Custom Function $tag: $val\n";
        }
    }
}


1; # end
