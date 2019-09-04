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
$LBCGI::POST_MAX = 20000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use MAILPROG qw(sendmail);
require "data/boardinfo.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";

$|++;

$thisprog = "mailmembers.cgi";

$remprog = "remmail.cgi";

$query = new LBCGI;

$action = $query->param('action');
$subjekt = $query->param('subjekt');
$message = $query->param('text');
$sendto = $query->param('sendto');
$membersnamesin = $query->param('membersnames');
$footerlinein = $query->param('footerline');
$action = &unHTML("$action");
$subjekt = &unHTML("$subjekt");
$message = &unHTML("$message");
$sendto = &unHTML("$sendto");

$in_member_name = $query->cookie("adminname");
$in_password = $query->cookie("adminpass");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$WIN = $^O =~ /Win32/oi;
$MAC = $^O =~ /MacOS/oi;
$UNIX = !($WIN || $MAC);

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;

&getmember("$in_member_name", "no");

if (($member_code eq "ad") && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {

    print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / Email 群发</b>
            </td></tr>
            ~;

    if ($action eq "send") {&sendmymail;}
    elsif ($action eq "sent") {&mailsent;}
    elsif ($action eq "compose") {&composemail;}
    elsif ($action eq "view") {&view;}
    elsif ($action eq "Update") {&update;}
    elsif ($action eq "footer") {&viewfoot;}
    elsif ($action eq "Save") {&updatefoot;}
    else {&mailoptions;}

    print qq~</table></td></tr></table>~;
}
else {
    &adminlogin;
}
exit;

sub mailoptions {

    $output = qq~
 <tr>
 <br><br><td bgcolor=#eeeeee colspan=2 align=center><font color=#333333><b>功能菜单</b><BR>为了不打扰用户，在非必要情况下，尽量不要使用此功能</font>  </td>
 </tr>
 <tr  bgcolor="#ffffff"> 
 <td align="center"><BR><SELECT name=action style="WIDTH: 250px">
 <OPTION selected value="compose">编辑并发送邮件</OPTION>
 <OPTION value="view">已退出邮件用户列表</OPTION>
 <OPTION value="footer">查看／编辑页脚</OPTION>
 </SELECT>
 <BR>
 <BR>
 </td>
 </tr>
 <tr> 
 <td colspan="2" width="100%" bgcolor=#eeeeee align=center>
 <input type="submit" name="Button" value="确 定">
 </td>
 </tr>
~;
    &displayoutput;

}

sub composemail {

    $output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>编辑要发送的邮件</td>
 </tr>
 <tr bgcolor="#FFFFFF" valign=top> 
 <td>
 <b>主题：</b>
 </td>
 <td>
 <input type="text" name="subjekt">
 </td>
 </tr>
 <tr bgcolor="#FFFFFF" valign=top> 
 <td width="40%">
 <b>内容：</b>
 </td>
 <td width="60%">
 <textarea size=20 name="text" cols="60" rows="10"></textarea>
 <br>
 </td>
 </tr>
 <tr> 
 <td colspan="2" align="center" width="100%" bgcolor=#EEEEEE>
 <SELECT name="sendto" style="HEIGHT: 22px; WIDTH: 148px"> 
 <OPTION selected value="members">所有注册用户</OPTION>
 <OPTION value="moderators">论坛所有版主</OPTION>
 </SELECT>
 &nbsp;
 <input type=hidden name="action" value="send">
 <input type="submit" name="Button" value="确 定">　<input type="reset" name="Button" value="重 置">
 </td>
 </tr>
~;
    &displayoutput;

}

sub sendmymail {

    if (($message eq "") || ($subjekt eq "")) {

        $output = qq~
  <tr>
  <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>出错。。。</td>
  </tr>
  <tr>
  <td width="100%" align="center">
  <br><br>
  <font color="#FF0000">请输入主题和邮件内容</font><br>
  <a href="$thisprog?action=compose">按此返回</a>
  </tr>
  <tr>
  ~;
        &displayoutput
    }

    $filetoopen = "$lbdir" . "data/footer.cgi";
    open(FILE, "<$filetoopen");
    flock(FILE, 2);
    @footerin = <FILE>;
    close(FILE);

    $footer = "\n";
    foreach $line (@footerin) {
        chomp($line);
        if ($line ne "") {
            $footer .= "$line\n";
        }
    }

    $filetoopen = "$lbdir" . "data/remmem.cgi";
    open(FILE, "<$filetoopen");
    flock(FILE, 2);
    @members = <FILE>;
    close(FILE);

    if ($sendto eq "members") {
        &sendmembers
    }
    elsif ($sendto eq "moderators") {
        &sendmoderators
    }
    else {
        &composemail
    }
}

sub mailsent {

    $output = qq~
 <tr>
 <br><br><td bgcolor=#eeeeee colspan=2><font color=#333333><b>群发 Email</b></font>  </td>
 </tr>
 <tr  bgcolor="#ffffff">
 <Td align="center">
 邮件已经发送给了 $membercount 个用户了。
 </td>
 </tr>
 <tr>
 <td colspan="2" width="100%" bgcolor=#eeeeee>
 <input type="submit" name="Button" value="返 回">
 </td>
 </tr>
 ~;
    &displayoutput;

}

sub sendmembers {
    $mail = "";
    open(MEMFILE, "${lbdir}data/lbmember.cgi");
    flock(MEMFILE, 1) if ($OS_USED eq "Unix");
    @cgi = <MEMFILE>;
    close(MEMFILE);

    $membercount = 0;
    foreach $member (@cgi) {
        @memberdaten = split(/\t/, $member);
        $mail = $memberdaten[4];

        $checkmember = 1;
        foreach $remmember (@members) {
            chomp($remmember);
            if ($remmember eq $memberdaten[0]) {$checkmember = 0;}
        }
        if ($checkmember == 1 && $mail ne "") {
            $membercount++;
        }
    }
    &mailsent;

    if ($UNIX) {
        my $pid = fork();
        if (defined $pid) {
            if ($pid > 0) {
                exit;
            }
            else {
                close(STDOUT);
                &mailall;
                exit;
            }
        }
        else {
            &mailall;
            exit;
        }
    }
    else {
        close(STDOUT);
        &mailall;
        exit;
    }

}

sub mailall {
    ####
    foreach $member (@cgi) {
        @memberdaten = split(/\t/, $member);
        $mail = $memberdaten[4];

        $checkmember = 1;
        foreach $remmember (@members) {
            chomp($remmember);
            if ($remmember eq $memberdaten[0]) {$checkmember = 0;}
        }
        if ($checkmember == 1 && $mail ne "") {
            &gosend;
        }
    }
    ####

}

sub sendmoderators {
    $mail = "";
    open(MEMFILE, "${lbdir}data/lbmember.cgi");
    flock(MEMFILE, 1) if ($OS_USED eq "Unix");
    @cgi = <MEMFILE>;
    close(MEMFILE);

    $membercount = 0;
    foreach $member (@cgi) {
        @memberdaten = split(/\t/, $member);
        $mail = $memberdaten[4];
        if (($memberdaten[1] eq "ad") || ($memberdaten[1] eq 'smo') || ($memberdaten[1] eq "cmo") || ($memberdaten[1] eq "amo") || ($memberdaten[1] eq "mo")) {

            $checkmember = 1;
            foreach $remmember (@members) {
                chomp($remmember);
                if ($remmember eq $memberdaten[0]) {$checkmember = 0;}
            }
            if ($checkmember == 1 && $mail ne "") {
                $membercount++;
            }
        }
    }
    &mailsent;

    if ($UNIX) {
        my $pid = fork();
        if (defined $pid) {
            if ($pid > 0) {
                exit;
            }
            else {
                close(STDOUT);
                &mailm;
                exit;
            }
        }
        else {
            &mailm;
            exit;
        }
    }
    else {
        close(STDOUT);
        &mailm;
        exit;
    }
}

sub mailm {
    ####
    foreach $member (@cgi) {
        @memberdaten = split(/\t/, $member);
        $mail = $memberdaten[4];
        if (($memberdaten[1] eq "ad") || ($memberdaten[1] eq 'smo') || ($memberdaten[1] eq "cmo") || ($memberdaten[1] eq "amo") || ($memberdaten[1] eq "mo")) {

            $checkmember = 1;
            foreach $remmember (@members) {
                chomp($remmember);
                if ($remmember eq $memberdaten[0]) {$checkmember = 0;}
            }
            if ($checkmember == 1 && $mail ne "") {
                &gosend;
            }
        }
    }
    ####

}

sub gosend {
    $mymessage = "$message\n<br><br>\n$footer\n<br><br>\n如果以后不想收到类似的信件，请点击下面的链接：<br>\n$boardurl/remmail.cgi?member=$memberdaten[0]<br>\n.\n";
    &sendmail($adminemail_out, $adminemail_in, $mail, $subjekt, $mymessage);
}

sub view {

    $filetoopen = "$lbdir" . "data/remmem.cgi";
    open(FILE, "<$filetoopen");
    flock(FILE, 2);
    @members = <FILE>;
    close(FILE);

    $memberoutput = "\n";
    foreach $member (@members) {
        chomp($member);
        if ($member ne "") {
            $memberoutput .= "$member\n";
        }
    }

    $output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>已退出邮件用户列表</td>
 </tr>
 <tr bgcolor="#FFFFFF">
 <td align="center">
 <center>
 <TEXTAREA style="WIDTH: 200px; HEIGHT: 400px" name=membersnames rows=29 cols=25>$memberoutput</TEXTAREA>
 </center>
 </td>
 </tr>
 <tr>
 <td align="center" width="100%" bgcolor=#EEEEEE>
 &nbsp;
 <input type="hidden" name="action" value="Update">
 <input type="submit" value="保 存">
 </td>
 </tr>
~;
    &displayoutput;

}

sub update {

    @membersname = split(" ", $membersnamesin);

    foreach $membername (@membersname) {
        chomp($membername);
        if ($membername ne "") {
            chomp($membername);
            $membersnames .= "$membername\n";
        }
    }

    $filetoopen = "$lbdir" . "data/remmem.cgi";
    open(FILE, ">$filetoopen");
    flock(FILE, 2);
    print FILE "$membersnames";
    close(FILE);

    $output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>已退出邮件用户列表</td>
 </tr>
 <tr bgcolor="#FFFFFF">
 <td align="center">
 <center>
 所有数据已经保存
 </center>
 </td>
 </tr>
 <tr>
 <td align="center" width="100%" bgcolor=#EEEEEE>
 &nbsp;
 <input type="submit" name="Button" value="返 回">
 </td>
 </tr>
~;
    &displayoutput;
}

sub viewfoot {
    $filetoopen = "$lbdir" . "data/footer.cgi";
    open(FILE, "<$filetoopen");
    flock(FILE, 2);
    @footer = <FILE>;
    close(FILE);
    $footeroutput = "";
    foreach $line (@footer) {
        chomp($line);
        if ($line ne "") {
            $footeroutput .= "$line\n";
        }
    }

    $output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>编辑页脚</td>
 </tr>
 <tr bgcolor="#FFFFFF">
 <td align="center">
 <center>
 <TEXTAREA style="WIDTH: 400px; HEIGHT: 100px" name=footerline rows=29 cols=25>$footeroutput</TEXTAREA>
 </center>
 </td>
 </tr>
 <tr>
 <td align="center" width="100%" bgcolor=#EEEEEE>
 &nbsp;
 <input type="hidden" name="action" value="Save">
 <input type="submit" value="保 存">
 </td>
 </tr>
~;
    &displayoutput;

}

sub updatefoot {

    @footerline = split("\n", $footerlinein);

    foreach $line (@footerline) {
        chomp($line);
        if ($line ne "") {
            chomp($line);
            $footerlines .= "$line\n";
        }
    }

    $filetoopen = "$lbdir" . "data/footer.cgi";
    open(FILE, ">$filetoopen");
    flock(FILE, 2);
    print FILE "$footerlines";
    close(FILE);

    $output = qq~
 <tr>
 <br><br><td bgcolor=#EEEEEE align="center" colspan=2><font color=#333333><b>更新页脚完成</td>
 </tr>
 <tr bgcolor="#FFFFFF">
 <td align="center">
 <center>
 信息已经保存
 </center>
 </td>
 </tr>
 <tr>
 <td align="center" width="100%" bgcolor=#EEEEEE>
 &nbsp;
 <input type="submit" name="Button" value="返 回">
 </td>
 </tr>
~;
    &displayoutput;
}

sub displayoutput {

    print qq~
 <form action="$thisprog" method="post">
 <table border="0" align="center" width="456">
 $output
 </table>
 </form>
 </table>
 </body>
 </html>
~;
}
