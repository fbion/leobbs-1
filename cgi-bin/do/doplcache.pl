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

require "rebuildlist.pl";

if ($inshow eq 0) {
    if ((-e "${lbdir}cache/forumstoptopic$in_forum.pl") && ((-M "${lbdir}cache/forumstoptopic$in_forum.pl") * 86400 < 180)) {
        eval {require "${lbdir}cache/forumstoptopic$in_forum.pl";};
        if (($@) || ($#toptopic < ($abstopcount + $cattopcount + $topcount - 3))) {
            unlink("${lbdir}cache/forumstoptopic$in_forum.pl");
            unlink("${lbdir}cache/plcache$in_forum\_0.pl");
            require "dotoptopic.pl";
        }
    }
    else {require "dotoptopic.pl";}
}
else {undef @toptopic;}

$filetoopen = "${lbdir}boarddata/listno$in_forum.cgi";
if (-e $filetoopen) {
    open(FILE, "$filetoopen");
    sysread(FILE, my $topics, (stat(FILE))[7]);
    close(FILE);
    $topics =~ s/\r//isg;
    @topics = split(/\n/, $topics);
}
else {&error("打开论坛&对不起，这个论坛不存在！如果确定分论坛号码没错，那么请进入管理区修复论坛一次！");}

$numberofitems = @topics;

if ($threadagesstart ne "") {
    unlink("${lbdir}cache/threadages$in_forum\_$inthreadages.pl") if ((-M "${lbdir}cache/threadages$in_forum\_$inthreadages.pl") > 0.5);
    if (-e "${lbdir}cache/threadages$in_forum\_$inthreadages.pl") {
        open(FILE, "${lbdir}cache/threadages$in_forum\_$inthreadages.pl");
        $numberofitems = <FILE>;
        close(FILE);
        chomp $numberofitems;
    }
    else {
        my $threadagelimit = $currenttime - $inthreadages * 86400;
        my $forumtop = 0;
        my $forumbottom = $numberofitems - 1;
        while ($forumbottom > $forumtop + 1) {
            my $linenow = int(($forumbottom + $forumtop) / 2);
            my $topic = @topics[$linenow];
            chomp $topic;

            my $rr = &readthreadpl($in_forum, $topic);
            ($lastpostdate, $no) = split(/\t/, $rr);

            if ($lastpostdate > $threadagelimit) {$forumtop = $linenow;}
            else {$forumbottom = $linenow;}
        }
        $numberofitems = $forumbottom + 1;
        if (!(-e "${lbdir}cache/threadages$in_forum\_$inthreadages.pl")) {
            open(FILE, ">${lbdir}cache/threadages$in_forum\_$inthreadages.pl");
            print FILE "$numberofitems\n";
            close(FILE);
        }
    }
}

my $tempnumberofpages = $numberofitems / $maxthreads;
$numberofpages = int($tempnumberofpages);
$numberofpages++ if ($numberofpages != $tempnumberofpages);

if ($numberofpages > 1) {
    $startarray = $inshow;
    $endarray = $inshow + $maxthreads - 1;
    $endarray = $numberofitems - 1 if ($endarray >= $numberofitems);

    my $currentpage = int($inshow / $maxthreads) + 1;
    my $endstart = ($numberofpages - 1) * $maxthreads;
    my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?forum=$in_forum&show=0$threadagesstart title="首 页" ><font face=webdings>9</font></a>~;
    my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?forum=$in_forum&show=$endstart$threadagesstart title="尾 页" ><font face=webdings>:</font></a>~;

    my $uppage = $currentpage - 1;
    my $nextpage = $currentpage + 1;
    my $upstart = $inshow - $maxthreads;
    my $nextstart = $inshow + $maxthreads;
    my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?forum=$in_forum&show=$upstart$threadagesstart title="第 $uppage 页"><font face=webdings>7</font></a>~;
    my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?forum=$in_forum&show=$nextstart$threadagesstart title="第 $nextpage 页"><font face=webdings>8</font></a>~;

    my $tempstep = $currentpage / 7;
    my $currentstep = int($tempstep);
    $currentstep++ if ($currentstep != $tempstep);
    my $upsteppage = ($currentstep - 1) * 7;
    my $nextsteppage = $currentstep * 7 + 1;
    my $upstepstart = ($upsteppage - 1) * $maxthreads;
    my $nextstepstart = ($nextsteppage - 1) * $maxthreads;
    my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?forum=$in_forum&show=$upstepstart$threadagesstart class=hb title="第 $upsteppage 页">←</a> ~;
    my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?forum=$in_forum&show=$nextstepstart$threadagesstart class=hb title="第 $nextsteppage 页">→</a> ~;

    $topicpages = "";
    my $currentstart = $upstepstart + $maxthreads;
    for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++) {
        last if ($i > $numberofpages);
        $topicpages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=forums.cgi?forum=$in_forum&show=$currentstart$threadagesstart class=hb>$i</a> ~;
        $currentstart += $maxthreads;
    }
    $topicpages = "<font color=$menufontcolor>$beginpage $showup \[ $showupstep$topicpages$shownextstep\] $shownext $endpage　 <b>共<font color=$fonthighlight>$numberofpages</font>页</b></font>";
}
else {
    $startarray = 0;
    $endarray = $numberofitems - 1;
    $topicpages = "<font color=$menufontcolor>本论坛只有一页</font>";
}

foreach $topicid (@topics[$startarray ... $endarray]) {
    chomp $topicid;
    next if (($topicid eq "") || ($topicid !~ /^[0-9]+$/));
    next if (($ontopdata =~ /\_$topicid\_/) || ($absontopdata =~ /\_$in_forum\|$topicid\_/) || ($catontopdata =~ /\_$in_forum\|$topicid\_/));
    my $rr = &readthreadpl($in_forum, $topicid);
    if ($rr ne "") {
        ($lastpostdate, my $topicid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $posticon, $posttemp, $addmetype) = split(/\t/, $rr);
    }
    else {next;}
    push(@toptopic, "$topicid\t$in_forum\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype\n");
}

if (($startarray <= $maxthreads * 4) && ($threadagesstart eq "")) {
    if ((!(-e "${lbdir}cache/plcache$in_forum\_$startarray.pl")) || ((-M "${lbdir}cache/plcache$in_forum\_$startarray.pl") * 86400 > 120)) {
        open(FILE, ">${lbdir}cache/plcache$in_forum\_$startarray.pl");
        print FILE "$topicpages\n";
        print FILE "$abstopcount\t$cattopcount\t$topcount\t\n";
        foreach (@toptopic) {
            chomp $_;
            print FILE "$_\n";
        }
        close(FILE);
    }
}
1;
