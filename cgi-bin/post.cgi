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
$LBCGI::POST_MAX=1024 * 10000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "dopost.pl";

$|++;
$thisprog = "post.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
#    $cookiepath =~ tr/A-Z/a-z/;
}

#$addme  = $query->param('addme');
$listmy = $query->param('listmy');

for ('forum','topic','membername','password','action','postno','inshowsignature',
     'notify','inshowemoticons','intopictitle','inshowchgfont',
     'inpost','posticon','inhiddentopic','postweiwang','moneyhidden','moneypost','uselbcode','inwater','floor') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}
$intopictitle  =~ s/\\0//isg;
#$intopictitle  =~ s/\\/&#92;/isg;
$intopictitle  = "＊＃！＆＊$intopictitle";

$inforum       = $forum;
$intopic       = $topic;
&error("打开文件&老大，别乱黑我的程序呀！") if (($intopic) && ($intopic !~ /^[0-9]+$/));
&error("打开文件&老大，别乱黑我的程序呀！！") if ($inforum !~ /^[0-9]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
$maxupload = 300 if ($maxupload eq "");

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

$inpostno      = $postno;
$innotify      = $notify;
$currenttime   = time;
$postipaddress = &myip();
$inpost        =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost        =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost        =~ s/USECHGFONTE/USECHGFONT\&\#069\;/sg;
$inpost        =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost        =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;

$inpost        .=($uselbcode eq "yes")?"":"[DISABLELBCODE]" if ($action eq "addnew" || $action eq "addreply"|| $action eq "addnewpay");
$inpost        .=($inshowchgfont eq "yes")?"[USECHGFONTE]":"" if (($action eq "addnew" || $action eq "addreply"|| $action eq "addnewpay")&&($canchgfont ne "no"));

if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword)   { $inpassword   = $query->cookie("apasswordcookie"); }
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

$inposticon    = $posticon;

&ipbanned; #封杀一些 ip

if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("普通错误&老大，别乱黑我的程序呀！！！"); }

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}

if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }

if (!(-e "${lbdir}boarddata/listno$inforum.cgi")) { &error ("发表新主题&对不起，这个论坛不存在！如果确定分论坛号码没错，那么请进入管理区修复论坛一次！"); }

if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
    $userregistered = "no";
} else {
    
    &getmember("$inmembername");
    &error("普通错误&此用户根本不存在！") if ($inpassword ne "" && $userregistered eq "no");
     if ($inpassword ne $password && $userregistered ne "no") {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
     }
}

&doonoff;  #论坛开放与否

$mymembercode=$membercode;
$myrating=$rating;
$myrating="-6" if !($myrating);
$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100)&&($maxpoststr ne ""));

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-charset=>utf8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&moderator("$inforum");
$myinmembmod = $inmembmod;

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

require "postjs.cgi";

if ($wwjf ne "no") {
    for (my $i=0;$i<$maxweiwang;$i++) {
	$weiwangoption.=qq~<option value=$i>$i</option>~;
    }
    $weiwangoptionbutton=qq~<input type=checkbox name="inhiddentopic" value="yes">加密此帖，只对部分用户可见，用户威望至少需要  <select name=postweiwang>$weiwangoption</select><br>~;
} else {
    undef $weiwangoptionbutton;
}

if ($cansale ne "no") {
    my $cessinfo = " (收取税率: $postcess%)" if ($postcess ne '' && $postcess >= 1 && $postcess <= 100);
    $salepost = qq~<input type=checkbox name="moneyhidden" value="yes">出售此帖，只有付钱才可以查看，售价 <input type="text" name="moneypost" size="5" maxlength="5" value="100"> $moneyname$cessinfo<br>~;
} else {
    undef $salepost;
}

if ($canchgfont ne "no") {
    $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes">使用字体转换？<br>~;
} else {
    undef $fontpost;
}

if ($nowater eq "on") { 
    $gsnum = 0 if ($gsnum<=0);
    $nowaterpost =qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>灌水限制</b></font></td><td bgcolor=$miscbackone><input type="radio" class=1 name="inwater" value="no"> 不许灌水　 <input name="inwater" type="radio" class=1 value="yes" checked> 允许灌水　    [如果选择“不许灌水”，则回复不得少于 <B>$gsnum</B> 字节]</td></tr>~;
}

if ($useemote eq "yes") {
    $filetoopen = "$lbdir" . "data/emote.cgi";
    open (FILE, "$filetoopen");
    $emote = <FILE>;
    close (FILE);
}
else { undef $emote; }


$helpurl = &helpfiles("阅读标记");
$helpurl = qq~$helpurl<img src=$imagesurl/images/$skin/help_b.gif border=0></span>~;

my %Mode = (
    'new'        => \&newthread,
    'reply'      => \&reply,
    'replyquote' => \&replyquote,
    'pay'      => \&pay,
    'copy1'      => \&copy1
);

    if ($arrawpostpic eq "on")      { $postpicstates = "允许";}      else { $postpicstates = "禁止";}
    if ($arrawpostflash eq "on")    { $postflashstates = "允许";}    else { $postflashstates = "禁止";}
    if ($arrawpostfontsize eq "on") { $postfontsizestates = "允许";} else { $postfontsizestates = "禁止";}
    if ($arrawpostsound eq "on")    { $postsoundstates = "允许";}    else { $postsoundstates = "禁止";}

    if ($postjf eq "yes")    { $postjfstates = "允许";}    else { $postjfstates = "禁止";}
    if ($jfmark eq "yes")    { $jfmarkstates = "允许";}    else { $jfmarkstates = "禁止";}
    if ($hidejf eq "yes")    { $hidejfstates = "允许";}    else { $hidejfstates = "禁止";}

    if ($Mode{$action}) { $Mode{$action}->(); }
    elsif ($action eq "addnew"  )  { &addnewthread; }
    elsif ($action eq "addreply")  { &addreply; }
    elsif ($action eq "addnewpay"  )  { &addnewpay; }
    else { &error("普通错误&请以正确的方式访问本程序！"); }

&output("$boardname - 在$forumname内发帖",\$output);
exit;

sub copy1 {
    require "gettopiccopy.pl";
}

sub pay {
    require "pay.pl";
}

sub addnewpay {
    require "addnewpay.pl";
}

sub addreply {
    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
        &error("发帖&你的积分为 $jifen，而本论坛只有积分大于等于 $replyminjf 的才能回复！") if ($replyminjf > 0 && $jifen < $replyminjf);
    }
    &error("出错&请不要用外部连接本程序！") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
    require "dotopicreplay.pl";
}

sub addnewthread {
    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
        &error("发帖&你的积分为 $jifen，而本论坛只有积分大于等于 $postminjf 的才能发言！") if ($postminjf > 0 && $jifen < $postminjf);
    }
    &error("出错&请不要用外部连接本程序！") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
    require "doaddnewtopic.pl";
}

sub replyquote {
    if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
        &error("发帖&你的积分为 $jifen，而本论坛只有积分大于等于 $replyminjf 的才能回复！") if ($replyminjf > 0 && $jifen < $replyminjf);
    }
    require "doreplyquote.pl";
}

sub newthread {
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

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	&error("发表新主题&对不起，你的删贴率超过了<b>$deletepercent</b>%，管理员不允许你发表新主题！请联系坛主解决！") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") { &whosonline("$inmembername\t$forumname\tnone\t发表新主题\t"); }
	                       else { &whosonline("$inmembername\t$forumname(密)\tnone\t发表新的保密主题\t"); }
    }
    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     {  $onlinetime = $onlinetime + $onlinetimeadd; &error("发表新主题&对不起，本论坛不允许在线时间少于 $onlinepost 秒的用户发表主题！你目前已经在线 $onlinetime 秒！<BR>如果在线时间统计不正确,请重新登陆论坛一次即可解决！"); }

    &mischeader("发表新主题");

    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>有回复时使用邮件通知您？<br>~;
    }

    if ($startnewthreads eq "no")        { $startthreads = "在此论坛中新的主题和帖子回复只能由坛主、版主发表！"; }
    elsif ($startnewthreads eq "follow") { $startthreads = "在此论坛中新的主题只能由坛主、版主发表！普通会员只可以跟帖！"; }
    elsif ($startnewthreads eq "all")    { $startthreads = "任何人均可以发表和回复主题，未注册用户发帖密码请留空！"; }
    elsif ($startnewthreads eq "cert")   { $startthreads = "在此论坛中新的主题只能由坛主、版主、认证的会员发表！"; }
    else { $startthreads = "所有注册会员均可以发表和回复主题！"; }

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
<input type=hidden name=action value=addnew>
<input type=hidden name=forum value=$inforum>
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>谁可以发表？</b> $startthreads</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>主题标题</b></font>　
<select name=font onchange=DoTitle(this.options[this.selectedIndex].value)>
<OPTION selected value="">选择话题</OPTION> <OPTION value=[原创]>[原创]</OPTION><OPTION value=[转帖]>[转帖]</OPTION><OPTION value=[灌水]>[灌水]</OPTION><OPTION value=[讨论]>[讨论]</OPTION><OPTION value=[求助]>[求助]</OPTION><OPTION value=[推荐]>[推荐]</OPTION><OPTION value=[公告]>[公告]</OPTION><OPTION value=[注意]>[注意]</OPTION><OPTION value=[贴图]>[贴图]</OPTION><OPTION value=[建议]>[建议]</OPTION><OPTION value=[下载]>[下载]</OPTION><OPTION value=[分享]>[分享]</OPTION>
</SELECT></td><td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="intopictitle" value="$intopictitle">　不得超过 40 个汉字</td></tr>$nowaterpost
    ~;
    &posttable(1);
}

sub reply {
#&getoneforum("$inforum");
    &moderator("$inforum");
    $tempaccess = "forumsallowed". "$inforum";
    $testentry = $query->cookie("$tempaccess");
    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("发表&对不起，您不允许在此论坛发表！");}
    if ($postopen eq "no") { &error("发表或回复主题&对不起，本论坛不允许发表或回复主题！"); }
    &error("普通错误&客人不能查看贴子内容，请注册或登录后再试") if (($guestregistered eq "off")&&($inmembername eq "客人"));

    open(FILE, "${lbdir}forum$inforum/$intopic.thd.cgi");
    @threads = <FILE>;
    close(FILE);
    $posttoget = $inpostno - 1;
    ($membername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post) = split(/\t/, $threads[$posttoget]);
    $topictitle =~ s/^＊＃！＆＊//;

    if ($emoticons eq "on") {
        $emoticonslink = qq~<li><a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">允许<B>使用</B>表情字符转换</a>~;
        $emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>您是否希望<b>使用</b>表情字符转换在您的文章中？<br>~;
    }
    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>有回复时使用邮件通知您？<br>~;
    }

    &mischeader("发表回复");

    $output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;

    if ($htmlstate eq "on")     { $htmlstates = "可用";     } else { $htmlstates = "不可用";     }
    if ($idmbcodestate eq "on") { $idmbcodestates = "可用"; $canlbcode =qq~<input type=checkbox name="uselbcode" value="yes" checked>使用 LeoBBS 标签？<br>~; } else { $idmbcodestates = "不可用"; $canlbcode= "";}
    if ($useemote eq "no")      { $emotestates = "不可用";  } else { $emotestates = "可用"; }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") {
     	    &whosonline("$inmembername\t$forumname\tnone\t回复<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t");
	}
	else {
            &whosonline("$inmembername\t$forumname(密)\tnone\t回复保密帖子\t");
	}
    }
    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     {  $onlinetime = $onlinetime + $onlinetimeadd; &error("回复主题&对不起，本论坛不允许在线时间少于 $onlinepost 秒的用户回复主题！你目前已经在线 $onlinetime 秒！<BR>如果在线时间统计不正确,请重新登陆论坛一次即可解决！"); }

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
<input type=hidden name="action" value="addreply">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor><b>主题标题</b>： $topictitle</td></tr>
    ~;
    &posttable(2);
    require "dothreadreview.pl";
}

sub posttable {
    my $page = shift;
    $output .= qq~<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>您目前的身份是： <font color=$fonthighlight><B><u>$inmembername</u></B></font> ，要使用其他用户身份，请输入用户名和密码。未注册客人请输入网名，密码留空。</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的用户名</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">您没有注册？</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>请输入您的密码</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">忘记密码？</a></font></td></tr>
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
	$output .= qq~<input type=radio value="$_" name="posticon"><img src=$imagesurl/posticons/$_ $defaultsmilewidth $defaultsmileheight>&nbsp;~;
	$tempiconnum ++;
    }
    if ((($page eq 1)&&($arrowupload ne "off"))||(($page eq 2)&&($allowattachment ne "no"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) {
    $uploadreqire = "" if ($uploadreqire <= 0);
    $uploadreqire = "<BR>发帖数要大于 <B>$uploadreqire</B> 篇(认证用户不限)" if ($uploadreqire ne "");
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        $output .= qq~<tr><td bgcolor=$miscbackone><b>上传附件或图片</b> (最大容量 <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>目前附件:(如不需要某个附件，只需删除内容中的相应 [UploadFile$imgslt ...] 标签即可)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=删除所有未被发布的附件临时文件 OnClick="return confirm('确定删除所有未被发布的附件临时文件么？');">删除</a>] </font></font><SPAN id=showupfile name=showupfile></SPAN></td></tr>~;
    }
    $maxpoststr = "(帖子中最多包含 <B>$maxpoststr</B> 个字符)" if ($maxpoststr ne "");
    
    $output .= qq~</td></tr><td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>内容</b>　$maxpoststr<p>在此论坛中：<li>HTML 　标签: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE　标签</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS 标签</a>: <b>$idmbcodestates</b><li>贴图标签 　: <b>$postpicstates</b><li>Flash 标签 : <b>$postflashstates</b><li>音乐标签 　: <b>$postsoundstates</b><li>文字大小 　: <b>$postfontsizestates</b><li>帖数标签 　: <b>$postjfstates</b><li>积分标签 　: <b>$jfmarkstates</b><li>保密标签 　: <b>$hidejfstates</b>$emoticonslink</font></td><td bgcolor=$miscbackone>$insidejs<TEXTAREA cols=80 name=inpost id=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$inpost</TEXTAREA><br>
&nbsp; 模式:<input type="radio" name="mode" value="help" onClick="thelp(1)">帮助　<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">完全　<input type="radio" name="mode" value="basic"  onClick="thelp(0)">基本　　>> <a href=javascript:HighlightAll('FORM.inpost')>复制到剪贴板</a> | <a href=javascript:checklength(document.FORM);>查看长度</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">转换剪贴板超文本</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<
</td></tr></tr>~;
    
    if ($emoticons eq "on") {
	$output .= qq~<tr><td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>点击表情图即可在帖子中加入相应的表情</B></font><br>&nbsp;~;
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
$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton$salepost
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
}

sub addmytopic {
   my ($mode, $cleanmembername, $inforum, $intopic, $topictitle, $currenttime, $posticon) = @_;
   if ($recorddir eq "") {
     opendir (DIRS, "$lbdir");
     my @files = readdir(DIRS);
     closedir (DIRS);
     @files = grep(/^\w+?$/i, @files);
     my @recorddir = grep(/^record/i, @files);
     $recorddir = $recorddir[0];
   }
#   mkdir ("${lbdir}$recorddir", 0777) if (!(-e "${lbdir}$recorddir"));
   mkdir ("${lbdir}$recorddir/$mode", 0777) if (!(-e "${lbdir}$recorddir/$mode"));
   my $filetoopen = $lbdir . "$recorddir/" . $mode . "/" . $cleanmembername . ".cgi";
   my $lockfile = &lockfilename($filetoopen);
   isc><b>