#!/usr/bin/perl
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
use warnings;
use strict;
use LBCGI;
use diagnostics;
$query = new LBCGI;
require "data/boardinfo.cgi";
require "bbs.lib.pl";
require "wap.pl";
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
print "<title>生成幸运ID</title>";
$in_member_name = $query->cookie("amembernamecookie");
$in_password = $query->cookie("apasswordcookie");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ((!$in_member_name) or ($in_member_name eq "客人")) {&error("普通错误&客人不能进行操作");}
else {
    &getmember("$in_member_name", "no");
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
    &error("普通错误&用户没有登录或注册！") if ($userregistered eq "no");
}

$ip = $query->param('ip');
if ($ip ne '') {
    FILE:
    my $x = int(rand(99999999999999));
    $x = substr($x, 2, 9);
    if (-e "${lbdir}wap/$x") {goto FILE;}
    my $xh2 = $ip;
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
    print qq~<p>您的幸运ID为：$x,您的IP为：$xh2，请不要泄漏您的幸运ID给任何人！请把下面进入的首页地址加入手机书签(书签地址：$boardurl/wap.cgi?lid=$x ，加入之后可免登陆) 。否则请不要加入书签！</p><p>注意：本幸运ID全为数字。</p>~;
}
else {
    print "<form name=post method=post action=loginwap.cgi>请输入您的手机IP：<br><br>进入手机WAP：$boardurl/wap.cgi，点击“登陆”，获取手机IP<br><input name=ip value='' type=text><input type=submit value=生成Url></form>";
}
exit;