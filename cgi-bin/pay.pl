#&getoneforum("$inforum");

    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    	&error("发帖&你的积分为 $jifen，而本论坛只有积分大于等于 $postminjf 的才能发言！") if ($postminjf > 0 && $jifen < $postminjf);
    }

    if ($startnewthreads eq "onlysub") {&error("发表&对不起，这里是纯子论坛区，不允许发言！"); }
    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");

    if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("发表&对不起，您没有在此论坛中发表的权利！"); }

    if ($postopen eq "no") { &error("发表主题&对不起，本论坛不允许发表主题！"); }

    if ($payopen eq "no") { &error("发表交易帖&对不起，本论坛不允许发表交易帖！"); }

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	&error("发表交易帖&对不起，你的删贴率超过了<b>$deletepercent</b>%，管理员不允许你发表交易帖！") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") { &whosonline("$inmembername\t$forumname\tnone\t发表交易帖\t"); }
                       else { &whosonline("$inmembername\t$forumname(密)\tnone\t发表新的保密交易帖\t"); }
    }
    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     {  $onlinetime = $onlinetime + $onlinetimeadd; &error("发表交易帖&对不起，本论坛不允许在线时间少于 $onlinepost 秒的用户发表交易帖！你目前已经在线 $onlinetime 秒！"); }

    &mischeader("发表交易帖");

    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>有回复时使用邮件通知您？<br>~;
    }

    if ($startnewthreads eq "no")        { $startthreads = "在此论坛中新的交易帖和帖子回复只能由坛主、版主发表！"; }
    elsif ($startnewthreads eq "follow") { $startthreads = "在此论坛中新的交易帖只能由坛主、版主发表！普通会员只可以跟帖！"; }
    elsif ($startnewthreads eq "all")    { $startthreads = "任何人均可以发表和回复交易帖，未注册用户发帖密码请留空！"; }
    elsif ($startnewthreads eq "cert")   { $startthreads = "在此论坛中新的交易帖只能由坛主、版主、认证的会员发表！"; }
    else { $startthreads = "所有注册会员均可以发表和回复交易帖！"; }

    $startthreads .= " <B>(贴子内必须带附件)</B>" if ($mastpostatt eq "yes");

    if ($emoticons eq "on") {
	$emoticonslink = qq~<li><a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">允许<B>使用</B>表情字符转换</a>~;
	$emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>您是否希望<b>使用</b>表情字符转换在您的文章中？<br>~;
    }

    if ($emoticons eq "on") {
	$output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;
    }
    if ($htmlstate eq "on")     { $htmlstates = "可用"; }     else { $htmlstates = "不可用"; }
    if ($idmbcodestate eq "on") { $idmbcodestates = "可用"; $canlbcode =qq~<input type=checkbox name="uselbcode" value="yes" checked>使用 LeoBBS 标签？<br>~; } else { $idmbcodestates = "不可用"; $canlbcode= "";}
    if ($useemote eq "no")      { $emotestates = "不可用"; }  else { $emotestates = "可用"; }

    $intopictitle =~ s/^＊＃！＆＊//;
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
var revisedTitle;var currentTitle = document.FORM.intopictitle.value;revisedTitle = addTitle+currentTitle;document.FORM.intopictitle.value=revisedTitle;document.FORM.intopictitle.focus();
return;}
</script>
<form action=$thisprog method=post name="FORM" enctype="multipart/form-data">
<input type=hidden name=action value=addnewpay>
<input type=hidden name=forum value=$inforum>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>谁可以发表？</b> $startthreads　关于支付宝的具体说明请访问 <a href=http://www.alipay.com/ target=_blank>http://www.alipay.com/</a></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>主题标题</b></font>　
<select name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
<OPTION selected value="">选择话题</OPTION> <OPTION value=[原创]>[原创]</OPTION><OPTION value=[转帖]>[转帖]</OPTION><OPTION value=[灌水]>[灌水]</OPTION><OPTION value=[讨论]>[讨论]</OPTION><OPTION value=[求助]>[求助]</OPTION><OPTION value=[推荐]>[推荐]</OPTION><OPTION value=[公告]>[公告]</OPTION><OPTION value=[注意]>[注意]</OPTION><OPTION value=[贴图]>[贴图]</OPTION><OPTION value=[建议]>[建议]</OPTION><OPTION value=[下载]>[下载]</OPTION><OPTION value=[分享]>[分享]</OPTION>
</SELECT></td><td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="intopictitle" value="$intopictitle">　不得超过 40 个汉字</td></tr>$nowaterpost
    ~;
        $output .= qq~<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername">   <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password">   <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>当前心情</b><br><li>将放在帖子的前面<BR></font></td><td bgcolor=$miscbackone valign=top>
~;
    open (FILE, "${lbdir}data/lbpost.cgi");
    my @posticondata = <FILE>;
    close (FILE);
    chomp @posticondata;
    my $tempiconnum=1;
    foreach (@posticondata) {
if ($tempiconnum > 12) {
    $tempiconnum = 1;
    $output .= qq~<BR>~;
}
$output .= qq~<input type=radio value="$_" name="posticon"><img src=$imagesurl/posticons/$_ $defaultsmilewidth $defaultsmileheight> ~;
$tempiconnum ++;
}

    if (($arrowupload ne "off")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
    $uploadreqire = "" if ($uploadreqire <= 0);
    $uploadreqire = "<BR>发帖数要大于 <B>$uploadreqire</B> 篇(认证用户不限)" if ($uploadreqire ne "");
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        $output .= qq~<tr><td bgcolor=$miscbackone><b>上传附件或图片</b> (最大容量 <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>目前附件:(如不需要某个附件，只需删除内容中的相应 [UploadFile$imgslt ...] 标签即可)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=删除所有未被发布的附件临时文件 OnClick="return confirm('确定删除所有未被发布的附件临时文件么？');">删除</a>] </font></font><SPAN id=showupfile name=showupfile></SPAN></td></tr>~;
    }

    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>我的支付宝账号</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="alipayid" value="$emailaddress">　如果没有，请填写正确的邮件地址</td></tr>~;
$output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>商品名称</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="warename">　没有名称，买家怎么买呢?</td></tr>~;
$output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>商品展示地址</b></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="wareurl">　给客户更加详细的介绍</td></tr>~;
    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>商品价格</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="wareprice">　请填写正确的价格</td></tr>~;
    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>邮费承担方选择</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone>
<input onclick="document.FORM.postage_mail.disabled=true; document.FORM.postage_express.disabled=true; document.FORM.postage_ems.disabled=true" type="radio" CHECKED value="s" name="transport"> 卖家承担邮费<br>
<input onclick="document.FORM.postage_mail.disabled=false; document.FORM.postage_express.disabled=false; document.FORM.postage_ems.disabled=false" type="radio" value="b" name="transport"> 买家承担邮费<br>
通过物流费用选择注明该交易是由买卖哪方承担运费。<br>
如果是买家承担运费，请选择可以提供的物流方式以及相应费用。<br>
平邮 <input disabled size="3" name="postage_mail"> 元 (不填视作不提供平邮)<br>
快递 <input disabled size="3" name="postage_express"> 元 (不填视作不提供快递)<br>
EMS&nbsp; <input disabled size="3" name="postage_ems"> 元 (不填视作不提供 EMS)<br>
</td></tr>
~;
    $maxpoststr = "(帖子中最多包含 <B>400</B> 个字符)" ;
    
    $output .= qq~</td></tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>商品描述</b> <font color=$fonthighlight>(*)</font>　$maxpoststr<p>在此论坛中：<li>HTML 　标签: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE　标签</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a>: <b>$idmbcodestates</b><li>贴图标签 　: <b>$postpicstates</b><li>Flash 标签 : <b>$postflashstates</b><li>音乐标签 　: <b>$postsoundstates</b><li>文字大小 　: <b>$postfontsizestates</b><li>帖数标签 　: <b>$postjfstates</b><li>积分标签 　: <b>$jfmarkstates</b><li>保密标签 　: <b>$hidejfstates</b>$emoticonslink</font></td><td bgcolor=$miscbackone>$insidejs<TEXTAREA cols=80 name=inpost id=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$inpost</TEXTAREA><br>
  模式:<input type="radio" name="mode" value="help" onClick="thelp(1)">帮助　<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">完全　<input type="radio" name="mode" value="basic"  onClick="thelp(0)">基本　　>> <a href=javascript:HighlightAll('FORM.inpost')>复制到剪贴板</a> | <a href=javascript:checklength(document.FORM);>查看长度</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">转换剪贴板超文本</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<
</td></tr></tr>~;
    
    if ($emoticons eq "on") {
$output .= qq~<tr><td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>点击表情图即可在帖子中加入相应的表情</B></font><br> ~;
if (open (FILE, "${lbdir}data/lbemot.cgi")) {
    @emoticondata = <FILE>;
    close (FILE);
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
} else {
    my $emoticondata = "'" . join ("', '", @emoticondata) . "'";
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
<td bgcolor=$miscbacktwo><font color=$fontcolormisc>$canlbcode
<input type=checkbox name="inshowsignature" value="yes" checked>是否显示您的签名？<br>
$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton
</font><BR></td></tr><tr><td bgcolor=$miscbacktwo colspan=2 align=center>
<input type=Submit value="发 表" name=Submit onClick="return clckcntr();">　　<input type=button value='预 览' name=Button onclick=gopreview()>　　<input type="reset" name="Clear" value="清 除"></td></form></tr></table></tr></td></table>
<SCRIPT>valignend()</SCRIPT>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$inforum"></form>
<script>
function gopreview(){
document.preview.body.value=document.FORM.inpost.value;
var popupWin = window.open('', 'preview_page', 'scrollbars=yes,width=600,height=400');
document.preview.submit()
}
</script>
    ~;
1;
