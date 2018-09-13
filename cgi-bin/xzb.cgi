#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "code.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "postjs.cgi";
$|++;
$thisprog = "xzb.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$hownews = "100" if (($hownews eq "") || ($hownews < 50));

for ('forum', 'membername', 'password', 'action', 'inpost', 'message', 'id') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$in_forum = $forum;
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$inmembername = $membername;
$inpassword = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime = time;
$inmembername = &stripMETA($inmembername);

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}
if ($catsbackpicinfo ne "") {$catsbackpicinfo = "background=$imagesurl/images/$skin/$catsbackpicinfo";}

if (!$inmembername) {$inmembername = $query->cookie("amembernamecookie");}
if (!$inpassword) {$inpassword = $query->cookie("apasswordcookie");}
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$inmembername) or ($inmembername eq "客人")) {
    $inmembername = "客人";
    $userregistered = "no";
    &error("普通错误&请登录后再使用本功能！");
}
else {
    &getmember("$inmembername", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if ($inpassword ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}
&doonoff; #论坛开放与否
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

$helpurl = &helpfiles("阅读标记");
$helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

#        &moderator("$in_forum");
&getoneforum("$in_forum");
if ($startnewthreads eq "onlysub") {&error("发表&对不起，这里是纯子论坛区，不允许发言！");}
&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$membercode,/);
if ($allowusers ne '') {
    &error('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /\Q,$inmembername,\E/i);
}

my %Mode = (
    'new'    => \&newthread,
    'addnew' => \&addnewthread,
    'view'   => \&view,
    'del'    => \&del,
);

if ($Mode{$action}) {
    $Mode{$action}->();
}
else {&error("普通错误&请以正确的方式访问本程序！");}

&output("$boardname - 在$forumname内发小字报", \$output);

sub newthread {

    if (($privateforum eq "yes") || ($xzbopen eq "no") || ($startnewthreads eq "no")) {
        &error("张贴小字报&本论坛不允许张贴小字报!");
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t$forumname\tboth\t张贴小字报\t") if ($privateforum ne "yes");
        &whosonline("$inmembername\t$forumname(密)\tboth\t张贴新的保密小字报\t") if ($privateforum eq "yes");
    }
    if (($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes")) {
        &error("张贴小字报&斑竹和坛主不得参与,谢谢合作！");
    }

    &mischeader("张贴小字报");
    if (($xzbcost ne "") && ($xzbcost >= 0)) {
        $xzbcost = qq~<B>（花费 $xzbcost $moneyname）</B>~;
    }

    $startthreads = "任何注册会员(版主级别以上除外)均可以张贴！$xzbcost";

    $output .= qq~
                <form action="$thisprog" method=post name="FORM" >
                <input type=hidden name="action" value="addnew">
                <input type=hidden name="forum" value="$in_forum">
                <SCRIPT>valigntop()</SCRIPT>
        	<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            	<tr><td>
                <table cellpadding=6 cellspacing=1 width=100%>
                <tr>
                    <td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>谁可以张贴小字报？</b> $startthreads</td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，如果要以其他用户身份发表，请在下面输入用户名和密码。如果不想改变用户身份，请留空。</td>
                </tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td>
            <td bgcolor=$miscbackone>　<input type=text name="membername"></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td>
            <td bgcolor=$miscbackone>　<input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
		<tr>
		<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>小字报标题(最大 80 字)</b></td>
		<td bgcolor=$miscbackone>
		　<input type="text" maxlength="80" name=inpost onkeydown=ctlent() value="$inpost" size=80><br>

		</td></tr>
		<tr>
		<td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>小字报内容</b> (最多 $hownews 字)<p>
		 在此论坛中：<li>HTML 标签: <b>不可用</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a>: <b>可用</b>
		</td>
		<td bgcolor=$miscbacktwo valign=top>
		<b>　　每小时一贴，一旦发布可以免费宣传48小时</b><br>　
		<TEXTAREA cols=58 name=message rows=6 wrap=soft onkeydown=ctlent()>$message</TEXTAREA>
		</td>
		</tr>
		<tr>
                <td bgcolor=$miscbacktwo colspan=2 align=center>
                <input type=Submit value="发 布" name=Submit"  onClick="return clckcntr();">　　　<input type="reset" name="Clear" value="清 除">
                </td></form></tr>
            </table>
        </tr></td></table>
     <SCRIPT>valignend()</SCRIPT>
        ~;
}

sub addnewthread {

    if (($xzbcost ne "") && ($xzbcost >= 0)) {
        $mymoney2 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        if ($mymoney2 < $xzbcost) {
            &error("张贴小字报&对不起，你的钱数不够。至少应有 $xzbcost $moneyname。");
        }
    }
    if ($userregistered eq "no") {&error("张贴小字报&您没有注册！");}
    elsif ($inpassword ne $password) {&error("张贴小字报&您的密码错误！");}
    elsif (($membercode eq "banned") || ($membercode eq "masked")) {&error("张贴小字报&您被禁止发言！");}
    elsif ($inpost eq "") {&error("张贴小字报&必须输入标题！");}
    elsif (length($inpost) > 82) {&error("发表新投票&标题过长！");}
    else {
        if (($privateforum eq "yes") || ($xzbopen eq "no") || ($startnewthreads eq "no") || ($startnewthreads eq "cert")) {
            &error("张贴小字报&本论坛不允许张贴小字报!");
        }

        $dirtoopen = "$lbdir" . "boarddata";
        open(DIR, "<$dirtoopen/xzb$in_forum.cgi");
        @xzbdata = <DIR>;
        close(DIR);
        chomp(@xzbdata);
        $sizexzb = @xzbdata;
        $currenttime = time;
        if (($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes")) {
            &error("张贴小字报&斑竹和坛主不得参与,谢谢合作！");
        }

        ($tmp, $tmp, $tmp, $tmp, $lastpost) = split(/\t/, $xzbdata[0]);
        $lastpost = ($lastpost + 3600);

        if ($lastpost > $currenttime) {
            &error("张贴小字报&这个小时已经有人发表过一次小字报了，请过一个小时继续！");
        }

        $inpost =~ s/</&lt;/sg;
        $inpost =~ s/>/&gt;/sg;
        my $temp = &dofilter("$inpost\t$message");
        ($inpost, $message) = split(/\t/, $temp);

        $sizexzb = 48 if ($sizexzb > 48);
        $write = "＃―＃―・\t$inpost\t$inmembername\t$message\t$currenttime\t";
        @newxzb = ($write, @xzbdata);
        open(DIR, ">$dirtoopen/xzb$in_forum.cgi");
        for ($i = 0; $i <= $sizexzb; $i++) {
            print DIR "$newxzb[$i]\n";
        }

        &mischeader("新小字报张贴成功");

        $relocurl = "forums.cgi?forum=$in_forum";

        if (($xzbcost ne "") && ($xzbcost >= 0)) {
            $cleanmembername = $inmembername;
            $cleanmembername =~ s/ /\_/isg;
            $cleanmembername =~ tr/A-Z/a-z/;

            $cleanmembername = &stripMETA($cleanmembername);
            $cleanmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

            my $namenumber = &getnamenumber($cleanmembername);
            &checkmemfile($cleanmembername, $namenumber);
            $filetomake = "$lbdir" . "$memdir/$namenumber/$cleanmembername.cgi";
            &winlock($filetomake) if ($OS_USED eq "Nt");
            open(fh, "$filetomake");
            flock(fh, 1) if ($OS_USED eq "Unix");
            $filedata = <fh>;
            close(fh);
            chomp $filedata;
            (my $membername, my $password, my $membertitle, my $membercode, my $numberofposts, my $emailaddress, my $showemail, my $ipaddress, my $homepage, my $oicqnumber, my $icqnumber, my $location, my $interests, my $joineddate, my $lastpostdate, my $signature, my $timedifference, my $privateforums, my $useravatar, my $userflag, my $userstar, my $usersx, my $personalavatar, my $personalwidth, my $personalheight, my $rating, my $lastgone, my $visitno, my $useradd04, my $useradd02, my $mymoney, my $postdel, my $sex, my $education, my $marry, my $work, my $born, my $chatlevel, my $chattime, my $jhmp, my $jhcount, my $ebankdata, my $onlinetime, my $awards, my $jifen, my $userface, my $soccerdata, my $useradd5) = split(/\t/, $filedata);
            $mymoney -= $xzbcost;

            if ($password ne "") {
                if (open(fh, ">${lbdir}$memdir/$namenumber/$cleanmembername.cgi")) {
                    flock(fh, 2) if ($OS_USED eq "Unix");
                    print fh "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userstar\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t\n";
                    close(fh);
                }
            }
            &winunlock($filetomake) if ($OS_USED eq "Nt");
        }

        $output .= qq~
            <SCRIPT>valigntop()</SCRIPT>
            <table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
            <tr>
            <td>
            <table cellpadding=6 cellspacing=1 width=100%>
            <tr>
            <td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>谢谢！您的新小字报已经张贴成功！</b></font></td></tr>
            <tr>
            <td bgcolor=$miscbackone><font color=$fontcolormisc>
            如果浏览器没有自动返回，请点击下面的链接！
            <ul>
            <li><a href="forums.cgi?forum=$in_forum">返回论坛</a>
            <li><a href="leobbs.cgi">返回论坛首页</a>
            </ul>
            </tr>
            </td>
            </table></td></tr></table>
            <SCRIPT>valignend()</SCRIPT>
            <meta http-equiv="refresh" content="3; url=$relocurl">
            ~;

    }
}



sub view {
    &error("老大你别黑我的程序啊!") if (($id eq "") || ($in_forum eq ""));
    $dirtoopen = "$lbdir" . "boarddata";
    open(DIR, "<$dirtoopen/xzb$in_forum.cgi");
    @xzbdata = <DIR>;
    close(DIR);
    chomp(@xzbdata);
    $xzbdata[$id] =~ s/^＃―＃―・\t//isg;
    ($title, $postid, $msg, $posttime) = split(/\t/, $xzbdata[$id]);
    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t$forumname\tboth\t阅读小字报\t") if ($privateforum ne "yes");
        &whosonline("$inmembername\t$forumname(密)\tboth\t阅读保密小字报\t") if ($privateforum eq "yes");
    }

    $dateposted = $posttime + ($timedifferencevalue * 3600) + ($timezone * 3600);
    $dateposted = &dateformat("$dateposted");
    &lbcode(\$msg);
    $admindelete = qq~
       <a href=xzb.cgi?action=del&forum=$in_forum&id=$id OnClick="return confirm('确定删除这个小字报么？');">删除</a>
       ~;
    $output = qq~<P><SCRIPT>valigntop()</SCRIPT>
	<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=#000000 align=center>
	                <tr>
	                    <td>
	                    <table cellpadding=3 cellspacing=1 width=100% style="TABLE-LAYOUT: fixed">
	~;

    $output .= qq~
	                  <tr>
	                  <td bgcolor=$titlecolor align=center valign=top $catbackpic><font face="$font" color=$titlefontcolor><b>>> $title <<</b></td></tr>
		    ~;
    if (($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes") || ($postid eq "$inmembername")) {
        $output .= qq~
	                      	<tr>
	                      	    <td bgcolor=$postcolortwo align=right>$admindelete</td>
	                       	</tr>
			  ~;
    }

    $output .= qq~
	                 <tr>
	                    <td bgcolor="$postcolortwo" valign=top style="LEFT: 0px; WIDTH: 100%; WORD-WRAP: break-word"><font face="$font" color=$postfontcolortwo>
	                        $msg
	                    </td>
	                 </tr>
	                 <tr>
	                    <td bgcolor="$postcolortwo" valign=middle>
	                     <table width=100% border="0" cellpadding="0" cellspacing="0">
	                        <tr><td align=left>&nbsp;&nbsp;&nbsp;<font face="$font" color=$postfontcolortwo><b>发布人</b>： $postid</font>
	                        </td><td align=right><font face="$font" color=$postfontcolortwo><b>发布时间</b>： $dateposted</font>&nbsp;&nbsp;&nbsp;
	                        </tr>
	                        </table>
	                        </td>
	                        </font>
	                        </tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>

	              ~;
    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
    &output("$boardname - 在$forumname内查看小字报", \$output);

    exit;
}

sub del {
    &error("老大你别黑我的程序啊!") if (($id eq "") || ($in_forum eq ""));
    $dirtoopen = "$lbdir" . "boarddata";
    open(DIR, "<$dirtoopen/xzb$in_forum.cgi");
    @xzbdata = <DIR>;
    $sizexzb = @xzbdata;
    close(DIR);
    chomp(@xzbdata);
    ($nouse, $title, $postid, $msg, $posttime) = split(/\t/, $xzbdata[$id]);
    if (($membercode ne "ad") && ($membercode ne 'smo') && ($inmembmod ne "yes") && ($postid ne "$inmembername")) {
        &error("删除小字报&你没权力删除!");
    }

    open(DIR, ">$dirtoopen/xzb$in_forum.cgi");
    for ($i = 0; $i < $sizexzb; $i++) {
        if ($i ne $id) {
            print DIR "$xzbdata[$i]\n";

        }
    }
    close(DIR);

    $output = qq~
	<script>alert("小字报删除成功！");top.window.close();</script>
	~;
    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
    print $output;

    exit;
}
