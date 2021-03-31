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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

my $query = new LBCGI;
$thisprog = "friendlist.cgi";

my $action = $query->param('action');
my $deluser = $query->param('deluser');
my $adduser = $query->param('adduser');
my $in_member_name = $query->param('membername');
my $in_password = $query->param('password');
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}

$adduser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\;\\\{\}\'\:\"\,\.\/\<\>\?]//isg;
$deluser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\;\\\{\}\'\:\"\,\.\/\<\>\?]//isg;

if (!$in_member_name) {$in_member_name = cookie("amembernamecookie");}
if (!$in_password) {$in_password = cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($in_member_name eq "" || $in_member_name eq "客人") {
    $in_member_name = "客人";
    $userregistered = "no";
    errorbl("请登录后再使用本功能！");
}
else {
    &getmember("$in_member_name", "no");
    &error("普通错误&此用户根本不存在！") if ($in_password ne "" && $userregistered eq "no");
    &error("普通错误&密码与用户名不相符，请重新登录！") if ($in_password ne $password && $userregistered ne "no");
    &action;
}

sub action {
    if ($action eq "adduser") {&adduser($adduser);}
    elsif ($action eq "deluser") {&deluser($deluser);}
    else {&list;}
}

sub adduser {
    errorbl("自己添加自己为好友做什么？") if ($adduser eq $in_member_name);
    &getmember($adduser, "no");
    if ($userregistered ne "no") {

        $memberfiletitle = $in_member_name;
        $memberfiletitle =~ s/ /_/g;
        $memberfiletitle =~ tr/A-Z/a-z/;

        $deluser =~ s/\+/ /;

        $filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
        if (-e $filetomake) {
            open(FILE, "$filetomake");
            @currentlist = <FILE>;
            close(FILE);
        }

        unless (grep (/^＊＃！＆＊$adduser$/, @currentlist)) {
            push(@currentlist, $adduser);
        }

        if (open(FILE, ">$filetomake")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            foreach $user (@currentlist) {
                chomp($user);
                $user =~ s/^＊＃！＆＊//isg;
                print FILE "＊＃！＆＊$user\n";
            }
            close(FILE);
        }

        &list;
    }
    else {
        errorbl("没有该注册用户！");
    }
} ### end adduser

sub deluser {

    $memberfiletitle = $in_member_name;
    $memberfiletitle =~ s/ /_/g;
    $memberfiletitle =~ tr/A-Z/a-z/;

    $deluser =~ s/\+/ /;

    $filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
    if (-e $filetomake) {
        open(FILE, "$filetomake");
        @currentlist = <FILE>;
        close(FILE);
    }
    else {
        errorbl("你的好友列表为空！");
    }

    if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach $user (@currentlist) {
            chomp($user);
            $user =~ s/^＊＃！＆＊//isg;
            unless ($user eq $deluser) {
                print FILE "＊＃！＆＊$user\n";
            }
        }
        close(FILE);
    }

    &list;

} ### end deluser

sub list {

    $output .= qq~<html>
<head>
<script type="text/javascript">
function openScript(url, width, height) {
        var Win = window.open(url,"openwindow",'width=' + width + ',height=' + height + ',resizable=1,scrollbars=yes,menubar=yes,status=yes' );
}
</script>
<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}

</style>
<title>$in_member_name - 好友列表</title>
</head>
<body bgcolor="#D1D9E2"  alink="#333333" vlink="#333333" link="#333333" >
<center>$in_member_name 的好友列表</center><br>
<table width=97% align=center cellspacing=0 cellpadding=1 bgcolor=#333333>
		<tr><td>
<table width=100% cellspacing=0 cellpadding=4>
~;

    $memberfiletitle = $in_member_name;
    $memberfiletitle =~ s/ /_/g;
    $memberfiletitle =~ tr/A-Z/a-z/;

    $filetomake = "$lbdir" . "memfriend/${memberfiletitle}.cgi";
    if (-e $filetomake) {
        open(FILE, "$filetomake");
        @currentlist = <FILE>;
        close(FILE);
    }

    $colspant = "7";
    $colspans = "5";

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$in_member_name\t好友列表\tnone\t查看好友列表\t");
    }

    $output .= qq~
<tr>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>姓名</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>短消息</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>Email</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>ICQ</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>OICQ</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>主页</b></center></font></td>
<td bgcolor=$catback><font face="$font" color=$titlefont ><center><b>删除?</b></center></font></td>
</tr>
~;
    $pmnamenumber = 0;
    foreach $user (@currentlist) {
        chomp $user;
        $user =~ s/^＊＃！＆＊//isg;
        #    &getmember($user);
        &getmember("$user", "no");
        $memname = $membername;
        $memname =~ s/ /+/;
        $pmname = $membername;
        $pmname =~ s/ /_/;
        $duser = $user;
        $duser =~ s/ /+/;
        $pmnamenumber++;
        if ($userregistered ne "no") {

            $homepage =~ s/http\:\/\///sg;

            if ($homepage) {$homepage = qq~<a href="http://$homepage" target="_blank"><img src="$imagesurl/images/homepage.gif" border=0></a>~;}
            else {$homepage = "N/A";}
            $emailaddress = &encodeemail($emailaddress);
            if ($showemail eq "no" || $emailstatus eq "no" || $emailaddress eq "" || $showemail eq "msn") {
                $emailaddress = "未输入" if ($$emailaddress eq "");
                $emailaddress = "保密" if ($emailstatus eq "no");
                $emailaddress = "保密" if ($showemail eq "no");
                $emailaddress = "<a href=mailto:$emailaddress><img border=0 src=$imagesurl/images/msn.gif></a>" if ($showemail eq "msn");
            }
            else {$emailaddress = "<a href=mailto:$emailaddress><img border=0 src=$imagesurl/images/email.gif></a>"}

            if ($icqnumber) {$icqnumber = qq~<a href="javascript:openScript('misc.cgi?action=icq&UIN=$icqnumber',450,300)"><img src=$imagesurl/images/icq.gif border=0></a>~;}
            else {$icqnumber = "N/A";}
            if ($oicqnumber) {$oicqnumber = qq~<a href="javascript:openScript('http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$oicqnumber',450,200)"><img src="$imagesurl/images/oicq.gif" border=0></a>~;}
            else {$oicqnumber = "N/A";}

            my $membernametemp = "\_$membername\_";
            if ($onlineuserlist =~ /$membernametemp/i) {
                $onlineinfo = "该用户目前在线";
                $onlinepic = "online1.gif";
            }
            else {
                $onlineinfo = "该用户目前不在线";
                $onlinepic = "offline1.gif";
            }
            if (($mymembercode eq "ad") && ($onlineuserlisthidden =~ /$membernametemp/i)) {
                $onlineinfo = "该用户目前处于隐身状态";
                $onlinepic = "onlinehidden.gif";
            }
            $online = qq~<IMG SRC=$imagesurl/images/$onlinepic width=15 alt=$onlineinfo align=absmiddle>~;

            $output .= qq~
	<tr>
	<td bgcolor=$miscbackone>$online <a href="profile.cgi?action=show&member=~ . uri_escape($pmname) . qq~" target=_blank>$user</a></td>
	<td bgcolor=$miscbackone><center><a href=# onClick="javascript:openScript('messanger.cgi?action=new&touser=~ . uri_escape($pmname) . qq~',600,400)"><img src="$imagesurl/images/message.gif" border=0></a></center></td>
	<td bgcolor=$miscbackone><center>$emailaddress</center></td>
	<td bgcolor=$miscbackone><center>$icqnumber</center></td>
	<td bgcolor=$miscbackone><center>$oicqnumber</center></td>
	<td bgcolor=$miscbackone><center>$homepage</center></td>
	<td bgcolor=$miscbackone><center><form action=friendlist.cgi method=post name=pm$pmnamenumber><input type=hidden name=action value=deluser><input type=hidden name=deluser value=$duser><a href="javascript:document.pm$pmnamenumber.submit()">删除</a></center></td></form></tr>
	~;
        }
        else {
            $output .= qq~
	<tr>
	<td bgcolor=$miscbackone>$user (未注册)</td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone></td>
	<td bgcolor=$miscbackone><center><form action=friendlist.cgi method=post name=pm$pmnamenumber><input type=hidden name=action value=deluser><input type=hidden name=deluser value=$duser><a href="javascript:document.pm$pmnamenumber.submit()">删除</a></center></td></form></tr>
	~;

        }
    }

    $output .= qq~
<tr>
<form action=friendlist.cgi method=post name=adduser><input type=hidden name=action value=adduser><td bgcolor=$miscbackone><font  color=black >好友姓名:</td><td colspan=$colspans bgcolor=$miscbackone><input type=text size=20 name=adduser></td><td bgcolor=$miscbackone><center><a href="javascript:document.adduser.submit()">增加</a></center></td></form>
<tr><td bgcolor=$miscbackone colspan=$colspant><center><font  color=black >输入你要想增加的好友姓名，点击增加确认操作！<br><br><a href=javascript:top.close();>[关闭窗口]</a></center></td></tr>
</table></td></tr>
	    </table>
</body>
</html>
~;

    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
    print "$output";
} ### end of list

sub errorbl {
    $errormsg = shift;
    $output = qq~
<html>
<head>
<title>$in_member_name - 好友列表 >> 错误</title>
<meta http-equiv="refresh" content="30;URL=friendlist.cgi">
<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline 	}
		A:link 	  {	text-decoration: none;}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;
			SCROLLBAR-HIGHLIGHT-COLOR: buttonface;
 			SCROLLBAR-SHADOW-COLOR: buttonface;
 			SCROLLBAR-3DLIGHT-COLOR: buttonhighlight;
 			SCROLLBAR-TRACK-COLOR: #eeeeee;
 			SCROLLBAR-DARKSHADOW-COLOR: buttonshadow	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}

</style>
</head>
<body bgcolor="#D1D9E2"  alink="#333333" vlink="#333333" link="#333333">
<br>
<center>好友列表错误</center><br><br>
<font color=red>
<center>
<b>$errormsg</b>
</center>
</font>
<br><br>
<center><font color=$fontcolormisc> << <a href="javascript:history.go(-1)">返回上一页</a></center>

</body>
</html>
~;
    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
    print "$output";
    exit;
}
