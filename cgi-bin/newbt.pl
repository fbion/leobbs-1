#####################################################
#  LEO SuperCool BBS / LeoBBS X / é›·å‚²æé…·è¶…çº§è®ºå›  #
#####################################################
# åŸºäºå±±é¹°(ç³Š)ã€èŠ±æ— ç¼ºåˆ¶ä½œçš„ LB5000 XP 2.30 å…è´¹ç‰ˆ  #
#   æ–°ç‰ˆç¨‹åºåˆ¶ä½œ & ç‰ˆæƒæ‰€æœ‰: é›·å‚²ç§‘æŠ€ (C)(R)2004    #
#####################################################
#      ä¸»é¡µåœ°å€ï¼š http://www.LeoBBS.com/            #
#      è®ºå›åœ°å€ï¼š http://bbs.LeoBBS.com/            #
#####################################################
sub newbt {
    $tmptopic = $intopic%100;

    open(FILE, "${imagesdir}$usrdir/$inforum/$tmptopic/$1.torrent.btfile");
    sysread(FILE, $btinfo,(stat(FILE))[7]);
    close(FILE);
    $btinfo =~ s/\r//isg;

    chomp($btinfo);

    if (length($btinfo) <= 50) {
	eval("use BTINFO;");
	if ($@ eq "") {
		$/ = "";
		if (open(FILE, "${imagesdir}$usrdir/$inforum/$tmptopic/$1.torrent")) {
		binmode(FILE);
		my $bufferall = <FILE>;
		close(FILE);
		$/ = "\n";
		my $btfileinfo = process_file($bufferall);
		my (undef, $hash, $announce) = split(/\n/, $btfileinfo);
		open(FILE, ">${imagesdir}$usrdir/$inforum/$inforum/$tmptopic/$1.torrent.btfile");
		print FILE "$btfileinfo\|$seedinfo";
		close(FILE);
		$btinfo = "$btfileinfo\|$seedinfo";
		} else { $btinfo = "æ²¡æœ‰ç›¸åº”é™„ä»¶|0"; }
	}
    }
    
    my ($btfileinfo, $hash, $seedinfo) = split(/\n/, $btinfo);
    ($announce, $seeds, $leeches, $downloaded) = split (/\|/, $seedinfo);
    if ($seeds eq "") {
	$seeds = "æœªçŸ¥";
	$leeches = "æœªçŸ¥";
	$downloaded = "æœªçŸ¥";
    }

my @btfileinfo = split (/\t/, $btfileinfo);
$addme .= qq~
<script>
function ShowMore(){
for (var i = 0; i < AFILE.length; i++){var e = AFILE[i];e.style.display = "";}
var _S = BFILE;
_S.style.display = "none";
}
</script>
<ul><table cellSpacing=1 cellPadding=4 bgColor=$tablebordercolor width=280><tr bgColor=$titlecolor><td align=middle nowrap><font color=$titlefontcolor>æ–‡ä»¶å</td><td align=middle nowrap><font color=$titlefontcolor>æ–‡ä»¶å¤§å°</td></tr>~;

my $allfilelength = 0;
my $count = 0;
foreach (@btfileinfo) {
    next if ($_ eq "");
    $count++;
    if ($count % 2 == 1) {
	$postbackcolor1 = $postcolorone;
	$postfontcolor1 = $postfontcolorone;
    } else {
	$postbackcolor1 = $postcolortwo;
	$postfontcolor1 = $postfontcolortwo;
    }
    my ($filename, $filelength) = split (/\|/, $_);
    $allfilelength += $filelength;

    $lbsd = 'Bytes';
    if ($filelength > 1024) {
	$filelength /= 1024;
	$lbsd = 'KB';
    }
    if($filelength > 1024) {
	$filelength /= 1024;
	$lbsd = 'MB';
    }
    if($filelength > 1024) {
	$filelength /= 1024;
	$lbsd = 'GB';
    }
    $filelength = sprintf("%6.2f",$filelength) . " $lbsd";

    if ($count eq 8 ) { $addme1 .= qq~ id=AFILE style=display:none~; }
	if (length($filename) > 60) { $filename1 = substr($filename,0,57) . " ..."; } else { $filename1 = $filename; }
    $addme .= qq~<tr bgColor=$postbackcolor1 $addme1><td align=middle nowrap><font color=$postfontcolor1 title=$filename>$filename1</td><td align=middle nowrap><font color=$postfontcolor1>$filelength</td></tr>~;
}
if ($count >= 8 ) { $addme .= qq~<tr bgColor=$postbackcolor1 id=BFILE style=display:""><td align=right nowrap colspan=2><span style=CURSOR:hand onclick=ShowMore()><font color=$postfontcolor1 title=æ˜¾ç¤ºæ‰€æœ‰æ–‡ä»¶>æ›´å¤š...</font></span>&nbsp;</td></tr>~; }

($announce, $seeds, $leeches, $downloaded) = split (/\|/, $seedinfo);
if ($seeds eq "") {
    $seeds      = "æœªçŸ¥";
    $leeches    = "æœªçŸ¥";
    $downloaded = "æœªçŸ¥";
}
$lbsd = 'Bytes';
if ($allfilelength > 1024) {
    $allfilelength /= 1024;
    $lbsd = 'KB';
}
if($allfilelength > 1024) {
    $allfilelength /= 1024;
    $lbsd = 'MB';
}
if($allfilelength > 1024) {
    $allfilelength /= 1024;
    $lbsd = 'GB';
}
$allfilelength = sprintf("%6.2f",$allfilelength) . " $lbsd";

$addme .= qq~<tr bgColor=$titlecolor><td align=right nowrap colspan=2>ç§å­æ•°ï¼š$seedsforum=$inforum&filename=$1&topic=$intopic target=_blank title="°´´Ë¿É»ñµÃ¼´Ê±µÄ×ÊÁÏÊı¾İ£¬Èç¹ûÏÔÊ¾³öÏÖ\n°×ÆÁ£¬¿ÉÄÜÊÇ¶Ô·½·şÎñÆ÷ÎŞ·¨Á¬½Ó¡£">±¾Ò³ÃæÊı¾İ²¢·Ç¼´Ê±£¬ÈçĞèÒª¼´Ê±ĞÅÏ¢Çë°´ÕâÀï</a>]&nbsp;{br}×Ü¹²ÓĞ $count ¸öÎÄ¼ş£¬ÄÚÈİ¹²ÓĞ $allfilelength&nbsp;{br}URL: $announce&nbsp;</td></tr></table></ul>~;
}
1;
