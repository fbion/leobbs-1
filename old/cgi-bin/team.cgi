#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

BEGIN {
    $startingtime = (times)[0] + (times)[1];
    foreach ($0, $ENV{'PATH_TRANSLATED'}, $ENV{'SCRIPT_FILENAME'}) {
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g;
        $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC, $LBPATH);
    }
}

use strict;
use warnings;
use diagnostics;
use diagnostics;

use LBCGI;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/membertitles.cgi";
require "bbs.lib.pl";

$|++;

$maxshowmembers = $maxtopics;

$thisprog = "team.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") {$cookiepath = $mycookiepath;}
elsif ($COOKIE_USED eq 1) {$cookiepath = "";}
else {
    $boardurltemp = $boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
    #    $cookiepath =~ tr/A-Z/a-z/;
}
$in_member_name = $query->cookie("amembernamecookie");
$in_password = $query->cookie("apasswordcookie");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&ipbanned; #封杀一些 ip
$inpage = $query->param("page");
if ($inpage eq "") {$inpage = 1;}
$in_password =~ s/\t//isg;

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

if ($in_member_name eq "" || $in_member_name eq "客人") {
    $in_member_name = "客人";
}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}
$inmembercode = $member_code;
if ($infosopen == 2) {
    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
    &error("查看管理团队&客人无权查看管理团队！") if ($in_member_name eq "客人");
    if ($userregistered eq "no") {&error("查看管理团队&你还没注册呢！");}
    &error("查看管理团队&论坛管理团队只有坛主和版主可以查看！") if (($member_code ne "ad") && ($member_code ne 'smo') && ($member_code ne 'cmo') && ($member_code ne "mo") && ($member_code ne "amo"));
}
elsif ($infosopen == 1) {
    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
    &error("查看管理团队&客人无权查看管理团队！") if ($in_member_name eq "客人");
    if ($userregistered eq "no") {&error("查看管理团队&你还没注册呢！");}
}
elsif ($infosopen == 3) {
    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
    &error("查看管理团队&客人无权查看管理团队！") if ($in_member_name eq "客人");
    if ($userregistered eq "no") {&error("查看管理团队&你还没注册呢！");}
    &error("查看管理团队&论坛管理团队只有坛主可以查看！") if ($member_code ne "ad");
}

$defaultwidth = "width=$defaultwidth" if ($defaultwidth ne "");
$defaultheight = "height=$defaultheight" if ($defaultheight ne "");

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    &whosonline("$in_member_name\t管理团队\tboth\t查看管理人员名单\t");
}

open(FILE, "$lbdir/data/lbmember.cgi");
sysread(FILE, my $memberdata, (stat(FILE))[7]);
close(FILE);
$memberdata =~ s/\r//isg;
@memberdata = split(/\n/, $memberdata);
foreach $line (@memberdata) {
    @tmpuserdetail = split(/\t/, $line);
    chomp @tmpuserdetail;
    if ($tmpuserdetail[1] eq ad) {
        push(@teamlist, "1\t$tmpuserdetail[0]");}
    elsif ($tmpuserdetail[1] eq smo) {
        push(@teamlist, "2\t$tmpuserdetail[0]");}
    elsif ($tmpuserdetail[1] eq "cmo") {
        push(@teamlist, "3\t$tmpuserdetail[0]");}
    elsif ($tmpuserdetail[1] eq "mo") {
        push(@teamlist, "4\t$tmpuserdetail[0]");}
    elsif ($tmpuserdetail[1] eq "amo") {
        push(@teamlist, "4\t$tmpuserdetail[0]");}
}
## calculate the page's number
$totalpages = @teamlist / $maxshowmembers;
($pagenumbers, $decimal) = split(/\./, $totalpages);
if ($decimal > 0) {
    $pagenumbers++;}
$page = 1;
$pagedigit = 0;
$pagelinks = qq~Page: ~;
while ($pagenumbers > $pagedigit) {
    # start while
    $pagedigit++;
    if ($inpage ne $page) {
        $pagelinks .= qq~[<a href="$thisprog?page=$page">$pagedigit</a>] ~;}
    else {
        $pagelinks .= qq~[$pagedigit] ~;}
    $page++;
} # end while
if ($totalpages <= 1) {
    $pagelinks = qq~本列表只有一页~;}

## calculate the number of the start and final member, those to be displayed on this page 
$startmember = ($inpage - 1) * $maxshowmembers;
$endmember = $startmember + $maxshowmembers - 1;
if ($endmember > (@teamlist - 1)) {
    $endtopic = @teamlist - 1;}

## Mitglieder-Details auslesen und die Mitglieder Seitenweise darstellen
@teamlist = sort alphabetically (@teamlist);
@teamlist = sort numerically (@teamlist);
foreach $teammember (@teamlist[$startmember ... $endmember]) {
    ($trash, $teammemberfile) = split(/\t/, $teammember);
    chomp $teammemberfile;
    $teammemberfile =~ s/ /_/g;
    $teammemberfile =~ tr/A-Z/a-z/;
    my $namenumber = &getnamenumber($teammemberfile);
    &checkmemfile($teammemberfile, $namenumber);
    $memopenfile = "${lbdir}$memdir/$namenumber/$teammemberfile.cgi";

    open(FILE, "$memopenfile");
    $memberline = <FILE>;
    close(FILE);
    chomp $memberline;
    @userdetail = split(/\t/, $memberline);
    chomp @userdetail;
    #	 $userdetail[0] =~ tr/A-Z/a-z/;
    next if (($userdetail[3] ne "ad") && ($userdetail[3] ne "smo") && ($userdetail[3] ne "cmo") && ($userdetail[3] ne "mo") && ($userdetail[3] ne "amo"));
    ## Definiere die Hintergrund- und Textfarbe f黵 die Zeilen
    if ($lastcolor eq $postcolortwo) {
        $color = $postcolorone;
        $fontcolor = $postfontcolorone;
    }
    else {
        $color = $postcolortwo;
        $fontcolor = $postfontcolortwo;
    }

    ## Registrierdatum
    $userdetail[13] = $userdetail[13] + ($userdetail[16] + $timezone) * 3600;
    if ($userdetail[13]) {$userdetail[13] = &longdate($userdetail[13])}
    else {$userdetail[13] = "未知";}

    $lastgone = $userdetail[26];
    $lastgone = $joineddate if ($lastgone eq "");
    $today = time - $lastgone;
    $novisitdate = int($today / (3600 * 24));

    ## Setze Avatar-Grafiken
    if (($avatars eq "on") && ($userdetail[18]) && ($userdetail[18] ne "noavatar")) {
        $useravatar = qq~<br><img src="$imagesurl/avatars/$userdetail[18].gif" border=0 $defaultwidth $defaultheight>~;}
    else {
        $useravatar = "";}
    ($iiii, $jjjj) = split(/\|/, $userdetail[4]);
    $kkkk = $userdetail[31];
    $jifen = $userdetail[45];

    if ($jifen eq "") {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $jifen = $anzahl1 * $ttojf + $anzahl2 * $rtojf - $postdel * $deltojf;
    }

    if ($jifen >= $mpostmarkmax) {
        $mtitle = $mtitlemax;
        $membergraphic = $mgraphicmax;
    }
    elsif ($jifen >= $mpostmark19) {
        $mtitle = $mtitle19;
        $membergraphic = $mgraphic19;
    }
    elsif ($jifen >= $mpostmark18) {
        $mtitle = $mtitle18;
        $membergraphic = $mgraphic18;
    }
    elsif ($jifen >= $mpostmark17) {
        $mtitle = $mtitle17;
        $membergraphic = $mgraphic17;
    }
    elsif ($jifen >= $mpostmark16) {
        $mtitle = $mtitle16;
        $membergraphic = $mgraphic16;
    }
    elsif ($jifen >= $mpostmark15) {
        $mtitle = $mtitle15;
        $membergraphic = $mgraphic15;
    }
    elsif ($jifen >= $mpostmark14) {
        $mtitle = $mtitle14;
        $membergraphic = $mgraphic14;
    }
    elsif ($jifen >= $mpostmark13) {
        $mtitle = $mtitle13;
        $membergraphic = $mgraphic13;
    }
    elsif ($jifen >= $mpostmark12) {
        $mtitle = $mtitle12;
        $membergraphic = $mgraphic12;
    }
    elsif ($jifen >= $mpostmark11) {
        $mtitle = $mtitle11;
        $membergraphic = $mgraphic11;
    }
    elsif ($jifen >= $mpostmark10) {
        $mtitle = $mtitle10;
        $membergraphic = $mgraphic10;
    }
    elsif ($jifen >= $mpostmark9) {
        $mtitle = $mtitle9;
        $membergraphic = $mgraphic9;
    }
    elsif ($jifen >= $mpostmark8) {
        $mtitle = $mtitle8;
        $membergraphic = $mgraphic8;
    }
    elsif ($jifen >= $mpostmark7) {
        $mtitle = $mtitle7;
        $membergraphic = $mgraphic7;
    }
    elsif ($jifen >= $mpostmark6) {
        $mtitle = $mtitle6;
        $membergraphic = $mgraphic6;
    }
    elsif ($jifen >= $mpostmark5) {
        $mtitle = $mtitle5;
        $membergraphic = $mgraphic5;
    }
    elsif ($jifen >= $mpostmark4) {
        $mtitle = $mtitle4;
        $membergraphic = $mgraphic4;
    }
    elsif ($jifen >= $mpostmark3) {
        $mtitle = $mtitle3;
        $membergraphic = $mgraphic3;
    }
    elsif ($jifen >= $mpostmark2) {
        $mtitle = $mtitle2;
        $membergraphic = $mgraphic2;
    }
    elsif ($jifen >= $mpostmark1) {
        $mtitle = $mtitle1;
        $membergraphic = $mgraphic1;
    }
    else {
        $mtitle = $mtitle0;
        $mgraphic0 = "none.gif" if ($mgraphic0 eq "");
        $membergraphic = $mgraphic0;
    } #显示默认等级
    if ($membergraphic) {
        $membergraphic = qq~<img src="$imagesurl/images/$membergraphic" border="0" width=100 height=9>~;}
    if ($avatars eq "on") {
        if (($userdetail[22]) && ($userdetail[23]) && ($userdetail[24])) {
            #自定义头像存在
            $userdetail[22] =~ s/\$imagesurl/${imagesurl}/o;
            if (($userdetail[22] =~ /\.swf$/i) && ($flashavatar eq "yes")) {
                $userdetail[22] = uri_escape($userdetail[22]);
                $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$userdetail[23] HEIGHT=$userdetail[24]><PARAM NAME=MOVIE VALUE=$userdetail[22]><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$userdetail[22] WIDTH=$userdetail[23] HEIGHT=$userdetail[24] PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
            }
            else {
                $userdetail[22] = uri_escape($userdetail[22]);
                $useravatar = qq(<br>&nbsp; <img src=$userdetail[22] border=0 width=$userdetail[23] height=$userdetail[24]>);
            }
        }
        elsif (($userdetail[18] ne "noavatar") && ($userdetail[18])) {
            $userdetail[18] = uri_escape($userdetail[18]);
            $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$userdetail[18].gif" border=0 $defaultwidth $defaultheight>);
        }
        else {undef $useravatar;}
    }

    ## Setze Mitgliedsstatus
    if ($userdetail[3] eq "ad") {
        $posterfontcolor = "$adminnamecolor";
        $membername = qq~$userdetail[0] <img src="$imagesurl/images/teamad.gif" border=0 alt=此人为坛主 width=16 height=14>~;
        $membergraphic = "<img src=\"$imagesurl/images/$admingraphic\" border=\"0\" width=100 height=9>" if ($admingraphic ne "");
        $mtitle = $adtitle if ($adtitle ne "");
        if (($userdetail[2] eq "member") || ($userdetail[2] eq "Member") || ($userdetail[2] eq "")) {
            $membertitle = qq~<font face="$font" color=$fontcolor>论坛坛主</font>~;}
        else {
            $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~;}
    }
    elsif ($userdetail[3] eq "mo") {
        $posterfontcolor = "$teamnamecolor";
        $membername = qq~$userdetail[0] <img src="$imagesurl/images/teammo.gif" border=0 alt=此人为版主 width=16 height=14>~;
        $membergraphic = "<img src=\"$imagesurl/images/$modgraphic\" border=\"0\" width=100 height=9>" if ($modgraphic ne "");
        $mtitle = $motitle if ($motitle ne "");
        if (($userdetail[2] eq "") || ($userdetail[2] eq "Member") || ($userdetail[2] eq "member")) {
            $membertitle = qq~<font face="$font" color=$fontcolor>论坛版主</font>~;}
        else {
            $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~;}
    }
    elsif ($userdetail[3] eq "amo") {
        $posterfontcolor = "$amonamecolor";
        $membername = qq~$userdetail[0] <img src="$imagesurl/images/teamamo.gif" border=0 alt=此人为副版主 width=16 height=14>~;
        $membergraphic = "<img src=\"$imagesurl/images/$amodgraphic\" border=\"0\" width=100 height=9>" if ($amodgraphic ne "");
        $mtitle = $amotitle if ($amotitle ne "");
        if (($userdetail[2] eq "") || ($userdetail[2] eq "Member") || ($userdetail[2] eq "member")) {
            $membertitle = qq~<font face="$font" color=$fontcolor>论坛副版主</font>~;}
        else {
            $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~;}
    }
    elsif ($userdetail[3] eq "cmo") {
        $posterfontcolor = "$cmonamecolor";
        $membername = qq~$userdetail[0] <img src="$imagesurl/images/teamcmo.gif" border=0 alt=此人为分类区版主 width=16 height=14>~;
        $membergraphic = "<img src=\"$imagesurl/images/$cmodgraphic\" border=\"0\" width=100 height=9>" if ($cmodgraphic ne "");
        $mtitle = $cmotitle if ($cmotitle ne "");
        if (($userdetail[2] eq "") || ($userdetail[2] eq "Member") || ($userdetail[2] eq "member")) {
            $membertitle = qq~<font face="$font" color=$fontcolor>分类区版主</font>~;}
        else {
            $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~;}
    }
    elsif ($userdetail[3] eq "smo") {
        $posterfontcolor = "$smonamecolor";
        $membername = qq~$userdetail[0] <img src="$imagesurl/images/teamsmo.gif" border=0 alt=此人为总版主 width=16 height=14>~;
        $membergraphic = "<img src=\"$imagesurl/images/$smodgraphic\" border=\"0\" width=100 height=9>" if ($smodgraphic ne "");
        $mtitle = $smotitle if ($smotitle ne "");
        if (($userdetail[2] eq "") || ($userdetail[2] eq "Member") || ($userdetail[2] eq "member")) {
            $membertitle = qq~<font face="$font" color=$fontcolor>总版主</font>~;}
        else {
            $membertitle = qq~<font face="$font" color=$fontcolor>$userdetail[2]</font>~;}
    }
    ## Setze letzte Beitrags-Details
    ($postdate, $posturl, $posttopic) = split(/\%%%/, $userdetail[14]);
    if ($postdate ne "没有发表过") {
        $postdate = $postdate + ($userdetail[16] * 3600) + ($timezone * 3600);
        $lastpostdate = &longdate("$postdate");
        $lastposttime = &shorttime("$postdate");

        $posttopic =~ s/^＊＃！＆＊//;

        $lastpostdetails = qq~<a href="$posturl">$posttopic</a> ($lastpostdate $lastposttime)~;
    }
    else {$lastpostdetails = qq~从未发言过~;}
    if ($posturl eq "" && $posttopic eq "" && $postdate ne "没有发表过") {$lastpostdetails = qq~是发在保密论坛的哟，不给看~;}

    my $membernametemp = "\_$userdetail[0]\_";
    if ($onlineuserlist =~ /$membernametemp/i) {
        $onlineinfo = "该用户目前在线";
        $onlinepic = "online1.gif";
    }
    else {
        $onlineinfo = "该用户目前不在线";
        $onlinepic = "offline1.gif";
    }
    if (($inmembercode eq "ad") && ($onlineuserlisthidden =~ /$membernametemp/i)) {
        $onlineinfo = "该用户目前处于隐身状态";
        $onlinepic = "onlinehidden.gif";
    }
    $online = qq~<IMG SRC=$imagesurl/images/$onlinepic width=15 alt=$onlineinfo>~;

    ## Mehr Details
    $userdetail[5] = &encodeemail($userdetail[5]);
    $userdetail[6] = "no" if ($dispmememail eq "no");
    if ($userdetail[6] eq "no") {$email = "保密";}
    elsif ($userdetail[6] eq "msn") {$email = qq~<img src=$imagesurl/images/msn.gif border=0 width=16 align=absmiddle> <a href="mailto:$userdetail[5]">$userdetail[5]</a>~;}
    elsif ($userdetail[6] eq "popo") {$email = qq~<img src=$imagesurl/images/popo.gif border=0 width=16 align=absmiddle> <a href="mailto:$userdetail[5]">$userdetail[5]</a>~;}
    else {$email = qq~<a href="mailto:$userdetail[5]">$userdetail[5]</a>~;}

    if ($userdetail[8] eq "" || $userdetail[8] eq "http://") {
        $homepage = "没有";}
    else {
        $homepage = qq~<a href="$userdetail[8]" target="_blank">$userdetail[8]</a>~;}
    if ($userdetail[9] eq "") {
        $oicqnumber = "没有";}
    else {
        $oicqnumber = $userdetail[9];}
    if ($userdetail[10] eq "") {
        $icqnumber = "没有";}
    else {
        $icqnumber = $userdetail[10];}
    if ($userdetail[39] eq "") {
        $jhmp = "无门无派";}
    else {
        $jhmp = $userdetail[39];}

    ## Erstelle Liste der moderierten Foren des Mitglieds
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    open(FILE, "$filetoopen");
    @forumsdata = <FILE>;
    close(FILE);
    undef @moderatedforums;
    $userdetail[0] =~ tr/A-Z/a-z/;
    foreach $forum (@forumsdata) {
        @forumdetail = split(/\t/, $forum);
        chomp @forumdetail;
        if ($forumdetail[1] =~ /childforum-[0-9]+/) {
            $tempforumno = $forumdetail[1];
            $tempforumno =~ s/childforum-//;
            if ($subforumname[$tempforumno] eq "") {
                $filetoopen = "${lbdir}forum$tempforumno/foruminfo.cgi";
                open(FILE, "$filetoopen");
                $forums = <FILE>;
                close(FILE);
                ($subforumno[$tempforumno], $subforumcat[$tempforumno], undef, $subforumname[$tempforumno], undef) = split(/\t/, $forums);
                $subforumname = qq( > <a href="forums.cgi?forum=$subforumno[$tempforumno]">$subforumname[$tempforumno]</a>);
                $forumdetail[1] = $subforumcat[$tempforumno];
            }
            else {
                $subforumname = qq( > <a href="forums.cgi?forum=$subforumno[$tempforumno]">$subforumname[$tempforumno]</a>);
                $forumdetail[1] = $subforumcat[$tempforumno];
            }
        }
        else {
            undef $subforumname;
        }
        $forumdetail[5] =~ s/\, /\,/gi;
        $forumdetail[5] =~ s/ \,/\,/gi;
        $forumdetail[5] =~ tr/A-Z/a-z/;
        @forummodnames = split(/\,/, $forumdetail[5]);
        foreach $name (@forummodnames) {
            chomp $name;
            if (lc($name) eq lc($userdetail[0])) {
                push(@moderatedforums, "<a href=\"forums.cgi?forum=$forumdetail[0]\">$forumdetail[3]</a> ($forumdetail[1]$subforumname)<br>");
            }
        }
    }
    if (!@moderatedforums) {
        @moderatedforums = "$userdetail[0] 没有主持任何版块";}
    @moderatedforums = sort alphabetically (@moderatedforums);

    ## Schreibe HTML in eine Variable
    $teamguts .= qq~
        <!--Begin Profile for $userdetail[0]-->
        <tr bgcolor=$color>
        <td valign=top>
	<table style="filter:glow(color=$titlecolor,strength=2)">$online　<font face="$posternamefont" color="$posterfontcolor"><b>$membername</b></font>
	</table>
        头衔：$membertitle
        <br>$useravatar
        <br>$membergraphic
        <br>级别：<a href="lookinfo.cgi?action=style" target="_blank">$mtitle</a><br>门派: $jhmp</td>
        <td valign=top><table cellspacing=0 cellpadding=0 border=0 width=100%>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>注册日期：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor $userdetail[7]>$userdetail[13]</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>最后发言：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$lastpostdetails</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>失踪天数：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$novisitdate 天</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>电子邮件：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$email</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>主页：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$homepage</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>OICQ 号码：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$oicqnumber</font></td>
        </tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>ICQ 号码：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>$icqnumber</font></td>
        </tr>
        <tr><td colspan=2><font face="$font">&nbsp;</font></td></tr>
        <tr>
        <td width=25% valign=top><font face="$font" color=$fontcolor>主持板块：</font></td>
        <td width=75% valign=top><font face="$font" color=$fontcolor>@moderatedforums</font></td>
        </tr>
        </table></td>
        </tr>~;

    @moderatedforums = "";
    $lastcolor = $color;
    undef $membertitle;
    undef $icqnumber;
    undef $oicqnumber;
    undef $homepage;
    undef $email;
    undef $lastpostdetails;
    undef $membername;
    undef $jhmp;
    undef $useravatar;
    undef $membergraphic;
}

&title;

$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以查看到本站所有管理人员的列表及详细信息</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$board_name</a> → <a href="team.cgi">管理团队</a> → 查看列表<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$titlecolor>
<td width=25% align=center $catbackpic><font face="$font" color=$titlefontcolor><b>管 理 人 员</b></td>
<td width=75% align=center $catbackpic><font face="$font" color=$titlefontcolor><b>详 细 信 息</b></td>
</tr>
$teamguts
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<p>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr>
<td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr bgcolor=$menubackground>
<td align=center><font face=宋体 color=$fontcolormisc>$pagelinks</font></td>
</tr>
</table></td>
</tr>
</table>
~;

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&output("$board_name - 管理团队", \$output);
exit;