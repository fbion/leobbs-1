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
use IO::Socket;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$queryme = new LBCGI;
$in_member_name = $queryme->cookie("amembernamecookie");
$in_password = $queryme->cookie("apasswordcookie");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$query = $queryme->param('query');

if (($query eq "") || ($query !~ /^[0-9\.]+$/)) {
    &error("普通错误&请不要胡乱使用本功能！");
}
if ((!$in_member_name) or ($in_member_name eq "客人")) {
    $in_member_name = "客人";
}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    &error("普通错误&老大，偷用户名不偷密码有什么用呢？") if ($in_password ne $password);
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");
}
if (($member_code ne "ad") && ($member_code ne "smo")) {
    &error("普通错误&你不是本论坛的坛主或总斑竹，所以不能使用该功能！");
}
my $host = "sunny.nic.com";
my $path = "/cgi-bin/whois";
my $content = "domain=$query";
my $port = 80;
my $socketaddr;
openSock();
post($content);
@wholePage = <SOCK>;
close SOCK;
$out = join("", @wholePage);

$out =~ s/(.*?)(<pre>)(.+?)(<\/pre>)(.*?)/<pre>$3<\/pre>/isg;
$out =~ s/<br \/>//isg;
$out =~ s/<p>.*<\/p>//isg;
$out =~ s/<hr>(.*)$//isg;
$out =~ s/<\/pre>(.*)$//isg;
$out = "查询间隔太短，无法获取详细信息，请稍后再试！<BR><BR><BR>" if ($out =~ m/Forbidden/);
$out = qq~LeoBBS WHOIS 详细信息($query)：<BR>数据来源：<a href=http://sunny.nic.com/cgi-bin/whois>NIC Whois</a><BR><BR><BR>~ . $out . "<center><hr width=500><font color=black>版权所有：<a href=http://www.leobbs.com target=_blank>雷傲科技</a> & <a href=http://bbs.leobbs.com target=_blank>雷傲极酷超级论坛</a>　　Copyright 2003-2004<BR>";
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
print $out;
exit;


sub openSock {
    $socketaddr = sockaddr_in $port, inet_aton $host or return(1);
    #print "Connecting to $socketaddr $host, $port";
    socket SOCK, PF_INET, SOCK_STREAM, getprotobyname('tcp') or return(1);
    connect SOCK, $socketaddr or return(1);
    select((select(SOCK), $| = 1)[0]);
    return(0);
}

sub post {
    my $content = shift @_;
    print SOCK "POST http://$host/$path HTTP/1.0\n";
    print SOCK "Content-type: application/x-www-form-urlencoded\n";
    my $contentLength = length $content;
    print SOCK "Content-length: $contentLength\n";
    print SOCK "\n";
    print SOCK "$content";
}
