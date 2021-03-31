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

my $x = &myrand(1000000000);
$x = crypt($x, aun);
$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
$x =~ s/[^\w\d]//g;
$x = substr($x, 2, 9);
my $usrdir = "usr$x" if (rename("$imagesdir$usrdir", "${imagesdir}usr$x"));
1;
