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

use LBCGI;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;
use testinfo qw(ipwhere);

$queryme = new LBCGI;
$inmembername   = $queryme->cookie("amembernamecookie");
$inpassword     = $queryme->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$query = $queryme -> param('q');
if ((!$inmembername) or ($inmembername eq "客人")) {
    $inmembername = "客人";
}
else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("普通错误&老大，偷用户名不偷密码有什么用呢？") if ($inpassword ne $password);
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");  
}
if (($membercode ne "ad")&&($membercode ne "smo")){
    &error("普通错误&你不是本论坛的坛主或总斑竹，所以不能使用该功能！") ;
}

if (($query ne "")&&($query !~ /^[0-9\.]+$/)) {
    &error("普通错误&请不要胡乱使用本功能！") ;
}
if ($query ne "") { $fromwhere = &ipwhere("$query"); $fromwhere = "ＩＰ: $query\n<BR>来自: $fromwhere\n<BR><BR>如果对结果有疑问，请<a href=whois.cgi?query=$query>按此使用 NIC 数据库查询</a>！"} else { $fromwhere = "没有IP数据,我查什么啊!"; }
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print $fromwhere;
exit;
