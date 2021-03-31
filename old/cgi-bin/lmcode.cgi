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
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/styles.cgi";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$query = new LBCGI;

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

$thisprog = "lmcode.cgi";
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
$output = qq~<p>
<SCRIPT>valigntop()</SCRIPT>
  <table cellpadding="5" style="border-collapse: collapse" width=$tablewidth cellspacing="0" bordercolor=$tablebordercolor border=1 align=center>
    <tr>
      <td width="100%" colspan="3" bgcolor=$titlecolor $catbackpic>
      <p align="center"><font color="#333333"><b>欢迎增加 <u>$board_name</u> 联盟代码</b></font></td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>论坛名称：</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>$board_name</td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>论坛地址：</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>
      <a href="$boardurl/leobbs.cgi" target=_blank>
      $boardurl/leobbs.cgi</a></td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>论坛图标：</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>
~;
if ($boardlogos ne "http://" && $boardlogos ne "") {$output .= qq~<a href="$boardlogos" target=_blank>$boardlogos</a>~;}
else {$output .= qq~没有~;}
$output .= qq~
      </td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>论坛说明：</b></td>
      <td width="72%" colspan="2" bgcolor=$forumcolortwo>$boarddescription</td>
    </tr>
    <tr>
      <td width="28%" bgcolor=$forumcolorone><b>联盟演示：</b></td>
      <td width="100" bgcolor=$forumcolortwo>
      <p align="center">
~;
if ($boardlogos ne "http://" && $boardlogos ne "") {$output .= qq~<a href="$boardurl/leobbs.cgi" target=_blank><img src="$boardlogos" align="left" width="88" height="31" border="0"></a>~;}
else {$output .= qq~暂缺图标~;}
$output .= qq~
      </td>
      <td width="*" bgcolor=$forumcolortwo>
      <a target="_blank" href="$boardurl/leobbs.cgi">
      <b>$board_name</b></a><br>
      $boarddescription</td>
    </tr>
    <tr>
      <td width="100%" colspan="3" bgcolor=$catback $catbackpic>
      <p align="center">
<input type=submit name="winclose" value="关 闭" onclick=window.close();></td>
    </tr>
  </table><SCRIPT>valignend()</SCRIPT>
~;
&output("$board_name - 查看联盟论坛代码", \$output, "msg");
exit;