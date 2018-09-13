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

$show .= qq~<card  title="$board_name">~;
$in_member_name = $query->param('n1');
if ($in_member_name ne '') {
    # login
    $in_member_name = $uref->fromUTF8("UTF-8", $in_member_name);
    $in_password = $query->param('p');
    if ($in_password ne "") {
        eval {$in_password = md5_hex($in_password);};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
        unless ($@) {$in_password = "lEO$in_password";}
    }
    if ($in_member_name eq "" || $in_member_name eq "客人") {
        $in_member_name = "客人";
    }
    else {
        &getmember("$in_member_name", "no");
        &errorout("普通错误&此用户根本不存在！") if ($userregistered eq "no");
        if ($in_password ne $password) {
            &errorout("普通错误&密码与用户名不相符，请重新登录！");}
    }
    FILE:
    my $x = &myrand(1000000000);
    $x = crypt($x, aun);
    $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
    $x =~ s/[^\w\d]//g;
    $x = substr($x, 2, 9);
    if (-e "${lbdir}wap/$x") {goto FILE;}
    my $xh2 = $ENV{'REMOTE_ADDR'};
    open(file, ">${lbdir}wap/$x");
    print file "$in_member_name,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2";
    close(file);

    open(file, "${lbdir}wap/all.h");
    my @s = <file>;
    close(file);

    open(file, ">${lbdir}wap/all.h");
    foreach (@s) {
        chomp;
        my ($n, $s) = split(/\,/, $_);
        if ($in_member_name eq $n) {
            unlink "${lbdir}wap/$s";
        }
        else {print file "$_\n";}
    }
    print file "$in_member_name,$x\n";
    close(file);
    $show .= qq~<p>您的幸运ID为：$x,您的IP为：$xh2，请不要泄漏您的幸运ID给任何人！如果您是用手机访问且手机为私有，请把下面进入的首页地址加入书签(书签地址：$boardurl/wap.cgi?lid=$x ，加入之后可免登陆) 。否则请不要加入书签！</p><p><a href="wap.cgi?lid=$x">点击此处进入首页</a></p>~;
    &wapfoot;
}

$lid = $query->param('lid');
$lid = 'a' if ($lid eq "");
&check($lid);
if (-e "${lbdir}wap/leoM.cgi") {
    require "${lbdir}wap/leoM.cgi";
}
else {
    my $filetoopen = "$lbdir" . "data/allforums.cgi";
    open(FILE, "$filetoopen");
    my @forums = <FILE>;
    close(FILE);
    $a = 0;
    foreach (@forums) {
        $a = sprintf("%09d", $a);
        chomp $_;
        ($forumid, $category, $categoryplace, $forumname, my $no, $bz) = split(/\t/, $_);
        next if ($forumid !~ /^[0-9]+$/);
        if ($category =~ /^childforum-[0-9]+/) {
            $topforumno = $category;
            $topforumno =~ s/^childforum-//;
            my $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$bz\t$forumid\t$topforumno\t");
            push(@cforums, $rearrange);
            next;
        }
        $categoryplace = sprintf("%09d", $categoryplace);
        my $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$bz\t$forumid\t");
        push(@rearrangedforums, $rearrange);
        $a++;
    }
    my @rearrangedforums1 = sort (@rearrangedforums);
    undef @rearrangedforums;
    foreach (@rearrangedforums1) {
        chomp $_;
        ($categoryplace, my $a, $category, $forumname, $bz, $forumid) = split(/\t/, $_);
        push(@rearrangedforums, "$categoryplace\t$a\t$category\t$forumname\t$bz\t$forumid\t");
        @tempcforum = grep (/\t$forumid\t$/i, @cforums);
        push(@rearrangedforums, @tempcforum);
    }
    foreach (@rearrangedforums) {
        chomp $_;
        ($categoryplace, my $a, $category, $forumname, $bz, $forumid) = split(/\t/, $_);
        $categoryplace = sprintf("%01d", $categoryplace);
        if ($categoryplace ne $lastcategoryplace) {
            $r1 .= "$category<br>";
        }
        if ($category =~ /^childforum-[0-9]+/) {
            $addspace = "&nbsp;";
        }
        else {
            $addspace = "";
        }
        $r1 .= qq~$addspace<a href="wap_forum.cgi?forum=$forumid&amp;lid=sidFid">$forumname</a><br>~;
        $lastcategoryplace = $categoryplace;
    }
    $r1 =~ s/~/\\\~/g;
    open(file, ">${lbdir}wap/leoM.cgi");
    print file "\$r1=qq~$r1~;1;";
    close(file);
}

my $r = &msg($in_member_name);
$show .= qq~<p>$in_member_name,$board_name欢迎您！<br/><a href="wap_new.cgi?lid=$lid">最新帖子</a><br/><a href="wap_sms.cgi?lid=$lid">短消息</a><br/>$r\n~;
my @a = split(/\<br>/, $r1);
my $allfile = @a;
my $yema = $allfile / $pre_index;
my $yema = ($yema > int($yema)) ? int($yema) + 1 : $yema;
$paGe = $query->param('paGe');
$paGe = ($paGe eq '' || $paGe <= 0) ? "1" : "$paGe";
my $k = ($paGe - 1) * $pre_index;
if ($k > $allfile) {$k = 0;}
my $s = $k + $pre_index - 1;
for ($ij = $paGe - 6; $ij <= $paGe + 6; $ij++) {
    next if ($ij < 1);
    next if ($ij > $allfile / $pre_index + 1);
    if ($ij ne $paGe) {$newpage .= " <a href=\"wap_index.cgi?paGe=$ij&amp;lid=$lid\">$ij</a> ";}
    else {$newpage .= " <i>$ij</i> ";}
}
$newpage or $newpage = '<i>1</i>';

foreach (@a[$k .. $s]) {
    next if $_ eq '';
    $_ =~ s/sidFid/$lid/g;
    $show .= $_ . '<br/>';
}
$show .= '<br/>[' . $paGe . '/' . $yema . '页]<br/>' . $newpage . '</p>';
&wapfoot;