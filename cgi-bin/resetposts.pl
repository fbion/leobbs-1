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
my $nowtime = $currenttime + 10;
&setlastvisit("$in_forum,$nowtime,1");
$forumlastvisit = $currenttime;
print header(-cookie => [ $tempvisitcookie, $permvisitcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
print qq~<script>location.href="$thisprog?forum=$in_forum";</script>~;
exit;
1;
