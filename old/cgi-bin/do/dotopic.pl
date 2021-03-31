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

if (-e "${lbdir}boarddata/jinghua$in_forum.cgi") {
    open(FILE, "${lbdir}boarddata/jinghua$in_forum.cgi");
    my @jhdatas = <FILE>;
    close(FILE);
    $jhdata = join("\_", @jhdatas);
    $jhdata = "\_$jhdata\_";
    $jhdata =~ s/\W//isg;
}

if (($category =~ /childforum-[0-9]+/) && ($indexforum ne "no")) {
    $tempforumno = $category;
    $tempforumno =~ s/childforum-//;
    $filetoopen = "${lbdir}forum$tempforumno/foruminfo.cgi";
    open(FILE, "$filetoopen");
    my $forums = <FILE>;
    close(FILE);
    (undef, undef, undef, $tempforumname, undef) = split(/\t/, $forums);
    $addlink = qq~ → <a href=forums.cgi?forum=$tempforumno>$tempforumname</a>~;
}
$forumdescription = &HTML("$forumdescription");
$forumdescription =~ s/<BR>//isg;
$forumdescription =~ s/<P>//isg;

if ($indexforum ne "no") {
    $tempoutput = qq~<table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=leobbs.cgi>$board_name</a>$addlink → <a href=forums.cgi?forum=$in_forum>$forumname</a> [<a href=forums.cgi?forum=$in_forum&show=\$inshow>返回</a>] → 浏览：topictitletempshow　jhimage</td><td bgcolor=\$navbackground align=right valign=bottom>\$uservisitdata</td></tr></table></td></tr></table>~;
}
else {
    $tempoutput = qq~<table width=\$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> $forumdescription</td></tr></table><table width=\$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=\$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3><tr height=25><td bgcolor=\$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=12> <font color=\$navfontcolor><a href=forums.cgi?forum=$in_forum>$forumname</a> [<a href=forums.cgi?forum=$in_forum&show=\$inshow>返回</a>] → 浏览：topictitletempshow　jhimage</td><td bgcolor=\$navbackground align=right valign=bottom>\$uservisitdata</td></tr></table></td></tr></table>~;
}
if (open(FILE, "${lbdir}data/notshowsignature.cgi")) {
    $notshowsignaturemember = <FILE>;
    close(FILE);
}
$notshowsignaturemember =~ s/^\t//;
$notshowsignaturemember =~ s/\t$//;
$notshowsignaturemember = "\t$notshowsignaturemember\t";

if (!(-e "${lbdir}cache/forumstopic$in_forum.pl")) {
    open(FILE, ">${lbdir}cache/forumstopic$in_forum.pl");
    print FILE qq~\$notshowsignaturemember=qq($notshowsignaturemember);\n~;
    $tempoutput =~ s/\\/\\\\/isg;
    $tempoutput =~ s/~/\\\~/isg;
    $tempoutput =~ s/\$/\\\$/isg;
    $tempoutput =~ s/\@/\\\@/isg;
    $tempoutput =~ s/\\\$/\$/isg;
    print FILE qq(\$tempoutput =qq~$tempoutput~;\n);
    $tempoutput =~ s/\$/\\\$/isg;
    $tempoutput =~ s/\\\~/~/isg;
    $tempoutput =~ s/\\\$/\$/isg;
    $tempoutput =~ s/\\\@/\@/isg;
    $tempoutput =~ s/\\\\/\\/isg;
    print FILE qq~\$jhdata=qq($jhdata);\n~;
    print FILE "1;\n";
    close(FILE);
}

$tempoutput =~ s/\$inshow/$inshow/isg;
$tempoutput =~ s/\$uservisitdata/$uservisitdata/isg;
$tempoutput =~ s/\$tablewidth/$tablewidth/isg;
$tempoutput =~ s/\$navborder/$navborder/isg;
$tempoutput =~ s/\$navbackground/$navbackground/isg;
$tempoutput =~ s/\$navfontcolor/$navfontcolor/isg;
$jhdata = "" if ($usejhpoint ne "yes");

1;
