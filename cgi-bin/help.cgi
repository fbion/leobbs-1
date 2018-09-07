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

use strict;
use warnings;
use diagnostics;
use LBCGI;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "help.cgi";
$query = new LBCGI;

$inadmin                = $query -> param('admin');
$innew                = $query -> param('helpnew');
$action                 = $query -> param('action');
$inhelpon               = $query -> param('helpon');
$inadminmodpass         = $query -> param("adminmodpass");
$inadminmodname         = $query -> param("adminmodname");
$inadminmodpass         = &cleaninput($inadminmodpass);
$inadminmodname         = &cleaninput($inadminmodname);
&error("普通错误&老大，别乱黑我的程序呀！") if (($inadminmodname =~ m/\//)||($inadminmodname =~ m/\\/)||($inadminmodname =~ m/\.\./));
$inadminmodname =~ s/\///g;
$inadminmodname =~ s/\.\.//g;
$inadminmodname =~ s/\\//g;
if ($inadminmodpass ne "") {
    eval {$inadminmodpass = md5_hex($inadminmodpass);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inadminmodpass = md5_hex($inadminmodpass);');}
    unless ($@) {$inadminmodpass = "lEO$inadminmodpass";}
}

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

$inhelpon = &cleaninput($inhelpon);
$inhelpon =~ s/\///g;
$inhelpon =~ s/\.cgi//ig;
$inhelpon =~ s/\.\.//g;
$inhelpon =~ s/\\//g;
$inadmin =~ s/\///g;
$inadmin =~ s/\.\.//g;
$inadmin =~ s/\\//g;
$innew =~ s/\///g;
$innew =~ s/\.\.//g;
$innew =~ s/\\//g;
$cleanhelpname = $inhelpon;
$cleanhelpname =~ s/\_/ /g;
$cleanadminname = $inadmin;
$cleanadminname =~ s/\_/ /g;
$cleannewname = $innew;
$cleannewname =~ s/\_/ /g;
if (($number) && ($number !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if (! $inadminmodname) { $inadminmodname = $inmembername; }
if (! $inadminmodpass) { $inadminmodpass = $inpassword; }

if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
}
else {
	&getmember("$inmembername","no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
     }
	&error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    if ($inhelpon) {
        $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
              <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                       <br><center>$inmembername，希望下面的帮助对您有用</center><br><br>
                       <font face="$font" color=$fontcolormisc>
                       <b>关于$cleanhelpname的帮助：</b><p>
	~;
        $filetoopen = "$lbdir" . "help/$inhelpon.dat";
        $filetoopen =~ s/[<>\^\(\)\{\}\a\f\n\e\0\r\"\`\&\;\*\?]//g;
        open (FILE, "$filetoopen");
        sysread(FILE, $helpdata,(stat(FILE))[7]);
        close (FILE);
	$helpdata =~ s/\r//isg;

            $output .= $helpdata;
    }
    elsif ($innew) {
        $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
              <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                       <br>
                       <font face="$font" color=$fontcolormisc>
                       <b>关于$cleannewname的帮助：</b><p>
	~;
        $filetoopen = "$lbdir" . "help/$cleannewname.pl";
        $filetoopen =~ s/[<>\^\(\)\{\}\a\f\n\e\0\r\"\`\&\;\*\?]//g;
        open (FILE, "$filetoopen");
        sysread(FILE, $helpdata,(stat(FILE))[7]);
        close (FILE);
	$helpdata =~ s/\r//isg;

            $output .= $helpdata;
    }
    elsif ($action eq "login") {

            &getmember("$inadminmodname","no");

            unless ($membercode eq "ad" ||($membercode eq 'smo')|| $membercode eq "cmo" || $membercode eq "amo" || $membercode eq "mo") { &messangererror("查看帮助&您没有权限查看此文件！"); }
            if ($inadminmodpass ne $password) { &messangererror("查看帮助&您的密码错误！"); }

            $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
               <tr>
                <td>
                  <table cellpadding=3 cellspacing=1 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                      <br><center>$inadminmodname，希望下面的帮助对您有用</center><br><br>
                      <font face="$font" color=$fontcolormisc>
                      <b>　　坛主/版主帮助文件</b><p>
             ~;
            $dirtoopen = "$lbdir" . "help";
            opendir (DIR, "$dirtoopen");
            @dirdata = readdir(DIR);
            closedir (DIR);
            @sorteddirdata = grep(/cgi$/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);

            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.cgi$//g;
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                $cleannamefile = uri_escape($cleanname);
                $output .= qq~&nbsp;&nbsp;&nbsp;&nbsp;关于<a href="$thisprog?admin=$cleannamefile" target="_self"><b>$cleanname</b></a>的帮助<p>~;
            }
	}
        elsif ($inadmin) {
	    &getmember("$inmembername","no");
            unless ($membercode eq "ad" || $membercode eq 'smo'|| $membercode eq 'cmo'|| $membercode eq 'amo'|| $membercode eq "mo") { &messangererror("查看帮助&您没有权限查看此文件！"); }
            if ($inpassword ne $password) { &messangererror("查看帮助&您的密码错误！"); }
	    $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
		<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
                 <tr>
                  <td>
                  <table cellpadding=3 cellspacing=1 width=100%>
                    <tr>
                      <td bgcolor=$miscbacktwo align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                    </tr>
                    <tr>
                      <td bgcolor=$miscbackone valign=middle align=cleft><font face="$font" color=$fontcolormisc>
                      <br><center>$inmembername，希望下面的帮助对您有用</center><br><br>
                      <font face="$font" color=$fontcolormisc>
                      <b>关于$cleanadminname的帮助</b><p>
            ~;

	    $filetoopen = "$lbdir" . "help/$inadmin.cgi";
            $filetoopen =~ s/[<>\^\(\)\{\}\a\f\n\e\0\r\"\`\&\;\*\?]//g;
            open (FILE, "$filetoopen");
            @helpdata = <FILE>;
            close (FILE);

	    foreach (@helpdata) {
                $output .= $_;
            }
        }
        else {
	    $output .= qq~<p>
<SCRIPT>valigntop()</SCRIPT>
              <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
                <tr>
                <td>
                    <table cellpadding=3 cellspacing=1 width=100%>
                        <tr>
                            <td bgcolor=$miscbacktwo align=center colspan=2 $catbackpic height=26><font face="$font" color=$fontcolormisc><b>$boardname的帮助文件</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone align=center><br><center><font face="$font" color=$fontcolormisc>
                            <b>&nbsp;&nbsp;&nbsp;&nbsp;常规帮助文件</b></td>
                        </tr>
                        <tr>
                            <td bgcolor=$miscbackone valign=top align=left><font face="$font" color=$fontcolormisc>
                            
                            
            ~;

            $dirtoopen = "$lbdir" . "help";
            opendir (DIR, "$dirtoopen");
            @dirdata = readdir(DIR);
            closedir (DIR);
            @sorteddirdata = grep(/dat$/,@dirdata);
            @newdirdata = sort alphabetically(@sorteddirdata);

            foreach (@newdirdata) {
                chomp $_;
                $filename = $_;
                $filename =~ s/\.dat$//g;
                $cleanname = $filename;
                $cleanname =~ s/\_/ /g;
                $cleannamefile = uri_escape($cleanname);
                $output .= qq~&nbsp;&nbsp;&nbsp;&nbsp;关于<a href="$thisprog?helpon=$cleannamefile" target="_self"><b>$cleanname</b></a>的帮助<p>~;
            }
	    $output .= qq~</td>~;
	}

$output .= qq~</tr><tr><td bgcolor=$miscbackone valign=middle align=center colspan=2><font face="$font" color=$fontcolormisc>~;
    if ($passwordverification eq "yes") { $passwordverification = "是必需的"; }
    else { $passwordverification = "不是必需的"; }

    if ($emailfunctions ne "on") { $emailfunctions = "关闭"; }

    if ($emoticons eq "on") {
	$emoticons = "使用";
        $emoticonslink = qq~| 查看<a href=javascript:openScript('misc.cgi?action=showsmilies',300,350)>表情转换</a>~;
    }
    else { $emoticons = "没有使用"; }
    $output .= qq~<p><br><br>查看<a href=\"$thisprog\" target=\"_self\">所有的帮助文件</a> $emoticonslink | 查看 <a href=\"javascript:openScript('misc.cgi?action=lbcode',300,350)\">LeoBBS 标签</a> | 查看 <a href=\"javascript:openScript('lookemotes.cgi?action=style',300,350)\">EMOTE 标签</a><BR><BR>~;

    $output .= qq~
    </td></tr>
    <tr>
    <td bgcolor=$miscbacktwo align=center colspan=2><font face="$font" color=$fontcolormisc><b>论坛常规信息</b><br><br>
    表情自动转换：<b>$emoticons</b><br>邮件地址确认：<b>$passwordverification</b><br>论坛邮件功能：<b>$emailfunctions</b><br><br>
    </td>
    </tr>
    <tr>
    <td bgcolor=$miscbackone align=center colspan=2><font face="$font" color=$fontcolormisc><b>登录访问坛主/版主的帮助</b><br>

    <form action="$thisprog" method="post">
    <input type=hidden name="action" value="login">
    <font face="$font" color=$fontcolormisc>
    您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。<BR>
    用户名：&nbsp; <input type=text name="adminmodname"> &nbsp;
    密　码：&nbsp; <input type=password name="adminmodpass"> &nbsp; <input type=submit value="登 录"></td></tr></form>
    </table></td></tr></table><SCRIPT>valignend()</SCRIPT>
    ~;

    &output("$boardname - 帮助",\$output,"msg");

sub messangererror {
    my $errorinfo = shift;
    (my $where,my $errormsg) = split(/\&/, $errorinfo);
    $output = qq~<p><SCRIPT>valigntop()</SCRIPT>
      <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
	<tr>
        <td>
        <table cellpadding=6 cellspacing=1 width=100%>
        <tr>
            <td bgcolor=$miscbacktwo valign=middle align=center $catbackpic height=26><font face="$font" color=$fontcolormisc><b>错误：$where</b></font></td></tr>
            <tr>
                <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
                <b>关于$where错误的详细原因：</b>
                <ul>
                <li><b>$errormsg</b>
                </ul>
                <b>产生$where错误的可能原因：：</b>
                <ul>
                <li>密码错误<li>用户名错误
                </ul>
                </tr>
                </td></tr>
                <tr>
                <td bgcolor=$miscbacktwo valign=middle align=center><font face="$font" color=$fontcolormisc> <a href="javascript:history.go(-1)"> << 返回上一页</a>
                </td></tr>
                </table></td></tr></table><SCRIPT>valignend()</SCRIPT>
    ~;
    &output("$boardname - 帮助",\$output,"msg");
}
