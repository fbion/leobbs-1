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
my $filetoopen = "${lbdir}forum$in_forum/foruminfo.cgi";
open(FILE, "$filetoopen");
my $forums = <FILE>;
close(FILE);
($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forum_pass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $forums);

if ($category =~ /childforum-[0-9]+/) {
    $tempforumno = $category;
    $tempforumno =~ s/childforum-//;
    $filetoopen = "${lbdir}forum$tempforumno/foruminfo.cgi";
    open(FILE, "$filetoopen");
    $forums = <FILE>;
    close(FILE);
    (undef, undef, undef, $tempforumname, undef) = split(/\t/, $forums);
    $addlink = qq~ → <a href=forums.cgi?forum=$tempforumno>$tempforumname</a>~;
}
$forumdescription = &HTML("$forumdescription");
$forumdescription =~ s/<BR>//isg;
$forumdescription =~ s/<P>//isg;

if ($indexforum ne "no") {
    $titleoutput = qq~<BR><table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=leobbs.cgi>$board_name</a>$addlink → <a href=forums.cgi?forum=$in_forum>$forumname</a> → misctypehtc</td><td bgcolor=\$navbackground align=right></td></tr></table></td></tr></table>~;
}
else {
    $titleoutput = qq~<BR><table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=forums.cgi?forum=$in_forum>$forumname</a> →　misctypehtc</td><td bgcolor=\$navbackground align=right></td></tr></table></td></tr></table>~;
}

$titleoutput .= qq~<br>~;
if ((!(-e "${lbdir}cache/forumstitle$in_forum.pl")) && ($forumid ne "")) {
    open(FILE, ">${lbdir}cache/forumstitle$in_forum.pl");
    $titleoutput =~ s/\\/\\\\/isg;
    $titleoutput =~ s/~/\\\~/isg;
    $titleoutput =~ s/\$/\\\$/isg;
    $titleoutput =~ s/\@/\\\@/isg;
    $titleoutput =~ s/\\\$/\$/isg;
    print FILE qq(\$titleoutput = qq~$titleoutput~;\n);
    $titleoutput =~ s/\$/\\\$/isg;
    $titleoutput =~ s/\\\~/~/isg;
    $titleoutput =~ s/\\\$/\$/isg;
    $titleoutput =~ s/\\\@/\@/isg;
    $titleoutput =~ s/\\\\/\\/isg;
    print FILE "1;\n";
    close(FILE);
}
$titleoutput =~ s/\$tablewidth/$tablewidth/isg;
$titleoutput =~ s/\$navborder/$navborder/isg;
$titleoutput =~ s/\$navbackground/$navbackground/isg;
$titleoutput =~ s/\$navfontcolor/$navfontcolor/isg;
1;
