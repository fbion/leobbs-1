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
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "data/cityinfo.cgi";
require "data/mpic.cgi";
require "bbs.lib.pl";

opendir (DIRS, "$lbdir");
my @files = readdir(DIRS);
closedir (DIRS);
@files = grep(/^\w+?$/i, @files);
my @ftpdir = grep(/^ftpdata/i, @files);
$ftpdir = $ftpdir[0];

require "$ftpdir/conf.cgi";

$|++;
$thisprog = "ftp.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

&ipbanned;


if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else
{
	my $boardurltemp = $boardurl;
	$boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath = $boardurltemp;
	$cookiepath =~ s/\/$//;
}

$inmembername = $query->cookie("amembernamecookie") unless ($inmembername);
$inpassword = $query->cookie("apasswordcookie") unless ($inpassword);
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t]//isg;
$cleanmembername = $inmembername;
$cleanmembername =~ s/ /\_/sg;
$cleanmembername =~ tr/A-Z/a-z/;
$ftplockfile = "${lbdir}lock/$cleanmembername\_ftpiii.lck";
$currenttime = time;
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");
&error("æ™®é€šé”™è¯¯&è€å¤§ï¼Œåˆ«ä¹±é»‘æˆ‘çš„ç¨‹åºå‘€ï¼") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

if ($inmembername eq "" || $inmembername eq "å®¢äºº")
{#æ£€æŸ¥ç”¨æˆ·èº«ä»½
	&error("æ™®é€šé”™è¯¯&è®¿å®¢ä¸èƒ½æŸ¥çœ‹FTP è”ç›Ÿ,è¯·å…ˆç™»å½•ï¼");
}
else
{
	&getmember($inmembername, 'no');
	&error("æ™®é€šé”™è¯¯&æ­¤ç”¨æˆ·æ ¹æœ¬ä¸å­˜åœ¨ï¼") if ($userregistered eq "no");
	&error("æ™®é€šé”™è¯¯&å¯†ç ä¸ç”¨æˆ·åä¸ç›¸ç¬¦ï¼Œè¯·é‡æ–°ç™»å½•ï¼") if ($inpassword ne $password);
	&error("æƒé™é”™è¯¯&è¢«å±è”½æ–‡ç« æˆ–ç¦è¨€çš„ç”¨ÈÏÖÏó
	if (-e $ftplockfile)
	{
		&myerror("Ë¢ĞÂ´íÎó&Çë²»ÒªË¢ĞÂFTPÁªÃËÌ«¿ì£¡") if ($currenttime < (stat($ftplockfile))[9] + 3);
	}
	open(LOCKCALFILE, ">$ftplockfile");
	close(LOCKCALFILE);

	$myallmoney = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
}

if (($membercode ne "ad")&&($plugstats eq "close")) {
    unlink($ftplockfile);
    &error("ÆÕÍ¨´íÎó&FTP ÁªÃËÒÑ¾­±»¹ÜÀíÔ±ÔİÊ±¹Ø±Õ£¡");
}

$action = $query->param("action");
my %Mode = (
	"view"	=> \&view,	#²é¿´Ä³¸öFTPµÄµÇÂ¼×ÊÁÏ
	"poll"	=> \&poll,	#¸øÄ³¸öFTP´ò·Ö
	"add"	=> \&add,	#Ìí¼ÓÒ»¸öFTPµÇÂ¼×ÊÁÏ
	"addok"	=> \&addok,
	"edit"	=> \&edit,	#±à¼­Ò»¸öFTPµÇÂ¼×ÊÁÏ
	"editok"=> \&editok,
	"info"	=> \&info,	#²éÑ¯FTPµÄ¹ºÂò¼ÇÂ¼
	"delete"=> \&delete,	#É¾³ıÒ»¸öFTPµÇÂ¼×ÊÁÏ
	"up"	=> \&up,	#ÌáÉıFTPÔÚÁªÃËÖĞµÄÎ»ÖÃ
	"repair"=> \&repair,	#ÖØ½¨ÁªÃËË÷Òı
	"config"=> \&config	#ÅäÖÃ³ÌĞòÉèÖÃ
);

if ($Mode{$action})
{
	$Mode{$action}->();
}
else
{
	&list;
}

unlink($ftplockfile);
print header(-cookie=>[$onlineviewcookie], -charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&output("$boardname - FTP ÁªÃË",\$output);
exit;

sub list
{
	my $onlineview = $query->cookie("onlineview");
	$onlineview = 0 if ($onlineview eq "");
	$onlineview = $onlineview == 1 ? 0 : 1 if ($action eq "onlineview");
	$onlineviewcookie = cookie(-name=>"onlineview", -value=>"$onlineview", -path=>"$cookiepath/", -expires=>"+30d");
	my $onlinetitle = $onlineview == 1 ? "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>¹Ø±ÕÏêÏ¸ÁĞ±í</font></a>]" : "[<a href=$thisprog?action=onlineview><font color=$titlefontcolor>ÏÔÊ¾ÏêÏ¸ÁĞ±í</font></a>]";

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬²¢»ñµÃÔÚÏßÁĞ±í
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	unless (-e "$filetoopens.lck")
	{
		$screenmode = $query->cookie("screenmode");
		$screenmode = 8 if ($screenmode eq "");
		&whosonline("$inmembername\tFTP ÁªÃË\tFTP ÁªÃË\t²é¿´ FTP ÁªÃËÁĞ±í");
		$membertongji =~ s/±¾·ÖÂÛÌ³/FTP ÁªÃË/o;
		undef $memberoutput if ($onlineview != 1);
	}
	else
	{
		$memberoutput = "";
		$membertongji = " <b>ÓÉÓÚ·şÎñÆ÷·±Ã¦£¬ËùÒÔ FTP ÁªÃËµÄÔÚÏßÊı¾İÔİÊ±²»Ìá¹©ÏÔÊ¾¡£</b>";
		$onlinetitle = "";
	}

	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(LIST, $listtoupdate);
	flock(LIST, 1) if ($OS_USED eq "Unix");
	my @ftpinfos = <LIST>;
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#Í·²¿Êä³öºÍÔÚÏßÍ³¼Æ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT><table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr>
	<td bgcolor=$titlecolor width=92% $catbackpic><font color=$titlefontcolor>$membertongji¡¡ $onlinetitle</td>
	<td bgcolor=$titlecolor width=8% align=center $catbackpic><a href="javascript:this.location.reload()"><img src=$imagesurl/images/refresh.gif border=0 width=40 height=12></a></td>
</tr>~;
	$output .= qq~\n<tr><td colspan=2 bgcolor=$forumcolorone $otherbackpic><table cellPadding=1 cellSpacing=0>$memberoutput</table><script language="JavaScript"> function O9(id) {if(id != "") window.open("profile.cgi?action=show&member=" + id);}</script></td></tr>~ if ($onlineview == 1 && $memberoutput);
	$output .= qq~
</table></td></tr></table><SCRIPT>valignend()</SCRIPT><p>
<script language="JavaScript">
function Closed()
{
	alert("Õâ¸ö FTP Ä¿Ç°±»ÔİÊ±¹Ø±ÕÁË£¡");
	return false;
}
function LeastRate()
{
	alert("ÄãµÄÍşÍûÖµºÃÏñ²»¹»Õâ¸ö FTP µÄ²é¿´ÒªÇó£¡");
	return false;
}
function LeastMoney(myallmoney)
{
	alert("ÄãµÄÉçÇø»õ±ÒºÃÏñ²»¹»£¬Ö»ÓĞ " + myallmoney + " $moneyname£¬Âò²»ÆğÕâ¸ö FTP µÄµÇÂ¼×ÊÁÏÅ¶£¡\\nÈç¹ûÄãÔÚÒøĞĞÓĞ´æ¿îµÄ»°¸Ï½ôÈ¥È¡Ç®£¬ÎÒÃÇÖ»ÊÕÏÖ½ğ:)");
	return false;
}
function MaxUser()
{
	alert("²é¿´Õâ¸ö FTP µÇÂ¼×ÊÁÏµÄÈËÊıÒÑ¾­´ïµ½ÁËÏŞ¶¨µÄ×î´óÊı¶î£¡");
	return false;
}
function ViewNEW(money, myallmoney)
{
	if (confirm("ÕâÊÇÄãµÚÒ»´Î²é¿´Õâ¸ö FTP£¬ÄãÏÖÔÚÓĞ " + myallmoney + " $moneynameÉçÇø»õ±Ò¡£\\n¹ºÂòµÇÂ¼×ÊÁÏĞèÒª»¨·ÑÄã " + money + " $moneynameÉçÇø»õ±Ò£¬ÊÇ·ñ¼ÌĞø£¿"))
		return true;
	else
		return false;
}
function ViewOLD()
{
	if (confirm("ÄãÒÔÇ°¹ºÂò¹ıÕâ¸ö FTP µÄ×ÊÁÏ£¬ÔÙ´Î²é¿´ÎŞĞè»¨Ç®:) ÊÇ·ñ¼ÌĞø£¿"))
		return true;
	else
		return false;
}
function AdminView()
{
	if (confirm("ÄãÊÇÕâ¸ö FTP µÄ¹ÜÀíÈËÔ±£¬²é¿´×ÊÁÏ²»ÊÜÏŞÖÆ£¬ÊÇ·ñ¼ÌĞø£¿"))
		return true;
	else
		return false;	
}
</script>~;
	$output .= "\n<table width=$tablewidth align=center><tr><td>¡¡¡¡<a href=$thisprog?action=add><font color=$fonthighlight><b>³öÊÛĞÂµÄ FTP ·şÎñ</b></font></a></td></tr></table>" if ($membercode eq "ad" || ",$saleusers," =~ /,$inmembername,/i);
	$output .= qq~
	<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $titlefontcolor; font-weight: bold; background-color: $titlecolor" align=center><td $catbackpic>FTP Ãû³Æ (µã»÷¹ºÂò)</td><td $catbackpic>×´Ì¬</td><td $catbackpic>ÀàĞÍ</td><td $catbackpic>¹ÜÀíÔ±</td><td $catbackpic>µ±Ç°ÊÛ¼Û</td><td $catbackpic>ÍşÍûÒªÇó</td><td $catbackpic>¹ºÂòÏŞÖÆ</td><td $catbackpic>µÃ·Ö</td></tr>~;

	foreach (@ftpinfos)
	{
		undef @ftpviews; undef $adminoption;
		chomp;
		my ($ftpid, $ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $_);
		my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
		if (-e $viewfile)
		{
			open(VIEW, $viewfile);
			@ftpviews = <VIEW>;
			close(VIEW);
		}
		my @view = grep(/^$cleanmembername\t/, @ftpviews);
		my $viewnum = @ftpviews;
		$ftpmoney -= $ftpreduce * int(($currenttime - $ftptime) / 86400);
		$ftpmoney = 1 if ($ftpmoney < 1);

		if ($ftpstatus eq "close")
		{
			$prompt = "Closed()";
		}
		elsif (lc($inmembername) eq lc($ftpadmin) || $membercode eq "ad")
		{
			$prompt = "AdminView()";
		}
		elsif ($rating < $ftprate)
		{
			$prompt = "LeastRate()";
		}
		elsif (@view >= 1)
		{
			$prompt = "ViewOLD()";
		}
		elsif ($viewnum >= $ftpmaxuser && $ftpmaxuser ne "")
		{
			$prompt = "MaxUser()";
		}
		elsif ($myallmoney < $ftpmoney)
		{
			$prompt = "LeastMoney($myallmoney)";
		}
		else
		{
			$prompt = "ViewNEW($ftpmoney, $myallmoney)";
		}

		if (lc($inmembername) eq lc($ftpadmin) || $membercode eq "ad")
		{
			$adminoption = qq~<a href=$thisprog?action=edit&id=$ftpid><font color=$titlecolor>±à</font></a> <font color=$titlecolor>|</font> <a href=$thisprog?action=delete&id=$ftpid OnClick="return confirm('Õâ½«³¹µ×É¾³ıÄãµÄ FTP ·şÎñ×ÊÁÏ£¬Èç¹ûÖ»ÊÇÒ»Ê±ÖĞ¶ÏÊ¹ÓÃ£¬½¨ÒéÄãÖ»½«ÆäÔİÊ±¹Ø±Õ¡£ÊÇ·ñ¼ÌĞø£¿');"><font color=$titlecolor>É¾</font></a> <font color=$titlecolor>|</font> <a href=$thisprog?action=info&id=$ftpid><font color=$titlecolor>¼ÇÂ¼</font></a>~;
		}
		$adminoption .= qq~ <font color=$titlecolor>|</font> <a href=$thisprog?action=up&id=$ftpid OnClick="return confirm('Õâ½«°ÑÕâ¸ö FTP ÌáÉıµ½ÁªÃËµÄ×î¶¥¶ËÎ»ÖÃ£¬ÊÇ·ñ¼ÌĞø£¿');"><font color=$titlecolor>Ìá</font></a>~ if ($membercode eq "ad");

		$ftpintro =~ s/<br>/\n/isg;
		$ftpname = "<font color=$fonthighlight><b>$ftpname</b></font>" if ($ftptype ne "priviate");
		$ftpname = qq~<a href=$thisprog?action=view&id=$ftpid OnClick="return $prompt;" title="$ftpintro">$ftpname</a>~;
		$ftpstatus = $ftpstatus eq "close" ? "¹Ø±Õ" : "¿ª·Å";
		$ftptype = $ftptype eq "priviate" ? "¸öÈË" : "¹«¹²";
		my $encodeftpadmin = uri_escape($ftpadmin);
		$ftpadmin = "<a href=profile.cgi?action=show&member=$encodeftpadmin target=_blank>$ftpadmin</a>";
		$ftpmaxuser = $ftpmaxuser eq "" ? qq~<span title="µ±Ç°¹ºÂòÈËÊı: $viewnum\n×î¶àÔÊĞí¹ºÂòÈËÊı: ²»ÏŞ">$viewnum / MAX</span>~ : qq~<span title="µ±Ç°¹ºÂòÈËÊı: $viewnum\n×î¶àÔÊĞí¹ºÂòÈËÊı: $ftpmaxuser">$viewnum / $ftpmaxuser</span>~;
		$pollscore = $polluser > 0 ? sprintf("%4.2f", $pollscore / $polluser) : "ÎŞ";
		$output .= "\n<tr bgColor=$forumcolortwo align=center><td>$ftpname<div align=right>$adminoption</div></td><td>$ftpstatus</td><td>$ftptype</td><td>$ftpadmin</td><td><i>$ftpmoney</i> $moneyname</td><td>$ftprate</td><td>$ftpmaxuser</td><td>$pollscore</td></tr>";
	}

	$output .= qq~</table></td></tr></table><SCRIPT>valignend()</SCRIPT><table cellPadding=0 cellSpacing=0 width=$tablewidth><tr><td align=right width=100% style="line-height: 150%">&copy; <b>³ÌĞòÉè¼Æ: <a href=http://www.94cool.net target=_blank><font color=5599ff>94Cool</font><font color=ff9955>.net</font></a></b> <a href=mailto:Jim_White\@etang.com>BigJim</a> </td></tr></table>~;

	if ($membercode eq "ad")
	{#Ì³Ö÷¿ÉÒÔ¿´µ½¹ÜÀíÑ¡Ïî
		$plugopenorclose = qq~<select name="plugstats"><option value="open">Õı³£¿ª·Å</option><option value="close">ÔİÊ±¹Ø±Õ</option></select>~;
		$plugopenorclose =~ s/value=\"$plugstats\"/value=\"$plugstats\" selected/;
		$output .= qq~<p>
<script language="JavaScript">
function AddSALE()
{
	if (name = prompt("ÇëÊäÈëÒªÌí¼ÓµÄÔÊĞí³öÊÛ FTP ·şÎñµÄ ID£º", ""))
	{
		if (CONFIG.saleusers.innerText) CONFIG.saleusers.innerText += "," + name;
		else CONFIG.saleusers.innerText = name;
	}
}
function DeleteSALE()
{
	if (name = prompt("ÇëÊäÈëÒªÈ¥³ıµÄÔÊĞí³öÊÛ FTP ·şÎñµÄ ID£º", ""))
	{
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/," + name + "/ig" + ",'')");
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/" + name + ",/ig" + ",'')");
		CONFIG.saleusers.innerText = eval("CONFIG.saleusers.innerText.replace(/" + name + "/ig" + ",'')");
	}
}
function ShowConfig()
{
	if (configtable.style.display == "none")
	{
		configtable.style.display = "";
		showtext.innerHTML = "Òş²Ø FTP ÁªÃËÉèÖÃ";
	}
	else
	{
		configtable.style.display = "none";
		showtext.innerHTML = "ÏÔÊ¾ FTP ÁªÃËÉèÖÃ";
	}
}
</script>
<SCRIPT>valigntop()</SCRIPT>
<table cellSpacing=0 cellPadding=0 width=$tablewidth bgColor=$tablebordercolor align=center><tr><td><table cellSpacing=1 cellPadding=6 width=100%>
<tr><td bgColor=$titlecolor $catbackpic><font color=$titlefontcolor>¡¡<b>¹ÜÀíÑ¡Ïî</b>¡¡¡¡<input type=checkbox OnClick="ShowConfig()"> <span id=showtext>ÏÔÊ¾ FTP ÁªÃËÉèÖÃ</span></font>¡¡¡¡¡¡¡¡<a href=$thisprog?action=repair OnClick="return confirm('µ±ÁªÃËÒ³ÃæĞÅÏ¢¶ªÊ§µÄÊ±ºò£¬¿ÉÒÔÊ¹ÓÃ´Ë¹¦ÄÜ»Ö¸´£¬ÊÇ·ñ¼ÌĞø£¿')"><font color=$fonthighlight><b>ĞŞ¸´ÁªÃËË÷Òı</b></font></a></td></tr>
<tr><td bgColor=$forumcolorone align=center><table id=configtable cellSpacing=15 style="display:none"><form name=CONFIG action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="config"><tr><td align=center><textarea name=saleusers rows=3 cols=40 readonly=true>$saleusers</textarea><br>³ıÌ³Ö÷ÒÔÍâµÄÔÊĞí³öÊÛÈËÔ±¡¡<input type=button value="Ìí ¼Ó" OnClick="AddSALE()">¡¡<input type=button value="É¾ ³ı" OnClick="DeleteSALE()"></td><td><br>¡¡¡¡FTP ÁªÃË²å¼ş×´Ì¬: $plugopenorclose<br>¡¡¡¡¸öÈË FTP ¹ÜÀíÔ±Ìá³É: <input name=percent type=text size=3 value="$percent"> %<br><br>¡¡¡¡¡¡¡¡<input type=submit name=submit value="±£¡¡´æ">¡¡<input type=reset value="ÖØ¡¡À´"></td><form></tr></table></td></tr>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
	}
	return;
}

sub view
{
	my $ftpid = $query->param("id");
	&myerror("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("ÆÕÍ¨´íÎó&ÄãÒª²é¿´µÄ FTP ²¢²»´æÔÚ£¡") unless (-e $infofile);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\t²é¿´ FTP ·şÎñµÇÂ¼×ÊÁÏ") unless(-e "$filetoopens.lck");

	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);

	&myerror("²é¿´´íÎó&Õâ¸ö FTP ÒÑ¾­ÔİÊ±¹Ø±Õ£¡") if ($ftpstatus eq "close");
	&myerror("²é¿´´íÎó&ÄãµÄÍşÍû²»¹»²é¿´Õâ¸ö FTP µÄ×îµÍÒªÇó£¡") if ($rating < $ftprate && lc($inmembername) ne lc($ftpadmin) && $membercode ne "ad");

	my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
	if (-e $viewfile)
	{
		open(VIEW, $viewfile);
		flock(VIEW, 1) if ($OS_USED eq "Unix");
		@ftpviews = <VIEW>;
		close(VIEW);
	}
	my @view = grep(/^$cleanmembername\t/, @ftpviews);
	if (@view < 1 && lc($inmembername) ne lc($ftpadmin) && $membercode ne "ad")
	{
		&myerror("²é¿´´íÎó&²é¿´Õâ¸ö FTP µÇÂ¼×ÊÁÏµÄÈËÊıÒÑ¾­´ïµ½ÁËÏŞ¶¨µÄ×î´óÊı¶î£¡") if (@ftpviews >= $ftpmaxuser && $ftpmaxuser ne "");
		$ftpmoney -= $ftpreduce * int(($currenttime - $ftptime) / 86400);
		$ftpmoney = 1 if ($ftpmoney < 1);
		&myerror("²é¿´´íÎó&ÄãµÄÂÛÌ³»õ±ÒÏÖ½ğ²»¹»Ö§¸¶²é¿´Õâ¸ö FTP ·şÎñµÇÂ¼×ÊÁÏËùĞèÒªµÄ»¨·Ñ£¡") if ($myallmoney < $ftpmoney);

		#¸üĞÂÓÃ»§½ğÇ®ºÍ²é¿´¼ÇÂ¼
		use testinfo qw(ipwhere);
		my $fromwhere = &ipwhere($trueipaddress);
		&updateusermoney($inmembername, -$ftpmoney);
		&winlock($viewfile) if ($OS_USED eq "Nt");
		open(VIEW, ">>$viewfile");
		flock(VIEW, 2) if ($OS_USED eq "Unix");
		print VIEW "$cleanmembername\t$trueipaddress\t$currenttime\t$fromwhere\n";
		close(VIEW);
		&winunlock($viewfile) if ($OS_USED eq "Nt");
		&updateusermoney($ftpadmin, $ftpmoney * $percent / 100) if ($ftptype eq "priviate");
	}

	if ($ftpuser =~ /\*$/)
	{#Ê¹ÓÃServ-UµÄ¶ÀÁ¢ÕË»§·½Ê½
		eval("use Digest::MD5 qw(md5_hex);");
		if ($@ eq "")
		{#MD5Ä£¿é¹¤×÷Õı³£
			$ftpuser =~ s/\*$//o;
			$ftpuser .= $cleanmembername;
			$ftppass = md5_hex("$ftppass$ftpuser");
		}
	}
	$pollscore = $polluser > 0 ? sprintf("%4.2f", $pollscore / $polluser) . " ·Ö" : "ÎŞ";

	#Êä³öÒ³Ãæ
	&ftpheader;
	$output .= qq~
	<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $fonthighlight; font-weight: bold; background-color: $titlecolor" align=center><td colSpan=2>$ftpname µÄ¾ßÌåµÇÂ¼×ÊÁÏ</td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" width=20% align=center>·şÎñµØÖ·:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$boardname</font>$ftpaddress<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>·şÎñ¶Ë¿Ú:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$boardname</font>$ftpport<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>µÇÂ½ÓÃ»§:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$boardname</font>$ftpuser<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>µÇÂ½ÃÜÂë:</td><td bgColor=$miscbacktwo><font color=$miscbacktwo>$boardname</font>$ftppass<font color=$miscbacktwo>$boarddescription</font></td></tr>
<tr><td style="color: $titlefontcolor; font-weight: bold; background-color: $miscbackone" align=center>Ïà¹ØËµÃ÷:¡¡</td><td bgColor=$miscbacktwo><form action=$thisprog method=POST><input name=action type=hidden value="poll"><input name=id type=hidden value="$ftpid"><table width=100%><tr><td width=12></td><td>$ftpintro</td><td align=right>µ±Ç°ÆÀ¼Û: $pollscore<br><br><select name=score><option value=1>1</option><option value=2>2</option><option value=3>3</option><option value=4>4</option><option value=5>5</option><option value=6 selected>6</option><option value=7>7</option><option value=8>8</option><option value=9>9</option><option value=10>10</option></select> <input type=submit value="ÆÀ·Ö"></td></tr></table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
	return;
}

sub poll
{
	my $ftpid = $query->param("id");
	&myerror("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("ÆÕÍ¨´íÎó&ÄãÒªÆÀ·ÖµÄ FTP ²¢²»´æÔÚ£¡") unless (-e $infofile);
	my $score = $query->param("score");
	&myerror("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") unless ($score =~/^[0-9]+$/ && $score > 0 && $score <= 10);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\t¶Ô FTP ·şÎñÆÀ·Ö") unless(-e "$filetoopens.lck");

	#¸üĞÂÓÃ»§ÆÀ·Ö²Ù×÷Ê±¼ä
	my $pollfile = "$lbdir$ftpdir/poll$ftpid.cgi";
	&winlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	if (-e $pollfile)
	{
		open(POLL, $pollfile);
		flock(POLL, 1) if ($OS_USED eq "Unix");
		@pollusers = <POLL>;
		close(POLL);
	}
	foreach (@pollusers)
	{
		chomp;
		my ($pollname, $lasttime) = split(/\t/, $_);
		$polltime{$pollname} = $lasttime;
	}
	if ($currenttime - $polltime{$cleanmembername} < 86400)
	{
		&winunlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		&myerror("ÆÀ·Ö´íÎó&ÄãÔÚ×î½ü24Ğ¡Ê±ÄÚÒÑ¾­¸øÕâ¸ö·şÎñÆ÷´ò¹ı·ÖÁË£¡");
	}
	$polltime{$cleanmembername} = $currenttime;
	open(POLL, ">$pollfile");
	flock(POLL, 2) if ($OS_USED eq "Unix");
	while (($pollname, $lasttime) = each(%polltime))
	{
		print POLL "$pollname\t$lasttime\n";
	}
	close(POLL);
	&winunlock($pollfile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#¸üĞÂ·şÎñÆ÷ÆÀ·Ö
	&winlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);
	$polluser++;
	$pollscore += $score;
	open(INFO, ">$infofile");
	flock(INFO, 2) if ($OS_USED eq "Unix");
	print INFO "$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore";
	close(INFO);
	&winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#¸üĞÂË÷ÒıÎÄ¼ş
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	$filetoopens = &lockfilename($listtoupdate);
	unless(-e "$filetoopens.lck")
	{#·şÎñÆ÷Ã¦Ôò·ÅÆú¸üĞÂË÷Òı
		&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		open(LIST, $listtoupdate);
		flock(LIST, 1) if ($OS_USED eq "Unix");
		my @ftpinfos = <LIST>;
		close(LIST);
		open(LIST, ">$listtoupdate");
		flock(LIST, 2) if ($OS_USED eq "Unix");
		foreach (@ftpinfos)
		{
			chomp;
			my ($id, undef) = split(/\t/, $_);
			print LIST $id == $ftpid ? "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n" : "$_\n";
		}
		close(LIST);
		&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	}

	#Êä³öÌø×ª·µ»ØÒ³Ãæ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>¶Ô FTP ·şÎñÆÀ·Ö³É¹¦£¡</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡<ul><li><a href=$thisprog>·µ»Ø FTP ÁªÃËÒ³Ãæ</a><li><a href=$thisprog?action=view&id=$ftpid>·µ»Ø FTP µÇÂ¼×ÊÁÏ</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub add
{
	&myerror("È¨ÏŞ´íÎó&ÄãÃ»ÓĞÈ¨Àû³öÊÛ FTP ·şÎñ£¡") unless ($membercode eq "ad" || ",$saleusers," =~ /,$inmembername,/i);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\t³öÊÛ FTP") unless(-e "$filetoopens.lck");

	&ftpheader;
	my $statusoption = qq~<input name=ftpstatus type=radio value="open" checked> Õı³£¿ª·Å¡¡¡¡<input name=ftpstatus type=radio value="close"> ÔİÊ±¹Ø±Õ~;
	my $typeoption = qq~<select name=ftptype><option value="public">ÂÛÌ³¹«¹²</option><option value="priviate">¸öÈË·şÎñ</option></select>~;
	my $rateoption = "";
	for (0 .. $maxweiwang)
	{
		$rateoption .= qq~<option value="$_">$_</option>~;
	}
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="addok">
<tr><td bgcolor=$miscbackone align=center><table width=80%>
<tr><td><b>FTP ×´Ì¬(*): ¡¡¡¡</b>$statusoption</td></tr>
<tr><td><b>FTP Ãû³Æ(*): ¡¡¡¡</b><input name=ftpname type=text size=60></td></tr>
<tr><td><b>FTP ÀàĞÍ(*): ¡¡¡¡</b>$typeoption¡¡¡¡<i>Ñ¡Ôñ¸öÈË·şÎñÀàĞÍ£¬ÔòÄú¸öÈË¿ÉÒÔµÃµ½¸Ã FTP ÊÕÒæµÄ $percent% ×÷Îª³êÀÍ¡£</i></td></tr>
<tr><td><b>FTP µØÖ·(*): ¡¡¡¡</b><input name=ftpaddress type=text size=24></td></tr>
<tr><td><b>FTP ¶Ë¿Ú(*): ¡¡¡¡</b><input name=ftpport type=text size=8 value="21" OnFocus="this.select()"></td></tr>
<tr><td><b>µÇÂ¼ÓÃ»§Ãû³Æ(*): </b><input name=ftpuser type=text size=36></td></tr>
<tr><td><b>µÇÂ¼ÃÜÂë(*): ¡¡¡¡</b><input name=ftppass type=text size=36></td></tr>
<tr><td>¡¡¡¡<i>×¢Òâ£ºÈç¹ûÄãÒªÊ¹ÓÃ Serv-U µÄ¶ÀÁ¢ÕÊ»§¹¦ÄÜ£¬Çë½«µÇÂ¼ÓÃ»§ÃûÌî³ÉÓÃ»§ÃûÇ°×º +¡°*¡±µÄĞÎÊ½£¬±ÈÈç¡°leobbs_*¡±£¬ÕâÑùÓÃ»§¡°BigJim¡°Ëù»ñµÃµÄÓÃ»§Ãû¾ÍÊÇ¡°leobbs_bigjim¡±£¬µÇÂ¼ÃÜÂëÌî Serv-U ²å¼şÀïÉè¶¨µÄÃÜÂëÉú³ÉÊ¹ÓÃµÄKey¡£Serv-U Ã»ÓĞ°²×°²å¼şÇĞÎğÈç´ËÊ¹ÓÃ£¡Serv-U ²å¼şµÄÏÂÔØµØÖ·Îª <a href=http://www.94cool.net/download/Serv-U.rar>http://www.94cool.net/download/Serv-U.rar</a>¡£</i></td></tr>
<tr><td><b>²é¿´ĞèÒªÍşÍû(*): </b><select name=ftprate>$rateoption</select></td></tr>
<tr><td><b>³õÊ¼ÊÛ¼Û(*): ¡¡¡¡</b><input name=ftpmoney type=text size=18></td></tr>
<tr><td><b>Ã¿24Ğ¡Ê±½µ¼Û:¡¡¡¡</b><input name=ftpreduce type=text size=15>¡¡¡¡<i>²»ĞèÒªÇëÁô¿Õ¡£</i></td></tr>
<tr><td><b>×î´ó³öÊÛÈËÊı:¡¡¡¡</b><input name=ftpmaxuser type=text size=8>¡¡¡¡<i>´ïµ½ÏŞÖÆÒÔºó£¬FTP »á×Ô¶¯Í£Ö¹³öÊÛ£¬Èç¹û²»ÏëÏŞÖÆÇëÁô¿Õ¡£</i></td></tr>
<tr><td><b>FTP ÆäËü¼ò½é:¡¡¡¡</b><textarea name=ftpintro rows=5 cols=60></textarea></td></tr>
<tr><td align=center><br><input type=submit name=submit value="³ö¡¡¡¡ÊÛ"></td></tr>
</table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
	return;
}

sub addok
{
	&myerror("È¨ÏŞ´íÎó&ÄãÃ»ÓĞÈ¨Àû³öÊÛ FTP ·şÎñ£¡") unless ($membercode eq "ad" || ",$saleusers," =~ /,$inmembername,/i);

	for ("ftpstatus", "ftpname", "ftptype", "ftpaddress", "ftpport", "ftpuser", "ftppass", "ftprate", "ftpmoney", "ftpreduce", "ftpmaxuser", "ftpintro")
	{
		${$_} = &cleaninput($query->param($_));
	}
	#ÊäÈë¼ì²é
	$ftpstatus = "open" unless ($ftpstatus eq "close");
	&myerror("ÊäÈë´íÎó&ÄãÃ»ÓĞÊäÈë FTP µÄÃû³Æ£¡") if ($ftpname eq "");
	$ftptype = "public" unless ($ftptype eq "priviate");
	&myerror("ÊäÈë´íÎó&ÄãÃ»ÓĞÊäÈë FTP µÄµØÖ·£¡") if ($ftpaddress eq "");
	$ftpport = 21 unless ($ftpport =~ /^[0-9]+$/);
	&myerror("ÊäÈë´íÎó&ÄãÃ»ÓĞÊäÈë FTP µÄÓÃ»§Ãû£¡") if ($ftpuser eq "");
	&myerror("ÊäÈë´íÎó&ÄãÃ»ÓĞÊäÈë FTP µÄÃÜÂë£¡") if ($ftppass eq "");
	$ftprate = 0 unless ($ftprate =~ /^[0-9]+$/);
	$ftpmoney = 1 unless ($ftpmoney =~ /^[0-9]+$/);
	$ftpreduce = "" unless ($ftpreduce =~ /^[0-9]+$/);
	$ftpmaxuser = "" unless ($ftpmaxuser =~ /^[0-9]+$/);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\t³öÊÛ FTP") unless(-e "$filetoopens.lck");

	#È¡µÃĞÂFTPµÄID
	my $numfiletoupdate = "$lbdir$ftpdir/lastnum.cgi";
	if (open(NUMFILE, $numfiletoupdate))
	{
		$lastnumber = <NUMFILE>;
		close(NUMFILE);
		chomp($lastnumber);
	}
	do
	{
		$lastnumber++;
	} while (-e "$lbdir$ftpdir/info$lastnumber.cgi");
	open(NUMFILE, ">$numfiletoupdate");
	flock(NUMFILE, 2) if ($OS_USED eq "Unix");
	print NUMFILE $lastnumber;
	close(NUMFILE);

	#Ğ´ÈëĞÂÊı¾İÎÄ¼ş
	open(INFO, ">$lbdir$ftpdir/info$lastnumber.cgi");
	print INFO "$ftpstatus\t$ftpname\t$ftptype\t$inmembername\t$currenttime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t0\t0";
	close(INFO);

	#¸üĞÂË÷ÒıÎÄ¼ş
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt");
	open(LIST, ">>$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	print LIST "$lastnumber\t$ftpstatus\t$ftpname\t$ftptype\t$inmembername\t$currenttime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t0\t0\t0\n";
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt");

	#Êä³öÌø×ª·µ»ØÒ³Ãæ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>³öÊÛÄãµÄ FTP ³É¹¦£¡</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡<ul><li><a href=$thisprog>·µ»Ø FTP ÁªÃËÒ³Ãæ</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub edit
{
	my $ftpid = $query->param("id");
	&myerror("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("ÆÕÍ¨´íÎó&ÄãÒª±à¼­µÄ FTP ²¢²»´æÔÚ£¡") unless (-e $infofile);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\t±à¼­ FTP ×ÊÁÏ") unless(-e "$filetoopens.lck");

	#¶ÁÈë¾ÉµÄ×ÊÁÏ
	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, undef, $ftpaddress, $ftpport, $ftpuser, $ftppass, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, undef) = split(/\t/, $ftpinfo);
	&myerror("È¨ÏŞ´íÎó&ÄãÃ»ÓĞÈ¨Àû±à¼­Õâ¸ö FTP£¡") unless ($membercode eq "ad" || lc($inmembername) eq lc($ftpadmin));

	&ftpheader;
	my $statusoption = qq~<input name=ftpstatus type=radio value="open"> Õı³£¿ª·Å¡¡¡¡<input name=ftpstatus type=radio value="close"> ÔİÊ±¹Ø±Õ~;
	$statusoption =~ s/value=\"$ftpstatus\"/value=\"$ftpstatus\" checked/o;
	my $typeoption = qq~<select name=ftptype><option value="public">ÂÛÌ³¹«¹²</option><option value="priviate">¸öÈË·şÎñ</option></select>~;
	$typeoption =~ s/value=\"$ftptype\"/value=\"$ftptype\" selected/o;
	my $rateoption = "";
	for (0 .. $maxweiwang)
	{
		$rateoption .= qq~<option value="$_">$_</option>~;
	}
	$rateoption =~ s/value=\"$ftprate\"/value=\"$ftprate\" selected/o;
	$ftpintro =~ s/<br>/\n/isg;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<form action=$thisprog method=POST OnSubmit="submit.disabled=true"><input type=hidden name=action value="editok"><input type=hidden name=id value="$ftpid">
<tr><td bgcolor=$miscbackone align=center><table width=80%>
<tr><td><b>FTP ×´Ì¬(*): ¡¡¡¡</b>$statusoption</td></tr>
<tr><td><b>FTP Ãû³Æ(*): ¡¡¡¡</b><input name=ftpname type=text size=60 value="$ftpname"></td></tr>
<tr><td><b>FTP ÀàĞÍ(*): ¡¡¡¡</b>$typeoption¡¡¡¡<i>Ñ¡Ôñ¸öÈË·şÎñÀàĞÍ£¬ÔòÄú¸öÈË¿ÉÒÔµÃµ½¸Ã FTP ÊÕÒæµÄ $percent% ×÷Îª³êÀÍ¡£</i></td></tr>
<tr><td><b>FTP µØÖ·(*): ¡¡¡¡</b><input name=ftpaddress type=text size=24 value="$ftpaddress"></td></tr>
<tr><td><b>FTP ¶Ë¿Ú(*): ¡¡¡¡</b><input name=ftpport type=text size=8 value="$ftpport" OnFocus="this.select()" value="$ftpport"></td></tr>
<tr><td><b>µÇÂ¼ÓÃ»§Ãû³Æ(*): </b><input name=ftpuser type=text size=36 value="$ftpuser"></td></tr>
<tr><td><b>µÇÂ¼ÃÜÂë(*): ¡¡¡¡</b><input name=ftppass type=text size=36 value="$ftppass"></td></tr>
<tr><td>¡¡¡¡<i>×¢Òâ£ºÈç¹ûÄãÒªÊ¹ÓÃ Serv-U µÄ¶ÀÁ¢ÕÊ»§¹¦ÄÜ£¬Çë½«µÇÂ¼ÓÃ»§ÃûÌî³ÉÓÃ»§ÃûÇ°×º +¡°*¡±µÄĞÎÊ½£¬±ÈÈç¡°dlmovie_*¡±£¬ÕâÑùÓÃ»§¡°BigJim¡°Ëù»ñµÃµÄÓÃ»§Ãû¾ÍÊÇ¡°dlmovie_bigjim¡±£¬µÇÂ¼ÃÜÂëÌî Serv-U ²å¼şÀïÉè¶¨µÄÃÜÂëÉú³ÉÊ¹ÓÃµÄKey¡£Serv-U Ã»ÓĞ°²×°²å¼şÇĞÎğÈç´ËÊ¹ÓÃ£¡Serv-U ²å¼şµÄÏÂÔØµØÖ·Îª <a href=http://www.94cool.net/download/Serv-U.rar>http://www.94cool.net/download/Serv-U.rar</a>¡£</i></td></tr>
<tr><td><b>²é¿´ĞèÒªÍşÍû(*): </b><select name=ftprate>$rateoption</select></td></tr>
<tr><td><b>³õÊ¼ÊÛ¼Û(*): ¡¡¡¡</b><input name=ftpmoney type=text size=18 value="$ftpmoney"></td></tr>
<tr><td><b>Ã¿24Ğ¡Ê±½µ¼Û:¡¡¡¡</b><input name=ftpreduce type=text size=15 value="$ftpreduce">¡¡¡¡<i>²»ĞèÒªÇëÁô¿Õ¡£</i></td></tr>
<tr><td><b>×î´ó³öÊÛÈËÊı:¡¡¡¡</b><input name=ftpmaxuser type=text size=8 value="$ftpmaxuser">¡¡¡¡<i>´ïµ½ÏŞÖÆÒÔºó£¬FTP »á×Ô¶¯Í£Ö¹³öÊÛ£¬Èç¹û²»ÏëÏŞÖÆÇëÁô¿Õ¡£</i></td></tr>
<tr><td><b>FTP ÆäËü¼ò½é:¡¡¡¡</b><textarea name=ftpintro rows=5 cols=60>$ftpintro</textarea></td></tr>
<tr><td><b>Çå³ıËùÓĞ²é¿´¼ÍÂ¼:</b>¡¡¡¡<input name=ftpclear type=checkbox value="yes"> <i>Ñ¡Ôñ´ËÏîÒÔºó£¬FTP µÄ²é¿´ÈËÔ±Ãûµ¥»á±»Çå¿Õ£¬ËùÓĞÈË¾ùĞèÖØĞÂ»¨·ÑÂÛÌ³»õ±Ò¹ºÂòĞÂµÄµÇÂ¼×ÊÁÏ¡£</i></td></tr>
<tr><td align=center><br><input type=submit name=submit value="¸ü¡¡¡¡ĞÂ"></td></tr>
</table></td></tr></form>
</table></td></tr></table><SCRIPT>valignend()</SCRIPT>~;
	return;
}

sub editok
{
	my $ftpid = $query->param("id");
	&myerror("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("ÆÕÍ¨´íÎó&ÄãÒª±à¼­µÄ FTP ²¢²»´æÔÚ£¡") unless (-e $infofile);

	for ("ftpstatus", "ftpname", "ftptype", "ftpaddress", "ftpport", "ftpuser", "ftppass", "ftprate", "ftpmoney", "ftpreduce", "ftpmaxuser", "ftpintro", "ftpclear")
	{
		${$_} = &cleaninput($query->param($_));
	}
	#ÊäÈë¼ì²é
	$ftpstatus = "open" unless ($ftpstatus eq "close");
	&myerror("ÊäÈë´íÎó&ÄãÃ»ÓĞÊäÈë FTP µÄÃû³Æ£¡") if ($ftpname eq "");
	$ftptype = "public" unless ($ftptype eq "priviate");
	&myerror("ÊäÈë´íÎó&ÄãÃ»ÓĞÊäÈë FTP µÄµØÖ·£¡") if ($ftpaddress eq "");
	$ftpport = 21 unless ($ftpport =~ /^[0-9]+$/);
	&myerror("ÊäÈë´íÎó&ÄãÃ»ÓĞÊäÈë FTP µÄÓÃ»§Ãû£¡") if ($ftpuser eq "");
	&myerror("ÊäÈë´íÎó&ÄãÃ»ÓĞÊäÈë FTP µÄÃÜÂë£¡") if ($ftppass eq "");
	$ftprate = 0 unless ($ftprate =~ /^[0-9]+$/);
	$ftpmoney = 1 unless ($ftpmoney =~ /^[0-9]+$/);
	$ftpreduce = "" unless ($ftpreduce =~ /^[0-9]+$/);
	$ftpmaxuser = "" unless ($ftpmaxuser =~ /^[0-9]+$/);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\t±à¼­ FTP ×ÊÁÏ") unless(-e "$filetoopens.lck");

	&winlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my (undef, undef, undef, $ftpadmin, $ftptime, undef, undef, undef, undef, undef, undef, undef, undef, undef, $polluser, $pollscore) = split(/\t/, $ftpinfo);
	unless ($membercode eq "ad" || lc($inmembername) eq lc($ftpadmin))
	{
		&winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
		&myerror("È¨ÏŞ´íÎó&ÄãÃ»ÓĞÈ¨Àû±à¼­Õâ¸ö FTP£¡");
	}

	#Çå¿Õ²é¿´¼ÇÂ¼
	if ($ftpclear eq "yes")
	{
		unlink("$lbdir$ftpdir/view$ftpid.cgi");
		$ftptime = $currenttime;
	}

	#¸üĞÂÊı¾İÎÄ¼ş
	open(INFO, ">$infofile");
	flock(INFO, 2) if ($OS_USED eq "Unix");
	print INFO "$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftpaddress\t$ftpport\t$ftpuser\t$ftppass\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore";
	close(INFO);
	&winunlock($infofile) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#¸üĞÂË÷ÒıÎÄ¼ş
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(LIST, $listtoupdate);
	flock(LIST, 1) if ($OS_USED eq "Unix");
	my @ftpinfos = <LIST>;
	close(LIST);
	open(LIST, ">$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	foreach (@ftpinfos)
	{
		chomp;
		my ($id, undef) = split(/\t/, $_);
		print LIST $id == $ftpid ? "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n" : "$_\n";
	}
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#Êä³öÌø×ª·µ»ØÒ³Ãæ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>±à¼­ÄãµÄ FTP ×ÊÁÏ³É¹¦£¡</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡<ul><li><a href=$thisprog>·µ»Ø FTP ÁªÃËÒ³Ãæ</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub info
{
	use testinfo qw(ipwhere);

	my $ftpid = $query->param("id");
	&myerror("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("ÆÕÍ¨´íÎó&ÄãÒª²éÑ¯µÄ FTP ²¢²»´æÔÚ£¡") unless (-e $infofile);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\t²éÑ¯ FTP ¹ºÂò¼ÇÂ¼") unless(-e "$filetoopens.lck");

	#ÅĞ¶ÏÓÃ»§È¨ÏŞ
	if ($membercode ne "ad")
	{
		open (INFO, $infofile);
		flock(INFO, 1) if ($OS_USED eq "Unix");
		my $ftpinfo = <INFO>;
		close(INFO);
		chomp($ftpinfo);
		my (undef, undef, undef, $ftpadmin, undef) = split(/\t/, $ftpinfo);
		&myerror("È¨ÏŞ´íÎó&ÄãÃ»ÓĞÈ¨Àû²éÑ¯Õâ¸ö FTP µÄ¹ºÂò¼ÇÂ¼£¡") unless (lc($inmembername) eq lc($ftpadmin));
	}

	#¶ÁÈ¡²é¿´¼ÇÂ¼
	my $viewfile = "$lbdir$ftpdir/view$ftpid.cgi";
	if (-e $viewfile)
	{
		open(VIEW, $viewfile);
		flock(VIEW, 1) if ($OS_USED eq "Unix");
		@ftpusers = <VIEW>;
		close(VIEW);
	}

	#°´Ö¸¶¨IPÌõ¼şËÑË÷
	my $key = $query->param("key");
	$key = "" unless ($key =~ /^[0-9\.]+$/);
	$key =~ s/^\.//sg;
	$key =~ s/\.$//sg;
	if ($key ne "")
	{
		@ips = split(/\./, $key);
		if (@ips < 4)
		{
			@ftpusers = grep(/\t$key\./, @ftpusers);
		}
		else
		{
			@ftpusers = grep(/\t$key/, @ftpusers);
		}
	}
	$allitems = @ftpusers;
	&splitpage("action=info&id=$ftpid&key=$key"); #·ÖÒ³

	#Êä³öÒ³Ãæ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr style="color: $titlefontcolor; font-weight: bold; background-color: $titlecolor" align=center><td $catbackpic>²é¿´Õß</td><td $catbackpic>À´×ÔIP</td><td $catbackpic>À´Ô´¼ø¶¨</td><td $catbackpic>¹ºÂòÊ±¼ä</td></tr>~;
	my $timeadd = ($timezone + $timedifferencevalue) * 3600;
	for ($i = $startnum; $i >= $endnum; $i--)
	{
		my $userinfo = $ftpusers[$i];
		chomp($userinfo);
		my ($username, $userip, $usertime, $userwhere) = split(/\t/, $userinfo);
		my $encodename = uri_escape($username);
		$userwhere = &ipwhere($userip) if ($userwhere eq "");
		my $usertime = &dateformatshort($usertime);
		$output .= qq~\n<tr align=center bgColor=$forumcolorone><td><a href=profile.cgi?action=show&member=$encodename target=_blank>$username</a></td><td>$userip</td><td>$userwhere</td><td>$usertime</td></tr>~;
	}
	$output .= qq~
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth align=center>
<form action=$thisprog><input name=action type=hidden value="info"><input name=id type=hidden value="$ftpid"><tr><td>$pages</td>
<td align=right>°´ÕÕ²é¿´ÕßIPËÑË÷(Ö§³Ö°´A¡¢B¡¢CÀàµØÖ·ËÑË÷) <input name=key type=text size=16> <input type=submit value="ËÑ Ë÷"></td></tr>
</table></form>~;
	return;
}

sub delete
{
	my $ftpid = $query->param("id");
	&myerror("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("ÆÕÍ¨´íÎó&ÄãÒªÉ¾³ıµÄ FTP ²¢²»´æÔÚ£¡") unless (-e $infofile);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\tÉ¾³ı FTP ×ÊÁÏ") unless(-e "$filetoopens.lck");

	#ÅĞ¶ÏÓÃ»§È¨ÏŞ
	if ($membercode ne "ad")
	{
		open (INFO, $infofile);
		flock(INFO, 1) if ($OS_USED eq "Unix");
		my $ftpinfo = <INFO>;
		close(INFO);
		chomp($ftpinfo);
		my (undef, undef, undef, $ftpadmin, undef) = split(/\t/, $ftpinfo);
		&myerror("È¨ÏŞ´íÎó&ÄãÃ»ÓĞÈ¨ÀûÉ¾³ıÕâ¸ö FTP£¡") unless (lc($inmembername) eq lc($ftpadmin));
	}

	#É¾³ıÊı¾İÎÄ¼ş
	unlink("$lbdir$ftpdir/info$ftpid.cgi");
	unlink("$lbdir$ftpdir/view$ftpid.cgi");
	unlink("$lbdir$ftpdir/poll$ftpid.cgi");

	#¸üĞÂË÷ÒıÎÄ¼ş
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(LIST, $listtoupdate);
	flock(LIST, 1) if ($OS_USED eq "Unix");
	my @ftpinfos = <LIST>;
	close(LIST);
	open(LIST, ">$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	foreach (@ftpinfos)
	{
		chomp;
		my ($id, undef) = split(/\t/, $_);
		print LIST "$_\n" unless ($id == $ftpid);
	}
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#Êä³öÌø×ª·µ»ØÒ³Ãæ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>É¾³ı FTP ×ÊÁÏ³É¹¦£¡</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡<ul><li><a href=$thisprog>·µ»Ø FTP ÁªÃËÒ³Ãæ</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub up
{
	&myerror("È¨ÏŞ´íÎó&ÄãÎŞÈ¨ÌáÉı FTP Î»ÖÃ£¡") unless ($membercode eq "ad");
	my $ftpid = $query->param("id");
	&myerror("ÆÕÍ¨´íÎó&ÀÏ´ó£¬±ğÂÒºÚÎÒµÄ³ÌĞòÑ½£¡") unless ($ftpid =~ /^[0-9]+$/);
	my $infofile = "$lbdir$ftpdir/info$ftpid.cgi";
	&myerror("ÆÕÍ¨´íÎó&ÄãÒªÌáÉıµÄ FTP ²¢²»´æÔÚ£¡") unless (-e $infofile);

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\tÌáÉı FTP Î»ÖÃ") unless(-e "$filetoopens.lck");

	#¶ÁÈë¾ÉµÄ×ÊÁÏ
	open (INFO, $infofile);
	flock(INFO, 1) if ($OS_USED eq "Unix");
	my $ftpinfo = <INFO>;
	close(INFO);
	chomp($ftpinfo);
	my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, undef, undef, undef, undef, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);

	#¸üĞÂË÷ÒıÎÄ¼ş
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
	open(LIST, $listtoupdate);
	flock(LIST, 1) if ($OS_USED eq "Unix");
	my @ftpinfos = <LIST>;
	close(LIST);
	open(LIST, ">$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	print LIST "$ftpid\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n";
	foreach (@ftpinfos)
	{
		chomp;
		my ($id, undef) = split(/\t/, $_);
		print LIST "$_\n" unless ($id == $ftpid);
	}
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");

	#Êä³öÌø×ª·µ»ØÒ³Ãæ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ÌáÉı FTP Î»ÖÃ³É¹¦£¡</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡<ul><li><a href=$thisprog>·µ»Ø FTP ÁªÃËÒ³Ãæ</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub repair
{
	&myerror("È¨ÏŞ´íÎó&ÄãÎŞÈ¨½øĞĞ FTP ÁªÃË¹ÜÀí£¡") unless ($membercode eq "ad");

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\tĞŞ¸´ FTP ÁªÃË") unless(-e "$filetoopens.lck");

	#»ñÈ¡ËùÓĞÊı¾İÎÄ¼şID²¢ÅÅĞò
	opendir(DIR, "$lbdir$ftpdir");
	my @infofiles = readdir(DIR);
	closedir(DIR);
	@infofiles = grep(/^info[0-9]+\.cgi$/i, @infofiles);
	foreach (@infofiles)
	{
		s/^info//is;
		s/\.cgi$//is;
	}
	@infofiles = sort numerically @infofiles;

	#ÖØĞÂ´ÓÊı¾İÎÄ¼şÖĞ¶ÁÈë
	my $listtoupdate = "$lbdir$ftpdir/list.cgi";
	&winlock($listtoupdate) if ($OS_USED eq "Nt");
	open(LIST, ">$listtoupdate");
	flock(LIST, 2) if ($OS_USED eq "Unix");
	foreach (@infofiles)
	{
		open (INFO, "$lbdir$ftpdir/info$_.cgi");
		flock(INFO, 1) if ($OS_USED eq "Unix");
		my $ftpinfo = <INFO>;
		close(INFO);
		chomp($ftpinfo);
		my ($ftpstatus, $ftpname, $ftptype, $ftpadmin, $ftptime, undef, undef, undef, undef, $ftprate, $ftpmoney, $ftpreduce, $ftpmaxuser, $ftpintro, $polluser, $pollscore) = split(/\t/, $ftpinfo);
		print LIST "$_\t$ftpstatus\t$ftpname\t$ftptype\t$ftpadmin\t$ftptime\t$ftprate\t$ftpmoney\t$ftpreduce\t$ftpmaxuser\t$ftpintro\t$polluser\t$pollscore\n";
	}
	close(LIST);
	&winunlock($listtoupdate) if ($OS_USED eq "Nt");

	#Êä³öÌø×ª·µ»ØÒ³Ãæ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ÖØ½¨ FTP ÁªÃËË÷ÒıÍê³É£¡</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡<ul><li><a href=$thisprog>·µ»Ø FTP ÁªÃËÒ³Ãæ</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;
}

sub config
{
	&myerror("È¨ÏŞ´íÎó&ÄãÎŞÈ¨½øĞĞ FTP ÁªÃË¹ÜÀí£¡") unless ($membercode eq "ad");

	#Ğ´ÈëÓÃ»§ÔÚÏß×´Ì¬
	my $filetoopens = "${lbdir}data/onlinedata.cgi";
	$filetoopens = &lockfilename($filetoopens);
	&whosonline("$inmembername\tFTP ÁªÃË\tnone\tÉè¶¨ FTP ÁªÃË") unless(-e "$filetoopens.lck");

	my $newsaleusers = $query->param("saleusers");
	my $newpercent = $query->param("percent");
	my $newplugstats = $query->param("plugstats");
	$newpercent = 10 if ($newpercent eq "");
	$newplugstats = "open" if ($newplugstats eq "");
	if (($newpercent ne "")||($newsaleusers ne "")||($newplugstats ne "")) {
	    my $configtomake = "$lbdir$ftpdir/conf.cgi";
	    &winlock($configtomake) if ($OS_USED eq "Nt");
	    open(CONFIG, ">$configtomake");
	    flock(CONFIG, 2) if ($OS_USED eq "Unix");
	    print CONFIG qq~\$plugstats = "$newplugstats";\n\$saleusers = "$newsaleusers";\n\$percent = $newpercent;\n1;~;
	    close(CONFIG);
	    &winunlock($configtomake) if ($OS_USED eq "Nt");
	}

	#Êä³öÌø×ª·µ»ØÒ³Ãæ
	&ftpheader;
	$output .= qq~
<SCRIPT>valigntop()</SCRIPT>
<table cellPadding=0 cellSpacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center><tr><td><table cellPadding=6 cellSpacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>ĞŞ¸Ä FTP ÁªÃËÉèÖÃÍê³É£¡</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡<ul><li><a href=$thisprog>·µ»Ø FTP ÁªÃËÒ³Ãæ</a></ul></td></tr>
</table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="2; url=$thisprog">~;
	return;	
}

sub ftpheader
{#Êä³öÍ·²¿µ¼º½À¸
	my $boardgraphic = $boardlogo =~ /\.swf$/i ? qq~<param name=play value=true><param name=loop value=true><param name=quality value=high><embed src=$imagesurl/myimages/$boardlogo quality=high width=$fgwidth height=$fgheight pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash" type="application/x-shockwave-flash"></embed>~ : "<img src=$imagesurl/myimages/$boardlogo border=0>";

	my $jump;
	if ($action eq "view")
	{
		$jump = qq~²é¿´ FTP ·şÎñµÇÂ¼×ÊÁÏ~;
	}
	elsif ($action eq "poll")
	{
		$jump = qq~¶Ô FTP ·şÎñÆÀ·Ö~;
	}
	elsif ($action eq "add")
	{
		$jump = qq~³öÊÛÄãµÄ FTP~;
	}
	elsif ($action eq "addok")
	{
		$jump = qq~³öÊÛÄãµÄ FTP ³É¹¦~;
	}
	elsif ($action eq "edit")
	{
		$jump = qq~±à¼­ÄãµÄ FTP ×ÊÁÏ~;
	}
	elsif ($action eq "editok")
	{
		$jump = qq~±à¼­ÄãµÄ FTP ×ÊÁÏ³É¹¦~;
	}
	elsif ($action eq "info")
	{
		$jump = qq~²é¿´ FTP ¹ºÂò¼ÇÂ¼~;
	}
	elsif ($action eq "delete")
	{
		$jump = qq~É¾³ı FTP ×ÊÁÏ³É¹¦~;
	}
	elsif ($action eq "up")
	{
		$jump = qq~ÌáÉı FTP Î»ÖÃ³É¹¦~;
	}
	elsif ($action eq "repair")
	{
		$jump = qq~ÖØ½¨ FTP ÁªÃËË÷ÒıÍê³É~;
	}
	elsif ($action eq "config")
	{
		$jump = qq~ĞŞ¸Ä FTP ÁªÃËÉèÖÃÍê³É~;
	}
	else
	{
		$jump = qq~²é¿´ FTP ÁªÃË~;
	}

	&title;
	$output .= qq~
<br>
<table width=$tablewidth align=center cellspacing=0 cellpadding=0><tr><td>>>> ÔÚÕâÀïÄú¿ÉÒÔ²é¿´±¾Õ¾ FTP ÁªÃËµÄÁĞ±í¼°ÏêÏ¸ĞÅÏ¢</td></tr></table>
<table width=$tablewidth align=center cellspacing=0 cellpadding=1 bgcolor=$navborder><tr><td><table width=100% cellspacing=0 cellpadding=3 height=25><tr><td bgcolor=$navbackground><img src=$imagesurl/images/item.gif align=absmiddle width=11> <font face="$font" color=$navfontcolor> <a href="leobbs.cgi">$boardname</a> ¡ú <a href=$thisprog>FTP ÁªÃË</a> ¡ú $jump<td bgcolor=$navbackground align=right></td></tr></table></td></tr></table>
<p>
~;
	return;
}

sub updateusermoney
{#¸üĞÂÓÃ»§½ğÇ®
	my ($nametochange, $cmoney) = @_;
	$nametochange =~ s/ /\_/sg;
	$nametochange =~ tr/A-Z/a-z/;
	my $namenumber = &getnamenumber($nametochange);
	&checkmemfile($nametochange,$namenumber);
	my $memfiletoupdate = "$lbdir$memdir/$namenumber/$nametochange.cgi";
	$memfiletoupdate = &stripMETA($memfiletoupdate);
	if (-e $memfiletoupdate)
	{
		&winlock($memfiletoupdate) if ($OS_USED eq "Nt");
		open(FILE, $memfiletoupdate);
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $filedata = <FILE>;
		close(FILE);
		chomp($filedata);
		my ($membername, $password, $membertitle, $membercode, $numberofposts, $emailaddress, $showemail, $ipaddress, $homepage, $oicqnumber, $icqnumber, $location, $interests, $joineddate, $lastpostdate, $signature, $timedifference, $privateforums, $useravatar, $userflag, $userxz, $usersx, $personalavatar, $personalwidth, $personalheight, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $soccerdata,$useradd5) = split(/\t/, $filedata);
		$mymoney += int($cmoney);
		if ($membername ne "" && $password ne "")
		{
			open(FILE, ">$memfiletoupdate");
			flock(FILE, 2) if ($OS_USED eq "Unix");
			print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$soccerdata\t$useradd5";
			close(FILE);
		}
		&winunlock($memfiletoupdate) if ($OS_USED eq "Nt");
	}
	return;
}

sub splitpage
{#»ñµÃ·ÖÒ³
	my $addstring = shift;
	my $instart = $query->param("start");
	$instart = 0 if ($instart !~ /^[0-9]+$/);

	my $temppages = $allitems / 20;
	my $numberofpages = int($temppages);
	$numberofpages++ if ($numberofpages != $temppages);

	if ($numberofpages > 1)
	{
		$startnum = $allitems - $instart - 1;
		$endnum = $startnum - 19;
		$endnum = 0 if ($endnum < 0);

		my $currentpage = int($instart / 20) + 1;
		my $endstart = ($numberofpages - 1) * 20;
		my $beginpage = $currentpage == 1 ? "<font color=$fonthighlight face=webdings>9</font>" : qq~<a href=$thisprog?start=0&$addstring title="Ê× Ò³" ><font face=webdings>9</font></a>~;
		my $endpage = $currentpage == $numberofpages ? "<font color=$fonthighlight face=webdings>:</font>" : qq~<a href=$thisprog?start=$endstart&$addstring title="Î² Ò³" ><font face=webdings>:</font></a>~;

		my $uppage = $currentpage - 1;
		my $nextpage = $currentpage + 1;
		my $upstart = $instart - 20;
		my $nextstart = $instart + 20;
		my $showup = $uppage < 1 ? "<font color=$fonthighlight face=webdings>7</font>" : qq~<a href=$thisprog?start=$upstart&$addstring title="µÚ$uppageÒ³"><font face=webdings>7</font></a>~;
		my $shownext = $nextpage > $numberofpages ? "<font color=$fonthighlight face=webdings>8</font>" : qq~<a href=$thisprog?start=$nextstart&$addstring title="µÚ$nextpageÒ³"><font face=webdings>8</font></a>~;

		my $tempstep = $currentpage / 7;
		my $currentstep = int($tempstep);
		$currentstep++ if ($currentstep != $tempstep);
		my $upsteppage = ($currentstep - 1) * 7;
		my $nextsteppage = $currentstep * 7 + 1;
		my $upstepstart = ($upsteppage - 1) * 20;
		my $nextstepstart = ($nextsteppage - 1) * 20;
		my $showupstep = $upsteppage < 1 ? "" : qq~<a href=$thisprog?start=$upstepstart&$addstring class=hb title="µÚ$upsteppageÒ³">¡û</a> ~;
		my $shownextstep = $nextsteppage > $numberofpages ? "" : qq~<a href=$thisprog?start=$nextstepstart&$addstring class=hb title="µÚ$nextsteppageÒ³">¡ú</a> ~;

		$pages = "";
		my $currentstart = $upstepstart + 20;
		for (my $i = $upsteppage + 1; $i < $nextsteppage; $i++)
		{
			last if ($i > $numberofpages);
			$pages .= $i == $currentpage ? "<font color=$fonthighlight><b>$i</b></font> " : qq~<a href=$thisprog?start=$currentstart&$addstring class=hb>$i</a> ~;
			$currentstart += 20;
		}
		$pages = "<font color=$menufontcolor><b>¹² <font color=$fonthighlight>$numberofpages</font> Ò³</b> $beginpage $showup \[ $showupstep$pages$shownextstep\] $shownext $endpage</font><br>";
	}
	else
	{
		$startnum = $allitems - 1;
		$endnum = 0;
		$pages = "<font color=$menufontcolor>Ö»ÓĞÒ»Ò³</font><br>";
	}
	return;
}

sub myerror
{
	my $errorinfo = shift;
	unlink($ftplockfile);
	&error($errorinfo);
	return;
}