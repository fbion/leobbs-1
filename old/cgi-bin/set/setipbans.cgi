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

$thisprog = "setipbans.cgi";

$query = new LBCGI;

$wordarray = $query->param('wordarray');
$action = $query->param("action");
$action = &cleaninput("$action");

$in_member_name = $query->cookie("adminname");
$in_password = $query->cookie("adminpass");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

&admintitle;

if ($action eq "process") {

    &getmember("$in_member_name", "no");

    if ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {

        $wordarray =~ s/\s+/\n/ig;
        $wordarray =~ s/\n\n/\n/ig;
        $wordarray =~ s/[^0-9\.\-\n\.\$]//isg;

        $wordarray2display = $wordarray;
        $wordarray2display =~ s/\n/<br>/g;

        $filetomake = "$lbdir" . "data/ipbans.cgi";
        open(FILE, ">$filetomake");
        print FILE $wordarray;
        close(FILE);

        opendir(DIRS, "${lbdir}cache/id");
        my @files = readdir(DIRS);
        closedir(DIRS);
        foreach (@files) {
            $_ =~ s/\.cgi//isg;
            unlink("${lbdir}cache/id/$_\.cgi");
        }

        if (-e $filetomake && -w $filetomake) {
            print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / IP 禁止</b>
		</td></tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#333333><center><b>所有的信息已经保存</b></center><br><br>
		<b>你已经对下列 IP 进行了处理（第一个字符是 - 的为禁止）</b><br><br>
		);
            print qq(<b>$wordarray2display</b><br>);
            print qq(
                <br><br><br><center><a href="setipbans.cgi">再次增加一些禁止的 IP</a></center>);
        }
        else {
            print qq(
                    <tr><td bgcolor=#2159C9" colspan=2><font color=#FFFFFF>
			<b>欢迎来到 LeoBBS 论坛管理中心</b>
			</td></tr>
			<tr>
			<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
			<font color=#333333><b>所有的信息没有保存</b><br>有文件或目录为不可写，请设置属性 777 ！
                    	</td></tr></table></td></tr></table>
		     	);
        }
    }
}
else {

    &getmember("$in_member_name", "no");

    if ((($member_code eq "ad") || ($member_code eq "smo")) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {

        $filetoopen = "$lbdir" . "data/ipbans.cgi";
        open(FILE, "$filetoopen");
        @bannedips = <FILE>;
        close(FILE);

        print qq(
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
		<b>欢迎来到论坛管理中心 / IP 禁止</b>
		</td></tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<font color=#333333><b>IP 禁止列表</b>
		</td></tr>
		<form action="$thisprog" method="post">
		<input type=hidden name="action" value="process">
		<tr>
		<td bgcolor=#FFFFFF valign=middle colspan=2>
		<font color=#000000>
		<b>请注意:</b>如果你禁止了一个 IP 的话，那么这个 IP 将无法进入论坛！<br>
		<br>
                    <table width="100%" border="1" height="122" cellspacing="0" cellpadding="0">
                      <tr> 
                        <td width="34%"> 
                          <div align="center">规则</div>
                        </td>
                        <td width="33%"> 
                          <div align="center">例１</div>
                        </td>
                        <td width="33%"> 
                          <div align="center">例２</div>
                        </td>
                      </tr>
                      <tr> 
                        <td height="51" width="35%">１列出的单机或网段地址为允许地址<br>
                          ２在ip前加“-”为不允许<br>
                          ３同一网段的，应长地址排前</td>
                        <td height="51" width="33%"> 
                          <p>80.32.96.11<br>
                            -80.32.96.<br>
                            <br>
                            注：不允许80.32.96段，只允许80.32.96.11<br>
                          </p>
                        </td>
                        <td height="51" width="33%">-80.32.96.11 <br>
                          80.32.96.<br>
                          <br>
                          注：允许80.32.96段，不允许80.32.96.11</td>
                      </tr>
                      <tr> 
                        <td> 
                          <div align="center">备注</div>
                        </td>
                        <td>&nbsp;</td>
                        <td>&nbsp;</td>
                      </tr>
                      <tr> 
                        <td colspan="3">说明１：不列出的地址默认为允许，见备注。</td>
                      </tr>
                      <tr>
                        <td colspan="3">说明２：地址不足三位，左边不用补０（不要画蛇添足哦）。</td>
                      </tr>
                      <tr> 
                        <td colspan="3">说明３：如果你要禁止一个 B 类网，那么你可以不输入 IP 的最后两位，比如：202.100.。</td>
                      </tr>
                      <tr>
                        <td colspan="3">说明４：注意上面的写法，如果禁止的是一个 C 类或者 B 类网，请最后保留点号(.)，切记！</td>
                      </tr>
                      <tr> 
                        <td colspan="3">说明５：每行写一个 IP，注意最后回车！</td>
                      </tr>
                      <tr> 
                        <td colspan="3">说明６：如果要封类似210.126.1.这样的IP段，请用-210.126.1\.！</td>
                      </tr>
                      <tr> 
                        <td colspan="3">说明７：如果要封类似210.126.1.4这样的IP段，请用-210.126.1.4\$ ！</td>
                      </tr>
                    </table>
	                </font></td>
		</tr>
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=center colspan=2>
		<textarea cols=60 rows=22  name="wordarray">);
        foreach (@bannedips) {
            $singleip = $_;
            chomp $_;
            next if ($_ eq "");
            #$singleip =~ s/\n\s/\n/g;
            print qq($singleip);
        }
        print qq(</textarea><BR>
		</td>
		</tr>
		<tr>
		<td bgcolor=#EEEEEE valign=middle align=center colspan=2>
		<input type=submit name=submit value=提交></td></form></tr></table></td></tr></table>
);

    }
    else {
        &adminlogin;
    }
}
print qq~</td></tr></table></body></html>~;
exit;
