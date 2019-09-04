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
use VISITFORUM qw(getlastvisit setlastvisit);
use MAILPROG qw(sendmail);
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "pag.cgi";
$query = new LBCGI;

$in_forum = $query->param('forum');
$in_topic = $query->param('topic');
$email = $query->param('email');

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic) && ($in_topic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($in_member_name eq "" || $in_member_name eq "客人") {
    $in_member_name = "客人";
    if ($reg_access eq "on" && &checksearchbot) {
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        print "<script language='javascript'>document.location = 'loginout.cgi?forum=$in_forum'</script>";
        exit;
    }
    &error("普通错误&客人不能查看贴子内容，请注册或登录后再试") if ($guestregistered eq "off");
}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if (($allowed_entry{$in_forum} eq "yes") || ($member_code eq "ad") || ($member_code eq 'smo')) {$allowed = "yes";}
    else {$allowed = "no";}
    #        &getmemberstime("$in_member_name");
    &getlastvisit;
    $forumlastvisit = $lastvisitinfo{$in_forum};
    $currenttime = time;
    &setlastvisit("$in_forum,$currenttime");
}

if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

&getoneforum("$in_forum");

$filetoopen = "$lbdir" . "forum$in_forum/$in_topic.thd.cgi";
&winlock($filetoopen) if ($OS_USED eq "Nt");
open(FILE, "$filetoopen");
flock(FILE, 1) if ($OS_USED eq "Unix");
@threads = <FILE>;
close(FILE);
&winunlock($filetoopen) if ($OS_USED eq "Nt");
($trash, $topictitle, $trash) = split(/\t/, @threads[0]);
$topictitle =~ s/^＊＃！＆＊//;

if ($addtopictime eq "yes") {
    my $topictime = &dispdate($postdate + ($timedifferencevalue * 3600) + ($timezone * 3600));
    $topictitle = "[$topictime] $topictitle";
}

$postdate = &dateformat($postdate + ($timedifferencevalue * 3600) + ($timezone * 3600));

if (($startnewthreads eq "cert") && (($member_code ne "ad" && $member_code ne "smo" && $member_code ne "cmo" && $member_code ne "mo" && $member_code ne "amo" && $member_code !~ /^rz/) || ($in_member_name eq "客人")) && ($userincert eq "no")) {&error("进入论坛&你一般会员不允许进入此论坛！");}
&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$member_code,/);
if ($allow_users ne '') {
    &error('进入论坛&你不允许进入该论坛！') if (",$allow_users," !~ /,$in_member_name,/i && $member_code ne 'ad');
}

if ($member_code ne 'ad' && $member_code ne 'smo' && $inmembmod ne 'yes') {
    &error("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &error("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &error("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

if (($privateforum eq "yes") && ($allowed ne "yes")) {
    &error("进入私密论坛&对不起，你无权访问这个论坛！");
}
else {
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {
            &whosonline("$in_member_name\t$forumname\tboth\t打包邮递贴子<a href=\"topic.cgi?forum=$in_forum&topic=$in_topic\"><b>$topictitle</b></a>\t");
        }
        else {
            &whosonline("$in_member_name\t$forumname(密)\tboth\t打包邮递贴子保密贴子\t");
        }
    }
}
if ($emailfunctions eq "off") {&error("打包邮递&非常抱歉，论坛的发送邮件功能已经关闭！");}

if ($email) {
    if ($email !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/) {&error("打包邮递&错误的邮件地址！");}
    $email =~ s/[\a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    $output .= qq~
        <html><head><title>$board_name</title>
	<style>
		A:visited {	TEXT-DECORATION: none	}
		A:active  {	TEXT-DECORATION: none	}
		A:hover   {	TEXT-DECORATION: underline overline	}
		A:link 	  {	text-decoration: none;}

	        A:visited {	text-decoration: none;}
	        A:active  {	TEXT-DECORATION: none;}
	        A:hover   {	TEXT-DECORATION: underline overline}

		.t     {	LINE-HEIGHT: 1.4					}
		BODY   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		SELECT {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		INPUT  {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt; height:22px;	}
		TEXTAREA{	FONT-FAMILY: 宋体; FONT-SIZE: 9pt;	}
		DIV    {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		FORM   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		OPTION {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		P	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		TD	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
		BR	   {	FONT-FAMILY: 宋体; FONT-SIZE: 9pt	}
	</style>
    </head>
    <body topmargin=10 leftmargin=0>
    <table cellpadding=0 cellspacing=0 width=90% align=center>
        <tr>
            <td>
            <p><b>从$board_name打包的主题</b><p>
            <b>论 坛 名- $board_name</b> ($boardurl/leobbs.cgi)<br>
            <b>讨论区名-- $forumname</b> ($boardurl/forums.cgi?forum=$in_forum)<br>
            <b>贴子标题--- $topictitle</b> ($boardurl/topic.cgi?forum=$in_forum&topic=$in_topic)
        </tr>
    </table>
    <p><p><p>
    <table cellpadding=0 cellspacing=0 width=90% align=center>
        <tr>
            <td>

    ~;
    foreach $line (@threads) {
        ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\t/, $line);
        $post = "<font color=red>屏蔽帖子不能打包<\/font>" if ($post =~ /\[POSTISDELETE=(.+?)\]/isg);
        $post =~ s/\[hide\](.*)\[\/hide\]/<font color=red>隐藏内容不能打包<\/font>/isg;
        $post = "<font color=red>加密贴子不能打包<\/font>" if ($post =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/isg || $post =~ /LBSALE\[(.*?)\]LBSALE/isg);
        $post =~ s/\[post=(.+?)\](.+?)\[\/post\]/<font color=red>加密贴子不能打包<\/font>/isg;
        $post =~ s/\[jf=(.+?)\](.+?)\[\/jf\]/<font color=red>加密贴子不能打包<\/font>/isg;
        $post =~ s/\[watermark\](.+?)\[\/watermark\]/<font color=red>加水印内容不能打包<\/font>/isg;
        $post =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[加密连结\]/isg if ($usecurl ne "no");
        $post =~ s/\[ALIPAYE\](.*)\[ALIPAYE\]//isg;

        &lbcode(\$post);

        $post =~ s/&lt\;/\</g;
        $post =~ s/&gt\;/\>/g;
        $post =~ s/&quot\;/\"/g;
        $postdate = &dateformat($postdate + ($timedifferencevalue * 3600) + ($timezone * 3600));

        $output .= qq~ 
        <hr><br>
        -- 发布人： $postermembername<BR>
        -- 发布时间： $postdate<br>
        $post      
        ~;
    }
    $output .= qq~
        </td></tr></table><center><hr><b>$board_name<br>&copy; 2000 LeoBBS.com</b></center>
        </body></html>
    ~;
    $subject = "从$board_name打包邮递过来的贴子";
    &sendmail($adminemail_out, $adminemail_in, $email, $subject, $output);
    print "<center><br><b>邮递贴子完毕!</b><br><br><a href=javascript:top.window.close()>关闭窗口</a><script>top.window.close()</script></center>";
    exit;
}
else {
    $output .= qq~
    <br><p>
<SCRIPT>valigntop()</SCRIPT>
    <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr><td>
    <table cellpadding=6 cellspacing=1 width=100%>
    <form action="$thisprog" method=post>
    <tr>
    <td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
    <input type=hidden name="forum" value="$in_forum">
    <input type=hidden name="topic" value="$in_topic">
    <font color=$fontcolormisc><b>打包邮递</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone colspan=2><font color=$fontcolormisc>
    <b>把本贴 <a href=topic.cgi?forum=$in_forum&topic=$in_topic>$topictitle</a> 打包邮递。</b><br>请正确输入你要邮递的邮件地址！
    </td></tr><tr>
    <td bgcolor=$miscbacktwo><font color=$fontcolormisc><b>邮递的 Email 地址：</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="email"></td>
    </tr><tr>
    <td colspan=2 bgcolor=$miscbacktwo align=center><input type=submit value="发 送" name="Submit"></table></td></form></tr></table><SCRIPT>valignend()</SCRIPT>
    ~;
    &output("$board_name - 帖子打包", \$output, "msg");
}
