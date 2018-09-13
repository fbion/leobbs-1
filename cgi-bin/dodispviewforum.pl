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
if ($inmembername ne "客人") {
    if (($membercode eq "ad" || $inmembmod eq "yes" || $membercode eq 'smo') && ($membercode ne 'amo')) {
        $deltopicmore1 = qq~论坛选项~;
        $deltopicmore2 = qq~<img src=$imagesurl/images/$skin/adminlock.gif width=12 height=15> <a href=forumoptions.cgi?action=prune&forum=$in_forum>批量管理文章</a>~;
        $deltopicmore3 = qq~<img src=$imagesurl/images/$skin/adminlock.gif width=12 height=15> <a href=postings.cgi?action=repireforum&forum=$in_forum>修复这个论坛</a>~;
    }
    else {
        $deltopicmore1 = "";
        $deltopicmore2 = "";
        $deltopicmore3 = "";
    }

    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellspacing=1 cellpadding=6 width=100%>
<tr><td width=80% bgcolor=$titlecolor $catbackpic><font color=$titlefontcolor><b>-=> LeoBBS 论坛图例</b></font> (<a href=delforumcache.cgi?forum=$in_forum title=如果本区有部分数据滞后的话，可以用此功能>更新该区缓存</a>)</td>
<td noWrap bgcolor=$titlecolor width=20% align=right $catbackpic><font color=$titlefontcolor> 所有时间均为 - $basetimes &nbsp;</td></tr><tr><td colspan=3 bgcolor=$forumcolorone>
<table cellspacing=4 cellpadding=0 width=94% align=center><tr>
<td width=20%><font color=$fonthighlight>打开的主题</font></td>
<td width=21%><font color=$fonthighlight>回复超 $hottopicmark 次的热门帖</font></td>
<td width=22%><font color=$fonthighlight>锁定帖子图标</font></td>
<td width=21%><font color=$fonthighlight>特殊帖子图标</font></td>
<td width=14%><font color=$fonthighlight>$deltopicmore1</font></td></tr><tr>
<td><img src=$imagesurl/images/$skin/topicnew3.gif> 上次来之后发表</td>
<td><img src=$imagesurl/images/$skin/topichot3.gif> <img src=$imagesurl/images/$skin/closedbhot.gif> 上次来之后发表</td>
<td><img src=$imagesurl/images/$skin/topiclocked3.gif> 不接受回复的主题</td>
<td><img src=$imagesurl/images/$skin/abstop.gif> <img src=$imagesurl/images/$skin/lockcattop.gif> <img src=$imagesurl/images/$skin/locktop.gif> 固顶的主题</td>
<td>$deltopicmore2</td></tr><tr>
<td><img src=$imagesurl/images/$skin/topicnonew.gif> 上次来之后无新回复</td>
<td><img src=$imagesurl/images/$skin/topichotnonew.gif> 上次来之后无新回复</td>
<td><img src=$imagesurl/images/$skin/closedb1.gif> 不接受回复的投票</td>
<td><img src=$imagesurl/images/$skin/closedb.gif> 投票类别的主题</td>
<td>$deltopicmore3</td></tr></table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>
~;
}
else {
    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellspacing=0 cellpadding=0 width=$tablewidth align=center bgcolor=$tablebordercolor>
<tr><td><table cellspacing=1 cellpadding=6 width="100%"><tr>
<td width=80% bgcolor=$titlecolor $catbackpic><font color=$titlefontcolor><b>-=> LeoBBS 论坛图例</b></font> (<a href=delforumcache.cgi?forum=$in_forum title=如果本区有部分数据滞后的话，可以用此功能>更新该区缓存</a>)</td>
<td noWrap bgcolor=$titlecolor width=20% align=right $catbackpic><font color=$titlefontcolor>所有时间均为 - $basetimes &nbsp;</td></tr><tr><td colspan=3 bgcolor=$forumcolorone>
<table cellspacing=4 cellpadding=0 width=92% align=center><tr>
<td width=21%><img src=$imagesurl/images/$skin/topicnonew.gif> 打开讨论的主题</td>
<td width=21%><img src=$imagesurl/images/$skin/closedb.gif> 投票类别的主题</td>
<td width=28%><img src=$imagesurl/images/$skin/topiclocked3.gif> <img src=$imagesurl/images/$skin/closedb1.gif> 关闭了的主题，不接受回复</td>
<td width=21%><img src=$imagesurl/images/$skin/abstop.gif> <img src=$imagesurl/images/$skin/lockcattop.gif> <img src=$imagesurl/images/$skin/locktop.gif> (总、区)固顶的主题</td>
</tr></table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR>
~;
}
1;
