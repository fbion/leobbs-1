#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

use strict;
use warnings;
use diagnostics;

unlink("${lbdir}cache/forumonline.pl") if ((-M "${lbdir}cache/forumonline.pl") * 86400 >= 180);
foreach (@onlinedata) {
    chomp $_;
    next if ($_ eq "");
    (my $savedusername, my $no, $no, my $savedwhere, $no, $no, $no, $no, $no, $no, my $hiddened) = split(/\t/, $_);
    (my $lookfor, $no) = split(/\(/, $savedusername);
    next if ($lookfor =~ m/[\(\)\*]/);
    $savedwhere =~ s/\(密\)$//isg;
    if ($savedusername =~ /^客人/) {
        $onlinehashguest{"$savedwhere"}++;
    }
    else {
        if ($hiddened eq 1) {
            $onlinehashguest{"$savedwhere"}++;
        }
        else {
            $onlinehashmember{"$savedwhere"}++;
            if ($onlinehashmember{"$savedwhere"} eq 1) {$onlinehashoutput{"$savedwhere"} .= qq~$savedusername~;}
            else {$onlinehashoutput{"$savedwhere"} .= qq~，$savedusername~;}
        }
    }
}
my @forums1 = @rearrangedforums;
push(@forums1, @forums);
foreach (@forums1) {
    chomp $_;
    next if ($_ eq "");
    ($no, $no, $no, $fname) = split(/\t/, $_);
    next if ($fname eq "");
    $onlinehashguest{"$fname"} = 0 if ($onlinehashguest{"$fname"} eq "");
    $onlinehashmember{"$fname"} = 0 if ($onlinehashmember{"$fname"} eq "");
    my $totleonline = $onlinehashguest{"$fname"} + $onlinehashmember{"$fname"};
    $onlinehashoutput{"$fname"} = qq~\|\| --= 会员列表（共 $onlinehashmember{"$fname"} 人） =--\|$onlinehashoutput{"$fname"}\|~ if ($onlinehashmember{"$fname"} > 0);
    if ($onlinehashguest{"$fname"} > 0) {
        $guestadd = qq~（其中 $onlinehashguest{"$fname"} 个客人）~;
    }
    else {undef $guestadd;}
    $titleinfos{"$fname\n"} = qq~ TITLE="目前共有 $totleonline 人在此论坛上$guestadd！$onlinehashoutput{"$fname"}"~;
    $outfileinfo .= qq~$fname\n$titleinfos{"$fname\n"}\n~;
    $titleinfos{"$fname\n"} =~ s/\|/\n/isg;
}
if (!(-e "${lbdir}cache/forumonline.pl")) {
    open(FILE, ">${lbdir}cache/forumonline.pl");
    print FILE $outfileinfo;
    close(FILE);
}
1;
