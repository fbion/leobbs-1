#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

use warnings;
use strict;
use diagnostics;
$links = &HTML("$links");
$output .= qq~
<img src=$imagesurl/images/none.gif height=5><br>
<SCRIPT>valigntop()</SCRIPT>
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellspacing=1 cellpadding=6 width=100%>
<tr><td bgcolor=$titlecolor colspan=7 $catbackpic><font color=$titlefontcolor><B>-=> 首页连接</td></tr>
<tr><td bgcolor=$forumcolortwo colspan=7 width=*><font color=$titlefontcolor>
<font color=$forumfontcolor>$links</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
1;
