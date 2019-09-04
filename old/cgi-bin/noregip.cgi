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

$thisprog = "noregip.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
$userarray = $query->param('userarray');
$action = $query->param("action");
$action = &cleaninput("$action");

$in_member_name = $query->cookie("adminname");
$in_password = $query->cookie("adminpass");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;

&getmember("$in_member_name", "no");

if ($action eq "process") {
    if ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
        $userarray .= "\n";
        $userarray =~ s/\t//isg;
        $userarray =~ s/\r\n/\n/ig;
        $userarray =~ s/\n+/\n/ig;
        $userarray =~ s/\n/\t/isg;
        $userarray =~ s/\*\[\]\(\)\?\+\=\|//isg;
        $filetomake = "$lbdir" . "data/baniplist.cgi";
        open(FILE, ">$filetomake");
        print FILE $userarray;
        close(FILE);

        if (-e $filetomake && -w $filetomake) {
            print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>欢迎来到论坛管理中心</b>
            </td></tr><tr><td bgcolor=#FFFFFF colspan=2><font color=#333333><center><b>所有的信息已经保存</b></center><br><br>
            <b>你已经禁止了下列 IP ，使用这些 IP 的用户将不允许被申请。</b><br><br>~;

            @saveduserarray = split(/\t/, $userarray);
            foreach (@saveduserarray) {
                chomp $_;
                print "$_<br>";
            }
            print qq~<br><br><br><center><a href="noregip.cgi">禁止更多的特殊 IP 地址注册用户</a></center>~;
        }
        else {
            print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>欢迎来到论坛管理中心</b></td></tr><tr>
            <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
            </td></tr></table></td></tr></table>~;
        }
    }
    else {
        &adminlogin;
    }

}
else {
    if ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
        open(FILE, "${lbdir}data/baniplist.cgi");
        my $badusers = <FILE>;
        close(FILE);
        $badusers =~ s/\t/\n/g;
        print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>欢迎来到论坛管理中心 / 禁止一些特殊的 IP 地址注册用户</b></td></tr><tr>
	    <td bgcolor=#EEEEEE align=center colspan=2><font color=#333333><b>禁止一些特殊的 IP 地址注册用户</b></td></tr>
            <form action="$thisprog" method="post">
            <input type=hidden name="action" value="process">
            <tr><td bgcolor=#FFFFFF colspan=2><font color=#000000>
            <b>请注意：</b> 此功能是用来禁止一些特殊的 IP 地址，使用这些 IP 的用户将不允许被注册。这样可以阻止一些捣乱的人多次注册用户。<BR><BR>输入的时候，每行输入一个 IP 地址即可(必须输入完整，比如： 202.96.111.42 )。<BR><BR>
            </font></td></tr>
            <tr><td bgcolor=#FFFFFF align=center colspan=2>
            <textarea cols=60 rows=18 wrap="virtual" name="userarray">$badusers</textarea><BR><BR>
            </td></tr>
            <tr><td bgcolor=#EEEEEE align=center colspan=2>
            <input type=submit name=submit value="提 交"></td></form></tr></table></td></tr></table>~;
    }
    else {
        &adminlogin;
    }
}
print qq~</td></tr></table></body></html>~;
exit;
