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
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
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

$queryme = new LBCGI;
$inmembername   = $queryme->cookie("amembernamecookie");
$inpassword     = $queryme->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$inmembername) or ($inmembername eq "客人")) {
    $inmembername = "客人";
    &error("普通错误&对不起，请先登录后再使用本功能？")
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("普通错误&老大，偷用户名不偷密码有什么用呢？") if ($inpassword ne $password);
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");  
}

$cleanmembername = $inmembername;
$cleanmembername =~ s/ /\_/isg;
$cleanmembername =~ tr/A-Z/a-z/;
unlink ("${lbdir}cache/myinfo/$cleanmembername.pl");
unlink ("${lbdir}cache/meminfo/$cleanmembername.pl");
unlink ("${lbdir}cache/mymsg/$cleanmembername.pl");
unlink ("${lbdir}cache/online/$cleanmembername.pl");
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq~
<SCRIPT>
alert("您在论坛的所有缓存都被清空了！");
document.location = 'leobbs.cgi'
</SCRIPT>
~;
exit;
