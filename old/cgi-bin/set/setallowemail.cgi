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

use warnings;
use strict;
use diagnostics;
use LBCGI;
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "setallowemail.cgi";
$query = new LBCGI;

$action = ($query->param('action') ne "") ? 'process' : 'toppage';
$wordarray = $query->param('wordarray');
$select_type = ($query->param('select_type') eq "allow") ? 'allow' : 'ban';

$in_member_name = $query->cookie('adminname');
$in_password = $query->cookie('adminpass');
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

my %Mode = ('process' => \&process);

#################--- Main program ---###################
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;
&getmember("$in_member_name", "no");
if ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
    print qq~
		<tr><td bgcolor="#2159C9" colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / 限制(允许)可注册邮箱</b>
		</td></tr>~;
    if ($Mode{$action}) {
        $Mode{$action}->();
    }
    else {
        &toppage;
    }
    print qq~</td></tr></table></td></tr></table>~;
}
else {
    &adminlogin;
}
sub toppage {
    $allowmail = "";
    $filetoopen = "$lbdir" . "data/allow_email.cgi";
    open(FILE, "$filetoopen");
    $allowtype = <FILE>;
    $allowmail = <FILE>;
    close(FILE);
    chomp $allowtype;
    chomp $allowmail;
    $allowmail =~ s/\t/\n/g;
    $allowmail =~ s/ //g;
    $allowtype = ($allowtype eq "allow") ? 'allow' : 'ban';
    $select_type{$allowtype} = ' checked';

    print qq~
	<form action="$thisprog" method="post">
	<tr>
	<td bgcolor="#EEEEEE" align="center" colspan="2">
	<font color="#333333"><b>限制可注册邮箱</b>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<table width=80% align=center>
	<tr><td><ol type="1">
	<li>此功能可限制必需以某些邮箱注册。
	<li>也可限制某几个邮箱不能注册，防止用免费邮箱大量注册。
	<li>输入的时候，每行输入一个邮箱域名即可。<B><U>不用加上帐号名称和 \@ 号</U></B>。
	<li>输入的邮箱域名不区分大小写。
	<LI>比如，输入 hotmail.com，限制方式为“以上的邮箱不允许注册”，<BR>这样就拒绝了所有使用 hotmail.com 信箱的人前来注册。
	</ol></td></tr>
	</table>
	</td>
	</tr>
	
	<input type=hidden name="action" value="process">
	
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<textarea cols=60 rows=20 wrap="virtual" name="wordarray">$allowmail</textarea>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" width="30%" align="right">限制方式：
	</td>
	<td bgcolor="#FFFFFF"><input type="radio" name="select_type" value="allow"$select_type{'allow'}>必需为以上邮箱才能注册 <input type="radio" name="select_type" value="ban"$select_type{'ban'}>以上的邮箱不允许注册</td>
	</tr>
	
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<input type=submit name=submit value="提 交">
	</td>
	</tr>
	</form>
	~;
}
sub process {
    $output_text = ($select_type eq "allow") ? '只能使用这些邮箱注册' : '使用这些邮箱注册不能注册';
    $select_type .= "\n";
    $wordarray .= "\n";
    $wordarray =~ s/[\a\f\e\0\r\t ]//isg;
    $wordarray =~ s/\r\n/\n/ig;
    $wordarray =~ s/\n+/\n/ig;
    $wordarray =~ s/\n/\t/isg;
    $filetoopen = "$lbdir" . "data/allow_email.cgi";
    open(FILE, ">$filetoopen");
    print FILE $select_type;
    print FILE $wordarray;
    close(FILE);

    print qq~
	<tr>
	<td bgcolor="#EEEEEE" align="center" colspan="2">
	<font color="#333333"><b>邮箱限制已经保存</b>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<font color="#333333"><b>下列限制邮箱被保存，$output_text。</b>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<table width=80% align=center>
	<tr><td>
	<ol>
	~;
    @savedwordarray = split(/\t/, $wordarray);
    foreach $word (@savedwordarray) {
        chomp $word;
        print qq~<li>$word~;
    }
    print qq~
	</ol></td></tr>
	</table>
	</td>
	</tr>
	<tr>
	<td bgcolor="#FFFFFF" align="center" colspan="2">
	<a href="$thisprog?"><font color="#333333">继续增加要限制的邮箱</font></a>
	</td>
	</tr>
	~;
}