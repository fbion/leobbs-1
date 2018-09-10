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

use strict;
use warnings;
use diagnostics;

if ($inmembername eq "客人") {$loginmessage = "（您必须登录才能查看详情，否则只显示该论坛的无新帖图例）";}
if ($membercode eq "ad" || $membercode eq 'smo') {$delcache = "　　<B>[<a href=delmaincache.cgi title=如果上方的信息有部分数据滞后的话，可以用此功能>立即更新首页缓存</a>]</B>"}
my $leopic = qq~<a href=http://www.LeoBBS.com target=_blank><img src=$imagesurl/images/lblogo.gif width=88 height=31 border=0 title="----------------    ☆    ---------------\n　极酷超级论坛(LeoBBS)由雷傲科技制作　\n　正版标示： Powered By LeoBBS.com　\n　感谢您采用我们的论坛，让我们做的更好！　\n----------------    ☆    ---------------"></a>~ if ($noads ne "yes");
$output .= qq~</td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><img src=$imagesurl/images/none.gif height=5><br><SCRIPT>valigntop()</SCRIPT>
<table cellspacing=0 cellpadding=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellspacing=1 cellpadding=6 width=100%>
<tr><td width=75% bgcolor=$titlecolor $catbackpic><b>-=> LeoBBS 论坛图例 $delcache</td>
<td align=right noWrap bgcolor=$titlecolor width=25% $catbackpic>所有时间均为 - $basetimes &nbsp;</td></tr>
<tr><td bgcolor=$forumcolortwo colspan=3>
<table cellspacing=4 cellpadding=0 width=92% align=center>
<tr><td colspan=6>论坛图例仅当你登录并且访问后才显示&nbsp;$loginmessage</font></div></td></tr>
<tr><td><font color=$fonthighlight TITLE=允许注册会员发言和回复>正规论坛</font></td>
<td><font color=$fonthighlight TITLE=允许任何人发言和回复>开放论坛</font></td>
<td><font color=$fonthighlight TITLE=允许坛主和版主发言，其他注册用户只能回复>评论论坛</font></td>
<td><font color=$fonthighlight TITLE=允许拥有访问密码或已经经过认证的注册会员发言>保密论坛</font></td>
<td><font color=$fonthighlight TITLE=允许认证会员发言和回复>认证论坛</font></td>
<td colspan=2><font color=$fonthighlight>特殊论坛</font></td></tr>
<tr><td><img src=$imagesurl/images/$skin/$zg_havenew> 有新的帖子</td>
<td><img src=$imagesurl/images/$skin/$kf_havenew> 有新的帖子</td>
<td><img src=$imagesurl/images/$skin/$pl_havenew> 有新的帖子</td>
<td><img src=$imagesurl/images/$skin/$bm_havenew> 有新的帖子</td>
<td><img src=$imagesurl/images/$skin/$rz_havenew> 有新的帖子</td>
<td><img src=$imagesurl/images/$skin/$jh_pic TITLE=只允许坛主和版主发言和操作> 只读精华区</td>
<td align=right valign=top rowspan=2>$leopic</td></tr>
<tr><td><img src=$imagesurl/images/$skin/$zg_nonew> 没有新帖子</td>
<td><img src=$imagesurl/images/$skin/$kf_nonew> 没有新帖子</td>
<td><img src=$imagesurl/images/$skin/$pl_nonew> 没有新帖子</td>
<td><img src=$imagesurl/images/$skin/$bm_nonew> 没有新帖子</td>
<td><img src=$imagesurl/images/$skin/$rz_nonew> 没有新帖子</td>
<td><img src=$imagesurl/images/$skin/shareforum.gif TITLE=和本论坛友情链接的联盟论坛> 联盟论坛区</td></tr>
</table>~;
1;
