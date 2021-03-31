#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
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
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
use testinfo qw(ipwhere);

my $queryme = new LBCGI;
my $in_member_name = $queryme->cookie("amembernamecookie");
my $in_password = $queryme->cookie("apasswordcookie");
my $password;
my $userregistered;
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

my $query = $queryme->param('q');
if ((!$in_member_name) or ($in_member_name eq "客人")) {
    $in_member_name = "客人";
}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    &error("普通错误&老大，偷用户名不偷密码有什么用呢？") if ($in_password ne $password);
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");
}
my $member_code;
if (($member_code ne "ad") && ($member_code ne "smo")) {
    &error("普通错误&你不是本论坛的坛主或总斑竹，所以不能使用该功能！");
}

if (($query ne "") && ($query !~ /^[0-9\.]+$/)) {
    &error("普通错误&请不要胡乱使用本功能！");
}
my $fromwhere;
my $EXP_MODE;
my $CACHE_MODES;
if ($query ne "") {
    $fromwhere = &ipwhere("$query");
    $fromwhere = "ＩＰ: $query\n<BR>来自: $fromwhere\n<BR><BR>如果对结果有疑问，请<a href=whois.cgi?query=$query>按此使用 NIC 数据库查询</a>！"
}
else {$fromwhere = "没有IP数据,我查什么啊!";}
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
print $fromwhere;
exit;
