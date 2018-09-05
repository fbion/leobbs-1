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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "code.cgi";
require "bbs.lib.pl";

$|++;

$thisprog  = "modscard.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");
$prog_dir  = "${lbdir}${msgdir}/modscarddata/";
mkdir($prog_dir,0777) if (!(-e $prog_dir));
$query	= new LBCGI;
$adscript="";
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
	$boardurltemp	= $boardurl;
	$boardurltemp	=~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath	= $boardurltemp;
	$cookiepath	=~ s/\/$//;
#	$cookiepath	=~ tr/A-Z/a-z/;
}
$currenttime = time;
if($lbbody !~/margin/i){
	$lbbody .=' topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0"';
}else{
	if($lbbody !~/topmargin/i){
		$lbbody .=' topmargin="0"';
	}else{
		$lbbody=~s/topmargin="?[0-9]+"?/topmargin="0"/i;
	}
	if($lbbody !~/leftmargin/i){
		$lbbody .=' leftmargin="0"';
	}else{
		$lbbody=~s/leftmargin="?[0-9]+"?/leftmargin="0"/i;
	}
	if($lbbody !~/rightmargin/i){
		$lbbody .=' rightmargin="0"';
	}else{
		$lbbody=~s/rightmargin="?[0-9]+"?/rightmargin="0"/i;
	}
	if($lbbody !~/bottommargin/i){
		$lbbody .=' bottommargin="0"';
	}else{
		$lbbody=~s/bottommargin="?[0-9]+"?/bottommargin="0"/i;
	}
}
if($lbbody !~/scroll/i){
	$lbbody .=' scroll="no"';
}else{
	$lbbody=~s/scroll="?[A-Z]+"?/scroll="no"/i;
}


#IP ç¦æ­¢
&ipbanned;

# -> param('action'));		#Ä£Ê½
$checkaction	= $query -> param('checkaction');				#¼ì²é¶¯×÷
$checkaction	= &cleaninput($checkaction);
$start_page	= int($query -> param('start_page'));			#ÏÖÔÚÒ³Êı
$otheraction_a	= $query -> param('otheraction_a');				#ÆäËû¶¯×÷
$otheraction_a	= &cleaninput($otheraction_a);
$otheraction_b	= $query -> param('otheraction_b');				#ÆäËû¶¯×÷
$otheraction_b	= &cleaninput($otheraction_b);
$otheraction_c	= $query -> param('otheraction_c');				#ÆäËû¶¯×÷
$otheraction_c	= &cleaninput($otheraction_c);
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");

&error("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

#È¡µÃ»áÔ±×ÊÁÏ
$inmembername	= $query -> cookie("amembernamecookie");
$inpassword		= $query -> cookie("apasswordcookie");
&page_error("ÆÕÍ¨´íÎó","ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") if(($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));

if ((!$inmembername) or ($inmembername eq "¿ÍÈË")){
	&page_error("ÆÕÍ¨´íÎó","Äú²»ÊÇÂÛÌ³µÄ¹ÜÀíÍÅ¶Ó£¡");
}else{
	&getmember($inmembername, "no");
	&page_error("ÆÕÍ¨´íÎó","ÃÜÂëÓëÓÃ»§Ãû²»Ïà·û£¬ÇëÖØĞÂµÇÂ¼£¡") if($inpassword ne $password);
	&page_error("ÆÕÍ¨´íÎó","ÓÃ»§Ã»ÓĞµÇÂ¼»ò×¢²á£¡") if($userregistered eq "no");
	&page_error("ÆÕÍ¨´íÎó","Äú²»ÊÇÂÛÌ³µÄ¹ÜÀíÍÅ¶Ó£¡") unless($membercode eq "ad" || $membercode eq "smo" || $membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo");
	$inmembername = $membername;
	$forum_ad = ($membercode eq "ad")?1:0;
}
$addtime = $mytimeadd * 3600 + $timezone * 3600;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
&whosonline("$inmembername\t°æÖ÷Ç©µ½\tboth\tÂÛÌ³°æÖ÷Ç©µ½\t") unless(-e "$filetoopens.lck");

$today_date = &longdate($currenttime+$addtime);
$output = "";
if($action eq "set_ad_announce" || $action eq "pcard_status" || $action eq "pcard_search" || $action eq "pcard_search_a"){
	&$action;
}else{
	&top_page;
}

#Êä³ö£ºÒ³Ãæ×ÊÁÏ

print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&output("$boardname - ÂÛÌ³°æÖ÷Ç©µ½",\$output,'msg');

sub top_page{
	my ($ad_announce,$ad_ann_date);
	if("${prog_dir}ad_announcement.cgi"){
		open(FILE,"${prog_dir}ad_announcement.cgi");
		$ad_ann_date = &fulldatetime((stat(FILE))[9]);
		$/="";
		$ad_announce = <FILE>;
		$/="\n";
		close(FILE);
		&lbcode(\$ad_announce);
		&doemoticons(\$ad_announce);
		&smilecode(\$ad_announce);
		chomp $ad_announce;
	}
	$ad_announce = "<br><br><br><center><i>ÔİÊ±Ã»ÓĞÈÎºÎ¹«¸æ</i></center>" if($ad_announce eq "");
	$ad_ann_date = "" if ($ad_ann_date eq "1970Äê01ÔÂ01ÈÕ 08:00am");
	my $today_log = "${prog_dir}$today_date.cgi";
	$pcard_or_not = 0;
	my (@get_today_log,$get_today_log_list);
	if(-e $today_log){
		open(FILE,$today_log);
		$/="";
		$get_today_log = <FILE>;
		$/="\n";
		close(FILE);
		$get_today_log =~s/[\n\r]/\_/g;
		$get_today_log =~s/^\_+//;
		$get_today_log =~s/\_+$//;
		$get_today_log = "\_$get_today_log\_";
		$pcard_or_not = 1 if($get_today_log=~/\_$inmembername\_/i);
		$get_today_log_list = $get_today_log;
		$get_today_log_list =~s/^\_+//;
		$get_today_log_list =~s/(.+?)\_/<option>$1<\/option>/gi;
	}
	if(!$pcard_or_not && $checkaction eq "pcard"){
		open(FILE,">>$today_log");
		print FILE "$inmembername\n";
		close(FILE);
		$pcard_or_not = 1;
		$get_today_log_list.=qq~<option>$inmembername</option>~;
	}
	
	$td_height = ($forum_ad)?163:238;
	$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$titlecolor" align="center" colspan="2" $catbackpic><font color="$fontcolormisc"><b>Ì³Ö÷¹«¸æ</b></font></td></tr>
<tr><td bgcolor="$miscbackone" valign="top" colspan="2" align="right">
<span style="height:$td_height;overflow:auto;padding:2px;color:$fontcolormisc;width:100%;text-align:left">
$ad_announce
</span><i>$ad_ann_date</i>
</td></tr>
<tr><td bgcolor="$miscbacktwo" align="center" colspan="2"><font color="$fontcolormisc"><b>´ò¿¨Ç©µ½</b></font></td></tr>~;
	if($pcard_or_not){
		$output .= qq~
<tr>
<td bgcolor="$miscbackone"><font color="$fontcolormisc">ÈÕÆÚ£º<i>$today_date<i></font></td>
<td bgcolor="$miscbackone" align="center"><b><font color="$fonthighlight">ÒÑ¾­Ç©µ½</font></b></td>
</tr>~;
	}else{
		$output .= qq~
<form action="$thisprog" method="GET">
<input type="hidden" name="checkaction" value="pcard">
<tr>
<td bgcolor="$miscbackone"><font color="$fontcolormisc">ÈÕÆÚ£º<i>$today_date<i></font></td>
<td bgcolor="$miscbackone" align="center"><input type="submit" value="Ç©µ½"></td>
</tr>
</form>~;
	}
	if($forum_ad){
		$output .= qq~
<tr>
<td bgcolor="$miscbacktwo"><select style="width:100%;background-color:$miscbacktwo"><option style="color:$fonthighlight;">½ñÌìÒÑÇ©µ½¹ÜÀíÔ±</option>$get_today_log_list</select></td>
<td bgcolor="$miscbacktwo" align="center"><font color="$fontcolormisc"><b>Ì³Ö÷¹ÜÀí</b></font></td>
</tr>
<form action="$thisprog" method="GET">
<input type="hidden" name="checkaction" value="pcard">
<tr>
<td bgcolor="$miscbackone" align="center" colspan="2">[<b><a href="$thisprog?action=set_ad_announce" target="_self">¸ü¸ÄÌ³Ö÷¹«¸æ</a></b>] [<b><a href="$thisprog?action=pcard_status" target="_self">²é¿´Ç©µ½¼ÇÂ¼</a></b>]</td>
</tr>
</form>~;
	}
	$output .= qq~
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}

sub set_ad_announce{
	&page_error("Ç©µ½¼ÇÂ¼","Ö»ÔÊĞíÌ³Ö÷¸ü¸Ä¹«¸æ£¡") unless($forum_ad);
	my $ad_announcement = "${prog_dir}ad_announcement.cgi";
	if($start_page != 0){
		open(FILE,">$ad_announcement");
		print FILE $checkaction;
		close(FILE);
		unlink($ad_announcement) if($checkaction eq "");
		$output = qq~<script>location.href="$thisprog";</script>~;
	}
	my ($ad_announce,$ad_ann_date);
	if(-e $ad_announcement){
		open(FILE,$ad_announcement);
		$ad_announce = <FILE>;
		close(FILE);
		$ad_announce =~s/<p>/\n\n/g;
		$ad_announce =~s/<br>/\n/g;
	}
	$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$titlecolor" align="center" colspan="2" $catbackpic><font color="$fontcolormisc"><b>Ì³Ö÷¹«¸æ</b></font></td></tr>
<form action="$thisprog" method="POST">
<input type="hidden" name="start_page" value="1">
<input type="hidden" name="action" value="set_ad_announce">
<tr><td bgcolor="$miscbackone" valign="top" align="center" colspan="2">
<textarea cols="60" rows="16" name="checkaction">$ad_announce</textarea><br>
¡ù¿ÉÒÔÊ¹ÓÃ LBCODE¡¡¡ù²»ÄÜÊ¹ÓÃ HTML
</td></tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50">
<< <a href="$thisprog">·µ»Ø</a>
</td>
<td bgcolor="$miscbackone" align="center" width="350"><input type="submit" value="¸ü¸Ä¹«¸æ" style="width:120px"></td>
</tr>
</form>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}

sub pcard_status{
	&page_error("Ç©µ½¼ÇÂ¼","Ö»ÔÊĞíÌ³Ö÷²é¿´Ç©µ½¼ÇÂ¼£¡") unless($forum_ad);
	$checkaction = ($checkaction =~/^[0-9]{4,4}Äê[0-9]{2,2}ÔÂ[0-9]{2,2}ÈÕ$/)?$checkaction:$today_date;
	my $that_day_log = "${prog_dir}$checkaction.cgi";
	if($start_page == -1) {
		$start_page = 0;
		unlink($that_day_log);
	}
	$no_log_that_day = (-e $that_day_log)?0:1;
	my $log_date_list = "";
	opendir(DIR,$prog_dir);
	foreach(readdir(DIR)){
		my $file_full_path = "${prog_dir}$_";
		unlink($file_full_path) if($_ =~/\_search.cgi/i && (stat($file_full_path))[9] < (time - 30*60));
		next if($_ eq "." || $_ eq ".." || $_ eq "index.html" || $_ eq "ad_announcement.cgi" || $_ eq "" || $_ =~/\_search.cgi/i);
		$_ =~s/\.cgi$//i;
		$log_date_list .=qq~<option value="$_">$_</option>~;
		if($no_log_that_day){
			$that_day_log = "${prog_dir}$_.cgi";
			$checkaction = $_;
		}
	}
	closedir(DIR);
	$checkaction_link = uri_escape($checkaction);
	$log_date_list =~s/value="$checkaction"/value="$checkaction" selected/;
	
	&page_error("Ç©µ½¼ÇÂ¼","Ã»ÓĞÈÎºÎÇ©µ½¼ÇÂ¼£¡") unless(-e $that_day_log);
	
	if($otheraction_a eq "search"){
		$that_day_log = "${prog_dir}$inmembername\_search.cgi";
		$checkaction = "ËÑÑ°Ç©µ½¼ÇÂ¼";
		$checkaction_link = "";
	}
	open(FILE,$that_day_log);
	my @memberdata = <FILE>;
	close(FILE);
	chomp @memberdata;
	my %memberdata = ();
	if($otheraction_a eq "search"){
		my @memberdata_b =@memberdata;
		foreach(@memberdata_b){
			my ($membername,$pcard_result) = split(/\t/,$_);
			next if($membername eq "");
			$memberdata{$membername}.="<u>$pcard_result</u><br>";
		}
		@memberdata = keys %memberdata;
	}
	@memberdata = sort alphabetically @memberdata;
	$total_member = @memberdata;
	&page_error("Ç©µ½¼ÇÂ¼","Ã»ÓĞÈÎºÎÇ©µ½¼ÇÂ¼£¡") unless($total_member);
	%membernameimg = ();
	$membernameimg{'ad'} = "<img src=$imagesurl/images/teamad.gif alt=´ËÈËÎªÌ³Ö÷ width=16 align='absmiddle'>";
	$membernameimg{'mo'} = "<img src=$imagesurl/images/teammo.gif alt=´ËÈËÎª°æÖ÷ width=16 align='absmiddle'>";
	$membernameimg{'amo'} = "<img src=$imagesurl/images/teamamo.gif alt=´ËÈËÎª¸±°æÖ÷ width=16 align='absmiddle'>";
	$membernameimg{'smo'} = "<img src=$imagesurl/images/teamsmo.gif alt=´ËÈËÎª×Ü°æÖ÷ width=16 align='absmiddle'>";
	$membernameimg{'cmo'} = "<img src=$imagesurl/images/teamcmo.gif alt=´ËÈËÎªÇø°æÖ÷ width=16 align='absmiddle'>";
	
	$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr>
<td bgcolor="$titlecolor" align="center" $catbackpic><a href="$thisprog?action=pcard_search"><font color="$fontcolormisc">[ËÑÑ°]</font></a></td>
<td bgcolor="$titlecolor" align="center" $catbackpic><font color="$fontcolormisc"><b>Ç©µ½¼ÇÂ¼ - $checkaction</b></font></td>
</tr>
<tr><td bgcolor="$miscbackone" valign="top" align="right" colspan="2">
<span style="height:230;overflow:auto;padding:2px;color:$fontcolormisc;width:100%;text-align:left">~;
	my $last_membername = 0;
	for($i=$start_page;($i<$start_page+5)&&($i<$total_member);$i++){
		my ($membername,$pcard_result) = split(/\t/,$memberdata[$i]);
		$pcard_result = '<font color="'.$fonthighlight.'">´Ë°æÖ÷ÓĞÔÚ±¾ÈÕÇ©µ½</font>' if($pcard_result eq "" || $otheraction_a ne "search");
		my $memberlinkname = uri_escape($membername);
		my $memberfilename = $membername;
		$memberfilename =~s/ /_/g;
		$memberfilename =~ tr/A-Z/a-z/;
		my $namenumber = &getnamenumber($memberfilename);
		&checkmemfile($memberfilename,$namenumber);
    		my $filetoopen = "${lbdir}$memdir/$namenumber/$memberfilename.cgi";
		open (FILE, "$filetoopen");
		$memberline = <FILE>;
		close (FILE);
		@userdetail = split (/\t/, $memberline);
		chomp @userdetail;
		undef $useravatar;
		if ($avatars eq "on") {
			if (($userdetail[22])&&($userdetail[23])&&($userdetail[24])) { #×Ô¶¨ÒåÍ·Ïñ´æÔÚ
				$userdetail[22] =~ s/\$imagesurl/${imagesurl}/o;
				if (($userdetail[22] =~ /\.swf$/i)&&($flashavatar eq "yes")) {
					$userdetail[22]=&uri_escape($userdetail[22]);
					$useravatar = qq(<OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$userdetail[23] HEIGHT=$userdetail[24]><PARAM NAME=MOVIE VALUE=$userdetail[22]><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$userdetail[22] WIDTH=$userdetail[23] HEIGHT=$userdetail[24] PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT></td>);
				}else{
					$userdetail[22]=&uri_escape($userdetail[22]);
					$useravatar = qq(<img src=$userdetail[22] border=0 width=$userdetail[23] height=$userdetail[24]>);
				}
			}elsif (($userdetail[18] ne "noavatar") && ($userdetail[18])) {
				$userdetail[18]=&uri_escape($userdetail[18]);
				$useravatar = qq(<img src="$imagesurl/avatars/$userdetail[18].gif" border="0">);
            }
            $useravatar = qq~<td rowspan="4" width="$maxposticonwidth" align="center">$useravatar</td>~ if(defined $useravatar);
        }
		$userdetail[13] = $userdetail[13] + ($userdetail[16] * 3600) + ($timezone * 3600);
		if ($userdetail[13]) { $userdetail[13] = &longdate ($userdetail[13]) } else { $userdetail[13] = "Unknown"; }
		$lastgone   = $userdetail[26];
		$lastgone   = $joineddate if($lastgone eq "");
		$today      = time-$lastgone;
		$novisitdate = int($today/(3600*24));
		$lastgone   = &dateformat($lastgone + ($timedifferencevalue*3600) + ($timezone*3600));
		if($novisitdate < 2){
			$visitresult=qq(´Ë°æÖ÷±È½ÏÇÚ¿ì);
		}elsif($novisitdate < 7){
			$visitresult=qq(´Ë°æÖ÷ £· ÌìÖ®ÄÚÓĞ·ÃÎÊ);
		}elsif($novisitdate < 15){
			$visitresult=qq(´Ë°æÖ÷ £±£µ ÌìÖ®ÄÚÓĞ·ÃÎÊ);
		}else{
			$visitresult=qq(´Ë°æÖ÷ÒÑÓĞºÜ¾ÃÎ´·ÃÎÊÂÛÌ³);
		}
		my $emailgraphic	= qq~<img src=$imagesurl/images/email.gif border=0 width=16 align=absmiddle style=filter:gray><font style=color:#444444 disabled>ÓÊ¼ş</font>~;
		my $homepagegraphic= qq~<img src=$imagesurl/images/homepage.gif border=0 width=16 align=absmiddle style=filter:gray><font style=color:#444444 disabled>Ö÷Ò³</font>~;
		my $oicqgraphic	= qq~<img src=$imagesurl/images/oicq.gif border=0 width=16 align=absmiddle style=filter:gray><font style=color:#444444 disabled>QQ</font>~;
		my $icqgraphic		= qq~<img src=$imagesurl/images/icq.gif border=0 width=16 align=absmiddle style=filter:gray><font style=color:#444444 disabled>ICQ</font>~;
	        $userdetail[5] = &encodeemail($userdetail[5]);
	        $userdetail[6] = "no" if ($dispmememail eq "no");
		if ($userdetail[6] eq "yes") { 
			$emailgraphic = qq~<a href=mailto:$userdetail[5] title=µç×ÓÓÊ¼şµØÖ·><img src=$imagesurl/images/email.gif border=0 width=16 align=absmiddle>ÓÊ¼ş</a>~;
		} elsif ($userdetail[6] eq "msn") {
			$emailgraphic = qq~<a href=mailto:$userdetail[5] title="MSN µØÖ·"><img src=$imagesurl/images/msn.gif border=0 width=16 align=absmiddle>MSN</a>~;
		} elsif ($userdetail[6] eq "popo"){
                       $emailgraphic = qq~<a href=mailto:$userdetail[5] title="ÅİÅİµØÖ·"><img src=$imagesurl/images/popo.gif border=0 width=16 align=absmiddle>ÅİÅİ</a>~;
		}
		if ($userdetail[8]=~/^([a-z]+?:\/\/){1}([a-z0-9\-\.,\?!%\*_\#:;~\\&$@\/=\+\(\)]+)/i) {
			$homepagegraphic = qq~<a href="$userdetail[8]" target=_blank title="·ÃÎÊ $membername µÄÖ÷Ò³"><img src=$imagesurl/images/homepage.gif border=0 width=16 align=absmiddle>Ö÷Ò³</a>~;
		}
		if (($userdetail[9]) && ($userdetail[9] =~ /^[0-9]+$/)) {
			$oicqgraphic = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$userdetail[9] target=_blank title="²é¿´ QQ:$userdetail[9] µÄ×ÊÁÏ"><img src=$imagesurl/images/oicq.gif border=0 width=16 align=absmiddle>QQ</a>~;
		}
		if (($userdetail[10]) && ($userdetail[10] =~ /^[0-9]+$/)) {
			$icqgraphic = qq~<span style="cursor:hand" onClick="javascript:openScript('misc.cgi?action=icq&UIN=$userdetail[10]',450,300)" title="¸ø ICQ:$userdetail[10] ·¢¸öÏûÏ¢"><img src=$imagesurl/images/icq.gif border=0 width=16 align=absmiddle>ICQ</span>~;
		}
		if($otheraction_a ne "search"){
		$output .= qq~
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="$maxposticonheight" style="border:1 solid $tablebordercolor">
<tr>$useravatar<td>$membernameimg{$userdetail[3]} <b><a href="profile.cgi?action=show&member=$memberlinkname" title="²é¿´$membernameµÄ¸öÈË×ÊÁÏ" target=_blank><u>$membername</u></a></b></td></tr>
<tr>
<td>
<font color="$fontcolormisc">×îºóÀ´·Ã£º<i>$lastgone</i><br>
Ê§×ÙÌìÊı£º¹² <b>$novisitdate</b> Ìì<br>
ÆÀ¶¨½á¹û£º<b><font color="$fonthighlight">$visitresult</font></b></font></td>
</tr>
<tr>
<td><font color="$fontcolormisc">$homepagegraphic $emailgraphic $oicqgraphic $icqgraphic</font></td>
</tr>
<tr>
<td><u>$pcard_result</u></td>
</tr>
</table><br>~;
		}else{
				$output .= qq~
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="$maxposticonheight" style="border:1 solid $tablebordercolor">
<tr>$useravatar<td>$membernameimg{$userdetail[3]} <b><a href="profile.cgi?action=show&member=$memberlinkname" title="²é¿´$membernameµÄ¸öÈË×ÊÁÏ"><u>$membername</u></a></b></td></tr>
<tr>
<td><span style="height:100;overflow:auto;padding:2px;color:$fontcolormisc;width:100%;">$memberdata{$membername}</span></td>
</tr>
</table><br>~;
		}
	}
	$page_link = &page_link_gen($total_member,8,$start_page,5,"start_page","action=pcard_status&checkaction=$checkaction_link&otheraction_a=$otheraction_a",$thisprog,$fontcolormisc,$fonthighlight);
	$output .= qq~
</span>$page_link
</td></tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50">
<< <a href="$thisprog">·µ»Ø</a>
</td>
<form action="$thisprog" method="GET">
<input type="hidden" name="action" value="pcard_status">
<td bgcolor="$miscbackone" align="center" width="350">
<select name="checkaction" style="width:120px">$log_date_list</select> <input type="submit" value="²é¿´Ç©µ½¼ÇÂ¼"> 
[<a href="$thisprog?action=pcard_status&checkaction=$checkaction_link&start_page=-1" target="_self">É¾³ı¼ÇÂ¼</a>]
</td>
</form>
</tr>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}

sub pcard_search{
	my $log_date_list = "";
	my $log_date_list_b = "";
	opendir(DIR,$prog_dir);
	foreach(readdir(DIR)){
		next if($_ eq "." || $_ eq ".." || $_ eq "index.html" || $_ eq "ad_announcement.cgi" || $_ eq "" || $_ =~/\_search.cgi/i);
		$_ =~s/\.cgi$//i;
		$log_date_list .=qq~<option value="$_">$_µÄ¼ÇÂ¼</option>~;
		$log_date_list_b .=qq~<option value="$_">$_</option>~;
	}
	closedir(DIR);
	$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$titlecolor" align="center" colspan="2" $catbackpic><font color="$fontcolormisc"><b>ÀàĞÍËÑÑ°</b></font></td></tr>
<form action="$thisprog" method="POST">
<input type="hidden" name="start_page" value="1">
<input type="hidden" name="action" value="pcard_search_a">
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>¼ÇÂ¼</b></td>
<td bgcolor="$miscbackone" align="left" width="350"><select name="checkaction" style="width:150px"><option value="ËùÓĞ">ËÑÑ°ËùÓĞ¼ÇÂ¼</option>$log_date_list</select></td>
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>ÀàĞÍ</b></td>
<td bgcolor="$miscbackone" align="left" width="350"><input type="checkbox" name="otheraction_a" value="ad"> Ì³Ö÷ <input type="checkbox" name="otheraction_a" value="smo"> ×Ü°æÖ÷ <input type="checkbox" name="otheraction_a" value="cmo"> Çø°æÖ÷ <input type="checkbox" name="otheraction_a" value="mo"> °æÖ÷ <input type="checkbox" name="otheraction_a" value="amo"> ¸±°æÖ÷ </td>
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>·½Ê½</b></td>
<td bgcolor="$miscbackone" align="left" width="350">
<input type="radio" name="otheraction_b" value="1" checked> ÔÚËùÑ¡¼ÇÂ¼ÖĞËÑÑ°ÓĞÇ©µ½µÄËùÑ¡ÀàĞÍ<br>
<input type="radio" name="otheraction_b" value="2"> ÔÚËùÑ¡¼ÇÂ¼ÖĞËÑÑ°Ã»ÓĞÇ©µ½µÄËùÑ¡ÀàĞÍ<br>
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" colspan="2"><input type="submit" value="¿ªÊ¼ËÑÑ°" style="width:120px"></td>
</tr>
</form>
<tr><td bgcolor="$titlecolor" align="center" colspan="2" $catbackpic><font color="$fontcolormisc"><b>»áÔ±ËÑÑ°</b></font></td></tr>
<form action="$thisprog" method="POST">
<input type="hidden" name="start_page" value="2">
<input type="hidden" name="action" value="pcard_search_a">
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>»áÔ±</b></td>
<td bgcolor="$miscbackone" align="left" width="350"><input type="text" name="otheraction_a" value="" size="30"> ÒÔ°ëĞÎ¶ººÅ(,)·Ö¸ô
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>·½Ê½</b></td>
<td bgcolor="$miscbackone" align="left" width="350">
<input type="radio" name="otheraction_b" value="1" checked> ÔÚËùÓĞ¼ÇÂ¼ÖĞËÑÑ°ÓĞÇ©µ½µÄÊäÈë»áÔ±<br>
<input type="radio" name="otheraction_b" value="2"> ÔÚËùÓĞ¼ÇÂ¼ÖĞËÑÑ°Ã»ÓĞÇ©µ½µÄÊäÈë»áÔ±<br>
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" colspan="2"><input type="submit" value="¿ªÊ¼ËÑÑ°" style="width:120px"></td>
</tr>
</form>
<tr>
<td bgcolor="$miscbackone" align="center" width="50">
<< <a href="$thisprog">·µ»Ø</a>
</td>
<form action="$thisprog" method="GET">
<input type="hidden" name="action" value="pcard_status">
<td bgcolor="$miscbackone" align="center" width="350">
<select name="checkaction" style="width:120px">$log_date_list_b</select> <input type="submit" value="²é¿´Ç©µ½¼ÇÂ¼"> 
</td>
</form>
</tr>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}
sub pcard_search_a{
	if($start_page == 1){
		#Òª SEARCH µÄîĞÍ
		my @otheraction_a = $query -> param('otheraction_a');
		my $otheraction_a = join("\_",@otheraction_a);
		$otheraction_a = &cleaninput($otheraction_a);
		$otheraction_a .="\_";
		my @memberdata;
		#ßx³öÄÇ(Ğ©)îĞÍ
		my %membernamecode = ('ad' => 1,'smo' => 2,'cmo' => 3,'mo' => 4,'amo' => 5);
		open (FILE, "$lbdir/data/lbmember.cgi");
		while(<FILE>){
			my @tmpuserdetail = split (/\t/, $_);
			chomp @tmpuserdetail;
			next unless(defined $membernamecode{$tmpuserdetail[1]});
			push(@memberdata,$tmpuserdetail[0]) if($otheraction_a=~/$tmpuserdetail[1]\_/i);
		}
		chomp @memberdata;
		close (FILE);
		#Òª SEARCH µÄÓ›ä›
		my (@log_selected);
		if($checkaction eq "ËùÓĞ"){
			opendir(DIR,$prog_dir);
			foreach(readdir(DIR)){
				next if($_ eq "." || $_ eq ".." || $_ eq "index.html" || $_ eq "ad_announcement.cgi" || $_ eq "" || $_ =~/\_search.cgi/i);
				push(@log_selected,$_);
			}
			closedir(DIR);
		}else{
			my $that_day_log = "${prog_dir}$checkaction.cgi";
			push(@log_selected,"$checkaction\.cgi") if(-e $that_day_log);
		}
		#é_Ê¼ SEARCH
		my $i=0;
		my (@have_pcard,@have_not_pcard);
		my $search_file = "${prog_dir}$inmembername\_search.cgi";
		unlink $search_file;
		foreach $log_file(@log_selected){
			my $log_file_date = substr($log_file,0,-4);
			my $that_day_log = "${prog_dir}$log_file";
			next unless(-e $that_day_log);
			open(FILE,$that_day_log);
			$/="";
			my $get_that_day_log = <FILE>;
			$/="\n";
			close(FILE);
			$get_that_day_log =~s/[\n\r]/\_/g;
			$get_that_day_log =~s/^\_+//;
			$get_that_day_log =~s/\_+$//;
			
			$get_that_day_log = "\_$get_that_day_log\_";
			open(SFILE,">>$search_file");
			foreach $membername(@memberdata){
				if($get_that_day_log=~/\_$membername\_/i){
					print SFILE "$membername\t<font color=\"$fonthighlight\">´Ë°æÖ÷ÓĞÔÚ$log_file_dateÇ©µ½</font>\n" if($otheraction_b == 1);
				}else{
					print SFILE "$membername\t<font color=\"$fontcolormisc\">´Ë°æÖ÷Ã»ÓĞÔÚ$log_file_dateÇ©µ½</font>\n" if($otheraction_b == 2);
				}
			}
			close(SFILE);
			$i++;
		}
		&page_error("Ç©µ½¼ÇÂ¼","Ã»ÓĞÈÎºÎÇ©µ½¼ÇÂ¼£¡") unless($i);
	}else{
		#Òª SEARCH µÄ»áÔ±
		my @otheraction_a = split(/\,/,$otheraction_a);
		my @memberdata;
		my %membernamecode = ('ad' => 1,'smo' => 2,'cmo' => 3,'mo' => 4,'amo' => 5);
		foreach $membername(@otheraction_a){
			my $memberfilename = $membername;
			$memberfilename =~s/ /_/g;
			$memberfilename =~ tr/A-Z/a-z/;
			my $namenumber = &getnamenumber($memberfilename);
			&checkmemfile($memberfilename,$namenumber);
	    		my $filetoopen = "${lbdir}$memdir/$namenumber/$memberfilename.cgi";
			open (FILE, "$filetoopen");
			$memberline = <FILE>;
			close (FILE);
			@userdetail = split (/\t/, $memberline);
			chomp @userdetail;
			push(@memberdata,$userdetail[0]) if(defined $membernamecode{$userdetail[3]});
		}
		#Òª SEARCH µÄÓ›ä›
		my @log_selected;
		opendir(DIR,$prog_dir);
		foreach(readdir(DIR)){
			next if($_ eq "." || $_ eq ".." || $_ eq "index.html" || $_ eq "ad_announcement.cgi" || $_ eq "" || $_ =~/\_search.cgi/i);
			push(@log_selected,$_);
		}
		closedir(DIR);
		#é_Ê¼ SEARCH
		my $i=0;
		my (@have_pcard,@have_not_pcard);
		my $search_file = "${prog_dir}$inmembername\_search.cgi";
		unlink $search_file;
		foreach $log_file(@log_selected){
			my $log_file_date = substr($log_file,0,-4);
			my $that_day_log = "${prog_dir}$log_file";
			next unless(-e $that_day_log);
			open(FILE,$that_day_log);
			$/="";
			my $get_that_day_log = <FILE>;
			$/="\n";
			close(FILE);
			$get_that_day_log =~s/[\n\r]/\_/g;
			$get_that_day_log =~s/^\_+//;
			$get_that_day_log =~s/\_+$//;
			
			$get_that_day_log = "\_$get_that_day_log\_";
			open(SFILE,">>$search_file");
			foreach $membername(@memberdata){
				if($get_that_day_log=~/\_$membername\_/i){
					print SFILE "$membername\t<font color=\"$fonthighlight\">´Ë°æÖ÷ÓĞÔÚ$log_file_dateÇ©µ½</font>\n" if($otheraction_b == 1);
				}else{
					print SFILE "$membername\t<font color=\"$fontcolormisc\">´Ë°æÖ÷Ã»ÓĞÔÚ$log_file_dateÇ©µ½</font>\n" if($otheraction_b == 2);
				}
			}
			close(SFILE);
			$i++;
		}
		&page_error("Ç©µ½¼ÇÂ¼","Ã»ÓĞÈÎºÎÇ©µ½¼ÇÂ¼£¡") unless($i);
	}
	$output = qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$miscbacktwo" align="center" height="20" $catbackpic><font color="$fontcolormisc"><b>ËÑÑ°Íê³É</b></font></td></tr>
<tr><td bgcolor="$miscbackone" valign="top">
<font color="$fontcolormisc">
<b>ÒÑ¾­Íê³ÉËÑÑ°£º</b>
<ul>
<li><b>ÒÑ¾­½¨Á¢ĞèÒªµÄËÑÑ°¼ÇÂ¼</b>
<li><a href="$thisprog?action=pcard_status&checkaction=$checkaction_link&otheraction_a=search">Èç¹ûÄúµÄä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÌøÒ³£¬Çë°´ÕâÀï</a>
</ul>
<meta http-equiv="refresh" content="2; url=$thisprog?action=pcard_status&checkaction=$checkaction_link&otheraction_a=search">
</font>
</td></tr>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}

sub page_error{
	my ($where,$errormsg) = @_;

	$output = qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="2" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$miscbacktwo" align="center" $catbackpic><font color="$fontcolormisc"><b>´íÎó£º $where</b></font></td></tr>
<tr><td bgcolor="$miscbackone" valign="top">
<font color="$fontcolormisc">
<b>¹ØÓÚ$whereµÄÏêÏ¸Ô­Òò£º</b>
<ul>
<li><b>$errormsg</b>
<li>ÄúÊÇ·ñĞèÒª²é¿´<span style="cursor:hand" onClick="javascript:openScript('help.cgi',500,400)">°ïÖúÎÄ¼ş</span>?
</ul>
<b>²úÉú$where´íÎóµÄ¿ÉÄÜÔ­Òò£º</b>
<ul>
<li>ÃÜÂë´íÎó
<li>ÓÃ»§Ãû´íÎó
<li>Äú²»ÊÇ<a href="register.cgi" target="_blank">×¢²á</a>ÓÃ»§
</ul>
<br><br><center><font color=$fontcolormisc> << <a href="javascript:history.go(-1)">·µ»ØÉÏÒ»Ò³</a></center>
</font>
</td></tr>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
	&output("$boardname - ÂÛÌ³°æÖ÷Ç©µ½",\$output,'msg');
	exit;
}

sub page_link_gen{
	#ÒıÊı£ºÏîÄ¿×ÜÊı£¬ÏÔÊ¾ÊıÁ¿£¬ÏÖÊ±Î»ÖÃ£¬£Ï£Æ£Æ£Ó£Å£Ô£¬±äÊıÃû£¬´«µİ±äÊı£¬³ÌĞòÃû³Æ£¬Í¨³£ÑÕÉ«£¬¼ÓÖØÑÕÉ«£¬Á¬½áÄ¿±ê£¬ÎÄ×ÖÑùÊ½
	my ($total_count,$disp_count,$now_count,$each_count,$var_this,$var_add,$this_prog,$color_a,$color_b,$link_target,$link_temp) = @_;
	#³õÊ¼»¯£ºËùÓĞĞèÒªÖµ
	my ($link_s,$link_e,$this_count,$this_dec,$i,$count,$uplink_page,$downlink_page,$link_of_page,$now_page);
	$total_count= int($total_count);				#±äÊı´¦Àí£ºÏîÄ¿×ÜÊı£¨”µÖµ»¯£©
	$disp_count	= int($disp_count);					#±äÊı´¦Àí£ºÏÔÊ¾ÊıÁ¿£¨”µÖµ»¯£©
	$now_count	= int($now_count);					#±äÊı´¦Àí£ºÏÖÊ±Î»ÖÃ£¨”µÖµ»¯£©
	$var_this	=~s/[^A-Za-z0-9\_]//g;				#±äÊı´¦Àí£º±äÊıÃû¡¡£¨É¾³ıÓ¢Êı×ÖÒÔÍâ×Ö´®£©
	$color_a	= "#333333" if($color_a eq "");		#±äÊı´¦Àí£ºÍ¨³£ÑÕÉ«£¨Ä¬ÈÏ£º#333333£©
	$color_b	= "#990000" if($color_b eq "");		#±äÊı´¦Àí£º¼ÓÖØÑÕÉ«£¨Ä¬ÈÏ£º#990000£©
	$link_target= "_self" if($link_target eq "");	#±äÊı´¦Àí£ºÁ¬½áÄ¿±ê£¨Ä¬ÈÏÎªÄ¿Ç°¿ò£©
	#¼ì²é±ØĞèÖµ£¬ÈçÎŞ£¨ÈÎºÎ£©·µ»Ø£ºÏÔÊ¾ÊıÁ¿£¬£Ï£Æ£Æ£Ó£Å£Ô£¬±äÊıÃû
	goto RETURN if($disp_count < 0 || $each_count < 0 || $var_this eq "");
	#ÔO¶¨ÎÄ×ÖÑùÊ½£ºÎÄ×ÖÑùÊ½µÄÔ¤ÉèÖµ
	$link_temp		= qq~<font color="$color_a"><b>¹² <font color="$color_b">%d</font> Ò³</b> %s [ %s ] %s</font>~ unless(defined $link_temp && $link_temp=~/\%d.*\%s.*%s.*%s/);
	#È¡µÃÄ¿Ç°³ÌĞòÃû³Æ£º³ÌĞòÃû³ÆµÄÔ¤ÉèÖµ
	$this_prog		= substr($ENV{'SCRIPT_NAME'},rindex($ENV{'SCRIPT_NAME'},"/")+1) unless(defined $this_prog && $this_prog ne "");
	#ÏÖËùÔÚÒ³
	$now_page= ($now_count/$each_count)+1;
	#×ÜÒ³Êı
	($this_count,$this_dec) = split(/\./,($total_count/$each_count));	#¼ÆËã×ÜÒ³Êı£ºÏîÄ¿×ÜÊı³ı£Ï£Æ£Æ£Ó£Å£Ô
	$this_count++ if($this_dec > 0);									#½øÎ»£ºÎŞÌõ¼ş
	$this_count=1 if(!$this_count);										#ÕıÊı»¯£º×îÉÙ£±
	#»ØÈ¦Ìõ¼ş£º
	$link_s = $now_page-int($disp_count/2);#¿ªÊ¼
	$link_e = $now_page+int($disp_count/2);#½áÊø
	#»ØÈ¦Ìõ¼ş´¦Àí£º¿ªÊ¼Ìõ¼şÉÙì¶×ÜÒ³Êı
	if($link_s < 0){
		$link_e += (0 - $link_s);
		$link_s = 0;
	}
	#»ØÈ¦Ìõ¼ş´¦Àí£º½áÊøÌõ¼ş´óì¶£°
	if($link_e > $this_count){
		$link_s -= ($link_e - $this_count);
		$link_e = $this_count;
	}
	#´¦Àí£ºÌøÒ³ÏÔÊ¾
	my @PARRAY = ($link_s..$link_e);
	$link_of_page = join("  ",@PARRAY);
	$link_of_page =~s/^\s+//;
	$link_of_page =~s/\s+$//;
	$link_of_page = " $link_of_page ";
	$link_of_page =~s/ (-?[0-9]+) /
		my $i=$1;
		my $return_t="";
		my $link_c= $i*$each_count;							#Ò³£Ï£Æ£Æ£Ó£Å£Ô
		my $page_c= $i+1;									#´¦ÀíÒ³Êı
		if($link_c != $now_count){
			#²»µÈì¶ÏÖ£Ï£Æ£Æ£Ó£Å£Ô£ºÏÔÊ¾Êı×ÖÁ¬½á
			$return_t=qq~<a href="$this_prog?$var_this=$link_c&$var_add" title="µÚ $page_c Ò³" style="color:$color_a" target="$link_target"><b>$page_c<\/b><\/a> ~;
		}else{
			#ÏàµÈì¶ÏÖ£Ï£Æ£Æ£Ó£Å£Ô£ºÏÔÊ¾´¿Êı×Ö
			$return_t=qq~<font color="$color_b"><b>$page_c<\/b><\/font> ~;
		}
		$count++;#µİÔö£ºÏÖÏÔÊ¾Êı
		$return_t="" if($count > $disp_count || $i >= $this_count || $i < 0);
		$return_t;
		/ge;
	#³ıÈ¥×îÎ²µÄ¿Õ¸ñ
	chop $link_of_page;
	#´¦Àí£ºÏòÉÏÌøÒ³
	$uplink_page		= qq~<font color="$color_b" face="webdings">9</font> <font color="$color_b" face="webdings">7</font>~;
	if($now_count > 0){
		#²»ì¶Ê×Ò³£¬¼ÓÉÏÏòÉÏÌøÒ³µÄÁ¬½á
		my $perv_page = $now_page-1;
		my $perv_page_count = ($perv_page-1)*$each_count;
		$uplink_page=qq~<a href="$this_prog?$var_this=0&$var_add" title="Ê× Ò³" target="$link_target"><font face="webdings" color="$color_a">9</font></a> <a href="$this_prog?$var_this=$perv_page_count&$var_add" title="µÚ $perv_page Ò³" target="$link_target"><font face="webdings" color="$color_a">7</font></a>~;
	}
	#´¦Àí£ºÏòÏÂÌøÒ³
	$downlink_page	= qq~<font color="$color_b" face="webdings">8</font> <font color="$color_b" face="webdings">:</font>~;
	if($now_count < ($this_count-1)*$each_count){
		#²»ì¶Î²Ò³£¬¼ÓÉÏÏòÏÂÌøÒ³µÄÁ¬½á
		my $last_page_count = ($this_count-1)*$each_count;
		my $next_page = $now_page+1;
		my $next_page_count = ($next_page-1)*$each_count;
		$downlink_page=qq~<a href="$this_prog?$var_this=$next_page_count&$var_add" title="µÚ $next_page Ò³" target="$link_target"><font face="webdings" color="$color_a">8</font></a> <a href="$this_prog?$var_this=$last_page_count&$var_add" title="Î² Ò³" target="$link_target"><font face="webdings" color="$color_a">:</font></a>~;
	}
	$link_of_page = sprintf($link_temp,$this_count,$uplink_page,$link_of_page,$downlink_page);
	#·µ»Ø£ºÁ¬½áÒ³×ÊÁÏ
	RETURN:
	return $link_of_page;
}
