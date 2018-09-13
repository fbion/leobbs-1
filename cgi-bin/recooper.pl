#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use warnings;
use strict;
use diagnostics;
sub addadminlog {
    my ($message, $in_topic) = @_;
    my $logtime = time;
    my $trueipaddress = $ENV{"HTTP_CLIENT_IP"};
    $trueipaddress = $ENV{"HTTP_X_FORWARDED_FOR"} if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    $trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);

    my $filetomake = "${lbdir}boarddata/adminlog$in_forum.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    open(FILE, ">>$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "$inmembername\t$logtime\t$in_topic\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t$message\n";
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");
    return;
}
1;
