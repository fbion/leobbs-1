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
open(FILE, "${lbdir}forum${inforum}/foruminfo.cgi");
my $forums = <FILE>;
close(FILE);
($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forum_pass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $forums);

#父论坛斑竹继承
if ($category =~ /childforum-[0-9]+/) {
    my $tempforumno = $category;
    $tempforumno =~ s/childforum-//;
    open(FILE, "${lbdir}forum${tempforumno}/foruminfo.cgi");
    my $forums1 = <FILE>;
    close(FILE);
    (undef, undef, undef, undef, undef, my $fmod, undef) = split(/\t/, $forums1);
    $forummoderator .= ",$fmod";
}

#分区版主获得
if (open(CATEFILE, "${lbdir}boarddata/catemod${categoryplace}.cgi")) {
    my $catemods = <CATEFILE>;
    close(CATEFILE);
    chomp($catemods);
    $forummoderator .= ",$catemods";
}

$forummoderator =~ s/\, /\,/gi;
$forummoderator =~ s/ \,/\,/gi;
$forummoderator =~ s/\,\,/\,/gi;
$forummoderator =~ s/\,$//gi;
$forummoderator =~ s/^\,//gi;
if (!(-e "${lbdir}cache/forumsone$in_forum.pl")) {
    open(FILE, ">${lbdir}cache/forumsone$in_forum.pl");
    $forums =~ s/\\/\\\\/isg;
    $forums =~ s/~/\\\~/isg;
    $forums =~ s/\$/\\\$/isg;
    $forums =~ s/\@/\\\@/isg;
    print FILE qq(\$forums = qq~$forums~;\n);
    $forums =~ s/\\\~/~/isg;
    $forums =~ s/\\\$/\$/isg;
    $forums =~ s/\\\@/\@/isg;
    $forums =~ s/\\\\/\\/isg;
    print FILE qq~\$forummoderator = qq($forummoderator);\n~;
    print FILE "1;\n";
    close(FILE);
}
1;
