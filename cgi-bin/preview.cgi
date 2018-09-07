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

BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$query = new LBCGI;
$error =0;
$inpost = $query->param('body');
$inpost = &cleaninput("$inpost");
if ($inpost eq "") {$inpost="内容校验出错&必须输入内容！"; $error=1;}
$inforum  = $query->param('forum');
if ($inforum !~ /^[0-9]+$/) {$inpost="打开文件&老大，别乱黑我的程序呀！"; $error=1;}
$intopic  = $query->param('topic');
if ($intopic !~ /^[0-9]+$/ && $intopic ne "") {$inpost="打开文件&老大，别乱黑我的程序呀！"; $error=1;}
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

&getoneforum("$inforum");
$inselectstyle = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./)){ $inpost="普通错误&老大，别乱黑我的程序呀！"; $error=1;}
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
if (($defaultflashwidth eq "")||($defaultflashwidth < 200)||($defaultflashheight eq "")||($defaultflashheight < 100)) {
    $defaultflashwidth = 410;
    $defaultflashheight = 280;
}

$end_q_tag = 0;
$srt_q_tag = 0;
$end_q_tag++ while $inpost =~ m/\[\/QUOTE\]/ig;
$srt_q_tag++ while $inpost =~ m/\[QUOTE\]/ig;
if ($end_q_tag ne $srt_q_tag) { $inpost="内容校验出错&你输入了 $srt_q_tag 个 [QUOTE] 标签和 $end_q_tag 个 [/QUOTE] 标签，数目不匹配！"; $error=1;}
$postbackcolor = "$postcolorone";
$postfontcolor = "$postfontcolorone";
if($error == 0) {
if (($inpost =~ /(\&\#35\;|#)Moderation Mode/i && ($inmembmod eq "yes" || $membercode eq "ad" || $membercode eq "smo")) || $htmlstate eq "on") {
	$inpost =~ s/(\&\#35\;|#)Moderation Mode/***** 版主模式 *****\<br\>/g;
	$inpost =~ s/&lt;/</g;
	$inpost =~ s/&gt;/>/g;
	$inpost =~ s/&quot;/\"/g;
} else {
	$inpost =~ s/style/\&\#115\;tyle/isg;
}
$inpost =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost =~ s/LBSALE/LBSAL\&\#069\;/sg;
if ($inpost =~ /\[UploadFile.{0,6}=tmp\_.+?\]/) {
    $inpost =~ s/\[UploadFile.{0,6}=tmp\_.+?\]/\[新上传文件预览中不可显示\]\<BR\>/isg;
}


    if (($emoticons eq 'on') and ($showemoticons eq 'yes')) {
        &doemoticons(\$inpost);
	&smilecode(\$inpost);
    }

    if ($idmbcodestate eq 'on') {
	&lbcode(\$inpost);
        if ($inpost =~/<blockquote><font face=$font>代码/isg){
            $inpost =~ s/\&amp\;/\&/ig ;
            $inpost =~ s/\&lt\;br\&gt\;/<br>/ig;
	}
    } else {
    	require "codeno.cgi";
	&lbnocode(\$inpost);
	$inpost =~ s/\[DISABLELBCODE\]//isg;
    }

$output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center height="95%">
<tr><td><table cellpadding=4 cellspacing=1 width=100% height="100%">
<tr><td bgcolor=$titlecolor $catbackpic align=center height="20"><font color=$titlefontcolor><b>-=> 预览 <=-</b></td></tr>
<tr><td colspan=2 bgcolor="$postbackcolor" height="*" valign="top"><font color=$postfontcolor>$inpost</td></tr></tr>
<tr><td bgcolor=$titlecolor $catbackpic align=center height="20"><font color=$titlefontcolor><a href="javascript:close()">-=> 关闭 <=-</a></td></tr></table></td></table><SCRIPT>valignend()</SCRIPT><p>~;
} else {
@Error=split(/\&/,$inpost);
$output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center height="95%">
<tr><td><table cellpadding=4 cellspacing=1 width=100% height="100%">
<tr><td bgcolor=$titlecolor $catbackpic align=center height="20"><font color=$titlefontcolor><b>-=> $Error[0] <=-</b></td></tr>
<tr><td colspan=2 bgcolor="$postbackcolor" height="*" valign="middle" align="center"><font color=color><b>$Error[1]</b></td></tr></tr>
<tr><td bgcolor=$titlecolor $catbackpic align=center height="20"><font color=$titlefontcolor><a href="javascript:close()">-=> 关闭 <=-</a></td></tr></table></td></table><SCRIPT>valignend()</SCRIPT><p>~;
}

&output("$boardname - 预览",\$output,"msg");
exit;
