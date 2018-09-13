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
$LBCGI::POST_MAX = 1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
use MAILPROG qw(sendmail);
require "data/boardinfo.cgi";
require "data/cityinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "register.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

if ($COOKIE_USED eq 2 && $mycookiepath ne "") {$cookiepath = $mycookiepath;}
elsif ($COOKIE_USED eq 1) {$cookiepath = "";}
else {
    $boardurltemp = $boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
    #    $cookiepath =~ tr/A-Z/a-z/;
}

$addme = $query->param('addme');

$in_forum = $query->param('forum');
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));

&ipbanned; #封杀一些 ip

if ($arrowavaupload ne "on") {undef $addme;}
$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

if ($regonoff == 2) {
    $regonoff = 1;
    $regonoffinfo = "1";
    my (undef, undef, $hour, $mday, undef, undef, $wday, undef) = localtime(time + $timezone * 3600);
    $regautovalue =~ s/[^\d\-]//sg;
    my ($starttime, $endtime) = split(/-/, $regautovalue);
    if ($regauto eq "day") {
        $regonoff = 0 if ($hour == $starttime && $endtime eq "");
        $regonoff = 0 if ($hour >= $starttime && $hour < $endtime);
    }
    elsif ($regauto eq "week") {
        $wday = 7 if ($wday == 0);
        $regonoff = 0 if ($wday == $starttime && $endtime eq "");
        $regonoff = 0 if ($wday >= $starttime && $wday <= $endtime);
    }
    elsif ($regauto eq "month") {
        $regonoff = 0 if ($mday == $starttime && $endtime eq "");
        $regonoff = 0 if ($mday >= $starttime && $mday <= $endtime);
    }
}
if ($regonoff == 1) {
    $in_member_name = $query->cookie("amembernamecookie");
    $in_password = $query->cookie("apasswordcookie");
    $in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\|\'\:\"\,\.\/\<\>\?]//isg;
    $in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
    unless ($in_member_name eq "" || $in_member_name eq "客人") {
        &getmember("$in_member_name");
        &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
        &error("普通错误&论坛密码与用户名不相符，请重新登录！") if ($in_password ne $password);
        $regonoff = 0 if ($member_code eq "ad");
    }
}

for ('inmembername', 'password', 'password2', 'emailaddress', 'showemail', 'homepage', 'oicqnumber', 'icqnumber', 'newlocation', 'recommender',
    'interests', 'signature', 'timedifference', 'useravatar', 'action', 'personalavatar', 'personalwidth', 'personalheight', 'mobilephone',
    'sex', 'education', 'marry', 'work', 'year', 'month', 'day', 'userflag', 'userxz', 'usersx') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &unHTML("$tp");
    ${$_} = $tp;
}
$recommender =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\|\'\:\"\,\.\/\<\>\?]//isg;

&error("论坛密码提示问题和答案&论坛密码提示问题和答案中，不允许有非法字符，请更换提问和答案！") if ($query->param('getpassq') =~ /[\||\a|\f|\n|\e|\0|\r|\t]/ || $query->param('getpassa') =~ /[\||\a|\f|\n|\e|\0|\r|\t]/);
$userquestion = $query->param('getpassq') . "|" . $query->param('getpassa');
$userquestion = "" if ($passwordverification eq "yes" && $emailfunctions ne "off");

$helpurl = &helpfiles("用户注册");
$helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

if ($arrawsignpic eq "on") {$signpicstates = "允许";}
else {$signpicstates = "禁止";}
if ($arrawsignflash eq "on") {$signflashstates = "允许";}
else {$signflashstates = "禁止";}
if ($arrawsignfontsize eq "on") {$signfontsizestates = "允许";}
else {$signfontsizestates = "禁止";}
if ($arrawsignsound eq "on") {$signsoundstates = "允许";}
else {$signsoundstates = "禁止";}

&mischeader("用户注册");
$output .= qq~<p><SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
~;

if ($regonoff eq 1) {
    if ($regonoffinfo eq "1") {
        if ($regauto eq "day") {$regauto = "每天";}
        elsif ($regauto eq "week") {$regauto = "每周";}
        elsif ($regauto eq "month") {$regauto = "每月";}
        $regauto = "，开放注册时间：$regauto $regautovalue ！";
    }
    else {$regauto = "";}

    $output .= qq~<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>对不起，论坛目前暂时不允许注册新用户$regauto</b>
    </td></tr><td bgcolor=$miscbackone align=center><font color=$fontcolormisc size=3><BR><BR>~;
    if ($noregwhynot ne "") {
        $noregwhynot = &HTML($noregwhynot);
        $noregwhynot =~ s/\n/<BR>/isg;
        $output .= qq~$noregwhynot~;
    }
    else {$output .= qq~由于一些特殊的原因，本论坛暂时不接受用户注册！~;}
    $output .= qq~<BR><BR><BR></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
}
elsif ($action eq "addmember") {
    &error("出错&请不要用外部连接本程序！") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '') && ($canotherlink ne "yes"));
    $member_code = "me";
    $membertitle = "Member";
    $numberofposts = "0|0";
    $joineddate = time;
    $lastgone = $joineddate;
    $mymoney = $joinmoney;
    $jifen = $joinjf;
    $jhmp = "无门无派";
    $lastpostdate = "没有发表过";
    $emailaddress = lc($emailaddress);

    if (($in_member_name eq "") || ($emailaddress eq "")) {
        &error("用户注册&请输入用户名和邮件地址，这些是必需的！");
    }

    $ipaddress = $ENV{'REMOTE_ADDR'};
    my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress =~ m/a-z/i || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 !~ m/a-z/i && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
    $ipaddress = $trueipaddress;
    $year =~ s/\D//g;
    $year = "19$year" if ($year < 1900 && $year ne "");
    my (undef, undef, undef, undef, undef, $yeartemp, undef, undef) = localtime(time + $timezone * 3600);
    $yeartemp = 1900 + $yeartemp if ($yeartemp < 1900);
    if ($year ne "") {
        &error("用户注册&请正确输入你的出生年份！") if ($year <= 1900 || $year >= $yeartemp - 3);
    }
    if (($year eq "") || ($month eq "") || ($day eq "")) {
        $year = "";
        $month = "";
        $day = "";
    }
    $born = "$year/$month/$day";

    if ($born ne "//") { #开始自动判断星座
        if ($month eq "01") {
            if (($day >= 1) && ($day <= 19)) {$userxz = "z10";}
            else {$userxz = "z11";}
        }
        elsif ($month eq "02") {
            if (($day >= 1) && ($day <= 18)) {$userxz = "z11";}
            else {$userxz = "z12";}
        }
        elsif ($month eq "03") {
            if (($day >= 1) && ($day <= 20)) {$userxz = "z12";}
            else {$userxz = "z1";}

        }
        elsif ($month eq "04") {
            if (($day >= 1) && ($day <= 19)) {$userxz = "z1";}
            else {$userxz = "z2";}
        }
        elsif ($month eq "05") {
            if (($day >= 1) && ($day <= 20)) {$userxz = "z2";}
            else {$userxz = "z3";}
        }
        elsif ($month eq "06") {
            if (($day >= 1) && ($day <= 21)) {$userxz = "z3";}
            else {$userxz = "z4";}
        }
        elsif ($month eq "07") {
            if (($day >= 1) && ($day <= 22)) {$userxz = "z4";}
            else {$userxz = "z5";}
        }
        elsif ($month eq "08") {
            if (($day >= 1) && ($day <= 22)) {$userxz = "z5";}
            else {$userxz = "z6";}
        }
        elsif ($month eq "09") {
            if (($day >= 1) && ($day <= 22)) {$userxz = "z6";}
            else {$userxz = "z7";}
        }
        elsif ($month eq "10") {
            if (($day >= 1) && ($day <= 23)) {$userxz = "z7";}
            else {$userxz = "z8";}
        }
        elsif ($month eq "11") {
            if (($day >= 1) && ($day <= 21)) {$userxz = "z8";}
            else {$userxz = "z9";}
        }
        elsif ($month eq "12") {
            if (($day >= 1) && ($day <= 21)) {$userxz = "z9";}
            else {$userxz = "z10";}
        }
    }

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
            &error("用户注册&对不起，这输入的 Email 已经被注册用户：<u>$1</u> 使用了");
        }
    }

    #邮件限制 _S
    my $allow_eamil_file = "$lbdir" . "data/allow_email.cgi";
    if (-e $allow_eamil_file) {
        open(AEFILE, $allow_eamil_file);
        my $allowtype = <AEFILE>;
        my $allowmail = <AEFILE>;
        close(AEFILE);
        chomp $allowtype;
        chomp $allowmail;
        my $check_result = 0;
        my $get_email_server = substr($emailaddress, rindex($emailaddress, '@') + 1);
        if ($allowmail ne "") {
            my @allowmail = split(/\t/, $allowmail);
            chomp @allowmail;
            foreach (@allowmail) {
                next if ($_ eq "");
                if (lc($get_email_server) eq lc($_)) {
                    $check_result = 1;
                    last;
                }
            }
            if ($allowtype eq "allow") {
                if ($check_result == 0) {
                    &error("用户注册&必需使用指定的邮箱才能注册！<a href=\"javascript:openScript('dispemail.cgi',200,300);\">[列表]</a>");
                }
            }
            else {
                if ($check_result == 1) {
                    &error("用户注册&您提供的邮箱被禁止使用注册！<a href=\"javascript:openScript('dispemail.cgi',200,300);\">[列表]</a>");
                }
            }
        }
    }
    #邮件限制 _E

    &error("用户注册&对不起，您输入的用户名有问题，请不要在用户名中包含\@\#\$\%\^\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]\|这类字符！") if ($in_member_name =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\|\;\'\:\"\,\.\/\<\>\?\[\]]/);
    if ($in_member_name =~ /_/) {&error("用户注册&请不要在用户名中使用下划线！");}

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
    $in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\|\'\:\"\,\.\/\<\>\?\[\]]//isg;
    $in_member_name =~ s/\s*$//g;
    $in_member_name =~ s/^\s*//g;

    &error("用户注册&对不起，您输入的用户名有问题，请更换一个") if ($in_member_name =~ /^q(.+?)-/ig || $in_member_name =~ /^q(.+?)q/ig);

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

    $bannedmember = "yes" if (($in_member_name =~ /^m-/i) || ($in_member_name =~ /^s-/i) || ($in_member_name =~ /tr-/i) || ($in_member_name =~ /^y-/i) || ($in_member_name =~ /注册/i) || ($in_member_name =~ /guest/i) || ($in_member_name =~ /qq-/i) || ($in_member_name =~ /qq/i) || ($in_member_name =~ /qw/i) || ($in_member_name =~ /q-/i) || ($in_member_name =~ /qx-/i) || ($in_member_name =~ /qw-/i) || ($in_member_name =~ /qr-/i) || ($in_member_name =~ /^全体/i) || ($in_member_name =~ /register/i) || ($in_member_name =~ /诚聘中/i) || ($in_member_name =~ /斑竹/i) || ($in_member_name =~ /管理系统讯息/i) || ($in_member_name =~ /leobbs/i) || ($in_member_name =~ /leoboard/i) || ($in_member_name =~ /雷傲/i) || ($in_member_name =~ /LB5000/i) || ($in_member_name =~ /全体管理人员/i) || ($in_member_name =~ /管理员/i) || ($in_member_name =~ /隐身/i) || ($in_member_name =~ /短消息广播/i) || ($in_member_name =~ /暂时空缺/i) || ($in_member_name =~ /＊＃！＆＊/i) || ($in_member_name =~ /版主/i) || ($in_member_name =~ /坛主/i) || ($in_member_name =~ /nodisplay/i) || ($in_member_name =~ /^system/i) || ($in_member_name =~ /---/i) || ($in_member_name eq "admin") || ($in_member_name eq "root") || ($in_member_name eq "copy") || ($in_member_name =~ /^sub/) || ($in_member_name =~ /^exec/) || ($in_member_name =~ /\@ARGV/i) || ($in_member_name =~ /^require/) || ($in_member_name =~ /^rename/i) || ($in_member_name =~ /^dir/i) || ($in_member_name =~ /^print/i) || ($in_member_name =~ /^con/i) || ($in_member_name =~ /^nul/i) || ($in_member_name =~ /^aux/i) || ($in_member_name =~ /^com/i) || ($in_member_name =~ /^lpt/i) || ($in_member_name =~ /^open/i));

    if ($bannedmember eq "yes") {&error("用户注册&不允许注册，你填写的用户名、Email 或当前的 IP 被管理員设置成禁止注册新用户了，请更换或者联系管理員以便解决！");}

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
    &error("用户注册&对不起，你所注册的用户名已经被保留或者被禁止注册，请更换一个用户名！") if ($noreg eq "yes");

    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
        $seed = int(myrand(100000));
        $password = crypt($seed, aun);
        $password =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        $password =~ s/[^a-zA-Z0-9]//isg;
        $password = substr($password, 4, 8);
    }

    if ($interests) {
        $interests =~ s/[\t\r]//g;
        $interests =~ s/  / /g;
        $interests =~ s/\n\n/\<p\>/g;
        $interests =~ s/\n/\<br\>/g;
    }

    if ($signature) {
        $signature =~ s/[\t\r]//g;
        $signature =~ s/  / /g;
        $signature =~ s/\n\n/\n\&nbsp;\n/isg;
        $signature =~ s/\n/\[br\]/isg;
        $signature =~ s/\[br\]\[br\]/\[br\]\&nbsp;\[br\]/isg;
        $signature = &dofilter("$signature");
        $signature =~ s/(ev)a(l)/$1&#97;$2/isg;
    }

    my @testsig = split(/\[br\]/, $signature);
    my $siglines = @testsig;

    if ($siglines > $maxsignline) {&error("用户注册&对不起，在您的签名中只允许有 $maxsignline 行！");}
    if (length($signature) > $maxsignlegth) {&error("用户注册&对不起，签名不能超过 $maxsignlegth 字符！");}

    my @testins = split(/\<br\>/, $interests);
    my $inslines = @testins;
    if ($inslines > $maxinsline) {&error("用户注册&对不起，个人简介只允许有 $maxinsline 行！");}
    if (length($interests) > $maxinslegth) {&error("用户注册&对不起，个人简介不能超过 $maxinslegth 字符！");}

    if (($personalavatar) && ($personalwidth) && ($personalheight)) {
        if ($personalavatar !~ /^http:\/\/[\w\W]+\.[\w\W]+$/) {&error("用户注册&自定义头像的 URL 地址有问题！");}
        if (($personalavatar !~ /\.gif$/isg) && ($personalavatar !~ /\.jpg$/isg) && ($personalavatar !~ /\.png$/isg) && ($personalavatar !~ /\.bmp$/isg)) {&error("用户注册&自定义头像必须为 PNG、GIF 或 JPG 格式");}
        if (($personalwidth < 20) || ($personalwidth > $maxposticonwidth)) {&error("用户注册&对不起，您填写的自定义图像宽度必须在 20 -- $maxposticonwidth 像素之间！");}
        if (($personalheight < 20) || ($personalheight > $maxposticonheight)) {&error("用户注册&对不起，您填写的自定义图像高度必须在 20 -- $maxposticonheight 像素之间！");}
        $useravatar = "noavatar";
        $personalavatar =~ s/${imagesurl}/\$imagesurl/o;
    }
    else {
        if ($addme) {$personalavatar = "";}
        else {
            $personalavatar = "";
            $personalwidth = "";
            $personalheight = "";
        }
    } #清除自定义头像信息

    if ($in_member_name =~ /\t/) {&error("用户注册&请不要在用户名中使用特殊字符！");}
    if ($password =~ /[^a-zA-Z0-9]/) {&error("用户注册&论坛密码只允许大小写字母和数字的组合！！");}
    if ($password =~ /^lEO/) {&error("用户注册&论坛密码不允许是 lEO 开头，请更换！！");}

    $recomm_q = $recommender;
    $recomm_q =~ y/ /_/;
    $recomm_q =~ tr/A-Z/a-z/;
    $member_q = $in_member_name;
    $member_q =~ y/ /_/;
    $member_q =~ tr/A-Z/a-z/;
    if ($recomm_q eq $member_q) {&error("用户注册&您不能推荐自己！");}

    $tempinmembername = $in_member_name;
    $tempinmembername =~ s/ //g;
    $tempinmembername =~ s/　//g;
    if ($tempinmembername eq "") {&error("用户注册&你的用户名有点问题哟，换一个！");}
    if ($in_member_name =~ /^客人/) {&error("用户注册&请不要在用户名的开头中使用客人字样！");}
    if (length($in_member_name) > 12) {&error("用户注册&用户名太长，请不要超过12个字符（6个汉字）！");}
    if (length($in_member_name) < 2) {&error("用户注册&用户名太短了，请不要少於2个字符（1个汉字）！");}
    if (length($newlocation) > 16) {&error("用户注册&来自地区过长，请不要超过16个字符（8个汉字）！");}

    if (($in_member_name =~ m/_/) || (!$in_member_name)) {&error("用户注册&用户名中含有非法字符！");}

    if ($passwordverification eq "no") {
        if ($password ne $password2) {&error("用户注册&对不起，你输入的两次论坛密码不相同！");}
        if (length($password) < 8) {&error("用户注册&论坛密码太短了，请更换！论坛密码必须 8 位以上！");}
        #       if ($password =~ /^[0-9]+$/) { &error("用户注册&论坛密码请不要全部为数字，请更换！"); }
    }

    if ($in_member_name eq $password) {&error("用户注册&请勿将用户名和论坛密码设置成相同！");}

    if ($emailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) {&error("用户注册&邮件地址错误！");}
    $emailaddress =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    $homepage =~ s/[\ \a\f\n\e\0\r\t\|\$\@]//isg;
    $homepage =~ s/ARGV//isg;
    $homepage =~ s/system//isg;

    &getmember("$in_member_name", "no");
    if ($userregistered ne "no") {&error("用户注册&该用户已经存在，请重新输入一个新的用户名！");}
    $member_code = "me";

    $memberfiletitle = $in_member_name;
    $memberfiletitle =~ y/ /_/;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitletemp = unpack("H*", "$memberfiletitle");
    if ($addme) {

        my ($file_name) = $addme =~ m|([^/:\\]+)$|; #注意,获取文件名字的形式变化
        my $fileexp;

        $fileexp = ($file_name =~ /\.jpe?g\s*$/i) ? 'jpg'
            : ($file_name =~ /\.gif\s*$/i) ? 'gif'
            : ($file_name =~ /\.png\s*$/i) ? 'png'
            : ($file_name =~ /\.swf\s*$/i) ? 'swf'
            : ($file_name =~ /\.bmp\s*$/i) ? 'bmp'
            : undef;
        $maxuploadava = 200 if (($maxuploadava eq "") || ($maxuploadava < 1));

        if (($fileexp eq "swf") && ($flashavatar ne "yes")) {&error("不支持你所上传的图片，请重新选择！&仅支持 GIF，JPG，PNG，BMP 类型!");}
        if (!defined $fileexp) {&error("不支持你所上传的图片，请重新选择！&仅支持 GIF，JPG，PNG，BMP，SWF 类型!");}

        my $filesize = 0;
        my $buffer;
        open(FILE, ">${imagesdir}/usravatars/$memberfiletitletemp.$fileexp");
        binmode(FILE);
        binmode($addme); #注意
        while (((read($addme, $buffer, 4096))) && !($filesize > $maxuploadava)) {
            print FILE $buffer;
            $filesize = $filesize + 4;
        }
        close(FILE);
        close($addme);

        if ($fileexp eq "gif" || $fileexp eq "jpg" || $fileexp eq "bmp" || $fileexp eq "jpeg" || $fileexp eq "png") {
            eval("use Image::Info qw(image_info);");
            if ($@ eq "") {
                my $info = image_info("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
                if ($info->{error} eq "Unrecognized file format") {
                    unlink("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
                    &error("上传出错&上传文件不是图片文件，请上传标准的图片文件！");
                }
                if ($personalwidth eq "" || $personalwidth eq 0) {
                    if ($info->{width} ne "") {$personalwidth = $info->{width};}
                    elsif ($info->{ExifImageWidth} ne "") {$personalwidth = $info->{ExifImageWidth};}
                }
                if ($personalheight eq "" || $personalheight eq 0) {
                    if ($info->{height} ne "") {$personalheight = $info->{height};}
                    elsif ($info->{ExifImageLength} ne "") {$personalheight = $info->{ExifImageLength};}
                }
                undef $info;
            }
        }
        if ($filesize > $maxuploadava) {
            unlink("${imagesdir}usravatars/$memberfiletitletemp.$fileexp");
            &error("上传出错&上传文件大小超过$maxuploadava，请重新选择！");
        }

        if (($personalwidth < 20) || ($personalwidth > $maxposticonwidth)) {&error("用户注册&对不起，您填写的自定义图像宽度($personalwidth)必须在 20 -- $maxposticonwidth 像素之间！");}
        if (($personalheight < 20) || ($personalheight > $maxposticonheight)) {&error("用户注册&对不起，您填写的自定义图像高度($personalheight)必须在 20 -- $maxposticonheight 像素之间！");}

        $useravatar = "noavatar";
        $personalavatar = "\$imagesurl/usravatars/$memberfiletitletemp.$fileexp";
    }
    if ($useverify eq "yes") {
        &error("用户注册&对不起，你输入的校验码有问题或者已经过期！") if (&checkverify);
    }

    $regcontrollimit = 30 if (($regcontrollimit eq "") || ($regcontrollimit < 0));
    $regcontrol = 0;

    $filetoopen = "$lbdir" . "data/lastregtime.cgi";
    if (-e "$filetoopen") {
        open(FILE, "$filetoopen");
        my $lastfiledate = <FILE>;
        close(FILE);
        chomp $lastfiledate;
        my ($lastregtime, $lastregip) = split(/\|/, $lastfiledate);
        $lastregtime = $lastregtime + $regcontrollimit;
        if (($lastregtime > $joineddate) && ($ipaddress eq $lastregip)) {$regcontrol = 1;}
    }
    open(FILE, ">$filetoopen");
    print FILE "$joineddate|$ipaddress";
    close(FILE);

    if ($regcontrol eq 1) {&error("用户注册&对不起，您必须等待 $regcontrollimit 秒钟才能再次注册！");}

    if ($adminverification eq "yes") {
        $emailaddress1 = $emailaddress;
        $emailaddress = $adminemail_out;
    }

    if ($password ne "") {
        $notmd5password = $password;
        eval {$password = md5_hex($password);};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$password = md5_hex($password);');}
        unless ($@) {$password = "lEO$password";}
    }
    else {
        $notmd5password = $password;
    }

    $signature =~ s/\n/<br>/g;
    require "dosignlbcode.pl";
    $signature1 = &signlbcode($signature);
    $signature = $signature . "aShDFSiod" . $signature1;
    mkdir("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod(0777, "${lbdir}$memdir/old");
    my $namenumber = &getnamenumber($memberfiletitle);
    $filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
    if (open(FILE, ">$filetomake")) {
        print FILE "$in_member_name\t$password\t$membertitle\t$member_code\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$useradd04\t$useradd02\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t$jifen\t\t$soccerdata\t0\t";
        close(FILE);
    }
    $filetomake = "$lbdir" . "$memdir/old/$memberfiletitle.cgi";
    if (open(FILE, ">$filetomake")) {
        print FILE "$in_member_name\t$password\t$membertitle\t$member_code\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$useradd04\t$useradd02\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t$jifen\t\t$soccerdata\t0\t";
        close(FILE);
    }

    if (($recommender ne "") && ($recomm_q ne $member_q)) {
        $recomm_q = &stripMETA($recomm_q);
        $namenumber = &getnamenumber($recomm_q);
        &checkmemfile($recomm_q, $namenumber);
        my $filetoopen = "${lbdir}$memdir/$namenumber/$recomm_q.cgi";
        if (-e $filetoopen) {
            &recommfunc("$recommender");
            $recommfuncerror = "";
        }
        else {$recommfuncerror = " (注意：推荐人用户名不存在！)";}
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

    if (($born ne "") && ($born ne "//")) {
        $filetomakeopen = "${lbdir}data/lbmember3.cgi";
        if (open(MEMFILE, ">>$filetomakeopen")) {
            print MEMFILE "$in_member_name\t$born\t\n";
            close(MEMFILE);
        }
        $month = int($month);
        if (open(MEMFILE, ">>${lbdir}calendar/borninfo$month.cgi")) {
            print MEMFILE "$in_member_name\t$born\t\n";
            close(MEMFILE);
        }
    }

    $filetomakeopen = "${lbdir}data/lbmember4.cgi";
    if (open(MEMFILE, ">>$filetomakeopen")) {
        print MEMFILE "$in_member_name\t$ipaddress\t\n";
        close(MEMFILE);
    }

    $in_member_name =~ y/_/ /;
    $inmemberfile = $in_member_name;
    $inmemberfile =~ y/ /_/;
    $inmemberfile =~ tr/A-Z/a-z/;
    $currenttime = time;
    if ($sendwelcomemessage ne "no" && $allowusemsg ne "off") {
        $filetoopen = "$lbdir" . "data/newusrmsg.dat";
        open(FILE, $filetoopen);
        sysread(FILE, $tempoutput, (stat(FILE))[7]);
        close(FILE);
        $tempoutput =~ s/\r//isg;

        $tempoutput =~ s/\n//;

        $filetoopen = "$lbdir" . "$msgdir/in/$inmemberfile" . "_msg.cgi";
        if (open(FILE, ">$filetoopen")) {
            print FILE "＊＃！＆＊全体管理人员\tno\t$currenttime\t欢迎您访问$board_name，祝你使用愉快！\t$tempoutput<BR><BR>----------------------------<BR>LeoBBS 由雷傲科技荣誉出品<BR>主页:<a href=http://www.LeoBBS.com target=_blank>http://www.LeoBBS.com</a>\n";
            close(FILE);
        }
    }
    ###发送注册信件
    if (($passwordverification eq "no") && ($emailfunctions ne "off")) {
        $to = $emailaddress;
        $from = $adminemail_out;
        $subject = "感谢您在$board_name中注册！";
        $message .= "\n欢迎你加入$board_name! <br>\n";
        $message .= "论坛URL: $boardurl/leobbs.cgi\n <br><br>\n <br>\n";
        $message .= "------------------------------------<br>\n";
        $message .= "您的用户名、论坛密码如下。\n <br>\n";
        $message .= "用户名： $in_member_name <br>\n";
        $message .= "论坛密码： $notmd5password\n <br><br>\n <br>\n";
        $message .= "要注意论坛密码是区分大小写的\n <br>\n";
        $message .= "您随时可以使用用户资料修改您的论坛密码 <br>\n";
        $message .= "如果您改变了您的邮件地址， <br>\n";
        $message .= "将会有一个新的论坛密码寄给您。\n <br><br>\n";
        $message .= "------------------------------------<br>\n";
        &sendmail($from, $from, $to, $subject, $message);
    }
    ####发送注册信件结束

    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/", -expires => "now");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/", -expires => "now");

        if ($adminverification eq "yes") {
            $to = $adminemail_out;
            $from = $emailaddress;
            $subject = "等待您认证$board_name中的注册！";
            $message .= "\n欢迎你加入$board_name！\n";
            $message .= "论坛URL:$boardurl/leobbs.cgi\n\n\n";
            $message .= "------------------------------------\n";
            $message .= "您的用户名、论坛密码如下。\n\n";
            $message .= "用户名： $in_member_name\n";
            $message .= "论坛密码： $notmd5password\n\n\n";
            $message .= "邮  箱： $emailaddress1\n\n\n";
            $message .= "论坛密码是区分大小写的\n\n";
            $message .= "请立即登录并修改信箱(现在信箱是管理员的\n";
            $message .= "信箱)，将会有新的论坛密码直接寄给您。\n\n";
            $message .= "------------------------------------\n";
            $message .= "请回复或转发认证该会员，并要求其修改信箱！\n";
        }
        else {
            $to = $emailaddress;
            $from = $adminemail_out;
            $subject = "感谢您在$board_name中注册！";
            $message .= "\n欢迎你加入$board_name！<br>\n";
            $message .= "论坛URL:$boardurl/leobbs.cgi\n <br><br>\n <br>\n";
            $message .= "------------------------------------<br>\n";
            $message .= "您的用户名、论坛密码如下。\n<br><br>\n";
            $message .= "用户名： $in_member_name <br>\n";
            $message .= "论坛密码： $notmd5password\n <br><br>\n<br>\n";
            $message .= "论坛密码是区分大小写的 \n<br><br>\n";
            $message .= "您随时可以使用用户资料修改您的论坛密码 <br>\n";
            $message .= "如果您改变了您的邮件地址， <br>\n";
            $message .= "将会有一个新的论坛密码寄给您。 <br><br>\n\n";
            $message .= "------------------------------------<br>\n";
        }
        &sendmail($from, $from, $to, $subject, $message);
    }

    if ($newusernotify eq "yes" && $emailfunctions ne "off") {
        $to = $adminemail_in;
        $from = $adminemail_out;
        $subject = "$board_name有新用户注册了！";
        $message = "\n论坛：$board_name <br>\n";
        $message .= "论坛URL:$boardurl/leobbs.cgi <br>\n";
        $message .= "-------------------------------------\n<br><br>\n";
        $message .= "新用户注册的信息如下。 <br><br>\n\n";
        $message .= "用户名： $in_member_name <br>\n";
        $message .= "密  码： $notmd5password <br>\n";
        $message .= "邮  件： $emailaddress <br>\n";
        $message .= "主  页： $homepage <br>\n";
        $message .= "IP地址： $ipaddress\n <br><br>\n";
        $message .= "推荐人： $recommender\n <br><br>\n" if ($recommender ne "");
        $message .= "------------------------------------<br>\n";
        &sendmail($from, $from, $to, $subject, $message);
    }

    if ($in_forum eq "") {$refrashurl = "leobbs.cgi";}
    else {$refrashurl = "forums.cgi?forum=$in_forum";}
    $output .= qq~<tr>
	<td bgcolor=$titlecolor $catbackpic valign=middle align=center><font color=$fontcolormisc><b>感谢您注册，$in_member_name</b>$recommfuncerror</font></td></tr><tr>
        <td bgcolor=$miscbackone valign=middle><font color=$fontcolormisc>具体情况：<ul><li><a href="$refrashurl">按此返回论坛</a>
        <meta http-equiv="refresh" content="3; url=$refrashurl">
	</ul></tr></td></table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;

    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {$output =~ s/按此返回论坛/您的论坛密码已经寄出，按此返回论坛，然后使用邮件中的密码登录/;}
    else {
        $namecookie = cookie(-name => "amembernamecookie", -value => "$in_member_name", -path => "$cookiepath/", -expires => "+30d");
        $passcookie = cookie(-name => "apasswordcookie", -value => "$password", -path => "$cookiepath/", -expires => "+30d");
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
}
elsif ($action eq "agreed") {
    require "cleanolddata.pl";
    &cleanolddata1;
    if (($passwordverification eq "yes") && ($emailfunctions ne "off")) {
        if ($adminverification eq "yes") {
            $requirepass = qq~<tr><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc><b>您的论坛密码将通过邮件寄给管理员，在经过管理员认证后将承认你的注册！</td></tr>~;
        }
        else {
            $requirepass = qq~<tr><td bgcolor=$miscbackone colspan=2 align=center><font color=$fontcolormisc><b>您的论坛密码将通过邮件寄给您<BR>如果你一直没有收到邮件，那么请检查注册信是否被放到了垃圾箱内了！</td></tr>~;
        }
        $qa = qq~~;
    }
    else {
        $requirepass = qq~<tr>
        <td bgcolor=$miscbackone width=40%><font color=$fontcolormisc><b>论坛密码： (至少8位)</b><br>请输入论坛密码，区分大小写<br>只能使用大小写字母和数字的组合</td>
        <td bgcolor=$miscbackone width=60%><input type=password name="password" maxlength=20>&nbsp;* 此项必须填写</td>
        </tr><tr>
        <td bgcolor=$miscbackone><font color=$fontcolormisc><b>论坛密码： (至少8位)</b><br>再输一遍，以便确定！</td>
        <td bgcolor=$miscbackone><input type=password name="password2" maxlength=20>&nbsp;* 此项必须填写</td>
        </tr>~;
        $qa = qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>论坛密码提示问题：</b>用于取得忘记了的论坛密码<br>最大 20 个字节（10个汉字）</td>
<td bgcolor=$miscbackone><input type=text name="getpassq" value="" size=20 maxlength=20></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>论坛密码提示答案：</b>配合上栏使用<br>最大 20 个字节（10个汉字）</td> 
<td bgcolor=$miscbackone><input type=text name="getpassa" value="" size=20 maxlength=20></td></tr>~;
        $passcheck = qq~	if (document.creator.password.value == '')
	{
		window.alert('您还没有输入您的密码！');
		document.creator.password.focus();
		return false;
	}
	if (document.creator.password.value != document.creator.password2.value)
	{
		window.alert('两次输入的密码不一致！');
		document.creator.password.focus();
		return false;
	}
	if (document.creator.password.value.length < 8)
	{
		window.alert('密码太短了，请更换！密码必须 8 位以上！');
		document.creator.password.focus();
		return false;
	}~;
    }

    if ($avatars eq "on") {
        if ($arrowavaupload eq "on") {$avaupload = qq~<br>上传头像： <input type="file" size=20 name="addme">　上传自定义头像。<br>~;}
        else {undef $avaupload;}
        open(FILE, "${lbdir}data/lbava.cgi");
        sysread(FILE, $totleavator, (stat(FILE))[7]);
        close(FILE);
        $totleavator =~ s/\r//isg;
        my @images = split(/\n/, $totleavator);
        $totleavator = @images - 1;
        $selecthtml .= qq~<option value="noavatar" selected>不要头像</option>\n~;
        $currentface = "noavatar";

        foreach (@images) {
            $_ =~ s/\.(gif|jpg)$//i;
            next if ($_ =~ /admin_/);
            if ($_ ne "noavatar") {$selecthtml .= qq~<option value="$_">$_</option>\n~;}
        }

        $avatarhtml = qq~<script language="javascript">
function showimage(){document.images.useravatars.src="$imagesurl/avatars/"+document.creator.useravatar.options[document.creator.useravatar.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>个性图片：</b><br>您可以选择一个个性图片，当你发表时将显示在您的名字下方。<BR>如果你填写了下面的自定义头像部分，那么你的头像以自定义的为准。否则，请你留空自定义头像的所有栏目！<BR>
<br><br><b>关于自定义头像</b>：<br>你也可以在这里给出你自定义头像的 URL 地址，头像的高度和宽度(像素)。 如果不想要自定义头像，请将相应栏目全部留空！<BR>如果不填写头像的高度和宽度，则系统将自动判断并填入。<BR><BR>
<br><b>如果你不想要任何的头像，那么请首先在菜单上选“不要头像”，然后留空所有自定义头像的部分！</b><BR><br>
<td bgcolor=$miscbackone valign=top>总头像个数： $totleavator 个。　<a href=viewavatars.cgi target=_blank><B>按此查看</B></a>所有头像名称列表。<BR>
<select name="useravatar" size=1 onChange="showimage()">
$selecthtml
</select>
<img src=$imagesurl/avatars/$currentface.gif name="useravatars" width=32 height=32 hspace=15><br><br><br>
$avaupload
<br>图像位置： <input type=text name="personalavatar" size=20 value="">　输入完整的 URL 路径。<br>
<br>图像宽度： <input type=text name="personalwidth" size=2 maxlength=3 value=32>　必须是 20 -- $maxposticonwidth 之间的一个整数。<br>
<br>图像高度： <input type=text name="personalheight" size=2 maxlength=3 value=32>　必须是 20 -- $maxposticonheight 之间的一个整数。<br></td>
</td></tr>~;
    }

    $flaghtml = qq~<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=$miscbackone valign=top><font face=$font color=$fontcolormisc><b>所在国家:</b><br>请选择你所在的国家。</td>
<td bgcolor=$miscbackone>
<select name="userflag" size=1 onChange="showflag()">
<option value="blank" selected>保密</option>
<option value="China">中国</option>
<option value="Angola">安哥拉</option>
<option value="Antigua">安提瓜</option>
<option value="Argentina">阿根廷</option>
<option value="Armenia">亚美尼亚</option>
<option value="Australia">澳大利亚</option>
<option value="Austria">奥地利</option>
<option value="Bahamas">巴哈马</option>
<option value="Bahrain">巴林</option>
<option value="Bangladesh">孟加拉</option>
<option value="Barbados">巴巴多斯</option>
<option value="Belgium">比利时</option>
<option value="Bermuda">百慕大</option>
<option value="Bolivia">玻利维亚</option>
<option value="Brazil">巴西</option>
<option value="Brunei">文莱</option>
<option value="Canada">加拿大</option>
<option value="Chile">智利</option>
<option value="Colombia">哥伦比亚</option>
<option value="Croatia">克罗地亚</option>
<option value="Cuba">古巴</option>
<option value="Cyprus">塞浦路斯</option>
<option value="Czech_Republic">捷克</option>
<option value="Denmark">丹麦</option>
<option value="Dominican_Republic">多米尼加</option>
<option value="Ecuador">厄瓜多尔</option>
<option value="Egypt">埃及</option>
<option value="Estonia">爱沙尼亚</option>
<option value="Finland">芬兰</option>
<option value="France">法国</option>
<option value="Germany">德国</option>
<option value="Great_Britain">英国</option>
<option value="Greece">希腊</option>
<option value="Guatemala">危地马拉</option>
<option value="Honduras">洪都拉斯</option>
<option value="Hungary">匈牙利</option>
<option value="Iceland">冰岛</option>
<option value="India">印度</option>
<option value="Indonesia">印度尼西亚</option>
<option value="Iran">伊朗</option>
<option value="Iraq">伊拉克</option>
<option value="Ireland">爱尔兰</option>
<option value="Israel">以色列</option>
<option value="Italy">意大利</option>
<option value="Jamaica">牙买加</option>
<option value="Japan">日本</option>
<option value="Jordan">约旦</option>
<option value="Kazakstan">哈萨克</option>
<option value="Kenya">肯尼亚</option>
<option value="Kuwait">科威特</option>
<option value="Latvia">拉脱维亚</option>
<option value="Lebanon">黎巴嫩</option>
<option value="Lithuania">立陶宛</option>
<option value="Malaysia">马来西亚</option>
<option value="Malawi">马拉维</option>
<option value="Malta">马耳他</option>
<option value="Mauritius">毛里求斯</option>
<option value="Morocco">摩洛哥</option>
<option value="Mozambique">莫桑比克</option>
<option value="Netherlands">荷兰</option>
<option value="New_Zealand">新西兰</option>
<option value="Nicaragua">尼加拉瓜</option>
<option value="Nigeria">尼日利亚</option>
<option value="Norway">挪威</option>
<option value="Pakistan">巴基斯坦</option>
<option value="Panama">巴拿马</option>
<option value="Paraguay">巴拉圭</option>
<option value="Peru">秘鲁</option>
<option value="Poland">波兰</option>
<option value="Portugal">葡萄牙</option>
<option value="Romania">罗马尼亚</option>
<option value="Russia">俄罗斯</option>
<option value="Saudi_Arabia">沙特阿拉伯</option>
<option value="Singapore">新加坡</option>
<option value="Slovakia">斯洛伐克</option>
<option value="Slovenia">斯洛文尼亚</option>
<option value="Solomon_Islands">所罗门</option>
<option value="Somalia">索马里</option>
<option value="South_Africa">南非</option>
<option value="South_Korea">韩国</option>
<option value="Spain">西班牙</option>
<option value="Sri_Lanka">印度</option>
<option value="Surinam">苏里南</option>
<option value="Sweden">瑞典</option>
<option value="Switzerland">瑞士</option>
<option value="Thailand">泰国</option>
<option value="Trinidad_Tobago">多巴哥</option>
<option value="Turkey">土耳其</option>
<option value="Ukraine">乌克兰</option>
<option value="United_Arab_Emirates">阿拉伯联合酋长国</option>
<option value="United_States">美国</option>
<option value="Uruguay">乌拉圭</option>
<option value="Venezuela">委内瑞拉</option>
<option value="Yugoslavia">南斯拉夫</option>
<option value="Zambia">赞比亚</option>
<option value="Zimbabwe">津巴布韦</option>
</select>
<img src="$imagesurl/flags/blank.gif" name="userflags" border=0 height=14 width=21>
</td></tr>~;

    if ($useverify eq "yes") {

        if ($verifyusegd ne "no") {
            eval ('use GD;');
            if ($@) {
                $verifyusegd = "no";
            }
        }
        if ($verifyusegd eq "no") {
            $houzhui = "bmp";
        }
        else {
            $houzhui = "png";
        }

        require 'verifynum.cgi';
        $venumcheck = qq~
    	if (document.creator.verifynum.value.length < 4)
	{
		window.alert('请输入正确的校验码！');
		return false;
	}
    ~;
    }
    $output .= qq~<script>
function Check(){
var Name=document.creator.inmembername.value;
window.open("./checkname.cgi?name="+Name,"Check","width=200,height=20,status=0,scrollbars=0,resizable=1,menubar=0,toolbar=0,location=0");
}
function CheckInput()
{
	if (document.creator.inmembername.value == '')
	{
		window.alert('您还没有填写用户名呢？');
		document.creator.inmembername.focus();
		return false;
	}
	if (document.creator.inmembername.value.length > 12)
	{
		window.alert('您的用户名太长了，请不要多于12个字符（6个汉字）！');
		document.creator.inmembername.focus();
		return false;
	}

$passcheck

	var s = document.creator.emailaddress.value;
	if (s.length > 50)
	{
		window.alert('Email地址长度不能超过50位!');
		return false;
	}

$venumcheck;
	return true;
}
</script>

<form action="$thisprog" method=post name="creator" enctype="multipart/form-data" OnSubmit="return CheckInput()"><tr>
<input type=hidden name="forum" value="$in_forum">
<td bgcolor=$miscbacktwo width=40%><font color=$fontcolormisc><b>用户名：</b><br>注册用户名不能超过12个字符（6个汉字）</td>
<td bgcolor=$miscbacktwo width=60%><input type=text maxlength="12" name="inmembername">&nbsp;<input onClick="javascript:Check()" type=button value="检测帐号" name="button" class="button">&nbsp;* 此项必须填写</td>
</tr>$requirepass
<tr><td bgcolor=$miscbacktwo><font color=$fontcolormisc><b>邮件地址：</b><br>请输入有效的邮件地址，这将使您能用到论坛中的所有功能</td>
<td bgcolor=$miscbacktwo><input type=text name="emailaddress">&nbsp;* 此项必须填写</td></tr>
~;

    #	var regu = "^(([0-9a-zA-Z]+)|([0-9a-zA-Z]+[_.0-9a-zA-Z-]*[0-9a-zA-Z]+))\@([a-zA-Z0-9-]+[.])+([a-zA-Z]{4}|net|NET|com|COM|gov|GOV|mil|MIL|org|ORG|edu|EDU|int|INT|name|shop|NAME|SHOP)\$";
    #	var re = new RegExp(regu);
    #	if (s.search(re) == -1)
    #	{
    #		window.alert ('请输入有效合法的E-mail地址！')
    #		return false;
    #       }

    $output .= qq~<tr><td bgcolor=$miscbacktwo><font color=$fontcolormisc><b>注册验证码：(验证码有效期为20分钟)</b><br>请输入右列的验证码，输入不正确时将不能正常注册。<br>（注意：只有数字， 0 是零而不是英文字母的 O）</font></td><td bgcolor=$miscbacktwo><input type=hidden name=sessionid value="$sessionid"><input type=text name="verifynum" size=4 maxlength=4> * <img src=$imagesurl/verifynum/$sessionid.$houzhui align=absmiddle> 一共是四个数字，如果看不清，请刷新</td></tr>~ if ($useverify eq "yes");
    $output .= qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>推荐人用户名：</b><br>是谁推荐您加入我们的社区的？(这将使你的推荐人积分值增长)</td>
<td bgcolor=$miscbackone><input type=text name="recommender">&nbsp;如没有请保持空白</td>
</tr></table></td></tr></table>
~;
    if ($advreg == 1) {
        $advregister = "true";
        $advmode = qq~<td width=50%><INPUT id=advcheck name=advshow type=checkbox value=1 checked onclick=showadv()><span id="advance">关闭更多注册选项</a></span> </td><td width=50%><input type=submit value="注 册" name=submit></td>~;
    }
    else {
        $advregister = "none";
        $advmode = qq~<td width=50%><INPUT id=advcheck name=advshow type=checkbox value=1 onclick=showadv()><span id="advance">显示更多注册选项</a></span> </td><td width=50%><input type=submit value="注 册" name=submit></td>~;
    }
    $output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center id=adv style="DISPLAY: $advregister"><tr><td>
<table cellpadding=4 cellspacing=1 width=100%>
$qa
<tr><td bgcolor=$miscbacktwo valign=middle colspan=2 align=center> 
<font color=$fonthighlight><b>论坛密码提示问题和答案是不能够修改的，请谨慎输入！</b></font></td></tr>
<tr>
<td bgcolor=$miscbackone width=40%><font color=$fontcolormisc><b>显示邮件地址</b><br>您是否希望在您发表文章之后显示您的邮件？</td>
<td bgcolor=$miscbackone width=60%><font color=$fontcolormisc><input name="showemail" type="radio" value="yes" checked> 是　 <input name="showemail" type="radio" value="msn"> MSN　 <input name="showemail" type="radio" value="popo"> 网易泡泡　 <input name="showemail" type="radio" value="no"> 否</font></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>性别</b></td><td bgcolor=$miscbackone>
<select name="sex" size="1">
<option value="no">保密 </option>
<option value="m">帅哥 </option>
<option value="f">美女 </option>
</select>
</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>最高学历</b></td>
<td bgcolor=$miscbackone>
<select name="education" size="1">
<option value="保密">保密 </option>
<option value="小学">小学 </option>
<option value="初中">初中 </option>
<option value="高中">高中</option>
<option value="大专">大专</option>
<option value="本科">本科</option>
<option value="硕士">硕士</option>
<option value="博士">博士</option>
<option value="博士后">博士后</option>
</select>
</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>婚姻状况</b></td>
<td bgcolor=$miscbackone>
<select name="marry" size="1">
<option value="保密">保密 </option>
<option value="未婚">未婚 </option>
<option value="已婚">已婚 </option>
<option value="离婚">离婚 </option>
<option value="丧偶">丧偶 </option>
</select>
</td></tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>职业状况</b></td>
<td bgcolor=$miscbackone>
<select name="work" size="1">
<option value="保密">保密 </option>
<option value="计算机业">计算机业 </option>
<option value="金融业">金融业 </option>
<option value="商业">商业 </option>
<option value="服务行业">服务行业 </option>
<option value="教育业">教育业 </option>
<option value="学生">学生 </option>
<option value="工程师">工程师 </option>
<option value="主管，经理">主管，经理 </option>
<option value="政府部门">政府部门 </option>
<option value="制造业">制造业 </option>
<option value="销售/广告/市场">销售/广告/市场 </option>
<option value="失业中">失业中 </option>
</select>
</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>生日：</b>如不想填写，请全部留空。此项可选</td>
<td bgcolor=$miscbackone><input type="text" name="year" size=4 maxlength=4>年 
  <select name="month">
      <option value="" selected></option>
      <option value="01">01</option>
      <option value="02">02</option>
      <option value="03">03</option>
      <option value="04">04</option>
      <option value="05">05</option>
      <option value="06">06</option>
      <option value="07">07</option>
      <option value="08">08</option>
      <option value="09">09</option>
      <option value="10">10</option>
      <option value="11">11</option>
      <option value="12">12</option>
  </select>月
   <select name="day">
      <option value="" selected></option>
      <option value="01">01</option>
      <option value="02">02</option>
      <option value="03">03</option>
      <option value="04">04</option>
      <option value="05">05</option>
      <option value="06">06</option>
      <option value="07">07</option>
      <option value="08">08</option>
      <option value="09">09</option>
      <option value="10">10</option>
      <option value="11">11</option>
      <option value="12">12</option>
      <option value="13">13</option>
      <option value="14">14</option>
      <option value="15">15</option>
      <option value="16">16</option>
      <option value="17">17</option>
      <option value="18">18</option>
      <option value="19">19</option>
      <option value="20">20</option>
      <option value="21">21</option>
      <option value="22">22</option>
      <option value="23">23</option>
      <option value="24">24</option>
      <option value="25">25</option>
      <option value="26">26</option>
      <option value="27">27</option>
      <option value="28">28</option>
      <option value="29">29</option>
      <option value="30">30</option>
      <option value="31">31</option>
  </select>日
</td>
</tr>
<tr><SCRIPT language=javascript>
function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
</SCRIPT>
<td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>所属生肖：</b><br>请选择你所属的生肖。</td>
<td bgcolor=$miscbackone><SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"sx1\">子鼠</OPTION> <OPTION value=\"sx2\">丑牛</OPTION> <OPTION value=\"sx3\">寅虎</OPTION> <OPTION value=\"sx4\">卯兔</OPTION> <OPTION value=\"sx5\">辰龙</OPTION> <OPTION value=\"sx6\">巳蛇</OPTION> <OPTION value=\"sx7\">午马</OPTION> <OPTION value=\"sx8\">未羊</OPTION> <OPTION value=\"sx9\">申猴</OPTION> <OPTION value=\"sx10\">酉鸡</OPTION> <OPTION value=\"sx11\">戌狗</OPTION> <OPTION value=\"sx12\">亥猪</OPTION></SELECT> <IMG border=0 name=usersxs src="$imagesurl/sx/blank.gif" align="absmiddle">
</TD></tr><tr>
<SCRIPT language=javascript>
function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
</SCRIPT>
<td bgcolor=$miscbackone vAlign=top><font color=$fontcolormisc><b>所属星座：</b><br>请选择你所属的星座。<br>如果你正确输入了生日的话，那么此项无效！</td>
<td bgcolor=$miscbackone><SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>保密</OPTION> <OPTION value=\"z1\">白羊座(3月21--4月19日)</OPTION> <OPTION value=\"z2\">金牛座(4月20--5月20日)</OPTION> <OPTION value=\"z3\">双子座(5月21--6月21日)</OPTION> <OPTION value=\"z4\">巨蟹座(6月22--7月22日)</OPTION> <OPTION value=\"z5\">狮子座(7月23--8月22日)</OPTION> <OPTION value=\"z6\">处女座(8月23--9月22日)</OPTION> <OPTION value=\"z7\">天秤座(9月23--10月23日)</OPTION> <OPTION value=\"z8\">天蝎座(10月24--11月21日)</OPTION> <OPTION value=\"z9\">射手座(11月22--12月21日)</OPTION> <OPTION value=\"z10\">魔羯座(12月22--1月19日)</OPTION> <OPTION value=\"z11\">水瓶座(1月20--2月18日)</OPTION> <OPTION value=\"z12\">双鱼座(2月19--3月20日)</OPTION></SELECT> <IMG border=0 name=userxzs src="$imagesurl/star/blank.gif" width=15 height=15 align="absmiddle">
</TD>
</TR><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>主页地址：</b><br>如果您有主页，请输入主页地址。此项可选</td>
<td bgcolor=$miscbackone><input type=text name="homepage" value="http://"></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>OICQ 号：</b><br>如果您有 OICQ，请输入号码。此项可选</td>
<td bgcolor=$miscbackone><input type=text name="oicqnumber"></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>ICQ 号：</b><br>如果您有 ICQ，请输入号码。此项可选</td>
<td bgcolor=$miscbackone><input type=text name="icqnumber"></td>
</tr>$flaghtml<tr>
<script src=$imagesurl/images/comefrom.js></script>
<body onload="init()">
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>来自：</b><br>请输入您所在国家的具体地方。此项可选</td>
<td bgcolor=$miscbackone>
省份 <select name="province" onChange = "select()"></select>　城市 <select name="city" onChange = "select()"></select><br>
我在 <input type=text name="newlocation" maxlength=12 size=12 style="font-weight: bold">　不能超过12个字符（6个汉字）
</td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>时差：</b><br>
服务器所在时区：$basetimes<br>如果您所在的位置和服务器有时差，请输入。<br>您看到所有的时间将按照您所在的地区时间显示。</td>
<td bgcolor=$miscbackone>
<select name="timedifference"><option value="-23">- 23</option><option value="-22">- 22</option><option value="-21">- 21</option><option value="-20">- 20</option><option value="-19">- 19</option><option value="-18">- 18</option><option value="-17">- 17</option><option value="-16">- 16</option><option value="-15">- 15</option><option value="-14">- 14</option><option value="-13">- 13</option><option value="-12">- 12</option><option value="-11">- 11</option><option value="-10">- 10</option><option value="-9">- 9</option><option value="-8">- 8</option><option value="-7">- 7</option><option value="-6">- 6</option><option value="-5">- 5</option><option value="-4">- 4</option><option value="-3">- 3</option><option value="-2">- 2</option><option value="-1">- 1</option><option value="0" selected>0</option><option value="1">+ 1</option><option value="2">+ 2</option><option value="3">+ 3</option><option value="4">+ 4</option><option value="5">+ 5</option><option value="6">+ 6</option><option value="7">+ 7</option><option value="8">+ 8</option><option value="9">+ 9</option><option value="10">+ 10</option><option value="11">+ 11</option><option value="12">+ 12</option><option value="13">+ 13</option><option value="14">+ 14</option><option value="15">+ 15</option><option value="16">+ 16</option><option value="17">+ 17</option><option value="18">+ 18</option><option value="19">+ 19</option><option value="20">+ 20</option><option value="21">+ 21</option><option value="22">+ 22</option><option value="23">+ 23</option></select> 小时
</td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>自我简介： </b><BR>不能超过 <B>$maxinsline</B> 行，也不能超过 <B>$maxinslegth</B> 个字符<br><br>您可以在此输入您的个人简介。此项可选</td>
<td bgcolor=$miscbackone><textarea name="interests" cols="60" rows="5"></textarea></td>
</tr><tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>签名：</b><br>不能超过 <B>$maxsignline</B> 行，也不能超过 <B>$maxsignlegth</B> 个字符
<br><br>不能使用 HTML 标签<br>可以使用 <a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a><BR>
<li>贴图标签　: <b>$signpicstates</b><li>Flash 标签: <b>$signflashstates</b><li>音乐标签　: <b>$signsoundstates</b><li>文字大小　: <b>$signfontsizestates</b>
</td>
<td bgcolor=$miscbackone><textarea name="signature" cols="60" rows="8"></textarea></td>
</tr>
$avatarhtml
</table></td></tr><SCRIPT>valignend()</SCRIPT>
<script>
function showadv(){
if (document.creator.advshow.checked == true) {
adv.style.display = "";
advance.innerText="关闭更多用户设置选项"
}else{
adv.style.display = "none";
advance.innerText="显示更多用户设置选项"
}
}
</script>
</tr></table><img src="" width=0 height=4><BR>
<table cellpadding=0 cellspacing=0 width=$tablewidth align=center>
<tr>
$advmode 
<input type=hidden name=action value=addmember></form></tr></table><BR>
~;
}
else {
    require "cleanolddata.pl";
    &cleanolddata;
    $regdisptime = 15 if ($regdisptime < 1);
    $filetoopen = "$lbdir" . "data/register.dat";
    open(FILE, $filetoopen);
    sysread(FILE, my $tempoutput, (stat(FILE))[7]);
    close(FILE);
    $tempoutput =~ s/\r//isg;

    $output .= qq~<tr>
    <td bgcolor=$titlecolor $catbackpic align=center>
    <form action="$thisprog" method="post" name="agree">
    <input name="action" type="hidden" value="agreed">
    <input type=hidden name="forum" value="$in_forum">
    <font color=$fontcolormisc>
    <b>服务条款和声明</b>
    </td></tr>
    <td bgcolor=$miscbackone><font color=$fontcolormisc>
    $tempoutput
    </td></tr>
    <tr><td bgcolor=$miscbacktwo align=center>
    <center><input type="submit" value="请认真查看<服务条款和声明> ($regdisptime 秒后继续)" name="agreeb">　　
    <input onclick=history.back(-1) type="reset" value=" 我 不 同 意 ">
    </center>
    </td></form></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<SCRIPT language=javascript>
<!--
var secs = $regdisptime;
document.agree.agreeb.disabled=true;
for(i=1;i<=secs;i++) {
 window.setTimeout("update(" + i + ")", i * 1000);
}
function update(num) {
 if(num == secs) {
 document.agree.agreeb.value =" 我 同 意 ";
 document.agree.agreeb.disabled=false;
 }
else {
 printnr = secs-num;
 document.agree.agreeb.value = "请认真查看<服务条款和声明> (" + printnr +" 秒后继续)";
 }
}
//-->
</SCRIPT>

    ~;
}
print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&output("$board_name - 注册新用户", \$output);
exit;

sub recommfunc {
    my $recommender = shift;
    $recommender =~ s/ /\_/g;
    $recommender =~ tr/A-Z/a-z/;
    $recommender =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
    $namenumber = &getnamenumber($recommender);
    my $filetoopen = "${lbdir}$memdir/$namenumber/$recommender.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(REFILE, "+<$filetoopen");
        flock(REFILE, 2) if ($OS_USED eq "Unix");
        my $filedata = <REFILE>;
        chomp $filedata;
        ($lmembername, $lpassword, $lmembertitle, $lmembercode, $lnumberofposts, $lemailaddress, $lshowemail, $lipaddress, $lhomepage, $loicqnumber, $licqnumber, $llocation, $linterests, $ljoineddate, $llastpostdate, $lsignature, $ltimedifference, $lprivateforums, $luseravatar, $luserflag, $luserxz, $lusersx, $lpersonalavatar, $lpersonalwidth, $lpersonalheight, $lrating, $llastgone, $lvisitno, $luseradd04, $luseradd02, $lmymoney, $lpostdel, $lsex, $leducation, $lmarry, $lwork, $lborn, $lchatlevel, $lchattime, $ljhmp, $ljhcount, $lebankdata, $lonlinetime, $luserquestion, $lawards, $ljifen, $luserface, $lsoccerdata, $luseradd5) = split(/\t/, $filedata);

        my ($numberofposts, $numberofreplys) = split(/\|/, $lnumberofposts);
        $numberofposts ||= "0";
        $numberofreplys ||= "0";
        $ljifen = $numberofposts * 2 + $numberofreplys - $lpostdel * 5 if ($ljifen eq "");

        $addtjjf = 0 if ($addtjjf eq "");
        $addtjhb = 0 if ($addtjhb eq "");
        if ($lmymoney eq "") {$lmymoney = $addtjhb;}
        else {$lmymoney += $addtjhb;}

        $ljifen += $addtjjf;

        if (($lmembername ne "") && ($lpassword ne "")) {
            seek(REFILE, 0, 0);
            print REFILE "$lmembername\t$lpassword\t$lmembertitle\t$lmembercode\t$lnumberofposts\t$lemailaddress\t$lshowemail\t$lipaddress\t$lhomepage\t$loicqnumber\t$licqnumber\t$llocation\t$linterests\t$ljoineddate\t$llastpostdate\t$lsignature\t$ltimedifference\t$lprivateforums\t$luseravatar\t$luserflag\t$luserxz\t$lusersx\t$lpersonalavatar\t$lpersonalwidth\t$lpersonalheight\t$lrating\t$llastgone\t$lvisitno\t$luseradd04\t$luseradd02\t$lmymoney\t$lpostdel\t$lsex\t$leducation\t$lmarry\t$lwork\t$lborn\t$lchatlevel\t$lchattime\t$ljhmp\t$ljhcount\t$lebankdata\t$lonlinetime\t$luserquestion\t$lawards\t$ljifen\t$luserface\t$lsoccerdata\t$luseradd5\t";
            close(REFILE);
        }
        else {
            close(REFILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
    }
}

sub checkverify {
    my $verifynum = $query->param('verifynum');
    my $sessionid = $query->param('sessionid');
    $sessionid =~ s/[^0-9a-f]//isg;
    return 1 if (length($sessionid) != 32 && $useverify eq "yes");

    ###获取真实的 IP 地址
    my $ipaddress = $ENV{'REMOTE_ADDR'};
    my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $ipaddress = $trueipaddress if (($trueipaddress ne "") && ($trueipaddress ne "unknown"));
    $trueipaddress = $ENV{'HTTP_CLIENT_IP'};
    $ipaddress = $trueipaddress if (($trueipaddress ne "") && ($trueipaddress ne "unknown"));

    ###获取当前进程的验证码和验证码产生时间、用户密码
    my $filetoopen = "${lbdir}verifynum/$sessionid.cgi";
    open(FILE, $filetoopen);
    my $content = <FILE>;
    close(FILE);
    chomp($content);
    my ($trueverifynum, $verifytime, $savedipaddress) = split(/\t/, $content);
    my $currenttime = time;
    return ($verifynum ne $trueverifynum || $currenttime > $verifytime + 1200 + 120 || $ipaddress ne $savedipaddress) ? 1 : 0;
}
