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
$output .= qq~
<form action=forums.cgi method=post>
<input type=hidden name=forum value=$inforum>
<input type=hidden name=action value=accessrequired>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=3 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center><font color=$fontcolormisc><b>请输入您的名称、密码登录私有论坛</b></font></td></tr>
<tr><td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc><br>每个浏览器只需要登录一次，同时请确认你已经打开了浏览器的 Cookies 选项！<br>只有经过管理员许可的用户才可以访问该论坛，如果你不能登录，请联系管理员！<br><br></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，如果要以其他用户身份进入，请<a href=loginout.cgi>按此重新登录</a>。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入论坛访问密码</font></td>
<td bgcolor=$miscbackone>　<input type=password name=forumpassword value="$forumpassword">　 <font color=$fontcolormisc>如果你已经授权允许进入，则不必输入密码.</font></td></tr>
<tr height=28><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc>如果你确认输入了正确的密码，但还是无法登录的话，请刷新此页面(或者再次按登录键一次)。</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name=submit value="登  录"></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT></form>
~;
&output("$forumname",\$output);
exit;
1;
