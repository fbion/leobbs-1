#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use warnings;
use strict;
use diagnostics;

$xzb = "";
if (-e "${lbdir}boarddata/xzb$in_forum.cgi") {
    open(FILEX, "${lbdir}boarddata/xzb$in_forum.cgi");
    my @xzbdata = <FILEX>;
    close(FILEX);
    if (-e "${lbdir}boarddata/xzbs$in_forum.cgi") {
        open(FILEX, "${lbdir}boarddata/xzbs$in_forum.cgi");
        $xzbcount = <FILEX>;
        close(FILEX);
    }
    if ($xzbcount eq "") {$xzbcount = 0;}
    if ($xzbcount >= $#xzbdata) {$xzbcount = 0;}
    else {$xzbcount++;}
    $xzbdata[$xzbcount] =~ s/^＃―＃―・\t//isg;
    (my $title, my $postid, my $msg, my $posttime) = split(/\t/, $xzbdata[$xzbcount]);
    open(FILEX, ">${lbdir}boarddata/xzbs$in_forum.cgi");
    print FILEX $xzbcount;
    close(FILEX);
    if ($title ne "") {
        my $temppostid = $postid;
        $temppostid =~ s/ /\_/isg;
        $temppostid =~ tr/A-Z/a-z/;
        my $titletemps = &lbhz($title, 35);
        $xzb = qq~&nbsp;小字报: <img src=$imagesurl/images/icon.gif width=14> <span style=cursor:hand onClick="javascript:openScript('xzb.cgi?action=view&forum=$in_forum&id=$xzbcount',420,320)" title="$title"><font color=$fonthighlight>$titletemps</font></span> -- <span style=cursor:hand onClick=javascript:O9('~ . uri_escape($temppostid) . qq~')>$postid</span>~;
        $xzb = qq~<B>[<a href=xzbadmin.cgi?forum=$in_forum>管理</a>]</b>$xzb~ if (($member_code eq "ad") || ($member_code eq "smo") || ($inmembmod eq "yes"));
    }
}
1;
