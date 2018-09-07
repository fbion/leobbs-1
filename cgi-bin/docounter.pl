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
&winlock("${lbdir}data/counter.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
if (-e "${lbdir}data/counter.cgi") {
    open(FILE, "+<${lbdir}data/counter.cgi");
    $count = <FILE>;
    $onlinemax = @onlinedata;
    ($count1, $count2, $onlinemax1, $onlinemaxtime1) = split(/\t/, $count);
    $onlinemaxtime1 = $currenttime if ($onlinemaxtime1 eq "");
    $count1 = 0 if ($count1 eq "");
    $count2 = 0 if ($count2 eq "");
    $count2++;
    $count1++ if ($memberprinted eq "no");
    if ($onlinemax < $onlinemax1) {
        $onlinemax = $onlinemax1;
        $onlinemaxtime = $onlinemaxtime1;
    }
    else {$onlinemaxtime = $currenttime;}

    seek(FILE, 0, 0);
    print FILE "$count1\t$count2\t$onlinemax\t$onlinemaxtime\t";
    close(FILE);
}
else {
    $onlinemax = @onlinedata;
    $onlinemaxtime = $currenttime;
    $count1 = $count2 = 1;
    open(FILE, ">${lbdir}data/counter.cgi");
    print FILE "1\t1\t$onlinemax\t$onlinemaxtime\t";
    close(FILE);
}
&winunlock("${lbdir}data/counter.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
1;
