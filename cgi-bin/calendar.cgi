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

use strict;
use warnings;
use diagnostics;

use diagnostics;

use diagnostics;
use LBCGI;
use Time::Local;
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "code.cgi";
$|++;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$thisprog = "calendar.cgi";
$query = new LBCGI;

%event_list = ();
$currenttime = time;

for ('action', 'set_year', 'set_month', 'set_day') {
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}

$set_year = int($set_year);
$set_month = int($set_month);
$set_day = int($set_day);
if ($set_year + $set_month > 0) {
    &error("普通错误&老大，别乱黑我的程序呀！") unless ($set_year > 1900 && $set_month > 0 && $set_month < 13);
    $set_month -= 1;
}
@WEEK = ('星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六');
@YEAR_A = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
@YEAR_B = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
if ($set_day > 0) {
    &error("打开文件&老大，别乱黑我的程序呀！") if (($set_year % 4 == 0 && $set_day > $YEAR_B[$set_month]) || ($set_year % 4 != 0 && $set_day > $YEAR_A[$set_month]));
}
else {
    $set_day = 1;
}

$edit_event = (($set_year + $set_month > 0) && ($set_day > 0));

$YEAR_COUNT = 10;

$output = ''; #初始化输出


if (!$inmembername) {$inmembername = $query->cookie("amembernamecookie");}
if (!$inpassword) {$inpassword = $query->cookie("apasswordcookie");}
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~ m/\//) || ($inmembername =~ m/\\/) || ($inmembername =~ m/\.\./));
if ($inmembername eq "" || $inmembername eq "客人") {
    $inmembername = "客人";
    $userregistered = "no";
    &error("普通错误&客人不能使用此功能，请注册登录后再访问，谢谢！")
}
else {
    &getmember("$inmembername", "no");
    &error("普通错误&此用户根本不存在！") if ($inpassword ne "" && $userregistered eq "no");
    &error("普通错误&密码与用户名不相符，请重新登录！") if ($inpassword ne $password);
    $inmembername = $membername;
}
$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
mkdir("${lbdir}calendar", 0777) unless (-e "${lbdir}calendar");
chmod(0777, "${lbdir}calendar");

$mymembercode = $membercode;
my ($month_start, $month_end, $month_end_day);
$local_time = ($set_year + $set_month > 0) ? timelocal(0, 0, 0, $set_day, $set_month, $set_year) : $currenttime;

(undef, undef, undef, my $now_mday, my $now_mon, my $now_year, undef, undef, undef) = localtime($currenttime);
my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($local_time);

$now_year += 1900;
$now_mon += 1;
$year += 1900;
$set_year = $year;
$set_month = $mon + 1;
$set_day = $mday;

$year_display = sprintf('%04d年', $set_year);
$month_display = sprintf('%02d月', $set_month);
$date_display = sprintf('%04d年%02d月%02d日', $set_year, $set_month, $set_day);

$month_end_day = ($year % 4 == 0) ? $YEAR_B[$mon] : $YEAR_A[$mon];
$month_start = $local_time - (86400 * ($mday - 1));
$month_end = $local_time + (86400 * ($month_end_day - $mday));
my ($no, $no, $no, $no, $no, $no, $start_week, $no, $no) = localtime($month_start);
my ($no, $no, $no, $no, $no, $no, $end_week, $no, $no) = localtime($month_end);

#可選擇的列表 _S
#年
$YEAR_LIST = '';
for ($y = $now_year - $YEAR_COUNT; $y < $now_year + $YEAR_COUNT; $y++) {
    $YEAR_LIST .= sprintf('<option value="%04d">%04d年</option>', $y, $y);
}
$YEAR_LIST =~ s/value="$set_year"/value="$set_year" selected/;
#月
$MONTH_LIST = '';
for ($m = 1; $m <= 12; $m++) {
    $MONTH_LIST .= sprintf('<option value="%d">%02d月</option>', $m, $m);
}
$MONTH_LIST =~ s/value="$set_month"/value="$set_month" selected/;
#日
$DAY_LIST = '';
for ($d = 1; $d <= $month_end_day; $d++) {
    $DAY_LIST .= sprintf('<option value="%d">%02d日</option>', $d, $d);
}
$DAY_LIST =~ s/value="$set_day"/value="$set_day" selected/;
#可選擇的列表 _E


print header(-charset => 'UTF-8', -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
$catbackpic = 'background="' . $imagesurl . '/images/' . $skin . '/' . $catbackpic . '"' if ($catbackpic ne "");
&title;

if ($action eq "event") {
    &event_action if ($membercode eq "ad");
}
elsif ($action eq "getmenbrithday") {
    &getmenbrithday if ($membercode eq "ad");
}
elsif ($action eq "edit") {
    &edit_event if ($membercode eq "ad");
}
elsif ($action eq "view") {
    &view_event;
}

if (-e "${lbdir}calendar/borninfo$set_month.cgi") {
    open(MEMFILE, "${lbdir}calendar/borninfo$set_month.cgi");
    @birthdaydata = <MEMFILE>;
    close(MEMFILE);
}
else {
    open(MEMFILE, "${lbdir}data/lbmember3.cgi");
    @birthdaydata = <MEMFILE>;
    close(MEMFILE);
}
foreach (@birthdaydata) {
    chomp $_;
    next if ($_ eq "");
    (my $biruser, my $borns) = split(/\t/, $_);
    (my $biryear, my $birmon, my $birday) = split(/\//, $borns);
    $birday = $birday - 0;
    $biryear = 1900 + $biryear if ($biryear < 100);

    if (($birmon eq "0$set_month") || ($birmon eq "$set_month")) {
        $tempinfo = "$tempinfo$_\n";
        $age = $set_year - $biryear;
        if ($changed{$birday} ne "1") {
            $birdata{$birday} .= qq~<img src=$imagesurl/images/born.gif title="今天生日列表"><BR><font color=$postfontcolortwo title=$age岁生日>$biruser</font>, ~;
            $changed{$birday} = "1";
        }
        else {
            $birdata{$birday} .= qq~<font color=$postfontcolortwo title=$age岁生日>$biruser</font>, ~;
        }
    }
}
unless (-e "${lbdir}calendar/borninfo$set_month.cgi") {
    open(TFILE, ">${lbdir}calendar/borninfo$set_month.cgi");
    print TFILE "$tempinfo";
    close(TFILE);
}

$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以查看论坛月历和特别事件记录</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> → <a href="calendar.cgi">论坛月历</a> → 查看$year_display$month_display月历 <td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<style>
.TODAY {border:2px;border-style:outset;background-color:$miscbacktwo;}
</style>
<SCRIPT>valigntop()</SCRIPT>
<table border="0" cellspacing="0" cellpadding="4" width="$tablewidth" align="center" style="border:1 solid $tablebordercolor">
<tr align=center>
<td width="14%" bgcolor=$titlecolor $catbackpic><B>$WEEK[0]</td>
<td width="14%" bgcolor=$titlecolor $catbackpic><B>$WEEK[1]</td>
<td width="14%" bgcolor=$titlecolor $catbackpic><B>$WEEK[2]</td>
<td width="14%" bgcolor=$titlecolor $catbackpic><B>$WEEK[3]</td>
<td width="14%" bgcolor=$titlecolor $catbackpic><B>$WEEK[4]</td>
<td width="14%" bgcolor=$titlecolor $catbackpic><B>$WEEK[5]</td>
<td width="14%" bgcolor=$titlecolor $catbackpic><B>$WEEK[6]</td>
</tr></table>
<table border="0" cellspacing="2" cellpadding="4" width="$tablewidth" height="550" align="center" style="border:1 solid $tablebordercolor;border-top-width:0px">~;
my $month_starting = 0;
my $line_loop_end = 0;
for ($l = 0; $l < 6; $l++) {
    last if ($line_loop_end);
    #每月合计共 6 星期
    $output .= qq~
<tr>~;
    for ($i = 0; $i < 7; $i++) {
        last if ($line_loop_end);
        #每星期合计共 7 日
        if ($month_starting == 0 && $l == 0) {
            if ($i == $start_week) {
                $month_starting = 1;
            }
        }
        my $class = ($month_starting == $now_mday && $now_mon == $set_month && $now_year == $set_year) ? 'class="TODAY"' : '';
        my $fontcolor = ($class ne "") ? $fonthighlight : $fontcolormisc;
        my $bgcolor = ($month_starting) ? $miscbacktwo : $miscbackone;
        my $event_temp = '';
        $yearly_event = $lbdir . 'calendar/yearly_' . $set_month . '_' . $month_starting . '.cgi';
        $event_temp .= open_event($yearly_event) . "\n";

        $dayonly_event = $lbdir . 'calendar/dayonly_' . $set_year . '_' . $set_month . '_' . $month_starting . '.cgi';
        $event_temp .= open_event($dayonly_event) . "\n";

        $weekly_event = $lbdir . 'calendar/weekly_' . $i . '.cgi';
        $event_temp .= open_event($weekly_event) . "\n";

        $monthly_event = $lbdir . 'calendar/monthly_' . $month_starting . '.cgi';
        $event_temp .= open_event($monthly_event) . "\n";

        my $view_event = ($event_temp !~ /^[\n\s]*$/) ? '<a href="' . $thisprog . '?action=view&set_year=' . $set_year . '&set_month=' . $set_month . '&set_day=' . $month_starting . '"><img src="' . $imagesurl . '/images/openfold.gif" width="16" height="15" alt="查看完整事件" border="0"></a> ' : '';
        my $edit_event = ($membercode eq "ad") ? '<a href="' . $thisprog . '?action=event&set_year=' . $set_year . '&set_month=' . $set_month . '&set_day=' . $month_starting . '"><img src="' . $imagesurl . '/images/edit.gif" width="16" height="15" alt="编辑事件" border="0"></a> ' : '';
        if ($event_temp !~ /^[\n\s]*$/) {
            $event_temp =~ s/^\n+//;
            my @event_temp = split(/\n+/, $event_temp);
            @event_temp = splice(@event_temp, 0, 4);
            $event_temp = '';
            foreach (@event_temp) {
                my $temp_event = &temppost($_);
                $event_temp .= &lbhz($temp_event, 20) . '<br>';
            }
            chop $event_temp;
            chop $event_temp;
            chop $event_temp;
            chop $event_temp;
        }
        $event_temp =~ s/\n//isg;
        chop($birdata{$month_starting});
        chop($birdata{$month_starting});
        $birdata{$month_starting} = "<BR><BR>$birdata{$month_starting}" if ($event_temp ne "" && $birdata{$month_starting} ne "");
        $output .= qq~
<td height="110" width="14%" bgcolor="$bgcolor" valign="top"$class>~;
        $output .= qq~
<table border="0" cellspacing="1" cellpadding="0" width="100%" height="100%">
<tr><td width="65%" valign="middle" height="17">&nbsp;&nbsp;<b style="color:$fontcolor">$month_starting</b></td><td wisth="35%" valign="top" align="right">$view_event$edit_event</td></tr>
<tr><td height="*" colspan="2" valign="top" style="border:1 solid $miscbackone;padding:2px">$event_temp$birdata{$month_starting}</td></tr>
</table>~ if ($month_starting > 0);
        $output .= qq~
</td>~;
        $line_loop_end = ($month_starting + 1 > $month_end_day);
        $month_starting++ if ($month_starting > 0);
    }
    $output .= qq~
</tr>~;
}
$add_event = qq~<a href="$thisprog?action=event"><img src="$imagesurl/images/newevent.gif" width="99" height="25" alt="增加新事件" border="0"></a>&nbsp;&nbsp;[<a href=$thisprog?action=getmenbrithday>更新用户生日数据</a>]~ if ($membercode eq "ad");

$nextmonth = $set_month + 1;
$premonth = $set_month - 1;
$nextyear = $preyear = $set_year;

if ($nextmonth > 12) {
    $nextmonth = 1;
    $nextyear++;
}
if ($premonth < 1) {
    $premonth = 12;
    $preyear--;
}
$output .= qq~
</table>
<SCRIPT>valignend()</SCRIPT>
<table border="0" cellspacing="2" cellpadding="4" width="$tablewidth" align="center">
<tr>
<td width="*">$add_event</td>
<form action="$thisprog" method="GET"><td width="20%"><select name="set_year">$YEAR_LIST</select><select name="set_month">$MONTH_LIST</select> <input type="submit" value="显示月历"></td></form>
<form action="$thisprog" method="GET"><td width="10%"><input type="submit" value="显示本月"></td></form>
<td width="12%"><a href="$thisprog?set_year=$preyear&set_month=$premonth"><img src="$imagesurl/images/premonth.gif" width="52" height="12" alt="显示上一个月" border="0"></a> <a href="$thisprog?set_year=$nextyear&set_month=$nextmonth"><img src="$imagesurl/images/nextmonth.gif" width="52" height="12" alt="显示下一个月" border="0"></a></td></tr>
</table>~;

&output("$boardname - 月历", \$output);

sub view_event {
    my $event_list = '';
    my $event_count = 0;
    if ($edit_event) {
        $yearly_event = $lbdir . 'calendar/yearly_' . $set_month . '_' . $set_day . '.cgi';
        $yearly_event_contents = open_event($yearly_event);
        $yearly_event_contents =~ s/\n/<br>/g;
        &lbcode(\$yearly_event_contents);
        $event_list .= qq~
<td width="50%" height="200" valign="top" align="center">
<table width="90%" border="0" style="border:1 solid $tablebordercolor" height="100%">
<tr>
<td height="10" style="border-bottom:1 solid $tablebordercolor" bgcolor="$miscbacktwo" align=center><B>每 年 事 件</td>
</tr>
<tr>
<td valign="top" bgcolor="$miscbackone">$yearly_event_contents</td>
</tr>
</table>
</td>~, $event_count++ unless ($yearly_event_contents eq "");
            $event_list .= qq~
</tr>
<tr>~, $event_count = 0 if ($event_count == 2);

        $weekly_event = $lbdir . 'calendar/weekly_' . $wday . '.cgi';
        $weekly_event_contents = open_event($weekly_event);
        $weekly_event_contents =~ s/\n/<br>/g;
        &lbcode(\$weekly_event_contents);
        $event_list .= qq~
<td width="50%" height="200" valign="top" align="center">
<table width="90%" border="0" style="border:1 solid $tablebordercolor" height="100%">
<tr>
<td height="10" style="border-bottom:1 solid $tablebordercolor" bgcolor="$miscbacktwo" align=center><B>每 周 事 件</td>
</tr>
<tr>
<td valign="top" bgcolor="$miscbackone">$weekly_event_contents</td>
</tr>
</table>
</td>~, $event_count++ unless ($weekly_event_contents eq "");
            $event_list .= qq~
</tr>
<tr>~, $event_count = 0 if ($event_count == 2);

        $monthly_event = $lbdir . 'calendar/monthly_' . $set_day . '.cgi';
        $monthly_event_contents = open_event($monthly_event);
        $monthly_event_contents =~ s/\n/<br>/g;
        &lbcode(\$monthly_event_contents);
        $event_list .= qq~
<td width="50%" height="200" valign="top" align="center">
<table width="90%" border="0" style="border:1 solid $tablebordercolor" height="100%">
<tr>
<td height="10" style="border-bottom:1 solid $tablebordercolor" bgcolor="$miscbacktwo" align=center><B>每 月 事 件</td>
</tr>
<tr>
<td valign="top" bgcolor="$miscbackone">$monthly_event_contents</td>
</tr>
</table>
</td>~, $event_count++ unless ($monthly_event_contents eq "");
            $event_list .= qq~
</tr>
<tr>~, $event_count = 0 if ($event_count == 2);

        $dayonly_event = $lbdir . 'calendar/dayonly_' . $set_year . '_' . $set_month . '_' . $set_day . '.cgi';
        $dayonly_event_contents = open_event($dayonly_event);
        $dayonly_event_contents =~ s/\n/<br>/g;
        &lbcode(\$dayonly_event_contents);
        $event_list .= qq~
<td width="50%" height="200" valign="top" align="center">
<table width="90%" border="0" style="border:1 solid $tablebordercolor" height="100%">
<tr>
<td height="10" style="border-bottom:1 solid $tablebordercolor" bgcolor="$miscbacktwo" align=center><B>特 别 事 件</td>
</tr>
<tr>
<td valign="top" bgcolor="$miscbackone">$dayonly_event_contents</td>
</tr>
</table>
</td>~, $event_count++ unless ($dayonly_event_contents eq "");
            $event_list .= qq~
</tr>
<tr>~, $event_count = 0 if ($event_count == 2);
    }
    $event_list .= qq~<td width="50%"></td>~ if ($event_count == 1);
    $event_list =~ s/(<\/tr>\n<tr>)$//;
    $event_list = '<td  height="200" valign="middle" align="center"><u>本日没有任何事件</u></td>' if ($event_list eq "");

    $add_event = qq~<a href="$thisprog?action=event&set_year=$set_year&set_month=$set_month&set_day=$set_day"><img src="$imagesurl/images/newevent.gif" width="99" height="25" alt="增加新事件" border="0"></a>~ if ($membercode eq "ad");

    $nextday = $set_day + 1;
    $preday = $set_day - 1;
    $nextmonth = $premonth = $set_month;
    $nextyear = $preyear = $set_year;
    @YEAR_ARRAY = ($set_year % 4 == 0) ? @YEAR_B : @YEAR_A;
    if ($nextday > $YEAR_ARRAY[$set_month - 1]) {
        $nextday = 1;
        $nextmonth++;
    }
    if ($preday < 1) {
        $preday = $YEAR_ARRAY[$set_month - 2];
        $premonth--;
    }
    if ($nextmonth > 12) {
        $nextmonth = 1;
        $nextyear++;
    }
    if ($premonth < 1) {
        $premonth = 12;
        $preyear--;
    }
    my $prelink = qq~<a href="$thisprog?action=view&set_year=$preyear&set_month=$premonth&set_day=$preday"><img src="$imagesurl/images/preday.gif" width="52" height="12" alt="显示上一日" border="0"></a>~;
    if ($preyear <= $now_year - $YEAR_COUNT) {
        $prelink = qq~<img src="$imagesurl/images/preday.gif" width="52" height="12" alt="显示上一日" border="0" style=filter:gray>~;
    }
    my $nextlink = qq~<a href="$thisprog?action=view&set_year=$nextyear&set_month=$nextmonth&set_day=$nextday"><img src="$imagesurl/images/nextday.gif" width="52" height="12" alt="显示下一日" border="0"></a>~;
    if ($nextyear >= $now_year + $YEAR_COUNT) {
        $nextlink = qq~<img src="$imagesurl/images/nextday.gif" width="52" height="12" alt="显示下一日" border="0" style=filter:gray>~;
    }
    $preclass = 'style=filter:gray';
    $nextclass = 'style=filter:gray';
    $output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以查看论坛月历和特别事件记录</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> → <a href="$thisprog?set_year=$set_year&set_month=$set_month">论坛月历</a> → 查看事件<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p><SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>查看 <u>$date_display</u> 的事件</b></font></td></tr>
<tr><td bgcolor=$miscbackone align="center"><table width="80%" border="0" cellspacing="0"><tr>$event_list</tr></table></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT>
<table border="0" cellspacing="2" cellpadding="4" width="$tablewidth" align="center">
<tr>
<td width="*">$add_event</td>
<td width="12%">$prelink $nextlink</td></tr>
</table>~;
    &output("$boardname - 查看事件", \$output);
}
sub event_action {
    $action_now = ($edit_event) ? sprintf('编辑事件 [%04d年%02d月%02d日]', $set_year, $set_month, $set_day) : '增加事件';

    my ($yearly_event, $weekly_event, $monthly_event, $dayonly_event);
    my ($yearly_event_contents, $weekly_event_contents, $monthly_event_contents, $dayonly_event_contents);
    if ($edit_event) {
        $yearly_event = $lbdir . 'calendar/yearly_' . $set_month . '_' . $set_day . '.cgi';
        $yearly_event_contents = open_event($yearly_event);

        $weekly_event = $lbdir . 'calendar/weekly_' . $wday . '.cgi';
        $weekly_event_contents = open_event($weekly_event);

        $monthly_event = $lbdir . 'calendar/monthly_' . $set_day . '.cgi';
        $monthly_event_contents = open_event($monthly_event);

        $dayonly_event = $lbdir . 'calendar/dayonly_' . $set_year . '_' . $set_month . '_' . $set_day . '.cgi';
        $dayonly_event_contents = open_event($dayonly_event);
    }

    $output .= qq~
<script>
var YEAR_A = new Array(0,31,28,31,30,31,30,31,31,30,31,30,31);
var YEAR_B = new Array(0,31,29,31,30,31,30,31,31,30,31,30,31);
var YEAR_ARRAY = ($set_year%4 == 0)?YEAR_B:YEAR_A;
var select_month = $set_month;
function select_day(select_obj){
	var EVENTFORM = select_obj.form;
	if(select_obj.name == 'set_year'){
		if(select_obj.value%4 == 0){
			YEAR_ARRAY = YEAR_B;
		}else{
			YEAR_ARRAY = YEAR_A;
		}
	}else if(select_obj.name == 'set_month'){
		select_month = select_obj.value;
	}
	var month_end_day = YEAR_ARRAY[select_month];
	EVENTFORM.set_day.length = month_end_day;
	EVENTFORM.set_day.selectedIndex = 0;
	for(var d = 0;d < month_end_day;d++){
		var day = d+1;
		with(EVENTFORM.set_day){
			options[d].value = day;
			options[d].text = ((day < 10)?'0'+day:day)+'日';
		}
	}
	EVENTFORM['full_date'].innerText = '';
}
</script>
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以查看论坛月历和特别事件记录</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> → <a href="$thisprog?set_year=$set_year&set_month=$set_month">论坛月历</a> → 事件设定<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=3 cellspacing=1 border=0 width=100%>
<form action="$thisprog" method="POST" name="EVENTFORM">
<input type="hidden" name="action" value="edit">
<tr><td bgcolor=$titlecolor $catbackpic colspan="2" height="15"><font color=$titlefontcolor><b>$action_now</b></font></td></tr>
<tr>
<td width="30%" bgcolor="$miscbacktwo" valign=middle><font color=$fontcolormisc><b>事件日期</b></font></td>
<td width="70%" bgcolor="$miscbacktwo"><select name="set_year" onChange="select_day(this)">$YEAR_LIST</select><select name="set_month" onChange="select_day(this)">$MONTH_LIST</select><select name="set_day">$DAY_LIST</select></td>
</tr>
<tr>
<td width="30%" bgcolor="$miscbackone" valign=top><font color=$fontcolormisc><b>每周事件</b></font><br><br><li>在这栏填写每周也要注意的事件</td>
<td width="70%" bgcolor="$miscbackone"><textarea name="weekly_event_contents" cols="70" rows="6">$weekly_event_contents</textarea></td>
</tr>
<tr>
<td width="30%" bgcolor="$miscbackone" valign=top><font color=$fontcolormisc><b>每月事件</b></font><br><br><li>在这栏填写每月本日也要注意的事件</td>
<td width="70%" bgcolor="$miscbackone"><textarea name="monthly_event_contents" cols="70" rows="6">$monthly_event_contents</textarea></td>
</tr>
<tr>
<td width="30%" bgcolor="$miscbackone" valign=top><font color=$fontcolormisc><b>每年事件</b></font><br><br><li>在这栏填写每年本月本日也要注意的事件<li>例子：新年，圣诞，生日</td>
<td width="70%" bgcolor="$miscbackone"><textarea name="yearly_event_contents" cols="70" rows="6">$yearly_event_contents</textarea></td>
</tr>
<tr>
<td width="30%" bgcolor="$miscbackone" valign=top><font color=$fontcolormisc><b>特別事件</b></font><br><br><li>在这栏填写只要注意一次的事件</td>
<td width="70%" bgcolor="$miscbackone"><textarea name="dayonly_event_contents" cols="70" rows="6">$dayonly_event_contents</textarea></td>
</tr>
<tr>
<td bgcolor="$miscbacktwo" colspan="2" align="center">
<input type=Submit value="确 定 储 存" name=Submit>　　<input type="reset" name="Clear" value="清 除"></td>
</tr>
</form>
</table>
</td></tr></table><SCRIPT>valignend()</SCRIPT>~;
    &output("$boardname - 编辑事件", \$output);
}

sub edit_event {
    for ('weekly_event_contents', 'monthly_event_contents', 'yearly_event_contents', 'dayonly_event_contents') {
        $tp = $query->param($_);
        $tp = &cleaninput($tp);
        ${$_} = $tp;
    }
    my ($yearly_event, $weekly_event, $monthly_event, $dayonly_event);
    $yearly_event = $lbdir . 'calendar/yearly_' . $set_month . '_' . $set_day . '.cgi';
    write_event($yearly_event, $yearly_event_contents);

    $weekly_event = $lbdir . 'calendar/weekly_' . $wday . '.cgi';
    write_event($weekly_event, $weekly_event_contents);

    $monthly_event = $lbdir . 'calendar/monthly_' . $set_day . '.cgi';
    write_event($monthly_event, $monthly_event_contents);

    $dayonly_event = $lbdir . 'calendar/dayonly_' . $set_year . '_' . $set_month . '_' . $set_day . '.cgi';
    write_event($dayonly_event, $dayonly_event_contents);

    &delete_old_event; #删除过期的特别事件
    &title;
    $output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以查看论坛月历和特别事件记录</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> → <a href="$thisprog?set_year=$set_year&set_month=$set_month">论坛月历</a> → 事件设定<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>谢谢，$inmembername！您的事件已经成功储存！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！
<ul><li><a href="$thisprog?set_year=$set_year&set_month=$set_month">返回月历</a>
<li><a href="leoboard.cgi">返回论坛首页</a>
</ul></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$thisprog?set_year=$set_year&set_month=$set_month">~;
    &output("$boardname - 储存事件", \$output);
}

sub open_event {
    my $FILE_PATH = shift;
    return $event_list{$FILE_PATH} if (defined $event_list{$FILE_PATH});
    return '' unless (-e $FILE_PATH);
    &winlock($FILE_PATH) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    open(EVENTFILE, "$FILE_PATH");
    flock(EVENTFILE, 1) if ($OS_USED eq "Unix");
    $/ = '';
    my $FILE_EVENT = <EVENTFILE>;
    $/ = "\n";
    close(EVENTFILE);
    $FILE_EVENT =~ s/^＊＃！＆＊//;
    &winunlock($FILE_PATH) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    if ($FILE_EVENT =~ /^[\n|\s]*$/) {
        $FILE_EVENT = "";
        unlink($FILE_PATH);
    }
    $event_list{$FILE_PATH} = $FILE_EVENT;
    return $FILE_EVENT;
}
sub write_event {
    my ($FILE_PATH, $FILE_EVENT) = @_;
    $FILE_EVENT =~ s/<p>/\n\n/g;
    $FILE_EVENT =~ s/<br>/\n/g;
    if ($FILE_EVENT =~ /^[\n|\s]*$/) {
        unlink($FILE_PATH) if (-e $FILE_PATH);
    }
    else {
        $FILE_EVENT = '＊＃！＆＊' . $FILE_EVENT;
        my @FILE_EVENT = split(/\n+/, $FILE_EVENT);
        &winlock($FILE_PATH) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
        open(EVENTFILE, ">$FILE_PATH");
        flock(EVENTFILE, 2) if ($OS_USED eq "Unix");
        foreach (@FILE_EVENT) {
            print EVENTFILE $_ . "\n";
        }
        close(EVENTFILE);
        &winunlock($FILE_PATH) if (($OS_USED eq "Unix") || ($OS_USED eq "Nt"));
    }
}
sub delete_old_event {
    opendir(DIR, "${lbdir}calendar");
    my @event_files = readdir(DIR);
    closedir(DIR);
    chomp @event_files;
    shift @event_files;
    shift @event_files;
    my $count_end = 0;
    foreach (@event_files) {
        $count_end++;
        next unless ($_ =~ /^dayonly_/);
        last if ($count_end > 100);
        my $this_year = substr($_, 8, 4);
        next if ($this_year == $now_year);
        next if ($this_year > $now_year - $YEAR_COUNT);
        unlink("${lbdir}calendar/$_");
    }
}

sub getmenbrithday {
    &error("权限错误&对不起，本功能只限坛主使用！") if ($membercode ne "ad");
    open(MEMFILE, "${lbdir}data/lbmember3.cgi");
    @birthdaydata = <MEMFILE>;
    close(MEMFILE);
    foreach (@birthdaydata) {
        chomp $_;
        next if ($_ eq "");
        (my $biruser, my $borns) = split(/\t/, $_);
        (my $biryear, my $birmon, my $birday) = split(/\//, $borns);
        $birmon = $birmon - 0;
        next if ($birmon > 12 || $birmon < 1);
        $birdayinfo[$birmon] = "$birdayinfo[$birmon]$_\n";
    }
    for ($i = 1; $i <= 12; $i++) {
        open(FILE, ">${lbdir}calendar/borninfo$i.cgi");
        print FILE "$birdayinfo[$i]";
        close(FILE);
    }
    &title;
    $output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> 在这里您可以查看论坛月历和特别事件记录</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> → <a href="$thisprog?set_year=$set_year&set_month=$set_month">论坛月历</a> → 事件设定<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 border=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 border=0 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>所有用户生日数据已经更新！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！
<ul><li><a href="$thisprog?set_year=$set_year&set_month=$set_month">返回月历</a>
<li><a href="leoboard.cgi">返回论坛首页</a>
</ul></tr></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$thisprog?set_year=$set_year&set_month=$set_month">~;
    &output("$boardname - 更新用户生日数据", \$output);

}