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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
use VISITFORUM qw(getlastvisit setlastvisit);
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/mpic.cgi";
require "bbs.lib.pl";
$|++;
$thisprog = "forums.cgi";
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
&ipbanned; #封杀一些 ip

$jumpto = $query->param('jumpto');
if ($jumpto) {
    print redirect(-location => "$jumpto");
    exit;
}
$in_forum = $query->param('forum');
&error("打开论坛&老大，别乱黑我的程序呀！") if ($in_forum !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") {require "${lbdir}data/style${inforum}.cgi";}

$action = $query->param('action');
$action = &stripMETA("$action");
$inshow = $query->param('show');
$inshow = 0 if (($inshow !~ /^[0-9]+$/) || ($inshow eq ""));
$deshow = $query->param('dshow');
$deshow = "" if ($deshow !~ /^[0-9]+$/);
$startarray = $inshow;
$inthreadages = $query->param('threadages');
$inthreadages = $defaulttopicshow if ($inthreadages eq "" && $defaulttopicshow ne "");

$in_select_style = $query->cookie("selectstyle");
$in_select_style = $skin_selected if ($in_select_style eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($in_select_style =~ m/\//) || ($in_select_style =~ m/\\/) || ($in_select_style =~ m/\.\./));
if (($in_select_style ne "") && (-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
$currenttime = time;
&error("打开论坛&对不起，这个论坛不存在！如果确定分论坛号码没错，那么请进入管理区修复论坛一次！") if (!(-e "${lbdir}boarddata/listno$in_forum.cgi"));

$inshow = int($inshow / $maxthreads + 0.5) * $maxthreads;
$inshow = ($deshow - 1) * $maxthreads if ($deshow ne "");

$in_member_name = $query->param('membername');
$in_password = $query->param('password');
if ($in_password ne "") {
    eval {$in_password = md5_hex($in_password);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$in_password = md5_hex($in_password);');}
    unless ($@) {$in_password = "lEO$in_password";}
}

$forum_password = $query->param('forumpassword');
if (!$in_member_name) {$in_member_name = $query->cookie("amembernamecookie");}
if (!$in_password) {$in_password = $query->cookie("apasswordcookie");}
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;
if ((!$in_member_name) or ($in_member_name eq "客人")) {$in_member_name = "客人";}
else {
    #    &getmember("$in_member_name");
    &getmember("$in_member_name", "no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
    if ($in_password ne $password) {
        $namecookie = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
        $passcookie = cookie(-name => "apasswordcookie", -value => "", -path => "$cookiepath/");
        print header(-cookie => [ $namecookie, $passcookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
    }
    &getlastvisit;
    $forumlastvisit = $lastvisitinfo{$in_forum};
    &setlastvisit("$in_forum,$currenttime");
}
require "${lbdir}imagead.cgi" if (($forumimagead eq "1") || ($useimageadforum eq "1") || ($forumimagead1 eq "1") || ($useimageadforum1 eq "1"));

$defaultsmilewidth = "width=$defaultsmilewidth" if ($defaultsmilewidth ne "");
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
$addtimes = $timedifferencevalue * 3600 + $timezone * 3600;
$screenmode = $query->cookie("screenmode");
$screenmode = 8 if ($screenmode eq "");
my $onlineview1 = $query->cookie("onlineview");
$onlineview = $onlineview1 if ($onlineview1 ne "");
$onlineview = 0 if ($onlineview eq "");
$onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
$onlineviewcookie = cookie(-name => "onlineview", -value => "$onlineview", -path => "$cookiepath/", -expires => "+30d");
if ($onlineview == 1) {$onlinetitle = "[<a href=$thisprog?action=onlineview&forum=$in_forum><font color=$titlefontcolor>关闭详细列表</font></a>]";}
else {$onlinetitle = "[<a href=$thisprog?action=onlineview&forum=$in_forum><font color=$titlefontcolor>显示详细列表</font></a>]";}

&moderator("$in_forum");

require "doaccessrequire.pl" if ($action eq "accessrequired");
require "resetposts.pl" if ($action eq "resetposts");

if ($catbackpic ne "") {$catbackpic = "background=$imagesurl/images/$skin/$catbackpic";}
$insidead = "" if (($forumimagead ne "1") && ($useimageadforum eq "0"));
$insidead1 = "" if (($forumimagead1 ne "1") && ($useimageadforum1 eq "0"));

$in_forumcookies = $query->cookie("forumscookies");
if (",$in_forumcookies," !~ /,$in_forum,/) {
    $in_forumcookies .= ",$in_forum";}
my $forumscookie = cookie(-name => "forumscookies", -value => $in_forumcookies, -path => "$cookiepath/", -expires => "+30d");
print header(-cookie => [ $allowforumcookie, $onlineviewcookie, $tempvisitcookie, $permvisitcookie, $forumscookie ], -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

&error("进入论坛&一般会员不允许进入此论坛！") if (($startnewthreads eq "cert") && (($member_code ne "ad" && $member_code ne "smo" && $member_code ne "cmo" && $member_code ne "mo" && $member_code ne "amo" && $member_code !~ /^rz/) || ($in_member_name eq "客人")) && ($userincert eq "no"));
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

if ($adlinks ne "") {
    require "doadlinks.pl";
}

$rsshtml = qq~  <a href="rss.cgi/leo.xml?forum=$in_forum" target="_blank"><img src="$imagesurl/images/xml.gif" border="0" height=15 align="absmiddle" alt="RSS 订阅本论坛"></a>&nbsp;<a href="wap.cgi" target="_blank"><img src="$imagesurl/images/wap.gif" height=15 border="0" align="absmiddle" alt="通过手机访问论坛，地址：$boardurl/wap.cgi"></a>~;
if ($enterminmony > 0 || $enterminjf > 0 || $enterminweiwang > 0 || $allow_users ne '') {
    $rsshtml = "";
}
if ($reg_access eq "on") {
    $rsshtml = "";
}
if (($startnewthreads eq "cert") && ($userincert eq "no")) {
    $rsshtml = "";
}
if ($rssinfo eq "no") {
    $rsshtml = "";
}

&title;
if (-e "${lbdir}cache/forumshead$in_forum.pl") {
    eval {require "${lbdir}cache/forumshead$in_forum.pl";};
    if ($@) {
        unlink("${lbdir}cache/forumshead$in_forum.pl");
        require "doforumhead.pl";
    }
}
else {require "doforumhead.pl";}
$output .= qq~$adlinks<br>$titleoutput<br>~;

$output .= qq~<BGSOUND SRC=$imagesurl/midi/$midiaddr LOOP=-1>~ if ((-e "${imagesdir}midi/$midiaddr") && ($midiaddr ne ""));

if ($canusetreeview ne "no") {
    $output .= qq~<script>
function loadThreadFollows(f_id,t_id){ document.frames["hiddenframe"].location.replace("reply_tree.cgi?forum="+f_id+"&topic="+t_id);}
function loadThreadFollow(f_id,t_id,id_of_topic){
var targetImg =eval("document.images.followImg" + id_of_topic);
var targetDiv =eval("follow" + id_of_topic);
if (targetImg.nofollow <= 0){return false;}
if (typeof(targetImg) == "object"){
if (targetDiv.style.display!='block'){
targetDiv.style.display="block";targetImg.src="$imagesurl/images/cat1.gif";
if (targetImg.loaded=="no"){ document.frames["hiddenframe"].location.replace("reply_tree.cgi?forum="+f_id+"&topic="+t_id); }
}else{ targetDiv.style.display="none";targetImg.src="$imagesurl/images/cat.gif"; }
}}
</script>
<iframe width=0 height=0 align=center src="" id=hiddenframe></iframe>
~;
}

$output .= qq~<style>
.ha {color: $fonthighlight; font: bold;}
.hb {color: $menufontcolor; font: bold;}
.dp {padding: 4px 0px;}
.jc {position:relative;}
.ts {BORDER-RIGHT:black 1px solid;PADDING-RIGHT:2px;BORDER-TOP:black 1px solid;PADDING-LEFT:2px;PADDING-BOTTOM:2px;MARGIN-LEFT:18px;BORDER-LEFT:black 1px solid;WIDTH:170px;COLOR:black;PADDING-TOP:2px;BORDER-BOTTOM:black 1px solid;BACKGROUND-COLOR:lightyellow;cursor:hand;}
TABLE {BORDER-TOP: 0px; BORDER-LEFT: 0px; BORDER-BOTTOM: 1px; }
TD {BORDER-RIGHT: 0px; BORDER-TOP: 0px; color: $fontcolormisc; }
</style>
<script>
~;

if ($usefake eq "yes") {
    $output .= qq~
function O1(id) {window.open("topic-$in_forum-"+id+"-0-0-.htm");}
function O2(id) {window.open("view-$in_forum-"+id+".htm");}
function O5(id1,id2) {window.open("topic-"+id1+"-"+id2+"-.htm");}
function O6(id1,id2) {window.open("view-"+id1+"-"+id2+".htm");}
function O3(id1,id2,id3) {window.open("topic-" + id1 + "-" + id2 + "-" + id3 + "-0-last.htm#bottom", "_self");}
function O4(id) {window.open("forums-"+id+"-0.htm");}
function O9(id) {if(id!="")window.open("profile-"+id+".htm");}
~;
}
else {
    $output .= qq~
function O1(id) {window.open("topic.cgi?forum=$in_forum&topic="+id);}
function O2(id) {window.open("view.cgi?forum=$in_forum&topic="+id);}
function O5(id1,id2) {window.open("topic.cgi?forum="+id1+"&topic="+id2);}
function O6(id1,id2) {window.open("view.cgi?forum="+id1+"&topic="+id2);}
function O3(id1,id2,id3) {window.open("topic.cgi?forum=" + id1 + "&topic=" + id2 + "&start=" + id3 + "&replynum=last#bottom", "_self");}
function O4(id) {window.open("forums.cgi?forum="+id);}
function O9(id) {if(id!="")window.open("profile.cgi?action=show&member="+id);}
~;
}

$output .= qq~
var exp = new Date();exp.setTime(exp.getTime() + 30*86400*1000);
if (screen.width <= 800 ){SetCookie('screenmode','5',exp,"$cookiepath/");}
if ((screen.width >800 )&&(screen.width<=1024)){SetCookie('screenmode','8',exp,"$cookiepath/");}
if (screen.width >1024 ){SetCookie('screenmode','10',exp,"$cookiepath/");}
function SetCookie (name, value) { var argv = SetCookie.arguments;var argc = SetCookie.arguments.length;var expires = (argc > 2) ? argv[2] : null;var path = (argc > 3) ? argv[3] : null;var domain = (argc > 4) ? argv[4] : null;var secure = (argc > 5) ? argv[5] : false; document.cookie = name + "=" + escape (value) + ((expires == null) ? "" : ("; expires=" + expires.toGMTString())) + ((path == null) ? "" : ("; path=" + path)) + ((domain == null) ? "" : ("; domain=" + domain)) + ((secure == true) ? "; secure" : ""); }
</script>
$insidead$insidead1
~;

if ($privateforum eq "yes") {
    $rsshtml = "";
    if ($in_member_name eq "客人") {
        print "<script language='javascript'>document.location = 'loginout.cgi?forum=$in_forum'</script>";
        exit;
    }
    $test_entry = cookie("forumsallowed$in_forum");
    if ((($test_entry eq $forum_pass) && ($test_entry ne "")) || (($userregistered ne "no") && ($allowed_entry{$in_forum} eq "yes")) || ($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {
        if ($in_password ne $password) {&error("进入论坛&密码错误，你不允许进入该论坛！");}
    }
    else {require "accessform.pl";}
}

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
if (!(-e "$filetoopens.lck")) {
    if ($privateforum ne "yes") {
        &whosonline("$in_member_name\t$forumname\t$forumname\t查看论坛上的主题");
    }
    else {
        &whosonline("$in_member_name\t$forumname(密)\t$forumname\t查看保密论坛上的主题");
    }
    undef $memberoutput if ($onlineview != 1);
}
else {
    unlink("$filetoopens.lck") if ((-M "$filetoopens.lck") * 86400 > 30);
    $memberoutput = "";
    $membertongji = " <B>由于服务器繁忙，所以本分论坛的在线数据暂时不提供显示。</B>";
    $onlinetitle = "";
}

$nowtime = &shortdate($currenttime + $timeadd);
if ($startnewthreads ne "onlysub") {
    my ($todayforumpost, $todayforumposttime) = split(/\|/, $todayforumpost);
    $todayforumpost = 0 if (($nowtime ne $todayforumposttime) || ($todayforumpost eq ""));
    $membertongji .= " 今日新贴有 <font color=$fonthighlight><b>$todayforumpost</b></font> 篇";
    $modoutput = "<B>本论坛版主暂时空缺&nbsp;</B>" if (!$modoutput);
}

if ($announcements eq 'yes') {
    if (-e "${lbdir}data/announce$in_forum.pl") {
        require "${lbdir}data/announce$in_forum.pl";
        $announcedisp =~ s/\$forumfontcolor/$forumfontcolor/isg;
        $announcedisp =~ s/\$fonthighlight/$fonthighlight/isg;
    }
    else {
        $announcedisp = qq~&nbsp;<a href=announcements.cgi?forum=$in_forum target=_blank title="当前没有公告"><b>当前没有公告</b></a>~;
        $announcetemp1 = qq~<img src=$imagesurl/images/announce.gif border=0 alt=分论坛暂时无公告！ width=18>~;
    }
}

$output .= qq~
<SCRIPT FOR=forum EVENT=onclick>a();</SCRIPT>
<table cellpadding=1 cellspacing=0 width=$tablewidth align=center>
<tr><td width=2></td><td align=center width=34>$announcetemp1</td><td width=*>$announcedisp</td><td align=right width=500><p>
<SCRIPT>
function threadmenu(){var URL = document.jump1.threadages.options[document.jump1.threadages.selectedIndex].value;top.location.href = "forums.cgi?forum=$in_forum&threadages=" + URL; target = '_self';}
</SCRIPT>
<form action=forums.cgi method=post name=jump1><A href=javascript:JM_setTarget() value='' id=globalTarget><img src=$imagesurl/images/$skin/$wlogo border=0 alt=查看帖子使用的模式？ align=absmiddle></a>　
~;

eval {require "data/fname.pl";};
my @inforumcookies = split(/\,/, $in_forumcookies);
foreach (@inforumcookies) {
    chomp;
    next if ($_ eq '');
    next if ($_ eq $in_forum);
    my $a = 'fname' . $_;
    next if (${$a} eq '');
    $vist_f .= "<option value=$_>□-${$a}";
}

if ($usefake eq "yes") {
    $output .= qq~ <select onchange="if(this.options[this.selectedIndex].value != '')
window.location=('forums-'+this.options[this.selectedIndex].value+'-0.htm')"><option value=1 style=background-color:\$titlecolor>最近访问的版块...$vist_f</select>
~;
}
else {
    $output .= qq~ <select onchange="if(this.options[this.selectedIndex].value != '')
window.location=('forums.cgi?forum='+this.options[this.selectedIndex].value)"><option value=1 style=background-color:\$titlecolor>最近访问的版块...$vist_f</select>
~;
}
$output .= qq~
<select name="threadages" onchange="threadmenu()"><option value="all">查看所有的主题</option><option value="1">查看一天内的主题</option><option value="2">查看两天内的主题</option><option value="7">查看一星期内的主题</option><option value="15">查看半个月内的主题</option><option value="30">查看一个月内的主题</option><option value="61">查看两个月内的主题</option><option value="182">查看半年内的主题</option><option value="365">查看一年内的主题</option>
</select></form></p></td><td align=center width=4></td></tr></table>
<SCRIPT>
function a(){el=event.srcElement;if (el.tagName=='A' && el.target!="_blank") el.target=(globalTarget.value);}
function setVMcookie(vtype){var exp = new Date();exp.setTime(exp.getTime() + (30*86400*1000));SetCookie('viewMode',vtype,exp,"$cookiepath/");}
function JM_setTarget(){globalTarget.value=(globalTarget.value=='_blank')?'':'_blank';globalTarget.children[0].src=(globalTarget.value=='')?'$imagesurl/images/$skin/$wlogo':'$imagesurl/images/$skin/$nwlogo';setVMcookie(globalTarget.value);}
function initViewMode(){viewMode=GetCookie('viewMode');globalTarget.value=(!viewMode)?'':'_blank';globalTarget.children[0].src=(!viewMode)?'$imagesurl/images/$skin/$wlogo':'$imagesurl/images/$skin/$nwlogo';}
initViewMode()
function Jumptopage(form){Jumppage.dshow.value = document.Action.dshow.value; Jumppage.submit();}
</script><center>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor><tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor width=92% $catbackpic><font color=$titlefontcolor>$membertongji　 $onlinetitle</td>
<td bgcolor=$titlecolor width=8% align=center $catbackpic><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 height=12></a></td>
</tr>
~;
$output =~ s/option value=\"$inthreadages\"/option value=\"$inthreadages\" selected/;

if ($onlineview == 1) {$output .= qq~<tr><td colspan=2 bgcolor=$forumcolorone><table cellpadding=1 cellspacing=0>$memberoutput</table></td></tr>~;}

$output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>~;

my ($forumrule, $editrule);
if (-e "${lbdir}boarddata/forumrule$in_forum.cgi") {
    open FILE, "${lbdir}boarddata/forumrule$in_forum.cgi";
    $forumrule = <FILE>;
    close FILE;
    require "code.cgi";
    &lbcode(\$forumrule);
    my @testforumrule = split(/\<br\>/i, $forumrule);
    $forumrulelines = @testforumrule;
    $forumrule = qq~<span style="height:64;overflow:auto;padding:2px;color:#000000;width:100%;text-align:left">$forumrule</span>~ if ($forumrulelines > 5);
}

if (($member_code eq "ad") || ($member_code eq 'smo') || (",$catemods," =~ /\Q\,$in_member_name\,\E/i) || ($inmembmod eq "yes")) {
    $editrule = "<a href='forumrule.cgi?forum=$in_forum'><img src='$imagesurl/images/a_edit.gif' border=0></a>";
    $forumrule = "目前没有论坛规则及重要信息，按<a href='forumrule.cgi?forum=$in_forum'>这里</a>新增。" unless $forumrule;
}

$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor><tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor width=92% $catbackpic><font color=$titlefontcolor><B> 论坛规则及重要信息</B></td>
<td bgcolor=$titlecolor width=8% align=center $catbackpic>$editrule</td></tr>
<tr><td colspan=2 bgcolor=$forumcolorone>$forumrule</td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>
~ if ($forumrule);

if (($inshow eq 0) && ($#childforum >= 0)) {require "getcforms.pl";}

if ($startnewthreads ne "onlysub") {
    #是纯子论坛，就不做显示

    if (($xzbopen ne "no") && ($startnewthreads ne "no") && ($privateforum ne "yes")) {require "forumxzb.pl";}

    if (($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {
        $admindisp = $query->cookie('admindisp');
        $admini = $admindisp eq '' ? '隐藏' : '显示';
        $admini = qq~<img src=$imagesurl/images/icon.gif width=14> <b><span style=cursor:hand onClick=javascript:showadmini()><font color=$fonthighlight id=admini0 title=设置是否显示版主快速操作栏>$admini版主操作</font></span><span id=admini style="display:$admindisp"></span></b>　~;
        $multimanage = qq~<td bgcolor=$titlecolor width=25 align=center $catbackpic><font color=$titlefontcolor><b>选</b></td>~;
        $multimanageitem = qq~<td align=center><input type="button" name="chkall" value="全选" onclick="CheckAll(this.form)"><input type="button" name="clear2" value="反选" onclick="FanAll(this.form)"><input type="reset" name="Reset" value="重置"><BR><input type=button name=lock value="锁" OnClick="LockThreads(this.form)"><input type="submit" name="delete" value="删" onClick="SetAction('delete')"><input type="submit" name="move" value="移" onClick="SetAction('movetopic')"><input type="button" name="jinghua" value="精" onClick="AddToJingHua(this.form)"></td>~;
        $output .= qq~<script language="JavaScript">
function CheckAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];e.checked = true;}}
function FanAll(form){for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.checked == true){ e.checked = false; }else { e.checked = true;}}}
function SetAction(A){Action.action.value=A;}
function AddToJingHua(form){JingHua.topic.value='';for (var i=0;i<form.elements.length;i++){var e = form.elements[i];if (e.checked == true && e.name == 'topic'){JingHua.topic.value+=e.value+" "; }}JingHua.submit();}
function LockThreads(form){Lock.topic.value = "";for (var i = 0; i < form.topic.length; i++){var e = form.topic[i];if (e.checked == true) Lock.topic.value += e.value + " ";}Lock.submit();}
function showadmini(){
var exp = new Date();
exp.setTime(exp.getTime() + (24 * 3600 * 1000));
for (var i = 0; i < admini.length; i++){
var e = admini[i];
if (e.style.display == ""){
if (i == 0) if (confirm('是否要一直隐藏版主操作？')) SetCookie('admindisp', 'none', exp, "$cookiepath/");
e.style.display = "none";admini0.innerText = "显示版主操作";
}else{
if (i == 0) if (confirm('是否要一直显示版主操作？')) SetCookie('admindisp', '', exp, "$cookiepath/");
e.style.display = "";admini0.innerText = "隐藏版主操作";
}}}
</script>
~;
    }

    my $freshtime = $query->cookie("freshtime");
    if ($freshtime ne "") {
        $autofreshtime = $freshtime * 60 - 1;
        $autofreshtime = 300 if ($autofreshtime < 59);
        $output .= qq~\n<meta http-equiv="refresh" content="$autofreshtime;">~;
    }
    elsif ($refreshforum eq "on") {
        $autofreshtime = 300 if ($autofreshtime < 59);
        $output .= qq~\n<meta http-equiv="refresh" content="$autofreshtime;">~;
    }

    if (($privateforum eq "yes") || ($xzbopen eq "no") || ($startnewthreads eq "no") || ($startnewthreads eq "cert")) {$newthreadbutton3 = "";}
    else {$newthreadbutton3 = qq~<a href=xzb.cgi?action=new&forum=$in_forum><img src=$imagesurl/images/$skin/$newxzblogo border=0 alt=张帖一个小字报></a>　~;}
    if ($pollopen eq "no") {$newthreadbutton2 = "";}
    else {$newthreadbutton2 = qq~<a href=poll.cgi?action=new&forum=$in_forum><img src=$imagesurl/images/$skin/$newpolllogo border=0 alt=开启一个新投票></a>　~;}
    if ($postopen eq "no") {$newthreadbutton1 = "";}
    else {$newthreadbutton1 = qq~<a href=post.cgi?action=new&forum=$in_forum><img src=$imagesurl/images/$skin/$newthreadlogo border=0 alt=发表一个新主题></a>　~;}
    if ($payopen eq "no") {$newthreadbutton4 = "";}
    else {$newthreadbutton4 = qq~<a href=post.cgi?action=pay&forum=$in_forum><img src=$imagesurl/images/$skin/newpay.gif border=0 alt="发表一个新交易，关于支付宝的具体说明请访问 http://www.alipay.com/"></a>　~;}
    $newthreadbutton = "$newthreadbutton1$newthreadbutton2$newthreadbutton3$newthreadbutton4";

    if ($startnewthreads ne "no") {$jinghua = qq~<img src=$imagesurl/images/icon.gif width=14> <a href=jinghua.cgi?action=list&forum=$in_forum><font color=$fonthighlight><B>本版精华</B></font></a>&nbsp;~;}
    unless ($look eq "off") {$lookstyles = qq~<img src=$imagesurl/images/icon.gif width=14> <a href=lookstyles.cgi?forum=$in_forum>本版配色</a>&nbsp;~;}
    $forumlog = qq~<img src=$imagesurl/images/icon.gif width=14> <a href=forumlogs.cgi?forum=$in_forum><font color=$fonthighlight><B>版务日志</B></font></a>&nbsp;~;

    $output .= qq~
<script language="JavaScript" type="text/javascript">
function Download(ForumNo,TopicNo,ReplyNo){
document.Download.forum.value=ForumNo;
document.Download.topic.value=TopicNo;
document.Download.reply.value=ReplyNo;
document.Download.submit();
}
~;

    if ($usefake eq "yes") {
        $output .= qq~
function makepage(numberofpages,topicid,forumid){
var j=0;
if (numberofpages <= 11) {
for (var i=1; i <= numberofpages; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic-"+forumid+"-"+topicid+"-"+j+"-$inshow-.htm class=ha>"+ i +"</a> ");
}}
else{
for (var i=1; i <= 4; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic-"+forumid+"-"+topicid+"-"+j+"-$inshow-.htm class=ha>"+ i +"</a> ");
}
document.write(" . . . ");
for (var i=numberofpages-1; i <= numberofpages; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic-"+forumid+"-"+topicid+"-"+j+"-$inshow-.htm class=ha>"+ i +"</a> ");
}}}
~;
    }
    else {
        $output .= qq~
function makepage(numberofpages,topicid,forumid){
var j=0;
if (numberofpages <= 11) {
for (var i=1; i <= numberofpages; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic.cgi?forum="+forumid+"&topic="+topicid+"&start="+j+"&show=$inshow class=ha>"+ i +"</a> ");
}}
else{
for (var i=1; i <= 4; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic.cgi?forum="+forumid+"&topic="+topicid+"&start="+j+"&show=$inshow class=ha>"+ i +"</a> ");
}
document.write(" . . . ");
for (var i=numberofpages-1; i <= numberofpages; i++){
j = (i-1) * $maxtopics;
document.write("<a href=topic.cgi?forum="+forumid+"&topic="+topicid+"&start="+j+"&show=$inshow class=ha>"+ i +"</a> ");
}}}
~;
    }

    $output .= qq~
</script>
<table cellpadding=0 cellspacing=0 width=$tablewidth>
<tr><td align=center width=2></td><td>$newthreadbutton</td><td align=right colspan=2>$modoutput&nbsp;</td>
<form action=download.cgi name=Download method=POST target=_blank><input type=hidden name=forum><input type=hidden name=topic><input type=hidden name=reply></form>
<form action=jinghua.cgi method=post name=JingHua><input type=hidden name=action value=add><input type=hidden name=forum value="$in_forum"><input type=hidden name=topic></form>
<form action=postings.cgi method=post name=Lock><input type=hidden name=action value="lock"><input type=hidden name=forum value="$in_forum"><input type=hidden name=topic></form>
<form action=forums.cgi method=get name=Jumppage><input type=hidden name=forum value="$in_forum"><input type=hidden name=dshow><input type=hidden name=threadages value=$inthreadages></form>
</tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth><tr><td>$admini$xzb</td><td align=right width=*>$jinghua$forumlog$lookstyles$rsshtml</td><td width=4></td></tr></table>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor>
<form action=delpost.cgi name=Action method=post onsubmit="if ((Action.action.value != 'delete')&&(Action.action.value != 'movetopic')) return false;"><input type=hidden name=forum value="$in_forum"><input type=hidden name=action value="">
<tr><td height=1></td></tr></table>
<table cellpadding=0 cellspacing=0 width=$tablewidth height=27 bordercolor=$tablebordercolor border=1 align=center>
<tr><td bgcolor=$titlecolor $catbackpic width=30 align=center><font color=$titlefontcolor><b>状态</b></td>
<td bgcolor=$titlecolor $catbackpic width=* align=center><font color=$titlefontcolor><b>主　题</b> (点心情符为新闻方式阅读)</td>
<td bgcolor=$titlecolor $catbackpic align=center width=78><font color=$titlefontcolor><b>作 者</b></td>
<td bgcolor=$titlecolor $catbackpic align=center width=60><font color=$titlefontcolor><b>回复/点击</b></td>
<td bgcolor=$titlecolor $catbackpic width=193 align=center><font color=$titlefontcolor><b>　 最后更新 　 | 最后回复人</b></td>
$multimanage</tr></table>
~;

    if (-e "${lbdir}cache/forumstop$in_forum.pl") {
        eval {require "${lbdir}cache/forumstop$in_forum.pl";};
        if ($@) {
            unlink("${lbdir}cache/forumstop$in_forum.pl");
            unlink("${lbdir}cache/plcache$in_forum\_0.pl");
            require "dotop.pl";
            unlink("${lbdir}cache/forumstoptopic$in_forum.pl");
        }
        $jhdata = "" if ($usejhpoint ne "yes");
    }
    else {
        require "dotop.pl";
        unlink("${lbdir}cache/forumstoptopic$in_forum.pl");
        unlink("${lbdir}cache/plcache$in_forum\_0.pl");
    }

    if ($dispabstop ne "0") {
        @absontop = split(/\_/, $absontopdata);
        $abstopcount = @absontop;
        $absontopdata = "\_$absontopdata\_";
    }
    else {
        $abstopcount = 0;
        $absontopdata = "";
    }

    if ($dispcattop ne "0") {
        @catontop = split(/\_/, $catontopdata);
        $cattopcount = @catontop;
        $catontopdata = "\_$catontopdata\_";
    }
    else {
        $cattopcount = 0;
        $catontopdata = "";
    }

    if ($ontopdata ne "") {
        @ontop = split(/\_/, $ontopdata);
        $topcount = @ontop;
        $ontopdata = "\_$ontopdata\_";
    }

    if (($inthreadages) && ($inthreadages ne "all")) {$threadagesstart = "&threadages=$inthreadages";}
    else {undef $threadagesstart;}

    if ((-e "${lbdir}cache/plcache$in_forum\_$inshow.pl") && ((-M "${lbdir}cache/plcache$in_forum\_$inshow.pl") * 86400 < 300) && ($threadagesstart eq "")) {
        open(FILE, "${lbdir}cache/plcache$in_forum\_$inshow.pl");
        $topicpages = <FILE>;
        chomp $topicpages;
        ($abstopcount, $cattopcount, $topcount) = split(/\t/, <FILE>);
        @toptopic = <FILE>;
        close(FILE);
        my $topicnum = @toptopic;
        if ($topicnum < 7) {
            undef @toptopic;
            undef $topicpages;
            unlink("${lbdir}cache/plcache$in_forum\_$inshow.pl");
            require "doplcache.pl";
        }
    }
    else {
        require "doplcache.pl";
    }

    $output .= qq~<script>
var ns6=document.getElementById&&!document.all
var ie=document.all
var customcollect=new Array()
var i=0
function jiggleit(num){
if ((!document.all&&!document.getElementById)) return;
customcollect[num].style.left=(parseInt(customcollect[num].style.left)==-1)? customcollect[num].style.left=1 : customcollect[num].style.left=-1
}
function init(){
i=0;j=0;
if (ie){
while (i <= ($topcount+$abstopcount+$cattopcount)){
if (eval("document.all.jiggle"+i)!=null) {customcollect[j]= eval("document.all.jiggle"+i);j++;}
i++
}}
else if (ns6){
while (i <= ($topcount+$abstopcount+$cattopcount)){
if (document.getElementById("jiggle"+i)!=null) {customcollect[j]= document.getElementById("jiggle"+i);j++;}
i++
}}
if (customcollect.length==1)
setInterval("jiggleit(0)",120)
else if (customcollect.length>1)
for (y=0;y<customcollect.length;y++){
var tempvariable='setInterval("jiggleit('+y+')",'+'140)'
eval(tempvariable)
}}
window.onload=addSenToEventHandle(window.onload,"init();")
</script>
~;

    opendir(DIR, "${imagesdir}$usrdir/$in_forum");
    @usruploadfile = readdir(DIR);
    closedir(DIR);

    $topiccount = 0;
    $jnum = 0;
    $fnum = 0;

    if ($tablewidth > 100) {
        if ($tablewidth > 1000) {$topictitlemax = 84;}
        elsif ($tablewidth > 770) {$topictitlemax = 71;}
        else {$topictitlemax = 40;}
    }
    else {
        if ($screenmode >= 10) {$topictitlemax = 84;}
        elsif ($screenmode >= 8) {$topictitlemax = 71;}
        else {$topictitlemax = 40;}
    }

    $threadagelimit = $currenttime - $inthreadages * 86400;
    foreach $topic (@toptopic) {
        $addonlength = $canusetreeview ne "no" ? 3 : 0;
        chomp $topic;
        ($topicid, $forumid, $topictitle, $topicdescription, $threadstate, $threadposts, $threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, $posttemp, $addmetype) = split(/\t/, $topic);

        if ($multimanage eq "") {$multimanagebutton = "";}
        else {
            $multimanagebutton = qq~<td bgcolor=$forumcolortwo align=center width=25><input type=checkbox name=topic value=$topicid></td>~;
            $addonlength += 2.5;
        }

        if ($forumid eq $in_forum) {
            if ($jhdata =~ /\_$topicid\_/) {
                $jhimage = qq~ <img src=$imagesurl/images/$skin/$new_JH align=absmiddle alt=精华帖子>~;
                $jhbuttom = qq~<a href=jinghua.cgi?action=del&forum=$in_forum&topic=$topicid><font color=$titlecolor>取消精华</font></a>|~;
            }
            else {
                $jhimage = "";
                $jhbuttom = qq~<a href=jinghua.cgi?action=add&forum=$in_forum&topic=$topicid><font color=$titlecolor>精</font></a>|~;
            }
        }
        else {
            $jhimage = "";
            $jhbuttom = "";
        }

        $abslockbuttom = $member_code eq "ad" ? "<a href=postings.cgi?action=abslocktop&forum=$forumid&topic=$topicid><font color=$titlecolor>总固</font></a>|" : "";
        $catlockbuttom = $member_code eq "ad" || $member_code eq "smo" || ",$catemods," =~ /\Q\,$in_member_name\,\E/i ? "<a href=postings.cgi?action=catlocktop&forum=$in_forum&topic=$topicid><font color=$titlecolor>区固</font></a>|" : "";

        $hllink = ($highlight =~ m/\_$forumid-$topicid\_/i) ? "<a href=postings.cgi?action=lowlight&forum=$forumid&topic=$topicid><font color=$titlecolor>取消加重</font></a>" : "<a href=postings.cgi?action=highlight&forum=$forumid&topic=$topicid><font color=$titlecolor>加重</font></a>";

        if (($posticon eq "") || ($posticon =~ /<br>/i)) {
            $posticon = int(myrand(23));
            $posticon = "0$posticon" if ($posticon < 10);
            $posticon = qq~<img src=$imagesurl/posticons/$posticon.gif border=0 align=absmiddle>~;
        }
        else {
            $posticon = qq~<img src=$imagesurl/posticons/$posticon border=0 align=absmiddle>~;
        }

        $numberofitems = $threadposts + 1;
        $numberofpages = $numberofitems / $maxtopics;

        $threadpages = "";
        if ($numberofitems > $maxtopics) {
            if ($numberofpages > int($numberofpages)) {$numberofpages = int($numberofpages) + 1;}
            $gotoendpost = ($numberofpages - 1) * $maxtopics;
            $pagestoshow = qq~<font color=$forumfontcolor>　　[第 <script>makepage($numberofpages,$topicid,$forumid)</script> 页]</font>~;
        }
        else {
            $gotoendpost = "0";
            $pagestoshow = "";
        }

        if ($inthreadages && ($inthreadages ne "all") && (($topiccount >= $topcount + $abstopcount + $cattopcount) || ($startarray ne 0))) {
            if ($lastpostdate < $threadagelimit) {last;}
        }
        if (!$forumlastvisit) {$forumlastvisit = "0";}

        if ($startedpostdate > $currenttime - 3600 * $newmarktime) {
            $topnew = " <img src=$imagesurl/images/$skin/$new_blogo absmiddle>";
            $addonlength += 2;
        }
        else {$topnew = "";}

        if ((lc($in_member_name) eq lc($startedby)) && ($nodispown eq "yes")) {
            $mypost = "<img src=$imagesurl/images/$skin/$mypost_blogo title=我发表的主题> ";
            $addonlength += 2;
        }
        else {$mypost = "";}

        $topicicon = "<img src=$imagesurl/images/$skin/topicnonew.gif border=0>";

        if ($in_member_name ne "客人") {
            if (($threadposts >= $hottopicmark) && ($forumlastvisit < $lastpostdate)) {$topicicon = "<img src=$imagesurl/images/$skin/topichot3.gif border=0>";}
            elsif (($threadposts >= $hottopicmark) && ($forumlastvisit > $lastpostdate)) {$topicicon = "<img src=$imagesurl/images/$skin/topichotnonew.gif border=0>";}
            elsif (($threadposts < $hottopicmark) && ($forumlastvisit < $lastpostdate)) {$topicicon = "<img src=$imagesurl/images/$skin/topicnew3.gif border=0>";}
            elsif (($threadposts < $hottopicmark) && ($forumlastvisit > $lastpostdate)) {$topicicon = "<img src=$imagesurl/images/$skin/topicnonew.gif border=0>";}
        }

        $threadstate = "poll" if (($posticon =~ /<br>/i) && ($threadstate eq ""));
        if (($threadstate eq "poll") || ($threadstate eq "pollclosed")) {
            if (open(FILE, "${lbdir}forum$forumid/$topicid.poll.cgi")) {
                my @allpoll = <FILE>;
                close(FILE);
                $size = @allpoll;
            }
            else {
                $size = 0;
            }
        }
        if ($threadstate eq "closed") {$topicicon = "<img src=$imagesurl/images/$skin/topiclocked3.gif border=0>";}
        elsif ($threadstate eq "poll") {
            if ($size >= $hotpollmark) {$topicicon = "<img src=$imagesurl/images/$skin/closedbhot.gif border=0>";}
            else {$topicicon = "<img src=$imagesurl/images/$skin/closedb.gif border=0>";}
        }
        elsif ($threadstate eq "pollclosed") {$topicicon = "<img src=$imagesurl/images/$skin/closedb1.gif border=0>";}

        if ($lastpostdate ne "") {
            $lastpostdate = $lastpostdate + $addtimes;
            $lastpostdate = &dateformatshort("$lastpostdate");
        }
        else {$lastpostdate = qq~没有~;}

        if ($addtopictime eq "yes") {
            my $topictime = &dispdate($startedpostdate + $addtimes);
            $topictitle = "[$topictime] $topictitle";
        }

        $startedpostdate = $startedpostdate + $addtimes;
        $startedlongdate = &dateformat("$startedpostdate");
        $startedpostdate = qq~$startedlongdate~;

        $posttemp = "(无内容)" if ($posttemp eq "");

        $topictitletemp = &lbhz($topictitle, $topictitlemax - 6);

        $highlightstyle = $topiccount < $abstopcount && $startarray == 0 ? qq~style="color:$color_of_absontop; font-weight:900"~ : $topiccount < $abstopcount + $cattopcount && $startarray == 0 ? qq~style="color:$color_of_quontop; font-weight:900"~ : $topiccount < $abstopcount + $cattopcount + $topcount && $startarray == 0 ? qq~style="color:$color_of_ontop; font-weight:900"~ : $highlight =~ m/\_$forumid-$topicid\_/ ? qq~style="color:$color_of_hightopic; font-weight:600"~ : "";

        $topictitle = qq~<a href=topic.cgi?forum=$forumid&topic=$topicid&show=$inshow title="$topictitle \n发布时间： $startedpostdate \n最后回复： $posttemp "$highlightstyle t>$topictitletemp</a>~;

        if ($lastposter) {
            if ($lastposter =~ /\(客\)/) {
                $lastposter =~ s/\(客\)//isg;
                $lastposter = qq~<font color=$postfontcolorone title=此为未注册用户>$lastposter</font>~;
            }
            else {
                my $lastposterfilename = $lastposter;
                $lastposterfilename =~ s/ /\_/isg;
                $lastposterfilename =~ tr/A-Z/a-z/;
                $lastposter = qq~<span style=cursor:hand onClick="javascript:O9('~ . uri_escape($lastposterfilename) . qq~')">$lastposter</span>~;
            }
        }
        else {$lastposter = qq~--------~;}

        if ($topicdescription) {
            my $topicdescriptiontemp = $topicdescription;
            $topicdescriptiontemp =~ s/\s*(.*?)\s*\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/$3/isg;
            $topicdescriptiontemp =~ s/\<\/a\>//isg;
            if (length($topicdescriptiontemp) > ($topictitlemax - 4)) {
                $topicdescriptiontemp = &lbhz("$topicdescriptiontemp", $topictitlemax);
                $topicdescription =~ s/\<a \s*(.*?)\s*\>\s*(.*?)\s*\<\/a\>/\<a $1\>$topicdescriptiontemp\<\/a\>/isg;
            }
            $topicdescription = qq~<br>　　-=> $topicdescription~;
        }

        if (($topiccount >= $abstopcount + $cattopcount) || ($startarray ne 0) || ($forumid eq $in_forum)) {
            my @usruploadfile = grep (/^$in_forum\_$topicid(\.|\_)/, @usruploadfile);
            if ($#usruploadfile >= 0 || $addmetype ne "") {
                my @files = grep (/^$in_forum\_$topicid\./, @usruploadfile);
                if ($#files >= 0 || $addmetype ne "") {
                    if ($addmetype eq "") {
                        my $usrfilename = $files[0];
                        chomp $usrfilename;
                        ($up_name, $up_ext) = split(/\./, $usrfilename);
                    }
                    else {
                        $up_ext = $addmetype;
                    }
                    $up_ext =~ tr/A-Z/a-z/;
                    $filetype = "unknow";
                    $filetype = $up_ext if (-e "${imagesdir}icon/$up_ext.gif");

                    if (($up_ext eq 'jpg') || ($up_ext eq 'gif') || ($up_ext eq 'bmp') || ($up_ext eq 'png')) {$topictitle = "<img src=$imagesurl/icon/$filetype.gif width=16 alt=\"该主题含有 $filetype 格式的图片\" border=0 align=absmiddle></a> " . $topictitle;}
                    elsif ($up_ext eq "swf") {$topictitle = "<img src=$imagesurl/icon/$filetype.gif width=16 alt=\"该主题含有 $filetype 格式的动画\" border=0 align=absmiddle></a> " . $topictitle;}
                    else {
                        $topictitle = "<img src=$imagesurl/icon/$filetype.gif width=16 align=absmiddle alt=\"该主题含有“$filetype”类型的附件\" border=0></a> " . $topictitle;
                    }
                    $addonlength += 4;
                }
            }
        }
        if ($numberofpages == 0) {$pagestoshowtemp1 = 0;}
        elsif ($numberofpages > 11) {$pagestoshowtemp1 = 41;}
        else {$pagestoshowtemp1 = int($numberofpages) * 3.3 + 7;}
        $totlelength = $pagestoshowtemp1 + length($topictitletemp) + 3 + $addonlength; #标题栏的总长度

        if (($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {
            if ($member_code ne "amo") {
                $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>|$hllink|$jhbuttom$abslockbuttom$catlockbuttom<a href=postings.cgi?action=locktop&forum=$in_forum&topic=$topicid><font color=$titlecolor>固</font></a>|<a href=postings.cgi?action=puttop&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>提</font></a>|<a href=postings.cgi?action=putdown&forum=$in_forum&topic=$topicid><font color=$titlecolor>沉</font></a>|<a href=postings.cgi?action=lock&forum=$in_forum&topic=$topicid><font color=$titlecolor>锁</font></a>|<a href=postings.cgi?action=unlock&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|<a href=delpost.cgi?action=delete&forum=$in_forum&topic=$topicid><font color=$titlecolor>删</font></a>|<a href=delpost.cgi?action=movetopic&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>移</font></a>|</font>&nbsp;</DIV>~;
            }
            else {
                $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>|$hllink|<a href=postings.cgi?action=puttop&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>提</font></a>|<a href=postings.cgi?action=putdown&forum=$in_forum&topic=$topicid><font color=$titlecolor>沉</font></a>|<a href=postings.cgi?action=lock&forum=$in_forum&topic=$topicid><font color=$titlecolor>锁</font></a>|<a href=postings.cgi?action=unlock&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|</font>&nbsp;</DIV>~;
            }
        }
        elsif ((lc($in_member_name) eq lc($startedby)) && ($in_member_name !~ /^客人/)) {
            if ($arrowuserdel eq "on") {
                $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>快速操作： ~;
                $admini .= qq~| <a href=postings.cgi?action=lock&forum=$in_forum&topic=$topicid><font color=$titlecolor>锁定此帖，不允许别人回复</font></a> ~ unless ($threadstate eq "closed");
                $admini .= qq~| <a href=delpost.cgi?action=delete&forum=$in_forum&topic=$topicid><font color=$titlecolor>删除此帖</font></a> |</font>&nbsp;</DIV>~;
            }
            else {undef $admini;}
        }
        else {undef $admini;}
        if (($startarray eq 0) && ($topiccount < $topcount + $abstopcount + $cattopcount)) {
            if ($topiccount < $abstopcount) {
                if ($member_code eq "ad") {
                    $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>|<a href=postings.cgi?action=absunlocktop&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>取消总固顶</font></a>|<a href=postings.cgi?action=abslocktop&forum=$forumid&topic=$topicid><font color=$titlecolor>顶</font></a>|$jhbuttom<a href=postings.cgi?action=lock&forum=$forumid&topic=$topicid><font color=$titlecolor>锁</font></a>|<a href=postings.cgi?action=unlock&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|</font>&nbsp;</DIV>~;
                }
                else {undef $admini;}
                $topicicon = "<img src=$imagesurl/images/$skin/abstop.gif border=0>";
                $topictitle =~ s/\&nbsp\;\"\>/\&nbsp\;\" target=\_blank\>/isg;
                $pagestoshow =~ s/ class=ha\>/ target=\_blank class=ha\>/isg;
                $topictitle = "<font color=$color_of_absontop><B>[公告]</B></font> $topictitle";
                if ($abstopshake eq "1") {
                    $topictitle = "<span id=jiggle$jnum class=jc>$topictitle</span>";
                    $jnum++;
                }
                elsif ($abstopshake eq "2") {
                    $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=0 flashcolor=$color_of_absontop>/s;
                    $fnum++;
                }
                elsif ($abstopshake eq "3") {
                    $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=1 flashcolor=#cccccc>/s;
                    $fnum++;
                }
                $totlelength = $totlelength + 5;
                $multimanagebutton = "<td bgcolor=$forumcolortwo width=25>&nbsp;</td>" if ($multimanagebutton ne "");
            }
            elsif ($topiccount < $cattopcount + $abstopcount) {
                if ($member_code eq "ad" || $member_code eq "smo" || ",$catemods," =~ /\Q\,$in_member_name\,\E/i) {
                    $admini = qq~<div id=admini style="display:$admindisp" align=right><font color=$titlecolor>|<a href=postings.cgi?action=catunlocktop&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>取消区固顶</font></a>|$abslockbuttom<a href=postings.cgi?action=catlocktop&forum=$forumid&topic=$topicid><font color=$titlecolor>顶</font></a>|$jhbuttom<a href=postings.cgi?action=lock&forum=$forumid&topic=$topicid><font color=$titlecolor>锁</font></a>|<a href=postings.cgi?action=unlock&forum=$forumid&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|</font>&nbsp;</div>~;
                }
                else {$admini = "";}
                $topicicon = "<img src=$imagesurl/images/$skin/lockcattop.gif border=0>";
                $topictitle =~ s/\ \;\"\>/\ \;\" target=\_blank\>/isg;
                if ($cattopshake eq "1") {
                    $topictitle = "<span id=jiggle$jnum class=jc>$topictitle</span>";
                    $jnum++;
                }
                elsif ($cattopshake eq "2") {
                    $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=0 flashcolor=$color_of_quontop>/s;
                    $fnum++;
                }
                elsif ($cattopshake eq "3") {
                    $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=1 flashcolor=#cccccc>/s;
                    $fnum++;
                }
                $pagestoshow =~ s/ class=ha\>/ target=\_blank class=ha\>/isg;
                $multimanagebutton = "<td bgColor=$forumcolortwo width=25>&nbsp;</td>" if ($multimanagebutton ne "");
            }
            elsif ($topiccount < $topcount + $abstopcount + $cattopcount) {
                if (($member_code eq "ad") || ($inmembmod eq "yes") || ($member_code eq 'smo')) {
                    $admini = qq~<DIV id=admini style="display:$admindisp" ALIGN=Right><font color=$titlecolor>|<a href=postings.cgi?action=unlocktop&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>取消固顶</font></a>|$abslockbuttom$catlockbuttom<a href=postings.cgi?action=locktop&forum=$in_forum&topic=$topicid><font color=$titlecolor>顶</font></a>|$jhbuttom<a href=postings.cgi?action=lock&forum=$in_forum&topic=$topicid><font color=$titlecolor>锁</font></a>|<a href=postings.cgi?action=unlock&forum=$in_forum&topic=$topicid&checked=yes><font color=$titlecolor>解</font></a>|</font>&nbsp;</DIV>~;
                }
                else {undef $admini;}
                $topicicon = "<img src=$imagesurl/images/$skin/locktop.gif border=0>";
                $multimanagebutton = "<td bgcolor=$forumcolortwo width=25>&nbsp;</td>" if ($multimanagebutton ne "");
                if ($topshake eq "1") {
                    $topictitle = "<span id=jiggle$jnum class=jc>$topictitle</span>";
                    $jnum++;
                }
                elsif ($topshake eq "2") {
                    $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=0 flashcolor=$color_of_ontop>/s;
                    $fnum++;
                }
                elsif ($topshake eq "3") {
                    $topictitle =~ s/\ t\>/ id=flashlink$fnum flashtype=1 flashcolor=#cccccc>/s;
                    $fnum++;
                }
            }
        }
        $topictitle = "$mypost$topictitle";
        $topictitle .= $topnew;
        $topictitle .= $jhimage;
        $topictitle = $topictitle . "<BR>" if ($totlelength > $topictitlemax + 7);

        #    if ($threadviews > 9999) { $threadviewstemp = "<font color=$forumfontcolor title=点击：$threadviews>>Max</font>"; } else { $threadviewstemp = "<font color=$forumfontcolor>$threadviews</font>"; }
        #    if ($threadposts > 9999) { $threadpoststemp = "<font color=$forumfontcolor title=回复：$threadposts>>Max</font>"; } else { $threadpoststemp = "<font color=$forumfontcolor>$threadposts</font>"; }

        if ($threadposts < 1000 && $threadviews < 1000) {
            $threadposts = "$threadposts ";
            $threadviews = " $threadviews";
        }

        $startedbyfilename = $startedby;
        $startedbyfilename =~ s/ /\_/isg;
        $startedbyfilename =~ tr/A-Z/a-z/;

        if (($threadstate eq "poll") || ($threadstate eq "pollclosed")) {$outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=60 TITLE="回复：$threadposts 篇\n点击：$threadviews 次"><font color=$forumfontcolor>共 $size 票</font></td>~;}
        else {$outputtemp = qq~<td bgcolor=$forumcolortwo align=center width=60><font color=$forumfontcolor>$threadposts<font color=$fonthighlight>/</font>$threadviews</td>~;}
        if ($startedby =~ /\(客\)/) {
            $startedby =~ s/\(客\)//isg;
            $startedby = qq~<font color=$postfontcolorone title=此为未注册用户>$startedby</font>~;
        }
        else {$startedby = qq~<span style=cursor:hand onClick=javascript:O9('~ . uri_escape($startedbyfilename) . qq~')>$startedby</span>~;}
        if (($startarray eq 0) && ($topiccount < $abstopcount + $cattopcount)) {
            $topicicontemp = qq~<span style=cursor:hand onClick=javascript:O5($forumid,$topicid)>$topicicon</span>~;
            $posticontemp = qq~<span style=cursor:hand onClick=javascript:O6($forumid,$topicid)>$posticon</span>~;
        }
        else {
            $topicicontemp = qq~<span style=cursor:hand onClick=javascript:O1($topicid)>$topicicon</span>~;
            $posticontemp = qq~<span style=cursor:hand onClick=javascript:O2($topicid)>$posticon</span>~;
        }
        #文章树
        if ($canusetreeview ne "no") {
            if ($threadposts > 0) {$nofollow = "cat.gif";}
            else {$nofollow = "cat1.gif";}
            $id_of_this_topid = sprintf("%04d%05d", $forumid, $topicid);
            $followImg = qq(<img id=followImg$id_of_this_topid title=展开文章树 style=CURSOR:hand onclick=loadThreadFollow($forumid,$topicid,'$id_of_this_topid') src=$imagesurl/images/$nofollow width=9 loaded=no nofollow=$threadposts> );
        }
        else {undef $followImg;}

        $output .= qq~<table cellspacing=0 cellpadding=0 width=$tablewidth bordercolor=$tablebordercolor border=1 height=35><tr><td align=center width=30 bgcolor=$forumcolorone>$topicicontemp</td>
<td width=* class=dp bgColor=$forumcolortwo onmouseover=this.bgColor='$forumcolorone'; onmouseout=this.bgColor='$forumcolortwo';>&nbsp;$posticontemp $followImg<span id=forum>$topictitle$pagestoshow$topicdescription$admini</span></td>
<td align=center width=78 bgcolor=$forumcolorone>$startedby</td>$outputtemp<td width=193 bgcolor=$forumcolorone>&nbsp;<span style=cursor:hand onClick=javascript:O3($forumid,$topicid,$gotoendpost)>$lastpostdate</span><font color=$fonthighlight> | </font>$lastposter</td>$multimanagebutton</tr></table>
~;

        $output .= qq~<table cellspacing=0 width=$tablewidth bordercolor=$tablebordercolor border=1 id=follow$id_of_this_topid style=DISPLAY:none><tr><td id=followTd$id_of_this_topid><DIV class=ts onclick=loadThreadFollow($forumid,$topicid,'$id_of_this_topid')>正在读取，请稍候 ...</DIV></td></tr></table>~ if ($canusetreeview ne "no");
        $topiccount++;
    }
    $pn = ($inshow / $maxthreads) + 1;
    $output .= qq~</tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT><table cellpadding=0 cellspacing=2 width=$tablewidth><tr height=4></tr><tr><td>$topicpages，<b>转至</b>：<input type=text name="dshow" size=2 value="$pn"> <input type=button value=Go onClick="Jumptopage(this.form)"><BR> [本版共有主题 <B>$threads</B> 篇，回复 <b>$posts</b> 篇]</td>$multimanageitem</form>~;

    if (($indexforum ne "no") && ($dispjump ne "no")) {
        require "${lbdir}data/forumjump.pl" if (-e "${lbdir}data/forumjump.pl");
        $jumphtml =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg if (($disphideboard eq "yes") || ($member_code eq "ad") || ($member_code eq "smo") || ($member_code eq "cmo") || ($member_code eq "mo") || ($member_code eq "amo"));
        $jumphtml =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg if ($dispchildjump ne "no");
        $jumphtml = "<tr><td align=right>$jumphtml</td></form>";
    }
    else {$jumphtml = "";}

    $output .= qq~<td align=right><table cellpadding=0 cellspacing=2>~;
    $output .= qq~<tr><td align=right><form action=search.cgi method=post><input type=hidden name=action value=startsearch><input type=hidden name=POST_SEARCH value=topictitle_search><input type=hidden name=NAME_SEARCH value=topictitle_search><input name=SEARCH_STRING value=输入关键字 onfocus="this.value ='';" size=14><select name=TYPE_OF_SEARCH><option value="keyword_search">主题<option value="username_search">作者</select><input type=hidden name=FORUMS_TO_SEARCH value=$in_forum> <input type=submit value=搜索></td></form></tr>~ if ($searchopen ne "99");
    $output .= qq~$jumphtml</table></td></tr></table></tr></table><br>~;

    if ($usefastpost ne "no") {require "forumfastpost.pl";}
}
else {

    if (($indexforum ne "no") && ($dispjump ne "no")) {
        require "${lbdir}data/forumjump.pl" if (-e "${lbdir}data/forumjump.pl");
        $jumphtml =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg if (($disphideboard eq "yes") || ($member_code eq "ad") || ($member_code eq "smo") || ($member_code eq "cmo") || ($member_code eq "mo") || ($member_code eq "amo"));
        $jumphtml =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg if ($dispchildjump ne "no");
        $jumphtml = "<tr><td align=right>$jumphtml</td></form>";
    }
    else {$jumphtml = "";}

    $output .= qq~<table cellpadding=1 cellspacing=0 width=$tablewidth><tr><td align=right>$jumphtml</td></tr></table>~;
    $output .= "<BR><center><font color=$fonthighlight><B>这里是纯子论坛板块，请选择进入相应子论坛</B></font><BR><BR><BR>";
}
if (($dispview eq "yes") || (($member_code eq "ad" || $inmembmod eq "yes" || $member_code eq 'smo') && ($member_code ne 'amo'))) {require "dodispviewforum.pl";}

&output("$forumname", \$output);
exit;