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

use strict;
use warnings;
use diagnostics;

use diagnostics;

use LBCGI;
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use VISITFORUM qw(getlastvisit setlastvisit);
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/mpic.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "dispclick.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") {$cookiepath = $mycookiepath;}
elsif ($COOKIE_USED eq 1) {$cookiepath = "";}
else {
    $boardurltemp = $boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
    #    $cookiepath =~ tr/A-Z/a-z/;
}

$in_forum = $query->param('forum');
$in_topic = $query->param('topic');
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic !~ /^[0-9]+$/) || ($in_forum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$instart = $query->param('start');
$instart = 0 if ($instart eq "");

$in_member_name = $query->cookie("amembernamecookie");
$in_password = $query->cookie("apasswordcookie");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&ipbanned; #封杀一些 ip

$currenttime = time;

if ((!$in_member_name) or ($in_member_name eq "客人")) {
    $in_member_name = "客人";
    $myrating = "-1";
    $mymembercode = "no";
    &error("普通错误&客人不能查看!");
}
else {
    &getmember("$in_member_name", "no");
    $mymembercode = $member_code;
    $myrating = $rating;
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");
}

&getoneforum("$in_forum");
$myinmembmod = $inmembmod;

if (($allowed_entry{$in_forum} eq "yes") || (($test_entry eq $forum_pass) && ($test_entry ne "")) || ($member_code eq "ad") || ($inmembmod eq "yes") || ($member_code eq 'smo')) {$allowed = "yes";}
else {$allowed = "no";}

$addtimes = ($timedifferencevalue + $timezone) * 3600;
$myrating = -6 if ($myrating eq "");
&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$member_code,/);
if ($allow_users ne '') {
    &error('进入论坛&你不允许进入该论坛！') if (",$allow_users," !~ /,$in_member_name,/i && $member_code ne 'ad');
}

if ($member_code ne 'ad' && $member_code ne 'smo' && $inmembmod ne 'yes') {
    &error("普通错误&你无权查看！");
}

if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

print header(-expires => "$EXP_MODE", -cache => "$CACHE_MODES");

my $filetoopen = "${lbdir}forum$in_forum/$in_topic.pl";
open(FILE, "$filetoopen");
my $topicinfo = <FILE>;
close(FILE);
chomp $topicinfo;
$topicinfo =~ s/[\a\f\n\e\0\r]//isg;
($topicid, $topictitle, $topicdescription) = split(/\t/, $topicinfo);
$topictitletemp = $topictitle;
$topictitletemp =~ s/^＊＃！＆＊//;
$topictitletemp =~ s/ \(无内容\)$//;
$topictitletemp =~ s/\&\#039\;//isg;
$topictitletemp = &cleaninput($topictitletemp);

if (open(FILE, "${lbdir}forum$in_forum/$in_topic.clk.pl")) {
    sysread(FILE, my $threads, (stat(FILE))[7]);
    close(FILE);
    $threads =~ s/\r//isg;
    @threads = split(/\n/, $threads);
    @threads = reverse(@threads);
    $numberofitems = @threads;
}

my $tempnumberofpages = $numberofitems / $maxtopics;
$numberofpages = int($tempnumberofpages);
$numberofpages++ if ($numberofpages != $tempnumberofpages);

if ($numberofpages > 1) {
    $startarray = $instart;
    $endarray = $instart + $maxtopics - 1;
    $endarray = $numberofitems - 1 if ($endarray >= $numberofitems);

    if ($replynum eq "last" && $treeview ne "yes") {
        $instart = ($numberofpages - 1) * $maxtopics;
        $startarray = $instart;
        $endarray = $numberofitems - 1;
    }

    my $currentpage = int($instart / $maxtopics) + 1;
    my $endstart = ($numberofpages - 1) * $maxtopics;
    my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?forum=$in_forum&topic=$in_topic&start=0 title="首 页" ><font face=webdings>9</font></a>~;
    my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?forum=$in_forum&topic=$in_topic&start=$endstart title="尾 页" ><font face=webdings>:</font></a>~;

    my $uppage = $currentpage - 1;
    my $nextpage = $currentpage + 1;
    my $upstart = $instart - $maxtopics;
    my $nextstart = $instart + $maxtopics;
    my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?forum=$in_forum&topic=$in_topic&start=$upstart title="第$uppage页"><font face=webdings>7</font></a>~;
    my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?forum=$in_forum&topic=$in_topic&start=$nextstart title="第$nextpage页"><font face=webdings>8</font></a>~;

    my $tempstep = $currentpage / 7;
    my $currentstep = int($tempstep);
    $currentstep++ if ($currentstep != $tempstep);
    my $upsteppage = ($currentstep - 1) * 7;
    my $nextsteppage = $currentstep * 7 + 1;
    my $upstepstart = ($upsteppage - 1) * $maxtopics;
    my $nextstepstart = ($nextsteppage - 1) * $maxtopics;
    my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?forum=$in_forum&topic=$in_topic&start=$upstepstart class=hb title="第$upsteppage页">←</a> ~;
    my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?forum=$in_forum&topic=$in_topic&start=$nextstepstart class=hb title="第$nextsteppage页">→</a> ~;

    $pages = "";
    my $currentstart = $upstepstart + $maxtopics;
    for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++) {
        last if ($i > $numberofpages);
        $pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?forum=$in_forum&topic=$in_topic&start=$currentstart class=hb>$i</a> ~;
        $currentstart += $maxtopics;
    }
    $pages = "<font color=$menufontcolor><b>共 <font color=$fonthighlight>$numberofpages</font> 页</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font><br>";
}
else {
    $startarray = 0;
    $endarray = $numberofitems - 1;
    $pages = "<font color=$menufontcolor>只有一页</font><br>";
}

&title;

$output .= qq~<br>~;
if (-e "${lbdir}cache/forumstopic$in_forum.pl") {
    eval {require "${lbdir}cache/forumstopic$in_forum.pl";};
    if ($@) {
        unlink("${lbdir}cache/forumstopic$in_forum.pl");
        require "dotopic.pl";
    }
}
else {require "dotopic.pl";}

my $topictitletempshow = &lbhz($topictitletemp, 34);
$tempoutput =~ s/topictitletempshow/$topictitletempshow 的访问记录/isg;
$tempoutput =~ s/jhimage/$jhimage/isg;

$output .= $tempoutput;

$output .= qq~<BR>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$titlecolor>
<td width=33% align=center $catbackpic><font face="$font" color=$titlefontcolor><b>访 问 者</b></td>
<td width=33% align=center $catbackpic><font face="$font" color=$titlefontcolor><b>访 问 ＩＰ</b></td>
<td width=33% align=center $catbackpic><font face="$font" color=$titlefontcolor><b>访 问 时 间</b></td>
</tr>
~;
$addtimes = ($timedifferencevalue + $timezone) * 3600;

foreach (@threads[$startarray .. $endarray]) {
    chomp $_;
    #    next if ($_ eq "");
    ($recordmembername, $recordipaddress, $recordtrueipaddress, $recordtime) = split(/\t/, $_);
    #    next if ($membername eq "");

    if ($recordipaddress eq $recordtrueipaddress) {$recordipaddress = "";}
    else {$recordipaddress = qq~<BR><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$recordipaddress',420,320)" title="LB WHOIS信息">$recordipaddress</span>~;}

    ($ip1, $ip2, $ip3, $ip4) = split(/\./, $recordtrueipaddress);

    if ($mymembercode eq "ad") {
        $recordtrueipaddress = qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$recordtrueipaddress',420,320)" title="LB WHOIS信息">$recordtrueipaddress</span>$recordipaddress~;
    }
    elsif ($mymembercode eq "smo") {
        if ($smocanseeip eq "no") {$recordtrueipaddress = qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$recordtrueipaddress',420,320)" title="LB WHOIS信息">$recordtrueipaddress</span>$recordipaddress~;}
        else {
            if ($pvtip eq "on") {$recordtrueipaddress = qq~<span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$recordtrueipaddress',420,320)" title="LB WHOIS信息">$recordtrueipaddress</a>$recordipaddress~;}
            else {$recordtrueipaddress = "已设置保密";}
        }
    }
    elsif ($myinmembmod eq "yes") {
        if ($pvtip eq "on") {$recordtrueipaddress = "$ip1.$ip2.$ip3.*";}
        else {$recordtrueipaddress = "已设置保密";}
    }

    if ($lastcolor eq $postcolortwo) {
        $color = $postcolorone;
        $fontcolor = $postfontcolorone;
    }
    else {
        $color = $postcolortwo;
        $fontcolor = $postfontcolortwo;
    }

    $recordtime = &dateformat($recordtime + $addtimes);

    unless ($recordmembername eq "客人") {
        $ppp = qq~<a href="profile.cgi?action=show&member=~ . uri_escape($recordmembername) . qq~" target=_blank><font face=$font color=$fontcolor>$recordmembername</font></a>~;
    }
    else {
        $ppp = qq~<font face="$font" color=$fontcolor>$recordmembername~;
    }

    $output .= qq~
<tr bgcolor=$color>
<td width=33% align=center>$ppp</td>
<td width=33% align=center><font face="$font" color=$fontcolor>$recordtrueipaddress</td>
<td width=33% align=center><font face="$font" color=$fontcolor>$recordtime</td>
</tr>
~;
    $lastcolor = $color;

}

$output .= qq~</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT><img src=$imagesurl/images/none.gif height=3 width=0><BR><table cellpadding=0 cellspacing=2 width=$tablewidth align=center><tr bgcolor=$menubackground height=4></tr><tr><td><font color=$menufontcolor>&nbsp;$pages</td>~;
$output .= qq~</tr></table><br>~;

&output("$topictitletemp 的访问记录 @ $forumname", \$output);
exit;
