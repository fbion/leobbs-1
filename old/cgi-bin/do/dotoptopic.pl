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

unlink("${lbdir}cache/forumstoptopic$in_forum.pl") if ((-M "${lbdir}cache/forumstoptopic$in_forum.pl") * 86400 >= 300);
if ($abstopcount > 0) {
    foreach (@absontop) {
        chomp $_;
        if ($_ eq "") {
            $abstopcount--;
            next;
        }
        my ($tempinforum, $tempintopic) = split(/\|/, $_);
        my $rr = &readthreadpl($tempinforum, $tempintopic);
        if ($rr ne "") {
            (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetype) = split(/\t/, $rr);
            push(@toptopic, "$topicid\t$tempinforum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype");
        }
        else {$abstopcount--;}
    }
}
else {undef @toptopic;}

if ($cattopcount > 0) {
    foreach (@catontop) {
        chomp $_;
        my ($tempinforum, $tempintopic) = split(/\|/, $_);
        if ($_ eq "" || $absontopdata =~ /\_$tempinforum\|$tempintopic\_/) {
            $cattopcount--;
            next;
        }
        my $rr = &readthreadpl($tempinforum, $tempintopic);
        if ($rr ne "") {
            my ($lastpostdate, $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp, $addmetype) = split(/\t/, $rr);
            push(@toptopic, "$topicid\t$tempinforum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype");
        }
        else {$cattopcount--;}
    }
}
else {undef @toptopic if ($abstopcount <= 0);}

if ($topcount > 0) {
    foreach (@ontop) {
        chomp $_;
        if ($_ eq "") {
            $topcount--;
            next;
        }
        if ($absontopdata =~ /\_$in_forum\|$_\_/) {
            $topcount--;
            next;
        }
        if ($catontopdata =~ /\_$in_forum\|$_\_/) {
            $topcount--;
            next;
        }
        my $rr = &readthreadpl($in_forum, $_);
        if ($rr ne "") {
            (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp, my $addmetype) = split(/\t/, $rr);
            push(@toptopic, "$topicid\t$in_forum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype");
        }
        else {$topcount--;}
    }
}
else {undef @toptopic if ($abstopcount + $cattopcount <= 0);}

if (!(-e "${lbdir}cache/forumstoptopic$in_forum.pl")) {
    open(FILE, ">${lbdir}cache/forumstoptopic$in_forum.pl");
    print FILE qq~\@toptopic = (~;
    foreach (@toptopic) {
        chomp $_;
        $_ =~ s/\\/\\\\/isg;
        $_ =~ s/\"/\\\"/isg;
        $_ =~ s/\$/\\\$/isg;
        $_ =~ s/\@/\\\@/isg;
        print FILE qq~"$_",~ if ($_ ne "");
        $_ =~ s/\\\"/\"/isg;
        $_ =~ s/\\\$/\$/isg;
        $_ =~ s/\\\@/\@/isg;
        $_ =~ s/\\\\/\\/isg;
    }
    print FILE ");\n";
    print FILE "\$abstopcount = $abstopcount;\n";
    print FILE "\$cattopcount = $cattopcount;\n";
    print FILE "\$topcount = $topcount;\n";
    print FILE "1;\n";
    close(FILE);
}
1;
