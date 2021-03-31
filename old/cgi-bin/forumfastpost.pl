#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.leobbs.org/            #
#      论坛地址： http://bbs.leobbs.org/            #
#####################################################

use warnings;
use strict;
use diagnostics;

$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100) && ($maxpoststr ne ""));
if ($startnewthreads eq "no") {$startthreads = "在此论坛中新的主题和帖子回复只能由坛主、版主发表！";}
elsif ($startnewthreads eq "follow") {$startthreads = "在此论坛中新的主题只能由坛主、版主发表！普通会员只可以跟帖！";}
elsif ($startnewthreads eq "all") {$startthreads = "任何人均可以发表和回复主题，未注册用户发帖密码请留空！";}
elsif ($startnewthreads eq "cert") {$startthreads = "在此论坛中新的主题只能由坛主、版主、认证的会员发表！";}
else {$startthreads = "所有注册会员均可以发表和回复主题！";}

if ($emailfunctions eq "on") {
    if ($innotify eq "yes") {$requestnotify = " checked";}
    else {$requestnotify = "";}
    $requestnotify = qq~&nbsp;<input type=checkbox name="notify" value="yes"$requestnotify>有回复时使用邮件通知您？<br>~;
}
if ($emoticons eq "on") {
    $emoticonslink = qq~<li><span style=cursor:hand onClick="javascript:openScript('$miscprog?action=showsmilies',300,350)">允许<B>使用</B>表情字符转换</span>~;
    $emoticonsbutton = qq~&nbsp;<input type=checkbox name="inshowemoticons" value="yes" checked>您是否希望<b>使用</b>表情字符转换？<br>~;
}
$maxpoststr = "(帖子中最多包含 <B>$maxpoststr</B> 个字符)" if ($maxpoststr ne "");
if ($canchgfont ne "no") {
    $fontpost = qq~&nbsp;<input type=checkbox name="inshowchgfont" value="yes">使用字体转换？<br>~;
}
else {
    undef $fontpost;
}

if ($idmbcodestate eq "on") {
    $idmbcodestates = qq~&nbsp;<input type=checkbox name="uselbcode" value="yes" checked>使用 LeoBBS 标签？<BR>~;
}
else {
    $idmbcodestates = "";
}

$output .= qq~<script>
function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
function DoTitle(addTitle) { var revisedTitle;var currentTitle = document.FORM.intopictitle.value;revisedTitle = addTitle+currentTitle;document.FORM.intopictitle.value=revisedTitle;document.FORM.intopictitle.focus();return;}
</script><form action=post.cgi method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name=action value=addnew>
<input type=hidden name=forum value="$in_forum">
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic>&nbsp;<font color=$titlefontcolor><b>快速发表新主题</b></font> -- $startthreads</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <B><u><font color=$fonthighlight>$in_member_name</font></u></B> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbacktwo width=220>&nbsp;<font color=$fontcolormisc><b>输入用户名和密码:</b></font></td><td bgcolor=$miscbacktwo>　<font color=$fontcolormisc><b>用户名</b>: <input type=text name=membername> <span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style=cursor:hand>没有注册？</span>　<b>密码:</b> <input type=password name=password> <a href=profile.cgi?action=lostpass style=cursor:help>忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbackone>&nbsp;<font color=$fontcolormisc><b>主题标题</b></font>　
<select name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
<OPTION selected value="">选择话题</OPTION> <OPTION value=[原创]>[原创]</OPTION><OPTION value=[转帖]>[转帖]</OPTION><OPTION value=[灌水]>[灌水]</OPTION><OPTION value=[讨论]>[讨论]</OPTION><OPTION value=[求助]>[求助]</OPTION><OPTION value=[推荐]>[推荐]</OPTION><OPTION value=[公告]>[公告]</OPTION><OPTION value=[注意]>[注意]</OPTION><OPTION value=[贴图]>[贴图]</OPTION><OPTION value=[建议]>[建议]</OPTION><OPTION value=[下载]>[下载]</OPTION><OPTION value=[分享]>[分享]</OPTION>
</SELECT></td>
<td bgcolor=$miscbackone>　<input type=text size=60 maxlength=80 name="intopictitle" value="$in_topictitle">　不得超过 40 个汉字</td></tr>
<td bgcolor=$miscbacktwo valign=top>&nbsp;<font color=$fontcolormisc><b>选项</b>　~;

if ($magicface ne 'off') {
    $output .= qq~
<style>
.gray	{cursor: hand; filter:gray}
</style>
<script>
function magicfaceopen() {javascript:openScript('misc.cgi?action=showmagicface',400,550);}
function enable(btn){btn.filters.gray.enabled=0;}
function disable(btn){btn.filters.gray.enabled=1;}
</script>

<IMG onclick=magicfaceopen() align=absmiddle height=22 alt=插入魔法表情 src=$imagesurl/btg/magicface.gif width=23  class="gray" onmouseover="enable(this)" onmouseout="disable(this)">
~;
}

$output .= qq~
<br>$maxpoststr<BR>$idmbcodestates
&nbsp;<input type=checkbox name="inshowsignature" value="yes" checked>显示签名？<br>
$requestnotify$emoticonsbutton$fontpost</center>
<td bgcolor=$miscbacktwo>　<TEXTAREA cols=80 name=inpost rows=9 wrap="soft" onkeydown=ctlent()>$inpost</TEXTAREA><br></td></tr>~;

if (($arrowupload ne "off") || ($member_code eq "ad") || ($member_code eq 'smo') || ($inmembmod eq "yes")) {
    $uploadreqire = "" if ($uploadreqire <= 0);
    $uploadreqire = "<BR>发帖数要大于 <B>$uploadreqire</B> 篇(认证用户不限)" if ($uploadreqire ne "");
    $output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
    $output .= qq~<tr><td bgcolor=$miscbackone><b>上传附件或图片</b> (最大容量 <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$in_forum&topic=$in_topic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>目前附件:(如不需要某个附件，只需删除内容中的相应 [UploadFile$imgslt ...] 标签即可)  [<a href=upfile.cgi?action=delup&forum=$in_forum target=upframe title=删除所有未被发布的附件临时文件 OnClick="return confirm('确定删除所有未被发布的附件临时文件么？');">删除</a>] </font><SPAN id=showupfile name=showupfile></SPAN></td></tr>~;
}
$output .= qq~<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=Submit value="发 表 新 主 题" name=Submit onClick="return clckcntr();">　　<input type=button value='预 览 内 容' name=Button onclick=gopreview()>　　<input type="reset" name="Clear" value="清 除"></td></tr></table></td></tr></table><SCRIPT>valignend()</SCRIPT></form>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$in_forum"></form>
<script>
function gopreview(){
document.preview.body.value=document.FORM.inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.preview.submit()
}
</script>~;
1;
