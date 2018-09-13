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
require "data/boardinfo.cgi";
require "wap.pl";
mkdir("${lbdir}wap", 0777) if (!(-e "${lbdir}wap"));
chmod(0777, "${lbdir}wap");

$lid = $query->param('lid');
&check($lid);
if ($in_member_name ne '' && $in_member_name ne '客人') {
    $ad = "<a href=\"wap_index.cgi?lid=$lid\">论坛</a> <br/><a href=\"wap_login.cgi?lid=$lid&amp;check=loginout\">注销$in_member_name</a> <a href=\"wap_set.cgi?lid=$lid\">设置</a>";}
else {
    $ad = "<a href=\"wap_login.cgi\">登陆</a> <a href=\"wap_reg.cgi\">注册</a> <a href=\"wap_index.cgi\">论坛</a>";
}
&waptitle;
$show .= qq~<card  title="$board_name">~;
$show .= qq~<p align='center'>$in_member_name,欢迎光临$board_name</p><p>[社区功能]<br/>$ad<br/><a href="wap_new.cgi?lid=$lid">最新帖子</a><br/><a href="wap_sms.cgi?lid=$lid">短消息</a><br/>~;
$show .= qq~</p>~;
&wapfoot;
