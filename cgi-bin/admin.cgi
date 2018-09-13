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

&testsystem;
use strict;
use warnings;
use diagnostics;
use diagnostics;
use LBCGI;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "cleanolddata.pl";
eval {require "data/boardstats.cgi";};
if ($@) {
    require "repireboardinfo.pl";
    require "data/boardstats.cgi";
}

if (defined $_bbs_lib_loaded) {
    # do nothing
}
else {
    require "bbs.lib.pl";
}

eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;');
unless (WebGzip::getStatus()) {
    $gzipfunc = qq~Gzip 模块是否可用? == [通过]~;
}
else {
    $e = WebGzip::getStatus();
    $gzipfunc = qq~<font color=#FF0000>Gzip 模块是否可用? == [失败]</font> $e~
}

eval ('use GD;');
if ($@) {
    $gdfunc = qq~<font color=#FF0000>GD 模块是否可用? == [失败]</font>~;
}
else {
    $gdfunc = qq~GD 模块是否可用? == [通过]~;
}

$thisprog = "admin.cgi";
$query = new LBCGI;
#&ipbanned; #封杀一些 ip
$action = $query->param('action');
$loginprog = $query->param('loginprog');
$in_member_name = $query->param('membername');
$in_password = $query->param('password');
$in_passwordtemp = $in_password;
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}

$in_member_name = &unHTML("$in_member_name");
$in_password = &unHTML("$in_password");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

unlink("${lbdir}ilite.cgi");
unlink("${lbdir}cat.cgi");
unlink("${lbdir}record.cgi");

mkdir("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
mkdir("${lbdir}cache", 0777) if (!(-e "${lbdir}cache"));
mkdir("${lbdir}cache/online", 0777) if (!(-e "${lbdir}cache/online"));
mkdir("${lbdir}cache/myinfo", 0777) if (!(-e "${lbdir}cache/myinfo"));
mkdir("${lbdir}cache/mymsg", 0777) if (!(-e "${lbdir}cache/mymsg"));
mkdir("${lbdir}cache/meminfo", 0777) if (!(-e "${lbdir}cache/meminfo"));
mkdir("${lbdir}cache/id", 0777) if (!(-e "${lbdir}cache/id"));
mkdir("${lbdir}FileCount", 0777) if (!(-e "${lbdir}FileCount"));
mkdir("${lbdir}verifynum", 0777) if (!(-e "${lbdir}verifynum"));
mkdir("${lbdir}verifynum/login", 0777) if (!(-e "${lbdir}verifynum/login"));
mkdir("${lbdir}$saledir", 0777) if (!(-e "${lbdir}$saledir"));
chmod(0777, "${lbdir}verifynum");
chmod(0777, "${lbdir}verifynum/login");
chmod(0777, "${lbdir}$memdir/old");

if ((-e "${lbdir}install.cgi") && (!(-e "${lbdir}data/install.lock"))) {
    print "Content-type: text/html\n\n";
    print qq(
    <HTML><HEAD><TITLE>安装错误</TITLE></HEAD>
    <BODY BGCOLOR=#ffffff TEXT=#000000>
    <H1>LeoBBS 错误</H1><FONT COLOR=#ff0000><B>安全警告</B>：
    <br>install.cgi 文件仍然在您的服务器上，请马上利用 FTP 来将其删除！！<br> 当你删除之后，刷新本页面重新进入管理中心。</FONT></body></html>);
    exit;
}

if ($action eq "logout") {
    &cleanolddata1;
    print "Set-Cookie: adminname=\"\"\n";
    print "Set-Cookie: adminpass=\"\"\n";

    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

    &admintitle;
    print qq(
    <tr><td bgcolor=#2159C9><font color=#FFFFFF>
    <b>欢迎来到论坛管理中心</b>
    </td></tr>
    <tr><td bgcolor=#EEEEEE valign=middle align=center>
    <font color=#333333><b>您已经安全退出管理中心</b></font>
    </td></tr>
    <tr><td bgcolor=#FFFFFF></td></tr>
    </td></tr></table></td></tr></table>
    );
}
else {
    if ($action eq "login") {
        unlink("${lbdir}install.cgi") if (!(-e "${lbdir}data/install.lock"));
        &cleanolddata2;
        &checkverify;
        $tempmembername = uri_escape($in_member_name);
        print "Set-Cookie: adminname=$tempmembername\n";
        print "Set-Cookie: adminpass=$in_password\n";
    }
    else {
        &cleanolddata3;
        $in_member_name = $query->cookie('adminname');
        $in_password = $query->cookie('adminpass');
    }
    $in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
    &getadmincheck;

    print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

    &getmember("$in_member_name", "no");
    &admintitle;

    $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress = "no" if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);

    if ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
        if ($action eq "login") {
            my $thistime = time;
            $filetomake = "$lbdir" . "data/adminlogin.cgi";
            open(FILE, ">>$filetomake");
            print FILE "$in_member_name\t密码不显示\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t登录成功\t$thistime\t\n";
            close(FILE);
        }

        if ($loginprog ne "") {print "<script language='javascript'>document.location = '$loginprog'</script>";}

        $warning = qq~<br><font color=#000000>环境监测：<b>通过</b></font>~;

        $current_time = localtime;
        $in_member_name =~ s/\_/ /g;
        $start_topic_ratio = $totalthreads / $totalmembers if ($totalthreads && $totalmembers);
        $start_topic_ratio = substr($start_topic_ratio, 0, 5) if ($totalthreads && $totalmembers);
        $posting_ratio = $totalposts / $totalmembers if ($totalposts && $totalmembers);
        $posting_ratio = substr($posting_ratio, 0, 5) if ($totalposts && $totalmembers);
        $start_topic_ratio = 0 if ($start_topic_ratio eq "");
        $posting_ratio = 0 if ($posting_ratio eq "");

        $testcookie = $ENV{HTTP_COOKIE};
        if ($testcookie) {
            $cookie_result = qq(Cookies 是否可用? == [通过]);
        }
        else {
            $cookie_result = qq(<font color=#FF0000>Cookies 是否可用? == [失败]</font>);
        }

        $cgipath = &mypath();

        eval {$aa = md5_hex("112");};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$aa = md5_hex("112");');}
        unless ($@) {$md5mode = qq(MD5 模块是否可用? == [通过]);}
        else {$md5mode = qq(<font color=#FF0000>MD5 模块是否可用? == [失败]</font>);}

        print qq~
<tr><td bgcolor=#2159C9><font color=#FFFFFF><b>欢迎来到论坛管理中心</b></td></tr>
<tr><td bgcolor=#EEEEEE valign=middle align=center><font color=#333333><b>欢迎 $in_member_name</b></font></td></tr>
<tr><td bgcolor=#FFFFFF></td></tr>
<tr><td bgcolor=#FFFFFF valign=middle align=left>
<font color=#000000><center><br>
服务器时间：<b>$current_time</b><br>
</center>
$warning
<hr>
<font color=#000000><p>
<b>论坛数据摘要</b><br><br><br>
注册用户数：$totalmembers 人
<br>总发表主题：$totalthreads 篇
<br>总发表回复：$totalposts 篇<br><br>
<br>注册用户平均发表主题数：$start_topic_ratio 篇
<br>注册用户平均回复主题数：$posting_ratio 篇
<br><br>
<br>目录路径　：<font color=#FF0000>$cgipath</font> == [正确]
<br>Perl  版本：<font color=#FF0000>$]</font> == [通过]
<br>LBCGI 版本：<font color=#FF0000>$version_needed</font> == [通过]
<br>MD5　 测试：$md5mode
<br>Gzip　测试：$gzipfunc
<br>GD　　测试：$gdfunc
<br>Cookie测试：$cookie_result
<br><br>
<form action=setmembers.cgi method=POST>
<font color=#333333><b>查看、编辑、删除、禁止用户</b><BR>
<input type=hidden name=action value=edit>
<input type=text name=member size=10 maxlength=16>
<input type=submit value=快速定位>
</form>
<br><br><hr>
版权所有：山鹰(糊)、花无缺</font>
</font></td></tr></table></td></tr></table>
~;
    }
    else {
        &cleanolddata;
        &cleanolddata4;
        &adminlogin;

        if (($in_member_name ne "") && ($in_password ne "")) {
            my $thistime = time;
            $filetomake = "$lbdir" . "data/adminlogin.cgi";
            open(FILE, ">>$filetomake");
            print FILE "$in_member_name\t错$in_passwordtemp\t$ENV{'REMOTE_ADDR'}\t$trueipaddress\t\<B\>登录失败\<\/B\>\t$thistime\t\n";
            close(FILE);
            undef $thistime;
        }
    }
}
print qq~</td></tr></table></body></html>~;
exit;

sub testsystem {
    if (1 == 0) {
        print "Content-type: text/html\n\n";
        print qq(
	    <HTML><HEAD><TITLE>初始化错误</TITLE></HEAD>
	    <BODY BGCOLOR=#ffffff TEXT=#000000>
	    <H1>LeoBBS 出错</H1>如果您看到这个错误信息，那么说明本程序没有正确执行，它仅仅是作为普通的 HTML 输出显示。您必须要询问您的服务器管理员，这个目录是否有执行 CGI 程序的权限。<p></body></html>
	);
        exit;
    }
    my $prog = $0;
    open(PROG, $prog);
    my @prog = <PROG>;
    close(PROG);
    my $perl = $prog[0];
    $perl =~ s/^#!//;
    $perl =~ s/\s+$//;
    if ($] < 5.004) {
        print "Content-type: text/html\n\n";
        print qq(
	    <HTML><HEAD><TITLE>初始化错误</TITLE></HEAD>
	    <BODY BGCOLOR=#ffffff TEXT=#000000>
	    <H1>LeoBBS 出错</H1><FONT COLOR=#ff0000><B>Perl 版本警告</B>：您选择的 Perl 路径 - <B>$perl</B>，程序检测到它的版本为 $]，而 LeoBBS 必须运行在 Perl 5.004 以上版本。 <U>强烈</U> 推荐您联系服务器管理员升级 Perl 到 Perl 5.004 以上版本。</FONT></body></html>
	);
        exit;
    }
    $version_needed = $LBCGI::VERSION;
}

sub checkverify {
    my $verifynum = $query->param('verifynum');
    my $sessionid = $query->param('sessionid');
    $sessionid =~ s/[^0-9a-f]//isg;
    if (length($sessionid) != 32 && $useverify eq "yes") {
        $in_password = "";
        return;
    }

    ###获取真实的 IP 地址
    my $ipaddress = $ENV{'REMOTE_ADDR'};
    my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
    $trueipaddress = $ENV{'HTTP_CLIENT_IP'};
    $ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);

    ###获取当前进程的验证码和验证码产生时间、用户密码
    my $filetoopen = "${lbdir}verifynum/$sessionid.cgi";
    open(FILE, $filetoopen);
    $readdisktimes++;
    my $content = <FILE>;
    close(FILE);
    unlink($filetoopen);
    chomp($content);
    my ($trueverifynum, $verifytime, $savedipaddress) = split(/\t/, $content);
    my $currenttime = time;

    if (($verifynum ne $trueverifynum || $currenttime > $verifytime + 120 || $ipaddress ne $savedipaddress) && ($useverify eq "yes")) { #验证码有效时间仅为2分钟
        $in_password = "";
    }
    else {
        unlink("${lbdir}verifynum/$sessionid.cgi");
        unlink("${imagesdir}verifynum/$sessionid.cgi");
        mkdir("${lbdir}verifynum/login", 0777) unless (-d "${lbdir}verifynum/login");
        $memberfilename = $in_member_name;
        $memberfilename =~ y/ /_/;
        $memberfilename =~ tr/A-Z/a-z/;
        $memberfilename = "${lbdir}verifynum/login/$memberfilename.cgi";

        open(FILE, ">$memberfilename");
        print FILE "$currenttime\n";
        close(FILE);

    }
    return;
}

# 测试绝对路径
sub mypath {
    local $temp;
    if ($ENV{'SERVER_SOFTWARE'} =~ /apache/i) {
        if ($ENV{'SCRIPT_FILENAME'} =~ /cgiwrap/i) {
            $temp = $ENV{'PATH_TRANSLATED'};
        }
        else {
            $temp = $ENV{'SCRIPT_FILENAME'};
        }
        $temp =~ s/\\/\//g if ($temp =~ /\\/);
        $mypath = $temp;
        #        $mypath=substr($temp,0,rindex($temp,"/"));
    }
    else {
        $mypath = substr($ENV{'PATH_TRANSLATED'}, 0, rindex($ENV{'PATH_TRANSLATED'}, "\\"));
        $mypath =~ s/\\/\//g;
    }
    return $mypath;
}
