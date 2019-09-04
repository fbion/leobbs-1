#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

use warnings;
use strict;
use diagnostics;

$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100) && ($maxpoststr ne ""));
if ($emoticons eq "on") {$emoticonslink = qq~<input CHECKED name=inshowemoticons type=checkbox value=yes>使用表情字符转换？~;}
if ($emailfunctions eq "on") {
    if ($innotify eq "yes") {$requestnotify = qq~<input name=notify type=checkbox value=yes checked>有回复时使用邮件通知您？<br>~;}
    else {$requestnotify = qq~<input name=notify type=checkbox value=yes>有回复时使用邮件通知您？<br>~;}
}
if ($canchgfont ne "no") {
    $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes">使用字体转换？<br>~;
}
else {
    undef $fontpost;
}
if ($idmbcodestate eq "on") {
    $idmbcodestates = qq~<input type=checkbox name="uselbcode" value="yes" checked>使用 LeoBBS 标签？<BR>~;
}
else {
    $idmbcodestates = "";
}

$maxpoststr = "[帖子中最多包含 <B>$maxpoststr</B> 个字符]" if ($maxpoststr ne "");
$output .= qq~<form action=post.cgi method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name=action value=addreply>
<input type=hidden name=forum value=$in_forum>
<input type=hidden name=topic value=$in_topic>
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=5 cellSpacing=1 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td bgcolor=$titlecolor width=220 $catbackpic><font color=$fontcolormisc><b>快速回复主题:</b></font></td><td bgcolor=$titlecolor width=500 $catbackpic> <font color=$fontcolormisc>$topictitletemp</font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=3><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$in_member_name</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>输入用户名和密码:</b></font></td><td bgcolor=$miscbackone> <font color=$fontcolormisc><b>用户名</b>: <input type=text name=membername> <span onclick="javascript:location.href='register.cgi?forum=$in_forum'" style=cursor:hand>没有注册？</span>　<b>密码:</b> <input type=password name=password> <a href=profile.cgi?action=lostpass style=cursor:help>忘记密码？</a></font></td></tr>
~;

if (($allowattachment ne "no") || ($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($myinmembmod eq "yes")) {
    $uploadreqire = "" if ($uploadreqire <= 0);
    $uploadreqire = "<BR>发帖数要大于 <B>$uploadreqire</B> 篇(认证用户不限)" if ($uploadreqire ne "");
    $output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
    $output .= qq~<tr><td bgcolor=$miscbackone><b>上传附件或图片</b> (最大容量 <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone colspan=2> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$in_forum&topic=$in_topic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>目前附件:(如不需要某个附件，只需删除内容中的相应 [UploadFile$imgslt ...] 标签即可)  [<a href=upfile.cgi?action=delup&forum=$in_forum target=upframe title=删除所有未被发布的附件临时文件 OnClick="return confirm('确定删除所有未被发布的附件临时文件么？');">删除</a>] </font></font><SPAN id=showupfile name=showupfile></SPAN></td></tr>~;
}
$output .= qq~
<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>选项</b>　~;

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
<br>$maxpoststr<BR>
$idmbcodestates
<input CHECKED name=inshowsignature type=checkbox value=yes>显示您的签名？<br>
$requestnotify$emoticonslink<BR>$fontpost</font></td>
<td bgcolor=$miscbacktwo width=*> <A name=sub></A><textarea cols=75 name=inpost onKeyDown=ctlent() rows=8 title='使用 Ctrl+Enter 直接提交贴子'></textarea><br>
 <INPUT name=Submit onclick="return clckcntr();" type=submit value="发 表 回 复">　<input type=button value="预 览 内 容" name=Button onclick=gopreview()>　<INPUT name=Clear type=reset value="清 除">　　快速引用第 <input name=floor value="" size="4" maxlength="4"> 楼层的回复
</td></tr></table><SCRIPT>valignend()</SCRIPT></form>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$in_forum"></form>
<script>
function gopreview(){
document.preview.body.value=document.FORM.inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.preview.submit()
}
</script>
~;
1;
