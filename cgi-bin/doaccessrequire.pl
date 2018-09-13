#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use strict;
use warnings;
use diagnostics;

if ($inmembername eq "客人") {
    print "<script language='javascript'>document.location = 'loginout.cgi?forum=$in_forum'</script>";
    exit;
}
if ((($userregistered ne "no") && ($allowedentry{$in_forum} eq "yes")) || ($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes") || (($userregistered ne "no") && ($forumpassword eq $forumpass))) {
    $allowforumcookie = cookie(-name => "forumsallowed$in_forum", -value => "$forumpass", -path => "$cookiepath/", -expires => "0");

    print header(-cookie => [ $allowforumcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

    print qq~<script>location.href="$thisprog?forum=$in_forum";</script>~;
    exit;
}
&error("进入论坛&你不允许进入该论坛！");
1;
