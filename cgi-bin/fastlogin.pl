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

require "${lbdir}data/outputbutton.pl" if (-e "${lbdir}data/outputbutton.pl");
$outputbutton =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg if ($disphideboard eq "yes");
$outputbutton =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg if ($dispchildjump ne "no");

if ($query->cookie("selectstyle")) {$in_select_style = $query->cookie("selectstyle");}
$in_select_style = $skin_selected if ($in_select_style eq "");

$output .= qq~<tr><td bgcolor=$titlecolor colspan=3 $catbackpic><font color=$titlefontcolor><B>-=> 快速登录入口</B>　 [ 来自：$trueipaddress，$fromwhere1 。系统：$osinfo，$browseinfo ]</td></tr>
<script>
function submitonce(theform){
if (document.all||document.getElementById){
for (i=0;i<theform.length;i++){
var tempobj=theform.elements[i]
if(tempobj.type.toLowerCase()=="submit"||tempobj.type.toLowerCase()=="reset")
tempobj.disabled=true
}}}
</script>
<FORM name=login method=post action=loginout.cgi onSubmit="submitonce(this)">
<tr><td bgcolor=$forumcolorone align=center width=26><img src=$imagesurl/images/userlist2.gif width=17></td>
<td bgcolor=$forumcolortwo colspan=1 width=*>
<input type=hidden name=action value=login>
<input type=hidden name=selectstyle value="$in_select_style">
　用户名 ： <input type=text name=inmembername size=12 maxlength=16 onmouseover=this.focus() onfocus=this.select()>　　密　码 ： <input type=password name=inpassword size=12 maxlength=20 onmouseover=this.focus() onfocus=this.select()>　 Cookie ： <select name=CookieDate><option selected value=0>不保存</option><option value=+1d>保存一天</option><option value=+30d>保存一月</option><option value=+20y>永久保存</option></select><BR><BR>
　登录到 ： <select name=forum><option selected value=>论坛首页</option>$outputbutton</select>　　　<input type=submit name=submit value="　登　 录　">　　 <B><a href=register.cgi><U><font color=$fonthighlight>注册新用户</font></u></a></B><BR><BR>
</td>~;

1;
