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
$LBCGI::POST_MAX = 1024 * 10000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "addpost.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");
$query = new LBCGI;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") {$cookiepath = $mycookiepath;}
elsif ($COOKIE_USED eq 1) {$cookiepath = "";}
else {
    $boardurltemp = $boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}
for ('forum', 'topic', 'membername', 'password', 'inpost', 'id') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$num = $id;
$in_forum = $forum;
$in_topic = $topic;
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic) && ($in_topic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！！") if ($in_forum !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$in_member_name = $membername;
$in_password = $password;
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}
$currenttime = time;
$inpost =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost =~ s/\[USECHGFONTE\]/\[USECHGFONT\&\#069\;\]/sg;
$inpost =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;
$inpost = &dofilter("$inpost");
$inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&ipbanned; #封杀一些 ip
if (($num) && ($num !~ /^[0-9]+$/)) {&error("普通&老大，别乱黑我的程序呀！！！");}
if (!(-e "${lbdir}boarddata/listno$in_forum.cgi")) {&error("发表新主题&对不起，这个论坛不存在！如果确定分论坛号码没错，那么请进入管理区修复论坛一次！");}
if ($in_member_name eq "" || $in_member_name eq "客人") {
    $in_member_name = "客人";
    $userregistered = "no";
}
else {
    &getmember("$in_member_name");
    &error("普通错误&此用户根本不存在！") if ($in_password ne "" && $userregistered eq "no");
    if ($in_password ne $password && $userregistered ne "no") {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}
&doonoff;
$mymembercode = $member_code;
if ($inpost eq "") {&error("添加回复&请输入要续写的内容！");}
if (($member_code eq "banned") || ($member_code eq "masked")) {&error("添加回复&您被禁止发言或者发言被屏蔽，请联系管理员解决！");}
$myrating = $rating;
$myrating = "-6" if !($myrating);
$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100) && ($maxpoststr ne ""));
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}
print header(-charset => UTF -8, -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&moderator("$in_forum");
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
my $filetoopen = "$lbdir" . "forum$in_forum/$in_topic.thd.cgi";
&winlock($filetoopen) if ($OS_USED eq "Nt");
open(FILE, "$filetoopen");
flock(FILE, 1) if ($OS_USED eq "Unix");
my @threads = <FILE>;
close(FILE);
&winunlock($filetoopen) if ($OS_USED eq "Nt");
my ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon, $water) = split(/\t/, $threads[$num - 1]);
if (lc($postermembername) ne lc($in_member_name)) {&error("发生错误&文章作者不是你，你不能在此基础上续写");}

&error("发生错误&对不起，本论坛不允许发表或回复超过 <B>$maxpoststr</B> 个字符的文章！") if (((length($inpost) + length($post)) > $maxpoststr) && ($maxpoststr ne "") && ($member_code ne "ad") && ($member_code ne 'smo') && ($member_code ne 'cmo') && ($member_code ne "mo") && ($member_code ne "amo") && ($member_code !~ /^rz/) && ($inmembmod ne "yes"));

my $time1 = time;
$time1 = &longdateandtime($time1);

$addnewpost = "[br][br]\[color=$fonthighlight\]\[b\]-=-=-=- 以下内容由 \[i\]$postermembername\[\/i\] 在 \[i\]$time1\[\/i\] 时添加 -=-=-=-\[\/b\]\[\/color\]<br>" . $inpost;

if ($post =~ m/\[ALIPAYE\]/) {
    my ($no, $alipayid, $warename, $oldpost, $wareprice, $wareurl, $postage_mail, $postage_express, $postage_ems) = split(/\[ALIPAYE\]/, $post);

    $newpost = "\[ALIPAYE\]$alipayid\[ALIPAYE\]$warename\[ALIPAYE\]$oldpost$addnewpost\[ALIPAYE\]$wareprice\[ALIPAYE\]$wareurl\[ALIPAYE\]$postage_mail\[ALIPAYE\]$postage_express\[ALIPAYE\]$postage_ems\[ALIPAYE\]";

}
else {
    $newpost = "$post$addnewpost";
}

&winlock($filetoopen) if ($OS_USED eq "Nt");
open(FILE, ">$filetoopen");
flock(FILE, 2) if ($OS_USED eq "Unix");
my $j;
foreach $postline (@threads) {
    chomp $postline;
    $j++;
    if ($num eq $j) {
        my ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon, $water) = split(/\t/, $postline);
        print FILE "$postermembername\t$topictitle\t$postipaddress\t$showemoticons\t$showsignature\t$postdate\t$newpost\t$posticon\t$water\n";
    }
    else {
        print FILE "$postline\n";
    }
}
close(FILE);
&winunlock($filetoopen) if ($OS_USED eq "Nt");
&mischeader("续写贴子");
$gopage = int(($num - 1) / $maxtopics) * $maxtopics;
if ($refreshurl == 1) {
    $relocurl = "topic.cgi?forum=$in_forum&topic=$in_topic&start=$gopage#$num";
}
else {
    $relocurl = "forums.cgi?forum=$in_forum";
}
$output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>续写成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="topic.cgi?forum=$in_forum&topic=$in_topic&start=$gopage#$num">返回主题</a><li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul>
</tr></td></table></td></tr></table>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
&output("$board_name - 在$forumname内续写帖子", \$output);