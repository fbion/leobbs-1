#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use strict;
use warnings;
use diagnostics;

$ingetpassq = &cleaninput($query->param("getpassq"));
$ingetpassa = &cleaninput($query->param("getpassa"));

$inmembernamefile = $inmembername;
$inmembernamefile =~ s/ /\_/g;
$inmembernamefile =~ tr/A-Z/a-z/;

opendir(DIRS, "${lbdir}$msgdir");
my @files = readdir(DIRS);
closedir(DIRS);
@files = grep (/\.cgi$/i, @files);
foreach (@files) {unlink("${lbdir}$msgdir/$_") if ((-M "${lbdir}$msgdir/$_") > 1);}

if (-e "${lbdir}$msgdir/$inmembernamefile.cgi") {
    &error("密码获得失败&请不要重复获取密码，论坛规定用户每１５分钟才能取得密码一次！") if ((-M "${lbdir}$msgdir/$inmembernamefile.cgi") * 86400 < 900);
}

if ($password ne "") {
    if (-e "${lbdir}$msgdir/$inmembernamefile.cgi") {
        open(FILE, "${lbdir}$msgdir/$inmembernamefile.cgi");
        $x = <FILE>;
        close(FILE);
        chomp $x;
    }
    else {
        $x = &myrand(1000000000);
        $x = crypt($x, aun);
        $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
        $x =~ s/[^\w\d]//g;
        $x = substr($x, 2, 6);
    }
    open(FILE, ">${lbdir}$msgdir/$inmembernamefile.cgi");
    print FILE "$x";
    close(FILE);
    $password = "$x$password";
    eval {$password = md5_hex($password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$password = md5_hex($password);');}
}
else {&error("密码获得失败&你的密码资料已经丢失，请联系管理员修复！");}

if (($membercode eq "ad") || ($membercode eq "smo")) {require "doblocked.pl";}
elsif (($ingetpassq ne "") && ($ingetpassa ne "")) {
    my ($getpassq, $getpassa) = split(/\|/, $userquestion);
    if (($ingetpassq eq $getpassq) && ($ingetpassa eq $getpassa) && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode ne "cmo")) {
        $inmembername1 = uri_escape($inmembername);
        $output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>你好，$inmembername</b></font></td></tr> 
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>应您的要求，现将您的论坛密码获取方式给您！</td></tr> 
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc> 
您的用户名称：$inmembername<br><br><B><a href="$boardurl/getmypass.cgi?username=$inmembername1&password=$password">请按此获得您的论坛密码</a></B><br><br>
注意：此链接在一天后失效，请尽快访问并进行密码修改。<BR><BR>
</td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><BR><BR>
~;
    }
    else {
        $output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>非常抱歉，$inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>
你所输入的论坛密码提示问题和答案不正确，或是你没有在个人资料中填写，所以无法取回！ (注：如果你是斑竹，出于安全考虑，请用邮件取回论坛密码！)
</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
        unlink("${lbdir}$msgdir/$inmembernamefile.cgi");
    }
}
elsif ($emailfunctions eq "off") {
    $output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>非常抱歉，$inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>
由于这个论坛的发送邮件功能已经关闭，请通过另外的途径来联系坛主而拿取您的论坛密码！
</td></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
}
elsif ($userregistered ne "no") {
    $inmembername1 = uri_escape($inmembername);
    eval("use MAILPROG qw(sendmail);");
    $message .= "\n";
    $message .= "$boardname <br>\n";
    $message .= "$boardurl/leobbs.cgi \n<br><br>\n";
    $message .= "------------------------------------------------<br>\n";
    $message .= "应您的要求，现将您的论坛密码获取方式寄给您！\n <br><br>\n";
    $message .= "您的用户名：$inmembername <br>\n";
    $message .= "您的论坛密码按此获得： $boardurl/getmypass.cgi?username=$inmembername1&password=$password \n <br><br>\n";
    $message .= "注意：此链接在一天后失效，请尽快访问并进行密码修改。<br><br>\n";
    $message .= "------------------------------------------------<br>\n";
    $to = $emailaddress;
    $from = $adminemail_out;
    $subject = "忘记论坛密码[$boardname]";
    if (&sendmail($from, $from, $to, $subject, $message)) {
        $output =~ s/用户资料/论坛密码已经寄出/g;
        $output .= qq~
<tr><td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>你好，$inmembername</b></font></td></tr>
<tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc>您的论坛密码获取方式已经成功的通过指定的邮件地址发送给您了。</td></tr></table></td></tr></table>
~;
    }
    else {
        &error("密码邮递失败&似乎服务器发送邮件过程中出了一些问题，请稍后重试。");
    }
}
else {
    &error("请求论坛密码&错误，您不是注册用户！");
}
1;
