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
sub rebuildLIST {
    my %IN = (-Forum => "", @_,);
    undef @sortdat;
    opendir(DIR, "${lbdir}forum$IN{-Forum}");
    my @dirdata = readdir(DIR);
    closedir(DIR);
    @dirdata = grep (/\.thd\.cgi$/, @dirdata);
    foreach (@dirdata) {
        (my $id, my $tr) = split(/\./, $_);
        my $rr = &readthreadpl($IN{-Forum}, $id);
        push(@sortdat, $rr) if ($rr ne "");
    }
    undef @dirdata;
    @sortdat = sort ({$a <=> $b} @sortdat);
    @sortdat = reverse(@sortdat);
    my $allposts = 0;
    my $allthreads = 0;
    my $file = "$lbdir" . "boarddata/listall$IN{-Forum}.cgi";
    if (open(LIST, ">$file")) {
        open(LIST1, ">${lbdir}boarddata/listno$IN{-Forum}.cgi");
        foreach (@sortdat) {
            chomp $_;
            $_ =~ s/[\a\f\n\e\0\r]//isg;
            (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split(/\t/, $_);
            next if (($topicid !~ /^[0-9]+$/) || ($topictitle eq ""));
            print LIST "$topicid\t$topictitle\t$startedby\t$startedpostdate\t\n";
            print LIST1 "$topicid\n";
            $allposts = $allposts + $threadposts;
            $allthreads++;
        }
        close(LIST1);
        close(LIST);
    }
    return("$allthreads|$allposts");
}

sub readthreadpl {
    my ($in_forum, $id) = @_;
    my $topicinfo = "";
    if (open(PLFILE, "${lbdir}forum$in_forum/$id.pl")) {
        $topicinfo = <PLFILE>;
        close(PLFILE);
    }
    else {$topicinfo = "";}
    chomp $topicinfo;
    $topicinfo =~ s/[\a\f\n\e\0\r]//isg;
    (my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $lastpostdate, my $posticon, my $inposttemp, my $addmetype) = split(/\t/, $topicinfo);
    if (($topictitle eq "") || ($startedby eq "") || ($startedpostdate eq "") || ($threadposts eq "") || ($threadposts > 1000000)) {
        open(THDFILE, "${lbdir}forum$in_forum/$id.thd.cgi");
        my @topicall = <THDFILE>;
        close(THDFILE);
        my $topicall = @topicall;
        $topicall--;
        my $postfirst = $topicall[0];
        $postfirst =~ s/[\a\f\n\e\0\r]//isg;
        my $postlast = $topicall[-1];
        $postlast =~ s/[\a\f\n\e\0\r]//isg;
        (my $membername1, my $topictitle1, my $postipaddress1, my $showemoticons1, my $showsignature1, my $postdate1, my $post1, my $posticon1) = split(/\t/, $postfirst);
        (my $membername2, my $topictitle2, my $postipaddress2, my $showemoticons2, my $showsignature2, my $postdate2, my $post2, my $posticon2) = split(/\t/, $postlast);
        if ($post1 =~ /.*?\[UploadFile.{0,6}=(.+?)\].*?/i) {
            ($no, $addmetype) = split(/.*\./, $1);
        }
        else {
            $addmetype = "";
        }

        $topictitle1 =~ s/^＊＃！＆＊//;
        if ($topictitle1 eq "") {
            $topictitle1 = $topictitle2;
            $topictitle1 =~ s/^＊＃！＆＊//;
        }
        $threadviews = ($topicall + 1) * 8 if ($threadviews eq "");
        $membername2 = "" if ($topicall eq 0);
        $post2 = "(保密)" if ($post2 =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/sg);
        $post2 = "(保密)" if ($post2 =~ /LBSALE\[(.*?)\]LBSALE/sg);
        $post2 = &temppost($post2);
        $post2 = &lbhz($post2, 50);

        chomp $posticon1;
        $posticon1 =~ s/\s//isg;
        if ($posticon1 =~ /<br>/i) {
            $posticon1 =~ s/<br>/\t/ig;
            my @temppoll = split(/\t/, $posticon1);
            if ($#temppoll >= 1) {$posticon1 = "<br>";}
            else {$posticon1 = "";}
        }
        if (($posticon =~ m/<br>/i) && ($threadstate ne "poll") && ($threadstate ne "pollclosed")) {$threadstate = "poll";}
        else {$threadstate = "open" if ($threadstate eq "");}
        if ($topictitle1 eq "") {return "";}
        else {
            my $line = "$postdate2\t$id\t$topictitle1\t$topicdescription\t$threadstate\t$topicall\t$threadviews\t$membername1\t$postdate1\t$membername2\t$posticon1\t$post2\t$addmetype\t";
            $line =~ s/[\a\f\n\e\0\r]//isg;
            return("$line");
        }
    }
    else {
        $topictitle =~ s/^＊＃！＆＊//;
        $posticon =~ s/\s//isg;
        if ($posticon =~ /<br>/i) {$posticon = "<br>";}
        $threadviews = ($threadposts + 1) * 8 if ($threadviews eq "");
        if ($topictitle eq "") {return "";}
        else {
            my $line = "$lastpostdate\t$id\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$posticon\t$inposttemp\t$addmetype\t";
            $line =~ s/[\a\f\n\e\0\r]//isg;
            return("$line");
        }
    }
}
1;
