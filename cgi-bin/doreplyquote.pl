#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

    if ($startnewthreads eq "onlysub") {&error("发表&对不起，这里是纯子论坛区，不允许发言！"); }
    $testentry = $query->cookie("forumsallowed$inforum");
    if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("发表&对不起，您不允许在此论坛发表！"); }
    if ($postopen eq "no") { &error("发表或回复主题&对不起，本论坛不允许发表或回复主题！"); }
    &error("普通错误&客人不能查看贴子内容，请注册或登录后再试") if (($guestregistered eq "off")&&($inmembername eq "客人"));

    open(FILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
    @threads = <FILE>;
    close(FILE);
    $posttoget = $inpostno - 1;

    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $threads[$posttoget]);
    $topictitle =~ s/^＊＃！＆＊//;

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") {
	    &whosonline("$inmembername\t$forumname\tnone\t引用回复<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
	}
	else {
    	    &whosonline("$inmembername\t$forumname(密)\tnone\t引用回复保密帖子\t");
	}
    }

    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     {  $onlinetime = $onlinetime + $onlinetimeadd; &error("回复主题&对不起，本论坛不允许在线时间少于 $onlinepost 秒的用户回复主题！你目前已经在线 $onlinetime 秒！<BR>如果在线时间统计不正确,请重新登陆论坛一次即可解决！"); }

    &getmember($membername,"no");
    $post = "此用户的发言已经被屏蔽！" if ($membercode eq "masked");
    $membercode = $mymembercode;
	
    if  ($post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg){
	$checked=$1;
	if ((lc($inmembername) eq lc($membername))||($mymembercode eq "ad") || ($mymembercode eq 'smo') || ($mymembercode eq "mo") || ($mymembercode eq "amo") || ($inmembmod eq "yes")|| ($myrating >= $1) ){
	    $weiwangoptionbutton=~s/value=$checked/value=$checked selected/isg;
	    $weiwangoptionbutton=~s/value=\"yes\" /value=\"yes\" checked /;
	}
	undef $checked;
	$post="(保密帖子)";
    }
    if  ($post=~/LBSALE\[(.*?)\]LBSALE/sg){
	$post="(保密帖子)";
    }

    $post =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
    $post =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
    $post =~ s/\[hide\](.+?)\[\/hide\]//isg;
    $post =~ s/\[watermark\](.+?)\[\/watermark\]/\n\(水印部分不能引用\)\n/isg;
    $post =~ s/(\&\#35\;|#)Moderation Mode//isg;
    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;
    $post =~ s/ \&nbsp;/  /ig;
    $post =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[加密连结\]/isg if ($usecurl ne "no");
    $post =~ s/\[DISABLELBCODE\]//isg;
    $post =~ s/\[ADMINOPE=(.+?)\]//isg;
    $post  =~ s/\[ALIPAYE\](.*)\[ALIPAYE\]//isg; 
    $post2 =~ s/ \n/\n/isg;
    $post2 =~ s/　\n/\n/isg;
    if ($post =~ /\[POSTISDELETE=(.+?)\]/) {
    	if ($1 ne " ") { $presult = "屏蔽理由：$1"; } else { $presult = ""; }
        $post = "此帖子内容已经被单独屏蔽！$presult";
    }

    $membernametemp=$membername;

    $postdate = $postdate + ($timedifferencevalue + $timezone)*3600;
    $postdate = &dateformat("$postdate");
    $rawpost = $post;

    &mischeader("引用回复帖子");

    if ($emoticons eq "on") {
        $emoticonslink = qq~<li><a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">允许<B>使用</B>表情字符转换</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>您是否希望<b>使用</b>表情字符转换在您的文章中？<br>~;
    }

    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>有回复时使用邮件通知您？<br>~;
    }

    $output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;
    
    $rawpost =~ s/\[这个(.+?)最后由(.+?)编辑\]\n//isg;
    $rawpost =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $rawpost =~ s/LBSALE\[(.*?)\]LBSALE//sg;
    $rawpost =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[quote\](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[equote\](.*)\[\/equote\]//isg;
    $rawpost =~ s/\[fquote\](.*)\[\/fquote\]//isg;
    $rawpost =~ s/\[hide\](.*)\[hide\](.*)\[\/hide](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[hide\](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\](.*)\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/isg;
    $rawpost =~ s/\:.{0,20}\://isg;
    $rawpost =~ s/\<img\s*(.*?)\s*\>//isg;
    $rawpost =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|jpeg|bmp|gif|swf)/($2\.$3)/isg;
    $rawpost =~ s/\&nbsp;/ /ig;
    $rawpost =~ s/( )+$//isg;
    $rawpost =~ s/^( )+//isg;
    $rawpost =~ s/\[.+?\]//g;
    $rawpost =~ s/ \n/\n/isg;
    $rawpost =~ s/　\n/\n/isg;
    $rawpost =~ s/(\n)+/\n/isg;
    $rawpost =~ s/^\n//isg;
    chomp $rawpost;

    my @postall = split(/\n/,$rawpost);
    my $postall = @postall;
    if ($postall > 4) { $rawpost = "$postall[0]\n$postall[1]\n$postall[2]\n$postall[3]\n..."; }
    $rawpost = &lbhz($rawpost,200);

    $inpost = qq~\[quote\]\[b\]下面引用由\[u\]$membernametemp\[\/u\]在 \[i\]$postdate\[\/i\] 发表的内容：\[\/b\]\n$rawpost\n\[\/quote\]\n~;
    if ($htmlstate eq "on")     { $htmlstates = "可用";     } else { $htmlstates = "不可用";     }
    if ($idmbcodestate eq "on") { $idmbcodestates = "可用"; $canlbcode =qq~<input type=checkbox name="uselbcode" value="yes" checked>使用 LeoBBS 标签？<br>~; } else { $idmbcodestates = "不可用"; $canlbcode= "";}
    if ($useemote eq "no") { $emotestates = "不可用"; } else { $emotestates = "可用"; }

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
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic>
<form action=$thisprog method=post name=FORM enctype="multipart/form-data">
<input type=hidden name=action value=addreply>
<input type=hidden name=forum value=$inforum>
<input type=hidden name=topic value=$intopic>
<font color=$titlefontcolor><b>主题标题</b>： $topictitle</td></tr>
~;
    &posttable(2);
    require "dothreadreview.pl";
1;
