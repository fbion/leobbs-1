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
use LBCGI;
use diagnostics;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
$LBCGI::POST_MAX = 500000;
#require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
#require "postjs.cgi";
require "cleanolddata.pl";
require "recooper.pl";

$|++;
$thisprog = "postings.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

for ('forum', 'topic', 'membername', 'password', 'action', 'inpost', 'checked') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$in_forum = $forum;
$in_topic = $topic;
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic) && ($in_topic !~ /^[0-9 ]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if ($in_forum !~ /^[0-9 ]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$inmembername = $membername;
$inpassword = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime = time;

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
require "sendmanageinfo.pl" if ($sendmanageinfo eq "yes");
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

if (!$inmembername) {$inmembername = $query->cookie("amembernamecookie");}
if (!$inpassword) {$inpassword = $query->cookie("apasswordcookie");}
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "客人") {
    $inmembername = "客人";
}
else {
    #    &getmember("$inmembername");
    &getmember("$inmembername", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if ($inpassword ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}

&error("普通错误&没有这个分论坛！") if (!(-e "${lbdir}forum$in_forum"));
#&getoneforum("$in_forum");
&moderator("$in_forum");
&cleanolddata;

my %Mode = (
    'lock'         => \&lockthread,
    'unlock'       => \&unlockthread,
    'puttop'       => \&puttop,
    'putdown'      => \&putdown,
    'repireforum'  => \&repireforum,
    'locktop'      => \&locktop,
    'unlocktop'    => \&unlocktop,
    'catlocktop'   => \&catlocktop,
    'catunlocktop' => \&catunlocktop,
    'abslocktop'   => \&abslocktop,
    'absunlocktop' => \&absunlocktop,
    'highlight'    => \&highlight,
    'lowlight'     => \&lowlight,
);

if ($Mode{$action}) {$Mode{$action}->();}
else {&error("普通错误&请以正确的方式访问本程序");}

for (my $iii = 0; $iii <= 4; $iii++) {
    my $jjj = $iii * $maxthreads;
    unlink("${lbdir}cache/plcache$in_forum\_$jjj.pl");
}

&output($boardname, \$output);
exit;

sub lockthread {
    my $in_topics = $in_topic;
    my @intopic = split(/ +/, $in_topics);
    my $lockcount = @intopic;
    &error("主题锁定&请先选择需要锁定的主题！") if ($lockcount <= 0);
    &mischeader("主题锁定");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) {$cleartoedit = "yes";}

    if (($arrowuserdel eq "on") && ($cleartoedit ne "yes")) {
        open(ENT, "${lbdir}forum$in_forum/$in_topic.pl");
        $in = <ENT>;
        close(ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/, $in);
        if ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password)) {$cleartoedit = "yes";}
    }
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题锁定&您不是本论坛坛主或版主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $lockreason = $query->param("lockreason");
        $lockreason = &cleaninput($lockreason);
        $lockreason = &lbhz($lockreason, 60);
        $lockreason = "，理由是：$lockreason" if ($lockreason ne "");

        foreach $in_topic (@intopic) {
            my $filetomake = "${lbdir}forum$in_forum/$in_topic.pl";
            unless (-e $filetomake) {
                $lockcount--;
                next;
            }

            open(ENT, "${lbdir}forum$in_forum/$in_topic.pl");
            $in = <ENT>;
            close(ENT);
            chomp $in;
            ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/, $in);
            if (($threadstate eq "poll") || ($threadstate eq "pollclosed")) {$threadstate = "pollclosed";}
            else {$threadstate = "closed";}
            if (open(FILE, ">${lbdir}forum$in_forum/$in_topic.pl")) {
                print FILE "$in_topic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
                close(FILE);
            }
            $topictitle =~ s/^＊＃！＆＊//;
            &sendtoposter("$inmembername", "$startedby", "", "lock", "$in_forum", "$in_topic", "$topictitle", "$lockreason") if (($sendmanageinfo eq "yes") && (lc($inmembername) ne lc($startedby)));
        }

        if ($lockcount == 1) {
            &addadminlog("锁定贴子$lockreason", $in_topic);
        }
        else {
            &addadminlog("批量锁定贴子 $lockcount 篇$lockreason");
        }

        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题锁定成功：共锁定 <font color=$fonthighlight>$lockcount</font> 篇主题。</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="lock">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [锁定 $lockcount 个主题]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入锁定理由</font></td><td bgcolor=$miscbackone><input type=text name=lockreason size=60> （可不填）</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub unlockthread {
    &mischeader("主题解锁");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题解锁&您不是本论坛坛主或版主，或者您的密码错误！");}
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$in_forum/$in_topic.pl";
        open(ENT, $file);
        $in = <ENT>;
        close(ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/, $in);
        $topictitle =~ s/^＊＃！＆＊//;

        if (($threadstate eq "pollclosed") || ($threadstate eq "poll")) {$threadstate = "poll";}
        else {$threadstate = "open";}
        if (open(FILE, ">$file")) {
            print FILE "$in_topic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }

        &addadminlog("贴子解锁", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题解锁成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="unlock">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题解锁]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub repireforum {
    &mischeader("论坛修复");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("论坛修复&您不是本论坛坛主或正版主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        require "rebuildlist.pl";
        my $truenumber = rebuildLIST(-Forum => "$in_forum");
        ($tpost, $treply) = split(/\|/, $truenumber);

        open(FILE, "${lbdir}boarddata/listno$in_forum.cgi");
        $topicid = <FILE>;
        close(FILE);
        chomp $topicid;
        my $rr = &readthreadpl($forumid, $topicid);
        (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split(/\t/, $rr);

        open(FILE, "+<${lbdir}boarddata/foruminfo$in_forum.cgi");
        ($no, $no, $no, $todayforumpost, $no) = split(/\t/, <FILE>);
        $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
        $lastposter = $startedby if ($lastposter eq "");
        seek(FILE, 0, 0);
        print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
        close(FILE);
        $posts = 0 if ($posts eq "");
        $threads = 0 if ($threads eq "");
        open(FILE, ">${lbdir}boarddata/forumposts$in_forum.pl");
        print FILE "\$threads = $tpost;\n\$posts = $treply;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
        close(FILE);

        &addadminlog("修复论坛");
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>论坛修复成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="repireforum">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [论坛修复]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub puttop {
    &mischeader("主题提升");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题提升&您不是本论坛坛主或版主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$in_forum/$in_topic.pl";
        open(ENT, $file);
        $in = <ENT>;
        close(ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/, $in);

        if (open(FILE, ">$file")) {
            print FILE "$in_topic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }
        $topictitle =~ s/^＊＃！＆＊//;

        $file = "$lbdir" . "boarddata/listno$in_forum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open(LIST, "$file");
        flock(LIST, 1) if ($OS_USED eq "Unix");
        sysread(LIST, $listall, (stat(LIST))[7]);
        close(LIST);
        $listall =~ s/\r//isg;

        $listall =~ s/(^|\n)$in_topic\n/$1/isg;

        if (open(LIST, ">$file")) {
            flock(LIST, 2) if ($OS_USED eq "Unix");
            print LIST "$in_topic\n$listall";
            close(LIST);
        }
        &winunlock($file) if ($OS_USED eq "Nt");

        open(FILE, "+<${lbdir}boarddata/foruminfo$in_forum.cgi");
        ($no, $posts, $replys, $todayforumpost, $no) = split(/\t/, <FILE>);
        $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
        $lastposter = $startedby if ($lastposter eq "");
        seek(FILE, 0, 0);
        print FILE "$lastforumpostdate\t$posts\t$replys\t$todayforumpost\t$lastposter\t\n";
        close(FILE);
        $posts = 0 if ($posts eq "");
        $threads = 0 if ($threads eq "");
        open(FILE, ">${lbdir}boarddata/forumposts$in_forum.pl");
        print FILE "\$threads = $posts;\n\$posts = $replys;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
        close(FILE);

        &addadminlog("提升主题位置", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题提升成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="puttop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题提升]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub putdown {
    &mischeader("主题沉底");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题沉底&您不是本论坛坛主或版主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$in_forum/$in_topic.pl";
        open(ENT, $file);
        $in = <ENT>;
        close(ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/, $in);
        $lastpostdate = $lastpostdate - 3600 * 24 * 365; # 时间提前 1 年

        if (open(FILE, ">$file")) {
            print FILE "$in_topic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }
        $topictitle =~ s/^＊＃！＆＊//;

        $file = "$lbdir" . "boarddata/listno$in_forum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open(LIST, "$file");
        flock(LIST, 1) if ($OS_USED eq "Unix");
        sysread(LIST, $listall, (stat(LIST))[7]);
        close(LIST);
        $listall =~ s/\r//isg;

        $listall =~ s/(^|\n)$in_topic\n/$1/isg;

        if (open(LIST, ">$file")) {
            flock(LIST, 2) if ($OS_USED eq "Unix");
            print LIST "$listall$in_topic\n";
            close(LIST);
        }
        &winunlock($file) if ($OS_USED eq "Nt");

        &addadminlog("主题位置沉底", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题沉底成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="putdown">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题沉底]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub locktop {
    &mischeader("主题固定");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}

    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题固定首行&您不是本论坛坛主或正版主，或者您的密码错误！");}
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        unlink("${lbdir}cache/forumstop$in_forum.pl");
        my $file = "$lbdir" . "boarddata/ontop$in_forum.cgi";
        if (open(TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);
            if (open(TOPFILE, ">$file")) {
                print TOPFILE "$in_topic\n";
                $putno = 1;
                foreach (@toptopic) {
                    chomp $_;
                    if (($_ ne $in_topic) && (-e "${lbdir}forum$in_forum/$_.thd.cgi")) {
                        print TOPFILE "$_\n";
                        $putno++;
                    }
                    last if ($putno eq $maxtoptopic);
                }
                close(TOPFILE);
            }
        }
        else {
            if (open(TOPFILE, ">$file")) {
                print TOPFILE "$in_topic\n";
                close(TOPFILE);
            }
        }
        &addadminlog("固顶贴子", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题固定首行成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        if (open(TOPFILE, "${lbdir}boarddata/ontop$in_forum.cgi")) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);
        }
        $toptopic = 0;
        foreach (@toptopic) {
            chomp $_;
            if (-e "${lbdir}forum$in_forum/$_.thd.cgi") {
                $toptopic++;
            }
        }
        if ($toptopic >= $maxtoptopic) {$topnum = "<BR><B><font color=$fonthighlight>已经固定了 $toptopic 个帖子了，如果继续，最早一个被固定的帖子将被自动取消固定。</B></font>"}
        else {$topnum = "<BR><B><font color=$fonthighlight>已经固定了 $toptopic 个帖子了，你最多可以固定 $maxtoptopic 个帖子。</B></font>";}
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="locktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题固定首行]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub unlocktop {
    &mischeader("主题取消固定");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题取消固定&您不是本论坛坛主或正版主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        unlink("${lbdir}cache/forumstop$in_forum.pl");
        my $file = "${lbdir}boarddata/ontop$in_forum.cgi";
        if (open(TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);

            if (open(TOPFILE, ">$file")) {
                foreach (@toptopic) {
                    chomp $_;
                    if (($_ ne $in_topic) && (-e "${lbdir}forum$in_forum/$_.thd.cgi")) {
                        print TOPFILE "$_\n";
                    }
                }
                close(TOPFILE);
            }
        }
        &addadminlog("取消贴子固顶", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题取消固定成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="unlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题取消固定]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub abslocktop {
    &mischeader("主题总固定首行");
    if (($startnewthreads eq "no") || ($startnewthreads eq "cert") || ($privateforum eq "yes")) {&error("主题总固定首行&对不起，这个分论坛并不是对所有用户开放的，所以不能总固定帖子！");}
    $absmaxtoptopic = 3 if ($absmaxtoptopic <= 0);
    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题总固定首行&您不是本论坛坛主，或者您的密码错误！");}
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        opendir(CATDIR, "${lbdir}cache");
        my @dirdata = readdir(CATDIR);
        closedir(CATDIR);
        @dirdata = grep (/^forumstop/, @dirdata);
        foreach (@dirdata) {unlink("${lbdir}cache/$_");}
        my $file = "$lbdir" . "boarddata/absontop.cgi";
        if (open(TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);
            if (open(TOPFILE, ">$file")) {
                print TOPFILE "$in_forum\|$in_topic\n";
                $putno = 1;
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
                    ($tempinforum, $tempintopic) = split(/\|/, $_);
                    unless (($tempinforum eq $in_forum) && ($tempintopic eq $in_topic)) {
                        if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                            print TOPFILE "$_\n";
                            $putno++;
                        }
                    }
                    last if ($putno eq $absmaxtoptopic);
                }
                close(TOPFILE);
            }
        }
        else {
            if (open(TOPFILE, ">$file")) {
                print TOPFILE "$in_forum\|$in_topic\n";
                close(TOPFILE);
            }
        }
        &addadminlog("总固顶帖子", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题总固定首行成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        if (open(TOPFILE, "${lbdir}boarddata/absontop.cgi")) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);
        }
        $toptopic = 0;
        foreach (@toptopic) {
            chomp $_;
            next if ($_ eq "");
            ($tempinforum, $tempintopic) = split(/\|/, $_);
            if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                $toptopic++;
            }
        }
        if ($toptopic >= $absmaxtoptopic) {$topnum = "<BR><B><font color=$fonthighlight>已经总固定了 $toptopic 个帖子了，如果继续，最早一个被固定的帖子将被自动取消固定。</B></font>"}
        else {$topnum = "<BR><B><font color=$fonthighlight>已经总固定了 $toptopic 个帖子了，你最多可以总固定 $absmaxtoptopic 个帖子。</B></font>";}
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="abslocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题总固定首行]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub absunlocktop {
    &mischeader("主题取消总固定");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题取消总固定&您不是本论坛坛主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        opendir(CATDIR, "${lbdir}cache");
        my @dirdata = readdir(CATDIR);
        closedir(CATDIR);
        @dirdata = grep (/^forumstop/, @dirdata);
        foreach (@dirdata) {unlink("${lbdir}cache/$_");}
        my $file = "${lbdir}boarddata/absontop.cgi";
        if (open(TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);

            if (open(TOPFILE, ">$file")) {
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
                    my ($tempinforum, $tempintopic) = split(/\|/, $_);
                    unless (($tempinforum eq $in_forum) && ($tempintopic eq $in_topic)) {
                        if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                            print TOPFILE "$_\n";
                        }
                    }
                }
                close(TOPFILE);
            }
        }
        &addadminlog("取消贴子总固顶", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题取消总固定成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="absunlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题取消总固定]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}
sub highlight {
    &mischeader("加重帖子标题");
    $maxhightopic = 8 if ($maxhightopic <= 0);

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("加重帖子标题&您不是本论坛坛主或版主，或者您的密码错误！");}
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        unlink("${lbdir}cache/forumstop$in_forum.pl");
        my $file = "$lbdir" . "boarddata/highlight$in_forum.cgi";
        if (open(HIGHFILE, $file)) {
            @hightopic = <HIGHFILE>;
            close(HIGHFILE);
            if (open(HIGHFILE, ">$file")) {
                print HIGHFILE "$in_forum\-$in_topic\n";
                $putno = 1;
                foreach (@hightopic) {
                    chomp $_;
                    next if ($_ eq "");
                    ($tempinforum, $tempintopic) = split(/\-/, $_);
                    chomp $tempintopic;
                    chomp $tempinforum;
                    unless (($tempinforum eq $in_forum) && ($tempintopic eq $in_topic)) {
                        if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                            print HIGHFILE "$_\n";
                            $putno++;
                        }
                    }
                    last if ($putno eq $maxhightopic);
                }
                close(HIGHFILE);
            }
        }
        else {
            if (open(HIGHFILE, ">$file")) {
                print HIGHFILE "$in_forum\-$in_topic\n";
                close(HIGHFILE);
            }
        }
        &addadminlog("加重帖子标题", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>加重帖子标题成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        if (open(TOPFILE, "${lbdir}boarddata/highlight$in_forum.cgi")) {
            @hightopic = <TOPFILE>;
            close(TOPFILE);
        }
        $toptopic = 0;
        foreach (@hightopic) {
            chomp $_;
            next if ($_ eq "");
            ($tempinforum, $tempintopic) = split(/\-/, $_);
            if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                $toptopic++;
            }
        }
        if ($toptopic >= $maxhightopic) {$topnum = "<BR><B><font color=$fonthighlight>已经加重了 $toptopic 个帖子标题了，如果继续，最早一个被加重标题将被自动取消加重标题。</B></font>"}
        else {$topnum = "<BR><B><font color=$fonthighlight>已经加重了 $toptopic 个帖子标题了，你最多可以加重 $maxhightopic 个帖子标题。</B></font>";}
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="highlight">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [加重帖子标题]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub lowlight {
    &mischeader("帖子标题取消加重");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("帖子标题取消加重&您不是本论坛坛主或版主，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        unlink("${lbdir}cache/forumstop$in_forum.pl");
        my $file = "${lbdir}boarddata/highlight$in_forum.cgi";
        if (open(HIGHPFILE, $file)) {
            @hightopic = <HIGHPFILE>;
            close(HIGHPFILE);

            if (open(HIGHPFILE, ">$file")) {
                foreach (@hightopic) {
                    chomp $_;
                    next if ($_ eq "");
                    my ($tempinforum, $tempintopic) = split(/\-/, $_);
                    unless (($tempinforum eq $in_forum) && ($tempintopic eq $in_topic)) {
                        if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                            print HIGHPFILE "$_\n";
                        }
                    }
                }
                close(HIGHPFILE);
            }
        }
        &addadminlog("帖子标题取消加重", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>帖子标题取消加重成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="lowlight">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [帖子标题取消加重]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub catlocktop {
    &mischeader("主题区固定首行");
    if (($startnewthreads eq "no") || ($startnewthreads eq "cert") || ($privateforum eq "yes")) {&error("主题区固定首行&对不起，这个分论坛并不是对所有用户开放的，所以不能区固定帖子！");}
    $absmaxcantopic = 3 if ($absmaxcantopic <= 0);
    $cleartoedit = "no";
    if (($membercode eq "ad" || $membercode eq "smo" || ",$catemods," =~ /\Q\,$inmembername\,\E/i) && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题区固定首行&您不是本分区管理员，或者您的密码错误！");}
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        opendir(CATDIR, "${lbdir}cache");
        my @dirdata = readdir(CATDIR);
        closedir(CATDIR);
        @dirdata = grep (/^forumstop/, @dirdata);
        foreach (@dirdata) {unlink("${lbdir}cache/$_");}

        my $file = "${lbdir}boarddata/catontop$categoryplace.cgi";
        if (open(TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);
            if (open(TOPFILE, ">$file")) {
                print TOPFILE "$in_forum\|$in_topic\n";
                $putno = 1;
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
                    ($tempinforum, $tempintopic) = split(/\|/, $_);
                    unless (($tempinforum eq $in_forum && $tempintopic eq $in_topic) || !(-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi")) {
                        print TOPFILE "$_\n";
                        $putno++;
                    }
                    last if ($putno eq $absmaxcantopic);
                }
                close(TOPFILE);
            }
        }
        else {
            if (open(TOPFILE, ">$file")) {
                print TOPFILE "$in_forum\|$in_topic\n";
                close(TOPFILE);
            }
        }
        &addadminlog("区固顶帖子", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题区固定首行成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        if (open(TOPFILE, "${lbdir}boarddata/catontop$categoryplace.cgi")) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);
        }
        $toptopic = 0;
        foreach (@toptopic) {
            chomp $_;
            next if ($_ eq "");
            ($tempinforum, $tempintopic) = split(/\|/, $_);
            if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                $toptopic++;
            }
        }
        if ($toptopic >= $absmaxcantopic) {$topnum = "<BR><B><font color=$fonthighlight>已经区固定了 $toptopic 个帖子了，如果继续，最早一个被固定的帖子将被自动取消固定。</B></font>"}
        else {$topnum = "<BR><B><font color=$fonthighlight>已经区固定了 $toptopic 个帖子了，你最多可以区固定 $absmaxcantopic 个帖子。</B></font>";}
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="catlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题区固定首行]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub catunlocktop {
    &mischeader("主题取消区固定");

    $cleartoedit = "no";
    if (($membercode eq "ad" || $membercode eq "smo" || ",$catemods," =~ /\Q\,$inmembername\,\E/i) && ($inpassword eq $password)) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit = "no";}
    if ($cleartoedit eq "no" && $checked eq "yes") {&error("主题取消区固定&您不是本分区管理员，或者您的密码错误！");}

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        opendir(CATDIR, "${lbdir}cache");
        my @dirdata = readdir(CATDIR);
        closedir(CATDIR);
        @dirdata = grep (/^forumstop/, @dirdata);
        foreach (@dirdata) {unlink("${lbdir}cache/$_");}
        my $file = "${lbdir}boarddata/catontop$categoryplace.cgi";
        if (open(TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close(TOPFILE);

            if (open(TOPFILE, ">$file")) {
                foreach (@toptopic) {
                    chomp;
                    next if ($_ eq "");
                    my ($tempinforum, $tempintopic) = split(/\|/, $_);
                    unless (($tempinforum eq $in_forum && $tempintopic eq $in_topic) || !(-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi")) {
                        print TOPFILE "$_\n";
                    }
                }
                close(TOPFILE);
            }
        }
        &addadminlog("取消帖子区固顶", $in_topic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>主题取消区固定成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$in_forum">
~;
    }
    else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="catunlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic">
<font color=$fontcolormisc><b>请输入您的用户名、密码进入版主模式 [主题取消区固定]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="登 录"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}
