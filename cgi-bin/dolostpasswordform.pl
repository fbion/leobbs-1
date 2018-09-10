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

$helpurl = &helpfiles("遗忘密码");
$helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></a>~;

$output =~ s/\ 用户资料/\ 忘记论坛密码/g;
$output .= qq~<p>
<tr><td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
<form action=$thisprog method=post>
<input type=hidden name=action value=sendpassword>
<font color=$fontcolormisc><b>请输入您的用户名，我们可以将您的论坛密码取得方式通过邮件发给您！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</td>
<td bgcolor=$miscbackone><input type=text name=membername>　 $helpurl<BR><font color=$fonthighlight>有部分信箱（比如 Hotmail）会把论坛密码信放入垃圾邮件夹，请注意检查！</font></td></tr>
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center> 
<font color=$fontcolormisc><b>如你没有填写正确的E-Mail可以输入论坛密码提示问题和答案取得论坛密码获取方式！</b></font></td></tr> 
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入论坛密码提示问题</td> 
<td bgcolor=$miscbackone><input type=text size=20 name=getpassq></td></tr> 
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入论坛密码提示答案</td> 
<td bgcolor=$miscbackone><input type=text size=20 name=getpassa></td></tr> 
<td bgcolor=$miscbacktwo valign=middle colspan=2 align=center><input type=submit name=submit value="提 交">
</td></form></tr></table></td></tr></table>
~;
1;
