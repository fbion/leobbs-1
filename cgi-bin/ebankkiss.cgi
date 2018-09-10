#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

BEGIN {
    $startingtime = (times)[0] + (times)[1];
    foreach ($0, $ENV{'PATH_TRANSLATED'}, $ENV{'SCRIPT_FILENAME'}) {
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g;
        $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC, $LBPATH);
    }
}
use strict;
use warnings;
use diagnostics;
use LBCGI;
require "bbs.lib.pl";

require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
&GetCookie;
$|++;

$inmembername = $cookie{"amembernamecookie"};
$inpassword = $cookie{"apasswordcookie"};
print "Content-Type: text/html; Charset=UTF-8\n\n";

&error if (($inmembername =~ m/\//) || ($inmembername =~ m/\\/) || ($inmembername =~ m/\.\./));
&error if ($inmembername eq "" || $inmembername eq "客人");
$inmembername =~ s/ /\_/g;
$inmembername =~ tr/A-Z/a-z/;
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

my $namenumber = &getnamenumber($inmembername);
&checkmemfile($inmembername, $namenumber);

$filetoopen = $lbdir . $memdir . "/$namenumber/" . $inmembername . ".cgi";
$filetoopen = &stripMETA($filetoopen);
&error unless (-e $filetoopen);
&winlock($filetoopen) if ($OS_USED eq "Nt");
open(FILE, $filetoopen);
flock(FILE, 1) if ($OS_USED eq "Unix");
$filedata = <FILE>;
close(FILE);
chomp($filedata);
($membername, $password, $membertitle, $membercode, $numofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
if ($inpassword ne $password) {
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    &error;
}
($numberofposts, $numberofreplys) = split(/\|/, $numofposts);
if ($numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb < 50) {
    print "<html><body><img src=$imagesurl/ebank/waitress3.gif border=0 alt='连买花的钱都没有，555，警察叔叔有人非礼阿'></body></html>";
}
else {
    $mymoney -= 50;
    if (($membername ne "") && ($password ne "")) {
        if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            $lastgone = time;
            print FILE "$membername\t$password\t$membertitle\t$membercode\t$numofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
            close(FILE);
        }
    }
    print "<html><body><img src=$imagesurl/ebank/waitress2.gif border=0 alt='你真懂得讨好女孩子哦，我好喜欢你'></body></html>";
}
&winunlock($filetoopen) if ($OS_USED eq "Nt");
exit;

sub error {
    print "非法操作！";
    exit;
}

sub stripMETA {
    my $file = shift;
    $file =~ s/[<>\^\(\)\{\}\a\f\n\e\0\r\"\`\&\;\|\*\?]//g;
    return $file;
}

sub winlock {
    my $lockfile = shift;
    my $i = 0;
    $lockfile =~ s/\\/\//isg;
    $lockfile =~ s/\://isg;
    $lockfile =~ s/\//\_/isg;
    $lockfile = $lbdir . "lock/" . $lockfile;
    while (-e "$lockfile.lck") {
        last if ($i >= 120);
        select(undef, undef, undef, 0.1);
        $i++;
    }
    open(LOCKFILE, ">$lockfile.lck");
    close(LOCKFILE);
}

sub winunlock {
    my $lockfile = shift;
    $lockfile =~ s/\\/\//isg;
    $lockfile =~ s/\://isg;
    $lockfile =~ s/\//\_/isg;
    $lockfile = $lbdir . "lock/" . $lockfile;
    unlink("$lockfile.lck");
}

sub GetCookie {
    my $cookies = $ENV{"HTTP_COOKIE"} || defined($ENV{"COOKIE"});
    my @pairs = split(/;\s*/, $cookies);
    foreach (@pairs) {
        s/^\s+|\s+$//g;
        tr/+/ /;
        s/%([0-9a-fA-F]{2})/chr hex($1)/eg;
        my ($name, $value) = split(/=/, $_);
        next if ($value eq "");
        $cookie{$name} = $value;
    }
    return;
}