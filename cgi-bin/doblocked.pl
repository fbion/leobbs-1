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
if ($inmembername eq "") { $inusername = "客人"; }
$ipaddress = "$ENV{'REMOTE_ADDR'}($ENV{'HTTP_X_FORWARDED_FOR'} -- $ENV{'HTTP_CLIENT_IP'})";
$inmembername =~ s/\_/ /g;

$output .= qq~<p>
<tr>
<td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font color=$fontcolormisc><b><font color=$fonthighlight>不允许发送管理员的论坛密码</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
<b>从安全角度考虑，坛主和总版主的论坛密码是锁定的，不允许通过 Email 或者回答问题来寄送。</b><p>
为了防止有 hacker 攻击服务器，你的 IP 地址 $ipaddress 和你的用户名 $inmembername 已经被记录。<br>
你用的浏览器： $ENV{'HTTP_USER_AGENT'}<p>
如果你不是故意的，你不要过于担心。<p><p>
</td></tr></table></td></tr></table>
~;
$output =~ s/用户资料/警告！/g;
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output($boardname,\$output);
1;
