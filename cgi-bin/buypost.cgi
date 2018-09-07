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

use strict;
use warnings;
use LBCGI;
$LBCGI::POST_MAX=800000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "plugin.lib.pl";
$|++;       
$thisprog = "buypost.cgi";
$query = new LBCGI;

for ('postnumber','moneynumber','inforum','intopic','salemembername') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$salemembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]//isg;
&error("打开文件&老大，别乱黑我的程序呀1！") if ($postnumber !~ /^[0-9]+$/);
&error("打开文件&老大，别乱黑我的程序呀！") if ($intopic !~ /^[0-9]+$/);
&error("打开文件&老大，别乱黑我的程序呀！") if ($inforum !~ /^[0-9]+$/);
&error("打开文件&老大，别乱黑我的程序呀！") if (($moneynumber < 0)||($moneynumber > 99999));
&error("打开文件&老大，别乱黑我的程序呀！") if ($salemembername eq "");
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

&error("出错&请不要用外部连接本程序！") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "客人" ) {
    &error("普通错误&对不起，你目前的身份是访客，不能进入，请先登录!");
    exit;
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
     }
}
$mvmoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
if ($mvmoney < $moneynumber){ &error("购买帖子失败&老大，你的钱不够买这个帖子啊！");exit;}
if (lc($salemembername) eq lc($inmembername)) { &error("购买帖子失败&老大，你自己买自己的帖子做什么啊！");exit; }

open (FILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
my @threads = <FILE>;
close (FILE);

(my $membername1, my $no, $no, $no, $no, $no, my $post1, $no) = split(/\t/,$threads[$postnumber]);
$post1 =~ s/LBSALE\[(.*?)\]LBSALE//sg;
$buym = int($1);
&error("购买帖子失败&帖子数据有问题，不能进行买卖！") if ((lc($membername1) ne lc($salemembername))||($buym eq "")||($buym ne $moneynumber));

open (FILE, "${lbdir}$saledir/$inforum\_$intopic\_$postnumber.cgi");
$allbuyer = <FILE>;
close (FILE);
chomp $allbuyer;
$allbuyer = "\t$allbuyer\t";
$allbuyer =~ s/\t\t/\t/;
&error("购买帖子失败&你已经购买了这个帖子了，你刷新帖子就可以看到的！！") if ($allbuyer =~ /\t$inmembername\t/i);

open (FILE, ">>${lbdir}$saledir/$inforum\_$intopic\_$postnumber.cgi");
print FILE "$inmembername\t";
close (FILE);

&updateuserinfo("$inmembername",0,0,0,0,0,-$moneynumber,0);
$moneynumber1 = $moneynumber;
$moneynumber1 = int($moneynumber - $moneynumber * $postcess / 100) if ($postcess ne '' && $postcess >= 1 && $postcess <= 100);
&updateuserinfo("$salemembername",0,0,0,0,0,$moneynumber1,0);
$inmembername =~ s/ /\_/isg;
$inmembername =~ tr/A-Z/a-z/;
unlink ("${lbdir}cache/myinfo/$inmembername.pl");
unlink ("${lbdir}cache/meminfo/$inmembername.pl");
$salemembername =~ s/ /\_/isg;
$salemembername =~ tr/A-Z/a-z/;
unlink ("${lbdir}cache/myinfo/$salemembername.pl");
unlink ("${lbdir}cache/meminfo/$salemembername.pl");

$mvmoney = $mvmoney - $moneynumber;

print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&mischeader("购买帖子成功");

$output .= qq~<SCRIPT>valignend()</SCRIPT><table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>你付出 $moneynumber $moneyname，还剩余 $mvmoney $moneyname！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！
<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic">返回该主题</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=topic.cgi?forum=$inforum&topic=$intopic">
~;
&output("$boardname - 在$forumname内购买帖子",\$output);
exit;
