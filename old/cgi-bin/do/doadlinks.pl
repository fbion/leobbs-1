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

$adlinks = &HTML("$adlinks");
$adlinks =~ s/\$imagesurl/$imagesurl/isg;
$adlinks =~ s/\$tablebordercolor/$tablebordercolor/isg;
$adlinks =~ s/\$forumcolorone/$forumcolorone/isg;
$adlinks =~ s/\$forumcolortwo/$forumcolortwo/isg;
$adlinks =~ s/\[br\]/\n/isg;
$adlinks = "<table cellpadding=0 cellspacing=0 width=$tablewidth align=center><tr><td>$adlinks</td></tr></table>";
1;
