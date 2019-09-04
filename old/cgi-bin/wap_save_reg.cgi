#!/usr/bin/perl
#########################
# 手机论坛WAP版
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
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
$query = new LBCGI;
$LBCGI::POST_MAX = 2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "wap.lib.pl";
require "data/styles.cgi";
require "wap.pl";
$|++;
&waptitle;
$show .= qq~
<card  title="$board_name">~;
$in_member_name = $query->param('n');
$in_member_name = $uref->fromUTF8("UTF-8", $in_member_name);
$password = $query->param('p');
$password2 = $query->param('p1');
$emailaddress = $query->param('email');
$emailaddress = lc($emailaddress);
if (($in_member_name eq "") || ($emailaddress eq "")) {
    &errorout("用户注册&请输入用户名和邮件地址，这些是必需的！");
}
$ipaddress = $ENV{'REMOTE_ADDR'};
my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
$trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress eq "unknown" || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
$trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 ne "unknown" && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
$ipaddress = $trueipaddress;
my $charone = substr($emailaddress, 0, 1);
$charone = lc($charone);
$charone = ord($charone);
if ($oneaccountperemail eq "yes") {
    mkdir("${lbdir}data/lbemail", 0777) if (!(-e "${lbdir}data/lbemail"));
    chmod(0777, "${lbdir}data/lbemail");
    $/ = "";
    open(MEMFILE, "${lbdir}data/lbemail/$charone.cgi");
    my $allmemberemails = <MEMFILE>;
    close(MEMFILE);
    $/ = "\n";
    $allmemberemails = "\n$allmemberemails\n";
    chomp($allmemberemails);
    $allmemberemails = "\t$allmemberemails";

    if ($allmemberemails =~ /\n$emailaddress\t(.+?)\n/i) {
        &errorout("用户注册&对不起，这输入的 Email 已经被注册用户：<u>$1</u> 使用了");
    }
}
&errorout("用户注册&对不起，您输入的用户名（$in_member_name）有问题，请不要在用户名中包含\@\#\$\%\^\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]这类字符！") if ($in_member_name =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/);
if ($in_member_name =~ /_/) {&errorout("用户注册&请不要在用户名中使用下划线！");}
$in_member_name =~ s/\&nbsp\;//ig;
$in_member_name =~ s/　/ /g;
$in_member_name =~ s// /g;
$in_member_name =~ s/[ ]+/ /g;
$in_member_name =~ s/[ ]+/_/;
$in_member_name =~ s/[_]+/_/;
$in_member_name =~ s/�//isg;
$in_member_name =~ s///isg;
$in_member_name =~ s/　//isg;
$in_member_name =~ s///isg;
$in_member_name =~ s/()+//isg;
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]//isg;
$in_member_name =~ s/\s*$//g;
$in_member_name =~ s/^\s*//g;
&errorout("用户注册&对不起，您输入的用户名有问题") if ($in_member_name =~ /^q(.+?)-/ig || $in_member_name =~ /^q(.+?)q/ig);
$bannedmember = "no";
open(FILE, "${lbdir}data/banemaillist.cgi");
my $bannedemail = <FILE>;
close(FILE);
chomp $bannedemail;
$bannedemail = "\t$bannedemail\t";
$bannedemail =~ s/\t\t/\t/isg;
my $emailaddresstemp = "\t$emailaddress\t";
$bannedmember = "yes" if ($bannedemail =~ /$emailaddresstemp/i);
$filetoopen = "$lbdir" . "data/baniplist.cgi";
open(FILE, "${lbdir}data/baniplist.cgi");
my $bannedips = <FILE>;
close(FILE);
chomp $bannedips;
$bannedips = "\t$bannedips\t";
$bannedips =~ s/\t\t/\t/isg;

(my $ipaddresstemp = $ipaddress) =~ s/\./\\\./g;
$ipaddresstemp =~ /^((((.*?\\\.).*?\\\.).*?\\\.).*?)$/;
$bannedmember = "yes" if ($bannedips =~ /\t($1|$2|$3|$4)\t/);
$bannedmember = "yes" if (($in_member_name =~ /^m-/i) || ($in_member_name =~ /^s-/i) || ($in_member_name =~ /tr-/i) || ($in_member_name =~ /^y-/i) || ($in_member_name =~ /注册/i) || ($in_member_name =~ /guest/i) || ($in_member_name =~ /qq-/i) || ($in_member_name =~ /qq/i) || ($in_member_name =~ /qw/i) || ($in_member_name =~ /q-/i) || ($in_member_name =~ /qx-/i) || ($in_member_name =~ /qw-/i) || ($in_member_name =~ /qr-/i) || ($in_member_name =~ /^全体/i) || ($in_member_name =~ /register/i) || ($in_member_name =~ /诚聘中/i) || ($in_member_name =~ /斑竹/i) || ($in_member_name =~ /管理系统讯息/i) || ($in_member_name =~ /leobbs/i) || ($in_member_name =~ /leoboard/i) || ($in_member_name =~ /雷傲/i) || ($in_member_name =~ /LB5000/i) || ($in_member_name =~ /全体管理人员/i) || ($in_member_name =~ /管理员/i) || ($in_member_name =~ /隐身/i) || ($in_member_name =~ /短消息广播/i) || ($in_member_name =~ /暂时空缺/i) || ($in_member_name =~ /＊＃！＆＊/i) || ($in_member_name =~ /版主/i) || ($in_member_name =~ /坛主/i) || ($in_member_name =~ /nodisplay/i) || ($in_member_name =~ /^system/i) || ($in_member_name =~ /---/i) || ($in_member_name eq "admin") || ($in_member_name eq "root") || ($in_member_name eq "copy") || ($in_member_name =~ /^sub/) || ($in_member_name =~ /^exec/) || ($in_member_name =~ /\@ARGV/i) || ($in_member_name =~ /^require/) || ($in_member_name =~ /^rename/i) || ($in_member_name =~ /^dir/i) || ($in_member_name =~ /^print/i) || ($in_member_name =~ /^con/i) || ($in_member_name =~ /^nul/i) || ($in_member_name =~ /^aux/i) || ($in_member_name =~ /^com/i) || ($in_member_name =~ /^lpt/i));
if ($bannedmember eq "yes") {&errorout("用户注册&不允许注册，你填写的用户名、Email 或当前的 IP 被坛主设置成禁止注册新用户了，请更换或者联系坛主以便解决！");}
open(THEFILE, "${lbdir}data/noreglist.cgi");
$userarray = <THEFILE>;
close(THEFILE);
chomp $userarray;
@saveduserarray = split(/\t/, $userarray);
$noreg = "no";
foreach (@saveduserarray) {
    chomp $_;
    $_ =~ s/\|/\\\|/isg;
    if ($in_member_name =~ m/$_/isg) {
        $noreg = "yes";
        last;
    }
}
&errorout("用户注册&对不起，你所注册的用户名已经被保留或者被禁止注册，请更换一个用户名！") if ($noreg eq "yes");
if ($in_member_name =~ /\t/) {&errorout("用户注册&请不要在用户名中使用特殊字符！");}
if ($password =~ /[^a-zA-Z0-9]/) {&errorout("用户注册&论坛密码只允许大小写字母和数字的组合！！");}
if ($password =~ /^lEO/) {&errorout("用户注册&论坛密码不允许是 lEO 开头，请更换！！");}
$tempinmembername = $in_member_name;
$tempinmembername =~ s/ //g;
$tempinmembername =~ s/　//g;
if ($tempinmembername eq "") {&errorout("用户注册&你的用户名有点问题哟，换一个！");}
if ($in_member_name =~ /^客人/) {&errorout("用户注册&请不要在用户名的开头中使用客人字样！");}
if (length($in_member_name) > 12) {&errorout("用户注册&用户名太长，请不要超过12个字符（6个汉字）！");}
if (length($in_member_name) < 2) {&errorout("用户注册&用户名太短了，请不要少於2个字符（1个汉字）！");}
if (length($newlocation) > 12) {&errorout("用户注册&来自地区过长，请不要超过12个字符（6个汉字）！");}
if (($in_member_name =~ m/_/) || (!$in_member_name)) {&errorout("用户注册&用户名中含有非法字符！");}
if ($passwordverification eq "no") {
    if ($password ne $password2) {&errorout("用户注册&对不起，你输入的两次论坛密码不相同！");}
    if (length($password) < 8) {&errorout("用户注册&论坛密码太短了，请更换！论坛密码必须 8 位以上！");}
    #       if ($password =~ /^[0-9]+$/) { &errorout("用户注册&论坛密码请不要全部为数字，请更换！"); }
}
if ($in_member_name eq $password) {&errorout("用户注册&请勿将用户名和论坛密码设置成相同！");}
if ($emailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) {&errorout("用户注册&邮件地址错误！");}
$emailaddress =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
&getmember("$in_member_name", "no");
if ($userregistered ne "no") {&errorout("用户注册&该用户已经存在，请重新输入一个新的用户名！");}
$member_code = "me";
$memberfiletitle = $in_member_name;
$memberfiletitle =~ y/ /_/;
$memberfiletitle =~ tr/A-Z/a-z/;
$memberfiletitletemp = unpack("H*", "$memberfiletitle");
$joineddate = time;

mkdir("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
chmod(0777, "${lbdir}$memdir/old");
my $namenumber = &getnamenumber($memberfiletitle);
$filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
if (open(FILE, ">$filetomake")) {
    print FILE "$in_member_name\t$password\t$membertitle\t$member_code\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$addjy\t$meili\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t\t\t$soccerdata\t0\t";
    close(FILE);
}
$filetomake = "$lbdir" . "$memdir/old/$memberfiletitle.cgi";
if (open(FILE, ">$filetomake")) {
    print FILE "$in_member_name\t$password\t$membertitle\t$member_code\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$addjy\t$meili\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t\t\t$soccerdata\t0\t";
    close(FILE);
}

$filetomakeopen = "${lbdir}data/lbmember.cgi";
if (open(MEMFILE, ">>$filetomakeopen")) {
    print MEMFILE "$in_member_name\t$member_code\t0\t$joineddate\t$emailaddress\t\n";
    close(MEMFILE);
}

$filetomakeopen = "${lbdir}data/lbemail/$charone.cgi";
if (open(MEMFILE, ">>$filetomakeopen")) {
    print MEMFILE "$emailaddress\t$in_member_name\n";
    close(MEMFILE);
}

$filetomakeopen = "${lbdir}data/lbmember4.cgi";
if (open(MEMFILE, ">>$filetomakeopen")) {
    print MEMFILE "$in_member_name\t$ipaddress\t\n";
    close(MEMFILE);
}

require "$lbdir" . "data/boardstats.cgi";
$filetomake = "$lbdir" . "data/boardstats.cgi";
my $filetoopens = &lockfilename($filetomake);
if (!(-e "$filetoopens.lck")) {
    $totalmembers++;
    &winlock($filetomake) if ($OS_USED eq "Nt");
    if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$in_member_name\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close(FILE);
    }
    &winunlock($filetomake) if ($OS_USED eq "Nt");
}
else {
    unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
}
FILE:
my $x = &myrand(1000000000);
$x = crypt($x, aun);
$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
$x =~ s/[^\w\d]//g;
$x = substr($x, 2, 9);
if (-e "${lbdir}wap/$x") {goto FILE;}
my $xh2 = $ENV{'REMOTE_ADDR'};
open(file, ">${lbdir}wap/$x");
print file "$in_member_name,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2";
close(file);

open(file, "${lbdir}wap/all.h");
my @s = <file>;
close(file);

open(file, ">${lbdir}wap/all.h");
foreach (@s) {
    chomp;
    my ($n, $s) = split(/\,/, $_);
    if ($in_member_name eq $n) {
        unlink "${lbdir}wap/$s";
    }
    else {print file "$_\n";}
}
print file "$in_member_name,$x\n";
close(file);
$show .= qq~<p>
	注册成功，您的幸运ID为：$x,您的IP为：$xh2，请不要泄漏您的幸运ID给任何人！如果您是用手机访问且手机为私有，请把下面进入的首页地址加入书签(书签地址：$boardurl/wap.cgi?lid=$x ，加入之后可免登陆) 。否则请不要加入书签！</p><p><a href="wap.cgi?lid=$x">点击此处进入首页</a>
	</p>~;
&wapfoot;