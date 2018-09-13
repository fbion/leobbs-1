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
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use MAILPROG qw(sendmail);
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "lbfriend.cgi";
$query = new LBCGI;
&ipbanned; #封杀一些 ip
$in_forum = $query->param('forum');
$in_topic = $query->param('topic');
$action = $query->param('action');
$inrealname = $query->param('realname');
$intoname = $query->param('toname');
$infromemail = $query->param('fromemail');
$intoemail = $query->param('toemail');
$insubject = $query->param('subject');
$inemailmessage = $query->param('emailmessage');
$emailtopictitle = $query->param('emailtopictitle');
$inrealname = &cleaninput($inrealname);
$insubject = &cleaninput($insubject);
$inemailmessage = &cleaninput($inemailmessage);
$emailtopictitle = &cleaninput($emailtopictitle);
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic) && ($in_topic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));
$in_member_name = $query->cookie("amembernamecookie");
$in_password = $query->cookie("apasswordcookie");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($in_member_name eq "" || $in_member_name eq "客人") {
    $in_member_name = "客人";
    if ($reg_access eq "on" && &checksearchbot) {
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        print "<script language='javascript'>document.location = 'loginout.cgi?forum=$in_forum'</script>";
        exit;
    }
}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    $mymembercode = $member_code;
    $myrating = $rating;
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
}
if ($emailfunctions ne "on") {&error("发邮件给朋友&对不起，论坛管理员没有将邮件功能打开！");}
$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&title;
$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以用邮件功能发送本页面给朋友</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$board_name</a> → 发个邮件给朋友<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
  <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
    <tr>
      <td>
      <table cellpadding=6 cellspacing=1 width=100%>
~;
&getoneforum("$in_forum");
if (($allowed_entry{$in_forum} eq "yes") || ($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {$allowed = "yes";}
else {$allowed = "no";}
if (($startnewthreads eq "cert") && (($member_code ne "ad" && $member_code ne "smo" && $member_code ne "cmo" && $member_code ne "amo" && $member_code ne "mo" && $member_code !~ /^rz/) || ($in_member_name eq "客人")) && ($userincert eq "no")) {&error("进入论坛&你一般会员不允许进入此论坛！");}

if (($privateforum eq "yes") && ($allowed ne "yes")) {&error("进入私密论坛&对不起，你无权访问这个论坛！");}
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

if ($action eq "send") {
    $blankfields = "";
    if (!$inrealname) {$blankfields = "yes";}
    elsif (!$intoname) {$blankfields = "yes";}
    elsif (!$intoemail) {$blankfields = "yes";}
    elsif (!$infromemail) {$blankfields = "yes";}
    elsif (!$insubject) {$blankfields = "yes";}
    elsif (!$inemailmessage) {$blankfields = "yes";}

    if ($blankfields) {
        &error("发邮件给朋友&请输入所有内容然后发送！");
    }

    if ($infromemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/) {&error("发邮件给朋友&错误的邮件地址！");}
    if ($intoemail !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/) {&error("发邮件给朋友&错误的邮件地址！");}

    my $temp = &dofilter("$insubject\t$inemailmessage\t$emailtopictitle");
    ($insubject, $inemailmessage, $emailtopictitle) = split(/\t/, $temp);

    $to = $intoemail;
    $from = $infromemail;
    $subject = "$insubject";
    $message .= "\n";
    $message .= "$board_name <br>\n";
    $message .= "$boardurl/leobbs.cgi <br>\n";
    $message .= "来自 LeoBBS 论坛中朋友的消息\n";
    $message .= "---------------------------------------------------------------------\n<br><br>\n";
    $message .= "$inrealname 从 $homename 发送邮件给您。<br>\n";
    $message .= "---------------------------------------------------------------------\n<br><br>\n";
    $message .= "$inemailmessage\n <br><br>\n";
    $message .= "主题： $emailtopictitle\n <br><br>\n<br>\n";
    $message .= "网址： $boardurl/topic.cgi?forum=$in_forum&topic=$in_topic <br>\n";
    $message .= "---------------------------------------------------------------------\n<br><br>\n";
    $message .= "提示：您没有必要回复这封邮件，这只是论坛的内容通知。\n<br><br>\n";
    $message .= "---------------------------------------------------------------------<br>\n";

    &sendmail($from, $from, $to, $subject, $message);
    $output .= qq~
        <tr>
         <td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>Email 发送完成！</b></font></td></tr>
         <tr>
         <td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
         具体情况：：
         <ul>
         <li><a href="topic.cgi?forum=$in_forum&topic=$in_topic">返回主题</a>
         <li><a href="forums.cgi?forum=$in_forum">返回论坛</a>
         <li><a href="leobbs.cgi">返回论坛首页</a>
         </ul>
         </tr>
         </td>
         </table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
    ~;
}
else {

    $filetoopen = "${lbdir}forum$in_forum/$in_topic.pl";
    open(FILE, "$filetoopen");
    $allthreads = <FILE>;
    close(FILE);

    ($topicid, $topictitle, $no, $no, $no, $no, $startedby, $startedpostdate, $no) = split(/\t/, $allthreads);

    $topictitle = &cleanarea("$topictitle");
    $topictitle =~ s/^＊＃！＆＊//;

    if ($addtopictime eq "yes") {
        my $topictime = &dispdate($startedpostdate + ($timedifferencevalue * 3600) + ($timezone * 3600));
        $topictitle = "[$topictime] $topictitle";
    }

    $output .= qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="send">
    <input type=hidden name="forum" value="$in_forum">
    <input type=hidden name="topic" value="$in_topic">
    <tr>
    <td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center><font face="$font" color=$fontcolormisc><b>发个邮件给朋友</b></font></td></tr>
    <tr>
    <td bgcolor=$miscbackone valign=middle colspan=2><font face="$font" color=$fontcolormisc>
    <b>通过邮件发送主题 <a href="topic.cgi?forum=$in_forum&topic=$in_topic">$topictitle</a> 给您的朋友。</b>　下列所有项必填，并请输入正确的邮件地址！<br>你可以添加一些自己的信息在下面的内容框内。至于这个贴子的主题和 URL 你可以不必写，因为本程序会在发送的 Email 中自动添加的！
    </td>
    <tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>您的姓名：</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="realname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc><b>您的 Email 地址：</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="fromemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>您朋友的名字：</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="toname"></td>
    </tr><tr>
    <td bgcolor=$miscbacktwo><font face="$font" color=$fontcolormisc><b>您朋友的 Email：</b></td>
    <td bgcolor=$miscbacktwo><input type=text size=40 name="toemail"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>Email 标题：</b></td>
    <td bgcolor=$miscbackone><input type=text size=40 name="subject" value="$topictitle"></td>
    </tr><tr>
    <td bgcolor=$miscbackone><font face="$font" color=$fontcolormisc><b>消息内容：</b></td>
    <td bgcolor=$miscbackone><textarea name="emailmessage" cols="55" rows="6">我想你对 '$homename' 的 '$topictitle' 这个贴子内容会感兴趣的！请去看看！</textarea></td>
    </tr><tr>
    <td colspan=2 bgcolor=$miscbacktwo align=center><input type=hidden name="emailtopictitle" value="$topictitle"><input type=submit value="发 送" name="Submit"></table></td></form></tr></table>
<SCRIPT>valignend()</SCRIPT>
    ~;
}
&output($board_name, \$output);
