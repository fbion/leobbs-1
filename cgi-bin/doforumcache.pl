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

$docache = "yes";
open(LOCKFILE, ">${lbdir}cache/forumcache-$skin.pl.lock");
print LOCKFILE "die;";
close(LOCKFILE);
if (open(FILE, "${lbdir}data/allforums.cgi")) {
    sysread(FILE, $forums, (stat(FILE))[7]);
    close(FILE);
    $forums =~ s/\r//isg;
}
else {
    unlink("${lbdir}cache/forumcache-$skin.pl.lock");
    &error("论坛还没建立&请先在管理区建立分论坛！或者分类信息完全丢失，请坛主到管理区重建论坛主界面！");
}
@forums = split(/\n/, $forums);

my $a = 0;
foreach $forum (@forums) {
    $a = sprintf("%09d", $a);
    chomp $forum;
    next if (length("$forum") < 30);
    ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator, $htmlstate, $idmbcodestate, $privateforum, $startnewthreads, $lastposter, $lastposttime, $threadsno, $postsno, $forumgraphic, $tmp, $tmp, $forumpass, $hiddenforum, $indexforum, $teamlogo, $teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpostno, $miscad5) = split(/\t/, $forum);
    next if (($forumid !~ /^[0-9]+$/) || ($forumname eq ""));
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
        #	$topictitletemp =~ s/\&/\&amp;/g;
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

    if ($category =~ /^childforum-[0-9]+/) {
        $cforums[$forumid] = "$forumid\t$category\t$hiddenforum\t$forumname\t";
        $topforumno = $category;
        $topforumno =~ s/^childforum-//;
        $threadadds[$topforumno] += $threads;
        $postadds[$topforumno] += $posts;
        ($todayforumpost, $todayforumposttime) = split(/\|/, $todayforumpost);
        $todayforumpost = 0 if (($nowtime ne $todayforumposttime) || ($todayforumpost eq ""));
        $todayforumpostadds[$topforumno] += $todayforumpost;
        ($olastposttime, undef) = split(/\%\%\%/, $lastposttime[$topforumno]);
        ($clastposttime, undef) = split(/\%\%\%/, $lastposttime);
        if (($clastposttime > $olastposttime || ($lastposttime[$topforumno] eq "" && $lastposter[$topforumno] eq "")) && ($privateforum ne "yes")) {
            $lastposttime[$topforumno] = $lastposttime . "%%%$forumid";
            $lastposter[$topforumno] = $lastposter;
        }
        $lvisit .= "$forumid-$currenttime--";
    }
    else {
        $lastposttime[$forumid] = $lastposttime;
        $lastposter[$forumid] = $lastposter;
        $categoryplace = sprintf("%09d", $categoryplace);
        $rearrange = ("$categoryplace\t$a\t$category\t$forumname\t$forumdescription\t$privateforum\t$startnewthreads\t$lastposter\t$lastposttime\t$threads\t$posts\t$hiddenforum\t$forumid\t$team\t$miscad4\t$todayforumpost\t");
        push(@rearrangedforums, $rearrange);
        $lvisit .= "$forumid-$currenttime--";
        $a++;
    }

    $modnumber = 0;
    $modout = "";
    $adminstyle = 2 if ($adminstyle eq "");
    if ($forummoderator) {
        $forummoderator =~ s/\, /\,/gi;
        $forummoderator =~ s/ \,/\,/gi;
        $forummoderator =~ s/\,\,/\,/gi;
        $forummoderator =~ s/\,$//gi;
        $forummoderator =~ s/^\,//gi;
        my @mods = split(/\,/, $forummoderator);
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
                else {$modout .= qq~<option value="~ . &uri_escape($_) . qq~">~ . &lbhz($_, 10) . "</option>";}
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
    $modout[$forumid] = $modout;
}
@rearrangedforums = sort (@rearrangedforums);
@forums = @cforums;

if (-e "$lbdir/data/todaypost.cgi") {
    open(FILE, "$lbdir/data/todaypost.cgi");
    $todaypost = <FILE>;
    close(FILE);
    chomp $todaypost;
    ($nowtoday, $todaypostno, $maxday, $maxdaypost, $yestdaypost) = split(/\t/, $todaypost);
    if ($nowtoday ne $nowtime) {
        $yestdaypost = $todaypostno;
        $todaypostno = 0;
    }
}
else {
    $maxday = $nowtime;
    $yestdaypost = 0;
    $todaypostno = 0;
    $maxdaypost = 0;
}
$yestdaypost = 0 if ($yestdaypost eq "");
$todaypostlist = qq~<font color=\$titlecolor>　■ </font><font color=\$postfontcolortwo>昨/今日新帖: $yestdaypost/<font color=\$fonthighlight><b>$todaypostno</b></font> 篇</font><BR><font color=\$titlecolor>　■ </font><font color=\$postfontcolorone title="发生日期: $maxday">历史最高一天发帖量: <b>$maxdaypost</b> 篇</font><BR>~;

eval {require "data/boardstats.cgi";};
if ($@) {
    require "repireboardinfo.pl";
    require "data/boardstats.cgi";
}

$cleanlastregistered = $lastregisteredmember;
$cleanlastregistered =~ y/ /_/;
$cleanlastregistered =~ tr/A-Z/a-z/;
$cleanlastregistered = qq~<span style="cursor:hand" onClick="javascript:O9('~ . uri_escape($cleanlastregistered) . qq~')">$lastregisteredmember</span>~;
$todaypostlist = qq~<td bgcolor=$forumcolortwo width=210><font color=$titlecolor>　■ </font><font color=$postfontcolorone>最后注册会员: $cleanlastregistered</font><BR><font color=$titlecolor>　■ </font><font color=$postfontcolortwo>注册会员总数:  <a href="memberlist.cgi?a=5" target=_blank><b><font color=#990000>$totalmembers</font></b></a> 人<br></font><font color=$titlecolor>　■ </font><font color=$postfontcolorone>论坛主题总数: <b>$totalthreads</b> 篇</font><br><font color=$titlecolor>　■ </font><font color=$postfontcolortwo>论坛回复总数: <b>$totalposts</b> 篇</font><br><font color=$titlecolor>　■ </font><font color=$postfontcolorone>当前在线总数: <a href=whosonline.cgi><B>totleonlineall</B></a> 人</font><br>$todaypostlist~;

if ($dispborn ne "no") {
    &birthday;
    unless (($dispborn eq "auto") && ($birthdayuser eq "")) {
        $birthdayuser = "今天没有人过生日" if ($birthdayuser eq "");
        $birthdayoutput = qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=\$tablewidth bgcolor=\$tablebordercolor align=center><tr><td><table cellpadding=6 cellspacing=1 width=100%><tr><td bgcolor=\$titlecolor colspan=7 \$catbackpic><font color=\$titlefontcolor><B>-=> 今天过生日的注册用户 （共 $borncount 人）</b>     [<a href="calendar.cgi" target=_blank>论坛日历</a>]</td></tr><tr><td bgcolor=\$forumcolorone align=center width=26><img src=$imagesurl/images/\$skin/born.gif alt="今天过生日人员名单" width=16></td><td bgcolor=\$forumcolortwo colspan=6 width=*><img src=$imagesurl/images/none.gif width=400 height=0><br>　<font color=\$forumfontcolor>$birthdayuser</td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><img src=$imagesurl/images/none.gif height=5><br>~;
    }
}

require "${lbdir}data/forumcate.pl" if (($cancmodoutput ne "no") && (-e "${lbdir}data/forumcate.pl"));

open(FILE, ">${lbdir}cache/forumcache-$skin.pl");
print FILE qq~\$lvisit="$lvisit";\n~;
for ($i = 0; $i <= $#rearrangedforums; $i++) {
    $rearrangedforums[$i] =~ s/\\/\\\\/isg;
    $rearrangedforums[$i] =~ s/~/\\\~/isg;
    $rearrangedforums[$i] =~ s/\$/\\\$/isg;
    $rearrangedforums[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$rearrangedforums[$i] = qq~$rearrangedforums[$i]~;\n) if ($rearrangedforums[$i] ne "");
    $rearrangedforums[$i] =~ s/\\\~/~/isg;
    $rearrangedforums[$i] =~ s/\\\$/\$/isg;
    $rearrangedforums[$i] =~ s/\\\@/\@/isg;
    $rearrangedforums[$i] =~ s/\\\\/\\/isg;
}
for ($i = 0; $i <= $#threadadds; $i++) {
    print FILE qq~\$threadadds[$i] = "$threadadds[$i]";\n~ if ($threadadds[$i] ne "");
}
for ($i = 0; $i <= $#postadds; $i++) {
    print FILE qq~\$postadds[$i] = "$postadds[$i]";\n~ if ($postadds[$i] ne "");
}
for ($i = 0; $i <= $#todayforumpostadds; $i++) {
    print FILE qq~\$todayforumpostadds[$i] = "$todayforumpostadds[$i]";\n~ if ($todayforumpostadds[$i] ne "");
}
for ($i = 0; $i <= $#lastposttime; $i++) {
    $lastposttime[$i] =~ s/\\/\\\\/isg;
    $lastposttime[$i] =~ s/~/\\\~/isg;
    $lastposttime[$i] =~ s/\$/\\\$/isg;
    $lastposttime[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$lastposttime[$i] = qq~$lastposttime[$i]~;\n) if ($lastposttime[$i] ne "");
    $lastposttime[$i] =~ s/\\\~/~/isg;
    $lastposttime[$i] =~ s/\\\$/\$/isg;
    $lastposttime[$i] =~ s/\\\@/\@/isg;
    $lastposttime[$i] =~ s/\\\\/\\/isg;
}
for ($i = 0; $i <= $#lastposter; $i++) {
    $lastposter[$i] =~ s/~/\\\~/isg;
    $lastposter[$i] =~ s/\$/\\\$/isg;
    $lastposter[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$lastposter[$i] = qq~$lastposter[$i]~;\n) if ($lastposter[$i] ne "");
    $lastposter[$i] =~ s/\\\~/~/isg;
    $lastposter[$i] =~ s/\\\$/\$/isg;
    $lastposter[$i] =~ s/\\\@/\@/isg;
}
for ($i = 0; $i <= $#cforums; $i++) {
    $cforums[$i] =~ s/\\/\\\\/isg;
    $cforums[$i] =~ s/~/\\\~/isg;
    $cforums[$i] =~ s/\$/\\\$/isg;
    $cforums[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$forums[$i] = qq~$cforums[$i]~;\n) if ($cforums[$i] ne "");
    $cforums[$i] =~ s/\\\~/~/isg;
    $cforums[$i] =~ s/\\\$/\$/isg;
    $cforums[$i] =~ s/\\\@/\@/isg;
    $cforums[$i] =~ s/\\\\/\\/isg;
}
for ($i = 0; $i <= $#modout; $i++) {
    $modout[$i] =~ s/~/\\\~/isg;
    $modout[$i] =~ s/\$/\\\$/isg;
    $modout[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$modout[$i] = qq~$modout[$i]~;\n) if ($modout[$i] ne "");
    $modout[$i] =~ s/\\\~/~/isg;
    $modout[$i] =~ s/\\\$/\$/isg;
    $modout[$i] =~ s/\\\@/\@/isg;
}
for ($i = 0; $i <= $#cmodoutput; $i++) {
    $cmodoutput[$i] =~ s/~/\\\~/isg;
    $cmodoutput[$i] =~ s/\$/\\\$/isg;
    $cmodoutput[$i] =~ s/\@/\\\@/isg;
    print FILE qq(\$cmodoutput[$i] = qq~$cmodoutput[$i]~;\n) if ($cmodoutput[$i] ne "");
    $cmodoutput[$i] =~ s/\\\~/~/isg;
    $cmodoutput[$i] =~ s/\\\$/\$/isg;
    $cmodoutput[$i] =~ s/\\\@/\@/isg;
}
$todaypostlist =~ s/\\/\\\\/isg;
$todaypostlist =~ s/~/\\\~/isg;
$todaypostlist =~ s/\$/\\\$/isg;
$todaypostlist =~ s/\@/\\\@/isg;
$todaypostlist =~ s/\\\$/\$/isg;
print FILE qq(\$todaypostlist  = qq~$todaypostlist~;\n);
$todaypostlist =~ s/\$/\\\$/isg;
$todaypostlist =~ s/\\\~/~/isg;
$todaypostlist =~ s/\\\$/\$/isg;
$todaypostlist =~ s/\\\@/\@/isg;
$todaypostlist =~ s/\\\\/\\/isg;

$birthdayoutput =~ s/\\/\\\\/isg;
$birthdayoutput =~ s/~/\\\~/isg;
$birthdayoutput =~ s/\$/\\\$/isg;
$birthdayoutput =~ s/\@/\\\@/isg;
$birthdayoutput =~ s/\\\$/\$/isg;
print FILE qq(\$birthdayoutput = qq~$birthdayoutput~;\n);
$birthdayoutput =~ s/\$/\\\$/isg;
$birthdayoutput =~ s/\\\~/~/isg;
$birthdayoutput =~ s/\\\$/\$/isg;
$birthdayoutput =~ s/\\\@/\@/isg;
$birthdayoutput =~ s/\\\\/\\/isg;
print FILE "1;\n";
close(FILE);
$birthdayoutput =~ s/\$skin/$skin/isg;
$birthdayoutput =~ s/\$tablewidth/$tablewidth/isg;
$birthdayoutput =~ s/\$tablebordercolor/$tablebordercolor/isg;
$birthdayoutput =~ s/\$titlecolor/$titlecolor/isg;
$birthdayoutput =~ s/\$catbackpic/$catbackpic/isg;
$birthdayoutput =~ s/\$titlefontcolor/$titlefontcolor/isg;
$birthdayoutput =~ s/\$forumcolorone/$forumcolorone/isg;
$birthdayoutput =~ s/\$forumcolortwo/$forumcolortwo/isg;
$birthdayoutput =~ s/\$forumfontcolor/$forumfontcolor/isg;

$todaypostlist =~ s/\$titlecolor/$titlecolor/isg;
$todaypostlist =~ s/\$postfontcolortwo/$postfontcolortwo/isg;
$todaypostlist =~ s/\$fonthighlight/$fonthighlight/isg;
$todaypostlist =~ s/\$titlecolor/$titlecolor/isg;
$todaypostlist =~ s/\$postfontcolorone/$postfontcolorone/isg;

unlink("${lbdir}cache/forumcache-$skin.pl.lock");

sub birthday {
    $birthdayuser = "";
    $borncount = 0;
    my $filedate = "";
    my $nowtime = &shortdate($currenttime + $timeadd);
    ($nowy, $nowm, $nowd) = split(/\//, $nowtime);
    my $filetoopen = "${lbdir}data/birthdaytoday.cgi";
    if (-e $filetoopen) {
        open(BDILE, "$filetoopen");
        @birthdaytoday = <BDILE>;
        close(BDILE);
        chomp @birthdaytoday;
        $filedate = $birthdaytoday[0];
        chomp $filedate;
        $filedate =~ s/^#//isg;
    }
    if ($filedate ne $nowtime) {
        require "dotodaybirthday.pl";
    }
    else {
        $birthdayuser = $birthdaytoday[1];
        $borncount = $birthdaytoday[2];
    }

}
1;
