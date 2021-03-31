#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

use strict;
use warnings;
use diagnostics;

$threadposts = @threads;
$threadposts--;
my $postfirst = $threads[0];
$postfirst =~ s/[\a\f\n\e\0\r]//isg;
my $postlast = $threads[-1];
$postlast =~ s/[\a\f\n\e\0\r]//isg;
($startedby, $topictitle, my $postipaddress1, my $showemoticons1, my $showsignature1, $startedpostdate, my $post1, $posticon) = split(/\t/, $postfirst);
($lastposter, my $topictitle2, my $postipaddress2, my $showemoticons2, my $showsignature2, $lastpostdate, $inposttemp, my $posticon2) = split(/\t/, $postlast);
$topictitle =~ s/^＊＃！＆＊//;
if ($topictitle eq "") {
    $topictitle = $topictitle2;
    $topictitle =~ s/^＊＃！＆＊//;
}
$topictitle = "＊＃！＆＊$topictitle";
$topicid = $in_topic;

if ($post1 =~ /.*?\[UploadFile.{0,6}=(.+?)\].*?/i) {
    ($no, $addmetype) = split(/.*\./, $1);
}
else {
    $addmetype = "";
}

$threadviews = ($threadposts + 1) * 8 if ($threadviews eq "");
$lastposter = "" if ($threadposts eq 0);
$inposttemp = "(保密)" if ($inposttemp =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/sg);
$inposttemp = "(保密)" if ($inposttemp =~ /LBSALE\[(.*?)\]LBSALE/sg);
$inposttemp = &temppost($inposttemp);
$inposttemp = &lbhz($inposttemp, 50);

chomp $posticon;
$posticon =~ s/\s//isg;
if ($posticon =~ /<br>/i) {
    $posticon =~ s/<br>/\t/ig;
    my @temppoll = split(/\t/, $posticon);
    if ($#temppoll >= 1) {$posticon = "<br>";}
    else {$posticon = "";}
}
if (($posticon =~ m/<br>/i) && ($threadstate ne "poll") && ($threadstate ne "pollclosed")) {$threadstate = "poll";}
else {$threadstate = "open" if ($threadstate eq "");}
1;
