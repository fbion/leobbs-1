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
$LBCGI::POST_MAX=1024 * 1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "dopost.pl";

$|++;
$thisprog = "editpay.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$addme=$query->param('addme');

for ('forum','topic','membername','password','action',
     'notify','deletepost','intopictitle','intopicdescription',
     'inpost','inshowemoticons','inshowsignature','checked','movetoid','posticon','inshowchgfont',
     'newtopictitle','inhiddentopic','postweiwang','moneyhidden','moneypost','uselbcode','inwater') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$inforum       = $forum;
$intopic       = $topic;
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9 ]+$/));
&error("打开文件&老大，别乱黑我的程序呀！") if ($inforum !~ /^[0-9 ]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

&error("普通错误&请以正确的方式访问本程序！") if (($postweiwang > $maxweiwang)&&($inhiddentopic eq "yes"));
$moneymax = 99999 if ($moneymax <=0 || $moneymax >=99999);
$moneypost = int($moneypost) if (($moneypost ne "")&&($moneyhidden eq "yes"));
&error("普通错误&请正确的输入帖子的价格，不要少于 1，也不要大于 $moneymax ！") if ((($moneypost > $moneymax)||($moneypost < 1))&&($moneyhidden eq "yes"));
$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inpostno      = 1;
$innotify      = $notify;
$indeletepost  = $deletepost;
$currenttime   = time;
$inposticon    = $posticon;
$inpost        =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost        =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost        =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost        .=($uselbcode eq "yes")?"":"[DISABLELBCODE]" if($action eq "processedit");
$inpost        =~ s/\[USECHGFONTE\]/\[USECHGFONT\&\#069\;\]/sg;
$inpost        .=($inshowchgfont eq "yes")?"[USECHGFONTE]":"" if (($action eq "processedit")&&($canchgfont ne "no"));
$inpost        =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if($moneyhidden eq "yes" && $cansale ne "no"){ 
    if (open(FILE,"${lbdir}data/cansalelist.cgi")) {
        my $CANSALELIST=<FILE>;
        close(FILE);
        $CANSALELIST=~s/^\t//isg;
        $CANSALELIST=~s/\t$//isg;

	$CANSALELIST =~ s/^([01])\t//;
	if ($CANSALELIST ne "") {
	    my $type = $1;
	    $CANSALELIST="\t$CANSALELIST\t";
	    &error("普通错误&您不能够出售帖子！") if (!$type && $CANSALELIST !~/\t$inmembername\t/ || $type && $CANSALELIST =~/\t$inmembername\t/);
	}
    }
}

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
$maxupload = 300 if ($maxupload eq "");

if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }
if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }
if (($movetoid) && ($movetoid !~ /^[0-9]+$/)) { &error("普通错误&请不要修改生成的 URL！"); }

if ($useemote eq "yes") {
    open (FILE, "${lbdir}data/emote.cgi");
    $emote = <FILE>;
    close (FILE);
}
else { undef $emote; }

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
     }
}
require "postjs.cgi";

$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100)&&($maxpoststr ne ""));

print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&moderator("$inforum");
&error("进入论坛&你的论坛组没有权限进入论坛！") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &error('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&error("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
	&error("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

if ($action eq "edit") { &editform;}
    elsif ($action eq "processedit")  { &processedit;  }
    else { &error("普通错误&请以正确的方式访问本程序."); }
    
&output($boardname,\$output);
exit;

sub editform {
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    @threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");

    $posttoget = $inpostno;
    $posttoget--;
    
    ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon, $water) = split(/\t/, $threads[$posttoget]);
    $topictitle =~ s/^＊＃！＆＊//;
    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;

    &error("发表&对不起，不允许编辑投票贴子！") if (($posticon =~ m/<BR>/i)&&($posttoget eq 0));

    &error("发表&对不起，这个不是交易帖！") unless ($post=~m/\[ALIPAYE\]/);

    if ($noedittime ne '') {
	if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
	    &error("编辑帖子&超过 $noedittime 小时不允许再编辑帖子！") if(($currenttime - $postdate) > ($noedittime * 3600));
	}
    }

    $inmembmod = "no" if (($membercode eq "amo")&&($allowamoedit ne "yes"));
    if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")&&((lc($inmembername) ne lc($postermembername))||($usereditpost eq "no"))) {&error("编辑帖子&您不是原作者、论坛管理员，或者密码错誤，或者此区不允许编辑帖子！");} 

    $testentry  = $query->cookie("forumsallowed$inforum");
    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    else { $allowed  = "no"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("发表&对不起，您不允许在此论坛发表！"); }
    
    $rawpost = $post;
    
    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>有回复时使用邮件通知您？<br>~;
    }
    if ($emoticons eq "on") {
        $emoticonslink   = qq~<a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">允许<B>使用</B>表情字符转换</a>~;
        $emoticonsbutton = qq~<input type=checkbox name="inshowemoticons" value="yes" checked>您是否希望<b>使用</b>表情字符转换在您的文章中？<br>~;
    }

    if ($htmlstate eq "on")         { $htmlstates = "可用";         } else { $htmlstates = "不可用";       }
    if ($useemote eq "no") { $emotestates = "不可用"; } else { $emotestates = "可用"; }
    if ($arrawpostflash eq "on")    { $postflashstates = "允许";    } else { $postflashstates = "禁止";    }
    if ($arrawpostpic eq "on")      { $postpicstates = "允许";      } else { $postpicstates = "禁止";      }
    if ($arrawpostfontsize eq "on") { $postfontsizestates = "允许"; } else { $postfontsizestates = "禁止"; }
    if ($arrawpostsound eq "on")    { $postsoundstates = "允许";    } else { $postsoundstates = "禁止";    }
    if ($postjf eq "yes")           { $postjfstates = "允许";       } else { $postjfstates = "禁止";       }
    if ($jfmark eq "yes")    { $jfmarkstates = "允许";}    else { $jfmarkstates = "禁止";}
    if ($hidejf eq "yes")           { $hidejfstates = "允许";       } else { $hidejfstates = "禁止";       }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
      &whosonline("$inmembername\t$forumname\tnone\t编辑<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t") if ($privateforum ne "yes");
      &whosonline("$inmembername\t$forumname(密)\tnone\t编辑保密贴子\t") if ($privateforum eq "yes");
    }

if (($nowater eq "on")&&($inpostno eq "1")) { 
    $gsnum = 0 if ($gsnum<=0);
    $nowaterpost =qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>灌水限制</b></font></td><td bgcolor=$miscbackone><input type="radio" name="inwater" value=no> 不许灌水　 <input name="inwater" type="radio" value=yes> 允许灌水　    [如果选择“不许灌水”，则回复不得少于 <B>$gsnum</B> 字节]</td></tr>~;
    $nowaterpost =~ s/value=$water/value=$water checked/i if ($water ne "");
}

    $rawpost =~ s/\[这个(.+?)最后由(.+?)编辑\]\n//isg;
    if ($wwjf ne "no") {
	if ($rawpost=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
	    $weiwangchecked=" checked";
	    $weiwangchoice=$1;
        } else {
	    undef $weiwangchecked;
	    undef $weiwangchoice;
        }
        for (my $i=0;$i<$maxweiwang;$i++) {
	    $weiwangoption.=qq~<option value=$i>$i</option>~;
        }
        $weiwangoptionbutton=qq~<input type=checkbox name="inhiddentopic" value="yes" $weiwangchecked>加密此帖，只对部分用户可见，用户威望至少需要  <select name=postweiwang>$weiwangoption</select><br>~;
        $weiwangoptionbutton =~ s/option value=$weiwangchoice/option value=$weiwangchoice selected/i if ($weiwangchoice ne "");
    } else {
        undef $weiwangoptionbutton;
    }

    if (($rawpost =~ /\[POSTISDELETE=(.+?)\]/)&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
        &error("编辑帖子&不允许编辑已经被单独屏蔽的帖子！");
    }

    $rawpost=~s/LBSALE\[(.*?)\]LBSALE//sg;
    $rawpost=~s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $uselbcodecheck=($rawpost =~/\[DISABLELBCODE\]/)?"":" checked";
    $rawpost =~ s/\[DISABLELBCODE\]//isg;
    $usecanchgfont=($rawpost =~/\[USECHGFONTE\]/)?" checked":"";
    $rawpost =~ s/\[USECHGFONTE\]//isg;
    $rawpost =~ s/\[POSTISDELETE=(.+?)\]//isg;
    $rawpost =~ s/\[ADMINOPE=(.+?)\]//isg;

    &mischeader("编辑交易帖");

    $helpurl = &helpfiles("阅读标记");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></a>~;

if ($canchgfont ne "no") {
    $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes"$usecanchgfont>使用字体转换？<br>~;
} else {
    undef $fontpost;
}
    if ($idmbcodestate eq "on")     { $idmbcodestates = "可用"; $canlbcode = qq~<input type=checkbox name="uselbcode" value="yes"$uselbcodecheck>使用 LeoBBS 标签？<br>~; } else { $idmbcodestates = "不可用"; $canlbcode=""; }

    if ($inpostno eq "1") {
    	$topictitle = $newtopictitle if ($newtopictitle ne "");
        $topictitle =~s/ \(无内容\)$//;
        $topictitlehtml = qq~<td bgcolor=$miscbackone><font color=$fontcolormisc><b>贴子主题</b></font></td><td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="newtopictitle" value="$topictitle">　不得超过 40 个汉字</td>~;
        $topictitlehtml1="&nbsp;";
    }
    else {
        undef $topictitlehtml;
        $topictitlehtml1 = "<b>* 贴子主题</b>： $topictitle";
    }
    $output .= qq~<script>
function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}
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
<input type=hidden name="postno" value="$inpostno">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic"><SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td>
<table cellpadding=4 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor>$topictitlehtml1</td></tr>
$topictitlehtml$nowaterpost
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
<tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>当前心情</b><BR><li>将放在贴子的前面<BR></font></td>
<td bgcolor=$miscbackone valign=top>
~;
    open (FILE, "${lbdir}data/lbpost.cgi");
    my @posticondata = <FILE>;
    close (FILE);
    chomp @posticondata;
    my $tempiconnum=1;
    foreach (@posticondata) {
        $_ =~ s/[\a\f\n\e\0\r\t]//isg;
	if ($tempiconnum > 12) {
	    $tempiconnum = 1;
	    $tempoutput .= qq~<BR>~;
	}
	if ($_ eq $posticon) { $tempselect = " checked"; } else { $tempselect = ""; }
	$tempoutput .= qq~<input type=radio value="$_" name="posticon"$tempselect><img src=$imagesurl/posticons/$_ $defaultsmilewidth $defaultsmileheight>&nbsp;~;
	$tempiconnum ++;
    }
  
    $output .= qq~$tempoutput</td></tr>~;

#######旧方式的附件，为了兼容，保留############################
    my $p1=$inpostno-1;
    $dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
    opendir (DIR, "$dirtoopen2");
    @files = readdir(DIR);
    closedir (DIR);
    @files = grep(/^$inforum\_$intopic/,@files);
    if ($p1>0) { @files = grep(/^$inforum\_$intopic\_$p1\./,@files); } else { @files = grep(/^$inforum\_$intopic\./,@files); }
    if ( $#files >= 0 ) { $delimg="<BR><input type=checkbox name='delimg' value='no'>删除所有的原图像或附件</input>"; }
########################################################
if ( $rawpost =~ m/\[UploadFile.{0,6}=([^\\\]]+?)\]/is ) {$delimg="<BR><input type=checkbox name='delimg' value='no'>删除所有的原图像或附件</input>" if ($delimg eq "");}

    if (((($inpostno eq "1")&&($arrowupload ne "off"))||(($inpostno ne "1")&&($allowattachment ne "no"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"))) {
        $uploadreqire= "" if ($uploadreqire <= 0);
        $uploadreqire = "<BR>发帖数要大于 <B>$uploadreqire</B> 篇(认证用户不限)" if ($uploadreqire ne "");
#        $output .= qq~<tr><td bgcolor=$miscbacktwo><b>上传附件或图片</b>(最大 $maxupload KB)$uploadreqire</td><td bgcolor=$miscbacktwo> <input type="file" size=30 name="addme">　　$addtypedisp</td></tr>~;
        ###路杨add start
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        ###路杨add end
        $output .= qq~<tr><td bgcolor=$miscbackone><b>上传附件或图片</b> (最大容量 <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>目前附件:(如不需要某个附件，只需删除内容中的相应 [UploadFile$imgslt ...] 标签即可)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=删除所有未被发布的附件临时文件 OnClick="return confirm('确定删除所有未被发布的附件临时文件么？');">删除</a>] </font></font>$delimg<SPAN id=showupfile name=showupfile></SPAN></td></tr>~;

    }

($no,$alipayid,$warename,$oldpost,$wareprice,$wareurl,$postage_mail,$postage_express,$postage_ems) = split(/\[ALIPAYE\]/,$rawpost);

if ($postage_mail ne "" || $postage_express ne "" || $postage_ems ne "") {
    $pviewed = ""; $tcheck1 = ""; $tcheck2 = "CHECKED";
} else {
    $pviewed = "disabled"; $tcheck1 = "CHECKED"; $tcheck2 = "";
}

    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>我的支付宝账号</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="alipayid" value="$alipayid">　如果没有，请填写正确的邮件地址</td></tr>~;
$output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>商品名称</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="warename" value="$warename">　没有名称，买家怎么买呢?</td></tr>~;
$output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>商品展示地址</b></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="wareurl" value="$wareurl">　给客户更加详细的介绍</td></tr>~;
    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>商品价格</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone><input type=text size=28 maxlength=80 name="wareprice" value="$wareprice">　请填写正确的价格</td></tr>~;
    $output.=qq~</tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>邮费承担方选择</b> <font color=$fonthighlight>(*)</font></font></td><td bgcolor=$miscbackone>
<input onclick="document.FORM.postage_mail.disabled=true; document.FORM.postage_express.disabled=true; document.FORM.postage_ems.disabled=true" type="radio" $tcheck1 value="s" name="transport"> 卖家承担邮费<br>
<input onclick="document.FORM.postage_mail.disabled=false; document.FORM.postage_express.disabled=false; document.FORM.postage_ems.disabled=false" type="radio" $tcheck2 value="b" name="transport"> 买家承担邮费<br>
通过物流费用选择注明该交易是由买卖哪方承担运费。<br>
如果是买家承担运费，请选择可以提供的物流方式以及相应费用。<br>
平邮 <input $pviewed size="3" name="postage_mail" value="$postage_mail"> 元 (不填视作不提供平邮)<br>
快递 <input $pviewed size="3" name="postage_express" value="$postage_express"> 元 (不填视作不提供快递)<br>
EMS&nbsp; <input $pviewed size="3" name="postage_ems" value="$postage_ems"> 元 (不填视作不提供 EMS)<br>
</td></tr>
~;
    $maxpoststr = "(帖子中最多包含 <B>400</B> 个字符)" ;

    $output .= qq~<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>商品描述</b> <font color=$fonthighlight>(*)</font>　$maxpoststr<p>
在此论坛中：<li>HTML 标签　: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE　标签</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a>: <b>$idmbcodestates</b><li>贴图标签　 : <b>$postpicstates</b><li>Flash 标签 : <b>$postflashstates</b><li>音乐标签　 : <b>$postsoundstates</b><li>文字大小　 : <b>$postfontsizestates</b><li>帖数标签 　: <b>$postjfstates</b><li>积分标签 　: <b>$jfmarkstates</b><li>保密标签 　: <b>$hidejfstates</b><li>$emoticonslink</font></td>
<td bgcolor=$miscbackone>$insidejs
<TEXTAREA cols=80 name=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$oldpost</TEXTAREA><br>
&nbsp; 模式:<input type="radio" name="mode" value="help" onClick="thelp(1)">帮助　<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">完全　<input type="radio" name="mode" value="basic"  onClick="thelp(0)">基本　　>> <a href=javascript:HighlightAll('FORM.inpost')>复制到剪贴板</a> | <a href=javascript:checklength(document.FORM);>查看长度</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">转换剪贴板超文本</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<</td></tr>
<tr><td bgcolor=$miscbackone valign=top colspan=2>
~;
    if ($emoticons eq "on"){
	$output.=qq~<font color=$fontcolormisc><b>点击表情图即可在贴子中加入相应的表情</B></font><br>&nbsp;~;
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
    }
    if (($inpostno ne 1)&&(($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||(($arrowuserdel eq "on")&&(lc($inmembername) eq lc($postermembername))))) {
        $managetable = qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>管理员选项</b></td><td bgcolor=$miscbackone>&nbsp;<a href="delpost.cgi?action=processedit&postno=$inpostno&forum=$inforum&topic=$intopic&deletepost=yes" OnClick="return confirm('真的要删除此回复么？');">删除此回复(谨慎使用，不可恢复)</a></td></tr>~;
    }
    $output .= qq~</td></tr>
<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>选项</b><p>$helpurl
</font></td>
<td bgcolor=$miscbacktwo><font color=$fontcolormisc>$canlbcode
<input type=checkbox name="inshowsignature" value="yes" checked>是否显示您的签名？<br>$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton
</font></td></tr>$managetable
<tr><td bgcolor=$miscbackone colspan=2 align=center>
<input type=Submit value="发 表" name=Submit onClick="return clckcntr();">　　<input type=button value='预 览' name=Button onclick=gopreview()>　　<input type="reset" name="Clear" value="清 除"></td></form></tr></table></tr></td></table><SCRIPT>valignend()</SCRIPT>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$inforum"><input type=hidden name=topic value="$intopic"></form>
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
    $inpostno1=$inpostno;
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    if (-e $filetoopen) {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen") or &error("编辑&这个主题不存在！");
        flock(FILE, 1) if ($OS_USED eq "Unix");
	sysread(FILE, my $allthreads,(stat(FILE))[7]);
        close(FILE);
	$allthreads =~ s/\r//isg;
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        @allthreads = split(/\n/, $allthreads);
    }
    else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("编辑&这个主题不存在！"); }

    if (($inhiddentopic eq "yes") && ($moneyhidden eq "yes")) { &error("发表主题&请不要在一个贴子内同时使用威望和金钱加密！"); }
    if ((($inhiddentopic eq "yes")||($moneyhidden eq "yes")) && ($userregistered eq "no")) { &error("发表主题&未注册用户无权进行威望和金钱加密！"); }

    $delimg=$query->param('delimg');
    $posttoget = $inpostno;
    $posttoget--;
    $postcountcheck = 0;

    ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $allthreads[$posttoget]);

    $addpost = "";
    while ($post =~ /\[ADMINOPE=(.+?)\]/s) {
	$addpost .= "[ADMINOPE=$1]";
	$post =~ s/\[ADMINOPE=(.+?)\]//s;
    }
    
    if (($post =~ /\[POSTISDELETE=(.+?)\]/)&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
        &error("编辑帖子&不允许编辑已经被单独屏蔽的帖子！");
    }

    if ($noedittime ne '') {
	if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
	    &error("编辑帖子&超过 $noedittime 小时不允许再编辑帖子！") if(($currenttime - $postdate) > ($noedittime * 3600));
	}
    }

    while ($post =~ /\[UploadFile.{0,6}=(.+?)\]/) {
    	my $filenametemp = $1;
    	$filenametemp =~ s/\.\.//isg;
    	$filenametemp =~ s/\/\\//isg;
    	$addmetotle = "$addmetotle$filenametemp\n";
    	$post =~ s/\[UploadFile.{0,6}=(.+?)\]//;
    }
    @addmetotle = split(/\n/,$addmetotle);

$post =~ s/\[这个(.+?)最后(.+?)编辑\]//isg;
($edittimes, $temp) = split(/ 次/, $2);
($temp, $edittimes) = split(/第 /, $edittimes);
$edittimes = 0 unless ($edittimes);

    $testentry = $query->cookie("forumsallowed$inforum");
    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    else { $allowed  = "no"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("编辑主题&对不起，您不允许在此论坛发表！"); }

    &error("编辑帖子&对不起，本论坛不允许发表超过 <B>$maxpoststr</B> 个字符的文章！") if ((length($inpost) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo')&&($membercode ne 'amo') && ($membercode ne "mo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("编辑主题&对不起，不允许编辑投票贴子！") if (($posticon =~ m/<BR>/i)&&($posttoget eq 0));
    &error("编辑帖子&对不起，这个不是交易帖！") unless ($post=~m/\[ALIPAYE\]/);
    &error("编辑帖子&对不起，本论坛不允许发表少于 <B>$minpoststr</B> 个字符的文章！") if ((length($inpost) < $minpoststr)&&($minpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    $inmembmod = "no" if (($membercode eq "amo")&&($allowamoedit ne "yes"));
    if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")&&((lc($inmembername) ne lc($postermembername))||($usereditpost eq "no"))) {&error("编辑帖子&您不是原作者、论坛管理员，或者密码错誤，或者此区不允许编辑帖子！");} 
    if (($membercode eq "banned")||($membercode eq "masked"))      { &error("编辑帖子&您被禁止发言或者发言已经被屏蔽，请联系管理员以便解决！"); }

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if ((lc($inmembername) eq lc($postermembername)) && ($inpassword eq $password) && ($usereditpost ne "no")) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit eq "no"; }

    if ($cleartoedit eq "yes") {
        $editpostdate = $currenttime;
        $editpostdate = $editpostdate + ($timezone + $timedifferencevalue)*3600;
        $editpostdate = &dateformat("$editpostdate");
        $inpost =~ s/[\a\f\n\e\0\r\t]//g;
        $inpost =~ s/  / /g;
        $inpost =~ s/\n\n/\<p\>/g;
        $inpost =~ s/\n/\<br\>/g;
        $inpost =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;

        if ($emote && $inpost =~ m/\/\/\//) {
	    study ($inpost);
 	    my @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
	        chomp $_;
		($toemote, $beemote) = split(/=/,$_);
		$beemote =~ s/对象/〖$inmembername〗/isg;
		$inpost =~ s/$toemote/$beemote/isg;
		last unless ($inpost =~ m/\/\/\//);
	    }
	}

	$newtopictitle =~ s/\(无内容\)$//;
	my $temp = &dofilter("$newtopictitle\t$inpost");
	($newtopictitle,$inpost) = split(/\t/,$temp);
	
        if ($inpostno eq 1){ 
	$newtopictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
	$newtopictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
	$newtopictitle =~ s/(o|O)R/$1&#82;/sg;
	$newtopictitle =~ s/(o|O)r/$1&#114;/sg;
#	$newtopictitle =~ s/\\/&#92;/isg;

	    $newtopictitle =~ s/()+//isg;
	    my $tempintopictitle = $newtopictitle;
	    $tempintopictitle =~ s/ //g;
	    $tempintopictitle =~ s/\&nbsp\;//g;
	    $tempintopictitle =~ s/　//g;
	    $tempintopictitle =~ s/^＊＃！＆＊//;
	    if ($tempintopictitle eq "") { &error("编辑主题&主题标题有问题！"); }
	    undef $tempintopictitle; 
        }   
        
        if (($newtopictitle eq "")&&($inpostno eq 1)) { &error("编辑主题&对不起，贴子主题不能为空！"); }
        if ((length($newtopictitle) > 110)&&($inpostno eq 1))  { &error("编辑主题&对不起，主题标题过长！"); }
        $newtopictitle  = "＊＃！＆＊$newtopictitle";

	if (($nowater eq "on")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo')&&($membercode ne 'amo')&&($membercode ne 'mo')&&($inmembmod ne "yes")) {
          ($trash, $trash, $trash, $trash, $trash, $trash, $post, $trash,my $water) = split(/\t/,$allthreads[0]);
	  if ($water eq "no") {
	    my $inposttemp = $inpost;
	    $inposttemp =~ s/\[这个(.+?)最后由(.+?)编辑\]\<BR\>\<BR\>//isg;
	    $inposttemp =~ s/\[这个(.+?)最后由(.+?)编辑\]\<BR\>//isg;
	    $inposttemp =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;
	    $inposttemp =~ s/\[quote\]\[b\]下面引用由\[u\].+?\[\/u\]在 \[i\].+?\[\/i\] 发表的内容：\[\/b\].+?\[\/quote\]\<br\>//isg;
	    $inposttemp =~ s/\[quote\]\[b\]下面引用由\[u\].+?\[\/u\]在 \[i\].+?\[\/i\] 发表的内容：\[\/b\].+?\[\/quote\]//isg;
	    if ((length($inposttemp) < $gsnum)&&($gsnum > 0)) {
	        &error("发表回复&请不要灌水，本主题禁止 $gsnum 字节以下的灌水！");
                unlink ("${imagesdir}$usrdir/$inforum/$inforum\_$intopic\_$replynumber.$up_ext") if ($addme);
	    }
	  }
	}

        if ($inpostno eq 1) {
	    $newtopictitle = "$newtopictitle (无内容)" if (($inpost eq "")&&($addme eq ""));
	    if ($topictitle eq $newtopictitle) {
		$topictitlecomp = 1;
	    }
	    else {
	        $topictitle = $newtopictitle;
		$topictitlecomp = 0;
	    }
        }
	$edittimes++;
	$noaddedittime = 60 if ($noaddedittime < 0);
	$inpost = qq~[这个贴子最后由$inmembername在 $editpostdate 第 $edittimes 次编辑]<br><br>$inpost~ if (($currenttime - $postdate) > $noaddedittime || $postermembername ne $inmembername);

        if ($moneyhidden eq "yes") { $inposttemp = "(保密)"; $inpost="LBSALE[$moneypost]LBSALE".$inpost;}

	if ($inhiddentopic eq "yes") { $inposttemp = "(保密)"; $inpost="LBHIDDEN[$postweiwang]LBHIDDEN".$inpost; }

	$inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

	if ($inposttemp ne "(保密)") {
	    $inposttemp = $inpost;
	    $inposttemp = &temppost($inposttemp);
	    chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp,50);
        }

    $p1=$inpostno-1;

########删除旧方式的附件，兼容的话保留####
    $dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
    opendir (DIR, "$dirtoopen2");
    @files = readdir(DIR);
    closedir (DIR);
    @files = grep(/^$inforum\_$intopic/,@files);

    if ($p1>0) { @files = grep(/^$inforum\_$intopic\_$p1\./,@files);} else { @files = grep(/^$inforum\_$intopic\./,@files);}

    foreach (@files) {
        if (($addme ne "")||($delimg ne "")) {
            unlink ("$imagesdir/$usrdir/$inforum/$_");
        }
   }

#######删除全部原来的附件 START###(BY 路杨)
     if ($delimg ne "") {$showerr = &delupfiles(\$inpost,$inforum,$intopic);}; #新方式

#######删除全部原来的附件 END

    $topic =$intopic%100;
    my $topath = "${imagesdir}$usrdir/$inforum/$topic"; #目的目录
  foreach (@addmetotle) {
  	if ($inpost !~ /$_/i) { unlink("$topath\/$_"); }
  }


    my $filesize=0;

   $addme= &upfileonpost(\$inpost,$inforum,$intopic);#处理上传，返回数值给BT区做判断

    for ('alipayid','warename','wareurl','wareprice','transport','postage_mail','postage_express','postage_ems') {
    next unless defined $_;
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
if(length($inpost)>400){
&error("错误&商品描述不能超出400个字符");
}
&error("错误&明显不符合规定的价格")if($wareprice!~/^[0-9\.]+$/i);
&error("错误&明显不符合规定的价格")if($postage_mail!~/^[0-9\.]+$/i && $postage_mail ne '');
&error("错误&明显不符合规定的价格")if($postage_express!~/^[0-9\.]+$/i && $postage_express ne '');
&error("错误&明显不符合规定的价格")if($postage_ems!~/^[0-9\.]+$/i && $postage_ems ne '');

$transport = 's' if ($postage_mail eq "" && $postage_express eq "" && $postage_ems eq "");

if ($transport eq 's') {
    $postage_mail = "";
    $postage_express = "";
    $postage_ems = "";
}

    $alipayid  = lc($alipayid);
    $alipayid =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    if($alipayid !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) { &error("错误&支付宝账号错误！"); }

    $wareurl =~ s/[\a\f\n\e\0\r\t]//isg;
    $wareurl =~ s/^http:\/\///isg;

    $k="\[ALIPAYE\]$alipayid\[ALIPAYE\]$warename\[ALIPAYE\]$inpost\[ALIPAYE\]$wareprice\[ALIPAYE\]$wareurl\[ALIPAYE\]$postage_mail\[ALIPAYE\]$postage_express\[ALIPAYE\]$postage_ems\[ALIPAYE\]";
    $inpost = $k;

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            foreach $postline (@allthreads) {
                chomp $postline;
                if ($postcountcheck eq 0) { $water = "$inwater\t"; } else { $water=""; }
                if ($postcountcheck eq $posttoget) {
                    print FILE "$postermembername\t$topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$postdate\t$addpost$inpost\t$inposticon\t$water\n";
                }
                else {
                    (my $postermembertemp, my $topictitletemp, my @endall) = split(/\t/,$postline);
                    print FILE "$postermembertemp\t$topictitle\t";
                    foreach (@endall) {
                        print FILE "$_\t";
                    }
                    print FILE "\n";
                }
                $postcountcheck++;
            }
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");

        $postcountcheck--;
        $topictitle =~ s/^＊＃！＆＊//;
       	if (($inpostno eq 1)||($postcountcheck eq $posttoget)) {
            $filetoopen = "$lbdir" . "forum$inforum/$intopic.pl";
	    open(FILE, "$filetoopen");
	    my $topicall = <FILE>;
            close(FILE);
            chomp $topicall;
	    (my $topicidtemp, my $topictitletemp, my $topicdescription,my $threadstate,my $threadposts ,my $threadviews,my $startedby,my $startedpostdate,my $lastposter,my $lastpostdate,my $posticon,my $posttemp, my $addmetype) = split(/\t/,$topicall);
	    $posttemp = $inposttemp if ($postcountcheck eq $posttoget);
	    $posticon = $inposticon if ($inpostno eq 1);
            if ($inpost =~ /\[UploadFile.{0,6}=(.+?)\]/i) {
	         ($no,$addmetype1) = split(/.*\./,$1);
	    } else { $addmetype1 = ""; }
	    if ($inpostno eq 1) { $addmetype = $addmetype1; }
            if (open(FILE, ">$filetoopen")) {
                print FILE "$intopic\t＊＃！＆＊$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype\t\n";
                close(FILE);
            }

	    $filetoopen = "$lbdir" . "boarddata/listall$inforum.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE, "$filetoopen");
            flock(FILE, 2) if ($OS_USED eq "Unix");
	    sysread(FILE, my $allthreads,(stat(FILE))[7]);
            close(FILE);
	    $allthreads =~ s/\r//isg;
	    $allthreads =~ s/(.*)(^|\n)$intopic\t(.*?)\t(.*?)\t(.*?)\t\n(.*)/$1$2$intopic\t$topictitle\t$4\t$5\t\n$6/isg;

            if (open(FILE, ">$filetoopen")) {
                flock(FILE, 2) if ($OS_USED eq "Unix");
                print FILE "$allthreads";
                close(FILE);
            }
            &winunlock($filetoopen) if ($OS_USED eq "Nt");
	}
       	if (($inpostno eq 1)&&($topictitlecomp eq 0)) {

	    my $newthreadnumber;
	    $filetoopen = "$lbdir" . "boarddata/lastnum$inforum.cgi";
	    if (open(FILE, "$filetoopen")) {
		$newthreadnumber = <FILE>;
                close(FILE);
                chomp $newthreadnumber;
	    }
	    if ($newthreadnumber = $intopic) {
		$filetoopen = "${lbdir}boarddata/foruminfo$inforum.cgi";
		my $filetoopens = &lockfilename($filetoopen);
		if (!(-e "$filetoopens.lck")) {
	            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		    open(FILE, "+<$filetoopen");
		    my ($lastforumpostdate, $tpost, $treply, $todayforumpost, $lastposter) = split(/\t/,<FILE>);
		    my ($lastposttime,$threadnumber,$topictitle1)=split(/\%\%\%/,$lastforumpostdate);
		    seek(FILE,0,0);
		    $lastforumpostdate = "$lastposttime\%\%\%$threadnumber\%\%\%$topictitle";
		    print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
		    close(FILE);
		    &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		}
	    }

	    $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
    	    &winlock($filetomakeopen) if ($OS_USED eq "Nt");
	    open(FILE, "$filetomakeopen");
    	    flock (FILE, 1) if ($OS_USED eq "Unix");
	    @recentposts=<FILE>;
	    close(FILE);

            if (open (FILE, ">$filetomakeopen")) {
    	        flock (FILE, 2) if ($OS_USED eq "Unix");
                foreach (@recentposts) {
	            chomp $_;
	            ($tempno1, $tempno2, $no, @endall) = split (/\t/,$_);
    	            next if (($tempno1 !~ /^[0-9]+$/)||($tempno2 !~ /^[0-9]+$/));

                    if (($tempno1 eq $inforum)&&($tempno2 eq $intopic)) {
                        print FILE "$inforum\t$intopic\t$topictitle\t";
                        foreach (@endall) { print FILE "$_\t"; }
                        print FILE "\n"
                    }
                    else {
                        print FILE "$_\n"
                    }
                }
	        close(FILE);
	    }
    	    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
	}

        &mischeader("编辑贴子");

for(my $iii=0;$iii<=4;$iii++) {
    my $jjj = $iii * $maxthreads;
    unlink ("${lbdir}cache/plcache$inforum\_$jjj.pl");
}

$gopage = int(($posttoget-1)/$maxtopics)*$maxtopics;
$posttoget ++;
        if ($refreshurl == 1) { $relocurl = "topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$posttoget"; }
                         else { $relocurl = "forums.cgi?forum=$inforum"; }
        $output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>编辑成功</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
具体情况：<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$posttoget">返回主题</a><li><a href="forums.cgi?forum=$inforum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a></ul>
</tr></td></table></td></tr></table>
<meta http-equiv="refresh" content="3; url=$relocurl">
~;
    }
    else { &error("编辑贴子&您不是原作者，或者用户名、密码错误！"); }
}