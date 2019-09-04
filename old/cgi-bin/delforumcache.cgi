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

use diagnostics;

use LBCGI;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$queryme = new LBCGI;
$in_member_name   = $queryme->cookie("amembernamecookie");
$in_password     = $queryme->cookie("apasswordcookie");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$in_forum = $queryme -> param('forum');
&error("打开文件&老大，别乱黑我的程序呀！！") if (($in_forum !~ /^[0-9]+$/)||($in_forum eq ""));

if ((!$in_member_name) or ($in_member_name eq "客人")) {
    $in_member_name = "客人";
    &error("普通错误&对不起，请先登录后再使用本功能？")
}
else {
#    &getmember("$in_member_name");
    &getmember("$in_member_name","no");
    &error("普通错误&老大，偷用户名不偷密码有什么用呢？") if ($in_password ne $password);
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");  
}
&getoneforum("$in_forum");
if (($member_code ne "ad")&&($member_code ne "smo")&&($inmembmod ne "yes")){
    &error("普通错误&你不是本论坛的管理员，所以不能使用该功能！") if ($member_code ne "amo");
}
unlink ("${lbdir}cache/forums$in_forum.pl");
unlink ("${lbdir}cache/forumshead$in_forum.pl");
unlink ("${lbdir}cache/forumsone$in_forum.pl");
unlink ("${lbdir}cache/forumstitle$in_forum.pl");
unlink ("${lbdir}cache/forumstop$in_forum.pl");
unlink ("${lbdir}cache/forumstopic$in_forum.pl");
unlink ("${lbdir}cache/forumstoptopic$in_forum.pl");

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^plcache$in_forum\_/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^threadages$in_forum\_/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }

print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq~
<SCRIPT>
alert("本区的所有缓存都被清空了！");
document.location = 'forums.cgi?forum=$in_forum'
</SCRIPT>
~;
exit;
