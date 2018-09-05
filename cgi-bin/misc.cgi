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
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "misc.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$UIN     = $query -> param('UIN');
$UIN     = &cleaninput("$UIN");
$UIN =~ s/[^0-9]//isg;
$action  = $query -> param('action');
$action  = &cleaninput("$action");

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "客人" ) { $inmembername = "客人"; }
if ($action eq "showsmilies") {
    $output = qq~ 
<p>
<SCRIPT>valigntop()</SCRIPT>
    <table width=$tablewidth cellpadding=0 cellspacing=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1>
            <tr>
                <td bgcolor=$miscbackone $catbackpic align=center colspan=2>
                    <font color=$titlefontcolor><b>$boardname - 表情转换</b></font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo align=center>
                    <font color="$fontcolormisc">代码</font>
                </td>
                    <td bgcolor=$miscbacktwo align=center>
                    <font color=$fontcolormisc>转换后</font>
                </td>
                </tr>
    ~;
    
        open (FILE, "$lbdir/data/lbemot.cgi");
	my @emoticondata = <FILE>;
	close (FILE);
	chomp @emoticondata;
        
    foreach $picture (@emoticondata) {
	$smileyname = $picture;
	$smileyname =~ s/\.gif//g;
	$output .= qq~
	<tr>
	<td bgcolor=$miscbackone align=center>
	<font color=$fontcolormisc>:$smileyname:</font>
	</td>
	<td bgcolor=$miscbackone align=center>
	<img src=$imagesurl/emot/$picture>
	</td>
	</tr>
	~;
    }
    $output .= qq~
	</table>
	</td></tr>
	</table><SCRIPT>valignend()</SCRIPT>
	</body>
	</html>
    ~;
}
elsif ($action eq "showmagicface") {
    $CountLength = 0;
    opendir(DIR,"$imagesdir/MagicFace/gif/");
    @files = readdir(DIR);
    closedir(DIR);
    @numbers = grep(/\.gif$/i,@files);
    $CountLength = @numbers;
    
    $output = qq~ 
<script>
function MM_showHideLayers() {
	var i,p,v,obj,args=MM_showHideLayers.arguments;
	obj=document.getElementById("MagicFace");
	for (i=0; i<(args.length-2); i+=3) if (obj) { v=args[i+2];if (obj.style) { obj=obj.style; v=(v=='show')?'visible':(v=='hide')?'hidden':v; }obj.visibility=v; }
}
function ShowMagicFace(MagicID){var MagicFaceUrl = "$imagesurl/MagicFace/swf/" + MagicID + ".swf";document.getElementById("MagicFace").innerHTML = '<object codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="500" height="350"><param name="movie" value="'+ MagicFaceUrl +'"><param name="menu" value="false"><param name="quality" value="high"><param name="play" value="false"><param name="wmode" value="transparent"><embed src="' + MagicFaceUrl +'" wmode="transparent" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" width="500" height="350"></embed></object>';document.getElementById("MagicFace").style.top = (document.body.scrollTop+((document.body.clientHeight-300)/2))+"px";document.getElementById("MagicFace").style.left = (document.body.scrollLeft+((document.body.clientWidth-480)/2))+"px";document.getElementById("MagicFace").style.visibility = 'visible';MagicID += Math.random();setTimeout("MM_showHideLayers('MagicFace','','hidden')",8000);var NowMeID = MagicID;}
function ShowForum_Emot(page){
	var CountLength = $CountLength;
	var page_size = 25
	var showlist = ''
	var pagelist = ''
	var Page_Max = CountLength/page_size
	if ((CountLength % page_size)>0)Page_Max = Math.floor(Page_Max+1);
	for (i=page*page_size-page_size+1;i<=page*page_size;i++)
	{
		Audibles_ID = i;
		Audibles_Url = "$imagesurl/MagicFace/gif/"+Audibles_ID + ".gif";
		if (i<=CountLength)
		{
			showlist = showlist + '<tr><td width=33% align=center bgcolor=$miscbackone>第'+i+'个表情</td><td width=34% bgcolor=$miscbackone align=center><img src="'+ Audibles_Url +'" onclick="ShowMagicFace('+Audibles_ID+');"  style="cursor:hand;"></td>'
			showlist = showlist + '<td width=33% align=center bgcolor=$miscbackone><input type=button value=" 插入 "  onclick="InnerAudibles(\\'' + Audibles_ID + '\\')"><\\/td><\\/tr>'
		}
	}
	for (i=1;i<=Page_Max;i++)pagelist += (i==page)? '<font color=gray>['+i+']</font> ':'<A href="javascript:ShowForum_Emot('+i+')">['+i+']</A> '
	showlist = showlist + '<tr><td bgcolor=$miscbacktwo align=center colspan=3>'+ pagelist +'</TD></TR><tr><td bgcolor=$miscbacktwo align=center colspan=3><font color=blue>点击图片预览表情动画，每次只能一个.</font></TD></tr>'
	showlist = '<tr><td><table width=100% cellpadding=5 cellspacing=1>' + showlist + '</table></td></tr>'
	document.getElementById("AudiblesShow").innerHTML = showlist ;
}

function InnerAudibles(id)
{
	opener.FORM.inpost.value +='[MagicFace='+id+']';
	self.close();
}
</script>
<DIV id=MagicFace style="Z-INDEX: 99; VISIBILITY: hidden; POSITION: absolute"></DIV>
<SCRIPT>valigntop()</SCRIPT>
<table width=$tablewidth cellpadding=0 cellspacing=0 align=center bgcolor=$tablebordercolor>
<TD id="AudiblesShow"></TD></table><SCRIPT>valignend()</SCRIPT>
<script>ShowForum_Emot(1)</script>

~;

}
elsif ($action eq "icq") {
    $output = qq~
<p>
<SCRIPT>valigntop()</SCRIPT>
    <table width=$tablewidth cellpadding=0 cellspacing=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <form action="http://wwp.mirabilis.com/scripts/WWPMsg.dll" method="post">
        <input type="hidden" name="subject" value="来自 - $boardname"><input type="hidden" name="to" value="$UIN">
        <table width=100% cellpadding=5 cellspacing=1>
            <tr>
                <td bgcolor=$miscbackone align=center colspan=2>
                    <font color=$titlefontcolor><b>$boardname - ICQ 寻呼</b><br>发送一个消息给 $UIN</font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbacktwo valign=top>
                    <font color=$fontcolormisc>请输入您的姓名</font>
                </td>
                    <td bgcolor=$miscbacktwo>
                    <input type="text" name="from" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top>
                    <font color=$fontcolormisc>请输入您的 Email</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <input type="text" name="fromemail" size="20" maxlength="40">
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone valign=top>
                    <font color=$fontcolormisc>要发送的消息</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <textarea name="body" rows="3" cols="30" wrap="Virtual"></textarea>
                </td>
                </tr>
                <tr>
                <td bgcolor=$miscbacktwo align=center colspan=2>
                <input type="submit" name="Send" value="发送消息"></form>
                </td>
                </tr>
            </table>
        </td></tr>
    </table><SCRIPT>valignend()</SCRIPT>
    </body>
    </html>
    ~;
}
elsif ($action eq "lbcode") {
    $output = qq~<p>
<SCRIPT>valigntop()</SCRIPT>
    <table width=$tablewidth cellpadding=0 cellspacing=0 align=center bgcolor=$tablebordercolor>
    <tr>
        <td>
        <table width=100% cellpadding=5 cellspacing=1>
            <tr>
                <td bgcolor=$miscbacktwo align=center colspan=2>
                    <font color=$titlefontcolor><b>LeoBBS 标签</b>
                    <br>LeoBBS 标签很象 HTML 标签，但比 HTML 标签安全。你可以参照下面手册中的格式来使用它！
                    </font>
                    </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone><ul>
                    <font color=$fontcolormisc>
                    <font color=$fonthighlight>[quote]</font>这个标签是用来做为引用所设置的，如果你有什么内容是引用自别的地方，请加上这个标签！<font color=$fonthighlight>[/quote]</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><hr noshade color=$fonthighlight><blockquote>这个标签是用来做为引用所设置的，如果你有什么内容是引用自别的地方，请加上这个标签！</blockquote><hr noshade color=$fonthighlight></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone><UL>
                    <font color=$fontcolormisc>
                    <font color=$fonthighlight>[code]</font>
                    	<BR>unless ( eq "$authenticateme") {
			<BR>print "错误的管理密码";
			<BR>&unlock;
			<BR>exit;
			<BR>}<BR>
			<font color=$fonthighlight>[/code]</font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc>
			<BLOCKQUOTE>代码：<hr noshade color=$fonthighlight>
			unless ( eq "$authenticateme") { <BR>
			print "错误的管理密码"; <BR>
			&unlock; <BR>
			exit; <BR>
			}<hr noshade color=$fonthighlight></FONT></BLOCKQUOTE>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[html]</font>&lt;font size=5&gt;HTML 和 JS 代码支持&lt;/font&gt;<font color=$fonthighlight>[/html]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><SPAN><IMG src=$imagesurl/images/code.gif align=absBottom> HTML 代码片段如下:<BR><TEXTAREA style="WIDTH: 94%; BACKGROUND-COLOR: #f7f7f7" name=textfield rows=4>&lt;font size=5&gt;HTML 和 JS 代码支持&lt;/font&gt;<\/TEXTAREA><BR><INPUT onclick=runEx() type=button value=运行此代码 name=Button> [Ctrl+A 全部选择   提示:你可先修改部分代码，再按运行]</SPAN><BR></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[url]</font>http://www.LeoBBS.com<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="http://www.LeoBBS.com">http://www.LeoBBS.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[url=http://www.LeoBBS.com]</font>雷傲科技<font color=$fonthighlight>[/url]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="http://www.LeoBBS.com">雷傲科技</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[email=webmaster\@leobbs.com]</font>写信给我<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="mailto:webmaster\@leobbs.com">写信给我</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[email]</font>webmaster\@leobbs.com<font color=$fonthighlight>[/email]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><a href="mailto:webmaster\@leobbs.com">webmaster\@leobbs.com</a></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[b]</font>文字加粗体效果<font color=$fonthighlight>[/b]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><b>文字加粗体效果</b></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[i]</font>文字加倾斜效果<font color=$fonthighlight>[/i]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><i>文字加倾斜效果</i></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[u]</font>文字加下划线效果<font color=$fonthighlight>[/u]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><u>文字加下划线效果</u></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[size=4]</font>改变文字大小<font color=$fonthighlight>[/size]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font size=4>改变文字大小</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[font=impact]</font>改变字体<font color=$fonthighlight>[/font]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font face=impact>改变字体</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[color=red]</font>改变文字颜色<font color=$fonthighlight>[/color]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=red>改变文字颜色</font>
                </td>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[s]</font>文字上加删除线<font color=$fonthighlight>[/s]</font>
                    </font>
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><s>文字上加删除线</s></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sup]</font>上标文字<font color=$fonthighlight>[/sup]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><sup>上标文字</sup></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sub]</font>下标文字<font color=$fonthighlight>[/sub]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><sub>下标文字</sub></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[FLIPH]</font>左右颠倒文字<font color=$fonthighlight>[/FLIPH]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:flipH">左右颠倒文字</table></FLIPH>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[FLIPV]</font>上下颠倒文字<font color=$fonthighlight>[/FLIPV]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:flipV">上下颠倒文字</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[INVERT]</font>底片效果<font color=$fonthighlight>[/INVERT]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:invert"><img src="$imagesurl/images/leobbs8831.gif" border=0></table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[XRAY]</font>曝光效果<font color=$fonthighlight>[/XRAY]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table style="filter:xray"><img src="$imagesurl/images/logo.gif" border=0></table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[shadow=文字宽度,颜色,边界大小]</font>阴影文字<font color=$fonthighlight>[/shadow]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:shadow\(color=#f000ff\, direction=1)">阴影文字</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[GLOW=文字宽度,颜色,边界大小]</font>光晕文字<font color=$fonthighlight>[/GLOW]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:glow\(color=#00f0ff\, strength=1)">光晕文字</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[BLUR=文字宽度,方向,浓度]</font>模糊文字<font color=$fonthighlight>[/BLUR]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table width=50 style="filter:blur\(Add=0, direction=6\, strength=2)">模糊文字</table></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[list]</font>开始列表<br><font color=$fonthighlight>[*]</font>列表项目<br><font color=$fonthighlight>[/list]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><ul>开始列表<br><li>列表项目</ul></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[img]</font>http://bbs.LeoBBS.com/non-cgi/myimages/mainlogo.gif<font color=$fonthighlight>[/img]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><img src="$imagesurl/images/mainlogo.gif" border=0></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[fly]</font>飞行文字特效<font color=$fonthighlight>[/fly]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><marquee width=90% behavior=alternate scrollamount=3>飞行文字特效<\/marquee></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[move]</font>滚动文字特效<font color=$fonthighlight>[/move]</font>
                    </font>      
                </td>
                    <td bgcolor=$miscbackone>
                    <font color=$fontcolormisc><marquee width=90% scrollamount=3>滚动文字特效<\/marquee></font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[swf]</font>http://www.micromedia.com/demo.swf<font color=$fonthighlight>[/swf]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个 FLASH 文件(自动控制大小)</font>
                </td> 
                </tr> 
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[flash=宽度,高度]</font>http://www.micromedia.com/demo.swf<font color=$fonthighlight>[/flash]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个 FLASH 文件(手动设置大小)</font>
                </td> 
                </tr> 
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[sound]</font>http://www.LeoBBS.com/demo.wav<font color=$fonthighlight>[/sound]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个背景声音文件(*.mid,*.wav)</font>
                </td>
                </tr>
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[mms]</font>mms://www.microsoft.com/demo.asf<font color=$fonthighlight>[/mms]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个 WM 格式流数据</font>
                </td> 
                </tr> 
                <tr>
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[rtsp]</font>rtsp://www.real.com/demo.ram<font color=$fonthighlight>[/rtsp]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>插入一个 Real 格式流数据</font>
                </td> 
                </tr> 
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[ra]</font>http://www.LeoBBS.com/demo.ra<font color=$fonthighlight>[/ra]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Real Player播放音频文件(*.mp3,*.ra)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[rm]</font>http://www.LeoBBS.com/demo.rm<font color=$fonthighlight>[/rm]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Real Player播放视频文件(*.rm)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[real=宽度,高度]</font>http://www.LeoBBS.com/demo.rm<font color=$fonthighlight>[/real]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Real Player播放视频文件(*.rm)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wmv]</font>http://www.LeoBBS.com/demo.wmv<font color=$fonthighlight>[/wmv]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Windows Media Player播放视频文件(*.wmv)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wma]</font>http://www.LeoBBS.com/demo.wma<font color=$fonthighlight>[/wma]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Windows Media Player播放音频文件(*.wma)</font>
                </td>
                </tr>
                <tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[wm=宽度,高度]</font>http://www.LeoBBS.com/demo.wmv<font color=$fonthighlight>[/wm]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>在线Windows Media Player播放视频文件(*.wmv)</font>
                </td>
                </tr>
				<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[hide]</font>保密内容<font color=$fonthighlight>[/hide]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><blockquote><font face=$font>隐藏 : <hr noshade size=1><font color=red>本部分内容已经隐藏，必须回复后，才能查看<\/font><hr noshade size=1><\/blockquote><\/font><\/blockquote></font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[post=1000]</font>保密内容<font color=$fonthighlight>[/post]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><blockquote><font face=$font>文章内容 : <hr noshade size=1><font color=red>本内容已被隐藏 , 发言总数须有1000才能查看<\/font><hr noshade size=1><\/font><\/blockquote></font>
                </td>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[jf=1000]</font>保密内容<font color=$fonthighlight>[/jf]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><blockquote><font face=$font>文章内容 : <hr noshade size=1><font color=red>本内容已被隐藏 , 积分达到 1000 才能查看<\/font><hr noshade size=1><\/font><\/blockquote></font>
                </td>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[watermark]</font>加水印内容<font color=$fonthighlight>[/watermark]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><blockquote><font face=$font>文章内容 : <hr noshade size=1><font color=$miscbackone>72!*1</font><font color=red>本内容已被加水印，你用鼠标选中看看。<\/font><font color=$miscbackone>(:9!*1</font><hr noshade size=1><\/font><\/blockquote></font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[equote]</font>特别样式的引用，效果不错的。<font color=$fonthighliermark]</font><\/TR><\/TABLE></font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[fquote]</font>����һ���ر���ʽ�����ã�Ч�������ġ�<font color=$fonthighlight>[/fquote]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><table cellSpacing=0 cellPadding=0 width=100%><tr><td><table style=word-break: break-all cellSpacing=0 cellPadding=0><tr><td><img src=$imagesurl/images/top1_l.gif width=83 height=39></td><td width=100% background=$imagesurl/images/top1_c.gif>��</td><td><img src=$imagesurl/images/top1_r.gif width=7 height=39></td></tr><tr><td colSpan=3><table cellSpacing=0 cellPadding=0 width=100%><tr><td vAlign=top background=$imagesurl/images/center1_l.gif><img src=$imagesurl/images/top1_l2.gif width=11 height=1></td><td vAlign=center width=100% bgColor=#fffff1>����һ���ر���ʽ�����ã�Ч�������ġ�</td><td vAlign=top background=$imagesurl/images/center1_r.gif><img src=$imagesurl/images/top1_r2.gif width=7 height=2></td></tr></table></td></tr><tr><td colSpan=3><table cellSpacing=0 cellPadding=0 width=100%><tr><td vAlign=top><img src=$imagesurl/images/foot1_l1.gif width=12 height=18></td><td width=100% background=$imagesurl/images/foot1_c.gif><img src=$imagesurl/images/foot1_l3.gif width=1 height=18></td><td align=right><img src=$imagesurl/images/foot1_r.gif width=8 height=18></td></tr></table></td></tr></table></td></tr></table>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[curl=http://www.LeoBBS.com/]</font></font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>�������в����������</font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[buyexege]�������ӵ�����ע��[/buyexege]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>�������ӵ�����ע�⣬ֻ������ʱ����ʹ�ã�ע�����ݶ��κ��˶��ǿɼ��ġ�</font>
                </td>
                </tr>
		<tr> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc><font color=$fonthighlight>[iframe]</font>http://www.LeoBBS.com/<font color=$fonthighlight>[/iframe]</font>
                    </font>       
                </td> 
                    <td bgcolor=$miscbackone align=center>
                    <font color=$fontcolormisc>�������в�����ҳ</font>
                </td>
                </tr>

            </table>
        </td></tr>
    </table><SCRIPT>valignend()</SCRIPT>
    </body>
    </html>
    ~;
}

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

    &output("$boardname - ����",\$output,"msg");
exit;
