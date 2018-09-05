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
$LBCGI::POST_MAX=1024 * 1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";
require "dopost.pl";

$|++;
$thisprog = "editpost.cgi";
$query = new LBCGI;
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$addme=$query->param('addme');

for ('forum','topic','membername','password','action','postno',
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
&error("æ‰“å¼€æ–‡ä»¶&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if (($intopic) && ($intopic !~ /^[0-9 ]+$/));
&error("æ‰“å¼€æ–‡ä»¶&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if ($inforum !~ /^[0-9 ]+$/);
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }

&error("æ™®é€šé”™è¯¯&è¯·ä»¥æ­£ç¡®çš„æ–¹å¼è®¿é—®æœ¬ç¨‹åºï¼") if (($postweiwang > $maxweiwang)&&($inhiddentopic eq "yes"));
$moneymax = 99999 if ($moneymax <=0 || $moneymax >=99999);
$moneypost = int($moneypost) if (($moneypost ne "")&&($moneyhidden eq "yes"));
&error("æ™®é€šé”™è¯¯&è¯·æ­£ç¡®çš„è¾“å…¥å¸–å­çš„ä»·æ ¼ï¼Œä¸è¦å°‘äº 1ï¼Œä¹Ÿä¸è¦å¤§äº $moneymax ï¼") if ((($moneypost > $moneymax)||($moneypost < 1))&&($moneyhidden eq "yes"));
$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$inpostno      = $postno;
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
	    &error("æ™®é€šé”™è¯¯&æ‚¨ä¸èƒ½å¤Ÿå‡ºå”®å¸–å­ï¼") if (!$type && $CANSALELIST !~/\t$inmembername\t/ || $type && $CANSALELIST =~/\t$inmembername\t/);
	}
    }
}

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }
$maxupload = 300 if ($maxupload eq "");

if ($inshowemoticons ne "yes") { $inshowemoticons eq "no"; }
if ($innotify ne "yes")        { $innotify eq "no"; }
if (($inpostno) && ($inpostno !~ /^[0-9]+$/)) { &error("æ™®é€šé”™è¯¯&è¯·ä¸è¦ä¿®æ”¹ç”Ÿæˆçš„ URLï¼"); }
if (($movetoid) && ($movetoid !~ /^[0-9]+$/)) { &error("æ™®é€šé”™è¯¯&è¯·ä¸è¦ä¿®æ”¹ç”Ÿæˆçš„ URLï¼"); }

if ($useemote eq "yes") {
    open (FILE, "${lbdir}data/emote.cgi");
    $emote = <FILE>;
    close (FILE);
}
else { undef $emote; }

$defaultsmilewidth  = "width=$defaultsmilewidth"   if ($defaultsmilewidth ne "" );
$defaultsmileheight = "height=$defaultsmileheight" if ($defaultsmileheight ne "");

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

if ($action eq "edit") { &editform;}
    elsif ($action eq "processedit")  { &processedit;  }
    else { &error("æ™®é€šé”™è¯¯&è¯·ä»¥æ­£ç¡®çš„æ–¹å¼è®¿é—®æœ¬ç¨‹åº."); }
    
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
    $topictitle =~ s/^ï¼Šï¼ƒï¼ï¼†ï¼Š//;
    $post =~ s/\<p\>/\n\n/ig;
    $post =~ s/\<br\>/\n/ig;

    &error("å‘è¡¨&å¯¹ä¸èµ·ï¼Œä¸å…è®¸ç¼–è¾‘æŠ•ç¥¨è´´å­ï¼") if (($posticon =~ m/<BR>/i)&&($posttoget eq 0));

    &error("å‘è¡¨&å¯¹ä¸èµ·ï¼Œä¸å…è®¸è¿™æ ·ç¼–è¾‘äº¤æ˜“å¸–ï¼") if ($post=~m/\[ALIPAYE\]/);

    if ($noedittime ne '') {
	if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
	    &error("ç¼–è¾‘å¸–å­&è¶…è¿‡ $noedittime å°æ—¶ä¸å…è®¸å†ç¼–è¾‘å¸–å­ï¼") if(($currenttime - $postdate) > ($noedittime * 3600));
	}
    }

    $inmembmod = "no" if (($membercode eq "amo")&&($allowamoedit ne "yes"));
    if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")&&((lc($inmembername) ne lc($postermembername))||($usereditpost eq "no"))) {&error("ç¼–è¾‘å¸–å­&æ‚¨ä¸æ˜¯åŸä½œè€…ã€è®ºå›ç®¡ç†å‘˜ï¼Œæˆ–è€…å¯†ç é”™    
    if ($emailfunctions eq "on") {
	if ($innotify eq "yes") { $requestnotify = " checked"; } else { $requestnotify = ""; }
	$requestnotify = qq~<input type=checkbox name="notify" value="yes"$requestnotify>ÓĞ»Ø¸´Ê±Ê¹ÓÃÓÊ¼şÍ¨ÖªÄú£¿<br>~;
    }
    if ($emoticons eq "on") {
        $emoticonslink   = qq~<a href="javascript:openScript('misc.cgi?action=showsmilies',300,350)">ÔÊĞí<B>Ê¹ÓÃ</B>±íÇé×Ö·û×ª»»</a>~;
        $emoticonsbutton = qq~<input type=checkbox name="inshowemoticons" value="yes" checked>ÄúÊÇ·ñÏ£Íû<b>Ê¹ÓÃ</b>±íÇé×Ö·û×ª»»ÔÚÄúµÄÎÄÕÂÖĞ£¿<br>~;
    }

    if ($htmlstate eq "on")         { $htmlstates = "¿ÉÓÃ";         } else { $htmlstates = "²»¿ÉÓÃ";       }
    if ($useemote eq "no") { $emotestates = "²»¿ÉÓÃ"; } else { $emotestates = "¿ÉÓÃ"; }
    if ($arrawpostflash eq "on")    { $postflashstates = "ÔÊĞí";    } else { $postflashstates = "½ûÖ¹";    }
    if ($arrawpostpic eq "on")      { $postpicstates = "ÔÊĞí";      } else { $postpicstates = "½ûÖ¹";      }
    if ($arrawpostfontsize eq "on") { $postfontsizestates = "ÔÊĞí"; } else { $postfontsizestates = "½ûÖ¹"; }
    if ($arrawpostsound eq "on")    { $postsoundstates = "ÔÊĞí";    } else { $postsoundstates = "½ûÖ¹";    }
    if ($postjf eq "yes")           { $postjfstates = "ÔÊĞí";       } else { $postjfstates = "½ûÖ¹";       }
    if ($jfmark eq "yes")    { $jfmarkstates = "ÔÊĞí";}    else { $jfmarkstates = "½ûÖ¹";}
    if ($hidejf eq "yes")           { $hidejfstates = "ÔÊĞí";       } else { $hidejfstates = "½ûÖ¹";       }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
      &whosonline("$inmembername\t$forumname\tnone\t±à¼­<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t") if ($privateforum ne "yes");
      &whosonline("$inmembername\t$forumname(ÃÜ)\tnone\t±à¼­±£ÃÜÌù×Ó\t") if ($privateforum eq "yes");
    }

if (($nowater eq "on")&&($inpostno eq "1")) { 
    $gsnum = 0 if ($gsnum<=0);
    $nowaterpost =qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>¹àË®ÏŞÖÆ</b></font></td><td bgcolor=$miscbackone><input type="radio" name="inwater" value=no> ²»Ğí¹àË®¡¡ <input name="inwater" type="radio" value=yes> ÔÊĞí¹àË®¡¡    [Èç¹ûÑ¡Ôñ¡°²»Ğí¹àË®¡±£¬Ôò»Ø¸´²»µÃÉÙÓÚ <B>$gsnum</B> ×Ö½Ú]</td></tr>~;
    $nowaterpost =~ s/value=$water/value=$water checked/i if ($water ne "");
}

    $rawpost =~ s/\[Õâ¸ö(.+?)×îºóÓÉ(.+?)±à¼­\]\n//isg;
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
        $weiwangoptionbutton=qq~<input type=checkbox name="inhiddentopic" value="yes" $weiwangchecked>¼ÓÃÜ´ËÌû£¬Ö»¶Ô²¿·ÖÓÃ»§¿É¼û£¬ÓÃ»§ÍşÍûÖÁÉÙĞèÒª  <select name=postweiwang>$weiwangoption</select><br>~;
        $weiwangoptionbutton =~ s/option value=$weiwangchoice/option value=$weiwangchoice selected/i if ($weiwangchoice ne "");
    } else {
        undef $weiwangoptionbutton;
    }

    if ($cansale ne "no") {
	if ($rawpost=~/LBSALE\[(.*?)\]LBSALE/sg) { $salechecked=" checked"; $salechoice=$1; } else { undef $salechecked; $salechoice = 100; }
        $salepost = qq~<input type=checkbox name="moneyhidden" value="yes" $salechecked>³öÊÛ´ËÌù£¬Ö»ÓĞ¸¶Ç®²Å¿ÉÒÔ²é¿´£¬ÊÛ¼Û <input type="text" name="moneypost" size="5" maxlength="5" value="$salechoice"> $moneyname<br>~;
    } else {
        undef $salepost;
    }
    if (($rawpost =~ /\[POSTISDELETE=(.+?)\]/)&&($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
        &error("±à¼­Ìû×Ó&²»ÔÊĞí±à¼­ÒÑ¾­±»µ¥¶ÀÆÁ±ÎµÄÌû×Ó£¡");
    }

    $rawpost=~s/LBSALE\[(.*?)\]LBSALE//sg;
    $rawpost=~s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $uselbcodecheck=($rawpost =~/\[DISABLELBCODE\]/)?"":" checked";
    $rawpost =~ s/\[DISABLELBCODE\]//isg;
    $usecanchgfont=($rawpost =~/\[USECHGFONTE\]/)?" checked":"";
    $rawpost =~ s/\[USECHGFONTE\]//isg;
    $rawpost =~ s/\[POSTISDELETE=(.+?)\]//isg;
    $rawpost =~ s/\[ADMINOPE=(.+?)\]//isg;

    &mischeader("±à¼­Ìù×Ó");

    $helpurl = &helpfiles("ÔÄ¶Á±ê¼Ç");
    $helpurl = qq~$helpurl<img src="$imagesurl/images/$skin/help_b.gif" border=0></a>~;

if ($canchgfont ne "no") {
    $fontpost = qq~<input type=checkbox name="inshowchgfont" value="yes"$usecanchgfont>Ê¹ÓÃ×ÖÌå×ª»»£¿<br>~;
} else {
    undef $fontpost;
}
    if ($idmbcodestate eq "on")     { $idmbcodestates = "¿ÉÓÃ"; $canlbcode = qq~<input type=checkbox name="uselbcode" value="yes"$uselbcodecheck>Ê¹ÓÃ LeoBBS ±êÇ©£¿<br>~; } else { $idmbcodestates = "²»¿ÉÓÃ"; $canlbcode=""; }

    if ($inpostno eq "1") {
    	$topictitle = $newtopictitle if ($newtopictitle ne "");
        $topictitle =~s/ \(ÎŞÄÚÈİ\)$//;
        $topictitlehtml = qq~<td bgcolor=$miscbackone><font color=$fontcolormisc><b>Ìù×ÓÖ÷Ìâ</b></font></td><td bgcolor=$miscbackone><input type=text size=60 maxlength=80 name="newtopictitle" value="$topictitle">¡¡²»µÃ³¬¹ı 40 ¸öºº×Ö</td>~;
        $topictitlehtml1="&nbsp;";
    }
    else {
        undef $topictitlehtml;
        $topictitlehtml1 = "<b>* Ìù×ÓÖ÷Ìâ</b>£º $topictitle";
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
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr>
<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>µ±Ç°ĞÄÇé</b><BR><li>½«·ÅÔÚÌù×ÓµÄÇ°Ãæ<BR></font></td>
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

#######¾É·½Ê½µÄ¸½¼ş£¬ÎªÁË¼æÈİ£¬±£Áô############################
    my $p1=$inpostno-1;
    $dirtoopen2 = "$imagesdir" . "$usrdir/$inforum";
    opendir (DIR, "$dirtoopen2");
    @files = readdir(DIR);
    closedir (DIR);
    @files = grep(/^$inforum\_$intopic/,@files);
    if ($p1>0) { @files = grep(/^$inforum\_$intopic\_$p1\./,@files); } else { @files = grep(/^$inforum\_$intopic\./,@files); }
    if ( $#files >= 0 ) { $delimg="<BR><input type=checkbox name='delimg' value='no'>É¾³ıËùÓĞµÄÔ­Í¼Ïñ»ò¸½¼ş</input>"; }
########################################################
if ( $rawpost =~ m/\[UploadFile.{0,6}=([^\\\]]+?)\]/is ) {$delimg="<BR><input type=checkbox name='delimg' value='no'>É¾³ıËùÓĞµÄÔ­Í¼Ïñ»ò¸½¼ş</input>" if ($delimg eq "");}

    if (((($inpostno eq "1")&&($arrowupload ne "off"))||(($inpostno ne "1")&&($allowattachment ne "no"))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"))) {
        $uploadreqire= "" if ($uploadreqire <= 0);
        $uploadreqire = "<BR>·¢ÌûÊıÒª´óÓÚ <B>$uploadreqire</B> Æª(ÈÏÖ¤ÓÃ»§²»ÏŞ)" if ($uploadreqire ne "");
#        $output .= qq~<tr><td bgcolor=$miscbacktwo><b>ÉÏ´«¸½¼ş»òÍ¼Æ¬</b>(×î´ó $maxupload KB)$uploadreqire</td><td bgcolor=$miscbacktwo> <input type="file" size=30 name="addme">¡¡¡¡$addtypedisp</td></tr>~;
        ###Â·Ñîadd start
	$output .= qq~<script language="javascript">function jsupfile(upname) {upname='[UploadFile$imgslt='+upname+']';if (document.FORM.inpost.createTextRange && document.FORM.inpost.caretPos) {var caretPos = document.FORM.inpost.caretPos;caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? upname + ' ' : upname;document.FORM.inpost.focus();} else {document.FORM.inpost.value+=upname;document.FORM.inpost.focus();}}</script>~;
        ###Â·Ñîadd end
        $output .= qq~<tr><td bgcolor=$miscbackone><b>ÉÏ´«¸½¼ş»òÍ¼Æ¬</b> (×î´óÈİÁ¿ <B>$maxupload</B>KB)$uploadreqire</td><td bgcolor=$miscbackone> <iframe id="upframe" name="upframe" src="upfile.cgi?action=uppic&forum=$inforum&topic=$intopic" width=100% height=40 marginwidth=0 marginheight=0 hspace=0 vspace=0 frameborder=0 scrolling=NO></iframe><br><font color=$fonthighlight>Ä¿Ç°¸½¼ş:(Èç²»ĞèÒªÄ³¸ö¸½¼ş£¬Ö»ĞèÉ¾³ıÄÚÈİÖĞµÄÏàÓ¦ [UploadFile$imgslt ...] ±êÇ©¼´¿É)  [<a href=upfile.cgi?action=delup&forum=$inforum target=upframe title=É¾³ıËùÓĞÎ´±»·¢²¼µÄ¸½¼şÁÙÊ±ÎÄ¼ş OnClick="return confirm('È·¶¨É¾³ıËùÓĞÎ´±»·¢²¼µÄ¸½¼şÁÙÊ±ÎÄ¼şÃ´£¿');">É¾³ı</a>] </font></font>$delimg<SPAN id=showupfile name=showupfile></SPAN></td></tr>~;

    }
    $maxpoststr = "(Ìû×ÓÖĞ×î¶à°üº¬ <B>$maxpoststr</B> ¸ö×Ö·û)" if ($maxpoststr ne "");

    $output .= qq~<td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>ÄÚÈİ</b>¡¡$maxpoststr<p>
ÔÚ´ËÂÛÌ³ÖĞ£º<li>HTML ±êÇ©¡¡: <b>$htmlstates</b><li><a href="javascript:openScript('lookemotes.cgi?action=style',300,350)">EMOTE¡¡±êÇ©</a>: <b>$emotestates</b><li><a href="javascript:openScript('misc.cgi?action=lbcode',300,350)">LeoBBS ±êÇ©</a>: <b>$idmbcodestates</b><li>ÌùÍ¼±êÇ©¡¡ : <b>$postpicstates</b><li>Flash ±êÇ© : <b>$postflashstates</b><li>ÒôÀÖ±êÇ©¡¡ : <b>$postsoundstates</b><li>ÎÄ×Ö´óĞ¡¡¡ : <b>$postfontsizestates</b><li>ÌûÊı±êÇ© ¡¡: <b>$postjfstates</b><li>»ı·Ö±êÇ© ¡¡: <b>$jfmarkstates</b><li>±£ÃÜ±êÇ© ¡¡: <b>$hidejfstates</b><li>$emoticonslink</font></td>
<td bgcolor=$miscbackone>$insidejs
<TEXTAREA cols=80 name=inpost rows=12 wrap="soft" onkeydown=ctlent() onselect="storeCaret(this);" onclick="storeCaret(this);" onkeyup="storeCaret(this);">$rawpost</TEXTAREA><br>
&nbsp; Ä£Ê½:<input type="radio" name="mode" value="help" onClick="thelp(1)">°ïÖú¡¡<input type="radio" name="mode" value="prompt" CHECKED onClick="thelp(2)">ÍêÈ«¡¡<input type="radio" name="mode" value="basic"  onClick="thelp(0)">»ù±¾¡¡¡¡>> <a href=javascript:HighlightAll('FORM.inpost')>¸´ÖÆµ½¼ôÌù°å</a> | <a href=javascript:checklength(document.FORM);>²é¿´³¤¶È</a> | <span style=cursor:hand onclick="document.getElementById('inpost').value += trans()">×ª»»¼ôÌù°å³¬ÎÄ±¾</spn><SCRIPT>rtf.document.designMode="On";</SCRIPT> <<</td></tr>
<tr><td bgcolor=$miscbackone valign=top colspan=2>
~;
    if ($emoticons eq "on"){
	$output.=qq~<font color=$fontcolormisc><b>µã»÷±íÇéÍ¼¼´¿ÉÔÚÌù×ÓÖĞ¼ÓÈëÏàÓ¦µÄ±íÇé</B></font><br>&nbsp;~;
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
    }
    if (($inpostno ne 1)&&(($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")||(($arrowuserdel eq "on")&&(lc($inmembername) eq lc($postermembername))))) {
        $managetable = qq~<tr><td bgcolor=$miscbackone><font color=$fontcolormisc><b>¹ÜÀíÔ±Ñ¡Ïî</b></td><td bgcolor=$miscbackone>&nbsp;<a href="delpost.cgi?action=processedit&postno=$inpostno&forum=$inforum&topic=$intopic&deletepost=yes" OnClick="return confirm('ÕæµÄÒªÉ¾³ı´Ë»Ø¸´Ã´£¿');">É¾³ı´Ë»Ø¸´(½÷É÷Ê¹ÓÃ£¬²»¿É»Ö¸´)</a></td></tr>~;
    }
    $output .= qq~</td></tr>
<tr><td bgcolor=$miscbacktwo valign=top><font color=$fontcolormisc><b>Ñ¡Ïî</b><p>$helpurl
</font></td>
<td bgcolor=$miscbacktwo><font color=$fontcolormisc>$canlbcode
<input type=checkbox name="inshowsignature" value="yes" checked>ÊÇ·ñÏÔÊ¾ÄúµÄÇ©Ãû£¿<br>$requestnotify$emoticonsbutton$fontpost$weiwangoptionbutton$salepost
</font></td></tr>$managetable
<tr><td bgcolor=$miscbackone colspan=2 align=center>
<input type=Submit value="·¢ ±í" name=Submit onClick="return clckcntr();">¡¡¡¡<input type=button value='Ô¤ ÀÀ' name=Button onclick=gopreview()>¡¡¡¡<input type="reset" name="Clear" value="Çå ³ı"></td></form></tr></table></tr></td></table><SCRIPT>valignend()</SCRIPT>
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
        open(FILE, "$filetoopen") or &error("±à¼­&Õâ¸öÖ÷Ìâ²»´æÔÚ£¡");
        flock(FILE, 1) if ($OS_USED eq "Unix");
	sysread(FILE, my $allthreads,(stat(FILE))[7]);
        close(FILE);
	$allthreads =~ s/\r//isg;
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        @allthreads = split(/\n/, $allthreads);
    }
    else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("±à¼­&Õâ¸öÖ÷Ìâ²»´æÔÚ£¡"); }

    if (($inhiddentopic eq "yes") && ($moneyhidden eq "yes")) { &error("·¢±íÖ÷Ìâ&Çë²»ÒªÔÚÒ»¸öÌù×ÓÄÚÍ¬Ê±Ê¹ÓÃÍşÍûºÍ½ğÇ®¼ÓÃÜ£¡"); }
    if ((($inhiddentopic eq "yes")||($moneyhidden eq "yes")) && ($userregistered eq "no")) { &error("·¢±íÖ÷Ìâ&Î´×¢²áÓÃ»§ÎŞÈ¨½øĞĞÍşÍûºÍ½ğÇ®¼ÓÃÜ£¡"); }

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
        &error("±à¼­Ìû×Ó&²»ÔÊĞí±à¼­ÒÑ¾­±»µ¥¶ÀÆÁ±ÎµÄÌû×Ó£¡");
    }

    if ($noedittime ne '') {
	if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")) {
	    &error("±à¼­Ìû×Ó&³¬¹ı $noedittime Ğ¡Ê±²»ÔÊĞíÔÙ±à¼­Ìû×Ó£¡") if(($currenttime - $postdate) > ($noedittime * 3600));
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

$post =~ s/\[Õâ¸ö(.+?)×îºó(.+?)±à¼­\]//isg;
($edittimes, $temp) = split(/ ´Î/, $2);
($temp, $edittimes) = split(/µÚ /, $edittimes);
$edittimes = 0 unless ($edittimes);

    $testentry = $query->cookie("forumsallowed$inforum");
    if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
    else { $allowed  = "no"; }
    if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("±à¼­Ö÷Ìâ&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±í£¡"); }

    &error("±à¼­Ìû×Ó&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±í³¬¹ı <B>$maxpoststr</B> ¸ö×Ö·ûµÄÎÄÕÂ£¡") if ((length($inpost) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo')&&($membercode ne 'amo') && ($membercode ne "mo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("±à¼­Ö÷Ìâ&¶Ô²»Æğ£¬²»ÔÊĞí±à¼­Í¶Æ±Ìù×Ó£¡") if (($posticon =~ m/<BR>/i)&&($posttoget eq 0));
    &error("·¢±í&¶Ô²»Æğ£¬²»ÔÊĞíÕâÑù±à¼­½»Ò×Ìû£¡") if ($inpost=~m/\[ALIPAYE\]/);
    &error("±à¼­Ìû×Ó&¶Ô²»Æğ£¬±¾ÂÛÌ³²»ÔÊĞí·¢±íÉÙÓÚ <B>$minpoststr</B> ¸ö×Ö·ûµÄÎÄÕÂ£¡") if ((length($inpost) < $minpoststr)&&($minpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    $inmembmod = "no" if (($membercode eq "amo")&&($allowamoedit ne "yes"));
    if (($membercode ne "ad")&&($membercode ne "smo")&&($inmembmod ne "yes")&&((lc($inmembername) ne lc($postermembername))||($usereditpost eq "no"))) {&error("±à¼­Ìû×Ó&Äú²»ÊÇÔ­×÷Õß¡¢ÂÛÌ³¹ÜÀíÔ±£¬»òÕßÃÜÂë´íÕ`£¬»òÕß´ËÇø²»ÔÊĞí±à¼­Ìû×Ó£¡");} 
    if (($membercode eq "banned")||($membercode eq "masked"))      { &error("±à¼­Ìû×Ó&Äú±»½ûÖ¹·¢ÑÔ»òÕß·¢ÑÔÒÑ¾­±»ÆÁ±Î£¬ÇëÁªÏµ¹ÜÀíÔ±ÒÔ±ã½â¾ö£¡"); }

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
        $inpost =~ s/\[Õâ¸ö(.+?)×îºóÓÉ(.+?)±à¼­\]//isg;

        if ($emote && $inpost =~ m/\/\/\//) {
	    study ($inpost);
 	    my @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
	        chomp $_;
		($toemote, $beemote) = split(/=/,$_);
		$beemote =~ s/¶ÔÏó/¡¼$inmembername¡½/isg;
		$inpost =~ s/$toemote/$beemote/isg;
		last unless ($inpost =~ m/\/\/\//);
	    }
	}

	$newtopictitle =~ s/\(ÎŞÄÚÈİ\)$//;
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
	    $tempintopictitle =~ s/¡¡//g;
	    $tempintopictitle =~ s/^£ª£££¡£¦£ª//;
	    if ($tempintopictitle eq "") { &error("±à¼­Ö÷Ìâ&Ö÷Ìâ±êÌâÓĞÎÊÌâ£¡"); }
	    undef $tempintopictitle; 
        }   
        
        if (($newtopictitle eq "")&&($inpostno eq 1)) { &error("±à¼­Ö÷Ìâ&¶Ô²»Æğ£¬Ìù×ÓÖ÷Ìâ²»ÄÜÎª¿Õ£¡"); }
        if ((length($newtopictitle) > 110)&&($inpostno eq 1))  { &error("±à¼­Ö÷Ìâ&¶Ô²»Æğ£¬Ö÷Ìâ±êÌâ¹ı³¤£¡"); }
        $newtopictitle  = "£ª£££¡£¦£ª$newtopictitle";

	if (($nowater eq "on")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo')&&($membercode ne 'amo')&&($membercode ne 'mo')&&($inmembmod ne "yes")) {
          ($trash, $trash, $trash, $trash, $trash, $trash, $post, $trash,my $water) = split(/\t/,$allthreads[0]);
	  if ($water eq "no") {
	    my $inposttemp = $inpost;
	    $inposttemp =~ s/\[Õâ¸ö(.+?)×îºóÓÉ(.+?)±à¼­\]\<BR\>\<BR\>//isg;
	    $inposttemp =~ s/\[Õâ¸ö(.+?)×îºóÓÉ(.+?)±à¼­\]\<BR\>//isg;
	    $inposttemp =~ s/\[Õâ¸ö(.+?)×îºóÓÉ(.+?)±à¼­\]//isg;
	    $inposttemp =~ s/\[quote\]\[b\]ÏÂÃæÒıÓÃÓÉ\[u\].+?\[\/u\]ÔÚ \[i\].+?\[\/i\] ·¢±íµÄÄÚÈİ£º\[\/b\].+?\[\/quote\]\<br\>//isg;
	    $inposttemp =~ s/\[quote\]\[b\]ÏÂÃæÒıÓÃÓÉ\[u\].+?\[\/u\]ÔÚ \[i\].+?\[\/i\] ·¢±íµÄÄÚÈİ£º\[\/b\].+?\[\/quote\]//isg;
	    if ((length($inposttemp) < $gsnum)&&($gsnum > 0)) {
	        &error("·¢±í»Ø¸´&Çë²»Òª¹àË®£¬±¾Ö÷Ìâ½ûÖ¹ $gsnum ×Ö½ÚÒÔÏÂµÄ¹àË®£¡");
                unlink ("${imagesdir}$usrdir/$inforum/$inforum\_$intopic\_$replynumber.$up_ext") if ($addme);
	    }
	  }
	}

        if ($inpostno eq 1) {
	    $newtopictitle = "$newtopictitle (ÎŞÄÚÈİ)" if (($inpost eq "")&&($addme eq ""));
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
	$inpost = qq~[Õâ¸öÌù×Ó×îºóÓÉ$inmembernameÔÚ $editpostdate µÚ $edittimes ´Î±à¼­]<br><br>$inpost~ if (($currenttime - $postdate) > $noaddedittime || $postermembername ne $inmembername);

        if ($moneyhidden eq "yes") { $inposttemp = "(±£ÃÜ)"; $inpost="LBSALE[$moneypost]LBSALE".$inpost;}

	if ($inhiddentopic eq "yes") { $inposttemp = "(±£ÃÜ)"; $inpost="LBHIDDEN[$postweiwang]LBHIDDEN".$inpost; }

	$inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

	if ($inposttemp ne "(±£ÃÜ)") {
	    $inposttemp = $inpost;
	    $inposttemp = &temppost($inposttemp);
	    chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp,50);
        }

    $p1=$inpostno-1;

########É¾³ı¾É·½Ê½µÄ¸½¼ş£¬¼æÈİµÄ»°±£Áô####
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

#######É¾³ıÈ«²¿Ô­À´µÄ¸½¼ş START###(BY Â·Ñî)
     if ($delimg ne "") {$showerr = &delupfiles(\$inpost,$inforum,$intopic);}; #ĞÂ·½Ê½

#######É¾³ıÈ«²¿Ô­À´µÄ¸½¼ş END

    $topic =$intopic%100;
    my $topath = "${imagesdir}$usrdir/$inforum/$topic"; #Ä¿µÄÄ¿Â¼
  foreach (@addmetotle) {
  	if ($inpost !~ /$_/i) { unlink("$topath\/$_"); }
  }


    my $filesize=0;

   $addme= &upfileonpost(\$inpost,$inforum,$intopic);#´¦ÀíÉÏ´«£¬·µ»ØÊıÖµ¸øBTÇø×öÅĞ¶Ï

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
        $topictitle =~ s/^£ª£££¡£¦£ª//;
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
                print FILE "$intopic\t£ª£££¡£¦£ª$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$posticon\t$posttemp\t$addmetype\t\n";
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

        &mischeader("±à¼­Ìù×Ó");

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
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>±à¼­³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
¾ßÌåÇé¿ö£º<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic&start=$gopage#$posttoget">·µ»ØÖ÷Ìâ</a><li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a></ul>
</tr></td></table></td></tr></table>
<meta http-equiv="refresh" content="3; url=$relocurl">
~;
    }
    else { &error("±à¼­Ìù×Ó&Äú²»ÊÇÔ­×÷Õß£¬»òÕßÓÃ»§Ãû¡¢ÃÜÂë´íÎó£¡"); }
}
