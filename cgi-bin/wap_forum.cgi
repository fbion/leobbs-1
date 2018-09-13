#!/usr/bin/perl
#########################
# 手机论坛WAP版
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
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
$query = new LBCGI;
$LBCGI::POST_MAX = 2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "wap.lib.pl";
require "wap.pl";
require "data/styles.cgi";
$|++;
&waptitle;
$lid = $query->param('lid');
&check($lid);
&getmember("$inmembername") if ($inmembername ne '' || $inmembername ne '客人');
$id = $query->param('forum');
$in_forum = $id;
&getoneforum($in_forum);
$show .= qq~<card  title="$forumname"> ~;
$mymembercode = $membercode;
$myinmembmod = $inmembmod;
$myrating = $rating;
$tempaccess = "forumsallowed" . $in_forum;
$testentry = $query->cookie($tempaccess);
$allowed = $allowedentry{$in_forum} eq "yes" || ($testentry eq $forumpass && $testentry ne "") || $mymembercode eq "ad" || $mymembercode eq "smo" || $myinmembmod eq "yes" ? "yes" : "no";
&errorout("打开文件&老大，别乱黑我的程序呀！") if ($in_forum !~ /^[0-9]+$/ && $in_forum ne 'leobbs.cgi');
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}
&errorout("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$membercode,/);
$addtimes = ($timedifferencevalue + $timezone) * 3600;
&errorout("进入会员论坛查看帖子内容&您是客人没有权限进入!") if ($inmembername eq "客人" && $regaccess eq "on" && &checksearchbot);
&errorout("进入私有论坛&对不起，您没有权限进入该私有论坛！") if ($privateforum eq "yes" && $allowed ne "yes");
if (($startnewthreads eq "cert") && (($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/) || ($inmembername eq "客人")) && ($userincert eq "no")) {&errorout("进入论坛&你一般会员不允许进入此论坛！");}
$paGe = $query->param('paGe');

if ($allowusers ne '') {
    &errorout('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}

if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &errorout("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &errorout("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &errorout("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}
my $r = &msg($inmembername, $password2);
$show .= "<p>$r<a href=\"wap_po.cgi?lid=$lid&amp;f=$in_forum\">发帖</a> <a href=\"wap_index.cgi?lid=$lid\">返回</a></p>";
open(file, "${lbdir}boarddata/listno$id.cgi");
my @allfav = <file>;
close(file);
my $allfile = @allfav;
my $yema = $allfile / $pre;
my $yema = ($yema > int($yema)) ? int($yema) + 1 : $yema;
$paGe = ($paGe eq '' || $paGe <= 0) ? "1" : "$paGe";
my $k = ($paGe - 1) * $pre;
if ($k > $allfile) {$k = 0;}
my $s = $k + $pre - 1;
for ($ij = $paGe - 2; $ij <= $paGe + 3; $ij++) {
    next if ($ij < 1);
    next if ($ij > $allfile / $pre + 1);
    if ($ij ne $paGe) {$newpage .= "<a href=\"wap_forum.cgi?forum=$id&amp;paGe=$ij&amp;lid=$lid\">$ij</a>&nbsp;";}
    else {$newpage .= "<i>$ij</i>&nbsp;";}
}

$newpage or $newpage = '&nbsp;<i>1</i>';

foreach (@allfav[$k .. $s]) {
    $k++;
    chomp;
    next if $_ eq '';
    open(file2, "${lbdir}forum$id/$_.pl");
    my $c = <file2>;
    close(file2);
    my ($top, $title, $no, $threadstate, $threadposts, $threadviews, $startedby) = split(/\t/, $c);
    $title =~ s/＊＃！＆＊//isg;
    $show .= qq~<p><a href="wap_topic.cgi?f=$id&amp;t=$top&amp;lid=$lid&amp;pa=$paGe">$k,$title</a>($threadposts/$threadviews, $startedby)</p>\n~;
}

$show .= qq~<p>[$paGe/$yema页]<br/>$newpage</p><p>跳到 <input type="text" size="4" maxlength="4" name="tz" format="*N"/> <a href="wap_forum.cgi?forum=$id&amp;paGe=\$(tz)&amp;lid=$lid">页</a><br/><a href="wap_index.cgi?lid=$lid">返回首页</a></p>~;
&wapfoot;