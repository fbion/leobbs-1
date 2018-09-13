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

use LBCGI;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
$LBCGI::POST_MAX = 500000;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "editpoll.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$addme = $query->param('addme');
for ('forum', 'topic', 'membername', 'password', 'action', 'inshowsignature', 'notify', 'inshowemoticons', 'newtopictitle',
    'inpost', 'posticon', 'hidepoll', 'inhiddentopic', 'postweiwang', 'canpoll', 'uselbcode', 'inshowchgfont', 'inwater') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}

$in_forum = $forum;
$in_topic = $topic;
&error("打开文件&老大，别乱黑我的程序呀！") if (($in_topic) && ($in_topic !~ /^[0-9 ]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if ($in_forum !~ /^[0-9 ]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}
&error("普通错误&请以正确的方式访问本程序！") if (($postweiwang > $maxweiwang) && ($inhiddentopic eq "yes"));
$inmembername = $membername;
$inpassword = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$innotify = $notify;
$indeletepost = $deletepost;
$currenttime = time;
$inposticon = $posticon;
$inpost =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost =~ s/\[USECHGFONTE\]/\[USECHGFONT\&\#069\;\]/sg;
$inpost =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;

$inpost .= ($uselbcode eq "yes") ? "" : "[DISABLELBCODE]" if ($action eq "processedit");
$inpost .= ($inshowchgfont eq "yes") ? "[USECHGFONTE]" : "" if (($action eq "processedit") && ($canchgfont ne "no"));

$inselectstyle = $query->cookie("selectstyle");
$inselectstyle = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~ m/\//) || ($inselectstyle =~ m/\\/) || ($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}
if (!$inmembername) {$inmembername = $query->cookie("amembernamecookie");}
if (!$inpassword) {$inpassword = $query->cookie("apasswordcookie");}
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "客人") {
    $inmembername = "客人";
}
else {
    #    &getmember("$inmembername");
    &getmember("$inmembername", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if ($inpassword ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
}
require "postjs.cgi";

$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100) && ($maxpoststr ne ""));

print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

&moderator("$in_forum");
&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz !~ /,$membercode,/);
if ($allowusers ne '') {
    &error('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0) {
        require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
        $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
        &error("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
        &error("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

if ($useemote eq "yes") {
    open(FILE, "${lbdir}data/emote.cgi");
    $emote = <FILE>;
    close(FILE);
}
else {undef $emote;}

if ($inshowemoticons ne "yes") {$inshowemoticons eq "no";}
if ($innotify ne "yes") {$innotify eq "no";}
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

if ($action eq "edit") {&editform;}
elsif ($action eq "processedit") {&processedit;}
else {&error("普通错误&请以正确的方式访问本程序");}

&output($boardname, \$output);
exit;

sub editform {
    $filetoopen = "$lbdir" . "forum$in_forum/$in_topic.thd.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my $threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    chomp $threads;

    ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon, $water) = split(/\t/, $threads);
    $topictitle =~ s/^＊＃！＆＊//;
    &error("编辑帖子&没搞错吧，这根本不是投票贴子啊！") if ($posticon !~ /<BR>/i);
    $inmembmod = "no" if (($membercode eq "amo") && ($allowamoedit ne "yes"));
    if (($membercode ne "ad") && ($membercode ne "smo") && ($inmembmod ne "yes") && ((lc($inmembername) ne lc($postermembername)) || ($usereditpost eq "no"))) {&error("编辑投票帖子&您不是原作者、论坛版主以上级别 , 或者密码错誤，或者此区不允许编辑帖子！");}
    $testentry = $query->cookie("forumsallowed$in_forum");
    if (($allowedentry{$in_forum} eq "yes") || (($testentry eq $forumpass) && ($testentry ne "")) || ($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes")) {$allowed = "yes";}
    else {$allowed = "no";}
    if (($privateforum eq "yes") && ($allowed ne "yes")) {&error("编辑投票&对不起，您不允许在此论坛发表！");}

    if ($nowater eq "on") {
        $gsnum = 0 if ($gsnum <= 0);
        $nowaterpost = qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>灌水限制</b></font></td><td bgcolor=$miscbackone><input type="radio" name="inwater" value=no> 不许灌水　 <input name="inwater" type="radio" value=yes> 允许灌水　    [如果选择“不许灌水”，则回复不得少于 <B>$gsnum</B> 字节]</td></tr>~;
        $nowaterpost =~ s/value=$water/value=$water checked/i if ($water ne "");
    }

    if ($wwjf ne "no") {
        if ($post =~ /LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
            $weiwangchecked = " checked";
            $weiwangchoice = $1;
        }
        else {
            undef $weiwangchecked;
            undef $weiwangchoice;
        }
        for (my $i = 0; $i < $maxweiwang; $i++) {
            $weiwangoption .= qq~<option value=$i>$i</option>~;
        }
        $weiwangoptionbutton = qq~<input type=checkbox name="inhiddentopic" value="yes" $weiwangchecked>加密此帖，只对部分用户可见，用户威望至少需要  <select name=postweiwang>$weiwangoption</select><br>~;
        $weiwangoptionbutton =~ s/option value=$weiwangchoice/option value=$weiwangchoice selected/i if ($weiwangchoice ne "");
    }
    else {
        undef $weiwangoptionbutton;
    }

    $showsignature = "yes$maxpollitem" if ($showsignature eq "yes");
    if ($showsignature =~ /^yes[0-9]+$/) {
        $duoxuan = 'checked';
        $canpoll = $showsignature;
        $canpoll =~ s/^yes//;
        $Selected[$canpoll] = " selected";
    }
    else {
        $duoxuan = '';
        $canpoll = 1;
    }
    if ($post =~ m/\[hidepoll\]/isg) {$PollHiddencheck = 'checked';}
    else {$PollHiddencheck = '';}

    if (($post =~ /\[POSTISDELETE=(.+?)\]/) && ($membercode ne "ad") && ($membercode ne "smo") && ($inmembmod ne "yes")) {
        &error("编辑帖子&不允许编辑已经被单独屏蔽的帖子！");
    }

    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;
    $post =~ s/\[hidepoll\]//isg;
    $post =~ s/\[这个投票最后由(.+?)编辑\]\n//isg;
    $post =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $uselbcodecheck = ($post =~ /\[DISABLELBCODE\]/) ? "" : " checked";
    $usecanchgfont = ($post =~ /\[USECHGFONTE\]/) ? " checked" : "";
    $post =~ s/\[DISABLELBCODE\]//isg;
    $post =~ s/\[USECHGFONTE\]//isg;
    $post =~ s/\[POSTISDELETE=(.+?)\]//isg;
    $post =~ s/\[ADMINOPE=(.+?)\]//isg;

    $posticon =~ s/\<p\>/\n\n/ig;
    $posticon =~ s/\<br\>/\n/ig;
    if (-e "${lbdir}forum$in_forum/$in_topic.poll.cgi") {$dis1 = "disabled";}
    if ($showsignature eq 'yes') {$dis2 = "checked";}

    &mischeader("编辑贴子");
    $helpurl = &helpfiles("阅读标记");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></a>~;
    if ($emailfunctions eq "on") {
        if ($innotify eq "yes") {$requestnotify = " checked";}
        else {$requestnotify = "";}
        $requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>有回复时使用邮件通知您？<br>~;
    }
    if ($emoticons eq "on") {
        $emoticonslink = qq~<a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">允许<B>使用</B>表情字符转换</a>~;
        $emoticonsbutton = qq~<input type=checkbox name="inshowemoticons" value="yes" checked>您是否希望<b>使用</b>表情字符转换在您的文章中？<br>~;
    }

    if ($canchgfont ne "no") {
        $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes"$usecanchgfont>使用字体转换？<br>~;
    }
    else {
        undef $fontpost;
    }

    if ($htmlstate eq "on") {$htmlstates = "可用";}
    else {$htmlstates = "不可用";}
    if ($idmbcodestate eq "on") {
        $idmbcodestates = "可用";
        $canlbcode = qq~<input type=checkbox name="uselbcode" value="yes"$uselbcodecheck>使用 LeoBBS 标签？<br>~;
    }
    else {
        $idmbcodestates = "不可用";
        $canlbcode = "";
    }
    if ($arrawpostflash eq "on") {$postflashstates = "允许";}
    else {$postflashstates = "禁止";}
    if ($useemote eq "no") {$emotestates = "不可用";}
    else {$emotestates = "可用";}

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
        &whosonline("$inmembername\t$forumname\tnone\t编辑<a href=\"topic.cgi?forum=$in_forum&topic=$in_topic\"><b>$topictitle</b></a>\t") if ($privateforum ne "yes");
        &whosonline("$inmembername\t$forumname(密)\tnone\t编辑保密投票\t") if ($privateforum eq "yes");
    }

    $output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;
    $maxpoststr = "(帖子中最多包含 <B>$maxpoststr</B> 个字符)" if ($maxpoststr ne "");
    foreach (2 .. $maxpollitem) {$canpolllist .= qq~<option value="$_"$Selected[$_]>$_</option>~;}

    $output .= qq~<script>
var autoSave = false;
function storeCaret(textEl) {if (textEl.createTextRange) textEl.caretPos = document.selection.createRange().duplicate();if (autoSave)savePost();}
function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
</script>
<form action="$thisprog" method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name="action" value="processedit">
<input type=hidden name="forum" value="$in_forum">
<input type=hidden name="topic" value="$in_topic"><SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=4 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor>&nbsp;</td></tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>投票标题</b></font></td>
<td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="newtopictitle" value="$topictitle">　不得超过 40 个汉字</td></tr>$nowaterpost
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>投票项目</b><br><li>每行一个投票项目，最多 <B>$maxpollitem</b> 项<BR><li>超过自动作废，空行自动过滤<BR><li>如果投票需要多选，请在选择中打钩</font></td><td bgcolor=$miscbacktwo valign=top>
<TEXTAREA cols=80 name=posticon rows=6 wrap=soft $dis1>$posticon</TEXTAREA><BR>
<input type=checkbox name="inshowsignature" value="yes" $duoxuan>最多可投<select name="canpoll">$canpolllist</select>项　 <input type=checkbox name="hidepoll" value="yes" $PollHiddencheck>是否必须投票后才可查看结果？<br></td></tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>内容</b>　$maxpoststr<p>
在此论坛中：<li>HTML 标签　: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE　标签</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a>: <b>$idmbcodestates</b><li>贴图标签　 : <b>$postpicstates</b><li>Flash 标签 : <b>$postflashstates</b><li>音乐标签　 : <b>$postsoundstates</b><li>文字大小　 : <b>$postfontsizestates</b><li>帖数标签 　: <b>$postjfstates</b><li>积分标签 　: <b>$jfmarkstates</b><li>保密标签 　: <b>$hidejfstates</b><li>$emoticonslink</font></td>
<td bgcolor=$miscbackone>$insidejs<TEXTAREA cols=80 name=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$post</TEXTAREA><br>
&nbsp; 模式:<input type="radio" name="mode" value="help" onClick="thelp(1)">帮助　<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">完全　<input type="radio" name="mode" value="basic"  onClick="thelp(0)">基本　　>> <a href=javascript:HighlightAll('FORM.inpost')>复制到剪贴板</a> | <a href=javascript:checklength(document.FORM);>查看长度</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">转换剪贴板超文本</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<</td></tr>
<tr><td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>点击表情图即可在贴子中加入相应的表情</B></font><br>&nbsp;~;
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
    $output .= qq~</td></tr><tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>选项</b><p>$helpurl</font></td><td bgcolor=$miscbacktwo>
<font color=$fontcolormisc>$canlbcode$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton</font></td></tr><tr><td bgcolor=$miscbackone colspan=2 align=center>
<input type=Submit value="发 表" name=Submit onClick="return clckcntr();">　　<input type=button value='预 览' name=Button onclick=gopreview()>　　<input type="reset" name="Clear" value="清 除"></td></form></tr></table></tr></td></table><SCRIPT>valignend()</SCRIPT>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$in_forum"></form>
<script>
function gopreview(){
document.forms[1].body.value=document.forms[0].inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.forms[1].submit()
}
</script>
    ~;
}

sub processedit {
    $filetoopen = "$lbdir" . "forum$in_forum/$in_topic.thd.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        sysread(FILE, my $allthreads, (stat(FILE))[7]);
        close(FILE);
        $allthreads =~ s/\r//isg;
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        @allthreads = split(/\n/, $allthreads);
    }
    else {
        unlink("$lbdir" . "forum$in_forum/$in_topic.pl");
        &error("编辑&这个主题不存在！");
    }

    ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature, $postdate, $post, $posticon) = split(/\t/, $allthreads[0]);

    $addpost = "";
    while ($post =~ /\[ADMINOPE=(.+?)\]/s) {
        $addpost .= "[ADMINOPE=$1]";
        $post =~ s/\[ADMINOPE=(.+?)\]//s;
    }

    if (($post =~ /\[POSTISDELETE=(.+?)\]/) && ($membercode ne "ad") && ($membercode ne "smo") && ($inmembmod ne "yes")) {
        &error("编辑投票帖&不允许编辑已经被单独屏蔽的帖子！");
    }

    $post =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;
    ($edittimes, $temp) = split(/ 次/, $2);
    ($temp, $edittimes) = split(/第 /, $edittimes);
    $edittimes = 0 unless ($edittimes);

    $inmembmod = "no" if (($membercode eq "amo") && ($allowamoedit ne "yes"));
    if (($membercode ne "ad") && ($membercode ne "smo") && ($inmembmod ne "yes") && (lc($inmembername) ne lc($postermembername))) {&error("编辑帖子&您不是原作者、论坛管理员 , 或者用户名、密码错誤！");}
    $testentry = $query->cookie("forumsallowed$in_forum");
    if (($allowedentry{$in_forum} eq "yes") || (($testentry eq $forumpass) && ($testentry ne "")) || ($membercode eq "ad") || ($membercode eq 'smo') || ($inmembmod eq "yes")) {$allowed = "yes";}
    else {$allowed = "no";}
    if (($privateforum eq "yes") && ($allowed ne "yes")) {&error("发表投票&对不起，您不允许在此论坛发表投票！");}

    &error("编辑帖子&没搞错吧，这根本不是投票贴子啊！") if ($posticon !~ /<BR>/i);
    &error("编辑帖子&对不起，本论坛不允许发表超过 <B>$maxpoststr</B> 个字符的文章！") if ((length($inpost) > $maxpoststr) && ($maxpoststr ne "") && ($membercode ne "ad") && ($membercode ne 'smo') && ($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("编辑帖子&对不起，本论坛不允许发表少于 <B>$minpoststr</B> 个字符的文章！") if ((length($inpost) < $minpoststr) && ($minpoststr ne "") && ($membercode ne "ad") && ($membercode ne 'smo') && ($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    if (($membercode eq "banned") || ($membercode eq "masked")) {&error("编辑投票&您被禁止发言或者发言已经被屏蔽，请联系管理员以便解决！");}

    if (($membercode eq "ad") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) {$cleartoedit = "yes";}
    if ((lc($inmembername) eq lc($postermembername)) && ($inpassword eq $password) && ($usereditpost ne "no")) {$cleartoedit = "yes";}
    unless ($cleartoedit eq "yes") {$cleartoedit eq "no";}

    if ($cleartoedit eq "yes") {
        $editpostdate = $currenttime + ($timezone + $timedifferencevalue) * 3600;
        $editpostdate = &dateformat("$editpostdate");
        $inpost =~ s/\t//g;
        $inpost =~ s/\r//g;
        $inpost =~ s/  / /g;
        $inpost =~ s/\n\n/\<p\>/g;
        $inpost =~ s/\n/\<br\>/g;
        $inpost =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;

        $filetoopen = "$lbdir" . "forum$in_forum/$in_topic.poll.cgi";
        if (!(-e $filetoopen)) {
            $inposticon =~ s/<p>/<BR>/isg;
            $inposticon =~ s/<BR><BR>/<BR>/isg;
            $inposticon =~ s/(.*)<BR>$/$1/i;
            $inposticon =~ s/^<BR>(.*)/$1/i;
            $inposticon =~ s/<BR>(\s*)/<BR>/i;
            $inposticon =~ s/(\s*)<BR>/<BR>/i;
            $inposticontemp = $inposticon;
            $inposticontemp =~ s/<br>/\t/ig;
            my @temppoll = split(/\t/, $inposticontemp);
            my $temppoll = @temppoll;
            $canpoll = $temppoll if ($canpoll > $temppoll || $canpoll =~ m/[^0-9]/);
            $inshowsignature .= $canpoll if ($inshowsignature ne "no");
            if ($inposticon !~ m/<br>/i) {&error("编辑投票&投票选项太少！");}
            if ($temppoll > $maxpollitem) {&error("编辑投票&投票选项过多，不能超过 $maxpollitem 项！(您此次投票的选项有 $temppoll 项)");}
        }
        else {
            $inposticon = $posticon;
            $inposticontemp = $inposticon;
            $inposticontemp =~ s/<br>/\t/ig;
            my @temppoll = split(/\t/, $inposticontemp);
            my $temppoll = @temppoll;
            $canpoll = $temppoll if ($canpoll > $temppoll || $canpoll =~ m/[^0-9]/);
            $inshowsignature .= $canpoll if ($inshowsignature ne "no");
        }
        if ($emote && $inpost =~ m/\/\/\//) {
            study($inpost);
            my @pairs1 = split(/\&/, $emote);
            foreach (@pairs1) {
                my ($toemote, $beemote) = split(/=/, $_);
                chomp $beemote;
                $beemote =~ s/对象/〖$inmembername〗/isg;
                $inpost =~ s/$toemote/$beemote/isg;
                last unless ($inpost =~ m/\/\/\//);
            }
        }

        my $temp = &dofilter("$newtopictitle\t$inpost");
        ($newtopictitle, $inpost) = split(/\t/, $temp);
        $newtopictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
        $newtopictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
        $newtopictitle =~ s/(o|O)R/$1&#82;/sg;
        $newtopictitle =~ s/(o|O)r/$1&#114;/sg;
        #	$newtopictitle =~ s/\\/&#92;/isg;

        if ($newtopictitle eq "") {&error("编辑投票&对不起，贴子主题不能为空！");}
        if (length($newtopictitle) > 110) {&error("编辑投票&对不起，主题标题过长！");}
        $newtopictitletemp = $newtopictitle;
        $newtopictitle = "＊＃！＆＊$newtopictitle";

        $edittimes++;
        $noaddedittime = 60 if ($noaddedittime < 0);
        $inpost = qq~[这个投票最后由$inmembername在 $editpostdate 第 $edittimes 次编辑]<br><br>$inpost~ if (($currenttime - $postdate) > $noaddedittime || $postermembername ne $inmembername);

        $inpost =~ s/\[hidepoll\]//isg;
        $inpost .= "[hidepoll]" if ($hidepoll eq "yes");

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
        $postcountcheck = 0;
        $inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

        $filetoopen = "$lbdir" . "forum$in_forum/$in_topic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            foreach $postline (@allthreads) {
                chomp $postline;
                if ($postcountcheck eq 0) {
                    print FILE "$postermembername\t$newtopictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$postdate\t$addpost$inpost\t$inposticon\t$inwater\t\n";
                }
                else {
                    (my $postermembertemp, my $no, my @endall) = split(/\t/, $postline);
                    print FILE "$postermembertemp\t$newtopictitle\t";
                    foreach (@endall) {
                        chomp $_;
                        print FILE "$_\t";
                    }
                    print FILE "\n";
                }
                $postcountcheck++;
            }
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        $threadnum = @allthreads;
        $newtopictitle =~ s/^＊＃！＆＊//;

        $filetoopen = "${lbdir}forum$in_forum/$in_topic.pl";
        open(FILE, "$filetoopen");
        my $topicall = <FILE>;
        close(FILE);
        chomp $topicall;
        (my $topicidtemp, $topictitletemp, my @endall) = split(/\t/, $topicall);
        $oldinposttemp = pop(@endall);
        $oldinposttemp = $inposttemp if ($threadnum eq 1);
        if (($topictitletemp ne $newtopictitletemp) || ($threadnum eq 1)) {
            $oldinposttemp = $inposttemp if ($threadnum eq 1);
            $topicall =~ s/^$in_topic\t(.*?)\t(.*)\t(.*?)\t(.*?)\t/$in_topic\t＊＃！＆＊$newtopictitletemp\t$2\t$oldinposttemp\t$4\t/isg;
            if (open(FILE, ">$filetoopen")) {
                print FILE "$topicall";
                close(FILE);
            }

            $filetoopen = "$lbdir" . "boarddata/listall$in_forum.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE, "$filetoopen");
            flock(FILE, 2) if ($OS_USED eq "Unix");
            sysread(FILE, my $allthreads, (stat(FILE))[7]);
            close(FILE);
            $allthreads =~ s/\r//isg;
            $allthreads =~ s/(.*)(^|\n)$in_topic\t(.*?)\t(.*?)\t(.*?)\t\n(.*)/$1$2$in_topic\t$newtopictitletemp\t$4\t$5\t\n$6/isg;

            if (open(FILE, ">$filetoopen")) {
                print FILE "$allthreads";
                close(FILE);
            }
            &winunlock($filetoopen) if ($OS_USED eq "Nt");
        }
        if ($topictitletemp ne $newtopictitletemp) {

            my $newthreadnumber;
            $filetoopen = "$lbdir" . "boarddata/lastnum$in_forum.cgi";
            if (open(FILE, "$filetoopen")) {
                $newthreadnumber = <FILE>;
                close(FILE);
                chomp $newthreadnumber;
            }
            if ($newthreadnumber = $in_topic) {
                $filetoopen = "${lbdir}boarddata/foruminfo$in_forum.cgi";
                my $filetoopens = &lockfilename($filetoopen);
                if (!(-e "$filetoopens.lck")) {
                    &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
                    open(FILE, "+<$filetoopen");
                    my ($lastforumpostdate, $tpost, $treply, $todayforumpost, $lastposter) = split(/\t/, <FILE>);
                    my ($lastposttime, $threadnumber, $topictitle1) = split(/\%\%\%/, $lastforumpostdate);
                    seek(FILE, 0, 0);
                    $lastforumpostdate = "$lastposttime\%\%\%$threadnumber\%\%\%$newtopictitletemp";
                    print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
                    close(FILE);
                    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
                }
            }

            $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
            my $filetoopens = &lockfilename($filetomakeopen);
            if (!(-e "$filetoopens.lck")) {
                &winlock($filetomakeopen) if ($OS_USED eq "Nt");
                open(FILE, "$filetomakeopen");
                flock(FILE, 1) if ($OS_USED eq "Unix");
                my @recentposts = <FILE>;
                close(FILE);
                if (open(FILE, ">$filetomakeopen")) {
                    flock(FILE, 2) if ($OS_USED eq "Unix");
                    foreach (@recentposts) {
                        chomp $_;
                        ($tempno1, $tempno2, $no, @endall) = split(/\t/, $_);
                        next if (($tempno1 !~ /^[0-9]+$/) || ($tempno2 !~ /^[0-9]+$/));

                        if (($tempno1 eq $in_forum) && ($tempno2 eq $in_topic)) {
                            print FILE "$in_forum\t$in_topic\t$newtopictitletemp\t";
                            foreach (@endall) {
                                chomp $_;
                                print FILE "$_\t";
                            }
                            print FILE "\n"
                        }
                        else {print FILE "$_\n"}
                    }
                    close(FILE);
                }
                &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
            }
            else {
                unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
            }
        }
    }

    &mischeader("编辑投票");

    for (my $iii = 0; $iii <= 4; $iii++) {
        my $jjj = $iii * $maxthreads;
        unlink("${lbdir}cache/plcache$in_forum\_$jjj.pl");
    }

    if ($refreshurl == 1) {$relocurl = "topic.cgi?forum=$in_forum&topic=$in_topic";}
    else {$relocurl = "forums.cgi?forum=$in_forum";}
    $output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>编辑成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>具体情况：
<ul><li><a href="topic.cgi?forum=$in_forum&topic=$in_topic">返回投票主题</a>
<li><a href="forums.cgi?forum=$in_forum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a>
</ul></tr></td></table></td></tr></table>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
}