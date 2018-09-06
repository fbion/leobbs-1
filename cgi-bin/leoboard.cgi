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
    	next if ($_ eq '');
    	s/\\/\//g; s/\/[^\/]+$//o;
        unshift(@INC,$_);
    }
}

use LBCGI;
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print "<script language='javascript'>document.location = 'leobbs.cgi'</script>";
exit;
