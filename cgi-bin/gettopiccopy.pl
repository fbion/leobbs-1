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

$tempaccess = "forumsallowed" . "$inforum";
$testentry = $query->cookie("$tempaccess");
if ((($testentry eq $forumpass) && ($testentry ne "")) || ($allowedentry{$inforum} eq "yes") || ($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes")) {$allowed = "yes";}
if (($privateforum eq "yes") && ($allowed ne "yes")) {&error("复制帖子&对不起，您不允许复制保密论坛的帖子！");}
&error("普通错误&客人不能查看贴子内容，请注册或登录后再试") if (($guestregistered eq "off") && ($inmembername eq "客人"));
&error("普通错误&客人不能查看贴子内容，请注册或登录后再试") if ($waterwhenguest eq "yes" && $inmembername eq "客人");

open(FILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
my @threads = <FILE>;
close(FILE);
$posttoget = $inpostno - 1;
($membername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post) = split(/\t/, $threads[$posttoget]);
$topictitle =~ s/^＊＃！＆＊//;

if ($addtopictime eq "yes") {
    my $topictime = &dispdate($postdate + ($timedifferencevalue * 3600) + ($timezone * 3600));
    $topictitle = "[$topictime] $topictitle";
}

$post =~ s/\<p\>/\n\n/ig;
$post =~ s/\<br\>/\n/ig;

if (($post =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/sg) || ($post =~ /LBSALE\[(.*?)\]LBSALE/sg)) {
    unless ((lc($inmembername) eq lc($membername)) || ($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($inmembmod eq "yes") || ($myrating >= $1)) {
        &error("复制帖子&对不起，您不允许复制保密帖子！");
    }
    else {
        $post =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//isg;
        $post =~ s/LBSALE\[(.*?)\]LBSALE//isg;
    }
}

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
        &whosonline("$inmembername\t$forumname\tnone\t复制帖子<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
    }
    else {
        &whosonline("$inmembername\t$forumname(密)\tnone\t复制保密帖子\t");
    }
}

&getmember($membername, "no");
&error("复制帖子&对不起，您不允许复制被屏蔽的帖子！") if (($membercode eq "masked") && ($mymembercode ne "ad") && ($mymembercode ne 'smo') && ($inmembmod ne "yes"));

$post =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
$post =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
$post =~ s/\[hide\](.+?)\[\/hide\]//isg;
$post =~ s/\[watermark\](.+?)\[\/watermark\]/\n\(水印部分不能复制\)\n/isg;
$post =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[加密连结\]/isg if ($usecurl ne "no");
$postdate = $postdate + ($timedifferencevalue + $timezone) * 3600;
$postdate = &dateformat("$postdate");
$rawpost = $post;
$rawpost =~ s/\[ALIPAYE\](.*)\[ALIPAYE\]//isg;
$rawpost =~ s/\[hide\](.*)\[\/hide\]//isg;
$rawpost =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
$rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
$rawpost =~ s/\[DISABLELBCODE\]//isg;
$rawpost =~ s/\[ADMINOPE=(.+?)\]//isg;
if ($rawpost =~ /\[POSTISDELETE=(.+?)\]/) {
    if ($1 ne " ") {$presult = "屏蔽理由：$1";}
    else {$presult = "<BR>";}
    $rawpost = "此帖子内容已经被单独屏蔽！$presult";
}

&mischeader("复制帖子");

$temppost = qq~-=-=-=-=-=>\n$rawpost\n-=-=-=-=-=>~;
$output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=4 cellspacing=1 width=100%><tr><td bgcolor=$titlecolor $catbackpic colspan=2>
<form action="$thisprog" method=post><font color=$titlefontcolor>主题： $topictitle</td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>复制帖子</b><p></font></td><td bgcolor=$miscbackone>&nbsp;&nbsp;<textarea cols=90 rows=12 wrap="soft" name="inpost">$temppost</textarea><BR><BR></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type="button" value="高亮显示文字" onClick="this.form.inpost.focus();this.form.inpost.select();">　　<input type="button" value="复制到剪贴板" name="cmdCopy" onClick="copy(this.form.inpost)"></center></td></tr></td></table></table>
<SCRIPT>valignend()</SCRIPT>
    ~;
1;
