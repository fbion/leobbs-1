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
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
$LBCGI::POST_MAX=500000;
#require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
#require "postjs.cgi";
require "cleanolddata.pl";
require "recooper.pl";

$|++;
$thisprog = "postings.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

for ('forum','topic','membername','password','action','inpost','checked') {
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

$inmembername  = $membername;
$inpassword    = $password;
if ($inpassword ne "") {
    eval {$inpassword = md5_hex($inpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$inpassword = md5_hex($inpassword);');}
    unless ($@) {$inpassword = "lEO$inpassword";}
}

$currenttime   = time;

$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
require "sendmanageinfo.pl" if ($sendmanageinfo eq "yes");
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

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

&error("æ™®é€šé”™è¯¯&æ²¡æœ‰è¿™ä¸ªåˆ†è®ºå›ï¼") if (!(-e "${lbdir}forum$inforum"));
#&getoneforum("$inforum");
&moderator("$inforum");
&cleanolddata;

my %Mode = (
    'lock'                 =>    \&lockthread,
    'unlock'               =>    \&unlockthread,
    'puttop'               =>    \&puttop,
    'putdown'              =>    \&putdown,
    'repireforum'          =>    \&repireforum,
    'locktop'		   =>	 \&locktop,
    'unlocktop'		   =>	 \&unlocktop,
    'catlocktop'           =>    \&catlocktop,
    'catunlocktop'         =>    \&catunlocktop,
    'abslocktop'	   =>	 \&abslocktop,
    'absunlocktop'	   =>	 \&absunlocktop,
    'highlight' 	   =>    \&highlight,
    'lowlight'  	   =>    \&lowlight,
);

if ($Mode{$action}) { $Mode{$action}->(); } else { &error("æ™®é€šé”™è¯¯&è¯·ä»¥æ­£ç¡®çš„æ–¹å¼è®¿é—®æœ¬ç¨‹åº"); }

for(my $iii=0;$iii<=4;$iii++) {
    my $jjj = $iii * $maxthreads;
    unlink ("${lbdir}cache/plcache$inforum\_$jjj.pl");
}

&output($boardname,\$output);
exit;

sub lockthread {
	my $intopics = $intopic;
	my @intopic = split(/ +/, $intopics);
	my $lockcount = @intopic;
	&error("ä¸»é¢˜é”å®š&è¯·å…ˆé€‰æ‹©éœ€è¦é”å®šçš„ä¸»é¢˜ï¼") if ($lockcount <= 0);
    &mischeader("ä¸»é¢˜é”å®š");

    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }

    if (($arrowuserdel eq "on")&&($cleartoedit ne "yes")) {
        open (ENT, "${lbdir}forum$inforum/$intopic.pl");
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/,$in);
        if ((lc($inmembername) eq lc($startedby)) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("ä¸»é¢˜é”å®š&æ‚¨ä¸æ˜¯æœ¬è®ºå›å›ä¸»æˆ–ç‰ˆä¸»ï¼Œæˆ–è€…æ‚¨çš„å¯†ç é”™è¯¯ï¼"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
	my $lockreason = $query->param("lockreason");
	$lockreason = &cleaninput($lockreason);
	$lockreason = &lbhz($lockreason, 60);
	$lockreason = "ï¼Œç†ç”±æ˜¯ï¼š$lockreason" if ($lockreason ne "");

      foreach $intopic (@intopic) {
	my $filetomake = "${lbdir}forum$inforum/$intopic.pl";
	unless (-e $filetomake) {
	    $lockcount--;
	    next;
	}

        open (ENT, "${lbdir}forum$inforum/$intopic.pl");
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $inposticon, $inposttemp, $addmetemp) = split(/\t/,$in);
        if (($threadstate eq "poll")||($threadstate eq "pollclosed")) { $threadstate = "pollclosed"; } else { $threadstate = "closed"; }
        if (open(FILE, ">${lbdir}forum$inforum/$intopic.pl")) {
            print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }
        $topictitle =~ s/^ï¼Šï¼ƒï¼ï¼†ï¼Š//;
        &sendtoposter("$inmembername","$startedby","","lock","$inforum","$intopic", "$topictitle","$lockreason") if (($sendmanageinfo eq "yes")&&(lc($inmembername) ne lc($startedby)));
      }

		if ($lockcount == 1)
		{
			&addadminlog("é”å®šè´´å­$lockreason", $intopic);
		}
		else
		{
			&addadminlog("æ‰¹é‡é”å®šè´´å­ $lockcount ç¯‡$lockreason");
		}

        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ä¸»é¢˜é”å®šæˆåŠŸï¼šå…±é”å®š <font color=$fonthighlight>$lockcount</font> ç¯‡ä¸»é¢˜ã€‚</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
å…·ä½“æƒ…å†µï¼š<ul><li><a href="forums.cgi?forum=$inforum">è¿”å›è®ºå›</a><li><a href="leobbs.cgi">è¿”å›è®ºå›é¦–é¡µ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="lock">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·åã€å¯†ç è¿›å…¥ç‰ˆä¸»æ¨¡å¼ [é”å®š $lockcount ä¸ªä¸»é¢˜]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>æ‚¨ç›®å‰çš„èº«ä»½æ˜¯ï¼š <font color=$fonthighlight><B><u>$inmembername</u></B></font> ï¼Œè¦ä½¿ç”¨å…¶ä»–ç”¨æˆ·èº«ä»½ï¼Œè¯·è¾“å…¥ç”¨æˆ·åå’Œå¯†ç ã€‚æœªæ³¨å†Œå®¢äººè¯·è¾“å…¥ç½‘åï¼Œå¯†ç ç•™ç©ºã€‚</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·å</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">æ‚¨æ²¡æœ‰æ³¨å†Œï¼Ÿ</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„å¯†ç </font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">å¿˜è®°å¯†ç ï¼Ÿ</a></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥é”å®šç†ç”±</font></td><td bgcolor=$miscbackone><input type=text name=lockreason size=60> ï¼ˆå¯ä¸å¡«ï¼‰</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ç™» å½•"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub unlockthread {
    &mischeader("ä¸»é¢˜è§£é”");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit  = "yes"; }
    if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("ä¸»é¢˜è§£é”&æ‚¨ä¸æ˜¯æœ¬è®ºå›å›ä¸»æˆ–ç‰ˆä¸»ï¼Œæˆ–è€…æ‚¨çš„å¯†ç é”™è¯¯ï¼"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$inforum/$intopic.pl";
        open (ENT, $file);
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$inposticon, $inposttemp,$addmetemp) = split(/\t/,$in);
 	$topictitle =~ s/^ï¼Šï¼ƒï¼ï¼†ï¼Š//;

        if (($threadstate eq "pollclosed")||($threadstate eq "poll")) { $threadstate = "poll"; } else { $threadstate = "open"; }
        if (open(FILE, ">$file")) {
            print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }

	&addadminlog("è´´å­è§£é”", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ä¸»é¢˜è§£é”æˆåŠŸ</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
å…·ä½“æƒ…å†µï¼š<ul><li><a href="forums.cgi?forum=$inforum">è¿”å›è®ºå›</a><li><a href="leobbs.cgi">è¿”å›è®ºå›é¦–é¡µ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="unlock">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·åã€å¯†ç è¿›å…¥ç‰ˆä¸»æ¨¡å¼ [ä¸»é¢˜è§£é”]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>æ‚¨ç›®å‰çš„èº«ä»½æ˜¯ï¼š <font color=$fonthighlight><B><u>$inmembername</u></B></font> ï¼Œè¦ä½¿ç”¨å…¶ä»–ç”¨æˆ·èº«ä»½ï¼Œè¯·è¾“å…¥ç”¨æˆ·åå’Œå¯†ç ã€‚æœªæ³¨å†Œå®¢äººè¯·è¾“å…¥ç½‘åï¼Œå¯†ç ç•™ç©ºã€‚</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·å</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">æ‚¨æ²¡æœ‰æ³¨å†Œï¼Ÿ</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„å¯†ç </font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">å¿˜è®°å¯†ç ï¼Ÿ</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ç™» å½•"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub repireforum {
    &mischeader("è®ºå›ä¿®å¤");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("è®ºå›ä¿®å¤&æ‚¨ä¸æ˜¯æœ¬è®ºå›å›ä¸»æˆ–æ­£ç‰ˆä¸»ï¼Œæˆ–è€…æ‚¨çš„å¯†ç é”™è¯¯ï¼"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	require "rebuildlist.pl";
        my $truenumber = rebuildLIST(-Forum=>"$inforum");
        ($tpost,$treply) = split (/\|/,$truenumber);
        
            open(FILE, "${lbdir}boarddata/listno$inforum.cgi");
            $topicid = <FILE>;
            close(FILE);
            chomp $topicid;
	    my $rr = &readthreadpl($forumid,$topicid);
	    (my $lastpostdate, my $topicid, my $topictitle, my $topicdescription, my $threadstate, my $threadposts, my $threadviews, my $startedby, my $startedpostdate, my $lastposter, my $posticon, my $posttemp) = split (/\t/,$rr);

            open(FILE, "+<${lbdir}boarddata/foruminfo$inforum.cgi");
            ($no, $no, $no, $todayforumpost, $no) = split(/\t/,<FILE>);
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
	    seek(FILE,0,0);
            print FILE "$lastforumpostdate\t$tpost\t$treply\t$todayforumpost\t$lastposter\t\n";
            close(FILE);
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $tpost;\n\$posts = $treply;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);

	&addadminlog("ä¿®å¤è®ºå›");
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>è®ºå›ä¿®å¤æˆåŠŸ</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
å…·ä½“æƒ…å†µï¼š<ul><li><a href="forums.cgi?forum=$inforum">è¿”å›è®ºå›</a><li><a href="leobbs.cgi">è¿”å›è®ºå›é¦–é¡µ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="repireforum">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·åã€å¯†ç è¿›å…¥ç‰ˆä¸»æ¨¡å¼ [è®ºå›ä¿®å¤]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>æ‚¨ç›®å‰çš„èº«ä»½æ˜¯ï¼š <font color=$fonthighlight><B><u>$inmembername</u></B></font> ï¼Œè¦ä½¿ç”¨å…¶ä»–ç”¨æˆ·èº«ä»½ï¼Œè¯·è¾“å…¥ç”¨æˆ·åå’Œå¯†ç ã€‚æœªæ³¨å†Œå®¢äººè¯·è¾“å…¥ç½‘åï¼Œå¯†ç ç•™ç©ºã€‚</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·å</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">æ‚¨æ²¡æœ‰æ³¨å†Œï¼Ÿ</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„å¯†ç </font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">å¿˜è®°å¯†ç ï¼Ÿ</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ç™» å½•"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub puttop {
    &mischeader("ä¸»é¢˜æå‡");

    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit  = "yes"; }
    if (($inmembmod eq "yes")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("ä¸»é¢˜æå‡&æ‚¨ä¸æ˜¯æœ¬è®ºå›å›ä¸»æˆ–ç‰ˆä¸»ï¼Œæˆ–è€…æ‚¨çš„å¯†ç é”™è¯¯ï¼"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$inforum/$intopic.pl";
        open (ENT, $file);
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$inposticon,$inposttemp,$addmetemp) = split(/\t/,$in);

        if (open(FILE, ">$file")) {
            print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$currenttime\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }
 	$topictitle =~ s/^ï¼Šï¼ƒï¼ï¼†ï¼Š//;

        $file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
	sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
        $listall =~ s/\r//isg;

	$listall =~ s/(^|\n)$intopic\n/$1/isg;

        if (open (LIST, ">$file")) {
	    flock (LIST, 2) if ($OS_USED eq "Unix");
            print LIST "$intopic\n$listall";
            close (LIST);
        }
        &winunlock($file) if ($OS_USED eq "Nt");


            open(FILE, "+<${lbdir}boarddata/foruminfo$inforum.cgi");
            ($no, $posts, $replys, $todayforumpost, $no) = split(/\t/,<FILE>);
            $lastforumpostdate = "$lastpostdate\%\%\%$topicid\%\%\%$topictitle";
	    $lastposter = $startedby if ($lastposter eq "");
	    seek(FILE,0,0);
            print FILE "$lastforumpostdate\t$posts\t$replys\t$todayforumpost\t$lastposter\t\n";
	    close(FILE);
	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $posts;\n\$posts = $replys;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);


	&addadminlog("æå‡ä¸»é¢˜ä½ç½®", $intopic);
       $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ä¸»é¢˜æå‡æˆåŠŸ</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
å…·ä½“æƒ…å†µï¼š<ul><li><a href="forums.cgi?forum=$inforum">è¿”å›è®ºå›</a><li><a href="leobbs.cgi">è¿”å›è®ºå›é¦–é¡µ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="puttop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·åã€å¯†ç è¿›å…¥ç‰ˆä¸»æ¨¡å¼ [ä¸»é¢˜æå‡]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>æ‚¨ç›®å‰çš„èº«ä»½æ˜¯ï¼š <font color=$fonthighlight><B><u>$inmembername</u></B></font> ï¼Œè¦ä½¿ç”¨å…¶ä»–ç”¨æˆ·èº«ä»½ï¼Œè¯·è¾“å…¥ç”¨æˆ·åå’Œå¯†ç ã€‚æœªæ³¨å†Œå®¢äººè¯·è¾“å…¥ç½‘åï¼Œå¯†ç ç•™ç©ºã€‚</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·å</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">æ‚¨æ²¡æœ‰æ³¨å†Œï¼Ÿ</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„å¯†ç </font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">å¿˜è®°å¯†ç ï¼Ÿ</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ç™» å½•"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub putdown {
    &mischeader("ä¸»é¢˜æ²‰åº•");

    $cleartoedit = "no";
    if (($membercode eq "ad")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if (($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit  = "yes"; }
    if (($inmembmod eq "yes")  && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("ä¸»é¢˜æ²‰åº•&æ‚¨ä¸æ˜¯æœ¬è®ºå›å›ä¸»æˆ–ç‰ˆä¸»ï¼Œæˆ–è€…æ‚¨çš„å¯†ç é”™è¯¯ï¼"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
        my $file = "${lbdir}forum$inforum/$intopic.pl";
        open (ENT, $file);
        $in = <ENT>;
        close (ENT);
        chomp $in;
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate,$inposticon,$inposttemp,$addmetemp) = split(/\t/,$in);
	$lastpostdate = $lastpostdate - 3600 * 24 * 365; # æ—¶é—´æå‰ 1 å¹´
        
        if (open(FILE, ">$file")) {
            print FILE "$intopic\t$topictitle\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$lastposter\t$lastpostdate\t$inposticon\t$inposttemp\t$addmetemp\t";
            close(FILE);
        }
 	$topictitle =~ s/^ï¼Šï¼ƒï¼ï¼†ï¼Š//;

        $file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
	flock (LIST, 1) if ($OS_USED eq "Unix");
	sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
        $listall =~ s/\r//isg;

	$listall =~ s/(^|\n)$intopic\n/$1/isg;

        if (open (LIST, ">$file")) {
	    flock (LIST, 2) if ($OS_USED eq "Unix");
            print LIST "$listall$intopic\n";
            close (LIST);
        }
        &winunlock($file) if ($OS_USED eq "Nt");

	&addadminlog("ä¸»é¢˜ä½ç½®æ²‰åº•", $intopic);
       $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ä¸»é¢˜æ²‰åº•æˆåŠŸ</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
å…·ä½“æƒ…å†µï¼š<ul><li><a href="forums.cgi?forum=$inforum">è¿”å›è®ºå›</a><li><a href="leobbs.cgi">è¿”å›è®ºå›é¦–é¡µ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="putdown">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·åã€å¯†ç è¿›å…¥ç‰ˆä¸»æ¨¡å¼ [ä¸»é¢˜æ²‰åº•]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>æ‚¨ç›®å‰çš„èº«ä»½æ˜¯ï¼š <font color=$fonthighlight><B><u>$inmembername</u></B></font> ï¼Œè¦ä½¿ç”¨å…¶ä»–ç”¨æˆ·èº«ä»½ï¼Œè¯·è¾“å…¥ç”¨æˆ·åå’Œå¯†ç ã€‚æœªæ³¨å†Œå®¢äººè¯·è¾“å…¥ç½‘åï¼Œå¯†ç ç•™ç©ºã€‚</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·å</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">æ‚¨æ²¡æœ‰æ³¨å†Œï¼Ÿ</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„å¯†ç </font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">å¿˜è®°å¯†ç ï¼Ÿ</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ç™» å½•"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub locktop {
    &mischeader("ä¸»é¢˜å›ºå®š");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    if(($membercode eq 'smo') && ($inpassword eq $password)) { $cleartoedit = "yes";}
    if (($inmembmod eq "yes") && ($membercode ne 'amo') && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }

    if ($cleartoedit eq "no" && $checked eq "yes") { &error("ä¸»é¢˜å›ºå®šé¦–è¡Œ&æ‚¨ä¸æ˜¯æœ¬è®ºå›å›ä¸»æˆ–æ­£ç‰ˆä¸»ï¼Œæˆ–è€…æ‚¨çš„å¯†ç é”™è¯¯ï¼"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	unlink("${lbdir}cache/forumstop$inforum.pl");
        my $file = "$lbdir" . "boarddata/ontop$inforum.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$intopic\n";
	        $putno = 1;
	        foreach (@toptopic) {
	            chomp $_;
	            if (($_ ne $intopic)&&(-e "${lbdir}forum$inforum/$_.thd.cgi")) {
	    	        print TOPFILE "$_\n";
	    	        $putno ++;
	            }
	            last if ($putno eq $maxtoptopic);
	        }
                close (TOPFILE);
            }
        } else {
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$intopic\n";
                close (TOPFILE);
            }
        }
	&addadminlog("å›ºé¡¶è´´å­", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ä¸»é¢˜å›ºå®šé¦–è¡ŒæˆåŠŸ</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
å…·ä½“æƒ…å†µï¼š<ul><li><a href="forums.cgi?forum=$inforum">è¿”å›è®ºå›</a><li><a href="leobbs.cgi">è¿”å›è®ºå›é¦–é¡µ</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        if (open (TOPFILE, "${lbdir}boarddata/ontop$inforum.cgi")) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
	}
	$toptopic = 0;
	        foreach (@toptopic) {
	            chomp $_;
	            if (-e "${lbdir}forum$inforum/$_.thd.cgi") {
	    	        $toptopic ++;
	            }
	        }
	if ($toptopic >= $maxtoptopic) { $topnum = "<BR><B><font color=$fonthighlight>å·²ç»å›ºå®šäº† $toptopic ä¸ªå¸–å­äº†ï¼Œå¦‚æœç»§ç»­ï¼Œæœ€æ—©ä¸€ä¸ªè¢«å›ºå®šçš„å¸–å­å°†è¢«è‡ªåŠ¨å–æ¶ˆå›ºå®šã€‚</B></font>" } else { $topnum = "<BR><B><font color=$fonthighlight>å·²ç»å›ºå®šäº† $toptopic ä¸ªå¸–å­äº†ï¼Œä½ æœ€å¤šå¯ä»¥å›ºå®š $maxtoptopic ä¸ªå¸–å­ã€‚</B></font>"; }
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="locktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·åã€å¯†ç è¿›å…¥ç‰ˆä¸»æ¨¡å¼ [ä¸»é¢˜å›ºå®šé¦–è¡Œ]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>æ‚¨ç›®å‰çš„èº«ä»½æ˜¯ï¼š <font color=$fonthighlight><B><u>$inmembername</u></B></font> ï¼Œè¦ä½¿ç”¨å…¶ä»–ç”¨æˆ·èº«ä»½ï¼Œè¯·è¾“å…¥ç”¨æˆ·åå’Œå¯†ç ã€‚æœªæ³¨å†Œå®¢äººè¯·è¾“å…¥ç½‘åï¼Œå¯†ç ç•™ç©ºã€‚</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„ç”¨æˆ·å</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">æ‚¨æ²¡æœ‰æ³¨å†Œï¼Ÿ</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>è¯·è¾“å…¥æ‚¨çš„å¯†ç </font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">å¿˜è®°å¯†ç ï¼Ÿ</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="ç™» å½•"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub unlocktop {
    &mischeader("ä¸»é¢˜å–æ¶ˆå›ºå®š");

    $cleartoedit = "no";
    if (($membercodtd bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>le cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>Ö÷ÌâÈ¡Ïû¹Ì¶¨³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
¾ßÌåÇé¿ö£º<ul><li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="unlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>ÇëÊäÈëÄúµÄÓÃ»§Ãû¡¢ÃÜÂë½øÈë°æÖ÷Ä£Ê½ [Ö÷ÌâÈ¡Ïû¹Ì¶¨]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="µÇ Â¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}

sub abslocktop {
    &mischeader("Ö÷Ìâ×Ü¹Ì¶¨Ê×ĞĞ");
    if (($startnewthreads eq "no")||($startnewthreads eq "cert")||($privateforum eq "yes")) { &error("Ö÷Ìâ×Ü¹Ì¶¨Ê×ĞĞ&¶Ô²»Æğ£¬Õâ¸ö·ÖÂÛÌ³²¢²»ÊÇ¶ÔËùÓĞÓÃ»§¿ª·ÅµÄ£¬ËùÒÔ²»ÄÜ×Ü¹Ì¶¨Ìû×Ó£¡"); }
    $absmaxtoptopic = 3 if ($absmaxtoptopic <=0);
    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("Ö÷Ìâ×Ü¹Ì¶¨Ê×ĞĞ&Äú²»ÊÇ±¾ÂÛÌ³Ì³Ö÷£¬»òÕßÄúµÄÃÜÂë´íÎó£¡"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	opendir (CATDIR, "${lbdir}cache");
	my @dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^forumstop/,@dirdata);
	foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
        my $file = "$lbdir" . "boarddata/absontop.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$inforum\|$intopic\n";
	        $putno = 1;
	        foreach (@toptopic) {
	            chomp $_;
                    next if ($_ eq "");
	            ($tempinforum,$tempintopic) = split (/\|/,$_);
	            unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
	            	if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
	    	            print TOPFILE "$_\n";
	    	            $putno ++;
	    	        }
	            }
	            last if ($putno eq $absmaxtoptopic);
	        }
                close (TOPFILE);
            }
        } else {
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$inforum\|$intopic\n";
                close (TOPFILE);
            }
        }
	&addadminlog("×Ü¹Ì¶¥Ìû×Ó", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>Ö÷Ìâ×Ü¹Ì¶¨Ê×ĞĞ³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
¾ßÌåÇé¿ö£º<ul><li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        if (open (TOPFILE, "${lbdir}boarddata/absontop.cgi")) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
        }
        $toptopic = 0;
	        foreach (@toptopic) {
	            chomp $_;
                    next if ($_ eq "");
	            ($tempinforum,$tempintopic) = split (/\|/,$_);
	            	if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
	    	            $toptopic ++;
	    	        }
	        }
	if ($toptopic >= $absmaxtoptopic) { $topnum = "<BR><B><font color=$fonthighlight>ÒÑ¾­×Ü¹Ì¶¨ÁË $toptopic ¸öÌû×ÓÁË£¬Èç¹û¼ÌĞø£¬×îÔçÒ»¸ö±»¹Ì¶¨µÄÌû×Ó½«±»×Ô¶¯È¡Ïû¹Ì¶¨¡£</B></font>" } else { $topnum = "<BR><B><font color=$fonthighlight>ÒÑ¾­×Ü¹Ì¶¨ÁË $toptopic ¸öÌû×ÓÁË£¬Äã×î¶à¿ÉÒÔ×Ü¹Ì¶¨ $absmaxtoptopic ¸öÌû×Ó¡£</B></font>"; }
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="abslocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>ÇëÊäÈëÄúµÄÓÃ»§Ãû¡¢ÃÜÂë½øÈë°æÖ÷Ä£Ê½ [Ö÷Ìâ×Ü¹Ì¶¨Ê×ĞĞ]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="µÇ Â¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub absunlocktop {
    &mischeader("Ö÷ÌâÈ¡Ïû×Ü¹Ì¶¨");

    $cleartoedit = "no";
    if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("Ö÷ÌâÈ¡Ïû×Ü¹Ì¶¨&Äú²»ÊÇ±¾ÂÛÌ³Ì³Ö÷£¬»òÕßÄúµÄÃÜÂë´íÎó£¡"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	opendir (CATDIR, "${lbdir}cache");
	my @dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^forumstop/,@dirdata);
	foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
        my $file = "${lbdir}boarddata/absontop.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);

            if (open (TOPFILE, ">$file")) {
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
	            my ($tempinforum,$tempintopic) = split (/\|/,$_);
	            unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
	            	if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
	    	            print TOPFILE "$_\n";
	    	        }
	            }
	        }
                close (TOPFILE);
            }
        }
	&addadminlog("È¡ÏûÌù×Ó×Ü¹Ì¶¥", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>Ö÷ÌâÈ¡Ïû×Ü¹Ì¶¨³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
¾ßÌåÇé¿ö£º<ul><li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="absunlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>ÇëÊäÈëÄúµÄÓÃ»§Ãû¡¢ÃÜÂë½øÈë°æÖ÷Ä£Ê½ [Ö÷ÌâÈ¡Ïû×Ü¹Ì¶¨]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="µÇ Â¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}
sub highlight {
  &mischeader("¼ÓÖØÌû×Ó±êÌâ");
  $maxhightopic = 8 if ($maxhightopic <=0);

  $cleartoedit = "no";
  if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
  if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
  if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
  unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
  if ($cleartoedit eq "no" && $checked eq "yes") { &error("¼ÓÖØÌû×Ó±êÌâ&Äú²»ÊÇ±¾ÂÛÌ³Ì³Ö÷»ò°æÖ÷£¬»òÕßÄúµÄÃÜÂë´íÎó£¡"); }
  if (($cleartoedit eq "yes") && ($checked eq "yes")) {
      unlink("${lbdir}cache/forumstop$inforum.pl");
      my $file = "$lbdir" . "boarddata/highlight$inforum.cgi";
      if (open (HIGHFILE, $file)) {
          @hightopic = <HIGHFILE>;
          close (HIGHFILE);
          if (open (HIGHFILE, ">$file")) {
              print HIGHFILE "$inforum\-$intopic\n";
              $putno = 1;
      foreach (@hightopic) {
          chomp $_;
          next if ($_ eq "");
          ($tempinforum,$tempintopic) = split (/\-/,$_);
          chomp $tempintopic;chomp $tempinforum;
          unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
              if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
          	  print HIGHFILE "$_\n";
          	  $putno ++;
              }
          }
          last if ($putno eq $maxhightopic);
      }
              close (HIGHFILE);
          }
      } else {
          if (open (HIGHFILE, ">$file")) {
              print HIGHFILE "$inforum\-$intopic\n";
              close (HIGHFILE);
          }
      }
      &addadminlog("¼ÓÖØÌû×Ó±êÌâ", $intopic);
      $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>¼ÓÖØÌû×Ó±êÌâ³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
¾ßÌåÇé¿ö£º<ul><li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
  } else {
        if (open (TOPFILE, "${lbdir}boarddata/highlight$inforum.cgi")) {
            @hightopic = <TOPFILE>;
            close (TOPFILE);
        }
        $toptopic = 0;
	        foreach (@hightopic) {
	            chomp $_;
                    next if ($_ eq "");
	            ($tempinforum,$tempintopic) = split (/\-/,$_);
	            	if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
	    	            $toptopic ++;
	    	        }
	        }
	if ($toptopic >= $maxhightopic) { $topnum = "<BR><B><font color=$fonthighlight>ÒÑ¾­¼ÓÖØÁË $toptopic ¸öÌû×Ó±êÌâÁË£¬Èç¹û¼ÌĞø£¬×îÔçÒ»¸ö±»¼ÓÖØ±êÌâ½«±»×Ô¶¯È¡Ïû¼ÓÖØ±êÌâ¡£</B></font>" } else { $topnum = "<BR><B><font color=$fonthighlight>ÒÑ¾­¼ÓÖØÁË $toptopic ¸öÌû×Ó±êÌâÁË£¬Äã×î¶à¿ÉÒÔ¼ÓÖØ $maxhightopic ¸öÌû×Ó±êÌâ¡£</B></font>"; }
      $inmembername =~ s/\_/ /g;
      $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="highlight">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>ÇëÊäÈëÄúµÄÓÃ»§Ãû¡¢ÃÜÂë½øÈë°æÖ÷Ä£Ê½ [¼ÓÖØÌû×Ó±êÌâ]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="µÇ Â¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

  }
}

sub lowlight {
  &mischeader("Ìû×Ó±êÌâÈ¡Ïû¼ÓÖØ");

  $cleartoedit = "no";
  if (($membercode eq "ad") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
  if(($membercode eq 'smo') && ($inpassword eq $password)) {$cleartoedit = "yes";}
  if (($inmembmod eq "yes") && ($inpassword eq $password)) { $cleartoedit = "yes"; }
  unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
  if ($cleartoedit eq "no" && $checked eq "yes") { &error("Ìû×Ó±êÌâÈ¡Ïû¼ÓÖØ&Äú²»ÊÇ±¾ÂÛÌ³Ì³Ö÷»ò°æÖ÷£¬»òÕßÄúµÄÃÜÂë´íÎó£¡"); }

  if (($cleartoedit eq "yes") && ($checked eq "yes")) {
      unlink("${lbdir}cache/forumstop$inforum.pl");
      my $file = "${lbdir}boarddata/highlight$inforum.cgi";
      if (open (HIGHPFILE, $file)) {
          @hightopic = <HIGHPFILE>;
          close (HIGHPFILE);

          if (open (HIGHPFILE, ">$file")) {
              foreach (@hightopic) {
                  chomp $_;
                  next if ($_ eq "");
          my ($tempinforum,$tempintopic) = split (/\-/,$_);
          unless (($tempinforum eq $inforum)&&($tempintopic eq $intopic)) {
              if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
          	  print HIGHPFILE "$_\n";
              }
          }
      }
              close (HIGHPFILE);
          }
      }
      &addadminlog("Ìû×Ó±êÌâÈ¡Ïû¼ÓÖØ", $intopic);
      $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>Ìû×Ó±êÌâÈ¡Ïû¼ÓÖØ³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
¾ßÌåÇé¿ö£º<ul><li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
  } else {
      $inmembername =~ s/\_/ /g;
      $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="lowlight">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>ÇëÊäÈëÄúµÄÓÃ»§Ãû¡¢ÃÜÂë½øÈë°æÖ÷Ä£Ê½ [Ìû×Ó±êÌâÈ¡Ïû¼ÓÖØ]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="µÇ Â¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
  }
} 

sub catlocktop {
    &mischeader("Ö÷ÌâÇø¹Ì¶¨Ê×ĞĞ");
    if (($startnewthreads eq "no")||($startnewthreads eq "cert")||($privateforum eq "yes")) { &error("Ö÷ÌâÇø¹Ì¶¨Ê×ĞĞ&¶Ô²»Æğ£¬Õâ¸ö·ÖÂÛÌ³²¢²»ÊÇ¶ÔËùÓĞÓÃ»§¿ª·ÅµÄ£¬ËùÒÔ²»ÄÜÇø¹Ì¶¨Ìû×Ó£¡"); }
    $absmaxcantopic = 3 if ($absmaxcantopic <= 0);
    $cleartoedit = "no";
    if (($membercode eq "ad" || $membercode eq "smo" || ",$catemods," =~ /\Q\,$inmembername\,\E/i) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("Ö÷ÌâÇø¹Ì¶¨Ê×ĞĞ&Äú²»ÊÇ±¾·ÖÇø¹ÜÀíÔ±£¬»òÕßÄúµÄÃÜÂë´íÎó£¡"); }
    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	opendir (CATDIR, "${lbdir}cache");
	my @dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^forumstop/,@dirdata);
	foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }

        my $file = "${lbdir}boarddata/catontop$categoryplace.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$inforum\|$intopic\n";
                $putno = 1;
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
                    ($tempinforum,$tempintopic) = split (/\|/,$_);
                    unless (($tempinforum eq $inforum && $tempintopic eq $intopic) || !(-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi")) {
                            print TOPFILE "$_\n";
                            $putno ++;
                    }
                    last if ($putno eq $absmaxcantopic);
                }
                close (TOPFILE);
            }
        } else {
            if (open (TOPFILE, ">$file")) {
                print TOPFILE "$inforum\|$intopic\n";
                close (TOPFILE);
            }
        }
	&addadminlog("Çø¹Ì¶¥Ìû×Ó", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>Ö÷ÌâÇø¹Ì¶¨Ê×ĞĞ³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
¾ßÌåÇé¿ö£º<ul><li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        if (open (TOPFILE, "${lbdir}boarddata/catontop$categoryplace.cgi")) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);
        }
        $toptopic = 0;
                foreach (@toptopic) {
                    chomp $_;
                    next if ($_ eq "");
                    ($tempinforum,$tempintopic) = split (/\|/,$_);
                    if (-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi") {
                            $toptopic ++;
                    }
                }
        if ($toptopic >= $absmaxcantopic) { $topnum = "<BR><B><font color=$fonthighlight>ÒÑ¾­Çø¹Ì¶¨ÁË $toptopic ¸öÌû×ÓÁË£¬Èç¹û¼ÌĞø£¬×îÔçÒ»¸ö±»¹Ì¶¨µÄÌû×Ó½«±»×Ô¶¯È¡Ïû¹Ì¶¨¡£</B></font>" } else { $topnum = "<BR><B><font color=$fonthighlight>ÒÑ¾­Çø¹Ì¶¨ÁË $toptopic ¸öÌû×ÓÁË£¬Äã×î¶à¿ÉÒÔÇø¹Ì¶¨ $absmaxcantopic ¸öÌû×Ó¡£</B></font>"; }
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="catlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>ÇëÊäÈëÄúµÄÓÃ»§Ãû¡¢ÃÜÂë½øÈë°æÖ÷Ä£Ê½ [Ö÷ÌâÇø¹Ì¶¨Ê×ĞĞ]</b></font>$topnum</td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="µÇ Â¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;

    }
}

sub catunlocktop {
    &mischeader("Ö÷ÌâÈ¡ÏûÇø¹Ì¶¨");

    $cleartoedit = "no";
    if (($membercode eq "ad" || $membercode eq "smo" || ",$catemods," =~ /\Q\,$inmembername\,\E/i) && ($inpassword eq $password)) { $cleartoedit = "yes"; }
    unless ($cleartoedit eq "yes") { $cleartoedit = "no"; }
    if ($cleartoedit eq "no" && $checked eq "yes") { &error("Ö÷ÌâÈ¡ÏûÇø¹Ì¶¨&Äú²»ÊÇ±¾·ÖÇø¹ÜÀíÔ±£¬»òÕßÄúµÄÃÜÂë´íÎó£¡"); }

    if (($cleartoedit eq "yes") && ($checked eq "yes")) {
    	opendir (CATDIR, "${lbdir}cache");
	my @dirdata = readdir(CATDIR);
	closedir (CATDIR);
	@dirdata = grep(/^forumstop/,@dirdata);
	foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
        my $file = "${lbdir}boarddata/catontop$categoryplace.cgi";
        if (open (TOPFILE, $file)) {
            @toptopic = <TOPFILE>;
            close (TOPFILE);

            if (open (TOPFILE, ">$file")) {
                foreach (@toptopic) {
                    chomp;
                    next if ($_ eq "");
                    my ($tempinforum,$tempintopic) = split (/\|/,$_);
                    unless (($tempinforum eq $inforum && $tempintopic eq $intopic) || !(-e "${lbdir}forum$tempinforum/$tempintopic.thd.cgi")) {
                            print TOPFILE "$_\n";
                    }
                }
                close (TOPFILE);
            }
        }
	&addadminlog("È¡ÏûÌû×ÓÇø¹Ì¶¥", $intopic);
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>Ö÷ÌâÈ¡ÏûÇø¹Ì¶¨³É¹¦</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>
¾ßÌåÇé¿ö£º<ul><li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a><li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a></ul></tr></td>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=forums.cgi?forum=$inforum">
~;
    } else {
        $inmembername =~ s/\_/ /g;
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic colspan=2 align=center>
<form action="$thisprog" method="post">
<input type=hidden name="action" value="catunlocktop">
<input type=hidden name="checked" value="yes">
<input type=hidden name="forum" value="$inforum">
<input type=hidden name="topic" value="$intopic">
<font color=$fontcolormisc><b>ÇëÊäÈëÄúµÄÓÃ»§Ãû¡¢ÃÜÂë½øÈë°æÖ÷Ä£Ê½ [Ö÷ÌâÈ¡ÏûÇø¹Ì¶¨]</b></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2><font color=$titlefontcolor>ÄúÄ¿Ç°µÄÉí·İÊÇ£º <font color=$fonthighlight><B><u>$inmembername</u></B></font> £¬ÒªÊ¹ÓÃÆäËûÓÃ»§Éí·İ£¬ÇëÊäÈëÓÃ»§ÃûºÍÃÜÂë¡£Î´×¢²á¿ÍÈËÇëÊäÈëÍøÃû£¬ÃÜÂëÁô¿Õ¡£</td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÓÃ»§Ãû</font></td><td bgcolor=$miscbackone><input type=text name="membername"> &nbsp; <font color=$fontcolormisc><span onclick="javascript:location.href='register.cgi?forum=$inforum'" style="cursor:hand">ÄúÃ»ÓĞ×¢²á£¿</span></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>ÇëÊäÈëÄúµÄÃÜÂë</font></td><td bgcolor=$miscbackone><input type=password name="password"> &nbsp; <font color=$fontcolormisc><a href="profile.cgi?action=lostpass" style="cursor:help">Íü¼ÇÃÜÂë£¿</a></font></td></tr>
<tr><td bgcolor=$miscbacktwo colspan=2 align=center><input type=submit name="submit" value="µÇ Â¼"></td></form></tr></table></td></tr></table>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
~;
    }
}
