#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

BEGIN {
    $startingtime = (times)[0] + (times)[1];
    foreach ($0, $ENV{'PATH_TRANSLATED'}, $ENV{'SCRIPT_FILENAME'}) {
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g;
        $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC, $LBPATH);
    }
}

use warnings;
use strict;
use diagnostics;
use LBCGI;
$LBCGI::POST_MAX = 20000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "lookstyles.cgi";

$query = new LBCGI;

@params = $query->param;
foreach $param (@params) {
    $theparam = $query->param($param);
    $theparam = &cleaninput("$theparam");
    $PARAM{$param} = $theparam;
}

$action = $PARAM{'action'};
$in_forum = $PARAM{'forum'};
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

$in_member_name = $query->param("membername");
$in_password = $query->param("password");
$action = &cleaninput("$action");
$in_member_name = &cleaninput("$in_member_name");
$in_password = &cleaninput("$in_password");
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}

if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($in_member_name eq "" || $in_member_name eq "客人") {$in_member_name = "客人";}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
&getoneforum("$in_forum");

&mischeader("本版配色列表");

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));

&error("本版配色&对不起，本版块不允许查看配色！") if ($look eq "off");

if ($privateforum ne "yes") {
    &whosonline("$in_member_name\t$forumname\tboth\t查看论坛$forumname的配色\t");
}
else {
    &whosonline("$in_member_name\t$forumname(密)\tboth\t查看保密论坛$forumname的配色\t");
}

$output .= qq~
<BR><SCRIPT>valigntop()</SCRIPT>
        <table cellpadding="5" style="border-collapse: collapse" width=$tablewidth cellspacing="0" bordercolor=$tablebordercolor border=1 align=center>               
              
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛BODY标签</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>控制整个论坛风格的背景颜色或者背景图片等</font></td>
                <td bgcolor=#FFFFFF>
                $lbbody</td>
                </tr>
                              
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛页首菜单</b>
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>页首背景颜色 (菜单带上方)</font></td>
                <td bgcolor=$titleback  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titleback</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>页首字体颜色 (菜单带上方)</font></td>
                <td bgcolor=$titlefont  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titlefont</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>页首边界颜色 (菜单带上方)</font></td>
                <td bgcolor=$titleborder  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titleborder</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带字体颜色</font></td>
                <td bgcolor=$menufontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $menufontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带背景颜色</font></td>
                <td bgcolor=$menubackground  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $menubackground</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>字体外观和颜色</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"最后发贴者"字体颜色</font></td>
                <td bgcolor=$lastpostfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $lastpostfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"加重区"字体颜色</font></td>
                <td bgcolor=$fonthighlight  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $fonthighlight</td>
                </tr>
                
                                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>一般用户名称字体颜色</font></td>
                <td bgcolor=$posternamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $posternamecolor</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>一般用户名称上的光晕颜色</font></td>
		<td bgcolor=$memglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$memglow</td>
		</tr>
               
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>坛主名称字体颜色</font></td>
                <td bgcolor=$adminnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $adminnamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>坛主名称上的光晕颜色</font></td>
		<td bgcolor=$adminglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$adminglow</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>总版主名称字体颜色</font></td>
                <td bgcolor=$smonamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $smonamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>总版主名称上的光晕颜色</font></td>
		<td bgcolor=$smoglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$smoglow</td>
		</tr>                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类区版主名称字体颜色</font></td>
                <td bgcolor=$cmonamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $cmonamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>分类区版主名称上的光晕颜色</font></td>
		<td bgcolor=$cmoglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$cmoglow</td>
		</tr>                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>版主名称字体颜色</font></td>
                <td bgcolor=$teamnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $teamnamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>版主名称上的光晕颜色</font></td>
		<td bgcolor=$teamglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$teamglow</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>副版主名称字体颜色</font></td>
                <td bgcolor=$teamnamecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $amonamecolor</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>副版主名称上的光晕颜色</font></td>
		<td bgcolor=$teamglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$amoglow</td>
		</tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>过滤和禁言用户名称上的光晕颜色</font></td>
		<td bgcolor=$banglow  width=12>　</td>
		<td bgcolor=#FFFFFF>
		$banglow</td>
		</tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>所有页面颜色</center></b><br>
                <font color=#333333>这些颜色配置将用于每个页面。用于注册、登录、在线以及其他页面。
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>主字体颜色</font></td>
                <td bgcolor=$fontcolormisc  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $fontcolormisc</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色一</font></td>
                <td bgcolor=$miscbackone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $miscbackone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色二</font></td>
                <td bgcolor=$miscbacktwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $miscbacktwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>表格颜色</center></b><br>
                <font color=#333333>这些颜色大部分用于leobbs.cgi，forums.cgi和topic.cgi
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带背景颜色</font></td>
                <td bgcolor=$catback  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $catback</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带字体颜色</font></td>
                <td bgcolor=$catfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $catfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>所有表格边界颜色</font></td>
                <td bgcolor=$tablebordercolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $tablebordercolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>所有表格宽度</font></td>
                <td bgcolor=#FFFFFF>
                $tablewidth</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>标题颜色</center></b><br>
                <font color=#333333>这里颜色配置用于发表第一个主题的标题
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏背景颜色</font></td>
                <td bgcolor=$titlecolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titlecolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏字体颜色</font></td>
                <td bgcolor=$titlefontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $titlefontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛内容颜色</center></b><br>
                <font color=#333333>查看论坛内容时颜色 (forums.cgi)
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色一</font></td>
                <td bgcolor=$forumcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $forumcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色二</font></td>
                <td bgcolor=$forumcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $forumcolortwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容字体颜色</font></td>
                <td bgcolor=$forumfontcolor  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $forumfontcolor</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>回复颜色</center></b><br>
                <font color=#333333>回复贴子颜色(topic.cgi)
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色一</font></td>
                <td bgcolor=$postcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $postcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色二</font></td>
                <td bgcolor=$postcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $postcolortwo</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色一</font></td>
                <td bgcolor=$postfontcolorone  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $postfontcolorone</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色二</font></td>
                <td bgcolor=$postfontcolortwo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                $postfontcolortwo</td>
                </tr>
               
              
                ~;

$output .= qq~</td></tr></table><SCRIPT>valignend()</SCRIPT><br><br></body></html>~;
&output("查看$forumname的配色", \$output);
exit;

