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

if ($avatars eq "on") {
    if (($personalavatar) && ($personalwidth) && ($personalheight)) {
        #自定义头像存在
        $personalavatar =~ s/\$imagesurl/${imagesurl}/o;
        if (($personalavatar =~ /\.swf$/i) && ($flashavatar eq "yes")) {
            $personalavatar = uri_escape($personalavatar);
            $useravatar = qq(<br><OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>);
        }
        else {
            $personalavatar = uri_escape($personalavatar);
            $useravatar = qq(<br><a href=profile.cgi?action=modify title=编辑您的个人资料><img src=$personalavatar width=$personalwidth height=$personalheight border=1></a>);
        }
    }
    elsif (($useravatar ne "noavatar") && ($useravatar)) {
        $useravatar = uri_escape($useravatar);
        $useravatar = qq(<br><a href=profile.cgi?action=modify title=编辑您的个人资料><img src=$imagesurl/avatars/$useravatar.gif border=1></a>);
    }
    elsif (($oicqnumber) && ($oicqnumber =~ /[0-9]/)) {
        $useravatar = qq~<a href=profile.cgi?action=modify title="您的 QQ 秀形象"><img src=http://qqshow-user.tencent.com/$oicqnumber/11/00/ width=70 height=113 border=1></a>~;
    }
    else {$useravatar = qq(<br><a href=profile.cgi?action=modify title=编辑您的个人资料><img src=$imagesurl/avatars/noavatar.gif border=1></a>);}
}
else {$useravatar = qq(<br><a href=profile.cgi?action=modify title=编辑您的个人资料><img src=$imagesurl/avatars/noavatar.gif border=1></a>);}

open(MSGOUT, "${lbdir}$msgdir/out/${memberfilename}_out.cgi");
sysread(MSGOUT, my $totalmessagesout, (stat(MSGOUT))[7]);
close(MSGOUT);
$totalmessagesout =~ s/\r//isg;
my @allmessages = split(/\n/, $totalmessagesout);
$totalmessagesout = @allmessages;

if ($unread eq "0") {$inboximg = qq~<img src=$imagesurl/images/inboxnonew.gif width=17>~;}
else {$inboximg = qq~<img src=$imagesurl/images/inboxnew.gif width=17>~;}

require "${lbdir}data/cityinfo.cgi";
$mymoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

$mymoney = "<font title=$mymoney>>999999999</font>" if ($mymoney > 999999999);
$moneyname = "雷傲元" if ($moneyname eq "");

my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
unless ($mystatus eq "1" || $mystatus eq "-1" || $ebankdata eq "") {
    $mysaves = "<B>没开户</B>";
    $myloan = "<B>没贷款</B>";
}
else {
    if ($mystatus) {
        $mysaves = "<B>$mysaves</B> $moneyname";
        if ($myloan) {
            $myloan = "<B>$myloan</B> $moneyname";
        }
        else {
            $myloan = "<B>没贷款</B>";
        }
    }
    else {
        $mysaves = "<B>没开户</B>";
        $myloan = "<B>没贷款</B>";
    }
}

$modscard_link = qq~\n :: [ <span style=cursor:hand onClick="javascript:openScript('modscard.cgi',420,320)"><font color=$fonthighlight><B>版主签到</B></font></span> ]~ if ($member_code eq "ad" || $member_code eq "smo" || $member_code eq "cmo" || $member_code eq "mo" || $member_code eq "amo");

$mysaves = "<font title=$mysaves>>999999999</font>" if ($mysaves > 999999999);
$myloan = "<font title=$myloan>>999999999</font>" if ($myloan > 999999999);
$postdel = 0 if ($postdel eq "");

my $lasttimes = $lastgone + ($timedifferencevalue + $timezone) * 3600;
$lasttimes = &dateformat($lasttimes);

my $in_member_names = uri_escape($in_member_name);
if (($maxmsgno eq "") || ($member_code eq "ad") || ($member_code eq "smo") || ($member_code eq "cmo") || ($member_code eq "amo") || ($member_code eq "mo")) {$maxmsgno = qq~<B>没有限制</B>~;}
else {$maxmsgno = qq~<font color=$fonthighlight><B>$maxmsgno</B></font> 条~;}
my $myoutput = qq~<tr><td bgcolor=\$titlecolor colspan=4 \$catbackpic><font color=\$titlefontcolor><B>-=>  个人状态</B>  [ 来自：$trueipaddress，$fromwhere1 。系统：$osinfo，$browseinfo。最后访问时间：$lasttimes ]</td></tr>
<tr><td bgcolor=\$forumcolorone align=center width=18>$inboximg</td>
<td bgcolor=\$forumcolortwo width=130 align=center>$useravatar</td>
<td bgcolor=\$forumcolortwo width=*><img src=$imagesurl/images/none.gif width=340 height=1><BR>
<table cellpadding=6 cellspacing=0 width=100%>
<tr><td nowarp>
<font color=\$fontcolormisc>* <B>我的财产</B></font><BR><img src=$imagesurl/images/none.gif height=6><BR>
现金: <B>$mymoney</B> $moneyname<BR>
存款: $mysaves<BR>
贷款: $myloan
</td>
<td nowarp>
<font color=\$fontcolormisc>* <B>我的短消息</B></font><BR><img src=$imagesurl/images/none.gif height=6><BR>
[<a href=messanger.cgi?action=inbox target=_blank>收件箱</a>]: <B>totalmessageshtc</B><BR>
[<a href=messanger.cgi?action=outbox target=_blank>发件箱</a>]: <B>$totalmessagesout</B><BR>
条数限制: $maxmsgno<BR>
</td>
<td nowarp>
<font color=\$fontcolormisc>* <B>我的文章</B></font><BR><img src=$imagesurl/images/none.gif height=6><BR>
发表数: <B>$numberofposts</B><BR>
回复数: <B>$numberofreplys</B><BR>
被删数: <B>$postdel</B><BR>
</td></tr></table><img src=$imagesurl/images/none.gif height=9><BR><center>
[ <a href=fav.cgi?action=show&member=$in_member_names>我的收藏夹</a> ] :: [ <span style=cursor:hand onClick="javascript:openScript('recopr.cgi?action=post',420,320)">我被回复的主题</span> ] :: [ <span style=cursor:hand onClick="javascript:openScript('recopr.cgi?action=reply',420,320)">我参与的主题</span> ] :: [ <span style=cursor:hand onClick="javascript:openScript('recopr.cgi?action=new',420,320)">论坛最新帖</span> ]$modscard_link</center>
</td>~;
if ($forumcached eq "yes") {
    open(FILE, ">${lbdir}cache/myinfo/$memberfilename.pl");
    $myoutput =~ s/\\/\\\\/isg;
    $myoutput =~ s/~/\\\~/isg;
    $myoutput =~ s/\$/\\\$/isg;
    $myoutput =~ s/\@/\\\@/isg;
    $myoutput =~ s/\\\$/\$/isg;
    print FILE qq(\$output .= qq~$myoutput~;\n);
    $myoutput =~ s/\$/\\\$/isg;
    $myoutput =~ s/\\\~/~/isg;
    $myoutput =~ s/\\\$/\$/isg;
    $myoutput =~ s/\\\@/\@/isg;
    $myoutput =~ s/\\\\/\\/isg;
    print FILE "1;\n";
    close(FILE);
}
$myoutput =~ s/\$titlecolor/$titlecolor/isg;
$myoutput =~ s/\$catbackpic/$catbackpic/isg;
$myoutput =~ s/\$titlefontcolor/$titlefontcolor/isg;
$myoutput =~ s/\$forumcolorone/$forumcolorone/isg;
$myoutput =~ s/\$forumcolortwo/$forumcolortwo/isg;
$myoutput =~ s/\$fontcolormisc/$fontcolormisc/isg;
$output .= $myoutput;
1;
