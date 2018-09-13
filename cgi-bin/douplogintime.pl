#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use strict;
use warnings;
use diagnostics;

sub uplogintime {
    my ($nametocheck, $visit) = @_;
    my $nametochecktemp = $nametocheck;
    $nametocheck =~ s/ /\_/g;
    $nametocheck =~ tr/A-Z/a-z/;
    $nametocheck =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    my $namenumber = &getnamenumber($nametocheck);
    &checkmemfile($nametocheck, $namenumber);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$nametocheck.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE6, "+<$filetoopen");
        flock(FILE6, 2) if ($OS_USED eq "Unix");
        my $filedata = <FILE6>;
        chomp($filedata);
        (my $membername, my $password, my $membertitle, my $member_code, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $oicqnumber, my $icqnumber, my $location, my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag, my $userxz, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno, my $useradd04, my $useradd02, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $chatlevel, my $chattime, my $jhmp, my $jhcount, my $ebankdata, my $onlinetime, my $userquestion, my $awards, my $jifen, my $userface, my $soccerdata, my $useradd5) = split(/\t/, $filedata);

        $nowtimetemp = time;
        if ($visit eq "T") {$visitno++ if (($nowtimetemp - $lastgone) > 300);}
        else {
            $onlinetime = 0 if ($onlinetime =~ /[^0-9]/);
            $onlinetime = $onlinetime + $savedtime - $savedcometime if (($nowtimetemp - $lastgone) > 150);
            unlink("${lbdir}cache/id/$nametocheck.cgi");
            unlink("${lbdir}cache/myinfo/$nametocheck.pl");
            unlink("${lbdir}cache/online/$nametocheck.cgi");
        }
        if (($membername ne "") && ($password ne "")) {
            $lastgone = $nowtimetemp;
            $mymoney = int($mymoney);
            seek(FILE6, 0, 0);
            print FILE6 "$membername\t$password\t$membertitle\t$member_code\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
            close(FILE6);
            my ($post1, $post2) = split(/\|/, $numberofposts);
            $post1 ||= "0";
            $post2 ||= "0";
            if ($jifen eq "") {
                require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
                $jifen = $post1 * $ttojf + $post2 * $rtojf - $postdel * $deltojf;
            }
            if (((-M "${lbdir}$memdir/old/$nametocheck.cgi") > 0.5) || (!(-e "${lbdir}$memdir/old/$nametocheck.cgi"))) {
                open(FILE6, ">${lbdir}$memdir/old/$nametocheck.cgi");
                print FILE6 "$membername\t$password\t$membertitle\t$member_code\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
                close(FILE6);
                unlink("${lbdir}cache/meminfo/$nametocheck.pl");
                unlink("${lbdir}cache/myinfo/$nametocheck.pl");
            }
        }
        else {
            close(FILE6);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }
}
1;
