#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / é›·å‚²æé…·è¶…çº§è®ºå›  #
#####################################################
# åŸºäºå±±é¹°(ç³Š)ã€èŠ±æ— ç¼ºåˆ¶ä½œçš„ LB5000 XP 2.30 å…è´¹ç‰ˆ  #
#   æ–°ç‰ˆç¨‹åºåˆ¶ä½œ & ç‰ˆæƒæ‰€æœ‰: é›·å‚²ç§‘æŠ€ (C)(R)2004    #
#####################################################
#      ä¸»é¡µåœ°å€ï¼š http://www.LeoBBS.com/            #
#      è®ºå›åœ°å€ï¼š http://bbs.LeoBBS.com/            #
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
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
$LBCGI::POST_MAX=500000;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "editpoll.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$addme=$query->param('addme');
for ('forum','topic','membername','password','action','inshowsignature','notify','inshowemoticons','newtopictitle',
    'inpost','posticon','hidepoll','inhiddentopic','postweiwang','canpoll','uselbcode','inshowchgfont','inwater') {
    next unless defined $_;
    next if $_ eq 'SEND_MAIL';
    $tp = $query->param($_);
    $tp = &cleaninput("$tp");
    ${$_} = $tp;
}

$inforum       = $forum;
$intopic       = $topic;
&error("æ‰“å¼€æ–‡ä»¶&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if (($intopic) && ($intopic !~ /^[0-9 ]+$/));
&error("æ‰“å¼€æ–‡ä»¶&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if ($inforum !~ /^[0-9 ]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }
&error("æ™®é€šé”™è¯¯&è¯·ä»¥æ­£ç¡®çš„æ–¹å¼è®¿é—®æœ¬ç¨‹åºï¼") if (($postweiwang > $maxweiwang)&&($inhiddentopic eq "yes"));
$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$innotify      = $notify;
$indeletepost  = $deletepost;
$currenttime   = time;
$inposticon    = $posticon;
$inpost        =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost        =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost        =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost        =~ s/\[USECHGFONTE\]/\[USECHGFONT\&\#069\;\]/sg;
$inpost        =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ALIPAYE\]/\[ALIPAY\&\#069\;\]/sg;

$inpost        .=($uselbcode eq "yes")?"":"[DISABLELBCODE]" if($action eq "processedit");
$inpost        .=($inshowchgfont eq "yes")?"[USECHGFONTE]":"" if (($action eq "processedit")&&($canchgfont ne "no"));

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
if (! $inmembername) { $inmembername = $query->cookie("amembernamecookie"); }
if (! $inpassword) { $inpassword = $query->cookie("apasswordcookie"); }
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

if ($inmembername eq "" || $inmembername eq "å®¢äºº" ) {
    $inmembername = "å®¢äºº";
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("æ™®é€šé”™è¯¯&æ­¤ç”¨æˆ·æ ¹æœ¬ä¸å­˜åœ¨ï¼") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie        = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie        = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("æ™®é€šé”™è¯¯&å¯†ç ä¸ç”¨æˆ·åä¸ç›¸ç¬¦ï¼Œè¯·é‡æ–°ç™»å½•ï¼");
     }
}
require "postjs.cgi";

$maxpoststr = "" if ($maxpoststr eq 0);
$maxpoststr = 100 if (($maxpoststr < 100)&&($maxpoststr ne ""));

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&moderator("$inforum"); 
&error("è¿›å…¥è®ºå›&ä½ çš„è®ºå›ç»„æ²¡æœ‰æƒé™è¿›å…¥è®ºå›ï¼") if ($yxz ne '' && $yxz!~/,$membercode,/);
if ($allowusers ne ''){
    &error('è¿›å…¥è®ºå›&ä½ ä¸å…è®¸è¿›å…¥è¯¥è®ºå›ï¼') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &error("è¿›å…¥è®ºå›&ä½ ä¸å…è®¸è¿›å…¥è¯¥è®ºå›ï¼Œä½ çš„å¨æœ›ä¸º $ratingï¼Œè€Œæœ¬è®ºå›åªæœ‰å¨æœ›å¤§äºç­‰äº $enterminweiwang çš„æ‰èƒ½è¿›å…¥ï¼") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&error("è¿›å…¥è®ºå›&ä½ ä¸å…è®¸è¿›å…¥è¯¥è®ºå›ï¼Œä½ çš„é‡‘é’±ä¸º $mymoney1ï¼Œè€Œæœ¬è®ºå›åªæœ‰é‡‘é’±å¤§äºç­‰äº $enterminmony çš„æ‰èƒ½è¿›å…¥ï¼") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
	&error("è¿›å…¥è®ºå›&ä½ ä¸å…è®¸è¿›å…¥è¯¥è®ºå›ï¼Œä½ çš„ç§¯åˆ†ä¸º $jifenï¼Œè€Œæœ¬è®ºå›åªæœ‰ç§¯åˆ†å¤§äºç­‰äº $enterminjf çš„æ‰èƒ½è¿›å…¥ï¼") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}

if ($useemote eq "yes") {
    open (FILE, "${lbdir}data/emote.cgi");
    $emote = <FILE>;
    close (FILE);
}
else { undef $emote; }

if ($inshowemoticons ne "yes")  { $inshowemoticons eq "no"; }
if ($innotify ne "yes")         { $innotify eq "no"; }
if ($arrawpostpic eq "on")      { $postpicstates = "å…è®¸";}      else { $postpicstates = "ç¦æ­¢";}
if ($arrawpostfontsize eq "on") { $postfontsizestates = "å…è®¸";} else { $postfontsizestates = "ç¦æ­¢";}
if ($arrawpostsound eq "on")    { $postsoundstates = "å…è®¸";}    else { $postsoundstates = "ç¦æ­¢";}
if ($postjf eq "yes")    { $postjfstates = "å…è®¸";}    else { $postjfstates = "ç¦æ­¢";}
if ($jfmark eq "yes")    { $jfmarkstates = "å…è®¸";}    else { $jfmarkstates = "ç¦æ­¢";}
if ($hidejf eq "yes")    { $hidejfstates = "å…è®¸";}    else { $hidejfstates = "ç¦æ­¢";}

if ($action eq "edit") { &editform;}
elsif ($action eq "processedit" )  { &processedit; }
else { &error("æ™®é€šé”™è¯¯&è¯·ä»¥æ­£ç¡®çš„æ–¹å¼è®¿é—®æœ¬ç¨‹åº"); }
    
&output($boardname,\$output);
exit;

sub editform {
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    &winlock($filetoopen) if ($OS_USED eq "Nt");
    open(FILE, "$filetoopen");
    flock(FILE, 1) if ($OS_USED eq "Unix");
    my $threads = <FILE>;
    close(FILE);
    &winunlock($filetoopen) if ($OS_USED eq "Nt");
    chomp $threads;

    ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon, $water) = split(/\t/, $threads);
    $topictitle =~ s/^ï¼Šï¼ƒï¼ï¼†ï¼Š//;
    &error("ç¼–è¾‘å¸–å­&æ²¡æé”™å§ï¼Œè¿™æ ¹æœ¬ä¸æ˜¯æŠ•ç¥¨è´´å­å•Šï¼") if ($posticon !~ /<BR>/i);
    $inmembmod = "no" if (($membercode eq "amo")&&($allowamoedit ne "yes"));
    if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")&&((lc($inmembername) ne lc($postermembername))||($usereditpost eq "no"))) {&error("ç¼–è¾‘æŠ•ç¥¨å¸–å­&æ‚¨ä¸æ˜¯åŸä½œè€…ã€è®ºå›ç‰ˆä¸»ä»¥ä¸Šçº§åˆ« , æˆ–è€…å¯†ç é”™Æ±&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±í£¡"); }

if ($nowater eq "on") { 
    $gsnum = 0 if ($gsnum<=0);
    $nowaterpost =qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>¹àË®ÏŞÖÆ</b></font></td><td bgcolor=$miscbackone><input type="radio" name="inwater" value=no> ²»Ğí¹àË®¡¡ <input name="inwater" type="radio" value=yes> ÔÊĞí¹àË®¡¡    [Èç¹ûÑ¡Ôñ¡°²»Ğí¹àË®¡±£¬Ôò»Ø¸´²»µÃÉÙÓÚ <B>$gsnum</B> ×Ö½Ú]</td></tr>~;
    $nowaterpost =~ s/value=$water/value=$water checked/i if ($water ne "");
}

    if ($wwjf ne "no") {
	if ($post=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg) {
	    $weiwangchecked=" checked";
	    $weiwangchoice=$1;
        } else {
	    undef $weiwangchecked;
	    undef $weiwangchoice;
        }
        for (my $i=0;$i<$maxweiwang;$i++) {
	    $weiwangoption.=qq~<option value=$i>$i</option>~;
        }
        $weiwangoptionbutton=qq~<input type=checkbox name="inhiddentopic" value="yes" $weiwangchecked>¼ÓÃÜ´ËÌû£¬Ö»¶Ô²¿·ÖÓÃ»§¿É¼û£¬ÓÃ»§ÍşÍûÖÁÉÙĞèÒª  <select name=postweiwang>$weiwangoption</select><br>~;
        $weiwangoptionbutton =~ s/option value=$weiwangchoice/option value=$weiwangchoice selected/i if ($weiwangchoice ne "");
    } else {
        undef $weiwangoptionbutton;
    }

    $showsignature="yes$maxpollitem" if($showsignature eq "yes");
    if ($showsignature =~/^yes[0-9]+$/) { $duoxuan='checked';$canpoll=$showsignature;$canpoll=~s/^yes//;$Selected[$canpoll]=" selected"; } else { $duoxuan='';$canpoll=1; }
    if ($post =~m/\[hidepoll\]/isg) { $PollHiddencheck='checked'; } else { $PollHiddencheck=''; }

    if (($post =~ /\[POSTISDELETE=(.+?)\]/)&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
        &error("±à¼­Ìû×Ó&²»ÔÊĞí±à¼­ÒÑ¾­±»µ¥¶ÀÆÁ±ÎµÄÌû×Ó£¡");
    }

    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;
    $post =~ s/\[hidepoll\]//isg;
    $post =~ s/\[Õâ¸öÍ¶Æ±×îºóÓÉ(.+?)±à¼­\]\n//isg;
    $post =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $uselbcodecheck=($post =~/\[DISABLELBCODE\]/)?"":" checked";
    $usecanchgfont=($post =~/\[USECHGFONTE\]/)?" checked":"";
    $post =~ s/\[DISABLELBCODE\]//isg;
    $post =~ s/\[USECHGFONTE\]//isg;
    $post =~ s/\[POSTISDELETE=(.+?)\]//isg;
    $post =~ s/\[ADMINOPE=(.+?)\]//isg;

    $posticon =~ s/\<p\>/\n\n/ig;
    $posticon =~ s/\<br\>/\n/ig;
    if (-e "${lbdir}forum$inforum/$intopic.poll.cgi") { $dis1 = "disabled"; }
    if ($showsignature eq 'yes') {$dis2="checked";}

    &mischeader("±à¼­Ìù×Ó");
    $helpurl = &helpfiles("ÔÄ¶Á±ê¼Ç");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></a>~;
    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>ÓĞ»Ø¸´Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~;
    }
    if ($emoticons eq "on") {
    	$emoticonslink = qq~<a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">ÔÊĞí<B>Ê¹ÓÃ</B>±íÇé×Ö·û×ª»»</a>~;
    	$emoticonsbutton =qq~<input type=checkbox name="inshowemoticons" value="yes" checked>ÄúÊÇ·ñÏ£Íû<b>Ê¹ÓÃ</b>±íÇé×Ö·û×ª»»ÔÚÄúµÄÎÄÕÂÖĞ£¿<br>~;
    }

if ($canchgfont ne "no") {
    $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes"$usecanchgfont>Ê¹ÓÃ×ÖÌå×ª»»£¿<br>~;
} else {
    undef $fontpost;
}

    if ($htmlstate eq "on")      { $htmlstates = "¿ÉÓÃ"; }     else { $htmlstates = "²»¿ÉÓÃ"; }
    if ($idmbcodestate eq "on")  { $idmbcodestates = "¿ÉÓÃ"; $canlbcode = qq~<input type=checkbox name="uselbcode" value="yes"$uselbcodecheck>Ê¹ÓÃ LeoBBS ±êÇ©£¿<br>~; } else { $idmbcodestates = "²»¿ÉÓÃ"; $canlbcode=""; }
    if ($arrawpostflash eq "on") { $postflashstates = "ÔÊĞí";} else {$postflashstates = "½ûÖ¹";}
    if ($useemote eq "no") { $emotestates = "²»¿ÉÓÃ"; } else { $emotestates = "¿ÉÓÃ"; }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
      &whosonline("$inmembername\t$forumname\tnone\t±à¼­<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t") if ($privateforum ne "yes");
      &whosonline("$inmembername\t$forumname(ÃÜ)\tnone\t±à¼­±£ÃÜÍ¶Æ±\t") if ($privateforum eq "yes");
    }
   
    $output .= qq~<script language="javascript">function smilie(smilietext) {smilietext=' :'+smilietext+': ';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? smilietext + ' ' : smilietext;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=smilietext;document.FORM.inpost.focus();}}</script>~;
    $maxpoststr = "(Ìû×ÓÖĞ×î¶à°üº¬ <B>$maxpoststr</B> ¸ö×Ö·û)" if ($maxpoststr ne "");
    foreach (2..$maxpollitem) { $canpolllist.=qq~<option value="$_"$Selected[$_]>$_</option>~; }

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
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic"><SCRIPT>valigntop()</SCRIPT>
<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td>
<table cellpadding=4 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor colspan=2 $catbackpic><font color=$titlefontcolor>&nbsp;</td></tr>
<td bgcolor=$miscbackone><font color=$fontcolormisc><b>Í¶Æ±±êÌâ</b></font></td>
<td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="newtopictitle" value="$topictitle">¡¡²»µÃ³¬¹ı 40 ¸öºº×Ö</td></tr>$nowaterpost
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>Í¶Æ±ÏîÄ¿</b><br><li>Ã¿ĞĞÒ»¸öÍ¶Æ±ÏîÄ¿£¬×î¶à <B>$maxpollitem</b> Ïî<BR><li>³¬¹ı×Ô¶¯×÷·Ï£¬¿ÕĞĞ×Ô¶¯¹ıÂË<BR><li>Èç¹ûÍ¶Æ±ĞèÒª¶àÑ¡£¬ÇëÔÚÑ¡ÔñÖĞ´ò¹³</font></td><td bgcolor=$miscbacktwo valign=top>
<TEXTAREA cols=80 name=posticon rows=6 wrap=soft $dis1>$posticon</TEXTAREA><BR>
<input type=checkbox name="inshowsignature" value="yes" $duoxuan>×î¶à¿ÉÍ¶<select name="canpoll">$canpolllist</select>Ïî¡¡ <input type=checkbox name="hidepoll" value="yes" $PollHiddencheck>ÊÇ·ñ±ØĞëÍ¶Æ±ºó²Å¿É²é¿´½á¹û£¿<br></td></tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>ÄÚÈİ</b>¡¡$maxpoststr<p>
ÔÚ´ËÂÛÌ³ÖĞ£º<li>HTML ±êÇ©¡¡: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE¡¡±êÇ©</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ±êÇ©</a>: <b>$idmbcodestates</b><li>ÌùÍ¼±êÇ©¡¡ : <b>$postpicstates</b><li>Flash ±êÇ© : <b>$postflashstates</b><li>ÒôÀÖ±êÇ©¡¡ : <b>$postsoundstates</b><li>ÎÄ×Ö´óĞ¡¡¡ : <b>$postfontsizestates</b><li>ÌûÊı±êÇ© ¡¡: <b>$postjfstates</b><li>»ı·Ö±êÇ© ¡¡: <b>$jfmarkstates</b><li>±£ÃÜ±êÇ© ¡¡: <b>$hidejfstates</b><li>$emoticonslink</font></td>
<td bgcolor=$miscbackone>$insidejs<TEXTAREA cols=80 name=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$post</TEXTAREA><br>
&nbsp; Ä£Ê½:<input type="radio" name="mode" value="help" onClick="thelp(1)">°ïÖú¡¡<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">ÍêÈ«¡¡<input type="radio" name="mode" value="basic"  onClick="thelp(0)">»ù±¾¡¡¡¡>> <a href=javascript:HighlightAll('FORM.inpost')>¸´ÖÆµ½¼ôÌù°å</a> | <a href=javascript:checklength(document.FORM);>²é¿´³¤¶È</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">×ª»»¼ôÌù°å³¬ÎÄ±¾</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<</td></tr>
<tr><td bgcolor=$miscbackone valign=top colspan=2><font color=$fontcolormisc><b>µã»÷±íÇéÍ¼¼´¿ÉÔÚÌù×ÓÖĞ¼ÓÈëÏàÓ¦µÄ±íÇé</B></font><br>&nbsp;~;
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
if (page != 1) { out += '<span style=cursor:hand onclick="emotpage(-1)" title=ÉÏÒ»Ò³><font face=webdings size=+1>7</font></span> '; }
for (var i=beginemot;i<emotarray.length && i < endemot ;i++){out += ' <img src=$imagesurl/emot/' + emotarray[i] + ' border=0 onClick="smilie(\\'' + emotarray[i].replace(".gif", "") + '\\');FORM.inpost.focus()" style=cursor:hand> ';}
if (page != eofpage){ out += ' <span style=cursor:hand onclick="emotpage(1)" title=ÏÂÒ»Ò³><font face=webdings size=+1>8</font></span>'; }
out += '  µÚ '+ page+' Ò³£¬×Ü¹² '+ eofpage+ ' Ò³£¬¹² '+emotarray.length+' ¸ö';
out += '  <B><span style=cursor:hand onclick="showall()" title="ÏÔÊ¾ËùÓĞ±íÇéÍ¼Ê¾">[ÏÔÊ¾ËùÓĞ]</span></B>';
emotbox.innerHTML=out;
}
emotpage (1);
function showall (){var out ='';for (var i=0;i<emotarray.length;i++){out += ' <img src=$imagesurl/emot/' + emotarray[i] + ' border=0 onClick="smilie(\\'' + emotarray[i].replace(".gif", "") + '\\');FORM.inpost.focus()" style=cursor:hand> ';}emotbox.innerHTML=out;}
</script>
~;
	}
    $output .= qq~</td></tr><tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>Ñ¡Ïî</b><p>$helpurl</font></td><td bgcolor=$miscbacktwo>
<font color=$fontcolormisc>$canlbcode$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton</font></td></tr><tr><td bgcolor=$miscbackone colspan=2 align=center>
<input type=Submit value="·¢ ±í" name=Submit onClick="return clckcntr();">¡¡¡¡<input type=button value='Ô¤ ÀÀ' name=Button onclick=gopreview()>¡¡¡¡<input type="reset" name="Clear" value="Çå ³ı"></td></form></tr></table></tr></td></table><SCRIPT>valignend()</SCRIPT>
<form name=preview action=preview.cgi method=post target=preview_page><input type=hidden name=body value=""><input type=hidden name=forum value="$inforum"></form>
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
    $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
    if (-e $filetoopen) {
	&winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE, "$filetoopen");
	flock(FILE, 1) if ($OS_USED eq "Unix");
	sysread(FILE, my $allthreads,(stat(FILE))[7]);
	close(FILE);
	$allthreads =~ s/\r//isg;
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
	@allthreads = split (/\n/, $allthreads);
    }
    else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("±à¼­&Õâ¸öÖ÷Ìâ²»´æÔÚ£¡"); }

    ($postermembername, $topictitle, $postipaddress, $showemoticons, $showsignature ,$postdate, $post, $posticon) = split(/\t/, $allthreads[0]);

    $addpost = "";
    while ($post =~ /\[ADMINOPE=(.+?)\]/s) {
	$addpost .= "[ADMINOPE=$1]";
	$post =~ s/\[ADMINOPE=(.+?)\]//s;
    }
    
    if (($post =~ /\[POSTISDELETE=(.+?)\]/)&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
        &error("±à¼­Í¶Æ±Ìû&²»ÔÊĞí±à¼­ÒÑ¾­±»µ¥¶ÀÆÁ±ÎµÄÌû×Ó£¡");
    }

$post =~ s/\[Õâ¸ö(.+?)×îºóÓÉ(.+?)±à¼­\]//isg;
($edittimes, $temp) = split(/ ´Î/, $2);
($temp, $edittimes) = split(/µÚ /, $edittimes);
$edittimes = 0 unless ($edittimes);

    $inmembmod = "no" if (($membercode eq "amo")&&($allowamoedit ne "yes"));
    if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")&&(lc($inmembername) ne lc($postermembername))) {&error("±à¼­Ìû×Ó&Äú²»ÊÇÔ­×÷Õß¡¢ÂÛÌ³¹ÜÀíÔ± , »òÕßÓÃ»§Ãû¡¢ÃÜÂë´íÕ`£¡");}
    $testentry = $query->cookie("forumsallowed$inforum");
    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    else { $allowed  = "no"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("·¢±íÍ¶Æ±&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±íÍ¶Æ±£¡"); }

    &error("±à¼­Ìû×Ó&Ã»¸ã´í°É£¬Õâ¸ù±¾²»ÊÇÍ¶Æ±Ìù×Ó°¡£¡") if ($posticon !~ /<BR>/i);
    &error("±à¼­Ìû×Ó&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±í³¬¹ı <B>$maxpoststr</B> ¸ö×Ö·ûµÄÎÄÕÂ£¡") if ((length($inpost) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("±à¼­Ìû×Ó&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±íÉÙÓÚ <B>$minpoststr</B> ¸ö×Ö·ûµÄÎÄÕÂ£¡") if ((length($inpost) < $minpoststr)&&($minpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    if (($membercode eq "banned")||($membercode eq "masked"))      { &error("±à¼­Í¶Æ±&Äú±»½ûÖ¹·¢ÑÔ»òÕß·¢ÑÔÒÑ¾­±»ÆÁ±Î£¬ÇëÁªÏµ¹ÜÀíÔ±ÒÔ±ã½â¾ö£¡"); }

    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if ((lc($inmembername) eq lc($postermembername)) && ($inpassword eq $password) && ($usereditpost ne "no")) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit eq "no"; }

    if ($cleartoedit eq "yes") {
	$editpostdate = $currenttime + ($timezone + $timedifferencevalue)*3600;
        $editpostdate = &dateformat("$editpostdate");
        $inpost =~ s/\t//g;
        $inpost =~ s/\r//g;
        $inpost =~ s/  / /g;
        $inpost =~ s/\n\n/\<p\>/g;
        $inpost =~ s/\n/\<br\>/g;
        $inpost =~ s/\[Õâ¸ö(.+?)×îºóÓÉ(.+?)±à¼­\]//isg;

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.poll.cgi";
        if(!(-e $filetoopen)){
	    $inposticon=~s/<p>/<BR>/isg;
            $inposticon=~s/<BR><BR>/<BR>/isg;
            $inposticon =~ s/(.*)<BR>$/$1/i;
            $inposticon =~ s/^<BR>(.*)/$1/i;
	    $inposticon =~ s/<BR>(\s*)/<BR>/i;
	    $inposticon =~ s/(\s*)<BR>/<BR>/i;
            $inposticontemp = $inposticon;
            $inposticontemp=~s/<br>/\t/ig;
            my @temppoll = split(/\t/, $inposticontemp);
            my $temppoll = @temppoll;
   	    $canpoll=$temppoll if($canpoll > $temppoll || $canpoll =~m/[^0-9]/);
   	    $inshowsignature.=$canpoll if($inshowsignature ne "no");
   	    if ($inposticon !~ m/<br>/i)   { &error("±à¼­Í¶Æ±&Í¶Æ±Ñ¡ÏîÌ«ÉÙ£¡"); }
	    if ($temppoll > $maxpollitem ) { &error("±à¼­Í¶Æ±&Í¶Æ±Ñ¡Ïî¹ı¶à£¬²»ÄÜ³¬¹ı $maxpollitem Ïî£¡(Äú´Ë´ÎÍ¶Æ±µÄÑ¡ÏîÓĞ $temppoll Ïî)"); }
	} else {
           $inposticon=$posticon;
           $inposticontemp = $inposticon;
           $inposticontemp=~s/<br>/\t/ig;
           my @temppoll = split(/\t/, $inposticontemp);
           my $temppoll = @temppoll;
           $canpoll=$temppoll if($canpoll > $temppoll || $canpoll =~m/[^0-9]/);
           $inshowsignature.=$canpoll if($inshowsignature ne "no");
        }
        if ($emote && $inpost =~ m/\/\/\//) {
	    study ($inpost);
 	    my @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		my ($toemote, $beemote) = split(/=/,$_);
		chomp $beemote;
		$beemote =~ s/¶ÔÏó/¡¼$inmembername¡½/isg;
		$inpost =~ s/$toemote/$beemote/isg;
		last unless ($inpost =~ m/\/\/\//);
	    }
	}

	my $temp = &dofilter("$newtopictitle\t$inpost");
	($newtopictitle,$inpost) = split(/\t/,$temp);
	$newtopictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
	$newtopictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
	$newtopictitle =~ s/(o|O)R/$1&#82;/sg;
	$newtopictitle =~ s/(o|O)r/$1&#114;/sg;
#	$newtopictitle =~ s/\\/&#92;/isg;

        if ($newtopictitle eq "") { &error("±à¼­Í¶Æ±&¶Ô²»Æğ£¬Ìù×ÓÖ÷Ìâ²»ÄÜÎª¿Õ£¡");}
        if (length($newtopictitle) > 110)  { &error("±à¼­Í¶Æ±&¶Ô²»Æğ£¬Ö÷Ìâ±êÌâ¹ı³¤£¡"); }
        $newtopictitletemp = $newtopictitle;
	$newtopictitle  = "£ª£££¡£¦£ª$newtopictitle";

	$edittimes++;
	$noaddedittime = 60 if ($noaddedittime < 0);
	$inpost = qq~[Õâ¸öÍ¶Æ±×îºóÓÉ$inmembernameÔÚ $editpostdate µÚ $edittimes ´Î±à¼­]<br><br>$inpost~ if (($currenttime - $postdate) > $noaddedittime || $postermembername ne $inmembername);

        $inpost =~ s/\[hidepoll\]//isg;
	$inpost .="[hidepoll]" if($hidepoll eq "yes");

	if ($inhiddentopic eq "yes") { $inposttemp = "(±£ÃÜ)"; $inpost="LBHIDDEN[$postweiwang]LBHIDDEN".$inpost; }
	else {
	    $inposttemp = $inpost;
	    $inposttemp = &temppost($inposttemp);
	    chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp,50);
        }
	$inpost =~ s/\[hidepoll\]//isg;
        $inpost .="[hidepoll]" if ($hidepoll eq "yes");
        $postcountcheck = 0;
	$inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

	$filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	if (open(FILE, ">$filetoopen")) {
	    flock(FILE, 2) if ($OS_USED eq "Unix");
            foreach $postline (@allthreads) {
		chomp $postline;
		if ($postcountcheck eq 0) {
		    print FILE "$postermembername\t$newtopictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$postdate\t$addpost$inpost\t$inposticon\t$inwater\t\n";
                }
                else {
		    (my $postermembertemp, my $no, my @endall) = split(/\t/,$postline);
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
        $newtopictitle =~ s/^£ª£££¡£¦£ª//;

        $filetoopen = "${lbdir}forum$inforum/$intopic.pl";
	open(FILE, "$filetoopen");
	my $topicall = <FILE>;
        close(FILE);
        chomp $topicall;
	(my $topicidtemp, $topictitletemp, my @endall) = split (/\t/, $topicall);
	$oldinposttemp = pop(@endall);
	$oldinposttemp = $inposttemp if ($threadnum eq 1);
	if (($topictitletemp ne $newtopictitletemp)||($threadnum eq 1)) {
	    $oldinposttemp = $inposttemp if ($threadnum eq 1);
            $topicall =~ s/^$intopic\t(.*?)\t(.*)\t(.*?)\t(.*?)\t/$intopic\t£ª£££¡£¦£ª$newtopictitletemp\t$2\t$oldinposttemp\t$4\t/isg;
            if (open(FILE, ">$filetoopen")) {
            	print FILE "$topicall";
                close(FILE);
            }

	    $filetoopen = "$lbdir" . "boarddata/listall$inforum.cgi";
            &winlock($filetoopen) if ($OS_USED eq "Nt");
            open(FILE, "$filetoopen");
            flock(FILE, 2) if ($OS_USED eq "Unix");
	    sysread(FILE, my $allthreads,(stat(FILE))[7]);
            close(FILE);
	    $allthreads =~ s/\r//isg;
	    $allthreads =~ s/(.*)(^|\n)$intopic\t(.*?)\t(.*?)\t(.*?)\t\n(.*)/$1$2$intopic\t$newtopictitletemp\t$4\t$5\t\n$6/isg;

            if (open(FILE, ">$filetoopen")) {
      		print FILE "$allthreads";
	        close(FILE);
	    }
	    &winunlock($filetoopen) if ($OS_USED eq "Nt");
	}
	if ($topictitletemp ne $newtopictitletemp) {

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
	    	flock (FILE, 1) if ($OS_USED eq "Unix");
	    	my @recentposts=<FILE>;
	    	close(FILE);
	    	if (open (FILE, ">$filetomakeopen")) {
		    flock (FILE, 2) if ($OS_USED eq "Unix");
		    foreach (@recentposts) {
		    	chomp $_;
		    	($tempno1, $tempno2, $no, @endall) = split (/\t/,$_);
		    	next if (($tempno1 !~ /^[0-9]+$/)||($tempno2 !~ /^[0-9]+$/));

		    	if (($tempno1 eq $inforum)&&($tempno2 eq $intopic)) {
                    	    print FILE "$inforum\t$intopic\t$newtopictitletemp\t";
                    	    foreach (@endall) { chomp $_; print FILE "$_\t"; }
                    	   print FILE "\n"
		    	}
		    	else { print FILE "$_\n" }
		    }
		    close(FILE);
		}
		&winunlock($filetomakeopen) if ($OS_USED eq "Nt");
	    }
	    else {
    		unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
	    }
	}
    }


    &mischeader("±à¼­Í¶Æ±");

for(my $iii=0;$iii<=4;$iii++) {
    my $jjj = $iii * $maxthreads;
    unlink ("${lbdir}cache/plcache$inforum\_$jjj.pl");
}

    if ($refreshurl == 1) { $relocurl = "topic.cgi?forum=$inforum&topic=$intopic"; }
	             else { $relocurl = "forums.cgi?forum=$inforum"; }
    $output .= qq~<table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>±à¼­³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>¾ßÌåÇé¿ö£º
<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic">·µ»ØÍ¶Æ±Ö÷Ìâ</a>
<li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a>
</ul></tr></td></table></td></tr></table>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
}
