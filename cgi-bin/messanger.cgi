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
$LBCGI::POST_MAX = 1000000;
$LBCGI::DISABLE_UPLOADS = 0;
$LBCGI::HEADERS_ONCE = 1;
require "code.cgi";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "bbs.lib.pl";

$|++;
$thisprog = "messanger.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
#&ipbanned;

&error("çŸ­æ¶ˆæ¯ç¦æ­¢ä½¿ç”¨&å¾ˆæŠ±æ­‰ï¼Œå›ä¸»ç”±äºæŸç§åŸå› å·²ç¦æ­¢æ‰€æœ‰ç”¨æˆ·ä½¿ç”¨çŸ­æ¶ˆæ¯åŠŸèƒ½&msg") if ($allowusemsg eq "off");

$action = $query->param("action");

$actionto = $query->param("actionto");

$inwhere = $query->param("where");
$inmsg = $query->param("msg");
$inmembername = $query->cookie("amembernamecookie");
$inpassword = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$inselectstyle  = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) {require "${lbdir}data/skin/${inselectstyle}.cgi";}
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($action eq "send" || $action eq "new")
{
	$intouser = $query->param("touser");
	$intouser =~ s/\; /\;/ig;
	$intouser =~ s/ \;/\;/ig;
	$intouser =~ s/\;$//ig;
	$intouser =~ s/^\;//ig;
	$intouser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\'\:\"\,\.\/\<\>\?]//isg;
	$inmsgtitle = $query->param("msgtitle");
	$inmessage = $query->param("message");
	$inmessage = &cleaninput($inmessage);
	$inmsgtitle = &cleaninput($inmsgtitle);
}
&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if ($inmembername =~  m/\// || $inmembername =~ m/\\/ || $inmembername =~ m/\.\./);
&error("æ™®é€šé”™è¯¯&è¯·ä¸è¦ä¿®æ”¹ç”Ÿæˆçš„ URLï¼") if ($inmsg =~ /[^0-9]/);

if ($inmembername eq "" || $inmembername eq "å®¢äºº")
{
	&error("æ™®é€šé”™è¯¯&ä½ è¿˜æ²¡ç™»å½•å‘¢ï¼Ÿè¯·å…ˆç™»å½•è®ºå›ï¼&msg");
}
else
{
	&getmember($inmembername,"no");
	&error("æ™®é€šé”™è¯¯&æ­¤ç”¨æˆ·æ ¹æœ¬ä¸å­˜åœ¨ï¼&msg") if ($userregistered eq "no");
	&error("æ™®é€šé”™è¯¯&å¯†ç ä¸ç”¨æˆ·åä¸ç›¸ç¬¦ï¼Œè¯·é‡æ–°ç™»å½•ï¼&msg") if ($inpassword ne $password);
}
&doonoff;  #è®ºå›å¼€æ”¾ä¸å¦

$msgmm = 0 if (($msgmm <= 0)||($msgmm eq ""));
$msgmneedmm = "off" if (($msgmm <= 0)||($msgmm eq ""));
$msgmneedmm = "off" if (($membercode eq "ad")||($membercode eq 'smo')||($membercode eq 'cmo')||($membercode eq "mo"));

$action = "inbox" if ($action eq "");
$memberfilename = $inmembername;
$memberfilename =~ s/ /\_/g;
$memberfilename =~ tr/A-Z/a-z/;

$output .= qq~<script language="JavaScript">
function bbimg(o){var zoom=parseInt(o.style.zoom,10)||100;zoom+=event.wheelDelta/12;if (zoom>0) o.style.zoom=zoom+'%';return false;}
function openscript(url, width, height)
{
	var Win = window.open(url, "openwindow", "width=" + width + ",height=" + height + ",resizable=1,scrollbars=yes,menubar=yes,status=yes");
}
function enable(btn)
{
	btn.filters.gray.enabled = 0;
}
function disable(btn)
{
	btn.filters.gray.enabled = 1;
}
</script>
<style>
.gray	{cursor: hand; filter:gray}
</style>~;

$inboxpm = qq~<img src=$imagesurl/images/inboxpm.gif border=0 alt="æ”¶ä»¶ç®±" width=40 height=40>~;
$outboxpm = qq~<img src=$imagesurl/images/outboxpm.gif border=0 alt="å‘ä»¶ç®±" width=40 height=40>~;
$newpm = qq~<img src=$imagesurl/images/newpm.gif border=0 alt="å‘é€æ¶ˆæ¯" width=40 height=40>~;
$replypm = qq~<img src=$imagesurl/images/replypm.gif border=0 alt="å›å¤æ¶ˆæ¯" width=40 height=40>~;
$fwpm = qq~<img src=$imagesurl/images/fwpm.gif border=0 alt="è½¬å‘æ¶ˆæ¯" width=40 height=40>~;
$deletepm = qq~<img src=$imagesurl/images/deletepm.gif border=0 alt="åˆ é™¤æ¶ˆæ¯" width=40 height=40>~;
$friendpm = qq~<img src=$imagesurl/images/friendpm.gif border=0 alt="æ‰“å¼€å¥½å‹å½•" width=40 height=40>~;
$blockpm = qq~<img src=$imagesurl/images/blockpm.gif border=0 alt="æ‰“å¼€é»‘åå•" width=40 height=40>~;

$output .= qq~
<p>
<SCRIPT>valigntop()</SCRIPT><table cellPadding=0 cellSpacing=0 border=0 width=$tablewidth bgColor=$tablebordercolor align=center><tr><td><table cellPadding=3 cellSpacing=1 border=0 width=100%>~;

if ($action eq "attach") {
	my $box = $query->param('box');
	my $filetoopen = $box eq 'out' ? "${lbdir}${msgdir}/out/${memberfilename}_out.cgi" : "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi";
	my $mestemp;
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	if (open(FILE, $filetoopen))
	{
        	flock (FILE, 1) if ($OS_USED eq "Unix");
		sysread(FILE, $mestemp, (stat(FILE))[7]);
		close(FILE);
		$mestemp =~ s/\r//isg;
	}
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
	my @boxmessages = split($/, $mestemp);
	my $msgtograb = $boxmessages[$inmsg];
	chomp($msgtograb);
	my ($from, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $msgtograb);
	&error("è¯»å–é™„ä»¶&æ¶ˆæ¯æ²¡æœ‰é™„ä»¶ï¼æˆ–æ­¤æ¶ˆæ¯å·²è¢«åˆ é™¤ï¼&msg") if ($attach eq '');

	my ($filename, $content) = split('ï¼Šï¼ƒï¼ï¼†ï¼Š', $attach);
	my $fileext = lc((split(/\./, $filename))[-1]);
	$content = &Base64decode($content);
	my $filesize = length($content);

	$fileext = 'jpeg' if ($fileext eq 'jpg');
	$fileext = 'html' if ($fileext eq 'htm');
	$fileext = 'plain' if ($fileext eq 'txt');
	print $fileext eq 'gif' || $fileext eq 'jpeg' || $fileext eq 'png' || $fileext eq 'bmp' ? header(-type=>"image/$fileext", -attachment=>$filename, -expires=>'0', -content_length=>$filesize) : $fileext eq 'swf' ? header(-type=>"application/x-shockwave-flash", -attachment=>$filename, -expires=>'0', -content_length=>$filesize) : $fileext eq 'plain' || $fileext eq 'html' ? header(-type=>"text/$fileext", -attachment=>$filename, -expires=>'0', -content_length=>$filesize) : header(-type=>"attachment/$fileext", -attachment=>$filename, -expires=>'0', -content_length=>$filesize);
	binmode(STDOUT);
	print $content;
	exit;
}

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

if ($action eq "new")
{
	my $messfilename = "${lbdir}${msgdir}/main/${memberfilename}_mian.cgi";
	&error("ä¸å…è®¸å‘é€çŸ­ä¿¡æ¯&æ‚¨è®¾ç½®äº†çŸ­ä¿¡æ¯å…æ‰“æ‰°ï¼Œè¿™æ ·ä½ æ˜¯æ— æ³•æ¥å—çŸ­æ¶ˆæ¯çš„ï¼Œæ‰€ä»¥ä½ ä¹Ÿæ— æ³•å‘é€çŸ­æ¶ˆæ¯ï¼<br><font color=$fonthighlight>è¯·å–æ¶ˆçŸ­ä¿¡æ¯å…æ‰“æ‰°ï¼Œç„¶åå†é‡æ–°å‘é€çŸ­æ¶ˆæ¯ï¼</font><br><br>&msg") if (-e $messfilename && $membercode ne "ad");
        $mymoney2 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	if (($msgmneedmm ne "off")&&($actionto eq "msg")) {
	    &error("$moneynameä¸è¶³&å‘é€çŸ­æ¶ˆæ¯éœ€è¦è´¹ç”¨:$msgmm $moneynameï¼Œä½†ä½ åªæœ‰ $mymoney2 $moneynameã€€<BR><BR>&msg") if ($mymoney2 < $msgmm);
	}
	my $cleanname = $intouser;
	$cleanname =~ tr/A-Z/a-z/;
	$cleanname =~ s/\_/ /g;
	$inmessage =~ s/<p>/\n\n/ig;
	$inmessage =~ s/<br>/\n/ig;

	my $friendlist = "";
	if (open(FILE, "${lbdir}memfriend/${memberfilename}.cgi")) {
        	sysread(FILE, my $currentlist,(stat(FILE))[7]);
		close(FILE);
		$currentlist =~ s/\r//isg;
		@currentlist = split (/\n/, $currentlist);
	}
	my $friendlist = "";
	foreach (@currentlist) {
		chomp;
		s/^ï¼Šï¼ƒï¼ï¼†ï¼Š//isg;
		$friendlist .= qq~<option value="$_">$_</option>~;
	}

	if ($msgmneedmm ne "off") {
	$addout=qq~
	<tr>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>æ‚¨çš„ç°é‡‘ï¼š</b></td>
            <td bgcolor=$miscbackone align="left">&nbsp;<B>$mymoney2</B> $moneyname</td>
            </tr>
	<tr>
            <td bgcolor=$miscbackone valign=top><font color=$fontcolormisc><b>è´¹ç”¨ï¼š</b></td>
            <td bgcolor=$miscbackone align="left">&nbsp;<b>$msgmm</B> $moneyname/æ¡</td>
            </tr>
	~;
	}

	$output .= qq~
<script language="Javascript">
function friendls1() {
    var myfriend = document.FORM.friend.options[document.FORM.friend.selectedIndex].value;
    if (myfriend != "") document.FORM.touser.value = document.FORM.touser.value = myfriend;
}
</script>
<tr><td bgColor=$miscbacktwo align=center colSpan=2 $catbackpic height=26><font color=$fontcolormisc><b>å‘é€çŸ­æ¶ˆæ¯</b></td></tr>
<tr><td bgColor=$miscbackone align=center colSpan=2><a href=$thisprog?action=inbox>$inboxpm</a>ã€€<a href=$thisprog?action=outbox>$outboxpm</a>ã€€<a href=$thisprog?action=new>$newpm</a>ã€€<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>ã€€<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbacktwo colSpan=2 align=center><form action=messanger.cgi method=POST name=FORM enctype="multipart/form-data"><input type=hidden name=action value="send"><input type=hidden name=check value="yes"><font color=$fontcolormisc><b>è¯·å®Œæ•´è¾“å…¥ä¸‹åˆ—ä¿¡æ¯</b></td></tr>
<tr>
<td bgColor=$miscbackone><font color=$fontcolormisc><b>æ”¶ä»¶äººï¼š</b></font></td>
<td bgColor=$miscbackone><input type=text name=touser value="$cleanname" size=16> ã€€<select name=friend OnChange="friendls1()"><option>å¥½å‹åå•</option>$friendlist</select></td>
</tr>
<tr>
<td bgColor=$miscbackone valign=top><font color=$fontcolormisc><b>æ ‡é¢˜ï¼š</b></font></td>
<td bgColor=$miscbackone><input type=text name=msgtitle size=36 maxlength=80 value=$inmsgtitle></td>
</tr>~;
	if ($allowmsgattachment ne 'no')
	{
		my $addtypedisp = $addtype;
		$addtypedisp =~ s/\, /\,/ig;
		$addtypedisp =~ s/ \,/\,/ig;
		$addtypedisp =~ tr/A-Z/a-z/;
		my @addtypedisp = split(/\,/, $addtypedisp);
		$addtypedisp = "<select><option value=#>æ”¯æŒç±»å‹ï¼š</option><option value=#>----------</option>";
		foreach (@addtypedisp)
		{
			chomp;
			next if ($_ eq "");
			$addtypedisp .= "<option>$_</option>";
		}
		$addtypedisp .= qq~</select>~;
		$output .= qq~
<tr>
<td bgColor=$miscbackone valign=top width=30%><font color=$fontcolormisc><b>é™„ä»¶ï¼š</b><br>(æœ€å¤§ <b>60</b> KB)</font></td>
<td bgColor=$miscbackone><input type=file size=30 name=addme><br>$addtypedisp</td>
</tr>
~;
	}

$output .= qq~
<tr>
<td bgColor=$miscbackone valign=top><font color=$fontcolormisc><b>å†…å®¹ï¼š</b></td>
<td bgColor=$miscbackone><textarea cols=35 rows=6 name=message OnKeyDown="ctlent()">$inmessage</textarea><br><input type=checkbox name=backup value="yes" class=1><font color=$fontcolormisc>æ˜¯å¦å¤åˆ¶ä¸€ä»½æ¶ˆæ¯è‡³å‘ä»¶ç®±ï¼Ÿ</font></td>
</tr>$addout
<tr><td  colSpan=2 bgColor=$miscbacktwo align=center><input type=submit value="å‘ é€" name=Submit> ã€€<input type=reset name=Clear value="æ¸… é™¤"></td></form></tr>
~;
}

elsif ($action eq "exportall")
{
	my $filetotrash = $inwhere eq "inbox" ? "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi" : "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";

	if (-e $filetotrash)
	{
		open(FILE, $filetotrash);
        	sysread(FILE, my $messanges,(stat(FILE))[7]);
		close(FILE);
		$messanges =~ s/\r//isg;
		my @messanges = split (/\n/, $messanges);
		
		$output .= qq~
<script language="JavaScript">
function HighlightAll(theField)
{
	var tempval = eval("document." + theField);
	tempval.focus();
	tempval.select();
	therange = tempval.createTextRange();
	therange.execCommand("Copy");
}
</script>
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>å¯¼å‡ºçŸ­æ¶ˆæ¯</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>ã€€<a href=$thisprog?action=outbox>$outboxpm</a>ã€€<a href=$thisprog?action=new>$newpm</a>ã€€<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>ã€€<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><form name=FORM2><textarea name=inpost rows=12 style="width=90%">~;
	my $boxname = $inwhere eq "inbox" ? "æ”¶ä»¶ç®±" : "å‘ä»¶ç®±";
	$current_time = localtime;
	$output .= qq~
$boardnameä¸­$inmembernameçš„çŸ­ä¿¡æ¯$boxnameå¯¼å‡ºå†…å®¹
(å¯¼å‡ºæ—¶é—´ï¼š$current_time)
----------------------------------------
~;
	my $addtime = ($timedifferencevalue + $timezone) * 3600;
	foreach (@messanges)
	{
		($usrname, $msgread, $msgtime, $msgtitle, $msgwords) = split(/\t/, $_);
		$usrname =~ s/^ï¼Šï¼ƒï¼ï¼†ï¼Š//isg;
		$msgwords =~ s/\r//ig;
		$msgwords =~ s/&nbsp;/ /g;
		$msgwords =~ s/"/\&quot;/g;
		$msgwords =~ s/\s+/ /g;
		$msgwords =~ s/<br>/\n/g;
		$msgwords =~ s/<p>/\n/g;
		$msgtime = &dateformat($msgtime + $addtime);
		$output .= "\n[æ”¶å‘å¯¹è±¡]ï¼š$usrname\n[æ”¶å‘æ—¶é—´]ï¼š$msgtime\n[çŸ­ä¿¡æ ‡é¢˜]ï¼š$msgtitle\n[çŸ­ä¿¡å†…å®¹]ï¼š$msgwords\n";
	}
	$output .= qq~</textarea><br>>> <a href="javascript:HighlightAll('FORM2.inpost')">å¤åˆ¶åˆ°å‰ªè´´æ¿ <<</a></form>
<font color=red>æ‚¨åœ¨$boxnameä¸­çš„çŸ­æ¶ˆæ¯å·²å…¨éƒ¨å¯¼å‡ºï¼Œè¿™äº›çŸ­ä¿¡æ¯å¹¶æœªè¢«çœŸæ­£åˆ é™¤ï¼<br>ä¸ºå‡å°‘æœåŠ¡å™¨å‹åŠ›ï¼Œè¯·å°½æ—©<a href=$thisprog?action=deleteall&where=$inwhere>[æ¸…ç©º]</a>æ‚¨åœ¨$boxnameä¸­çš„çŸ­æ¶ˆæ¯ï¼<br><br></td></tr>~;
	}
	else
	{
		&error("çŸ­æ¶ˆæ¯&æ–‡ä»¶æ²¡æœ‰æ‰¾åˆ°ï¼Œè¯·é‡å¤åˆšæ‰æ­¥éª¤ï¼&msg");
	}
}

elsif ($action eq "markall")
{	    
	$filetoopen = "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi";
	if (-e $filetoopen)
	{
		&winlock($filetoopen) if ($OS_USED eq "Nt");
		open(FILE, $filetoopen);
		flock(FILE, 1) if ($OS_USED eq "Unix");
        	sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
		close(FILE);
		$inboxmessages =~ s/\r//isg;
		my @inboxmessages = split (/\n/, $inboxmessages);
		
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@inboxmessages)
		{
			chomp;
			next if ($_ eq "");
			($from, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $_);
			print FILE "$from\tyes\t$date\t$messagetitle\t$post\t$attach\n";
		}
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
	}
	my $boxname = $inwhere eq "inbox" ? "æ”¶ä»¶ç®±" : "å‘ä»¶ç®±";
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>æ‰€æœ‰çš„çŸ­æ¶ˆæ¯å·²è¢«æ ‡è®°ä¸ºå·²è¯»</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>ã€€<a href=$thisprog?action=outbox>$outboxpm</a>ã€€<a href=$thisprog?action=new>$newpm</a>ã€€<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>ã€€<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>æ‚¨åœ¨$boxnameä¸­çš„çŸ­æ¶ˆæ¯å·²ç»å…¨éƒ¨æ ‡è®°ä¸ºå·²è¯»</b><br><br></td></tr>~;
}

elsif ($action eq "send")
{
	&error("å‡ºé”™&è¯·ä¸è¦ç”¨å¤–éƒ¨è¿æ¥æœ¬ç¨‹åºï¼") if (($ENV{'HTTP_REFERER'} !~ /$ENV{'HTTP_HOST'}/i && $ENV{'HTTP_REFERER'} ne '' && $ENV{'HTTP_HOST'} ne '')&&($canotherlink ne "yes"));
	&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼&msg") if ($intouser =~  m/\// || $intouser =~ m/\\/ || $intouser =~ m/\.\./);
	&error("çŸ­æ¶ˆæ¯&æ‚¨è¢«ç¦æ­¢å‘è¨€ï¼&msg") if ($membercode eq "banned" || $membercode eq "masked");
	if (($onlinetime + $onlinetimeadd) < $onlinemessage && $onlinemessage ne "" && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $membercode !~ /^rz/) { $onlinetime = $onlinetime + $onlinetimeadd; &error("çŸ­æ¶ˆæ¯&æœ¬è®ºå›ä¸å…è®¸åœ¨çº¿æ—¶é—´å°‘äº $onlinemessage ç§’çš„ç”¨æˆ·å‘é€çŸ­æ¶ˆæ¯ï¼ä½ ç›®å‰å·²ç»åœ¨çº¿ $onlinetime ç§’ï¼<BR>å¦‚æœåœ¨çº¿æ—¶é—´ç»Ÿè®¡ä¸æ­£ç¡®,è¯·é‡æ–°ç™»é™†è®ºå›ä¸€æ¬¡å³å¯è§£å†³ï¼&msg"); }
	my @sendtouserlist = split(/\;/, $intouser);
	&error("çŸ­æ¶ˆæ¯ç¦æ­¢å‘é€&å¾ˆæŠ±æ­‰ï¼Œä¸€æ¬¡ç¾¤å‘è®¯æ¯æœ€é«˜æ•°é‡æ˜¯ $maxsend æ¡ï¼&msg") if (@sendtouserlist > $maxsend && $maxsend =~ /^[0-9]+$/ && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo");
	$inbackup = $query->param("backup");
	&error("çŸ­æ¶ˆæ¯&æ²¡æœ‰æŒ‡å®šæ”¶ä»¶äººï¼&msg") if (@sendtouserlist == 0);
	
	$mymoney2 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	$msgmm = 0 if (($msgmm < 0)||($msgmm eq "")||($membercode eq "ad")||($membercode eq 'smo')||($membercode eq 'amo')||($membercode eq 'cmo')||($membercode eq "mo"));
	if ($msgmneedmm ne "off") {
		if ($mymoney2 < $msgmm) { &error("$moneynameä¸è¶³&å‘é€çŸ­æ¶ˆæ¯éœ€è¦è´¹ç”¨:$msgmm $moneynameï¼Œä½†ä½ åªæœ‰$mymoney2 $moneynameã€€<BR><BR>&msg"); }
		else {
		    $cleanmembername = $inmembername;
           	    $cleanmembername =~ s/ /\_/g;
		    $cleanmembername =~ tr/A-Z/a-z/;
		    my $namenumber = &getnamenumber($cleanmembername);
		    &checkmemfile($cleanmembername,$namenumber);

		    $filetomake = "$lbdir" . "$memdir/$namenumber/$cleanmembername.cgi";
        	    &winlock($filetomake) if ($OS_USED eq "Nt");
        	    if (open(FILE, ">$filetomake")) {
        		flock(FILE, 2) if ($OS_USED eq "Unix");
			$mymoney=$mymoney-$msgmm;
        		print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        		close(FILE);
        	    }
        	    &winunlock($filetomake) if ($OS_USED eq "Nt");
        	}
	}

    # $addme=$query->upload('addme'); #å¦‚æœCGI.pmç‰ˆæœ¬>2.47ï¼Œæ¨èä½¿ç”¨
    $addme=$query->param('addme'); #å¦‚æœCGI.pmç‰ˆæœ¬<2.47ï¼Œç”¨ä»–æ›¿æ¢ä¸Šå¥

        my $attach = '';
        if ($addme && $allowmsgattachment ne 'no')
        {

               my ($up_filename) = $addme =~ m|([^/:\\]+)$|; #æ³¨æ„,è·å–æ–‡ä»¶åå­—çš„å½¢å¼å˜åŒ–
               my @up_names = split(/\./,$up_filename); #æ³¨æ„
               my $up_name = $up_names[0];
               my $up_ext = $up_names[-1];
               $up_ext = lc($up_ext);


                my $checkadd = 0;
                foreach (split(/\,\s*/, $addtype))
                {
                        $checkadd = 1, last if ($up_ext eq lc($_));
                }
                &error("ä¸Šä¼ å‡ºé”™&ä¸æ”¯æŒä½ æ‰€ä¸Šä¼ çš„é™„ä»¶ç±»å‹($up_ext)ï¼Œè¯·é‡æ–°é€‰æ‹©ï¼&msg") if ($checkadd == 0);
                my $filesize = 0;
                my $bufferall = '';


                 binmode ($addme); #æ³¨æ„

                 while (read($addme,$buffer,4096) )
                 {#2
                   if ($up_ext eq "txt" || $up_ext eq "htm" || $up_ext eq "html" || $up_ext eq "shtml")
                   {
                       $buffer =~ s/\.cookie/\&\#46\;cookie/isg;
                       $buffer =~ s/on(mouse|exit|error|click|key)/\&\#111\;n$1/isg;
                       $buffer =~ s/script/scri\&\#112\;t/isg;
                       $buffer =~ s/style/\&\#115\;tyle/isg;
                   }
                  $bufferall .= $buffer;
                  $filesize += 4;
                  } #2

                 close ($addme); #æ³¨æ„

                &error("ä¸Šä¼ å‡ºé”™&ä¸Šä¼ é™„ä»¶å¤§å°è¶…è¿‡ 60 KBï¼Œè¯·é‡æ–°é€‰æ‹©ï¼&msg") if (length($bufferall) > 60 * 1024);

                if ($up_ext eq "gif" || $up_ext eq "jpg" || $up_ext eq "bmp" || $up_ext eq "jpeg" || $up_ext eq "png" || $up_ext eq "ppm" || $up_ext eq "svg" || $up_ext eq "xbm" || $up_ext eq "xpm")
                {
                        eval("use Image::Info qw(image_info);");
                        if ($@ eq "")
                        {
                                my $info = image_info(\$bufferall);
                                &error("ä¸Šä¼ å‡ºé”™&ä¸Šä¼ é™„ä»¶ä¸æ˜¯å›¾ç‰‡æ–‡ä»¶ï¼Œè¯·ä¸Šä¼ æ ‡å‡†çš„å›¾ç‰‡æ–‡ä»¶ï¼&msg") if ($info->{error} eq "Unrecognized file format");
                        }
                }
                $attach = "$up_filenameï¼Šï¼ƒï¼ï¼†ï¼Š" . &Base64encode($bufferall);
        }

	undef @NoRegUser; undef @Max; undef @NoPM;
	my $noadmin = $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "amo" && $membercode ne "mo" ? 1 : 0;
	my $currenttime = time;
	foreach (@sendtouserlist)
	{
		undef @inboxmessages; undef @allmessages; undef @blacklist;

		chomp;
		next if ($_ eq "");
		$cleanintouser = $_;
		$cleanintouser =~ s/ /\_/g;
		$cleanintouser =~ tr/A-Z/a-z/;
		$cleanintouser = &stripMETA($cleanintouser);

		&getmember($_,"no");
		if ($userregistered eq "no")
		{
			push(@NoRegUser, "å‘é€çŸ­ä¿¡æ¯é”™è¯¯-æ²¡æœ‰æ‰¾åˆ°ç”¨æˆ·ã€Œ$_ã€");
			next;
		}

		if ($noadmin)
		{
			if ($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "amo" && $membercode ne "mo" && $maxmsgno =~ /^[0-9]+$/ && $maxmsgno != 0)
			{
				my $filetoopen = "${lbdir}${msgdir}/in/${cleanintouser}_msg.cgi";
				if (open(FILE, $filetoopen)) {
        				sysread(FILE, my $allmessages,(stat(FILE))[7]);
					close(FILE);
					$allmessages =~ s/\r//isg;
					@allmessages = split (/\n/, $allmessages);
				}
				if (@allmessages >= $maxmsgno) {
					push(@Max, "æ— æ³•å‘é€çŸ­ä¿¡æ¯ç»™å¯¹æ–¹-$_çš„çŸ­æ¶ˆæ¯æ”¶ä»¶ç®±å·²å®¹çº³ $maxmsgno æ¡æ¶ˆæ¯ï¼Œç©ºé—´å·²æ»¡");
					next;
				}
			}

			my $filetoopen = "${lbdir}memblock/${cleanintouser}.cgi";
			if (open(FILE, $filetoopen)) {
        			sysread(FILE, my $blacklist,(stat(FILE))[7]);
				close(FILE);
				$blacklist =~ s/\r//isg;
				@blacklist = split (/\n/, $blacklist);
				chomp(@blacklist);
				if (grep(/^ï¼Šï¼ƒï¼ï¼†ï¼Š$inmembername$/i, @blacklist))
				{
					push(@Max, "æ— æ³•å‘é€çŸ­ä¿¡æ¯ç»™å¯¹æ–¹-$_å·²å°†ä½ çº³å…¥å…¶é»‘åå•å†…ï¼Œä¸æ¥å—ä½ çš„ä»»ä½•çŸ­ä¿¡æ¯ï¼");
					next;
				}
			}

			my $messfilename = "${lbdir}${msgdir}/main/${cleanintouser}_mian.cgi";
			if (open(FILE, $messfilename))
			{
				$mess = <FILE>;
				close(FILE);	
				push(@NoPM, "æ— æ³•å‘é€çŸ­ä¿¡æ¯-$_è®¾ç½®äº†çŸ­æ¶ˆæ¯å…æ‰“æ‰°åŠŸèƒ½ã€€<br><br>è‡ªåŠ¨å…æ‰“æ‰°å›è¦† <font color=$fonthighlight>$mess</font><br><br>");
				next;
			}
		}

		my $tmp = &dofilter("$inmsgtitle\t$inmessage");
		($inmsgtitle, $inmessage) = split (/\t/, $tmp);
		
		$inmsgtitle =~ s/()+//isg;
		my $tempinmsgtitle = $inmsgtitle;
		$tempinmsgtitle =~ s/ //g;
		$tempinmsgtitle =~ s/\&nbsp\;//g;
		$tempinmsgtitle =~ s/ã€€//isg;
		$tempinmsgtitle =~ s/winlock($filetoopen) if ($OS_USED eq "Nt");
		if (open (FILE, $filetoopen)) {
			flock(FILE, 1) if ($OS_USED eq "Unix");
       			sysread(FILE, $outboxmessages,(stat(FILE))[7]);
			close(FILE);
			$outboxmessages =~ s/\r//isg;
		}
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		$intouser =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
		print FILE "£ª£££¡£¦£ª$intouser\tyes\t$currenttime\t$inmsgtitle\t$inmessage\t$attach\n$outboxmessages";
		close(FILE);
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
		$backupmsg = "¸ÃÏûÏ¢Í¬Ê±Ò²¸´ÖÆµ½ÄúµÄ·¢¼şÏäÖĞÁË£¡<br>";
	}

	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>ÊÕ·¢¶ÌÏûÏ¢</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>¡¡<a href=$thisprog?action=outbox>$outboxpm</a>¡¡<a href=$thisprog?action=new>$newpm</a>¡¡<a href="javascript:openscript('friendlist.cgi',420,320)">$friendpm</a>¡¡<a href="javascript:openscript('blocklist.cgi',420,320)">$blockpm</a></td></tr>~;

	unless (@NoRegUser > 0 || @Max > 0 || @NoPM > 0)
	{
		$output .= qq~
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>¸ø$intouserµÄ¶ÌÏûÏ¢ÒÑ¾­·¢³ö¡£</b>$backupmsg<br>×Ô¶¯·µ»ØÊÕ¼şÏä¡£<br><br></td></tr>
<meta http-equiv="refresh" Content="2; url=$thisprog?action=inbox">~;
	}
	else
	{
		$output .= qq~
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>¶ÌÏûÏ¢·¢ËÍÓĞ´íÎó¡£</b>$backupmsg<br><br><br></td></tr>~;

		foreach (@NoRegUser, @Max, @NoPM)
		{
			$output .= qq~
<tr><td bgColor=$miscbackone align=center>$_</td></tr>~;
		}
	}
}

elsif ($action eq "outbox")
{
	$filetoopen = "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
	if (open(FILE, $filetoopen)) {
		sysread(FILE, my $outboxmessages,(stat(FILE))[7]);
		close(FILE);
		$outboxmessages =~ s/\r//isg;
		@outboxmessages = split (/\n/, $outboxmessages);
	}
	$totalinboxmessages = @outboxmessages;

	$output .= qq~
<style>
input	{border-top-width: 1px; padding-right: 1px; padding-left: 1px; border-left-width: 1px; font-size: 9pt; border-left-color: #cccccc; border-bottom-width: 1px; border-bottom-color: #cccccc; padding-bottom: 1px; border-top-color: #cccccc; padding-top: 1px; height: 18px; border-right-width: 1px; border-right-color: #cccccc}
</style>
<script language="JavaScript">
function CheckAll(form)
{
	for (var i = 0; i < form.elements.length; i++) form.elements[i].checked = true;
}
function FanAll(form)
{
	for (var i = 0; i < form.elements.length; i++) form.elements[i].checked = !(form.elements[i].checked);
}
</script>
<form action=$thisprog method=POST>
<input type=hidden name=where value="outbox">
<input type=hidden name=action value="delete">
<tr><td bgColor=$miscbacktwo align=center colSpan=3 $catbackpic height=26><font color=$fontcolormisc><b>»¶Ó­Ê¹ÓÃ¶ÌÏûÏ¢·¢ËÍ£¬$inmembername</b></td></tr>
<tr><td bgColor=$miscbackone align=center colSpan=3><a href=$thisprog?action=inbox>$inboxpm</a>¡¡<a href=$thisprog?action=outbox>$outboxpm</a>¡¡<a href=$thisprog?action=new>$newpm</a>¡¡<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>¡¡<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr>
<td bgColor=$miscbackone align=center width=20%><font color=$fontcolormisc><b>ÊÕ¼şÈË</b></td>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>Ö÷Ìâ</b></td>
<td bgColor=$miscbackone align=center width=10%><font color=$fontcolormisc><b>É¾³ı±ê¼Ç</b></td>
</tr>~;
	&splitpage("outbox");

	foreach (@outboxmessages [$startarray .. $endarray])
	{
		chomp;
		my ($from, $readstate, $date, $messagetitle, $message, $attach) = split(/\t/, $_);
		$from =~ s/^£ª£££¡£¦£ª//isg;
		$messagetitle = &dofilter($messagetitle);
		$messagetitle = "<a href=$thisprog?action=outread&msg=$count>$messagetitle</a>";
		$messagetitle .= qq~ <img src=$imagesurl/icon/replyattachment.gif width=15 align=absmiddle alt="¶ÌÏûÏ¢ÖĞº¬ÓĞ¸½¼ş">~ if($attach ne '');
		my $tempform = my $tempname = $from;
		$from = &lbhz($from, 12);
		$tempname =~ s/ /\_/g;
		$tempname = uri_escape($tempname);
		$output .= qq~
<tr>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><a href=profile.cgi?action=show&member=$tempname target=_blank title="$tempform">$from</a></td>
<td bgColor=$miscbackone><font color=$fontcolormisc>&nbsp;$messagetitle</td>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><b><input type=checkbox name="msg" value="$count" class=1></b></td>
</tr>~;
		$count++;
 	}
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center colSpan=3>$pages<font color=$fontcolormisc><a href=$thisprog?action=deleteall&where=outbox>[É¾³ıËùÓĞ]</a>  <a href=$thisprog?action=exportall&where=outbox>[µ¼³öËùÓĞ]</a>  <input type=button name=chkall value="È«Ñ¡" OnClick="CheckAll(this.form)"> <input type=button name=clear2 value="·´Ñ¡" OnClick="FanAll(this.form)"> <input type=reset name=Reset value="ÖØÖÃ"> <input type=submit name=delete value="É¾³ı"></td></tr></form>~;
}

elsif ($action eq "inbox")
{
	my $filetoopen = "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi";
	if (open (FILE, $filetoopen)) {
		sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
		close(FILE);
		$inboxmessages =~ s/\r//isg;
		@inboxmessages = split (/\n/, $inboxmessages);
	}
	$totalinboxmessages = @inboxmessages;

	$output .= qq~
<style>
input	{border-top-width: 1px; padding-right: 1px; padding-left: 1px; border-left-width: 1px; font-size: 9pt; border-left-color: #cccccc; border-bottom-width: 1px; border-bottom-color: #cccccc; padding-bottom: 1px; border-top-color: #cccccc; padding-top: 1px; height: 18px; border-right-width: 1px; border-right-color: #cccccc}
</style>
<script language="JavaScript">
function CheckAll(form)
{
	for (var i = 0; i < form.elements.length; i++) form.elements[i].checked = true;
}
function FanAll(form)
{
	for (var i = 0; i < form.elements.length; i++) form.elements[i].checked = !(form.elements[i].checked);
}
</script>
<form action=$thisprog method=POST>
<input type=hidden name=where value="inbox">
<input type=hidden name=action value="delete">
<tr><td bgColor=$miscbacktwo align=center colSpan=4 $catbackpic height=26><font color=$fontcolormisc>$dxxboom<b>»¶Ó­Ê¹ÓÃÄúµÄÊÕ¼şÏä£¬$membername</b></td>
</tr>
<tr><td bgColor=$miscbackone align=center colSpan=4><a href=$thisprog?action=inbox>$inboxpm</a>¡¡<a href=$thisprog?action=outbox>$outboxpm</a>¡¡<a href=$thisprog?action=new>$newpm</a>¡¡<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>¡¡<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr>
<td bgColor=$miscbackone align=center width=20%><font color=$fontcolormisc><b>·¢¼şÈË</b></td>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>Ö÷Ìâ</b></td>
<td bgColor=$miscbackone align=center width=10%><font color=$fontcolormisc><b>ÊÇ·ñÒÑ¶Á</b></td>
<td bgColor=$miscbackone align=center width=10%><font color=$fontcolormisc><b>É¾³ı±ê¼Ç</b></td>
</tr>~;
	&splitpage("inbox");

	foreach (@inboxmessages[$startarray .. $endarray])
	{
		my ($from, $readstate, $date, $messagetitle, $message, $attach) = split(/\t/, $_);
		$from =~ s/^£ª£££¡£¦£ª//isg;
		$callstate = 1 if($readstate eq "no");
		my $readstate = $readstate eq "no" ? qq~<img src=$imagesurl/images/unread.gif border=0 alt="Î´¶Á" width=16 height=12>~ : qq~<img src=$imagesurl/images/read.gif border=0 alt="ÒÑ¶Á" width=16 height=14>~;
		$messagetitle = &dofilter($messagetitle);
		$messagetitle = "<a href=$thisprog?action=read&msg=$count>$messagetitle</a>";
		$messagetitle .= qq~ <img src=$imagesurl/icon/replyattachment.gif width=15 height=15 align=absmiddle alt="¶ÌÏûÏ¢ÖĞº¬ÓĞ¸½¼ş">~ if($attach ne '');
		my $tempform = my $tempname = $from;
		$from = &lbhz($from, 12);
		$tempname =~ s/ /\_/g;
		$tempname = uri_escape($tempname);
		$output .= qq~
<tr>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><a href=profile.cgi?action=show&member=$tempname target=_blank title="$tempform">$from</a></td>
<td bgColor=$miscbackone><font color=$fontcolormisc>&nbsp;$messagetitle</td>
<td bgColor=$miscbackone align=center>$readstate</td>
<td bgColor=$miscbackone align=center><font color=$fontcolormisc><b><input type=checkbox name=msg value="$count" class=1></b></td>
</tr>~;
		$count++;
	}
	if ($membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "amo" && $membercode ne "mo" && $maxmsgno != 0)
	{
		$pmpercent = int(($totalinboxmessages / $maxmsgno) * 100);
		if ($pmpercent < 100)
		{
			$output .= qq~
<tr><td bgColor=$miscbacktwo colSpan=4 align=center>ÄãÏÖÔÚµÄ¶ÌÏûÏ¢´æ´¢Á¿: $pmpercent%</td></tr>
<tr><td bgColor=$miscbackone colSpan=4><img src=$imagesurl/images/pm_gauge.gif width=$pmpercent% height=9><table cellSpacing=1 width=100%><tr><td width=45% align=left>0%</td><td width=* align=center>50%</td><td width=45% align=right>100%</td></tr></table></td></tr>~;
		}
		else
		{
			$output .= qq~<tr><td bgColor=$miscbacktwo colSpan=4 align=center><font color=red>ÄãÏÖÔÚµÄ¶ÌÏûÏ¢´æ´¢Á¿ÒÑÂú£¬Èç²»½øĞĞÉ¾³ı½«²»ÄÜ½ÓÊÕ¶ÌĞÅÏ¢</font></td></tr>~;
		}
	}
	$output .= qq~<bgsound src=$imagesurl/images/mail.wav border=0>~ if(($callstate eq '1')&&($infofreshtime ne ''));
	$output .= qq~<meta http-equiv="refresh" content="$infofreshtime; url=$thisprog?action=inbox">~ if($infofreshtime ne '');
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center colSpan=4>$pages<font color=$fontcolormisc><a href=$thisprog?action=deleteall&where=inbox>[É¾³ıËùÓĞ]</a> <a href=$thisprog?action=exportall&where=inbox>[µ¼³öËùÓĞ]</a> <a href=$thisprog?action=markall&where=inbox>[ËùÓĞÒÑ¶Á]</a> <input type=button name=chkall value="È«Ñ¡" OnClick="CheckAll(this.form)"> <input type=button name=clear2 value="·´Ñ¡" OnClick="FanAll(this.form)"> <input type=reset name=Reset value="ÖØÖÃ"> <input type=submit name=delete value="É¾³ı"></td></tr></form>~;
}

elsif ($action eq "outread")
{
	$filetoopen = "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
	my @outboxmessages;
	if (open(FILE, $filetoopen)) {
		sysread(FILE, my $outboxmessages,(stat(FILE))[7]);
		close(FILE);
		$outboxmessages =~ s/\r//isg;
		@outboxmessages = split (/\n/, $outboxmessages);
	}
	my $msgtograb = $outboxmessages[$inmsg];
	&error("ä¯ÀÀÏûÏ¢&Ã»ÓĞ´ËÏûÏ¢£¡»ò´ËÏûÏ¢ÒÑ±»É¾³ı£¡&msg") if ($msgtograb eq "");

	$wwjf = "no";
	$hidejf = "no";
	$postjf = "no";
	$membercode = "no";
        
	my ($to, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $msgtograb);
	$to =~ s/^£ª£££¡£¦£ª//isg;
	$date = $date + ($timedifferencevalue + $timezone) * 3600;
	$date = &dateformat($date);
	
	$post1 = $post;
	&lbcode(\$post);
	if ($emoticons eq "on")
	{
		&doemoticons(\$post);
		&smilecode(\$post);
	}
	$remsg = "Re:$messagetitle";
	$fwmsg = "Fw:$messagetitle";
	$remodel = "$to£¬ÄúºÃ£¡ÉÏ´ÎÄúĞ´µÀ£º\n\n------------------------------\n$post1\n------------------------------";
	$fwmodel = "$to£¬ÄúºÃ£¡ÏÂÃæÊÇ×ª·¢µÄÏûÏ¢£º\n\n------------------------------\n$post1\n------------------------------";

	%readstatus = ("yes"=>"ÒÑ¶Á", "no"=>"Î´¶Á");
        if ($inmsg < @outboxmessages - 1)
	{
		my $outboxdown = $inmsg + 1;
		(undef, $nreadstate, undef, $nmessagetitle, undef) = split(/\t/, $outboxmessages[$outboxdown]);
		$outboxmsgdown = qq~<a href=$thisprog?action=outread&msg=$outboxdown title="ÏÂÒ»ÌõÏûÏ¢: ($readstatus{$nreadstate})\nÏûÏ¢±êÌâ: $nmessagetitle">ÏÂÒ»Ìõ</a>~;
	}
	if ($inmsg > 0)
	{
		my $outboxup = $inmsg - 1;
		(undef, $preadstate, undef, $pmessagetitle, undef) = split(/\t/, $outboxmessages[$outboxup]);
		$outboxmsgup = qq~<a href=$thisprog?action=outread&msg=$outboxup title="ÉÏÒ»ÌõÏûÏ¢: ($readstatus{$preadstate})\nÏûÏ¢±êÌâ: $pmessagetitle">ÉÏÒ»Ìõ</a>~;
	}
	$outboxsplitline = " | " if ($outboxmsgdown ne "" && $outboxmsgup ne "");
	if ($outboxmsgdown ne "" || $outboxmsgup ne "")
	{
		$outboxtempone = "[ ";
		$outboxtemptwo = " ]";
	}
	my $attachfile = '';
	if ($attach ne '')
	{
		$attachfile = (split('£ª£££¡£¦£ª', $attach), 1)[0];
		my $up_ext = lc((split(/\./, $attachfile))[-1]);
		my $filetype = "unknow";
		$filetype = $up_ext if (-e "${imagesdir}icon/$up_ext.gif");
		$attachfile = "<br><b>ÏûÏ¢¸½¼ş£º</b><img src=$imagesurl/icon/$filetype.gif width=16 height=16> <a href=$thisprog?action=attach&box=out&msg=$inmsg target=_blank>$attachfile</a>";
		if (($filetype eq "gif")||($filetype eq "jpg")||($filetype eq "jpe")||($filetype eq "jpeg")||($filetype eq "tif")||($filetype eq "png")||($filetype eq "bmp")) {
			$post = qq~<a href=$thisprog?action=attach&box=out&msg=$inmsg target=_blank><img src=$thisprog?action=attach&box=out&msg=$inmsg border=0 alt=°´´ËÔÚĞÂ´°¿Úä¯ÀÀÍ¼Æ¬ onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"></a><p>$post~;
		}
	}

	$output .= qq~
<form name=re action=$thisprog method=POST><input type=hidden name=action value="new"><input type=hidden name=touser value="$to"><input type=hidden name=msgtitle value="$remsg"><input type=hidden name=message value="$remodel"></form>
<form name=fw action=$thisprog method=POST><input type=hidden name=action value="new"><input type=hidden name=touser value="$to"><input type=hidden name=msgtitle value="$fwmsg"><input type=hidden name=message value="$fwmodel"></form>
<tr><td bgColor=$miscbacktwo align=center colSpan=3 $catbackpic height=26><font color=$fontcolormisc><b>»¶Ó­Ê¹ÓÃ¶ÌÏûÏ¢½ÓÊÕ£¬$inmembername</b></td></tr>
<tr><td bgColor=$miscbackone align=center colSpan=3><a href=$thisprog?action=delete&where=outbox&msg=$inmsg>$deletepm</a>¡¡<a href=$thisprog?action=inbox>$inboxpm</a>¡¡<a href=$thisprog?action=outbox>$outboxpm</a>¡¡<a href=$thisprog?action=new>$newpm</a>¡¡<a href="javascript:document.re.submit()">$replypm</a>¡¡<a href="javascript:document.fw.submit()">$fwpm</a>¡¡<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>¡¡<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc>ÔÚ<b>$date</b>£¬Äú·¢ËÍ´ËÏûÏ¢¸ø<b>$to</b>£¡</td></tr>
<tr><td bgColor=$miscbackone valign=top><font color=$fontcolormisc>
<b>ÏûÏ¢±êÌâ£º$messagetitle</b>$attachfile<p>$post
<p align=right>$outboxtempone$outboxmsgup$outboxsplitline$outboxmsgdown$outboxtemptwo</p>
</td></tr>~;
}

elsif ($action eq "read")
{
	my $filetoopen = "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi";
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	my @inboxmessages;
	if (open(FILE, $filetoopen)) {
        	flock (FILE, 1) if ($OS_USED eq "Unix");
		sysread(FILE, my $inboxmessages,(stat(FILE))[7]);
		close(FILE);
		$inboxmessages =~ s/\r//isg;
		@inboxmessages = split (/\n/, $inboxmessages);
	}
	$msgtograb = $inboxmessages[$inmsg];
	chomp $msgtograb;
	if ($msgtograb eq "")
	{
		&winunlock($filetoopen) if ($OS_USED eq "Nt");
		&error("ä¯ÀÀÏûÏ¢&Ã»ÓĞ´ËÏûÏ¢£¡»ò´ËÏûÏ¢ÒÑ±»É¾³ı£¡&msg");
	}
	my ($from, $readstate, $date, $messagetitle, $post, $attach) = split(/\t/, $msgtograb);
	if ($readstate eq "no")
	{
		$count = 0;
		open(FILE, ">$filetoopen");
		flock(FILE, 2) if ($OS_USED eq "Unix");
		foreach (@inboxmessages)
		{
			chomp;
			if ($count eq $inmsg) {
				print FILE "$from\tyes\t$date\t$messagetitle\t$post\t$attach\n";
			}
			else {
				print FILE "$_\n";
			}
			$count++;
		}
		close (FILE);
	}
	&winunlock($filetoopen) if ($OS_USED eq "Nt");

	$wwjf = "no";
	$hidejf = "no";
	$postjf = "no";
	$membercode = "no";

	$from =~ s/^£ª£££¡£¦£ª//isg;
	$date = $date + ($timedifferencevalue + $timezone) * 3600;
	$date = &dateformat($date);

	$post1 = $post;
	&lbcode(\$post);
	if ($emoticons eq "on")
	{
		&doemoticons(\$post);
		&smilecode(\$post);
	}

       if($messagetitle =~m/^Re:(.+?)$/){ 
       $omessagetitle=$messagetitle; 
       $replynum=1; 
       while($omessagetitle =~ m/^Re:/){ 
       $replynum++;$omessagetitle=~s/^Re://s; 
       } 
       $remsg="Re($replynum):$omessagetitle"; 
       }elsif($messagetitle =~m/^Re(.+?):(.+?)$/){ 
       $omessagetitle=$messagetitle; 
       $replynum=$1; 
       $replynum=~s/^\(//; 
       $replynum=~s/\)$//; 
       $replynum=int($replynum)+1; 
       $omessagetitle=~s/^Re(.+?)://; 
       $remsg="Re($replynum):$omessagetitle"; 
       }else{ 
       $remsg="Re:$messagetitle"; 
       } 
       if($messagetitle =~m/^Fw:(.+?)$/){ 
       $omessagetitle=$messagetitle; 
       $fornum=1; 
       while($omessagetitle =~ m/^Fw:/){ 
       $fornum++;$omessagetitle=~s/^Fw://s; 
       } 
       $fwmsg="Fw($fornum):$omessagetitle"; 
       }elsif($messagetitle =~m/^Fw(.+?):(.+?)$/){ 
       $omessagetitle=$messagetitle; 
       $fornum=$1; 
       $fornum=~s/^\(//; 
       $fornum=~s/\)$//; 
       $fornum=int($fornum)+1; 
       $omessagetitle=~s/^Fw(.+?)://; 
       $fwmsg="Fw($fornum):$omessagetitle"; 
       }else{ 
       $fwmsg="Fw:$messagetitle"; 
       } 

	$post1 =~ s/<p>/\n\n/ig;
	$post1 =~ s/<br>/\n/ig;
	$post1 =~ s/[\"|\<|\>]//ig;
	$remodel = "$from£¬ÄúºÃ£¡ÉÏ´ÎÄúĞ´µÀ£º\n\n------------------------------\n$post1------------------------------";
	$fwmodel = "$from£¬ÄúºÃ£¡ÏÂÃæÊÇ×ª·¢µÄÏûÏ¢£º\n\n------------------------------\n$post1------------------------------";

	%readstatus = ("yes"=>"ÒÑ¶Á", "no"=>"Î´¶Á");
        if ($inmsg < @inboxmessages - 1)
	{
		my $inboxdown = $inmsg + 1;
		(undef, $nreadstate, undef, $nmessagetitle, undef) = split(/\t/, $inboxmessages[$inboxdown]);
		$inboxmsgdown = qq~<a href=$thisprog?action=read&msg=$inboxdown title="ÏÂÒ»ÌõÏûÏ¢: ($readstatus{$nreadstate})\nÏûÏ¢±êÌâ: $nmessagetitle">ÏÂÒ»Ìõ</a>~;
	}
	if ($inmsg > 0)
	{
		my $inboxup = $inmsg - 1;
		(undef, $preadstate, undef, $pmessagetitle, undef) = split(/\t/, $inboxmessages[$inboxup]);
		$inboxmsgup = qq~<a href=$thisprog?action=read&msg=$inboxup title="ÉÏÒ»ÌõÏûÏ¢: ($readstatus{$preadstate})\nÏûÏ¢±êÌâ: $pmessagetitle">ÉÏÒ»Ìõ</a>~;
	}
	$inboxsplitline = " | " if ($inboxmsgdown ne "" && $inboxmsgup ne "");
	if ($inboxmsgdown ne "" || $inboxmsgup ne "")
	{
		$inboxtempone = "[ ";
		$inboxtemptwo = " ]";
	}

	my $attachfile = '';
	if ($attach ne '')
	{
		$attachfile = (split('£ª£££¡£¦£ª', $attach), 1)[0];
		my $up_ext = lc((split(/\./, $attachfile))[-1]);
		my $filetype = "unknow";
		$filetype = $up_ext if (-e "${imagesdir}icon/$up_ext.gif");
		$attachfile = "<br><b>ÏûÏ¢¸½¼ş£º</b><img src=$imagesurl/icon/$filetype.gif width=16 height=16> <a href=$thisprog?action=attach&box=in&msg=$inmsg target=_blank>$attachfile</a>";
		if (($filetype eq "gif")||($filetype eq "jpg")||($filetype eq "jpe")||($filetype eq "jpeg")||($filetype eq "tif")||($filetype eq "png")||($filetype eq "bmp")) {
			$post = qq~<a href=$thisprog?action=attach&box=in&msg=$inmsg target=_blank><img src=$thisprog?action=attach&box=in&msg=$inmsg border=0 alt=°´´ËÔÚĞÂ´°¿Úä¯ÀÀÍ¼Æ¬ onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333" onmousewheel="return bbimg(this)"></a><p>$post~;
		}
	}

	$output .= qq~
<form name=re action=$thisprog method=POST><input type=hidden name=action value="new"><input type=hidden name=touser value="$from"><input type=hidden name=msgtitle value="$remsg"><input type=hidden name=message value="$remodel"></form>
<form name=fw action=$thisprog method=POST><input type=hidden name=action value="new"><input type=hidden name=touser value="$from"><input type=hidden name=msgtitle value="$fwmsg"><input type=hidden name=message value="$fwmodel"></form>
<tr><td bgColor=$miscbacktwo align=center colSpan=2 $catbackpic height=26><font color=$fontcolormisc><b>»¶Ó­Ê¹ÓÃÄúµÄÊÕ¼şÏä£¬$inmembername</b></td></tr>
<tr><td bgColor=$miscbackone align=center colSpan=2><a href=$thisprog?action=delete&where=inbox&msg=$inmsg>$deletepm</a>¡¡<a href=$thisprog?action=inbox>$inboxpm</a>¡¡<a href=$thisprog?action=outbox>$outboxpm</a>¡¡<a href=$thisprog?action=new>$newpm</a>¡¡<a href="javascript:document.re.submit()">$replypm</a>¡¡<a href="javascript:document.fw.submit()">$fwpm</a>¡¡<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>¡¡<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbacktwo align=center colSpan=2><font color=$fontcolormisc>ÏûÏ¢À´×Ô<b>$from</b>£¬·¢ËÍ¸øÄúµÄÊ±¼ä£º<b>$date</b></font></td></tr>
<tr><td bgColor=$miscbackone valign=top colSpan=2><font color=$fontcolormisc>
<b>ÏûÏ¢±êÌâ£º$messagetitle</b>$attachfile<p>$post
<p align=right>$inboxtempone$inboxmsgup$inboxsplitline$inboxmsgdown$inboxtemptwo</p>
</td></tr>
<tr>
<td bgColor=$miscbacktwo valign=top width=20%><font color=$fontcolormisc><b>¿ìËÙ»Ø¸´£º</b></td> 
<td bgColor=$miscbacktwo>$remsg</td> 
</tr>
<tr> 
<form action=$thisprog method=POST name=FORM enctype="multipart/form-data"><input type=hidden name=action value="send"><input type=hidden name=touser value="$from"><input type=hidden name=msgtitle value="$remsg">
<td bgColor=$miscbackone valign=top width=20%><font color=$fontcolormisc><b>ÄÚÈİ£º</b></td> 
<td bgColor=$miscbackone><textarea cols=35 rows=4 name=message OnKeyDown="ctlent()"></textarea><br><input type=checkbox name=backup value=yes class=1><font color=$fontcolormisc>ÊÇ·ñ¸´ÖÆÒ»·İÏûÏ¢ÖÁ·¢¼şÏä£¿</font></td>
</tr>
~;
	if ($allowmsgattachment ne 'no')
	{
		my $addtypedisp = $addtype;
		$addtypedisp =~ s/\, /\,/ig;
		$addtypedisp =~ s/ \,/\,/ig;
		$addtypedisp =~ tr/A-Z/a-z/;
		my @addtypedisp = split(/\,/, $addtypedisp);
		$addtypedisp = "<select><option value=#>Ö§³ÖÀàĞÍ£º</option><option value=#>----------</option>";
		foreach (@addtypedisp)
		{
			chomp;
			next if ($_ eq "");
			$addtypedisp .= "<option>$_</option>";
		}
		$addtypedisp .= qq~</select>~;
		$output .= qq~
<tr>
<td bgColor=$miscbackone valign=top width=30%><font color=$fontcolormisc><b>¸½¼ş£º</b><br>(×î´ó <b>60</b> KB)</font></td>
<td bgColor=$miscbackone><input type=file size=30 name=addme><br>$addtypedisp</td>
</tr>
~;
	}
$output .= qq~
<tr><td bgColor=$miscbacktwo colSpan=2 align=center><input type=submit value="·¢ ËÍ" name=Submit>   <input type=reset name=Clear value="Çå ³ı"></td></form></tr>~;
}

elsif ($action eq "deleteall")
{
	my $filetotrash = $inwhere eq "inbox" ? "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi" : "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
	unlink($filetotrash);
	my $wherename = $inwhere eq "inbox" ? "ÊÕ¼şÏä" : "·¢¼şÏä";
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>ËùÓĞµÄ¶ÌÏûÏ¢ÒÑ±»É¾³ı</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>¡¡<a href=$thisprog?action=outbox>$outboxpm</a>¡¡<a href=$thisprog?action=new>$newpm</a>¡¡<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>¡¡<a href="javascript:openscript('blocklist.cgi', 420, 320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>ÄúÔÚ$wherenameÖĞµÄ¶ÌÏûÏ¢ÒÑ¾­È«²¿É¾³ı</b><br><br></td></tr>~;
}

elsif ($action eq "delete")
{
	@inmsg= $query->param("msg");
	my $filetoopen = $inwhere eq "inbox" ? "${lbdir}${msgdir}/in/${memberfilename}_msg.cgi" : "${lbdir}${msgdir}/out/${memberfilename}_out.cgi";
	my @boxmessages;

	&winlock($filetoopen) if ($OS_USED eq "Nt");
	if (open(FILE, $filetoopen)) {
		flock(FILE, 1) if ($OS_USED eq "Unix");
		sysread(FILE, my $boxmessages,(stat(FILE))[7]);
		close(FILE);
		$boxmessages =~ s/\r//isg;
		@boxmessages = split (/\n/, $boxmessages);
	}
	$count = 0;
	open (FILE, ">$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	foreach $line (@boxmessages) {
		chomp($line);
		my $checkmsg = 0;
		foreach (@inmsg)
		{
			if ($count eq $_)
			{
				$checkmsg = 1;
				last;
			}
		}
		print FILE "$line\n" if ($checkmsg == 0 && $line ne "");
		$count++;
	}
	close(FILE);
	&winunlock($filetoopen) if ($OS_USED eq "Nt");
	my $wherename = $inwhere eq "inbox" ? "ÊÕ¼şÏä" : "·¢¼şÏä";
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>ÏûÏ¢É¾³ı</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>¡¡<a href=$thisprog?action=outbox>$outboxpm</a>¡¡<a href=$thisprog?action=new>$newpm</a>¡¡<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>¡¡<a href="javascript:openscript('blocklist.cgi',420,320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>ÄúÔÚ$wherenameÖĞµÄ¶ÌÏûÏ¢ÒÑ¾­É¾³ı¡£<br><br>×Ô¶¯·µ»Ø$wherename<br><br></b></td></tr>
<meta http-equiv="refresh" Content="2; url=$thisprog?action=$inwhere">~;
}
elsif($action eq "disable_pm"){
	my $disable_pm_status = ($query->param('disable_pm_status') eq "¿ªÆô")?"¿ªÆô":"¹Ø±Õ";
	my $disable_pm_mess = &lbhz(&unHTML($query->param('mess')),40);
	my $memberfilename = $inmembername;
	$memberfilename =~ s/ /\_/g;
	$memberfilename =~ tr/A-Z/a-z/;
	my $messfilename = "${lbdir}${msgdir}/main/${memberfilename}_mian.cgi";
	if($disable_pm_status eq "¿ªÆô"){
		if (length($disable_pm_mess) == 0) {
			$disable_pm_mess = "¶Ô²»Æğ£¬ÎÒÏÖÔÚºÜÃ¦£¬ÇëÄúÉÔºóÔÙÁªÏµÎÒ¡£";
		}else {
			$disable_pm_mess =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\=\+\\\'\:\"\/\<\>\?\[\]]//isg;
		}
		if (open(FILE,">$messfilename")) {
			print FILE "$disable_pm_mess";
			close(FILE);
		}
	}else{
	    chomp $messfilename;
	    unlink ($messfilename) if (-e $messfilename);
	}
	$output .= qq~
<tr><td bgColor=$miscbacktwo align=center><font color=$fontcolormisc><b>¶ÌÏûÏ¢Ãâ´òÈÅ</b></td></tr>
<tr><td bgColor=$miscbackone align=center><a href=$thisprog?action=inbox>$inboxpm</a>¡¡<a href=$thisprog?action=outbox>$outboxpm</a>¡¡<a href=$thisprog?action=new>$newpm</a>¡¡<a href="javascript:openscript('friendlist.cgi', 420, 320)">$friendpm</a>¡¡<a href="javascript:openscript('blocklist.cgi',420,320)">$blockpm</a></td></tr>
<tr><td bgColor=$miscbackone align=center><font color=$fontcolormisc><b>ÄúÒÑ$disable_pm_statusÃâ´òÈÅÄ£Ê½¡£<br><br>×Ô¶¯·µ»ØÊÕ¼şÏä<br><br></b></td></tr>
<meta http-equiv="refresh" Content="2; url=$thisprog?action=inbox">~;
}
$memberfilename = $inmembername;
$memberfilename =~ s/ /\_/g;
$memberfilename =~ tr/A-Z/a-z/;
my $messfilename = "${lbdir}${msgdir}/main/${memberfilename}_mian.cgi";
my $disable_pm_mess ="";
if (open(FILE, $messfilename)){
	$disable_pm_mess = <FILE>;
	close(FILE);
}
$now_status=($disable_pm_mess ne "")?"¿ªÆô":"¹Ø±Õ";
$disable_pm_mess = "¶Ô²»Æğ£¬ÎÒÏÖÔÚºÜÃ¦£¬ÇëÄúÉÔºóÔÙÁªÏµÎÒ¡£" if (length($disable_pm_mess) == 0);

	my $cleanname = $intouser;
	$cleanname =~ tr/A-Z/a-z/;
	$cleanname =~ s/\_/ /g;
	$inmessage =~ s/<p>/\n\n/ig;
	$inmessage =~ s/<br>/\n/ig;

	if (open(FILE, "${lbdir}memfriend/${memberfilename}.cgi")) {
		my $currentlist = <FILE>;
		close(FILE);
		@currentlist = split (/\n/, $currentlist);
	}
	my $friendlist = "";
	foreach (@currentlist) {
		chomp;
		s/^£ª£££¡£¦£ª//isg;
		$friendlist .= qq~<option value="$_">$_</option>~;
	}

$output.=qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><br>

<form action=$thisprog method=POST><input type=hidden name=action value="disable_pm">
<p>
<SCRIPT>valigntop()</SCRIPT><table cellPadding=0 cellSpacing=0 width=$tablewidth bgColor=$tablebordercolor align=center><tr><td>
<table cellPadding=3 cellSpacing=1 width=100%><tr>
<td bgColor=$miscbacktwo align=center width="30%"><b>¶ÌÏûÏ¢Ãâ´òÈÅ×´Ì¬£º</b> <u style="color:$fonthighlight">$now_status</u></td>
<td bgColor=$miscbackone align=center><input type="text" name="mess" size=20 maxlength=40 value="$disable_pm_mess"></td>
<td bgColor=$miscbacktwo align=center width="25%"><input type="submit" value="¿ªÆô" name="disable_pm_status"> <input type="submit" value="¹Ø±Õ" name="disable_pm_status"></td>
</tr>
</form>~;

$output .= "</table></td></tr></table><SCRIPT>valignend()</SCRIPT>";
&output("$boardname - ¶ÌÏûÏ¢",\$output,"msg");

sub splitpage
{
	$maxthread = 9 if ($maxthread !~ /^[0-9]+$/);
	my $tmp = shift;
	my $instart = $query->param("start");
	$instart = 0 if ($instart !~ /^[0-9]+$/);
	$count = $instart;
	my $tempnumberofpages = $totalinboxmessages / $maxthread;
	my $numberofpages = int($tempnumberofpages);
	$numberofpages++ if ($numberofpages != $tempnumberofpages);

	if ($numberofpages > 1)
	{
		$startarray = $instart;
		$endarray = $instart + $maxthread - 1;
		$endarray = $totalinboxmessages - 1 if ($endarray >= $totalinboxmessages);

		my $currentpage = int($instart / $maxthread) + 1;
		my $endstart = ($numberofpages - 1) * $maxthread;
		my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?action=$tmp&start=0 title="Ê× Ò³" ><font face=webdings>9</font></a>~;
		my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?action=$tmp&start=$endstart title="Î² Ò³" ><font face=webdings>:</font></a>~;

		my $uppage = $currentpage - 1;
		my $nextpage = $currentpage + 1;
		my $upstart = $instart - $maxthread;
		my $nextstart = $instart + $maxthread;
		my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?action=$tmp&start=$upstart title="µÚ$uppageÒ³"><font face=webdings>7</font></a>~;
		my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?action=$tmp&start=$nextstart title="µÚ$nextpageÒ³"><font face=webdings>8</font></a>~;

		my $tempstep = $currentpage / 7;
		my $currentstep = int($tempstep);
		$currentstep++ if ($currentstep != $tempstep);
		my $upsteppage = ($currentstep - 1) * 7;
		my $nextsteppage = $currentstep * 7 + 1;
		my $upstepstart = ($upsteppage - 1) * $maxthread;
		my $nextstepstart = ($nextsteppage - 1) * $maxthread;
		my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?action=$tmp&start=$upstepstart class=hb title="µÚ$upsteppageÒ³">¡û</a> ~;
		my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?action=$tmp&start=$nextstepstart class=hb title="µÚ$nextsteppageÒ³">¡ú</a> ~;

		$pages = "";
		for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
		{
			last if ($i > $numberofpages);
			my $currentstart = ($i - 1) * $maxthread;
			$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?action=$tmp&start=$currentstart class=hb>$i</a> ~;
		}
		$pages = "<font color=$menufontcolor><b>¹² <font color=$fonthighlight>$numberofpages</font> Ò³</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font><br>";
	}
	else
	{
		$startarray = 0;
		$endarray = $totalinboxmessages - 1;
		$pages = "<font color=$menufontcolor>Ö»ÓĞÒ»Ò³</font><br>";
	}
	return;
}

sub Base64encode
#Base64±àÂëº¯Êı
{
	my $res = pack("u", $_[0]);
	$res =~ s/^.//mg;
	$res =~ s/\n//g;
	$res =~ tr|` -_|AA-Za-z0-9+/|;
	my $padding = (3 - length($_[0]) % 3) % 3;
	$res =~ s/.{$padding}$/'=' x $padding/e if $padding;
	return $res;
}

sub Base64decode
#Base64½âÂëº¯Êı
{
	local($^W) = 0;
	my $str = shift;
	my $res = '';
   
	$str =~ tr|A-Za-z0-9+/||cd;
	$str =~ tr|A-Za-z0-9+/| -_|;
	while ($str =~ /(.{1,60})/gs)
	{
		my $len = chr(32 + length($1)*3/4);
		$res .= unpack("u", $len . $1 );
	}
	return $res;
}
