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
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "getmypass.cgi";
$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

$inmembername  = $query -> param("username");
$inpassword    = $query -> param("password");
$inmembername =~ s/\_/ /isg;

$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&error("修改密码&错误，校验出错，请不要胡乱修改！") if (($inmembername eq "")||($inpassword eq ""));

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "客人") {
    $inmembername = "客人";
    $userregistered = "no";
    &error("修改密码&错误，用户名不能为空！");
}
else {
    &getmember("$inmembername","no");
    &error("修改密码&错误，此用户不存在！") if ($userregistered eq "no");
}

opendir (DIRS, "${lbdir}$msgdir");
my @files = readdir(DIRS);
closedir (DIRS);
@files = grep(/\.cgi$/i, @files);
foreach (@files) {unlink ("${lbdir}$msgdir/$_") if ((-M "${lbdir}$msgdir/$_") > 1);}

$inmembernamefile = $inmembername;
$inmembernamefile =~ s/ /\_/g;
$inmembernamefile =~ tr/A-Z/a-z/;

if (-e "${lbdir}$msgdir/$inmembernamefile.cgi") {
    open(FILE, "${lbdir}$msgdir/$inmembernamefile.cgi");
    $x = <FILE>;
    close(FILE);
    chomp $x;
} else {
    &error("修改密码&超时错误，请在取回密码操作的一天内完成修改密码工作！");
}

if ($password ne "") {
    $password = "$x$password";
    eval {$mypassword = md5_hex($password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$mypassword = md5_hex($password);');}
}

&error("修改密码&错误，密码校验出错，请不要胡乱修改！") if ($mypassword ne $inpassword);
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&mischeader("取回密码");
$action        = $query -> param('action');
$output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
~;

if ($action eq "login") {
    $password1 = $query -> param('password1');
    $password2 = $query -> param('password2');
    if ($password1 ne $password2) { &error("取回密码&对不起，你输入的两次论坛密码不相同！"); }
    if($password1 =~ /[^a-zA-Z0-9]/)     { &error("取回密码&论坛密码只允许大小写字母和数字的组合！！"); }
    if($password1 =~ /^lEO/)     { &error("取回密码&论坛密码不允许是 lEO 开头，请更换！！"); }
    if(length($password1)<8)      { &error("取回密码&论坛密码太短了，请更换！论坛密码必须 8 位以上！"); }

    if ($password1 ne "") {
        eval {$password1 = md5_hex($password1);};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$password1 = md5_hex($password1);');}
        $password1 = "lEO$password1";
    }
    
    if (($inmembername ne "")&&($password1 ne "")) {
    	my $namenumber = &getnamenumber($inmembernamefile);
	&checkmemfile($inmembernamefile,$namenumber);
	$filetomake = "$lbdir" . "$memdir/$namenumber/$inmembernamefile.cgi";
	&winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE3,"+<$filetomake");
        flock(FILE3, 2) if ($OS_USED eq "Unix");
        my $filedata = <FILE3>;
	chomp($filedata);
	($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber ,$location ,$interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount,$ebankdata,$onlinetime,$userquestion,$awards,$jifen,$userface,$soccerdata,$useradd5) = split(/\t/,$filedata);
	seek(FILE3,0,0);
	print FILE3 "$membername\t$password1\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
	close(FILE3);
	if (open(FILE, ">${lbdir}$memdir/old/$inmembernamefile.cgi")) {
	    print FILE "$membername\t$password1\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
	    close(FILE);
	}
	&winunlock($filetomake) if ($OS_USED eq "Nt");
    }
    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font face="$font" color=$fontcolormisc><b>$inmembername，您的新密码已经生效！</b></font></td></tr>
<tr><td bgcolor=$miscbackone valign=middle><font face="$font" color=$fontcolormisc>
具体情况：<ul><li><a href="loginout.cgi">按此登录论坛</a>
</ul></tr></td></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
~;
    unlink ("${lbdir}$msgdir/$inmembernamefile.cgi");
}
else {
    $output .= qq~<tr>
<td bgcolor=$titlecolor $catbackpic valign=middle colspan=2 align=center>
<form action="$thisprog" name="login" method="post" onSubmit="submitonce(this)">
<input type=hidden name="action" value="login">
<input type=hidden name="username" value="$inmembername">
<input type=hidden name="password" value="$inpassword">
<font face="$font" color=$fontcolormisc><b>$inmembername，您的身份已经通过确认，请输入您的新密码</b></font></td></tr>
<tr><td width=40% bgcolor=$miscbackone><font color=$fontcolormisc><b>论坛密码： (至少8位)</b><br>请输入论坛密码，区分大小写<br>只能使用大小写字母和数字的组合</font></td><td width=60% bgcolor=$miscbackone><input type=password name="password1">&nbsp;* 此项必须填写</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>论坛密码： (至少8位)</b><br>再输一遍，以便确定！</font></td><td bgcolor=$miscbackone><input type=password name="password2">&nbsp;* 此项必须填写</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit value="确 定" name=submit></td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR><BR>
~;
}
&output("$boardname - 取回密码",\$output);
exit;
