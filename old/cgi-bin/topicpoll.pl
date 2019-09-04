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
$maxpollitem = 5 if ($maxpollitem < 5);
$maxpollitem = 50 if ($maxpollitem > 50);
$showsignature = "yes$maxpollitem" if ($showsignature eq "yes");
if ($showsignature =~ /^yes[0-9]+$/) {$polltype = "checkbox";}
else {$polltype = "radio";}

$posticon =~ s/<br><br>/<BR>/isg;
$posticon =~ s/<br>/\t/ig;
my @temppoll = split(/\t/, $posticon);
if ($#temppoll >= 1) {
    $maxpolllength = 0;
    ($poll[1], $poll[2], $poll[3], $poll[4], $poll[5], $poll[6], $poll[7], $poll[8], $poll[9], $poll[10], $poll[11], $poll[12], $poll[13], $poll[14], $poll[15], $poll[16], $poll[17], $poll[18], $poll[19], $poll[20], $poll[21], $poll[22], $poll[23], $poll[24], $poll[25], $poll[26], $poll[27], $poll[28], $poll[29], $poll[30], $poll[31], $poll[32], $poll[33], $poll[34], $poll[35], $poll[36], $poll[37], $poll[38], $poll[39], $poll[40], $poll[41], $poll[42], $poll[43], $poll[44], $poll[45], $poll[46], $poll[47], $poll[48], $poll[49], $poll[50]) = split(/\t/, $posticon);
    $j = 0;
    $pollinput = "";
    for ($i = 1; $i <= $maxpollitem; $i++) {
        if ($poll[$i] ne "") {
            $j++;
            $pollinput .= qq~<input type="$polltype" name="myChoice" value='$i'> $poll[$i]<br>~;
            $maxpolllength = length($poll[$i]) if (length($poll[$i]) > $maxpolllength);
        }
    }
    $maxpolllength = $maxpolllength * 7 + 10;
    $maxpolllength = 150 if ($maxpolllength < 150);
    $maxpolllength = 510 if ($maxpolllength > 510);
    if ($showsignature =~ /^yes[0-9]+$/) {
        $showsignature =~ s/^yes//;
        $maxcanpoll = qq~最多可投 $showsignature 项<br>~;
    }
    $pollform = qq~<script>
function submitonce(theform){
if (document.all||document.getElementById){
for (i=0;i<theform.length;i++){
var tempobj=theform.elements[i]
if(tempobj.type.toLowerCase()=="submit"||tempobj.type.toLowerCase()=="reset")
tempobj.disabled=true
}}}
</script>
<form action=poll.cgi method=post onSubmit="submitonce(this)">
<input type=hidden name=action value=poll><input type=hidden name=forum value=$in_forum><input type=hidden name=threadname value=$in_topic>
<table cellpadding=1 cellspacing=0 width=$maxpolllength bgcolor=$tablebordercolor><tr><td nowrap><table width=100% cellpadding=4 cellspacing=0 bgcolor="$postbackcolor">
<tr><td nowrap>$pollinput<tr><td align=center nowrap><HR size=1 width=85%>$maxcanpoll<input type=submit name=results value='参加投票'>
</td></form></tr></table></td></tr></table>
~;

    $showpoll = "";
    $pollnull = "";
    if (($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes")) {
        $adminview = 1;
        $maxpolllength = 550;
        $adminviewcolspan = 3;
    }
    else {
        $adminview = 0;
        $maxpolllength = 510;
        $adminviewcolspan = 2;
    }

    $poll = qq~ <table width=$maxpolllength>~;

    if (open(FILE, "${lbdir}forum$in_forum/$in_topic.poll.cgi")) {
        sysread(FILE, my $allpoll, (stat(FILE))[7]);
        close(FILE);
        $allpoll =~ s/\r//isg;
        @allpoll = split(/\n/, $allpoll);
        $size = @allpoll;
    }
    else {
        $size = 0;
        @allpoll = ();
    }
    if ($size > 0) {
        $size = 0;
        @thispoll = ('0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0');
        @pollname = ('', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');

        foreach (@allpoll) {
            $_ =~ s/[\a\f\n\e\0\r]//isg;
            next if ($_ eq "");
            my ($tmpinmembername, $tmpmyChoice) = split(/\t/, $_);
            $tmpinmembername =~ s/^＊！＃＆＊//isg;
            for ($i = 1; $i <= $j; $i++) {
                if ($i == $tmpmyChoice) {
                    $thispoll[$i]++;
                    if (($thispoll[$i] >= $TheHigest) && ($usehigest eq 'yes')) {$TheHigest = $thispoll[$i];}
                    $pollname[$i] = "$pollname[$i]$tmpinmembername\t";
                    $size++;
                }
            }
            $showpoll = "true" if (lc($tmpinmembername) eq lc($in_member_name));
        }

        if (($showsignature eq 'yes') || ($showsignature =~ /[0-9]+$/)) {$poll .= qq~ <tr><td colspan=$adminviewcolspan><HR size=1 width=100%></td></tr><tr><td colspan=$adminviewcolspan>目前总共有 <font color=$fonthighlight><B>$size</B></font> 张投票，结果如下：<HR size=1 width=100%><BR></td></tr>~;}
        else {$poll .= qq~ <tr><td colspan=$adminviewcolspan><HR size=1 width=100%></td></tr><tr><td colspan=$adminviewcolspan>目前共有 <font color=$fonthighlight><B>$size</B></font> 人参加投票，结果如下：<HR size=1 width=100%><BR></td></tr>~;}
        for ($i = 1; $i <= $j; $i++) {
            if ($poll[$i] ne "") {
                my $mypoll = int(($thispoll[$i] / $size) * 1000) / 10;
                my $width = int(($mypoll / 100) * 160);
                if ($adminview == 1) {
                    $adminviewpoll = qq~</td><td nowarp><select><option>投票人名单　</option><option>----------</option>~;
                    @pollmanname = split(/\t/, $pollname[$i]);
                    $pollmanname = @pollmanname;
                    foreach (@pollmanname) {$adminviewpoll .= qq~<option value="$_">$_ </option>~;}
                    $adminviewpoll .= qq~</select>~;
                    $adminviewpoll = "</td><td nowarp>[没有人投票]" if ($pollmanname eq 0);
                }
                else {$adminviewpoll = "";}
                my $ii = $i;
                $ii = $ii - 40 if ($ii > 40);
                $ii = $ii - 30 if ($ii > 30);
                $ii = $ii - 20 if ($ii > 20);
                $ii = $ii - 10 if ($ii > 10);
                if (($thispoll[$i] >= $TheHigest) && ($usehigest eq 'yes')) {
                    $XA = qq~<font color="$higestcolor" size="$higestsize"><b>~;
                    $XB = qq~</b></font>~;
                }
                else {$XA = $XB = "";}
                $poll .= qq~<tr><td nowarp>$XA$poll[$i]$XB　　　&nbsp;　　　</td><td nowarp> <img src=$imagesurl/images/bar$ii.gif width=$width height=10> <b>$thispoll[$i]</b> 票数 $mypoll%　$adminviewpoll</td></tr>\n~;
            }
        }
    }
    else {
        $poll .= qq~ <tr><td colspan=2><HR size=1 width=100%></td></tr><tr><td colspan=2>没有人参加此投票，选项列表如下：<HR size=1 width=100%><BR></td></tr>~;
        for ($i = 1; $i <= $j; $i++) {$poll .= qq~<tr><td colspan=2>$poll[$i] </td></tr>~;}
        $pollnull = "true";
    }
    $poll .= "</td></tr><tr><td colspan=$adminviewcolspan><HR size=1 width=100%></td></tr></table>";

    if (($threadstate eq "pollclosed") || ($showpoll eq "true") || ($in_member_name eq "客人")) {
        my $poll1 = "<font color=$fonthighlight>客人不能投票，请注册！</font>" if ($in_member_name eq "客人");
        $poll1 = "<font color=$fonthighlight>谢谢，你已经投过票了！</font>" if ($showpoll eq "true");
        $poll1 = "<font color=$fonthighlight>对不起，此投票已经关闭！</font>" if ($threadstate eq "pollclosed");
        $poll = "<br><br><font color=$fonthighlight>对不起，你必需先投票才可看结果！</font><br>" if (($PollHidden eq "yes") && ($in_member_name eq "客人"));
        $poll = "$poll$poll1";
    }
    else {
        if (($PollHidden eq "yes") && ($membername{$membername} ne $in_member_name) && ($mymembercode ne "ad") && ($mymembercode ne 'smo') && ($myinmembmod ne "yes")) {
            $poll = "<br><font color=$fonthighlight>对不起，你必需先投票才可看结果！</font>";
        }
        elsif ($pollnull eq "true") {$poll = "<BR><font color=$fonthighlight>目前暂时没有人投票！</font>";}
        $poll = "$pollform$poll";
    }
    if (($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes") || (($usereditpost ne "no") && (lc($in_member_name) eq lc($membername{$membername})))) {$editgraphic = qq~<a href=editpoll.cgi?action=edit&forum=$in_forum&topic=$in_topic title=编辑这个投票><img src=$imagesurl/images/edit.gif border=0 width=16 align=absmiddle>编辑</a>　~}
    else {$editgraphic = "";}
    $delgraphic = "";
    $posticon = "";
}
$poll = "" if ($postdelete eq "1");

if ($poll ne "") {
    $post = "$post<br><br>$poll";
    $poll = "";
}
1;
