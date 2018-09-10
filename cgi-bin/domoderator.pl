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
my $filetoopen = "${lbdir}data/allforums.cgi";
open(FILE, $filetoopen);
@forums = <FILE>;
close(FILE);
my @thisforums = grep (/^$inforum\t/, @forums);
$inmembmod = "no";

($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc, $forumpass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $thisforums[0]);
$forummoderator =~ s/\,\,/\,/ig;
$forummoderator =~ s/\, /\,/ig;
$forummoderator =~ s/ \,/\,/ig;
$forummoderator =~ s/\,$//ig;
$forummoderator =~ s/^\,//ig;
my @forummodnames = split(/\,/, $forummoderator);

#父论坛斑竹继承
if ($category =~ /childforum-[0-9]+/) {
    my $tempforumno = $category;
    $tempforumno =~ s/childforum-//;
    my @thisparentforums = grep (/^$tempforumno\t/, @forums);
    (undef, undef, undef, undef, undef, $fmod, undef) = split(/\t/, $thisparentforums[0]);
    $fmod =~ s/\,\,/\,/ig;
    $fmod =~ s/\, /\,/ig;
    $fmod =~ s/ \,/\,/ig;
    $fmod =~ s/\,$//ig;
    $fmod =~ s/^\,//ig;
    @forummodnames1 = split(/\,/, $fmod);
}

#分区版主获得
if (open(CATEFILE, "${lbdir}boarddata/catemod${categoryplace}.cgi")) {
    $catemods = <CATEFILE>;
    close(CATEFILE);
    chomp($catemods);
    $catemods =~ s/\, /\,/ig;
    $catemods =~ s/ \,/\,/ig;
    $catemods =~ s/\,\,/\,/ig;
    $catemods =~ s/\,$//ig;
    $catemods =~ s/^\,//ig;
    @catemodnames = split(/\,/, $catemods);
}

my $cmodnumber = @catemodnames;
my $modnumber = @forummodnames;
my $modnumber1 = @forummodnames1;

$modoutput = qq~<SCRIPT>function surfto(list) { var myindex1 = list.selectedIndex; var newwindow = list.options[myindex1].value; if (newwindow != "") { var msgwindow = window.open("profile.cgi?action=show&member="+newwindow,"",""); }}</SCRIPT>
<img src=$imagesurl/images/team2.gif width=19 align=absmiddle><select OnChange="surfto(this);"><option style="color: $fonthighlight">本版管理员列表</option>~ if ($modnumber > 0 || $modnumber1 > 0 || $cmodnumber > 0);
if ($cmodnumber > 0) {
    $modoutput .= qq~<option style="background-color: $titlecolor">本分类区版主：</option>~;
    foreach (@catemodnames) {
        &getmodout($_);
    }
}
if ($modnumber > 0) {
    $modoutput .= qq~<option style="background-color: $titlecolor">本论坛版主：</option>~;
    foreach (@forummodnames) {
        &getmodout($_);
    }
}
if ($modnumber1 > 0) {
    $modoutput .= qq~<option style="background-color: $titlecolor">父论坛版主：</option>~;
    foreach (@forummodnames1) {
        &getmodout($_);
    }
}
$modoutput .= "</select>\n" if ($modnumber > 0 || $modnumber1 > 0 || $cmodnumber > 0);
$forummodnamestemp = ",$forummoderator,$fmod,$catemods,";
$inmembmod = "yes" if ($forummodnamestemp =~ /\Q\,$inmembername\,\E/i || (($membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && ($forummodnamestemp =~ /,全体版主,/ || $forummodnamestemp =~ /,全体斑竹,/)));

my @childforum1 = grep (/^[0-9]+\tchildforum-$inforum\t/, @forums);
for ($i = 0; $i <= $#childforum1; $i++) {
    chomp $childforum1[$i];
    next if ($childforum1[$i] eq "");
    my ($forumid, $category, $categoryplace, $forumname, $forumdescription, $cforummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threads, $posts, $forumgraphic, $tmp, $tmp, $forumpass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/, $childforum1[$i]);
    next if ($category ne "childforum-$inforum");

    $forumdescription = &HTML("$forumdescription");

    if (open(FILEFORUM, "${lbdir}boarddata/foruminfo$forumid.cgi")) {
        ($lastposttime, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/, <FILEFORUM>);
        close(FILEFORUM);
    }
    else {
        $lastposttime = $todayforumpost = $lastposter = "";
        $threads = $posts = "0";
    }

    ($lastposttime, $threadnumber, $topictitle) = split(/\%\%\%/, $lastposttime);
    if ($topictitle) {
        $topictitle =~ s/^＊＃！＆＊//;
        my $topictitletemp = $topictitle;
        $topictitletemp =~ s/\&lt;/</g;
        $topictitletemp =~ s/\&gt;/>/g;
        $topictitletemp =~ s/\&amp;/\&/g;
        $topictitletemp =~ s/\&nbsp;/ /g;
        $topictitletemp =~ s/  /　/g;
        $topictitletemp =~ s/\&quot;/\\\"/g;
        $topictitletemp = &lbhz($topictitle, 18);
        #     $topictitletemp =~ s/\&/\&amp;/g;
        $topictitletemp =~ s/</\&lt;/g;
        $topictitletemp =~ s/>/\&gt;/g;
        $topictitle = qq~&nbsp;主题： <a href=topic.cgi?forum=$forumid&topic=$threadnumber&replynum=last TITLE="$topictitle">$topictitletemp</a><BR>~;
        $lastposttime = $lastposttime + $timeadd;
        $lastposterfilename = $lastposter;
        $lastposterfilename =~ y/ /_/;
        $lastposterfilename =~ tr/A-Z/a-z/;
        if ($lastposter =~ /\(客\)/) {
            $lastposter =~ s/\(客\)//isg;
            $lastposter = qq~<font title="此为未注册用户">&nbsp;最后发表： $lastposter</font>　<img src="$imagesurl/images/lastpost.gif" width=11>~;
        }
        else {$lastposter = qq~&nbsp;最后发表： <span style="cursor:hand" onClick="javascript:O9('~ . uri_escape($lastposterfilename) . qq~')">$lastposter</span>　<img src="$imagesurl/images/lastpost.gif" width=11>~;}
    }

    $lastposttime = "$lastposttime%%%$threadnumber%%%$topictitle";

    if ($teamlogo =~ m/\.swf$/i) {
        my ($fgwidth, $fgheight) = split(/\|/, $fgheight);
        $teamlogo = qq~<PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><embed src=$imagesurl/myimages/$teamlogo width=$fgwidth height=$fgheight quality=high pluginspage="http:\/\/www.macromedia.com\/shockwave\/download\/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application\/x-shockwave-flash"><\/embed>~;
    }
    elsif ($teamlogo ne "") {$teamlogo = qq~<img src=$imagesurl/myimages/$teamlogo border=0>~;}
    if ($teamlogo eq "") {$team = "";}
    elsif (($teamurl eq "") || ($teamurl eq "http://")) {$team = qq~<a href=forums.cgi?forum=$forumid>$teamlogo</a>~;}
    else {$team = qq~<a href=$teamurl>$teamlogo</a>~;}
    $modnumber = 0;
    $modout = "";
    $adminstyle = 2 if ($adminstyle eq "");
    if ($cforummoderator) {
        $cforummoderator =~ s/\, /\,/gi;
        $cforummoderator =~ s/ \,/\,/gi;
        $cforummoderator =~ s/\,\,/\,/gi;
        $cforummoderator =~ s/\,$//gi;
        $cforummoderator =~ s/^\,//gi;
        my @mods = split(/\,/, $cforummoderator);
        $modnumber = @mods;
        my $modprintnum = 1;
        foreach (@mods) {
            my $modname = $_;
            $modname =~ y/ /_/;
            $modname =~ tr/A-Z/a-z/;

            if (($adminstyle eq 1) || ($modnumber <= 3 && $adminstyle eq 3)) {
                last if ($modprintnum > 3);
                if ($modprintnum != $modnumber) {
                    if (($_ =~ m/管理员/isg) || ($_ =~ m/诚聘中/isg) || ($_ =~ m/暂时空缺/isg) || ($_ =~ m/版主/isg) || ($_ =~ m/斑竹/isg) || ($_ =~ m/坛主/isg)) {$modout .= qq~<font color=$fontcolormisc2>$_</font><BR>~;}
                    else {$modout .= qq~<span style=cursor:hand onClick="javascript:O9('~ . uri_escape($modname) . qq~')">$_</span><BR>~;}
                }
                else {
                    if (($_ =~ m/管理员/isg) || ($_ =~ m/诚聘中/isg) || ($_ =~ m/暂时空缺/isg) || ($_ =~ m/版主/isg) || ($_ =~ m/斑竹/isg) || ($_ =~ m/坛主/isg)) {$modout .= qq~<font color=$fontcolormisc2>$_</font>~;}
                    else {$modout .= qq~<span style=cursor:hand onClick="javascript:O9('~ . uri_escape($modname) . qq~')">$_</span>~;}
                }
                $modprintnum++;
            }
            else {
                if (($_ =~ m/管理员/isg) || ($_ =~ m/诚聘中/isg) || ($_ =~ m/暂时空缺/isg) || ($_ =~ m/版主/isg) || ($_ =~ m/斑竹/isg) || ($_ =~ m/坛主/isg)) {$modout .= qq~<option>~ . &lbhz($_, 10) . qq~</option>~;}
                else {$modout .= qq~<option value="~ . &uri_escape($modname) . qq~">~ . &lbhz($_, 10) . "</option>";}
            }
        }
    }
    if (($adminstyle eq 1) || ($modnumber <= 3 && $adminstyle eq 3)) {
        $modout .= qq~<font color=$fontcolormisc2>More...~ if ($modnumber > 3);
        $modout = "<font color=$fontcolormisc>暂时空缺<BR>诚聘中" if ($modout eq "");
    }
    else {
        $modout = "<option>暂时空缺</option><option>诚聘中</option>" if ($modout eq "");
        $modout = qq~<select onChange="surfto(this)"><option style="background-color: $forumcolorone">版主列表</option><option>----------</option>$modout</select>~;
    }
    $childforum[$i] = qq~$forumname\t$forumdescription\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$hiddenforum\t$forumid\t$modout\t$team\t$miscad4\t$todayforumpost\t~;
}

if ((!(-e "${lbdir}cache/forums$inforum.pl")) && ($forumid ne "")) {
    open(FILE, ">${lbdir}cache/forums$inforum.pl");
    print FILE qq~\$catemods = qq($catemods);\n~;
    print FILE qq~\$forummodnamestemp = qq($forummodnamestemp);\n~;
    print FILE qq~\$modoutput  = qq($modoutput);\n~;
    $thisforums[0] =~ s/\\/\\\\/isg;
    $thisforums[0] =~ s/~/\\\~/isg;
    $thisforums[0] =~ s/\$/\\\$/isg;
    $thisforums[0] =~ s/\@/\\\@/isg;
    print FILE qq(\$thisforums = qq~$thisforums[0]~;\n);
    $thisforums[0] =~ s/\\\~/~/isg;
    $thisforums[0] =~ s/\\\$/\$/isg;
    $thisforums[0] =~ s/\\\@/\@/isg;
    $thisforums[0] =~ s/\\\\/\\/isg;
    for ($i = 0; $i <= $#childforum; $i++) {
        $childforum[$i] =~ s/\\/\\\\/isg;
        $childforum[$i] =~ s/~/\\\~/isg;
        $childforum[$i] =~ s/\$/\\\$/isg;
        $childforum[$i] =~ s/\@/\\\@/isg;
        print FILE qq(\$childforum[$i] = qq~$childforum[$i]~;\n) if ($childforum[$i] ne "");
        $childforum[$i] =~ s/\\\~/~/isg;
        $childforum[$i] =~ s/\\\$/\$/isg;
        $childforum[$i] =~ s/\\\@/\@/isg;
        $childforum[$i] =~ s/\\\\/\\/isg;
    }
    print FILE "1;\n";
    close(FILE);
}
undef $forummoderator;
undef $fmod;
undef @catemodnames;
undef @forummodnames;
undef @forummodnames1;

sub getmodout {
    my $modname = shift;
    return if ($modname eq "");
    my $cleanedmodname = $modname;
    $cleanedmodname =~ s/ /\_/g;
    #        $inmembmod = "yes" if (lc($inmembername) eq lc($modname) || (($membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo") && ($modname eq "全体版主" || $modname eq "全体斑竹")));
    if ($modname =~ m/管理员/isg || m/诚聘中/isg || m/暂时空缺/isg || m/版主/isg || m/斑竹/isg || m/坛主/isg) {
        $modoutput .= qq~<option>$modname</option>~;
    }
    else {
        $modoutput .= qq~<option value="~ . uri_escape($cleanedmodname) . qq~">$modname</option>~;
    }
    return;
}
1;
