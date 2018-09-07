#!/usr/bin/perl
#####################################################
#           论坛规则插件由 Money 维护制作           #
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      网站位址： http://www.LeoBBS.com/            #
#      论坛位址： http://bbs.LeoBBS.com/            #
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
use LBCGI;
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "forumrule.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$action = $query->param('action');
$inforum = $query->param('forum');
&error("开启档案&老大，别乱黑我的程序呀！") if ($inforum !~ /^[0-9 ]+$/);
require "${lbdir}data/style${inforum}.cgi" if (-e "${lbdir}data/style${inforum}.cgi");

#my $inmembername = $query->param('membername');
#my $inpassword = $query->param('password');
$inmembername = $query->param('membername');
$inpassword = $query->param('password');
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
require "${lbdir}data/skin/${inselectstyle}.cgi" if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi"));
$catbackpic = "background=$imagesurl/images/$skin/$catbackpic" if $catbackpic;

print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

$inmembername = $query->cookie("amembernamecookie") unless $inmembername;
$inpassword = $query->cookie("apasswordcookie") unless $inpassword;
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
} else {
    &getmember("$inmembername","no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if ($inpassword ne $password) {
	    $namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名称不相符，请重新登入！");
    }
}

&error("普通错误&没有这个分论坛！") unless -e "${lbdir}forum$inforum";

&moderator($inforum);

if ($action ne "edit") {
    &ShowForm();
}else {
    &Edit();
}

&output("编辑论坛规则及重要信息", \$output);
exit;

sub ShowForm {

    &mischeader("编辑论坛规则及重要信息");

    open FILE, "${lbdir}boarddata/forumrule$inforum.cgi";
    my $forumrule = <FILE>;
    close FILE;

    $forumrule =~ s/<br>/\n/isg;

    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="edit">
<input type=hidden name="forum" value="$inforum">
<font color=$fontcolormisc><b>请输入您的用户名称、密码进入版主模式 [编辑论坛规则及重要信息]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><b><u>$inmembername</u></b></font> ，要使用其他用户身份，请输入用户名称和密码。未注册客人请输入网名，密码留空白。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名称</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入论坛规则及重要信息<br>(允许使用 LBCODE 代码)<br><br><font color=$fonthighlight>为了美观，内容请控制在5行内。</font></td><td bgcolor=$miscbackone><textarea cols=60 name=forumrule rows=10>$forumrule</textarea> （留空表示不显示论坛规则及重要信息）</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="编 辑"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT><p>
~;

}

sub Edit {
    &mischeader("编辑论坛规则及重要信息");

    &error("权限不足&您不是本论坛坛主或版主，或是您的密码错误！") unless ((($membercode eq "ad")||($membercode eq 'smo')||(",$catemods," =~ /\Q\,$inmembername\,\E/i)||($inmembmod eq "yes"))&&($inpassword eq $password));

    my $forumrule = $query->param('forumrule');
       $forumrule = &cleaninput("$forumrule");
       $forumrule =~ s/\n/<br>/isg;
       $forumrule =~ s/<p>/<br><br>/isg;
       $forumrule =~ s/<br><br><br>/<br>/isg;
       $forumrule =~ s/<br>$//ig;

    if ($forumrule) {
        open FILE, ">${lbdir}boarddata/forumrule$inforum.cgi";
        print FILE $forumrule;
        close FILE;
    }else {
        # 反正都没有论坛规则及重要信息，倒不如整个档案删除，减少一次档案读取。
    	unlink "${lbdir}boarddata/forumrule$inforum.cgi";
    }

    require "recooper.pl";
    &addadminlog("编辑论坛规则及重要信息");

    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>论坛规则及重要信息已编辑</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$inforum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">~;

}