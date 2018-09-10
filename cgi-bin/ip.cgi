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
require "data/boardinfo.cgi";
use testinfo qw(ipwhere osinfo browseinfo);

print "Content-type: text/html;Charset=UTF-8\n\n";

my $ipaddress = $ENV{"REMOTE_ADDR"};
my $trueipaddress = $ENV{"HTTP_CLIENT_IP"};
$trueipaddress = $ENV{"HTTP_X_FORWARDED_FOR"} if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
$trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
my $fromwhere1 = &ipwhere("$trueipaddress");
print "您的 IP 地址：$trueipaddress，来源鉴定：$fromwhere1<BR>";
if ($ipaddress ne $trueipaddress) {
    my $fromwhere2 = &ipwhere("$ipaddress");
    print "代理 IP 地址：$ipaddress，来源鉴定：$fromwhere2<BR>";
}
else {print "代理 IP 地址未知(没有使用代理、代理服务器 IP 显示被禁止)";}
eval {my $osinfo = &osinfo();};
my $osinfo;
my $browseinfo;
my $ENV;
if ($@) {$osinfo = "Unknow";}
eval {$browseinfo = &browseinfo();};
if ($@) {$browseinfo = "Unknow";}
print "<BR><BR>您的操作系统是：$osinfo，使用的浏览器是：$browseinfo<BR>($ENV{\"HTTP_USER_AGENT\"})<BR>";
