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
$inforum = $forum;
$intopic = $topic;
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！！") if ($inforum !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

$inmembername = $membername;
$inpassword = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
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

if (!$inmembername) {$inmembername = $query->cookie("amembernamecookie");}
if (!$inpassword) {$inpassword = $query->cookie("apasswordcookie");}
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&ipbanned; #封杀一些 ip
if (($num) && ($num !~ /^[0-9]+$/)) {&error("普通&老大，别乱黑我的程序呀！！！");}
if (!(-e "${lbdir}boarddata/listno$inforum.cgi")) {&error("发表新主题&对不起，这个论坛不存在！如果确定分论坛号码没错，那么请进入管理区修复论坛一次！");}
if ($inmembername eq "" || $inmembername eq "客人") {
    $inmembername = "客人";
    $userregistered = "no";
}
else {
    &getmember("$inmembername");
    &error("普通错误&此用户根本不存在！") if ($inpassword ne "" && $userregistered eq "no");
    if ($inpassword ne $password && $userregistered ne "no") {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}
&doonoff;
$mymembercode = $membercode;
if ($inpost eq "") {&error("添加回复&请输入要续写的内容！");}
if (($membercode eq "banned") || ($membercode eq "masked")) {&error("添加回复&您被禁止发言或者发言被屏蔽，请联系管理员解决！");}
$myrating = $rating;
$myrating = "-6" if !($myrating);
$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100) && ($maxpoststr ne ""));
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}
print header(-charset => UTF -8, -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&moderator("$inforum");
&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$membercode,/);
if ($allowusers ne '') {
    &error('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &error("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &error("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}
my $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
&winlock($filetoopen) if ($OS_USED eq "Nt");
open(FILE, "$filetoopen");
flock(FILE, 1) if ($OS_USED eq "Unix");
my @threads = <FILE>;
close(FILE);
&winunlock($filetoopen) if ($OS_USED eq "Nt");
my ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon, $water) = split(/\t/, $threads[$num - 1]);
if (lc($postermembername) ne lc($inmembername)) {&error("发生错误&文章作者不是你，你不能在此基础上续写");}

&error("发生错误&对不起，本论坛不允许发表或回复超过 <B>$maxpoststr</B> 个字符的文章！") if (((length($inpost) + length($post)) > $maxpoststr) && ($maxpoststr ne "") && ($membercode ne "ad") && ($membercode ne 'smo') && ($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

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
    $relocurl = "topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$num";
}
else {
    $relocurl = "forums.cgi?forum=$inforum";
}
$output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>续写成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$num">返回主题</a><li><a href="forums.cgi?forum=$inforum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul>
</tr></td></table></td></tr></table>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
&output("$boardname - 在$forumname内续写帖子", \$output);