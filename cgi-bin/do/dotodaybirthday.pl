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

my $lockfile = "$lbdir" . "lock/birthday.lck";
if (!(-e $lockfile)) {
    open(LOCKBIRTH, ">$lockfile");
    close(LOCKBIRTH);

    undef @birthdaytoday;
    open(MEMFILE, "${lbdir}data/lbmember3.cgi");
    my @memberdata = <MEMFILE>;
    close(MEMFILE);

    foreach (@memberdata) {
        chomp $_;
        (my $users, my $borns) = split(/\t/, $_);
        (my $unowy, my $unowm, my $unowd) = split(/\//, $borns);
        if (($nowm eq $unowm) && ($nowd eq $unowd)) {
            my $usersfilename = $users;
            $usersfilename =~ s/ /\_/g;
            $usersfilename =~ tr/A-Z/a-z/;
            $usersfilename =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
            $unowy = $nowy - $unowy;
            $unowy = $unowy - 1900 if ($unowy > 1900);
            push(@birthdaytoday, "$users\t$usersfilename\t$unowy\t\n");
            if ($sendtobirthday eq "yes") {
                open(FILE, "${lbdir}$msgdir/in/${usersfilename}_msg.cgi");
                sysread(FILE, my $inboxmessages, (stat(FILE))[7]);
                close(FILE);
                $inboxmessages =~ s/\r//isg;
                open(FILE, ">${lbdir}$msgdir/in/${usersfilename}_msg.cgi");
                print FILE "＊＃！＆＊全体管理人员\tno\t$currenttime\t《$board_name》祝您生日快乐！\t今天是您 $unowy 岁生日,《$board_name》祝您生日快乐！\n$inboxmessages";
                close(FILE);
            }
        }
    }

    chomp @birthdaytoday;
    foreach (@birthdaytoday) {
        next if ($_ eq "");
        (my $users, my $usersfilename, my $unowy) = split(/\t/, $_);
        next if ($users eq "");
        $birthdayuser .= qq~<span style=cursor:hand onClick=javascript:O9('~ . uri_escape($usersfilename) . qq~') title=祝$unowy岁生日快乐！>$users</span>, ~;
    }
    chop $birthdayuser;
    chop $birthdayuser;
    $borncount = @birthdaytoday;

    open(BDILE, ">${lbdir}data/birthdaytoday.cgi");
    print BDILE "#$nowtime\n";
    print BDILE qq~$birthdayuser\n~;
    print BDILE qq~$borncount\n~;
    close(BDILE);
    unlink($lockfile);
}
else {
    (my $sec, my $no) = localtime($currenttime);
    $sec = int($sec / 15);
    unlink($lockfile) if ($sec == 2);
    $birthdayuser = "";
    $borncount = 0;
}
1;
