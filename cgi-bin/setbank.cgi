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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/ebankinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";

$|++;
$thisprog = "setbank.cgi";
$query = new LBCGI;
#&ipbanned;

$action = $query->param('action');
if ($action eq "login") {
    $in_member_name = $query->param("membername");
    $in_password = $query->param("password");
    $in_passwordtemp = $in_password;
    if ($in_password ne "") {
        eval {$in_password = md5_hex($in_password);};
        if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
        unless ($@) {$in_password = "lEO$in_password";}
    }
    &checkverify;
    my $tempmembername = uri_escape($in_member_name);
    print "Set-Cookie: adminname=$tempmembername\n";
    print "Set-Cookie: adminpass=$in_password\n";
}
else {
    $in_member_name = $query->cookie("adminname");
    $in_password = $query->cookie("adminpass");
}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
&getmember($in_member_name, "no");
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;

if (($member_code eq "ad" || ($member_code eq "smo" && $bankadminallow eq "all") || ",$bankmanager," =~ /,$in_member_name,/i) && ($in_password eq $password) && (lc($in_member_name) eq lc($membername))) {
    my %Mode = (
        'setinfo'   => \&setinfo,   #设定银行各项业务指标
        'setok'     => \&setok,     #保存设定
        'editmem'   => \&editmem,   #编辑一个用户的存贷款
        'editok'    => \&editok,    #保存编辑值
        'empty'     => \&empty,     #清空银行交易日志
        'deletelog' => \&deletelog, #删除指定日志
        'repair'    => \&repair,    #修复银行显示总量
        'viewloan'  => \&viewloan,  #查看贷款清单
        'bonus'     => \&bonus,     #给会员发红包
        'bonusok'   => \&bonusok
    );

    if ($Mode{$action}) {
        $Mode{$action}->();
    }
    else {
        &showlog;
    }
    print $output;
}
else {
    my $ipaddress = $ENV{'REMOTE_ADDR'};
    $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
    $trueipaddress = $ENV{'HTTP_CLIENT_IP'};
    $ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
    &logaction($in_member_name, "<b>从 $ipaddress 以密码 $in_passwordtemp 登录行长办公室失败。</b>") if ($in_member_name && $in_password);
    &ebankadminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;

sub viewloan {
    open(FILE, $lbdir . "ebankdata/allloan.cgi");
    my @loaninfo = <FILE>;
    close(FILE);

    $output = qq~<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=4><font color=#ffffff><b>欢迎来到论坛管理中心 / 银行行长办公室</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=4>　<a href=$thisprog>返 回</a>  >> 查看贷款清单：</td>
</tr>
<tr>
	<td bgcolor=#eeeeee align=center width=20%>贷款人</td>
	<td bgcolor=#eeeeee align=center width=40%>贷款日期</td>
	<td bgcolor=#eeeeee align=center width=20%>贷款数额</td>
	<td bgcolor=#eeeeee align=center width=20%>抵押威望</td>
</tr>~;

    foreach (@loaninfo) {
        chomp;
        my ($loaner, $loantime) = split(/,/, $_);
        my $namenumber = &getnamenumber($loaner);
        &checkmemfile($loaner, $namenumber);
        my $loanfile = "$lbdir$memdir/$namenumber/$loaner.cgi";
        if (-e $loanfile) {
            open(FILE, $loanfile);
            my $filedata = <FILE>;
            close(FILE);

            my ($membername, $password, $membertitle, $member_code, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
            my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
            $loantime = &shortdate($loantime);

            $output .= qq~<tr>
	<td bgcolor=#ffffff align=center><a href=profile.cgi?action=show&member=~ . uri_escape($loaner) . qq~ target=_blank>$membername</a></td>
	<td bgcolor=#ffffff align=center>$loantime</td>
	<td bgcolor=#ffffff align=center>$myloan</td>
	<td bgcolor=#ffffff align=center>$myloanrating</td>
</tr>~;
        }
    }
    $output .= "</table>";

    return;
}

sub bonusok {
    my $step = $query->param('step');
    $step = 1 if ($step eq "");
    my $bonusmem = $query->param('bonusmem');

    for ("bonustarget", "bonusday", "bonuspost", "bonusnum", "bonusreason") {
        ${$_} = &cleaninput($query->param($_));
    }
    &seterror("红包对象附加要求输入有误！") if ($bonusday =~ /[^0-9]/ || $bonuspost =~ /[^0-9]/);
    &seterror("没有输入红包的数额或者输入有误！") if ($bonusnum !~ /^[0-9]+$/);
    &seterror("必须输入发红包的理由！") if ($bonusreason eq "");

    opendir(DIR, "$lbdir$memdir/old");
    my @memberfiles = readdir(DIR);
    close(DIR);
    @memberfiles = grep (/\.cgi$/i, @memberfiles);

    my $currenttime = time;
    for ($i = ($step - 1) * 200; $i < $step * 200 && $i < @memberfiles; $i++) {
        &winunlock($lastfile) if (($OS_USED eq "Unix" || $OS_USED eq "Nt") && $lastfile ne "");
        ($nametocheck, $no) = split(/\./, $memberfiles[$i]);
        my $namenumber = &getnamenumber($nametocheck);
        &checkmemfile($nametocheck, $namenumber);
        $lastfile = $lbdir . $memdir . "/$namenumber/" . $memberfiles[$i];
        &winlock($lastfile) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
        open(FILE, $lastfile);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my $filedata = <FILE>;
        close(FILE);

        my ($membername, $password, $membertitle, $member_code, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
        my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
        my ($numberofposts, $numberofreplys) = split(/\|/, $numberofposts);

        next if ($member_code eq "banned" || $member_code eq "masked");
        next if ($bonustarget ne "all" && $mystatus != 1);
        next if ($bonusday ne "" && $currenttime - $joineddate < $bonusday * 86400);
        next if ($bonuspost ne "" && $numberofposts + $numberofreplys < $bonuspost);

        $mymoney += $bonusnum;
        open(FILE, ">$lastfile");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$password\t$membertitle\t$member_code\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        &winunlock($lastfile) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
        $bonusmem++;
        unlink("${lbdir}cache/meminfo/$nametocheck.pl");
        unlink("${lbdir}cache/myinfo/$nametocheck.pl");

        $lastfile = $memberfiles[$i];
        $lastfile =~ s/\.cgi$//isg;
        &bankmessage($lastfile, "<font color=red>红包通知</font>", "　　$in_member_name 以$bonusreason的理由，给您发了 $bonusnum $moneyname的红包，请查收您的现金。");
        $lastfile = "";
    }
    &winunlock($lastfile) if (($OS_USED eq "Unix" || $OS_USED eq "Nt") && $lastfile ne "");

    if ($i < @memberfiles - 1) {
        #继续下一步
        $step++;
        $output = qq~<form name=MAINFORM action=$thisprog?step=$step method=POST>
<input type=hidden name=action value=bonusok>
<input type=hidden name=step value=$step>
<input type=hidden name=bonustarget value="$bonustarget">
<input type=hidden name=bonusmem value="$bonusmem">
<input type=hidden name=bonusday value="$bonusday">
<input type=hidden name=bonuspost value="$bonuspost">
<input type=hidden name=bonusnum value="$bonusnum">
<input type=hidden name=bonusreason value="$bonusreason">
</form>
<script language="JavaScript">
setTimeout("MAINFORM.submit()", 1000);
</script>
　如果你的浏览器没有自动前进，请<a href="javascript: MAINFORM.submit()">点击继续</a>~;
    }
    else {
        $bonustarget = $bonustarget eq "all" ? "所有注册会员" : "所有银行客户";
        $bonusday = "注册 $bonusday 天以上" if ($bonusday ne "");
        $bonuspost = "发帖 $bonuspost 篇以上" if ($bonuspost ne "");
        $bonusday = $bonusday ne "" && $bonuspost ne "" ? "$bonusday且$bonuspost的" : $bonusday ne "" || $bonuspost ne "" ? "$bonusday$bonuspost的" : "";
        &logaction($in_member_name, "<font color=red>以$bonusreason的理由给$bonusday$bonustarget发了总共 $bonusmem 个 $bonusnum $moneyname 的红包。");
        $output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>欢迎来到论坛管理中心 / 雷傲银行行长办公室</b></td></tr>
<tr><td align=center><br><b><font color=red>给$bonusday$bonustarget的红包发放完成，总共发出红包 $bonusmem 个!</font></b></td></tr>
</table>~;
    }
    return;
}

sub repair {
    my $step = $query->param('step');
    $step = 1 unless ($step);

    my %ordersaves;
    if ($step == 1) {
        &setbankonoff("off");
        unlink($lbdir . "ebankdata/allsaves.cgi");
        unlink($lbdir . "ebankdata/allloan.cgi");
        unlink($lbdir . "ebankdata/order.cgi");
        unlink(&lockfilename($lbdir . "ebankdata/order.cgi") . ".lck");
    }
    else {
        #读取已有排序结果
        open(FILE, $lbdir . "ebankdata/order.cgi");
        my @orderdata = <FILE>;
        close(FILE);
        foreach (@orderdata) {
            chomp;
            my ($tempuser, $tempsave) = split(/\t/, $_);
            $ordersaves{$tempuser} = $tempsave if ($tempuser ne "");
        }
    }
    opendir(DIR, "${lbdir}ebankdata/log");
    my @memberfiles = readdir(DIR);
    close(DIR);
    @memberfiles = grep (/\.cgi$/i, @memberfiles);

    my $stepusers = 0;
    my $stepsaves = 0;
    for ($i = ($step - 1) * 200; $i < $step * 200 && $i < @memberfiles; $i++) {
        ($nametocheck, $no) = split(/\./, $memberfiles[$i]);
        my $namenumber = &getnamenumber($nametocheck);
        &checkmemfile($nametocheck, $namenumber);
        my $filetoopen = $lbdir . $memdir . "/$namenumber/" . $memberfiles[$i];
        open(FILE, $filetoopen);
        my $filedata = <FILE>;
        close(FILE);

        my ($membername, $password, $membertitle, $member_code, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
        my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

        if ($mystatus) {
            $membername =~ s/ /\_/sg;
            $membername =~ tr/A-Z/a-z/;
            $stepusers++;
            $stepsaves += $mysaves;
            $ordersaves{$membername} = $mysaves;
            if ($myloan) {
                my $filetomake = $lbdir . "ebankdata/allloan.cgi";
                &winlock($filetomake) if ($OS_USED eq "Nt");
                open(FILE, ">>$filetomake");
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE "$membername,$myloantime\n";
                close(FILE);
                &winunlock($filetomake) if ($OS_USED eq "Nt");
            }
        }
    }
    &updateallsave($stepusers, $stepsaves);
    #将本次排序和已有排序结果综合
    my @orderusers = sort {$ordersaves{$a} <=> $ordersaves{$b}} keys(%ordersaves);
    open(FILE, ">" . $lbdir . "ebankdata/order.cgi");
    for ($k = 1; $k <= $bankmaxdisplay * 2; $k++) {
        $j = @orderusers - $k;
        last if ($j < 0);
        print FILE $orderusers[$j] . "\t" . $ordersaves{$orderusers[$j]} . "\n" if ($ordersaves{$orderusers[$j]});
    }
    close(FILE);

    if ($i < @memberfiles - 1) {
        #继续下一步
        $step++;
        $output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=repair&step=$step"><br>　如果你的浏览器没有自动前进，请<a href=$thisprog>点击继续</a>~;
    }
    else {
        #贷款记录必须排序存放
        my $filetomake = $lbdir . "ebankdata/allloan.cgi";
        open(FILE, $filetomake);
        my @loaninfo = <FILE>;
        close(FILE);
        my %loantimes;
        foreach (@loaninfo) {
            chomp;
            my ($loaner, $loantime) = split(/,/, $_);
            $loantimes{$loaner} = $loantime if ($loaner ne "");
        }

        my @loaners = sort {$loantimes{$a} <=> $loantimes{$b}} keys(%loantimes);

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach (@loaners) {
            print FILE $_ . "," . $loantimes{$_} . "\n";
        }
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        &setbankonoff("on");
        $output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>欢迎来到论坛管理中心 / 雷傲银行行长办公室</b></td></tr>
<tr><td align=center><br><b>总量显示修复完成!</b></td></tr>
</table>~;
    }

    return;
}

sub showlog {
    my $page = $query->param('page');
    $page = 1 unless ($page);
    my $type = $query->param('type');
    $type = "name" unless ($type eq "key" || $type eq "time");
    my $key = $query->param('key');

    open(FILE, $lbdir . "ebankdata/alllogs.cgi");
    my @ebanklogs = <FILE>;
    close(FILE);

    if ($key ne "") { #选出指定纪录
        if ($type eq "name") {
            $key =~ s/ /\_/sg;
            @ebanklogs = grep (/^$key\t.+\t.+$/i, @ebanklogs);
        }
        elsif ($type eq "time") {
            my ($begin, $end);
            for ($begin = 0; $begin < @ebanklogs; $begin++) {
                my ($temp1, $temptime, $temp2) = split(/\t/, $ebanklogs[$begin]);
                $temptime = &shortdate($temptime + $timezone * 3600 + $timedifferencevalue * 3600);
                last if ($key eq $temptime);
            }
            for ($end = @ebanklogs - 1; $end >= $begin - 1; $end--) {
                my ($temp1, $temptime, $temp2) = split(/\t/, $ebanklogs[$end]);
                $temptime = &shortdate($temptime + $timezone * 3600 + $timedifferencevalue * 3600);
                last if ($key eq $temptime);
            }
            if ($begin > $end) {
                undef(@ebanklogs);
            }
            else {
                @ebanklogs = @ebanklogs[$begin .. $end];
            }
        }
        else {
            @ebanklogs = grep (/^.+\t.+\t.*$key.*$/i, @ebanklogs);
        }
    }

    my $allpages = int(@ebanklogs / 25) + 1;
    $page = 1 if ($page < 1);
    $page = $allpages if ($page > $allpages);
    my $showpage = "";
    if ($allpages > 1) {
        $showpage .= qq~记录共 <b>$allpages</b> 页 ~;
        $i = $page - 1;
        $showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();" title="上一页"><<</span> ~ if ($i > 0);
        $showpage .= "[ ";
        $i = $page - 3;
        $showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">←</span> ~ if ($i > 0);
        $i++;
        $showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i > 0);
        $i++;
        $showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i > 0);
        $i++;
        $showpage .= qq~<font color=#990000>$i</font> ~;
        $i++;
        $showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i <= $allpages);
        $i++;
        $showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">$i</span> ~ if ($i <= $allpages);
        $i++;
        $showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();">→</span> ~ if ($i <= $allpages);
        $showpage .= "] ";
        $i = $page + 1;
        $showpage .= qq~<span style="cursor:hand" OnClick="MAINFORM.page.value=$i; MAINFORM.submit();" title="下一页">>></span> ~ if ($i <= $allpages);
        $showpage .= "　直接跳转到第 <input type=text name=page size=2 value=$page style='text-align: right' OnMouseOver='this.focus();' OnFocus='this.select();'> 页 <input type=submit value='Go'>";
    }
    else {
        $showpage = "记录只有 <b>1</b> 页";
    }

    $output = qq~
<script language="JavaScript">
function goempty()
{
	if (clearday = prompt("请输入要清空多少天以前的日志：", "30"))
		location.href = "$thisprog?action=empty&day=" + clearday;
}
</script>
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=4><font color=#ffffff><b>欢迎来到论坛管理中心 / 雷傲银行行长办公室</b></td>
</tr>
<form name=EDIT action=$thisprog method=POST>
<input type=hidden name=action value="editmem">
<tr>
	<td bgcolor=#cccccc width=20%>　<a href=$thisprog?action=setinfo>设定银行业务</a></td>
	<td bgcolor=#cccccc width=20%><a href=$thisprog?action=repair OnClick="return confirm('这将暂时自动关闭银行，操作完成会自动重新开放。\\n一般无需进行此操作，是否继续？');">重新计算统计和排名</a></td>
	<td bgcolor=#cccccc width=20%><a href=$thisprog?action=bonus><font color=red>给所有客户发红包</font></a></td>
	<td bgcolor=#cccccc width=45% align=right>快速编辑会员帐户： <input type=text size=10 name=memid value=用户名 OnMouseOver="this.focus();" OnFocus="this.select();">　<input type=submit value=编辑></td>
</tr>
</form>
<form name=MAINFORM action=$thisprog method=POST>
<tr>
	<td align=left bgcolor=#ffffff>　<a href=$thisprog?action=viewloan><font color=#ff7700>贷款清单</font></a></td> 
	<td align=center colspan=3 bgcolor=#ffffff>$showpage</td>
</tr>
<tr>
	<td bgcolor=#eeeeee>　<b>查找日志</b></td>
	<td bgcolor=#eeeeee><select name=type><option value="name">搜索指定会员</option><option value="time">搜索特定日期</option><option value="key">搜索操作内容</option></select></td>
	<td bgcolor=#eeeeee align=right colspan=2><input name=key value="$key" type=text size=20 OnMouseOver="this.focus();" OnFocus="this.select();">　<input type=submit value=查找>　　<a href="javascript:goempty()">清空过期交易记录</a>　</td>	
</tr>
</form>
<form name=DELETE action=$thisprog method=POST>
<input type=hidden name=action value=deletelog>
<tr>
	<td bgcolor=#ffffff>　<b>营业状况</b></td>~;
    if ($key ne "") {
        $output .= qq~<td bgcolor=#ffffff colspan=3><table width=98%><td><i><font color=#0000ee>按日期搜索，输入日期的格式必须是 2002/09/29 这样的形式！</font></i></td><td align=right><a href="$thisprog">返回全部日志显示</a></td></table></td>~;
    }
    else {
        $output .= qq~<script language="JavaScript">
function CheckAll() {for (var i = 0; i < DELETE.dellogid.length; i++) {DELETE.dellogid[i].checked = true;}}
function FanAll() {for (var i = 0; i < DELETE.dellogid.length; i++) {DELETE.dellogid[i].checked = !DELETE.dellogid[i].checked;}}
</script>
<td bgcolor=#ffffff colspan=3><table width=98%><td><i><font color=#0000ee>按日期搜索，输入日期的格式必须是 2002/09/29 这样的形式！</font></i></td><td align=right><input type=button OnClick="CheckAll();" value="全选"> <input type=button OnClick="FanAll();" value="反选">　<a href="JavaScript:DELETE.submit();" OnClick="return confirm('这将删除你选定的交易日志，是否继续？');">删除选定的纪录</a></td></table></td>~;
    }
    $output .= qq~</tr>~;

    my $lognum = @ebanklogs - ($page - 1) * 25;
    my ($logcustomer, $logtime, $logevent);
    for ($i = $lognum - 1; $i >= $lognum - 25 && $i >= 0; $i--) {
        chomp($ebanklogs[$i]);
        ($logcustomer, $logtime, $logevent) = split(/\t/, $ebanklogs[$i]);
        $logtime = &dateformatshort($logtime + $timezone * 3600 + $timedifferencevalue * 3600);
        $logcustomer = qq~<a href=profile.cgi?action=show&member=~ . uri_escape($logcustomer) . qq~ target=_blank>$logcustomer</a>~ unless ($logcustomer =~ /银行自动处理程序/);
        $output .= qq~<tr>
	<td bgcolor=#ffffff>　$logcustomer</td>
	<td bgcolor=#ffffff>$logtime</td>~;
        if ($key ne "") {
            $output .= qq~<td bgcolor=#ffffff colspan=2>$logevent</td>~;
        }
        else {
            my $j = $i + 1;
            $output .= qq~<td bgcolor=#ffffff colspan=2><table width=98%><td>$logevent</td><td align=right><input type=checkbox name=dellogid value=$j></td></table></td>~;
        }
        $output .= qq~</tr>~;
    }

    $output .= qq~</form>
<form action=$thisprog method=POST>
<input type=hidden name=action value="search">
<tr>
	<td bgcolor=#eeeeee>　<b>查找日志</b></td>
	<td bgcolor=#eeeeee><select name=type><option value="name">搜索指定会员</option><option value="time">搜索特定日期</option><option value="key">搜索操作内容</option></select></td>
	<td bgcolor=#eeeeee align=right colspan=2><input name=key value="$key" type=text size=20 OnMouseOver="this.focus();" OnFocus="this.select();">　<input type=submit value=查找>　　<a href="javascript:goempty()">清空过期交易记录</a>　</td>	
</tr>
<tr>
	<td align=left bgcolor=#ffffff>　<a href=$thisprog?action=viewloan><font color=#ff7700>贷款清单</font></a></td> 
	<td align=center colspan=3 bgcolor=#ffffff>$showpage</td>
</tr>
</form>
</table>~;

    $output =~ s/<option value="$type">/<option value="$type" selected>/g;
    return;
}

sub bonus {
    $output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="bonusok">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>欢迎来到论坛管理中心 / 银行行长办公室</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>　<a href=$thisprog>返 回</a>  >> <font color=red>给客户发红包：</font></td>
</tr>
<tr>
	<td bgcolor=#ffffff width=35%>　红包对象：　</td>
	<td bgcolor=#ffffff>　<input type=radio name=bonustarget value="user" checked>　所有银行客户(除账号被冻结)　<input type=radio name=bonustarget value="all">　所有注册会员(除禁言和屏蔽)</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　对象附加要求：　</td>
	<td bgcolor=#ffffff>　注册 <input type=text size=3 name=bonusday> 天以上 并且发贴 <input type=text size=4 name=bonuspost> 以上　(不需要的请留空)</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　红包数额：　</td>
	<td bgcolor=#ffffff>　<input type=text size=12 name=bonusnum> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　红包理由：　</td>
	<td bgcolor=#ffffff>　<input type=text size=50 name=bonusreason></td>
</tr>
<tr>
	<td bgcolor=#ffffff align=center><input type=submit value=发　出></td>
	<td bgcolor=#ffffff align=center><input type=reset value=重　来></td>
</tr>
</table></form>~;
    return;
}

sub deletelog {
    my @dellogid = $query->param('dellogid');

    my $delnum = 0;
    my $currenttime = time;
    my $filetoopen = $lbdir . "ebankdata/alllogs.cgi";
    &winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    flock(FILE, 1) if ($OS_USED eq "Unix");
    open(FILE, $filetoopen);
    my @ebanklogs = <FILE>;
    close(FILE);
    foreach (@dellogid) {
        if ($_ > 0 && $_ <= @ebanklogs) {
            $ebanklogs[$_ - 1] = "";
            $delnum++;
        }
    }
    unless ($delnum) {
        &winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
        &seterror("请选择要删除的银行记录以后再操作！");
    }
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach (@ebanklogs) {
        chomp;
        print FILE $_ . "\n" if ($_);
    }
    print FILE "$in_member_name\t$currenttime\t<b>删除了 $delnum 条银行交易日志。</b>\n";
    close(FILE);
    &winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));

    $output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>　成功地删除了 $delnum 条银行交易日志。<br>　如果你的浏览器没有自动返回，请<a href=$thisprog>点击这里</a>~;
    return;
}

sub setinfo {
    my $banksave100rate = $banksaverate * 100;
    my $bankloan100rate = $bankloanrate * 100;
    my $banktrans100rate = $banktransrate * 100;
    my $bankpost100rate = $bankpostrate * 100;

    $output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="setok">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>欢迎来到论坛管理中心 / 银行行长办公室</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>　<a href=$thisprog>返 回</a>  >> 设定银行业务参数：</td>
</tr>
<tr>
	<td bgcolor=#ffffff width=35%>　银行状态：　</td>
	<td bgcolor=#ffffff>　<input type=radio name=bankopen value="on">　正常开放　<input type=radio name=bankopen value="off">　暂时关闭</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　银行名称：　</td>
	<td bgcolor=#ffffff>　<input type=text size=20 name=bankname value="$bankname"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　行长名称：　</td>
	<td bgcolor=#ffffff>　<input type=text size=20 name=bankmanager value="$bankmanager">　用英文逗号间隔多位行长</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　银行欢迎提示：　</td>
	<td bgcolor=#ffffff>　<input type=text size=60 name=bankmessage value="$bankmessage"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　存款日利率：　</td>
	<td bgcolor=#ffffff>　<input type=text size=4 name=banksaverate value="$banksave100rate"> %　<i>默认为 0.88%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　转帐汇款功能最低需要威望值：　</td>
	<td bgcolor=#ffffff>　<input type=text size=6 name=banktransneed value="$banktransneed"></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　转帐手续费率：</td>
	<td bgcolor=#ffffff>　<input type=text size=6 name=banktransrate value="$banktrans100rate"> %　<i>默认为 10%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　汇款手续费率：</td>
	<td bgcolor=#ffffff>　<input type=text size=6 name=bankpostrate value="$bankpost100rate"> %　<i>默认为 20%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　是否开放贷款功能：</td>
	<td bgcolor=#ffffff>　<input type=radio name=bankallowloan value="yes">　开放　　　<input type=radio name=bankallowloan value="no">　关闭</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　贷款最长偿还期限：</td>
	<td bgcolor=#ffffff>　<input type=text size=2 name=bankloanmaxdays value="$bankloanmaxdays"> 天　<i>默认为 7</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　贷款日利率：　</td>
	<td bgcolor=#ffffff>　<input type=text size=4 name=bankloanrate value="$bankloan100rate"> %　<i>默认为 1.88%</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　每点威望最高抵押贷款数额：　</td>
	<td bgcolor=#ffffff>　<input type=text size=6 name=bankrateloan value="$bankrateloan"> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　单笔交易最高限额：　</td>
	<td bgcolor=#ffffff>　<input type size=10 name=bankmaxdeal value="$bankmaxdeal"> $moneyname　<i>默认为 500000</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　单笔交易最低限额：　</td>
	<td bgcolor=#ffffff>　<input type size=10 name=bankmindeal value="$bankmindeal"> $moneyname　<i>默认为 10</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　首页显示的用户排名数：　</td>
	<td bgcolor=#ffffff>　<input type size=4 name=bankmaxdisplay value="$bankmaxdisplay">　<i>默认为 10 ，不能超过 20</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　24小时内最大交易次数：　</td>
	<td bgcolor=#ffffff>　<input type size=4 name=bankmaxdaydo value="$bankmaxdaydo">　<i>默认为 5 ，不能超过 10，对坛主无效</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　个人存折最多记录条数：　</td>
	<td bgcolor=#ffffff>　<input type size=4 name=banklogpriviate value="$banklogpriviate">　<i>默认为 6 ，不能超过 20</i></td>
</tr>
<tr>
	<td bgcolor=#ffffff>　允许管理银行会员：</td>
	<td bgcolor=#ffffff>　<select name=bankadminallow><option value="allad">所有坛主、行长</option><option value="all">所有总版主和坛主、行长</option></select></td>
</tr>
<tr>
	<td bgcolor=#ffffff align=center><input type=submit value=提　交></td>
	<td bgcolor=#ffffff align=center><input type=reset value=重　置></td>
</tr>
</table></form>~;

    $output =~ s/<input type=radio name=bankopen value="$bankopen">/<input type=radio name=bankopen value="$bankopen" checked>/g;
    $output =~ s/<input type=radio name=bankrateuse value="$bankrateuse">/<input type=radio name=bankrateuse value="$bankrateuse" checked>/g;
    $output =~ s/<input type=radio name=bankallowloan value="$bankallowloan">/<input type=radio name=bankallowloan value="$bankallowloan" checked>/g;
    $output =~ s/<option value="$bankadminallow">/<option value="$bankadminallow" selected>/g;

    return;
}

sub editmem {
    my $memid = $query->param('memid');
    &seterror("没有输入编辑的帐户名！") if ($memid eq "");
    &seterror("帐户名含有非法字符！") if (($memid =~ m/\//) || ($memid =~ m/\\/) || ($memid =~ m/\.\./));
    &getmember($memid, "no");
    &seterror("用户 $memid 不存在！") if ($userregistered eq "no");
    ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
    &seterror("用户 $memid 没有在本行开户！") unless ($mystatus);

    my $loanoutput;
    if ($myloan) {
        $loanoutput = qq~用户从本行贷款 $myloan $moneyname　　<input type=checkbox name=clearloan value="yes">　清除用户的贷款记录？~;
    }
    else {
        $loanoutput = qq~用户在本行没有贷款~;
    }

    $output = qq~<form action=$thisprog method=POST><input type=hidden name=action value="editok"><input type=hidden name=memid value="$memid">
<table width=100% cellpadding=6 cellspacing=0>
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>欢迎来到论坛管理中心 / 雷傲银行行长办公室</b></td>
</tr>
<tr>
	<td bgcolor=#cccccc colspan=2>　<a href=$thisprog>返 回</a>  >> 编辑 $memid 的存贷款资料：</td>
</tr>
<tr>
	<td bgcolor=#ffffff width=40%>　用户存款数额：　</td>
	<td bgcolor=#ffffff>　<input type=text size=15 name=newsavenums value="$mysaves"> $moneyname</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　用户贷款数额：　</td>
	<td bgcolor=#ffffff>　$loanoutput</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　修改取款密码：　</td>
	<td bgcolor=#ffffff>　<input type=text name=getpass size=15> (留空则不修改)</td>
</tr>
<tr>
	<td bgcolor=#ffffff>　用户账户状态：　</td>
	<td bgcolor=#ffffff>　<input name=accountstats type=radio value="on"> 正常使用　　<input name=accountstats value="off" type=radio> 暂时冻结</td>
</tr>
<tr>
	<td bgcolor=#ffffff align=center><input type=submit value=修　改></td>
	<td bgcolor=#ffffff align=center><input type=reset value=重　置></td>
</tr>
</table></form>~;

    if ($mystatus == 1) {
        $output =~ s/value="on"/value="on" checked/g;
    }
    else {
        $output =~ s/value="off"/value="on" checked/g;
    }

    return;
}

sub setok {
    my $newbankopen = $query->param('bankopen');
    my $newbankname = $query->param('bankname');
    my $newbankmanager = $query->param('bankmanager');
    my $newbankmessage = $query->param('bankmessage');
    my $newbanksaverate = $query->param('banksaverate');
    my $newbanktransneed = $query->param('banktransneed');
    my $newbanktransrate = $query->param('banktransrate');
    my $newbankpostrate = $query->param('bankpostrate');
    my $newbankallowloan = $query->param('bankallowloan');
    my $newbankloanmaxdays = $query->param('bankloanmaxdays');
    my $newbankloanrate = $query->param('bankloanrate');
    my $newbankrateloan = $query->param('bankrateloan');
    my $newbankmaxdeal = $query->param('bankmaxdeal');
    my $newbankmindeal = $query->param('bankmindeal');
    my $newbankmaxdisplay = $query->param('bankmaxdisplay');
    my $newbankmaxdaydo = $query->param('bankmaxdaydo');
    my $newbanklogpriviate = $query->param('banklogpriviate');
    my $newbankadminallow = $query->param('bankadminallow');

    $newbankopen = "on" if ($newbankopen ne "off");
    &seterror("还没有输入行长大名！") if ($newbankmanager eq "");
    $newbankmanager = &unHTML($newbankmanager);
    &seterror("还没有输入银行名称！") if ($newbankname eq "");
    $newbankname = &unHTML($newbankname);
    $newbankmessage = &unHTML($newbankmessage);
    &seterror("存款日利率输入错误！") if ($newbanksaverate =~ /[^0-9\.]/ or $newbanksaverate eq "");
    &seterror("存款日利率太高！") if ($newbanksaverate > 10);
    $newbanksaverate /= 100;
    &seterror("转帐汇款功能最低需要威望值输入错误！") if ($newbanktransneed =~ /[^0-9]/ or $newbanktransneed eq "");
    &seterror("转帐汇率输入错误！") if ($newbanktransrate =~ /[^0-9\.]/ or $newbanktransrate eq "");
    $newbanktransrate /= 100;
    &seterror("汇款汇率输入错误！") if ($newbankpostrate =~ /[^0-9\.]/ or $newbankpostrate eq "");
    $newbankpostrate /= 100;
    $newbankallowloan = "yes" if ($newbankallowloan ne "no");
    &seterror("贷款最长偿还期限输入错误！") if ($newbankloanmaxdays =~ /[^0-9]/ or $newbankloanmaxdays eq "");
    &seterror("贷款日利率输入错误！") if ($newbankloanrate =~ /[^0-9\.]/ or $newbankloanrate eq "");
    $newbankloanrate /= 100;
    &seterror("贷款利率必须高于存款利率！") if ($newbankloanrate <= $newbanksaverate);
    &seterror("每点威望最高抵押贷款数额输入错误！") if ($newbankrateloan =~ /[^0-9]/ or $newbankrateloan eq "");
    &seterror("单笔交易最高限额输入错误！") if ($newbankmaxdeal =~ /[^0-9]/ or $newbankmaxdeal eq "");
    &seterror("单笔交易最低限额输入错误！") if ($newbankmindeal =~ /[^0-9]/ or $newbankmindeal eq "");
    &seterror("单笔交易最高限额应该大于单笔交易最低限额！") if ($newbankmaxdeal <= $newbankmindeal);
    &seterror("首页显示的用户排名数输入错误！") if ($newbankmaxdisplay =~ /[^0-9]/ or $newbankmaxdisplay eq "");
    &seterror("首页显示的用户排名数过多！") if ($newbankmaxdisplay > 20);
    &seterror("24小时内最大交易次数输入错误！") if ($newbankmaxdaydo =~ /[^0-9]/ or $newbankmaxdaydo eq "");
    &seterror("24小时内最大交易次数过多！") if ($newbankmaxdaydo > 10);
    &seterror("个人存折最高记录条数输入错误！") if ($newbanklogpriviate =~ /[^0-9]/ or $newbanklogpriviate eq "");
    &seterror("个人存折最高记录条数过多！") if ($newbanklogpriviate > 20);
    $newbankadminallow = "allad" unless ($newbankadminallow eq "all" or $newbankadminallow eq "manager");

    my $filetomake = $lbdir . "data/ebankinfo.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    open(FILE, ">$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE qq~\# EbankMX For LB Plus is Powered By 94Cool.Net BigJim
\$bankopen = "$newbankopen";
\$bankname = "$newbankname";
\$bankmanager = "$newbankmanager";
\$bankmessage = "$newbankmessage";
\$banksaverate = $newbanksaverate;
\$banktransneed = $newbanktransneed;
\$banktransrate = $newbanktransrate;
\$bankpostrate = $newbankpostrate;
\$bankallowloan = "$newbankallowloan";
\$bankloanmaxdays = $newbankloanmaxdays;
\$bankloanrate = $newbankloanrate;
\$bankrateloan = $newbankrateloan;
\$bankmaxdeal = $newbankmaxdeal;
\$bankmindeal = $newbankmindeal;
\$bankmaxdisplay = $newbankmaxdisplay;
\$bankmaxdaydo = $newbankmaxdaydo;
\$banklogpriviate = $newbanklogpriviate;
\$bankadminallow = "$newbankadminallow";
1;~;
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");

    $output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>　如果你的浏览器没有自动返回，请<a href=$thisprog>点击这里</a>~;
    return;
}

sub editok {
    my $memid = $query->param('memid');
    &seterror("没有输入编辑的帐户名！") if ($memid eq "");
    &seterror("帐户名含有非法字符！") if (($memid =~ m/\//) || ($memid =~ m/\\/) || ($memid =~ m/\.\./));
    $memid =~ s/ /\_/sg;
    $memid =~ tr/A-Z/a-z/;

    my $newsavenums = $query->param('newsavenums');
    my $clearloan = $query->param('clearloan');
    my $accountstats = $query->param('accountstats');
    my $getpass = $query->param('getpass');
    $getpass =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    $memid = &stripMETA($memid);
    my $namenumber = &getnamenumber($memid);
    &checkmemfile($memid, $namenumber);
    my $filetoopen = "$lbdir$memdir/$namenumber/$memid.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, $filetoopen);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my $filedata = <FILE>;
        close(FILE);
        chomp($filedata);
        my ($membername, $password, $membertitle, $member_code, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/, $filedata);
        my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $mybankdotime, $bankgetpass, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

        if ($mystatus) {
            if ($mysaves != $newsavenums) {
                &logaction($in_member_name, "编辑用户 $membername 的存款从 $mysaves $moneyname到 $newsavenums $moneyname。");
                &updateallsave(0, $newsavenums - $mysaves);
                $mysaves = $newsavenums;
                &order($memid, $newsavenums);
            }

            if ($myloan && $clearloan eq "yes") {
                &logaction($in_member_name, "清除了用户 $membername $myloan $moneyname的贷款记录。");
                $myloan = 0;
                $myloantime = "";
                $myloanrating = 0;
            }

            if ($getpass ne "") {
                $bankgetpass = $getpass;
                &logaction($in_member_name, "<b>修改了用户 $membername 的取款密码。</b>");
            }

            if ($accountstats eq "on" && $mystatus == -1) {
                &bankmessage($memid, "解冻通知", "你在$bankname的账户已经被$in_member_name解冻。");
                &logaction($in_member_name, "<font color=green>解除了对用户 $membername 帐户的冻结。</font>");
                $mystatus = 1;
            }
            elsif ($accountstats eq "off" && $mystatus == 1) {
                &bankmessage($memid, "冻结通知", "你在$bankname的账户已经被$in_member_name冻结，如有疑问请与其联系。");
                &logaction($in_member_name, "<font color=red>暂时冻结了用户 $membername 的帐户。</font>");
                $mystatus = -1;
            }

            $ebankdata = "$mystatus,$mysaves,$mysavetime,$myloan,$myloantime,$myloanrating,$mybankdotime,$bankgetpass,$bankadd2,$bankadd3,$bankadd4,$bankadd5";

            if (($membername ne "") && ($password ne "")) {
                if (open(FILE, ">$filetoopen")) {
                    flock(FILE, 2) if ($OS_USED eq "Unix");
                    $lastgone = time;
                    print FILE "$membername\t$password\t$membertitle\t$member_code\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
                    close(FILE);
                }
            }
            &winunlock($filetoopen) if ($OS_USED eq "Nt");
        }
        else {
            &winunlock($filetoopen) if ($OS_USED eq "Nt");
            &seterror("用户 $memid 没有在本行开户！");
        }
    }
    else {
        &seterror("用户 $memid 不存在！");
    }

    $output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>　如果你的浏览器没有自动返回，请<a href=$thisprog>点击这里</a>~;
    return;
}

sub empty {
    my $clearday = $query->param("day");
    $clearday = 30 if ($clearday !~ /^[0-9]+$/);
    my $currenttime = time;
    my $cleartime = $currenttime - $clearday * 86400;
    my $filetomake = $lbdir . "ebankdata/alllogs.cgi";
    &winlock($filetomake) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");
    open(FILE, $filetomake);
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @alllogs = <FILE>;
    close(FILE);
    my $deletenum = 0;
    open(FILE, ">$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach (@alllogs) {
        chomp;
        my (undef, $logtime, undef) = split(/\t/, $_);
        if ($logtime < $cleartime) {
            $deletenum++;
        }
        else {
            print FILE "$_\n";
        }
    }
    print FILE "$in_member_name\t$currenttime\t<b>批量删除了银行 $clearday 天以前的过期交易日志共 $deletenum 条。</b>\n";
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Unix" || $OS_USED eq "Nt");

    $output = qq~<meta http-equiv="refresh" Content="0; url=$thisprog"><br>　如果你的浏览器没有自动返回，请<a href=$thisprog>点击这里</a>~;
    return;
}

sub seterror {
    my $message = $_[0];
    my $output = qq~
<table width=100% cellpadding=6 cellspacing=0>
<tr><td bgcolor=#2159C9><font color=#ffffff><b>欢迎来到论坛管理中心 / 银行管理发生错误</b></font></td></tr>
<tr><td bgcolor=#eeeeee><font color=#990000><b>　出错拉：</b>$message</font></td></tr>
<tr><td bgcolor=#ffffff>　　<a href="javascript:history.go(-1);">返回上一页</a></td></tr>
</table>
</td></tr></table></body></html>~;
    print $output;
    exit;
}

sub bankmessage #给用户发银行短消息（调用参数：收取人、主题、内容）
{
    my ($receivemember, $topic, $content) = @_;

    my @filedata;
    my $filetomake = $lbdir . $msgdir . "/in/" . $receivemember . "_msg.cgi";
    $filetomake = &stripMETA($filetomake);
    my $currenttime = time;
    &winlock($filetomake) if ($OS_USED eq "Nt");
    if (-e $filetomake) {
        open(FILE, $filetomake);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @filedata = <FILE>;
        close(FILE);
    }

    @filedata = ("＊＃！＆＊$bankname\tno\t$currenttime\t$topic\t$content<br><br>　　感谢使用$bankname的优质服务。<br><br>\n", @filedata);

    open(FILE, ">$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach (@filedata) {
        chomp;
        print FILE "$_\n";
    }
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");

    return;
}

sub updateallsave #利用变化量来更新总量信息
{
    my ($callusers, $callsaves) = @_;

    my $filetoopen = $lbdir . "ebankdata/allsaves.cgi";
    my $allusers = 0;
    my $allsaves = 0;
    &winlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    if (-e $filetoopen) {
        open(FILE, $lbdir . "ebankdata/allsaves.cgi");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        my $allinfo = <FILE>;
        close(FILE);
        chomp($allinfo);
        ($allusers, $allsaves) = split(/,/, $allinfo);
    }

    $allusers += $callusers;
    $allsaves += $callsaves;

    if (open(FILE, ">$filetoopen")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$allusers,$allsaves";
        close(FILE);
    }
    &winunlock($filetoopen) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));

    return;
}

sub logaction #记录银行日志（调用参数：操作人员，日志内容）
{
    my ($actionmember, $actionretail) = @_;
    my $currenttime = time;

    my $filetomake = $lbdir . "ebankdata/alllogs.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    open(FILE, ">>$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    print FILE "$actionmember\t$currenttime\t$actionretail\n";
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");

    return;
}

sub ebankadminlogin {
    if ($useverify eq 'yes') {
        if ($verifyusegd ne 'no') {
            eval ('use GD;');
            if ($@) {
                $verifyusegd = 'no';
            }
        }
        if ($verifyusegd eq 'no') {
            $houzhui = 'bmp';
        }
        else {
            $houzhui = 'png';
        }
        require 'verifynum.cgi';
    }

    print qq~
<tr>
	<td bgcolor=#2159C9 colspan=2><font color=#ffffff><b>欢迎来到银行行长办公室</b></font></td>
</tr>
<form action=$thisprog method=POST>
<input type=hidden name=action value="login">
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername" value="$in_member_name"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
~;
    print qq~
<tr>
	<td bgcolor=#ffffff valign=middle width=40% align=right><font color=#555555>请输入右边图片的数字</font></td>
	<td bgcolor=#ffffff valign=middle><input type=hidden name=sessionid value="$sessionid"><input type=text name=verifynum size=4 maxlength=4>　　<img src=$imagesurl/verifynum/$sessionid.$houzhui border=0 align=absmiddle></td>
</tr>
~ if ($useverify eq "yes");

    print qq~
<tr>
	<td bgcolor=#ffffff valign=middle colspan=2 align=center><input type=submit value="登 陆"></td>
</tr>
</form>
<tr>
	<td bgcolor=#ffffff valign=middle align=left colspan=2><font face=$font color=#555555>
		<blockquote><b>请注意</b><p><b>只有银行行长才能进入行长办公室。<br>未经过授权的尝试登录行为将会被记录在银行日志！</b><p>在进入行长办公室前，请确定你的浏览器打开了 Cookie 选项。<br> Cookie 只会存在于当前的浏览器进程中。为了安全起见，当你关闭了浏览器后，Cookie 会失效并被自动删除。</blockquote>
	</td>
</tr>
~;
    return;
}

sub order #银行排序程序
{
    my ($adduser, $addsave) = @_;
    my %ordersaves;

    my $filetoopen = $lbdir . "ebankdata/order.cgi";
    my $filetoopens = &lockfilename($filetoopen);
    return if (-e $filetoopens . ".lck");
    &winlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    if (-e $filetoopen) {
        open(FILE, $filetoopen);
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @orderdata = <FILE>;
        close(FILE);
    }
    foreach (@orderdata) {
        chomp;
        my ($tempuser, $tempsave) = split(/\t/, $_);
        $ordersaves{$tempuser} = $tempsave if ($tempuser ne "");
    }
    $ordersaves{$adduser} = $addsave if ($adduser ne "");
    my @orderusers = sort {$ordersaves{$a} <=> $ordersaves{$b}} keys(%ordersaves);
    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    for ($i = 1; $i <= $bankmaxdisplay * 2; $i++) {
        $j = @orderusers - $i;
        last if ($j < 0);
        print FILE $orderusers[$j] . "\t" . $ordersaves{$orderusers[$j]} . "\n" if ($ordersaves{$orderusers[$j]});
    }
    close(FILE);
    &winunlock($filetomake) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));

    return;
}

sub setbankonoff {
    my $status = shift;

    my $filetomake = $lbdir . "data/ebankinfo.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    open(FILE, $filetomake);
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my @tempinfo = <FILE>;
    close(FILE);
    open(FILE, ">$filetomake");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach $tempconfig (@tempinfo) {
        chomp($tempconfig);
        $tempconfig = "\$bankopen = \"$status\";" if ($tempconfig =~ /\$bankopen/);
        print FILE $tempconfig . "\n";
    }
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");
}

sub checkverify {
    my $verifynum = $query->param('verifynum');
    my $sessionid = $query->param('sessionid');
    $sessionid =~ s/[^0-9a-f]//isg;
    if (length($sessionid) != 32 && $useverify eq "yes") {
        $in_password = "";
        return;
    }
    mkdir("${lbdir}verifynum", 0777) unless (-e "${lbdir}verifynum");
    mkdir("${lbdir}verifynum/login", 0777) if (!(-e "${lbdir}verifynum/login"));

    ###获取真实的 IP 地址
    my $ipaddress = $ENV{'REMOTE_ADDR'};
    my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);
    $trueipaddress = $ENV{'HTTP_CLIENT_IP'};
    $ipaddress = $trueipaddress if ($trueipaddress ne "" && $trueipaddress ne "unknown" && $trueipaddress !~ m/^192\.168\./ && $trueipaddress !~ m/^10\./);

    ###获取当前进程的验证码和验证码产生时间、用户密码
    my $filetoopen = "${lbdir}verifynum/$sessionid.cgi";
    open(FILE, $filetoopen);
    my $content = <FILE>;
    close(FILE);
    unlink($filetoopen);
    chomp($content);
    my ($trueverifynum, $verifytime, $savedipaddress) = split(/\t/, $content);
    my $currenttime = time;

    if (($verifynum ne $trueverifynum || $currenttime > $verifytime + 300 || $ipaddress ne $savedipaddress) && ($useverify eq "yes")) { #验证码有效时间仅为5分钟
        $in_password = "";
    }
    else {
        unlink("${lbdir}verifynum/$sessionid.cgi");
        unlink("${imagesdir}verifynum/$sessionid.cgi");
        my $memberfilename = $in_member_name;
        $memberfilename =~ s/ /_/g;
        $memberfilename =~ tr/A-Z/a-z/;
        $memberfilename = "${lbdir}verifynum/login/$memberfilename.cgi";

        open(FILE, ">$memberfilename");
        print FILE "$currenttime";
        close(FILE);
    }
    return;
}