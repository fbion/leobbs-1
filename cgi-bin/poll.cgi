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
use LBCGI;
use diagnostics;
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "data/cityinfo.cgi";
$|++;
$thisprog = "poll.cgi";
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

for ('forum', 'topic', 'membername', 'password', 'action', 'inshowsignature',
    'notify', 'inshowemoticons', 'intopictitle', 'intopicdescription', 'myChoice', 'inshowchgfont',
    'inpost', 'posticon', 'threadname', 'inhiddentopic', 'postweiwang', 'hidepoll', 'canpoll', 'uselbcode', 'inwater') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$in_topictitle =~ s/\\0//isg;
#$in_topictitle  =~ s/\\/&#92;/isg;
$in_topictitle = "＊＃！＆＊$in_topictitle";
$in_forum = $forum;
$in_topic = $topic;
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic) && ($in_topic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_forum) && ($in_forum !~ /^[0-9]+$/));
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

&error("普通错误&请以正确的方式访问本程序！") if (($postweiwang > $maxweiwang) && ($inhiddentopic eq "yes"));
$in_member_name = $membername;
$in_password = $password;
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}

$innotify = $notify;
$currenttime = time;
$postipaddress = &myip();
$inposticon = $posticon;
$inpost =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost .= ($uselbcode eq "yes") ? "" : "[DISABLELBCODE]" if ($action eq "addnew");
$inpost =~ s/\[USECHGFONTE\]/\[USECHGFONT\&\#069\;\]/sg;
$inpost .= ($inshowchgfont eq "yes") ? "[USECHGFONTE]" : "" if (($action eq "addnew") && ($canchgfont ne "no"));
$inpost =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;

&ipbanned; #封杀一些 ip

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($inshowemoticons ne "yes") {$inshowemoticons eq "no";}
if ($innotify ne "yes") {$innotify eq "no";}

if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if (!(-e "${lbdir}boarddata/listno$in_forum.cgi")) {&error("发表新主题&对不起，这个论坛不存在！如果确定分论坛号码没错，那么请进入管理区修复论坛一次！");}

if ($in_member_name eq "" || $in_member_name eq "客人") {
    $in_member_name = "客人";
    $userregistered = "no";
}
else {
    &getmember("$in_member_name");
    &error("普通错误&此用户根本不存在！") if ($in_password ne "" && $userregistered eq "no");
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}

&moderator("$in_forum");

&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$member_code,/);
if ($allow_users ne '') {
    &error('进入论坛&你不允许进入该论坛！') if (",$allow_users," !~ /,$in_member_name,/i && $member_code ne 'ad');
}

if ($member_code ne 'ad' && $member_code ne 'smo' && $inmembmod ne 'yes') {
    &error("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &error("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &error("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

&doonoff; #论坛开放与否

$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100) && ($maxpoststr ne ""));
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}

require "postjs.cgi";

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

$maxpollitem = 5 if (($maxpollitem eq "") || ($maxpollitem !~ /^[0-9]+$/));
$maxpollitem = 5 if ($maxpollitem < 5);
$maxpollitem = 50 if ($maxpollitem > 50);

if (($threadname) && ($threadname !~ /^[0-9]+$/)) {&error("普通错误&老大，别乱黑我的程序呀！");}
#if (($id) && ($id !~ /^[0-9]+$/)) 		  { &error("普通错误&老大，别乱黑我的程序呀！"); }

$helpurl = &helpfiles("阅读标记");
$helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

if ($arrawpostpic eq "on") {$postpicstates = "允许";}
else {$postpicstates = "禁止";}
if ($arrawpostfontsize eq "on") {$postfontsizestates = "允许";}
else {$postfontsizestates = "禁止";}
if ($arrawpostsound eq "on") {$postsoundstates = "允许";}
else {$postsoundstates = "禁止";}
if ($postjf eq "yes") {$postjfstates = "允许";}
else {$postjfstates = "禁止";}
if ($jfmark eq "yes") {$jfmarkstates = "允许";}
else {$jfmarkstates = "禁止";}
if ($hidejf eq "yes") {$hidejfstates = "允许";}
else {$hidejfstates = "禁止";}

if ($action eq "new") {&newthread;}
elsif ($action eq "addnew") {&addnewthread;}
elsif ($action eq "poll") {&poll;}
else {&error("普通错误&请以正确的方式访问本程序！$action");}

&output("$board_name - 在$forumname内发新投票", \$output);
exit;

sub newthread {
    #&getoneforum("$in_forum");

    if ($member_code ne 'ad' && $member_code ne 'smo' && $inmembmod ne 'yes') {
        &error("发起投票帖&你的积分为 $jifen，而本论坛只有积分大于等于 $pollminjf 的才能发投票帖！") if ($pollminjf > 0 && $jifen < $pollminjf);
    }

    if ($startnewthreads eq "onlysub") {&error("发表&对不起，这里是纯子论坛区，不允许发言！");}
    if (($floodcontrol eq "on") && ($member_code ne "ad") && ($inmembmod ne "yes") && ($member_code ne 'smo') && ($member_code ne 'amo') && ($member_code ne 'mo') && ($member_code ne 'cmo')) {
        ($lastpost, $posturl, $posttopic) = split(/\%\%\%/, $lastpostdate);
        $lastpost = ($lastpost + $floodcontrollimit);
        if ($lastpost > $currenttime) {
            my $lastpost1 = $lastpost - $currenttime;
            &error("发表新投票&灌水预防机制已经使用，您必须再等待 $lastpost1 秒钟才能再次发表！");
        }
    }
    $tempaccess = "forumsallowed" . "$in_forum";
    $test_entry = $query->cookie("$tempaccess");

    if ((($test_entry eq $forum_pass) && ($test_entry ne "")) || ($allowed_entry{$in_forum} eq "yes") || ($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {$allowed = "yes";}

    if ($pollopen eq "no") {&error("发表新投票&对不起，本论坛不允许发表新投票！");}

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $member_code ne "ad" && $member_code ne "smo" && $member_code ne "cmo" && $member_code ne "mo" && $member_code ne "amo" && $inmembmod ne "yes") {
        &error("发表新投票&对不起，你的删贴率超过了<b>$deletepercent</b>%，管理员不允许你发表新投票！请联系坛主解决！") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    if (($privateforum eq "yes") && ($allowed ne "yes")) {&error("发表新投票&对不起，您没有在此论坛中发表的权利！");}

    if ($emoticons eq "on") {
        $emoticonslink = qq~<li><a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">允许<B>使用</B>表情字符转换</a>~;
        $emoticonsbutton = qq~　<input type=checkbox name="inshowemoticons" value="yes" checked>您是否希望<b>使用</b>表情字符转换在您的文章中？<br>~;
    }

    if ($wwjf ne "no") {
        for (my $i = 0; $i < $maxweiwang; $i++) {
            $weiwangoption .= qq~<option value=$i>$i</option>~;
        }
        $weiwangoptionbutton = qq~　<input type=checkbox name="inhiddentopic" value="yes" >加密此帖，只对部分用户可见，用户威望至少需要  <select name=postweiwang>$weiwangoption</select><br>~;
    }
    else {
        undef $weiwangoptionbutton;
    }

    if ($nowater eq "on") {
        $nowaterpost = qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>灌水限制</b></font></td><td bgcolor=$miscbackone>　<input type="radio" class=1 name="inwater" value="no"> 不许灌水　 <input name="inwater" type="radio" class=1 value="yes" checked> 允许灌水　    [如果选择“不许灌水”，则回复不得少于 <B>$gsnum</B> 字节]</td></tr>~;
    }

    if ($canchgfont ne "no") {
        $fontpost = qq~　<input type=checkbox name="inshowchgfont" value="yes">使用字体转换？<br>~;
    }
    else {
        undef $fontpost;
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {&whosonline("$in_member_name\t$forumname\tnone\t发表新投票\t");}
        else {&whosonline("$in_member_name\t$forumname(密)\tnone\t发表新的保密投票\t");}
    }
    if ((($onlinetime + $onlinetimeadd) < $onlinepost) && ($onlinepost ne "") && ($member_code ne "ad") && ($member_code ne "smo") && ($member_code ne "cmo") && ($member_code ne "mo") && ($member_code ne "amo") && ($member_code !~ /^rz/)) {
        $onlinetime = $onlinetime + $onlinetimeadd;
        &error("发表新投票&对不起，本论坛不允许在线时间少于 $onlinepost 秒的用户发表投票！你目前已经在线 $onlinetime 秒！<BR>如果在线时间统计不正确,请重新登陆论坛一次即可解决！");
    }

    &mischeader("发表新投票");
    if ($emailfunctions eq "on") {
        if ($innotify eq "yes") {$requestnotify = " checked";}
        else {$requestnotify = "";}
        $requestnotify = qq~　<input type=checkbox name="notify" value="yes"$requestnotify>有回复时使用邮件通知您？<br>~;
    }

    if ($startnewthreads eq "no") {$startthreads = "在此论坛中新的投票和回复帖子只能由坛主、版主发表！";}
    elsif ($startnewthreads eq "follow") {$startthreads = "在此论坛中新的投票只能由坛主、版主发表！普通会员只可以跟帖！";}
    elsif ($startnewthreads eq "all") {$startthreads = "任何人均可以发表新的投票和回复帖子，未注册用户发帖密码请留空！";}
    elsif ($startnewthreads eq "cert") {$startthreads = "在此论坛中只能由坛主、版主和认证会员发表新投票！";}
    else {$startthreads = "所有注册会员均可以发表新的投票和回复帖子！";}

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $member_code ne "ad" && $member_code ne "smo" && $member_code ne "cmo" && $member_code ne "mo" && $member_code ne "amo" && $inmembmod ne "yes") {
        &error("发表新投票&对不起，你的删贴率超过了<b>$deletepercent</b>%，管理员不允许你发表新投票！请联系坛主解决！") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    if ($emoticons eq "on") {
        $output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;
    }
    if ($htmlstate eq "on") {$htmlstates = "可用";}
    else {$htmlstates = "不可用";}
    if ($idmbcodestate eq "on") {
        $idmbcodestates = "可用";
        $canlbcode = qq~　<input type=checkbox name="uselbcode" value="yes" checked>使用 LeoBBS 标签？<br>~;
    }
    else {
        $idmbcodestates = "不可用";
        $canlbcode = "";
    }
    if ($arrawpostflash eq "on") {$postflashstates = "允许";}
    else {$postflashstates = "禁止";}
    if ($useemote eq "no") {$emotestates = "不可用";}
    else {$emotestates = "可用";}

    $maxpoststr = "(帖子中最多包含 <B>$maxpoststr</B> 个字符)" if ($maxpoststr ne "");
    $Selected[$maxpollitem] = " selected";
    foreach (2 .. $maxpollitem) {
        $canpolllist .= qq~<option value="$_"$Selected[$_]>$_</option>~;
    }

    $output .= qq~<script>
var autoSave = false;
function storeCaret(textEl) {if (textEl.createTextRange) textEl.caretPos = document.selection.createRange().duplicate();if (autoSave)savePost();}
function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function DoTitle(addTitle) {
var revisedTitle; var currentTitle = document.FORM.intopictitle.value; revisedTitle = currentTitle+addTitle; document.FORM.intopictitle.value=revisedTitle; document.FORM.intopictitle.focus();
return; }</script>
<form action="$thisprog" method=post name="FORM">
<input type=hidden name="action" value="addnew">
<input type=hidden name="forum" value="$in_forum">
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>谁可以发表？</b> $startthreads</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>投票标题</b></font>　
<select name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
<OPTION selected value="">选择话题</OPTION> <OPTION value=[原创]>[原创]</OPTION><OPTION value=[转帖]>[转帖]</OPTION> <OPTION value=[灌水]>[灌水]</OPTION><OPTION value=[讨论]>[讨论]</OPTION> <OPTION value=[求助]>[求助]</OPTION><OPTION value=[推荐]>[推荐]</OPTION> <OPTION value=[公告]>[公告]</OPTION><OPTION value=[注意]>[注意]</OPTION> <OPTION value=[贴图]>[贴图]</OPTION><OPTION value=[建议]>[建议]</OPTION> <OPTION value=[下载]>[下载]</OPTION><OPTION value=[分享]>[分享]</OPTION></SELECT></td>
<td bgcolor=$miscbackone>　<input type=text size=60 maxlength=80 name="intopictitle">　不得超过 40 个汉字</td></tr>$nowaterpost
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$in_member_name</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone>　<input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone>　<input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>投票项目</b><br><li>每行一个投票项目，最多 <B>$maxpollitem</b> 项<BR><li>超过自动作废，空行自动过滤<BR><li>如果投票需要多选，请在选择中打钩</font></td>
<td bgcolor=$miscbackone valign=top>
　<TEXTAREA cols=80 name=posticon rows=6 wrap=soft >$posticon</TEXTAREA><BR>
　<input type=checkbox name="inshowsignature" value="yes">最多可投<select name="canpoll">$canpolllist</select>项　 <input type=checkbox name="hidepoll" value="yes">是否必须投票后才可查看结果？<br>
</td></tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>内容</b>　$maxpoststr<p>在此论坛中：<br>
<li>HTML 　标签: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE　标签</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a>: <b>$idmbcodestates</b><li>贴图标签 　: <b>$postpicstates</b><li>Flash 标签 : <b>$postflashstates</b><li>音乐标签 　: <b>$postsoundstates</b><li>文字大小 　: <b>$postfontsizestates</b><li>帖数标签 　: <b>$postjfstates</b><li>积分标签 　: <b>$jfmarkstates</b><li>保密标签 　: <b>$hidejfstates</b>$emoticonslink</font></td>
<td bgcolor=$miscbackone>
    ~;
    $output .= qq~$insidejs<TEXTAREA cols=80 name=inpost rows=8 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$inpost</TEXTAREA><br>
&nbsp; 模式:<input type="radio" name="mode" value="help" onClick="thelp(1)">帮助　<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">完全　<input type="radio" name="mode" value="basic"  onClick="thelp(0)">基本　　>> <a href=javascript:HighlightAll('FORM.inpost')>复制到剪贴板</a> | <a href=javascript:checklength(document.FORM);>查看长度</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">转换剪贴板超文本</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<
</td></tr></tr>~;

    if ($emoticons eq "on") {
        $output .= qq~<tr><td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>点击表情图即可在帖子中加入相应的表情</B></font><br>&nbsp;~;
        if (open(FILE, "${lbdir}data/lbemot.cgi")) {
            @emoticondata = <FILE>;
            close(FILE);
            chomp @emoticondata;
            $emoticondata = @emoticondata;
        }
        $maxoneemot = 16 if ($maxoneemot <= 5);
        if ($maxoneemot > $emoticondata) {
            foreach (@emoticondata) {
                my $smileyname = $_;
                $smileyname =~ s/\.gif$//ig;
                $output .= qq~<img src=$imagesurl/emot/$_ border=0 onClick="smilie('$smileyname');FORM.inpost.focus()" style="cursor:hand"> ~;
            }
        }
        else {
            my $emoticondata = "'" . join("', '", @emoticondata) . "'";
            $output .= qq~
<table><tr><td id=emotbox></td></tr></table>
<script>
var emotarray=new Array ($emoticondata);
var limit=$maxoneemot;
var eofpage=ceil(emotarray.length/limit);
var page=0;
function ceil(x){return Math.ceil(x)}
function emotpage(topage){
var beginemot=(page+topage-1)*limit;
var endemot=(page+topage)*limit ;
var out='';
page=page+topage;
if (page != 1) { out += '<span style=cursor:hand onclick="emotpage(-1)" title=上一页><font face=webdings size=+1>7</font></span> '; }
for (var i=beginemot;i<emotarray.length && i < endemot ;i++){out += ' <img src=$imagesurl/emot/' + emotarray[i] + ' border=0 onClick="smilie(\\'' + emotarray[i].replace(".gif", "") + '\\');FORM.inpost.focus()" style=cursor:hand> ';}
if (page != eofpage){ out += ' <span style=cursor:hand onclick="emotpage(1)" title=下一页><font face=webdings size=+1>8</font></span>'; }
out += '  第 '+ page+' 页，总共 '+ eofpage+ ' 页，共 '+emotarray.length+' 个';
out += '  <B><span style=cursor:hand onclick="showall()" title="显示所有表情图示">[显示所有]</span></B>';
emotbox.innerHTML=out;
}
emotpage (1);
function showall (){var out ='';for (var i=0;i<emotarray.length;i++){out += ' <img src=$imagesurl/emot/' + emotarray[i] + ' border=0 onClick="smilie(\\'' + emotarray[i].replace(".gif", "") + '\\');FORM.inpost.focus()" style=cursor:hand> ';}emotbox.innerHTML=out;}
</script>
~;
        }
        $output .= qq~</td></tr>~;
    }
    $output .= qq~<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>选项</b><p>$helpurl</font></td>
<td bgcolor=$miscbacktwo><font color=$fontcolormisc>$canlbcode$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton<BR></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=Submit value="发 布" name="Submit"  onClick="return clckcntr();">　　<input type=button value='预 览' name=Button onclick=gopreview()>　　<input type="reset" name="Clear" value="清 除"></td></form></tr>
</table></tr></td></table>
<SCRIPT>valignend()</SCRIPT>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$in_forum"></form>
<script>
function gopreview(){
document.preview.body.value=document.FORM.inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.preview.submit()
}
</script>
</table></tr></td></table>
    ~;
}

sub addnewthread {
    #&getoneforum("$in_forum");

    if ($member_code ne 'ad' && $member_code ne 'smo' && $inmembmod ne 'yes') {
        &error("发起投票帖&你的积分为 $jifen，而本论坛只有积分大于等于 $pollminjf 的才能发投票帖！") if ($pollminjf > 0 && $jifen < $pollminjf);
    }

    &error("出错&请不要用外部连接本程序！") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '') && ($canotherlink ne "yes"));
    if ($startnewthreads eq "onlysub") {&error("发表&对不起，这里是纯子论坛区，不允许发言！");}
    if (($floodcontrol eq "on") && ($member_code ne 'smo') && ($member_code ne 'cmo') && ($member_code ne 'amo') && ($member_code ne 'mo') && ($member_code ne "ad") && ($inmembmod ne "yes")) {
        ($lastpost, $posturl, $posttopic) = split(/\%\%\%/, $lastpostdate);
        $lastpost = ($lastpost + $floodcontrollimit);
        if ($lastpost > $currenttime) {
            my $lastpost1 = $lastpost - $currenttime;
            &error("发表新投票&灌水预防机制已经使用，您必须再等待 $lastpost1 秒钟才能再次发表！");
        }
    }

    &error("发表新投票&对不起，本论坛不允许发表超过 <B>$maxpoststr</B> 个字符的文章！") if ((length($inpost) > $maxpoststr) && ($maxpoststr ne "") && ($member_code ne "ad") && ($member_code ne 'smo') && ($member_code ne 'cmo') && ($member_code ne "mo") && ($member_code ne "amo") && ($member_code !~ /^rz/) && ($inmembmod ne "yes"));
    &error("发表新投票&对不起，本论坛不允许发表少于 <B>$minpoststr</B> 个字符的文章！") if ((length($inpost) < $minpoststr) && ($minpoststr ne "") && ($member_code ne "ad") && ($member_code ne 'smo') && ($member_code ne 'cmo') && ($member_code ne "mo") && ($member_code ne "amo") && ($member_code !~ /^rz/) && ($inmembmod ne "yes"));

    if ($pollopen eq "no") {&error("发表新投票&对不起，本论坛不允许发表新投票！");}

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $member_code ne "ad" && $member_code ne "smo" && $member_code ne "cmo" && $member_code ne "mo" && $member_code ne "amo" && $inmembmod ne "yes") {
        &error("发表新投票&对不起，你的删贴率超过了<b>$deletepercent</b>%，管理员不允许你发表新投票！请联系坛主解决！") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        if ($privateforum ne "yes") {&whosonline("$in_member_name\t$forumname\tnone\t发表新投票\t");}
        else {&whosonline("$in_member_name\t$forumname(密)\tnone\t发表新的保密投票\t");}
    }

    if ((($onlinetime + $onlinetimeadd) < $onlinepost) && ($onlinepost ne "") && ($member_code ne "ad") && ($member_code ne "smo") && ($member_code ne "cmo") && ($member_code ne "mo") && ($member_code ne "amo") && ($member_code !~ /^rz/)) {
        $onlinetime = $onlinetime + $onlinetimeadd;
        &error("发表新投票&对不起，本论坛不允许在线时间少于 $onlinepost 秒的用户发表投票！你目前已经在线 $onlinetime 秒！<BR>如果在线时间统计不正确,请重新登陆论坛一次即可解决！");
    }

    if (($userregistered eq "no") && (length($in_member_name) > 12)) {&error("发表新主题&您输入的用户名太长，请控制在6个汉字内！");}
    if (($userregistered eq "no") && ($in_member_name =~ /^客人/)) {&error("发表新主题&请不要在用户名的开头中使用客人字样！");}

    $inposticon =~ s/<p>/<BR>/isg;
    $inposticon =~ s/<BR><BR>/<BR>/isg;
    $inposticon =~ s/(.*)<BR>$/$1/i;
    $inposticon =~ s/^<BR>(.*)/$1/i;
    $inposticon =~ s/<BR>(\s*)/<BR>/i;
    $inposticon =~ s/(\s*)<BR>/<BR>/i;

    $inposticontemp = $inposticon;
    $inposticontemp =~ s/<br>/\t/ig;
    @temppoll = split(/\t/, $inposticontemp);
    $temppoll = @temppoll;

    if (($userregistered eq "no") && ($startnewthreads ne "all")) {&error("发表新主题&您没有注册！");}
    elsif ((($in_password ne $password) && ($userregistered ne "no")) || (($in_password ne "") && ($userregistered eq "no"))) {&error("发表新主题&您的密码错误！");}
    elsif (($member_code eq "banned") || ($member_code eq "masked")) {&error("添加回复&您被禁止发言或者发言被屏蔽，请联系管理员解决！");}
    elsif ($in_topictitle eq "") {&error("发表新投票&必须输入主题标题！");}
    elsif (length($in_topictitle) > 92) {&error("发表新投票&主题标题过长！");}
    elsif ($inposticon !~ m/<br>/i) {&error("发表新投票&投票选项太少！");}
    elsif ($temppoll > $maxpollitem) {&error("发表新投票&投票选项过多，不能超过 $maxpollitem 项！(您此次投票的选项有 $temppoll 项)");}
    else {
        if ($startnewthreads eq "no") {
            unless ($member_code eq "ad" || $member_code eq 'smo' || $inmembmod eq "yes") {&error("发表新投票&在此论坛中只能由坛主或者版主发表新投票！");}
        }
        elsif (($startnewthreads eq "follow") && ($action eq "addnew")) {
            unless ($member_code eq "ad" || $member_code eq 'smo' || $inmembmod eq "yes") {&error("发表新投票&在此论坛中只能由坛主或者版主发表新投票！");}
        }
        elsif ($startnewthreads eq "cert") {
            unless ($member_code eq "ad" || $member_code eq 'smo' || $inmembmod eq "yes" || $member_code eq 'cmo' || $member_code eq 'mo' || $member_code eq 'amo' || $member_code =~ /^rz/) {&error("发表新投票&在此论坛中只能由坛主、版主和认证会员发表新投票！");}
        }
        elsif (($startnewthreads eq "all") && ($userregistered eq "no")) {
            $in_member_name = "$in_member_name(客)";
        }

        $in_topictitle =~ s/\(无内容\)$//;
        $in_topictitle =~ s/()+//isg;
        my $tempintopictitle = $in_topictitle;
        $tempintopictitle =~ s/ //g;
        $tempintopictitle =~ s/\&nbsp\;//g;
        $tempintopictitle =~ s/　//isg;
        $tempintopictitle =~ s///isg;
        $tempintopictitle =~ s/^＊＃！＆＊//;
        if ($tempintopictitle eq "") {&error("发表新投票&主题标题有问题！");}
        $inpost =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;
        $inpost = "\[watermark\]$inpost\[\/watermark\]" if (($in_topictitle =~ /\[原创\]/) && ($usewm ne "no"));

        $tempaccess = "forumsallowed" . "$in_forum";
        $test_entry = $query->cookie("$tempaccess");
        if (($allowed_entry{$in_forum} eq "yes") || (($test_entry eq $forum_pass) && ($test_entry ne "")) || ($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {$allowed = "yes";}
        if (($privateforum eq "yes") && ($allowed ne "yes")) {&error("发表投票&对不起，您不允许在此论坛发表投票！");}

        if ($useemote eq "yes") {
            $filetoopen = "$lbdir" . "data/emote.cgi";
            open(FILE, "$filetoopen");
            flock(FILE, 1) if ($OS_USED eq "Unix");
            $emote = <FILE>;
            close(FILE);
        }
        else {undef $emote;}

        if ($emote && $inpost =~ m/\/\/\//) {
            study($inpost);
            my @pairs1 = split(/\&/, $emote);
            foreach (@pairs1) {
                my ($toemote, $beemote) = split(/=/, $_);
                chomp $beemote;
                $beemote =~ s/对象/〖$in_member_name〗/isg;
                $inpost =~ s/$toemote/$beemote/isg;
                last unless ($inpost =~ m/\/\/\//);
            }
        }

        undef $newthreadnumber;
        $filetoopen = "$lbdir" . "boarddata/lastnum$in_forum.cgi";
        if (open(FILE, "$filetoopen")) {
            $newthreadnumber = <FILE>;
            close(FILE);
            chomp $newthreadnumber;
            $newthreadnumber++;
        }

        if ((!(-e "${lbdir}forum$in_forum/$newthreadnumber.pl")) && ($newthreadnumber =~ /^[0-9]+$/)) {
            if (open(FILE, ">$filetoopen")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE $newthreadnumber;
                close(FILE);
            }
        }
        else {
            opendir(DIR, "${lbdir}forum$in_forum");
            my @dirdata = readdir(DIR);
            closedir(DIR);
            @dirdata = grep (/.thd.cgi$/, @dirdata);
            @dirdata = sort {$b <=> $a} (@dirdata);
            $highest = $dirdata[0];
            $highest =~ s/.thd.cgi$//;
            $newthreadnumber = $highest + 1;
            if (open(FILE, ">$filetoopen")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE $newthreadnumber;
                close(FILE);
            }
        }
        my $oldthreadnumber = $newthreadnumber - 1;
        if (open(FILE, "${lbdir}forum$in_forum/$oldthreadnumber.thd.cgi")) {
            flock(FILE, 1) if ($OS_USED eq "Unix");
            my $threaddata = <FILE>;
            close(FILE);
            (my $amembername, my $atopictitle, my $no, my $no, my $no, my $no, my $apost, my $no) = split(/\t/, $threaddata);
            if (($amembername eq $in_member_name) && (($apost eq $inpost) && ($apost ne "") || ($atopictitle eq $in_topictitle) || ($aposticon eq $inposticon))) {
                if (open(FILE, ">${lbdir}boarddata/lastnum$in_forum.cgi")) {
                    flock(FILE, 2) if ($OS_USED eq "Unix");
                    print FILE $oldthreadnumber;
                    close(FILE);
                }
                &error("发表新投票&请不要重复发投票，已经存在与此投票主题相同或者内容相同的而且是你发的投票了！");
            }
        }

        my $temp = &dofilter("$in_topictitle\t$inpost");
        ($in_topictitle, $inpost) = split(/\t/, $temp);
        $in_topictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
        $in_topictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
        $in_topictitle =~ s/(o|O)R/$1&#82;/sg;
        $in_topictitle =~ s/(o|O)r/$1&#114;/sg;
        #	$in_topictitle  =~ s/\\/&#92;/isg;

        $in_topictitletemp = $in_topictitle;
        $in_topictitletemp =~ s/^＊＃！＆＊//;

        if ($privateforum ne "yes") {
            $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
            my $filetoopens = &lockfilename($filetomakeopen);
            if (!(-e "$filetoopens.lck")) {
                if (-e $filetomakeopen) {
                    &winlock($filetomakeopen) if ($OS_USED eq "Nt");
                    open(FILE, "$filetomakeopen");
                    flock(FILE, 1) if ($OS_USED eq "Unix");
                    my @recentposts = <FILE>;
                    close(FILE);
                    $recentposts = @recentposts;
                    $maxpostreport = 31;
                    if ($recentposts < $maxpostreport) {$maxpostreport = $recentposts;}
                    else {$maxpostreport--;}
                    if (open(FILE, ">$filetomakeopen")) {
                        flock(FILE, 2) if ($OS_USED eq "Unix");
                        print FILE "$in_forum\t$newthreadnumber\t$in_topictitletemp\t$currenttime\t$inposticon\t$in_member_name\t\n";
                        for ($i = 0; $i < $maxpostreport; $i++) {print FILE $recentposts[$i];}
                        close(FILE);
                    }
                    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
                }
                else {
                    if (open(FILE, ">$filetomakeopen")) {
                        print FILE "$in_forum\t$newthreadnumber\t$in_topictitletemp\t$currenttime\t$inposticon\t$in_member_name\t\n";
                        close(FILE);
                    }
                }
            }
            else {
                unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
            }
        }

        $canpoll = $temppoll if ($canpoll > $temppoll || $canpoll =~ m/[^0-9]/);
        $inshowsignature .= $canpoll if ($inshowsignature ne "no");

        $inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

        if ($inhiddentopic eq "yes") {
            $inposttemp = "(保密)";
            $inpost = "LBHIDDEN[$postweiwang]LBHIDDEN" . $inpost;
        }
        else {
            $inposttemp = $inpost;
            $inposttemp = &temppost($inposttemp);
            chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp, 50);
        }
        $inpost =~ s/\[hidepoll\]//isg;
        $inpost .= "[hidepoll]" if ($hidepoll eq "yes");

        if (open(FILE, ">${lbdir}forum$in_forum/$newthreadnumber.pl")) {
            print FILE "$newthreadnumber\t$in_topictitle\t$in_topicdescription\tpoll\t0\t0\t$in_member_name\t$currenttime\t\t$currenttime\t<BR>\t$inposttemp\t\t";
            close(FILE);
        }
        if (open(FILE, ">${lbdir}forum$in_forum/$newthreadnumber.thd.cgi")) {
            print FILE "$in_member_name\t$in_topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t$inwater\t\n";
            close(FILE);
        }

        $file = "$lbdir" . "boarddata/listno$in_forum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open(LIST, "$file");
        flock(LIST, 2) if ($OS_USED eq "Unix");
        sysread(LIST, $listall, (stat(LIST))[7]);
        close(LIST);
        $listall =~ s/\r//isg;

        if (length($listall) > 500) {
            if (open(LIST, ">$file")) {
                flock(LIST, 2) if ($OS_USED eq "Unix");
                print LIST "$newthreadnumber\n$listall";
                close(LIST);
            }
            &winunlock($file) if ($OS_USED eq "Nt");
            if (open(LIST, ">>${lbdir}boarddata/listall$in_forum.cgi")) {
                print LIST "$newthreadnumber\t$in_topictitletemp\t$in_member_name\t$currenttime\t\n";
                close(LIST);
            }
        }
        else {
            &winunlock($file) if ($OS_USED eq "Nt");
            require "rebuildlist.pl";
            my $truenumber = rebuildLIST(-Forum => "$in_forum");
            ($tpost, $treply) = split(/\|/, $truenumber);
        }

        $cleanmembername = $in_member_name;
        $cleanmembername =~ s/ /\_/isg;
        $cleanmembername =~ tr/A-Z/a-z/;
        if ($forumallowcount ne "no") {
            $numberofposts++;
            $mymoney += $forumpostmoney - $addmoney if ($forumpostmoney ne "");
        }
        $lastpostdate = "$currenttime\%\%\%topic.cgi?forum=$in_forum&topic=$newthreadnumber\%\%\%$in_topictitletemp" if ($privateforum ne "yes");
        chomp $lastpostdate;

        if (($userregistered ne "no") && ($password ne "")) {
            my $namenumber = &getnamenumber($cleanmembername);
            &checkmemfile($cleanmembername, $namenumber);
            $filetomake = "$lbdir" . "$memdir/$namenumber/$cleanmembername.cgi";
            &winlock($filetomake) if ($OS_USED eq "Nt");
            if ((open(FILE, ">$filetomake")) && ($in_member_name ne "")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE "$membername\t$password\t$membertitle\t$member_code\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
                close(FILE);
            }
            &winunlock($filetomake) if ($OS_USED eq "Nt");
            unlink("${lbdir}cache/myinfo/$cleanmembername.pl");
            if (((-M "${lbdir}cache/meminfo/$cleanmembername.pl") * 86400 > 60 * 2) || (!(-e "${lbdir}cache/meminfo/$cleanmembername.pl"))) {
                require "getnameinfo.pl" if ($onloadinfopl ne 1);
                &getmemberinfo($cleanmembername);
            }
        }

        my $nowtime = &shortdate($currenttime + $timezone * 3600);

        my $filetoopens = "$lbdir/data/todaypost.cgi";
        $filetoopens = &lockfilename($filetoopens);
        if (!(-e "$filetoopens.lck")) {
            &winlock("$lbdir/data/todaypost.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            if (-e "$lbdir/data/todaypost.cgi") {
                open(FILE, "+<$lbdir/data/todaypost.cgi");
                $todaypost = <FILE>;
                chomp $todaypost;
                my ($nowtoday, $todaypostno, $maxday, $maxdaypost, $yestdaypost) = split(/\t/, $todaypost);
                if ($nowtoday eq $nowtime) {
                    $todaypostno++;
                    if ($todaypostno > $maxdaypost) {
                        $maxday = $nowtime;
                        $maxdaypost = $todaypostno;
                    }
                }
                else {
                    opendir(CATDIR, "${lbdir}cache");
                    @dirdata = readdir(CATDIR);
                    closedir(CATDIR);
                    @dirdata = grep (/forumcache/, @dirdata);
                    foreach (@dirdata) {unlink("${lbdir}cache/$_");}
                    $nowtoday = $nowtime;
                    $yestdaypost = $todaypostno;
                    $todaypostno = 1;
                }
                seek(FILE, 0, 0);
                print FILE "$nowtoday\t$todaypostno\t$maxday\t$maxdaypost\t$yestdaypost\t";
                close(FILE);
            }
            else {
                open(FILE, ">$lbdir/data/todaypost.cgi");
                print FILE "$nowtime\t1\t$nowtime\t1\t0\t";
                close(FILE);
            }
            &winunlock("$lbdir/data/todaypost.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        }

        $filetoopen = "${lbdir}boarddata/foruminfo$in_forum.cgi";
        my $filetoopens = &lockfilename($filetoopen);
        if (!(-e "$filetoopens.lck")) {
            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            open(FILE, "+<$filetoopen");
            ($no, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/, <FILE>);

            $lastposter = $in_member_name;
            $lastposttime = $currenttime;
            if (($tpost ne "") && ($treply ne "")) {
                $threads = $tpost;
                $posts = $treply;
            }
            else {$threads++;}
            my ($todayforumpost, $todayforumposttime) = split(/\|/, $todayforumpost);
            if (($nowtime ne $todayforumposttime) || ($todayforumpost eq "")) {$todayforumpost = 1;}
            else {$todayforumpost++;}
            $todayforumpost = "$todayforumpost|$nowtime";
            $lastposttime = "$lastposttime\%\%\%$newthreadnumber\%\%\%$in_topictitletemp";
            seek(FILE, 0, 0);
            print FILE "$lastposttime\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
            $posts = 0 if ($posts eq "");
            $threads = 0 if ($threads eq "");
            open(FILE, ">${lbdir}boarddata/forumposts$in_forum.pl");
            print FILE "\$threads = $threads;\n\$posts = $posts;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            if ($threads < 10) {
                opendir(CATDIR, "${lbdir}cache");
                @dirdata = readdir(CATDIR);
                closedir(CATDIR);
                @dirdata = grep (/forumcache/, @dirdata);
                foreach (@dirdata) {unlink("${lbdir}cache/$_");}
            }
        }
        else {
            unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
        }

        require "$lbdir" . "data/boardstats.cgi";
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        my $filetoopens = &lockfilename($filetomake);
        if (!(-e "$filetoopens.lck")) {
            $totalthreads++;
            &winlock($filetomake) if ($OS_USED eq "Nt");
            if (open(FILE, ">$filetomake")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
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

        if (($emailfunctions eq "on") && ($innotify eq "yes")) {
            $filetomake = "$lbdir" . "forum$in_forum/$newthreadnumber.mal.pl";
            if (open(FILE, ">$filetomake")) {
                print FILE "$in_member_name\t$emailaddress\t\n";
                close(FILE);
            }
        }

        &mischeader("新投票发表成功");

        opendir(CATDIR, "${lbdir}cache");
        @dirdata = readdir(CATDIR);
        closedir(CATDIR);

        unlink("${lbdir}cache/plcache$in_forum\_0.pl");

        if ($refreshurl == 1) {$relocurl = "topic.cgi?forum=$in_forum&topic=$newthreadnumber";}
        else {$relocurl = "forums.cgi?forum=$in_forum";}
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>谢谢！您的新投票已经发表成功！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！
<ul><li><a href="topic.cgi?forum=$in_forum&topic=$newthreadnumber">返回新投票</a>
<li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a>
	<li><a href="postings.cgi?action=locktop&forum=$in_forum&topic=$newthreadnumber">新主题固顶</a>
	<li><a href="postings.cgi?action=catlocktop&forum=$in_forum&topic=$newthreadnumber">新主题区固顶</a>
	<li><a href="postings.cgi?action=abslocktop&forum=$in_forum&topic=$newthreadnumber">新主题总固顶</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;

    }
}

sub poll {
    #    if (($in_select_style ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
    #     else { if (-e "${lbdir}data/style${id}.cgi") { require "${lbdir}data/style${id}.cgi"; } }
    #&getoneforum("$in_forum");

    if ($member_code ne 'ad' && $member_code ne 'smo' && $inmembmod ne 'yes') {
        &error("投票&你的积分为 $jifen，而本论坛只有积分大于等于 $polledminjf 的才能进行投票！") if ($polledminjf > 0 && $jifen < $polledminjf);
    }

    &error("出错&请不要用外部连接本程序！") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '') && ($canotherlink ne "yes"));
    if ($startnewthreads eq "onlysub") {&error("发表&对不起，这里是纯子论坛区，不允许发言！");}
    if ($startnewthreads eq "no") {
        unless ($member_code eq "ad" || $member_code eq 'smo' || $inmembmod eq "yes") {
            &error("无权投票&在此论坛中只能由坛主或者版主投票！");
        }
    }
    elsif (($startnewthreads eq "follow") && ($action eq "addnew")) {
        unless ($member_code eq "ad" || $member_code eq 'smo' || $inmembmod eq "yes") {
            &error("无权投票&在此论坛中只能由坛主或者版主投票！");
        }
    }
    elsif ($startnewthreads eq "cert") {
        unless ($member_code eq "ad" || $member_code eq 'smo' || $inmembmod eq "yes" || $member_code eq 'cmo' || $member_code eq 'amo' || $member_code eq 'mo' || $member_code =~ /^rz/) {
            &error("无权投票&在此论坛中只能由坛主、版主和认证会员投票！");
        }
    }

    undef @myChoice;
    @myChoice = $query->param('myChoice');

    if ((($onlinetime + $onlinetimeadd) < $onlinepost) && ($onlinepost ne "") && ($member_code ne "ad") && ($member_code ne "smo") && ($member_code ne "cmo") && ($member_code ne "mo") && ($member_code ne "amo") && ($member_code !~ /^rz/)) {
        $onlinetime = $onlinetime + $onlinetimeadd;
        &error("发表新投票&对不起，本论坛不允许在线时间少于 $onlinepost 秒的用户投票！你目前已经在线 $onlinetime 秒！<BR>如果在线时间统计不正确,请重新登陆一次即可解决！");
    }

    &error("投票错误&你是客人无权投票！") if (($in_member_name eq "客人") || ($in_member_name eq ""));
    if (($member_code eq "banned") || ($member_code eq "masked")) {&error("投票错误&您被禁止发言或者发言被屏蔽，请联系管理员解决！");}

    $filetomake = "$lbdir" . "forum$in_forum/$threadname.poll.cgi";
    &winlock($filetomake) if ($OS_USED eq "Nt");
    open(FILE, "$filetomake");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @allpoll = <FILE>;
    close(FILE);
    &winunlock($filetomake) if ($OS_USED eq "Nt");
    foreach (@allpoll) {
        (my $tmpinmembername, my $tmpmyChoice) = split(/\t/, $_);
        $tmpinmembername =~ s/^＊！＃＆＊//isg;
        &error("投票错误&你已经投过票了，不能再投！") if (lc($tmpinmembername) eq lc($in_member_name));
    }

    my $file = "$lbdir" . "forum$in_forum/$threadname.thd.cgi";
    &winlock($file) if ($OS_USED eq "Nt");
    open(ENT, $file);
    flock(ENT, 1) if ($OS_USED eq "Unix");
    $in = <ENT>;
    close(ENT);
    &winunlock($file) if ($OS_USED eq "Nt");
    @tempdata = split(/\t/, $in);
    $tempdata[4] = "yes$maxpollitem" if ($tempdata[4] eq "yes");
    if ($tempdata[4] =~ /^yes[0-9]+$/) {
        $tempdata[4] =~ s/^yes//;
        $myChoiceNo = @myChoice;
        &error("投票错误&选择项目不可超出最多可投数！") if ($myChoiceNo > $tempdata[4]);
    }
    else {
        $myChoiceNo = @myChoice;
        &error("投票错误&本投票不允许多选！") if ($myChoiceNo > 1);
    }

    $myChoicenow = 0;

    &winlock($filetomake) if ($OS_USED eq "Nt");
    if (open(FILE, ">$filetomake")) {
        flock(FILE, 2) if ($OS_USED eq "Unix");
        foreach (@allpoll) {
            chomp $_;
            print FILE "$_\n";

        }
        foreach $myChoice (@myChoice) {
            if (($myChoice ne "") && ($myChoice =~ /^[0-9]+$/)) {
                print FILE "＊！＃＆＊$in_member_name\t$myChoice\t\n";
                $myChoicenow = 1;
            }
        }
        close(FILE);
    }
    &winunlock($filetomake) if ($OS_USED eq "Nt");

    &error("投票错误&你未选投票，请重投！") if ($myChoicenow eq 0);

    $file = "$lbdir" . "boarddata/listno$in_forum.cgi";
    $filetoopens = &lockfilename($file);
    if (!(-e "$filetoopens.lck")) {
        &winlock($file) if ($OS_USED eq "Unix");
        open(LIST, "$file");
        flock(LIST, 2) if ($OS_USED eq "Unix");
        sysread(LIST, $listall, (stat(LIST))[7]);
        close(LIST);
        $listall =~ s/\r//isg;

        $listall =~ s/(.*)(^|\n)$threadname\n(.*)/$threadname\n$1$2$3/;
        if (length($listall) > 500) {
            if (open(LIST, ">$file")) {
                flock(LIST, 2) if ($OS_USED eq "Unix");
                print LIST $listall;
                close(LIST);
            }
            &winunlock($file) if ($OS_USED eq "Unix");
        }
        else {
            &winunlock($file) if ($OS_USED eq "Unix");
            require "rebuildlist.pl";
            rebuildLIST(-Forum => "$in_forum");
        }
    }
    #$in_forum=$id;
    &mischeader("投票成功");
    if ($refreshurl == 1) {$relocurl = "topic.cgi?forum=$in_forum&topic=$threadname";}
    else {$relocurl = "forums.cgi?forum=$in_forum";}
    $output .= qq~<br><SCRIPT>valigntop()</SCRIPT>
	<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
	<tr><td>
	<table cellpadding=6 cellspacing=1 width=100%>
	<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>谢谢！您参与投票成功！</b></font></td></tr>
	<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
	如果浏览器没有自动返回，请点击下面的链接！
	<ul>
	<li><a href="topic.cgi?forum=$in_forum&topic=$threadname">返回此投票帖</a>
	<li><a href="forums.cgi?forum=$in_forum">返回论坛</a>
	<li><a href="leobbs.cgi">返回论坛首页</a>
	</ul>
	</td></tr>
	</table></td></tr></table>
	<SCRIPT>valignend()</SCRIPT>
	<meta http-equiv="refresh" content="3; url=$relocurl">
~;
}
