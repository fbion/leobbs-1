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
use MAILPROG qw(sendmail);
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
require "code.cgi"; 
require "data/cityinfo.cgi";
$|++;

$thisprog = "setmembers.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$action          = $query -> param('action');
$box          = $query -> param('box');
$checkaction     = $query -> param('checkaction');
$inletter        = $query -> param('letter');
$inmember        = $query -> param('member');
$inmember        = &unHTML("$inmember");
$action          = &unHTML("$action");

$indellast       = $query -> param('dellast');
$indellast       = &unHTML("$indellast");
$indelposts      = $query -> param('delposts');
$indelposts      = &unHTML("$indelposts");
$indeltime       = $query -> param('deltime');
$indeltime       = &unHTML("$indeltime");
$delusetype       = $query -> param('delusetype');
$delusetype       = &unHTML("$delusetype");
$indelcdrom      = $query -> param('delcdrom'); 
$indelcdrom      = &unHTML("$indelcdrom"); 
$undelname		 = $query -> param('undelname'); 
$undelname		 = &unHTML("$undelname"); 

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");       
&admintitle;
        
&getmember("$inmembername","no");
        
        
        if ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
	<script>
	function openScript(url, width, height){var Win = window.open(url,"openScript",'width=' + width + ',height=' + height + ',resizable=1,scrollbars=yes,menubar=yes,status=yes' );}
	</script>
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / ç”¨æˆ·ç®¡ç†</b>
            </td></tr>
            ~;
            
            my %Mode = ( 

            'viewletter'         =>    \&viewletter,
            'edit'               =>    \&edit,        
            'deletemember'       =>    \&deletemember,
            'unban'              =>    \&unban,
            'delnopost'		 =>    \&delnopost,
            'canceldel'		 =>    \&canceldel,
            'deleteavatar'	 =>    \&deleteavatar,
            'boxaction'          =>    \&boxaction,
            'delok'		 =>    \&delok,
            'viewip'         =>    \&viewip,
		'viewdelmembers' => \&viewdelmembers, 
		'undelmember' => \&undelmember 
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &memberoptions; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        

############### delete member

sub deleteavatar {

    $oldmembercode = $membercode;
    &getmember("$inmember");
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "mo")||($membercode eq "amo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>æ€»æ–‘ç«¹æ— æƒåˆ é™¤å›ä¸»å’Œæ–‘ç«¹èµ„æ–™ï¼</b></td></tr>";
            exit;
    }
    $inmember = $inmember;
    $inmember =~ y/ /_/;
    $inmember =~ tr/A-Z/a-z/;

    	unlink ("${imagesdir}usravatars/$inmember.gif");
    	unlink ("${imagesdir}usravatars/$inmember.png");
    	unlink ("${imagesdir}usravatars/$inmember.jpg");
    	unlink ("${imagesdir}usravatars/$inmember.jpeg");
    	unlink ("${imagesdir}usravatars/$inmember.swf");
    	unlink ("${imagesdir}usravatars/$inmember.bmp");
    	$memberfiletitletemp = unpack("H*","$inmember");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.gif");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.png");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.jpg");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.swf");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.bmp");

	unlink ("${lbdir}cache/meminfo/$inmember.pl");
	
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>ç”¨æˆ·å¤´åƒå·²ç»åˆ é™¤äº†</b>
        </td></tr>
         ~;


} # end routine

##################################################################################
######## Subroutes (forum list)


sub memberoptions {
   %iplist=();%lettlerlist=();
open (FILE, "$lbdir/data/lbmember4.cgi");
flock(FILE, 1) if ($OS_USED eq "Unix");
my @file = <FILE>;
close (FILE);
chomp @file;
@file=sort @file;
$nowcount_a = 0;$nowcount_b = 0;
foreach(@file){
    my ($getmembername,$getip)=split(/\t/,$_);
    my $fr;
    ($getip,$getip2)=split(/, /,$getip);
    $getip = $getip2 if (($getip2 ne "")&&($getip2 ne "unknown"));
    $getip=~s/\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$//;
    unless(defined($iplist{$getip})) {
        $iplist{$getip}="$_";
        $ipshow=sprintf("% 3s",$getip);
        $ipshow=~s/\s/\&nbsp\;/g;
        $tempoutput2 .= qq~<br>~ if ($nowcount_b%15 == 0);
        $tempoutput2 .= qq~ <a href="$thisprog?action=viewip&letter=$getip">$ipshow</a> ~;
        $nowcount_b++;
    }
    if ($getmembername =~ /^[\w\-]/) {
	$fr = substr($getmembername, 0, 1);
	$fr =~ tr/a-z/A-Z/;
        $frshow=sprintf("%- 2s",$fr);
        $frshow=~s/\s/\&nbsp\;/g;
    } else {
	$fr =substr($getmembername, 0, 2);
        $frshow=$fr;
    }
   unless(defined(($lettlerlist{$fr}))) {
	$lettlerlist{$fr}="$_";
        $tempoutput .= qq~<br>~ if ($nowcount_a%15 == 0);
        $tempoutput .= qq~ <a href="$thisprog?action=viewletter&letter=~ . uri_escape($fr) . qq~">$frshow</a> ~;
        $nowcount_a ++;
    }
    last if ($nowcount_a >= 300);
}

    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>è¯·é€‰æ‹©ä¸€é¡¹</b>
    </td>
    </tr>          
    ~;
  if ($membercode eq "ad") {
    print qq~

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="foruminit.cgi?action=uptop">æ›´æ–°ç”¨æˆ·æ’å</a></b><br>
    ç”¨æˆ·æ’åå…¶å®ä¸ä¼šè‡ªåŠ¨æ›´æ–°çš„ï¼Œé™¤éä½ åœ¨è¿™å„¿æ›´æ–°ä¸€ä¸‹ã€‚<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="foruminit.cgi?action=updatecount">é‡æ–°è®¡ç®—ç”¨æˆ·æ€»æ•°</a></b><br>
    å°†æ›´æ–°é¦–é¡µæ˜¾ç¤ºçš„ç”¨æˆ·æ•°ï¼Œè¿™æ ·å¯ä»¥ç”¨æ¥æ¢å¤æ­£ç¡®æ€»ç”¨æˆ·æ•°ã€‚<BR><BR>
    </td>
    </tr>
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b>åˆ é™¤ç¬¦åˆæ¡ä»¶çš„ç”¨æˆ·</b>(åŒæ—¶ä¼šè‡ªåŠ¨æ›´æ–°ç”¨æˆ·æ’å)<BR>
    é¢„åˆ é™¤å¹¶ä¸ä¼šçœŸæ­£åˆ é™¤ç”¨æˆ·ï¼Œåªæ˜¯åšä¸€ä¸ªç»Ÿè®¡ã€‚æ–‘ç«¹å’Œå›ä¸»æ˜¯ä¸å…è®¸åœ¨è¿™é‡Œåˆ é™¤çš„ã€‚<BR>
    é¢„åˆ é™¤å’ŒçœŸæ­£åˆ é™¤æœŸé—´ï¼Œå¦‚æœç”¨æˆ·è®¿é—®äº†è®ºå›ï¼Œé‚£ä¹ˆåœ¨çœŸæ­£åˆ é™¤çš„æ—¶å€™ï¼Œæ­¤ç”¨æˆ·èµ„æ–™å°†è¢«ä¿ç•™ã€‚<BR>
    çœŸæ­£åˆ é™¤åï¼Œç”¨æˆ·çš„æ‰€æœ‰èµ„æ–™éƒ½ä¼šä¸¢å¤±ï¼Œé™¤éä½ åšè¿‡å¤‡ä»½ï¼Œå¦åˆ™æ˜¯æ— æ³•æ¢å¤çš„ã€‚
	<form action="setmembers.cgi" method=POST>
        <input type=hidden name="action" value="delnopost">
        <select name="deltime">
        <option value="30" >ä¸€ä¸ªæœˆå†…æ²¡è®¿é—® 
        <option value="60" >äºŒä¸ªæœˆå†…æ²¡è®¿é—® 
        <option value="90" >ä¸‰ä¸ªæœˆå†…æ²¡è®¿é—®
        <option value="121">å››ä¸ªæœˆå†…æ²¡è®¿é—®
        <option value="151">äº”ä¸ªæœˆå†…æ²¡è®¿é—®
        <option value="182">å…­ä¸ªæœˆå†…æ²¡è®¿é—®
        <option value="212">ä¸ƒä¸ªæœˆå†…æ²¡è®¿é—®
        <option value="243">å…«ä¸ªæœˆå†…æ²¡è®¿é—®
        <option value="273">ä¹ä¸ªæœˆå†…æ²¡è®¿é—®
        <option value="304">åä¸ªæœˆå†…æ²¡è®¿é—®
        <option value="365">ä¸€å¹´ä¹‹å†…æ²¡è®¿é—®
        <option value="730">ä¸¤å¹´ä¹‹å†…æ²¡è®¿é—®
        </select> ä¸” 
        <select name="delposts">
		<option value="9999999999">ä¸ç®¡å‘è´´æ€»æ•° 
        <option value="0"   >æ²¡æœ‰å‘è¿‡è´´å­
        <option value="10"  >æ€»å‘è´´å°‘äº 10
        <option value="50"  >æ€»å‘è´´å°‘äº 50
        <option value="100" >æ€»å‘è´´å°‘äº 100
        <option value="200" >æ€»å‘è´´å°‘äº 200
        <option value="300" >æ€»å‘è´´å°‘äº 300
        <option value="500" >æ€»å‘è´´å°‘äº 500
        <option value="800" >æ€»å‘è´´å°‘äº 800
        <option value="1000">æ€»å‘è´´å°‘äº 1000
        </select> ä¸” 
        <select name="dellast">
        <option value="no"  >ä¸ç®¡è®¿é—®æ¬¡æ•°
        <option value="5"   >è®¿é—®å°‘äº 5 æ¬¡
        <option value="10"  >è®¿é—®å°‘äº 10 æ¬¡
        <option value="20"  >è®¿é—®å°‘äº 20 æ¬¡
        <option value="50"  >è®¿é—®å°‘äº 50 æ¬¡
        <option value="80"  >è®¿é—®å°‘äº 80 æ¬¡
        <option value="100" >è®¿é—®å°‘äº 100 æ¬¡
        <option value="200" >è®¿é—®å°‘äº 200 æ¬¡
        <option value="500" >è®¿é—®å°‘äº 500 æ¬¡
        </select> ä¸” 
       <select name="delcdrom"> 
       <option value="30" >ä¸€ä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="60" >äºŒä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="90" >ä¸‰ä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="121">å››ä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="151">äº”ä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="182">å…­ä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="212">ä¸ƒä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="243">å…«ä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="273">ä¹ä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="304">åä¸ªæœˆå†…æ²¡å‘è¨€ 
       <option value="365">ä¸€å¹´ä¹‹å†…æ²¡å‘è¨€ 
       <option value="730">ä¸¤å¹´ä¹‹å†…æ²¡å‘è¨€ 
       </select><BR>ç¬¦åˆæ–¹å¼ 
      <select name="delusetype"> 
      <option value="And">AND(æ‰€æœ‰èµ„æ–™ç¬¦åˆ)
      <option value="OR">OR(æŸä¸€èµ„æ–™ç¬¦åˆ)
      </select> <BR>è¾“å…¥æ¯æ¬¡è¿›è¡Œå¤„ç†çš„ç”¨æˆ·æ•° <input type=text name="users" size=4 maxlength=4 value=500> å¦‚æœæ— æ³•æ­£å¸¸å®Œæˆï¼Œè¯·å°½é‡å‡å°‘è¿™ä¸ªæ•°ç›®ï¼Œå»¶é•¿å¤„ç†æ—¶é—´<BR>

        <input type=submit value="é¢„ åˆ  é™¤">
        </form>
        ~;
	if (-e "${lbdir}data/delmember.cgi") {
	    open (FILE, "${lbdir}data/delmember.cgi");
	    @delmembers = <FILE>;
	    close (FILE);
	    $delmembersize = @delmembers;
	    $delmembersize --;
	    $pretime=$delmembers[0];
		if ($delmembersize ne "0") {
	    chomp $pretime;
    	    $nowtime = time;
    	    $nowtime = $nowtime - 3*24*3600;
    	    if ($nowtime > $pretime) {
    	    	$oooput = qq~è·ç¦»ä¸Šæ¬¡é¢„åˆ é™¤æ—¶é—´å·²ç»è¶…è¿‡ï¼“å¤©äº† [<a href=$thisprog?action=delok>ç¡®å®šåˆ é™¤</a>]~;
    	    }
    	    else {
    	    	$oooput = qq~è·ç¦»ä¸Šæ¬¡é¢„åˆ é™¤æ—¶é—´è¿˜æœªåˆ°ï¼“å¤© [<a href=$thisprog?action=delok>ä¸ç®¡ï¼Œå¼ºåˆ¶åˆ é™¤</a>]~;
    	    }
    	    $pretime=&dateformat($pretime);
    	    print qq~
        	ä¸Šæ¬¡é¢„åˆ é™¤æ—¶é—´ï¼š$pretime (é¢„åˆ é™¤ç”¨æˆ·ä¸ªæ•°ï¼š $delmembersize ) [<a href=$thisprog?action=canceldel>å–æ¶ˆé¢„åˆ é™¤</a>]<BR>
        	$oooput [<a href=$thisprog?action=viewdelmembers>æŸ¥çœ‹é¢„åˆ é™¤ä¼šå‘˜åˆ—è¡¨</a>]
    	    ~;
			} 
			else { #ethod=POST>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="¿ìËÙ¶¨Î»">
        </form>
    
    ~;
    
    print qq~
    ×¢²áÓÃ»§´óÖÂÁĞ±í£º<br>$tempoutput
<P><a href=$thisprog?action=viewip>Ñ°ÕÒÒÔÌØ¶¨£É£Ğ×¢²áµÄÓÃ»§</a>
    <p>×¢²á£É£Ğ´óÖÂÁĞ±í£º<br>$tempoutput2
    </td>
    </tr>           
                
                
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><BR>
    <b>×¢ÒâÊÂÏî£º</b><p>
    Èç¹ûÄúÏ£Íû¸øÄúµÄÓÃ»§Ò»¸ö×Ô¶¨ÒåµÄÍ·ÏÎ£¬Ö»Òª±à¼­Ëû£¨Ëı£©µÄ×ÊÁÏ¡£<br>
    Õâ¸öÂÛÌ³ÀûÓÃ´¢´æµÄ·¢ÌùÊıÀ´È·¶¨ËûÃÇµÄ³ÉÔ±Éí·İ.<br>
    Èç¹ûÄúÈÎÃüÒ»¸öÓÃ»§Îª°æÖ÷£¬¶øËû±¾ÉíÈ´Ã»ÓĞ×Ô¶¨ÒåµÄÍ·ÏÎ£¬ÄÇÃ´¾Í»á×Ô¶¯Ìí¼ÓÒ»¸ö°æÖ÷Í·ÏÎ¡£
    Èç¹ûËûÒÑÓĞ×Ô¶¨ÒåµÄµÈ¼¶£¬ÄÇÃ´ËûµÄÔ­Í·ÏÎ½«±»±£Áô¡£<br>
    °æÖ÷Ö»ÄÜ¹»¹ÜÀí×Ô¼ºµÄÂÛÌ³£¬µ«ÊÇËûÃÇÒ²¿ÉÒÔÔÚÆäËûÂÛÌ³ÖĞÊ¹ÓÃ #Moderation Mode ÏÂµÄ¹¦ÄÜ¡£<br>
    ÇëÈ·±£ÄúËùÌáÉıµÄ°æÖ÷ÊÇ¿É¿¿µÄ¡£<br>
    °æÖ÷Ò²ºÍÌ³Ö÷Ò»Ñù£¬²»ÊÜ¹àË®Ô¤·À»úÖÆÏŞÖÆ¡£<br>
    Ö»ÓĞÌ³Ö÷²ÅÄÜ¹»½øÈë¹ÜÀíÖĞĞÄ¡£<br><br>
    Èç¹ûÄã½ûÖ¹ÁËÒ»¸öÓÃ»§£¬ÄÇÃ´Ò²Í¬Ê±½ûÖ¹ÁËÓÃËûÃÇÔ­Ãû³Æ¡¢ÓÊ¼şÖØĞÂ×¢²áµÄ¿ÉÄÜ¡£
    </td>
    </tr>             
     ~;        
     
     } # end routne
     
     
##################################################################################
######## Subroutes (Do member count)  
sub canceldel {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>´íÎó£¡</b><p>
                    
        <font color=#333333>ÄãÃ»ÓĞÈ¨ÏŞÊ¹ÓÃÕâ¸ö¹¦ÄÜ£¡</font>
                    
        </td></tr>
         ~;
}
else {
	unlink ("${lbdir}data/delmember.cgi");
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>È¡ÏûÔ¤É¾³ı</b><p>
        <font color=#333333>Ô¤É¾³ıÒÑ¾­±»È¡Ïû£¡</font>
        </td></tr>
         ~;
}
}
sub delnopost
{
	$step = $query->param('step');
	$step = 1 unless ($step);
	$size1 = $query->param('size1');
	$size1 = 0 unless($size1);	
	$users = $query->param('users');
	$users = 500 unless($users);	
	
    opendir (DIR, "${lbdir}$memdir/old"); 
    @files = readdir(DIR);
    closedir (DIR);
    @memberfiles = grep(/\.cgi$/i,@files);
    $size = @memberfiles;

	$currenttime = time;

	if (-e "${lbdir}data/delmember.cgi" && $step == 1)
	{
		print qq~
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000>
<b>¼ÆËãÓÃ»§ÅÅÃû</b><p>
<font color=#333333>Ô¤É¾³ıÎÄ¼ş´æÔÚ£¬²»¿ÉÖØ¸´Ô¤É¾³ı£¡</font>
</td></tr>~;
	}
	else
	{
  		if ($step == 1)
		{
			open (FILE, ">${lbdir}data/delmember.cgi");
			print FILE "$currenttime\t\n";
			close (FILE);
			unlink("${lbdir}data/lbmember.cgi");
		}

		$sendtoemail = "";
		open(MEMFILE, ">>${lbdir}data/lbmember.cgi");
		flock(MEMFILE, 2) if ($OS_USED eq "Unix");
		for ($i = ($step - 1) * $users; $i < $step * $users && $i < $size; $i++)
		{
			($nametocheck,$no) = split(/\./,$memberfiles[$i]);
			my $namenumber = &getnamenumber($nametocheck);
			&checkmemfile($nametocheck,$namenumber);
			$memberfile = $memberfiles[$i];
		    	$usrname="${lbdir}$memdir/$namenumber/$memberfile";
	    		open (FILE, "$usrname");
			flock (FILE, 2) if ($OS_USED eq "Unix");
			$line = <FILE>;
			close (FILE);
			undef $joineddate;
			undef $lastgone;
			undef $anzahl;
			undef $lastpostdate;
			undef $userad;
			undef $visitno;
			undef $anzahl1;
			undef $anzahl2;
			undef $emailaddr;
			undef $membername;

			($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no ,$no ,$no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/,$line);

			($anzahl1, $anzahl2) = split(/\|/,$anzahl);
			$anzahl = $anzahl1 + $anzahl2;
			($lastpost, $posturl, $posttopic) = split(/\%\%\%/, $lastpostdate);

			$lastgone = $lastpost   if ($lastpost > $lastgone);
			$lastgone = $joineddate if ($joineddate > $lastgone);

			$lastposttime = $lastpost; 
			$lastposttime = $joineddate if ($joineddate > $lastposttime);
			$lastposttime1 = $lastposttime + $indelcdrom*3600*24; 

			$lastgone1 = $lastgone + $indeltime*3600*24;

			$DelThisMember="no";
			if($delusetype eq "And")
			{
				$DelThisMember="yes" if (($lastgone1 <= $currenttime)&&($anzahl <= $indelposts)&&($lastposttime1 <= $currenttime));
			}
			else
			{
				$DelThisMember="yes" if (($lastgone1 <= $currenttime)||($anzahl <= $indelposts && $indelposts ne 9999999999)||($lastposttime1 <= $currenttime));
			}
			$DelThisMember="no" if(($userad eq "ad")||($userad eq "mo")||($userad eq "smo")||($userad eq "cmo")||($userad eq "amo")||($userad =~ /^rz/) || ($useradd5 eq "1"));
			if ($DelThisMember eq "yes")
			{
				if ($indellast ne "no")
				{
					if (($visitno <= $indellast)||($delusetype eq "OR"))
					{
						open(FILE, ">>${lbdir}data/delmember.cgi");
						flock(FILE, 2) if ($OS_USED eq "Unix");
						print FILE "$memberfile\t$lastgone\t\n";
						close(FILE);
						$size1++;
						if ($sendtoemail eq "") { $sendtoemail = "$emailaddr"; } else { $sendtoemail = "$sendtoemail, $emailaddr"; }
					}
				}
				else
				{
					open(FILE, ">>${lbdir}data/delmember.cgi");
					flock(FILE, 2) if ($OS_USED eq "Unix");
					print FILE "$memberfile\t$lastgone\t\n";
					close(FILE);
					$size1++;
					if ($sendtoemail eq "") { $sendtoemail = "$emailaddr"; } else { $sendtoemail = "$sendtoemail, $emailaddr"; }
				}
			}
			print MEMFILE "$membername\t$userad\t$anzahl\t$joineddate\t\n";
		} 
		close(MEMFILE);

		if ($sendtoemail ne "" && $emailfunctions eq "on")
		{
			$from = "$adminemail_out";
			$subject = "À´×Ô$boardnameµÄÖØÒªÓÊ¼ş£¡£¡";
			$message = "";
			$message .= "\n";
			$message .= "$boardname <br>\n";
			$message .= "$boardurl/leobbs.cgi <br>\n";
			$message .= "------------------------------------------\n<br><br>\n";
			$message .= "ÏµÍ³·¢ÏÖÄãÒÑ¾­³¤Ê±¼äÎ´·ÃÎÊ±¾ÂÛÌ³²¢·¢ÑÔÁË£¬ <br>\n";
			$message .= "ÎªÁËÊÍ·Å¿Õ¼ä£¬ÄãµÄÓÃ»§Ãû½«ÔÚ£³ÈÕºóÉ¾³ı¡£ <br>\n";
			$message .= "Èç¹ûÄãÏë±£ÁôÄãµÄÓÃ»§Ãû£¬ÇëµÇÂ¼±¾ÂÛÌ³Ò»´Î¡£ <br>\n";
			$message .= "------------------------------------------<br>\n";
			$message .= "LeoBBS ÓÉ www.leobbs.com ÈÙÓş³öÆ·¡£<br>\n";
			&sendmail($from, $from, $sendtoemail, $subject, $message);
		}
		
		if ($i < $size - 1)
		{
			$step++;
		print qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=delnopost&deltime=$indeltime&delposts=$indelposts&dellast=$indellast&delcdrom=$indelcdrom&delusetype=$delusetype&size1=$size1&step=$step&users=$users">
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#333333><br>¡¡Èç¹ûÄãµÄä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯Ç°½ø£¬Çë<a href=$thisprog?action=delnopost&deltime=$indeltime&delposts=$indelposts&dellast=$indellast&delcdrom=$indelcdrom&delusetype=$delusetype&size1=$size1&step=$step&users=$users>µã»÷¼ÌĞø</a>
</td></tr>
~;
		}
		else
		{
			if ($size1 == 0)
			{
				$delwarn = "<BR><BR><font color=red><B>µ±Ç°Ã»ÓĞ·ûºÏÉ¾³ıÌõ¼şµÄ×¢²á»áÔ±£¡<B></font>";
			}
			elsif ($emailfunctions ne "on")
			{
				$delwarn = "<BR><BR><font color=red><B>ÓÊ¼ş¹¦ÄÜÃ»ÓĞ´ò¿ª£¬ËùÒÔÓÃ»§ÎŞ·¨½ÓÊÕÔ¤É¾³ıĞÅÏ¢£¡<B></font>";
			}
			else
			{
				$delwarn = "";
			}

			unlink("${lbdir}data/delmember.cgi") if ($size1 eq 0);
			print qq~
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000>
<b>¼ÆËãÓÃ»§ÅÅÃû</b><p>
<font color=#333333>µ±Ç°¹²ÓĞ $size ¸ö×¢²áÓÃ»§£¬ÅÅÃûÊı¾İÒÑ¾­¸üĞÂ£¡</font><BR>
<font color=#333333>Ô¤É¾³ı $size1 ¸ö×¢²áÓÃ»§£¬ÅÅÃûÊı¾İÒÑ¾­¸üĞÂ£¬£³Ììºó¿ÉÒÔ½øÈë¹ÜÀíÇø½øĞĞÕæÕıÉ¾³ı£¡</font>
$delwarn
</td></tr>~;
		}
	}
} # end routine

sub delok {

unless (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
       print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>´íÎó£¡</b><p>
                    
        <font color=#333333>ÄãÃ»ÓĞÈ¨ÏŞÊ¹ÓÃÕâ¸ö¹¦ÄÜ£¡</font>
                    
        </td></tr>
         ~;
}
else {

if ($checkaction eq "yes") {
	$step = $query->param('step');
	$step = 0 unless ($step);
	$users = $query->param('users');
	$users = 200 unless($users);	
	$delno = $query->param('delno');
	$delno = 0 unless($delno);	

        open (FILE, "${lbdir}data/delmember.cgi");
        @alldelname=<FILE>;
        close (FILE);
 	$delsize = @alldelname;

    opendir (DIRS, "$lbdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^\w+?$/i, @files);
    my @recorddir = grep(/^record/i, @files);
    $recorddir = $recorddir[0];
    my @memfavdir = grep(/^memfav/i, @files);
    $memfavdir = $memfavdir[0];
$from = "$adminemail_out";
$subject = "À´×Ô$boardnameµÄÖØÒªÓÊ¼ş£¡£¡";
$message = "";
$message .= "\n";
$message .= "$boardname <br>\n";
$message .= "$boardurl/leobbs.cgi <br>\n";
$message .= "------------------------------------------\n<br><br>\n";
$message .= "ÏµÍ³·¢ÏÖÄãÒÑ¾­³¤Ê±¼äÎ´·ÃÎÊ±¾ÂÛÌ³²¢·¢ÑÔÁË£¬ <br>\n";
$message .= "ÎªÁËÊÍ·Å¿Õ¼ä£¬ÄãµÄÓÃ»§ÃûÒÑ¾­±»ÍêÈ«É¾³ı¡£ <br>\n";
$message .= "Äú±»ÊÍ·ÅµÄÓÃ»§ÃûÎª£ºmembername¡£ <br>\n";
$message .= "------------------------------------------<br>\n";
$sendtoemail = "";

    if ($step*$users < $delsize) {
 	for ($i=$step*$users;$i<=($step+1)*$users;$i++) {
 	    last if ($i > $delsize);
	    ($memberfile, $deltime)= split(/\t/,$alldelname[$i]);

	    ($nametocheck,$no) = split(/\./,$memberfile);
	    my $namenumber = &getnamenumber($nametocheck);
	    &checkmemfile($nametocheck,$namenumber);
	    $usrname="${lbdir}$memdir/$namenumber/$memberfile";
	    open (FILE, "$usrname");
    	    $line = <FILE>;
    	    close (FILE);
	    undef $joineddate;
	    undef $lastgone;
	    undef $anzahl;
	    undef $lastpostdate;
	    undef $userad;
	    undef $visitno;
	    undef $anzahl1;
	    undef $anzahl2;
	    undef $emailaddr;
	    undef $membername;

    	    ($membername, $no, $no, $userad, $anzahl, $emailaddr, $no, $no, $no, $no, $no ,$no ,$no, $joineddate, $lastpostdate, $no, $timedifference, $no, $no, $no, $no, $no, $no, $no, $no, $rating, $lastgone, $visitno, $useradd04, $useradd02, $mymoney, $postdel, $sex, $education, $marry, $work, $born, $chatlevel, $chattime, $jhmp, $jhcount, $ebankdata, $onlinetime, $userquestion, $awards, $jifen, $userface, $soccerdata, $useradd5) = split(/\t/,$line);
	$messageto = $message;
	$messageto =~ s/membername/$membername/isg;
	    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
	    $anzahl = $anzahl1 + $anzahl2;
	    ($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	    $lastgone = $lastpost   if ($lastpost > $lastgone);
	    $lastgone = $joineddate if ($joineddate > $lastgone);
	    
	    $delbankno = 0;
	    $delbanksaves = 0;
	    if ($lastgone <= $deltime) {
	        $membername =~ s/ /\_/isg;
		$membername =~ tr/A-Z/a-z/;
		my $namenumber = &getnamenumber($membername);
		&checkmemfile($membername,$namenumber);
	        unlink ("${lbdir}$memdir/$namenumber/$membername.cgi");
	        unlink ("${lbdir}$memdir/old/$membername.cgi");
        	unlink ("${lbdir}$msgdir/in/${membername}_msg.cgi");
	        unlink ("${lbdir}$msgdir/out/${membername}_out.cgi");
        	unlink ("${lbdir}$msgdir/main/${membername}_mian.cgi");
	        unlink ("${lbdir}$memfavdir/$membername.cgi");
        	unlink ("${lbdir}$memfavdir/open/$membername.cgi");
	        unlink ("${lbdir}$memfavdir/close/$membername.cgi");
        	unlink ("${lbdir}memfriend/$membername.cgi");
        	unlink ("${lbdir}$recorddir/post/$membername.cgi");
      		unlink ("${lbdir}$recorddir/reply/$membername.cgi");
        	unlink ("${lbdir}memblock/$membername.cgi");
        	unlink ("${lbdir}cache/myinfo/$membername.cgi");
        	unlink ("${lbdir}cache/meminfo/$membername.cgi");
        	unlink ("${lbdir}cache/id/$membername.cgi");
	    	unlink ("${imagesdir}usravatars/$membername.gif");
    		unlink ("${imagesdir}usravatars/$membername.png");
	    	unlink ("${imagesdir}usravatars/$membername.jpg");
    		unlink ("${imagesdir}usravatars/$membername.swf");
	    	unlink ("${imagesdir}usravatars/$membername.bmp");
    	$memberfiletitletemp = unpack("H*","$membername");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.gif");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.png");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.jpg");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.swf");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.bmp");
		unlink ("${lbdir}ebankdata/log/" . $membername . ".cgi");
		my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);
		if ($mystatus)
		{
			$delbankno++;
			$delbanksaves += $mysaves;
		}

	        $delno ++;
	  	if ($sendtoemail eq "") { $sendtoemail = $emailaddr; } else { $sendtoemail = "$sendtoemail, $emailaddr"; }
	    }
	    &updateallsave(-$delbankno, -$delbanksaves);
 	}
 	
  	if (($emailfunctions eq "on")&&($sendtoemail ne "")) {
            &sendmail($from, $from, $sendtoemail, $subject, $messageto);
        }
	$step++;
	print qq~<meta http-equiv="refresh" Content="0; url=$thisprog?action=delok&checkaction=yes&delno=$delno&step=$step&users=$users">
<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#333333><br>¡¡Èç¹ûÄãµÄä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯Ç°½ø£¬Çë<a href=$thisprog?action=delok&checkaction=yes&delno=$delno&step=$step&users=$users>µã»÷¼ÌĞø</a>
</td></tr>
			~;

    } else {

 	 	
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers=$totalmembers - $delno;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        # Delete the database for the member

	unlink ("${lbdir}data/delmember.cgi");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$delno ¸ö¹ıÆÚ×¢²áÓÃ»§ÒÑ¾­±»ÍêÕûÉ¾³ı<BR>
        ÓÃ»§¿âÒÑ¾­È«²¿¸üĞÂ</b><br><Br><a href=foruminit.cgi?action=uptop>µãÕâ¶ù¸üĞÂÓÃ»§ÅÅÃûÒ»´Î</a><br>
        </td></tr>
         ~;
    }
}

else {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>¾¯¸æ£¡£¡</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>ÍêÈ«É¾³ıËùÓĞ·ûºÏÌõ¼şµÄÔ¤É¾³ıÓÃ»§£¬µã»÷ÏÂÃæµÄÁ´½Ó¼ÌĞø¡£<BR>
        ÔÚÔ¤É¾³ıÆÚ¼ä·ÃÎÊ¹ıÂÛÌ³µÄÓÃ»§²»»á±»É¾³ı<p>
        <p>
        >> <a href="$thisprog?action=delok&checkaction=yes">¿ªÊ¼É¾³ı</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }
}
} # end routine

sub viewletter {

open (FILE, "$lbdir/data/lbmember1.cgi");
my @membernames = <FILE>;
close (FILE);
undef @sortedfile;
foreach (@membernames) {
    chomp $_;
    ($no,$names) = split(/\t/,$_);
    push (@sortedfile, $names);
}

    @sortedfile = sort alphabetically(@sortedfile);
    
    foreach (@sortedfile) {
    	if ($_ =~ /^[\w\-]/) {
        $fr = substr($_, 0, 1);
        $fr =~ tr/a-z/A-Z/;
        }
        else {
           $fr =substr($_, 0, 2);
        }
        push(@letters,$fr);
        }
    @sortedletters = sort(@letters);

    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2><center>
    <font color=#990000><b>²é¿´ËùÓĞÒÔ "$inletter" ¿ªÍ·µÄÓÃ»§</b><p>
	<form action="setmembers.cgi" method=POST>
        <input type=hidden name="action" value="edit">
        <input type=text name="member" size=10 maxlength=16>
        <input type=submit value="¿ìËÙ¶¨Î»">
        </form>
</center>
    ~;

    print qq~
    </td>
    </tr>          
    <tr>
    <td bgcolor=#FFFFFF align=center colspan=2>
    &nbsp;
    </td>
    </tr>          
    ~;
               
               
    foreach (@sortedfile) {
    	if ($_ =~ /^[\w\-]/) {
        $frr = substr($_, 0, 1);
        $frr =~ tr/a-z/A-Z/;
        }
        else {
           $frr =substr($_, 0, 2);
        }
        if ($inletter eq $frr) {
            $_ =~ s/\.cgi$//;
            $member = $_;
            &getmember("$member");
            &showmember;
            }
        }
        
   } # end route

sub viewip {
    unless($inletter eq "findsame"){
	$inletters=$inletter;
	$inletter=($inletter !~/\./)?$inletter.".":$inletter;
	$inletter=~s/\./\\\./g;
	}
    %iplist=();%sameiplist=();@thatiplist=();
open (FILE, "$lbdir/data/lbmember4.cgi");
my @ipfile = <FILE>;
close (FILE);
chomp @ipfile;
	foreach(@ipfile){
		(my $membername,my $getip)=split(/\t/,$_);
		if($inletter ne "findsame"){
			push (@thatiplist,$membername) if($getip =~/^$inletter/);
		}else{
			$sameiplist{$getip}="" unless(defined($sameiplist{$getip}));
			$sameiplist{$getip}.=qq(<a href="$thisprog?action=edit&member=$membername">$membername</a>,);
		}
		($getip,$getip2)=split(/, /,$getip);
		$getip = $getip2 if (($getip2 ne "")&&($getip2 ne "unknown"));
		$getip=~s/\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$//;
		$iplist{$getip}="$getip" unless(defined($iplist{$getip}));
	}
	@iplist=keys %iplist;
    @iplist = sort(@iplist);
    
    print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>Ñ°ÕÒÒÔÌØ¶¨£É£Ğ×¢²áµÄÓÃ»§</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡<b>ËµÃ÷:</b><br>
¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ÄãÈç¹ûÒªÑ°ÕÒÒ»¸ö IP£¬¿ÉÒÔÖ±½ÓÊäÈë IP µØÖ·ÔÚÕâÀï£¬±ÈÈç£º 202.100.200.100¡£<br>
¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡Èç¹ûÄãÒªÑ°ÕÒÒ»¸ö C ÀàÍø£¬ÄÇÃ´Äã¿ÉÒÔ²»ÊäÈë IP µÄ×îºóÒ»Î»£¬±ÈÈç£º202.100.200. <br>
¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡Èç¹ûÄãÒªÑ°ÕÒÒ»¸ö B ÀàÍø£¬ÄÇÃ´Äã¿ÉÒÔ²»ÊäÈë IP µÄ×îºóÁ½Î»£¬±ÈÈç£º202.100. <br>
¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡×¢ÒâÉÏÃæµÄĞ´·¨£¬Èç¹ûÑ°ÕÒµÄÊÇÒ»¸ö C Àà»òÕß B ÀàÍø£¬Çë×îºó±£ÁôµãºÅ(.)£¬ÇĞ¼Ç£¡</td></tr>
    <tr>
    <form action="setmembers.cgi" method=POST><input type=hidden name="action" value="viewip"><td bgcolor=#EEEEEE align=center colspan=2><input type=text name="letter" size20 maxlength=16> <input type=submit value="Ñ°ÕÒÓÃ»§"></td></form></tr>
    <tr>
    <form action="setmembers.cgi" method=POST><input type=hidden name="action" value="viewip"><input type=hidden name="letter" value="findsame"><td bgcolor=#EEEEEE align=center colspan=2><input type=submit value="Ñ°ÕÒËùÓĞÏàÍ¬£É£ĞµÄÓÃ»§"></td></form></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>×¢²á£É£Ğ´óÖÂÁĞ±í</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡~;

    $nowcount =0;
    foreach (@iplist) {
        	$ipshow=sprintf("% 3s",$_);
        	$ipshow=~s/\s/\&nbsp\;/g;
            print qq~<br>¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡~ if ($nowcount == int($nowcount/15)*15);
            print qq~ <a href="$thisprog?action=viewip&letter=$_">$ipshow</a> ~;
            $nowcount ++;
    }

    print qq~$tempoutput</td></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>~;
    if($inletter ne "findsame"){
    print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>ËùÓĞ£É£ĞÒÔ "$inletters" ¿ªÍ·µÄÓÃ»§</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=center colspan=2 height="20"></td></tr>
    ~;
		foreach (@thatiplist) {
			$member = $_;
			&getmember("$member");
			&showmember;
			}
    }else{
    print qq~
    <tr><td bgcolor=#EEEEEE align=center colspan=2><font color=#990000><b>ËùÓĞÏàÍ¬£É£ĞµÄÓÃ»§</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF align=left colspan=2>¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡<b>×¢Òâ:</b><br>
¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ÏàÍ¬£É£Ğ²»Ò»¶¨´ú±íÊÇÍ¬Ò»ÈË¡£<br></td></tr>
    ~;
		while(($ip,$thisiplist)=each(%sameiplist)){
			my @listofthisip=split(/\,/,$thisiplist);
			my $listofthisipc=@listofthisip;
			next if($listofthisipc <= 1);
			$listofthisip=join(",",@listofthisip);
    print qq~
    <tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>£É£ĞÎª "<font color=#990000>$ip</font>" µÄÓÃ»§</b></font></td></tr>
    <tr><td bgcolor=#FFFFFF colspan=2 align=left>$listofthisip</td></tr>
    <tr><td bgcolor=#FFFFFF> </td><td bgcolor=#FFFFFF> </td></tr>
    ~;
		}
	}
}


##################################################################################
######## Subroutes (Show member) 


sub showmember {

    $joineddate = &longdate("$joineddate");
    
    $cleanmember = $member;
    $cleanmember =~ s/\_/ /g;
    
    ## Sort last post, and where
    
    ($postdate, $posturl, $posttopic) = split(/\%%%/,$lastpostdate);
    
    if ($postdate ne "Ã»ÓĞ·¢±í¹ı") {
        $postdate = &longdate("$postdate");
        $lastpostdetails = qq~×îºó·¢±í <a href="$posturl">$posttopic</a> ÔÚ $postdate~;
        }
        else {
            $lastpostdetails = "Ã»ÓĞ·¢±í¹ı";
            }

    if ($membercode eq "banned") {
        $unbanlink = qq~ | [<a href="$thisprog?action=unban&member=~ . uri_escape($member) . qq~">È¡Ïû½ûÖ¹·¢ÑÔ</a>]~;
        }
    $totlepostandreply = $numberofposts+$numberofreplys;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE colspan=2 align=center><font face=$font color=$fontcolormisc><b><font color=$fonthighlight>"$cleanmember"</b> µÄÏêÏ¸×ÊÁÏ ¡¡ [ <a href="$thisprog?action=edit&member=~ . uri_escape($member) . qq~">±à¼­</a> ] | [ <a href="$thisprog?action=deletemember&member=~ . uri_escape($member) . qq~">É¾³ı</a> ]$unbanlink</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF width=30%><font color=#333333><b>×¢²áÊ±¼ä£º</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF width=30%><font color=#333333><b>×¢²á£É£Ğ£º</b></font></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOISĞÅÏ¢"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">ÕÒÏàÍ¬£É£ĞµÄÓÃ»§</a>)</td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ÓÃ»§Í·ÏÎ£º</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$membertitle</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>×îºó·¢±í£º</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastpostdetails</font></td></tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>·¢±í×ÜÊı£º</b></font></td>
    <td bgcolor=#FFFFFF><font color=#333333>$totlepostandreply</font> Æª</td></tr>
    <tr>
    <td bgcolor=#FFFFFF>&nbsp;</td>
    <td bgcolor=#FFFFFF>&nbsp;</td></tr>
    
    ~;
    $unbanlink = "";
    } # end routine


##################################################################################
######## Subroutes (Edit member) 


sub edit {
    $oldmembercode = $membercode;
    
    if ($checkaction eq "yes") {
    
    
    $innewpassword      = $query -> param('password');
    $innewpassword      = &cleanarea("$innewpassword");
    $inrating           = $query -> param('rating');
    $inmembertitle      = $query -> param('membertitle');
    $inmembertitle      = &cleanarea("$inmembertitle");
    $inemailaddress     = $query -> param('emailaddress');
    $inhomepage         = $query -> param('homepage');
    $inoicqnumber          = $query -> param('oicqnumber');
    $inicqnumber        = $query -> param('icqnumber');
    $inlocation         = $query -> param('location');
    $innumberofposts    = $query -> param('numberofposts');
    $innumberofreplys   = $query -> param('numberofreplys');
    $intimedifference   = $query -> param('timedifference');
    $inmembercode       = $query -> param('membercode');
    $inmembercode       = &cleaninput("$inmembercode");
    $invisitno          = $query -> param('visitno');
    $injhmp             = $query -> param('jhmp');
    $injifen            = $query -> param('jifen');
    $inmymoney          = $query -> param('mymoney');
    $insex              = $query -> param('sex');
    $ineducation        = $query -> param('education');
    $inmarry            = $query -> param('marry');
    $inwork             = $query -> param('work');
    $inyear             = $query -> param('year');
    $inmonth            = $query -> param('month');
    $inday              = $query -> param('day');
    $inpostdel          = $query -> param('postdel');
    $newsignature       = $query -> param('newsignature');
    $notshowsignature      = ($query -> param('notshowsignature') eq "yes")?"yes":"no";
    $inuserflag         = $query -> param('userflag');
    $inusersx           = $query -> param('usersx');
    $inuserxz           = $query -> param('userxz');
    $injoineddate       = $query -> param('joineddate');
    $newsignature           = &unHTML("$newsignature");
    $newsignature           = &cleanarea("$newsignature");

    $inlocation = &cleaninput("$inlocation");
    $inonlinetime = $query -> param('onlinetime');

   $inuseradd1         = $query -> param('useradd1');
   $tinuseradd1        = $query -> param('tuseradd1');
   $tinuseradd2        = $query -> param('tuseradd2');
   $tinuseradd3        = $query -> param('tuseradd3');
   $tinuseradd4        = $query -> param('tuseradd4');
   $tinuseradd5        = $query -> param('tuseradd5');
   $tinuseradd6        = $query -> param('tuseradd6');

   $inawards=("$tinuseradd1:$tinuseradd2:$tinuseradd3:$tinuseradd4:$tinuseradd5:$tinuseradd6");

    $inyear =~ s/\D//g;
    if (($inyear eq "")||($inmonth eq "")||($inday eq "")) {
    	$inyear  = "";
    	$inmonth = "";
    	$inday   = "";
    }
    $inborn = "$inyear/$inmonth/$inday";
    
    if ($inborn ne "//") { #¿ªÊ¼×Ô¶¯ÅĞ¶ÏĞÇ×ù
    	if ($inmonth eq "01") {
    	    if (($inday >= 1)&&($inday <=19)) {
    	        $inuserxz = "z10";
    	    }
    	    else {
    	        $inuserxz = "z11";
    	    }
    	}
        elsif ($inmonth eq "02") {
    	    if (($inday >= 1)&&($inday <=18)) {
    	        $inuserxz = "z11";
    	    }
    	    else {
    	        $inuserxz = "z12";
    	    }
        }
        elsif ($inmonth eq "03") {
    	    if (($inday >= 1)&&($inday <=20)) {
    	        $inuserxz = "z12";
    	    }
    	    else {
    	        $inuserxz = "z1";
    	    }

        }
        elsif ($inmonth eq "04") {
    	    if (($inday >= 1)&&($inday <=19)) {
    	        $inuserxz = "z1";
    	    }
    	    else {
    	        $inuserxz = "z2";
    	    }
        }
        elsif ($inmonth eq "05") {
    	    if (($inday >= 1)&&($inday <=20)) {
    	        $inuserxz = "z2";
    	    }
    	    else {
    	        $inuserxz = "z3";
    	    }
        }
        elsif ($inmonth eq "06") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z3";
    	    }
    	    else {
    	        $inuserxz = "z4";
    	    }
        }
        elsif ($inmonth eq "07") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z4";
    	    }
    	    else {
    	        $inuserxz = "z5";
    	    }
        }
        elsif ($inmonth eq "08") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z5";
    	    }
    	    else {
    	        $inuserxz = "z6";
    	    }
        }
        elsif ($inmonth eq "09") {
    	    if (($inday >= 1)&&($inday <=22)) {
    	        $inuserxz = "z6";
    	    }
    	    else {
    	        $inuserxz = "z7";
    	    }
        }
        elsif ($inmonth eq "10") {
    	    if (($inday >= 1)&&($inday <=23)) {
    	        $inuserxz = "z7";
    	    }
    	    else {
    	        $inuserxz = "z8";
    	    }
        }
        elsif ($inmonth eq "11") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z8";
    	    }
    	    else {
    	        $inuserxz = "z9";
    	    }
        }
        elsif ($inmonth eq "12") {
    	    if (($inday >= 1)&&($inday <=21)) {
    	        $inuserxz = "z9";
    	    }
    	    else {
    	        $inuserxz = "z10";
    	    }
        }
        
    }

    $inmembertitle = "Member" if ($inmembertitle eq "");

    if (length($injhmp) > 21) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>½­ºşÃÅÅÉµÄÊäÈëÇë¿ØÖÆÔÚ20¸ö×Ö·û£¨10¸öºº×Ö£©ÄÚ¡£</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if (length($inmembertitle) > 21) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>¸öÈËÍ·ÏÎµÄÊäÈëÇë¿ØÖÆÔÚ20¸ö×Ö·û£¨10¸öºº×Ö£©ÄÚ¡£</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }
    if (length($inlocation) > 12) {
        print qq ~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2><font color=#333333><b>À´×ÔµÄÊäÈëÇë¿ØÖÆÔÚ12¸ö×Ö·û£¨6¸öºº×Ö£©ÄÚ¡£</b></font></td></tr>
        ~;
	print qq~</td></tr></table></body></html>~;
        exit;
    }

    if ($injhmp eq "") { $jhmp = "ÎŞÃÅÎŞÅÉ"; }
    else { $jhmp = ($jhmp); }
    if ($inrating eq "") { $inrating = 0; }
    elsif ($inrating > $maxweiwang) { $inrating = $maxweiwang; }
    elsif ($inrating < -6) { $inrating = -6 ; $inmembercode = "banned"; }

        $filetoopen = "$lbdir" . "data/allforums.cgi";
        open(FILE,"$filetoopen");
        @forums = <FILE>;
        close(FILE);
        
        foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $trash) = split(/\t/,$forum);
            $namekey = "allow" . "$forumid";
            $tocheck = $query -> param("$namekey");
            if ($tocheck eq "yes") {
                $allowedforums2 .= "$forumid=$tocheck&";
                }
            }
            
        &getmember("$inmember");
        if ($innewpassword eq "") { $innewpassword = $password; }
        else {

        if ($innewpassword =~ /[^a-zA-Z0-9]/) { print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>ÃÜÂëÖ»ÔÊĞí´óĞ¡Ğ´×ÖÄ¸ºÍÊı×ÖµÄ×éºÏ£¡£¡</b></td></tr>"; exit; }
        if ($innewpassword =~ /^lEO/) { print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>ÃÜÂë²»ÔÊĞíÊÇ lEO ¿ªÍ·£¬Çë¸ü»»£¡£¡</b></td></tr>"; exit; }
        if (length($innewpassword)<8) { print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>ÃÜÂëÌ«¶ÌÁË£¬Çë¸ü»»£¡ÃÜÂë±ØĞë 8 Î»ÒÔÉÏ£¡</b></td></tr>"; exit; }
if ($innewpassword ne "") {
    eval {$innewpassword = md5_hex($innewpassword);};
    if ($@) {eval('use Digest::MD5 qw(md5_hex);$innewpassword = md5_hex($innewpassword);');}
    unless ($@) {$innewpassword = "lEO$innewpassword";}
}
    }
    
    if ((($inmembercode eq "ad")||($inmembercode eq "smo")||($inmembercode eq "cmo")||($inmembercode eq "amo")||($inmembercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>×Ü°ßÖñÎŞÈ¨ÌáÉıÈÎºÎÈËÎªÌ³Ö÷ºÍ°ßÖñ£¡</b></td></tr>";
            exit;
    }

        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;
	unlink ("${lbdir}cache/meminfo/$memberfiletitle.pl");
	unlink ("${lbdir}cache/myinfo/$memberfiletitle.pl");

        if ($inmembercode eq "banned") {
            $filetoopen = "$lbdir" . "data/banemaillist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$inemailaddress\t";
            close(FILE);
            $filetoopen = "$lbdir" . "data/baniplist.cgi";
            open(FILE,">>$filetoopen");
            print FILE "$ipaddress\t";
            close(FILE);
            $banresult = "½ûÖ¹ $membername ·¢ÑÔ³É¹¦";
       }
	if ($oldmembercode eq "smo") {
$innumberofposts = $numberofposts;
$innumberofreplys = $numberofreplys;
$inpostdel = $postdel;
$inmymoney = $mymoney;
$invisitno = $visitno;
$inawards = $awards;
	}
        if ($newsignature) {
        $newsignature =~ s/\t//g;
        $newsignature =~ s/\r//g;
        $newsignature =~ s/  / /g;
        $newsignature =~ s/\&amp;nbsp;/\&nbsp;/g;
        $newsignature =~ s/\n\n/\n\&nbsp;\n/isg;
        $newsignature =~ s/\n/\[br\]/isg;
        $newsignature =~ s/\[br\]\[br\]/\[br\]\&nbsp;\[br\]/isg;
        }
	require "dosignlbcode.pl";
	$signature1=&signlbcode($newsignature); 
       	$newsignature=$newsignature."aShDFSiod".$signature1;
       	$onlinetime=($inonlinetime =~/[^0-9]/)?$onlinetime:$inonlinetime;
       	my $namenumber = &getnamenumber($memberfiletitle);
	&checkmemfile($memberfiletitle,$namenumber);
        unless ((-e "${lbdir}$memdir/$namenumber/$memberfiletitle.cgi")||(-e "${lbdir}$memdir/old/$memberfiletitle.cgi")) { print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>¸ÃÓÃ»§²»´æÔÚ£¡</b></td></tr>"; exit; }
        $filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$innewpassword\t$inmembertitle\t$inmembercode\t$innumberofposts|$innumberofreplys\t$inemailaddress\t$showemail\t$ipaddress\t$inhomepage\t$inoicqnumber\t$inicqnumber\t$inlocation\t$interests\t$injoineddate\t$lastpostdate\t$newsignature\t$intimedifference\t$allowedforums2\t$useravatar\t$inuserflag\t$inuserxz\t$inusersx\t$personalavatar\t$personalwidth\t$personalheight\t$inrating\t$lastgone\t$invisitno\t$inuseradd04\t$inuseradd02\t$inmymoney\t$inpostdel\t$insex\t$ineducation\t$inmarry\t$inwork\t$inborn\t$chatlevel\t$chattime\t$injhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$inawards\t$injifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        open(FILE, ">${lbdir}$memdir/old/$memberfiletitle.cgi");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$innewpassword\t$inmembertitle\t$inmembercode\t$innumberofposts|$innumberofreplys\t$inemailaddress\t$showemail\t$ipaddress\t$inhomepage\t$inoicqnumber\t$inicqnumber\t$inlocation\t$interests\t$injoineddate\t$lastpostdate\t$newsignature\t$intimedifference\t$allowedforums2\t$useravatar\t$inuserflag\t$inuserxz\t$inusersx\t$personalavatar\t$personalwidth\t$personalheight\t$inrating\t$lastgone\t$invisitno\t$inuseradd04\t$inuseradd02\t$inmymoney\t$inpostdel\t$insex\t$ineducation\t$inmarry\t$inwork\t$inborn\t$chatlevel\t$chattime\t$injhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$inawards\t$injifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
if($oldmembercode ne "smo"){ 
       my $notshowsignaturefile = "$lbdir" . "data/notshowsignature.cgi"; 
       if(open(FILE,"$notshowsignaturefile")){ 
       $notshowsignaturemember = <FILE>; 
       close(FILE); 
       } 
       $notshowsignaturemember1=$notshowsignaturemember; 
       $notshowsignaturemember1=~s/^\t//; 
       $notshowsignaturemember1=~s/\t$//; 
       $notshowsignaturemember1="\t$notshowsignaturemember\t"; 
       if($notshowsignature eq "yes"){ 
       if($notshowsignaturemember1 !~/\t$membername\t/){ 
       open(FILE,">$notshowsignaturefile"); 
       print FILE "$notshowsignaturemember$membername\t"; 
       close(FILE); 
       $banresult.="<br>ÆÁ±Î $membername Ç©Ãû³É¹¦"; 
       } 
       }else{ 
       if($notshowsignaturemember1 =~/\t$membername\t/){ 
       $notshowsignaturemember=~s/$membername\t//i; 
       open(FILE,">$notshowsignaturefile"); 
       print FILE "$notshowsignaturemember"; 
       close(FILE); 
       $banresult.="<br>¿ª·Å $membername Ç©Ãû³É¹¦"; 
       } 
       } 
   }

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^forumstopic/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
   
                print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=2>
                <font color=#333333><b>ËùÓĞĞÅÏ¢ÒÑ¾­±£´æ</b><br><br>$banresult<br>
                </td></tr>
                ~;
    
    }
    
    else {
    
    $filetoopen = "$lbdir" . "data/allforums.cgi";
         open(FILE,"$filetoopen");
         @forums = <FILE>;
         close(FILE);

         
         foreach $forum (@forums) {
            chomp $forum;
            ($forumid, $category, $categoryplace, $forumname, $forumdescription, $forummoderator ,$htmlstate ,$idmbcodestate ,$privateforum, $startnewthreads ,$lastposter ,$lastposttime, $threads, $posts, $forumgraphic, $miscad2, $misc,$forumpass,$hiddenforum,$indexforum,$teamlogo,$teamurl, $fgwidth, $fgheight, $miscad4, $todayforumpost, $miscad5) = split(/\t/,$forum);   
            if ($privateforum eq "yes") { 
                $grab = "$forumid\t$forumname";
                push(@newforums, $grab);
                }
            }
        $cleanmember = $inmember;
        $cleanmember =~ s/\_/ /g;
    
        &getmember("$inmember");
        $inmemberencode = uri_escape($inmember);
	$signature=$signatureorigin if ($signatureorigin);
	$signature="" if (($signatureorigin eq "")&&($signaturehtml eq ""));
	$signature =~ s/\[br\]/\n/isg;
        $signature =~ s/<br>/\n/isg;
        $signature =~ s/<p>/\n/isg;
        $signature =~ s/</&lt;/g;
        $signature =~ s/>/&gt;/g;
        $signature =~ s/\&amp;/\&/isg;
        $signature =~ s/&quot\;/\"/g;
        $signature =~ s/\&nbsp;/ /isg;
        if($privateforums) {
            @private = split(/&/,$privateforums);
            foreach $accessallowed (@private) {
                chomp $accessallowed;
                ($access, $value) = split(/=/,$accessallowed);
                $allowedentry2{$access} = $value;
                }
            }
    
        @allowedforums = sort alphabetically(@newforums);
        foreach $line (@allowedforums) {
            ($forumid, $forumname) = split(/\t/,$line);
            if ($allowedentry2{$forumid} eq "yes") { $checked = " checked"; }
            else { $checked = ""; }
            $privateoutput .= qq~<input type="checkbox" name="allow$forumid" value="yes" $checked>$forumname<br>\n~;
            }
            
    my $memteam1 = qq~<option value="rz1">$defrz1(ÈÏÖ¤ÓÃ»§)~ if ($defrz1 ne "");
    my $memteam2 = qq~<option value="rz2">$defrz2(ÈÏÖ¤ÓÃ»§)~ if ($defrz2 ne "");
    my $memteam3 = qq~<option value="rz3">$defrz3(ÈÏÖ¤ÓÃ»§)~ if ($defrz3 ne "");
    my $memteam4 = qq~<option value="rz4">$defrz4(ÈÏÖ¤ÓÃ»§)~ if ($defrz4 ne "");
    my $memteam5 = qq~<option value="rz5">$defrz5(ÈÏÖ¤ÓÃ»§)~ if ($defrz5 ne "");
    $memberstateoutput = qq~<select name="membercode"><option value="me">Ò»°ãÓÃ»§$memteam1$memteam2$memteam3$memteam4$memteam5<option value="rz">ÈÏÖ¤ÓÃ»§<option value="banned">½ûÖ¹´ËÓÃ»§·¢ÑÔ<option value="masked">ÆÁ±Î´ËÓÃ»§Ìù×Ó<option value="mo">ÂÛÌ³°æÖ÷<option value="amo">ÂÛÌ³¸±°æÖ÷<option value="cmo">·ÖÀàÇø°æÖ÷<option value="smo">ÂÛÌ³×Ü°æÖ÷ *<option value="ad">Ì³Ö÷ **</select>~;
    
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
        if ($userregistered eq "no") {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>ÎŞ´ËÓÃ»§£¡</b></td></tr>";
            exit;
        }
    
    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>×Ü°ßÖñÎŞÈ¨²é¿´Ì³Ö÷ºÍ°ßÖñ×ÊÁÏ£¡</b></td></tr>";
            exit;
    }
$userflag = "blank" if ($userflag eq "");
$flaghtml = qq~
<script language="javascript">
function showflag(){document.images.userflags.src="$imagesurl/flags/"+document.creator.userflag.options[document.creator.userflag.selectedIndex].value+".gif";}
</script>
<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>ËùÔÚ¹ú¼Ò:</b></td>
<td bgcolor=#ffffff>
<select name="userflag" size=1 onChange="showflag()">
<option value="blank">±£ÃÜ</option>
<option value="China">ÖĞ¹ú</option>
<option value="Angola">°²¸çÀ­</option>
<option value="Antigua">°²Ìá¹Ï</option>
<option value="Argentina">°¢¸ùÍ¢</option>
<option value="Armenia">ÑÇÃÀÄáÑÇ</option>
<option value="Australia">°Ä´óÀûÑÇ</option>
<option value="Austria">°ÂµØÀû</option>
<option value="Bahamas">°Í¹şÂí</option>
<option value="Bahrain">°ÍÁÖ</option>
<option value="Bangladesh">ÃÏ¼ÓÀ­</option>
<option value="Barbados">°Í°Í¶àË¹</option>
<option value="Belgium">±ÈÀûÊ±</option>
<option value="Bermuda">°ÙÄ½´ó</option>
<option value="Bolivia">²£ÀûÎ¬ÑÇ</option>
<option value="Brazil">°ÍÎ÷</option>
<option value="Brunei">ÎÄÀ³</option>
<option value="Canada">¼ÓÄÃ´ó</option>
<option value="Chile">ÖÇÀû</option>
<option value="Colombia">¸çÂ×±ÈÑÇ</option>
<option value="Croatia">¿ËÂŞµØÑÇ</option>
<option value="Cuba">¹Å°Í</option>
<option value="Cyprus">ÈûÆÖÂ·Ë¹</option>
<option value="Czech_Republic">½İ¿ËË¹Âå·¥¿Ë</option>
<option value="Denmark">µ¤Âó</option>
<option value="Dominican_Republic">¶àÃ×Äá¼Ó</option>
<option value="Ecuador">¶ò¹Ï¶à¶û</option>
<option value="Egypt">°£¼°</option>
<option value="Estonia">°®É³ÄáÑÇ</option>
<option value="Finland">·ÒÀ¼</option>
<option value="France">·¨¹ú</option>
<option value="Germany">µÂ¹ú</option>
<option value="Great_Britain">Ó¢¹ú</option>
<option value="Greece">Ï£À°</option>
<option value="Guatemala">Î£µØÂíÀ­</option>
<option value="Honduras">ºé¶¼À­Ë¹</option>
<option value="Hungary">ĞÙÑÀÀû</option>
<option value="Iceland">±ùµº</option>
<option value="India">Ó¡¶È</option>
<option value="Indonesia">Ó¡¶ÈÄáÎ÷ÑÇ</option>
<option value="Iran">ÒÁÀÊ</option>
<option value="Iraq">ÒÁÀ­¿Ë</option>
<option value="Ireland">°®¶ûÀ¼</option>
<option value="Israel">ÒÔÉ«ÁĞ</option>
<option value="Italy">Òâ´óÀû</option>
<option value="Jamaica">ÑÀÂò¼Ó</option>
<option value="Japan">ÈÕ±¾</option>
<option value="Jordan">Ô¼µ©</option>
<option value="Kazakstan">¹şÈø¿Ë</option>
<option value="Kenya">¿ÏÄáÑÇ</option>
<option value="Kuwait">¿ÆÍşÌØ</option>
<option value="Latvia">À­ÍÑÎ¬ÑÇ</option>
<option value="Lebanon">Àè°ÍÄÛ</option>
<option value="Lithuania">Á¢ÌÕÍğ</option>
<option value="Malaysia">ÂíÀ´Î÷ÑÇ</option>
<option value="Malawi">ÂíÀ­Î¬</option>
<option value="Malta">Âí¶úËû</option>
<option value="Mauritius">Ã«ÀïÇóË¹</option>
<option value="Morocco">Ä¦Âå¸ç</option>
<option value="Mozambique">ÄªÉ£±È¿Ë</option>
<option value="Netherlands">ºÉÀ¼</option>
<option value="New_Zealand">ĞÂÎ÷À¼</option>
<option value="Nicaragua">Äá¼ÓÀ­¹Ï</option>
<option value="Nigeria">ÄáÈÕÀûÑÇ</option>
<option value="Norway">Å²Íş</option>
<option value="Pakistan">°Í»ùË¹Ì¹</option>
<option value="Panama">°ÍÄÃÂí</option>
<option value="Paraguay">°ÍÀ­¹ç</option>
<option value="Peru">ÃØÂ³</option>
<option value="Poland">²¨À¼</option>
<option value="Portugal">ÆÏÌÑÑÀ</option>
<option value="Romania">ÂŞÂíÄáÑÇ</option>
<option value="Russia">¶í¹ú</option>
<option value="Saudi_Arabia">É³ÌØ°¢À­²®</option>
<option value="Singapore">ĞÂ¼ÓÆÂ</option>
<option value="Slovakia">Ë¹Âå·¥¿Ë</option>
<option value="Slovenia">Ë¹ÂåÎÄÄáÑÇ</option>
<option value="Solomon_Islands">ËùÂŞÃÅ</option>
<option value="Somalia">Ë÷ÂíÀï</option>
<option value="South_Africa">ÄÏ·Ç</option>
<option value="South_Korea">º«¹ú</option>
<option value="Spain">Î÷°àÑÀ</option>
<option value="Sri_Lanka">Ó¡¶È</option>
<option value="Surinam">ËÕÀïÄÏ</option>
<option value="Sweden">Èğµä</option>
<option value="Switzerland">ÈğÊ¿</option>
<option value="Thailand">Ì©¹ú</option>
<option value="Trinidad_Tobago">¶à°Í¸ç</option>
<option value="Turkey">ÍÁ¶úÆä</option>
<option value="Ukraine">ÎÚ¿ËÀ¼</option>
<option value="United_Arab_Emirates">°¢À­²®ÁªºÏÇõ³¤¹ú</option>
<option value="United_States">ÃÀ¹ú</option>
<option value="Uruguay">ÎÚÀ­¹ç</option>
<option value="Venezuela">Î¯ÄÚÈğÀ­</option>
<option value="Yugoslavia">ÄÏË¹À­·ò</option>
<option value="Zambia">ÔŞ±ÈÑÇ</option>
<option value="Zimbabwe">½ò°Í²¼Î¤</option>
</select>
<img src="$imagesurl/flags/$userflag.gif" name="userflags" border=0 height=14 width=21>
</td></tr>
~;
$flaghtml =~ s/value=\"$userflag\"/value=\"$userflag\" selected/;

        if ($userxz eq "") {$userxz = "blank"};
        $xzhtml =qq~
        <SCRIPT language=javascript>
        function showxz(){document.images.userxzs.src="$imagesurl/star/"+document.creator.userxz.options[document.creator.userxz.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>ËùÊôĞÇ×ù£º</b>ÇëÑ¡ÔñÄãËùÊôµÄĞÇ×ù¡£<br>Èç¹ûÊäÈëÁËÉúÈÕµÄ»°£¬ÄÇÃ´´ËÏîÎŞĞ§£¡</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"userxz\" onchange=showxz() size=\"1\"> <OPTION value=blank>±£ÃÜ</OPTION> <OPTION value=\"z1\">°×Ñò×ù(3ÔÂ21--4ÔÂ19ÈÕ)</OPTION> <OPTION value=\"z2\">½ğÅ£×ù(4ÔÂ20--5ÔÂ20ÈÕ)</OPTION> <OPTION value=\"z3\">Ë«×Ó×ù(5ÔÂ21--6ÔÂ21ÈÕ)</OPTION> <OPTION value=\"z4\">¾ŞĞ·×ù(6ÔÂ22--7ÔÂ22ÈÕ)</OPTION> <OPTION value=\"z5\">Ê¨×Ó×ù(7ÔÂ23--8ÔÂ22ÈÕ)</OPTION> <OPTION value=\"z6\">´¦Å®×ù(8ÔÂ23--9ÔÂ22ÈÕ)</OPTION> <OPTION value=\"z7\">Ìì³Ó×ù(9ÔÂ23--10ÔÂ23ÈÕ)</OPTION> <OPTION value=\"z8\">ÌìĞ«×ù(10ÔÂ24--11ÔÂ21ÈÕ)</OPTION> <OPTION value=\"z9\">ÉäÊÖ×ù(11ÔÂ22--12ÔÂ21ÈÕ)</OPTION> <OPTION value=\"z10\">Ä§ôÉ×ù(12ÔÂ22--1ÔÂ19ÈÕ)</OPTION> <OPTION value=\"z11\">Ë®Æ¿×ù(1ÔÂ20--2ÔÂ18ÈÕ)</OPTION> <OPTION value=\"z12\">Ë«Óã×ù(2ÔÂ19--3ÔÂ20ÈÕ)</OPTION></SELECT> <IMG border=0 height=15 name=userxzs src=$imagesurl/star/$userxz.gif width=15 align=absmiddle>
        </TD></TR>
	~;
        $xzhtml =~ s/value=\"$userxz\"/value=\"$userxz\" selected/;

        if ($usersx eq "") {$usersx = "blank"};
        $sxhtml =qq~
        <SCRIPT language=javascript>
        function showsx(){document.images.usersxs.src="$imagesurl/sx/"+document.creator.usersx.options[document.creator.usersx.selectedIndex].value+".gif";}
        </SCRIPT>
	<tr><td bgcolor=#ffffff valign=top><font color=#333333><b>ËùÊôÉúĞ¤£º</b>ÇëÑ¡ÔñÄãËùÊôµÄÉúĞ¤¡£</td>
	<td bgcolor=#ffffff>
        <SELECT name=\"usersx\" onchange=showsx() size=\"1\"> <OPTION value=blank>±£ÃÜ</OPTION> <OPTION value=\"sx1\">×ÓÊó</OPTION> <OPTION value=\"sx2\">³óÅ£</OPTION> <OPTION value=\"sx3\">Òú»¢</OPTION> <OPTION value=\"sx4\">Ã®ÍÃ</OPTION> <OPTION value=\"sx5\">³½Áú</OPTION> <OPTION value=\"sx6\">ËÈÉß</OPTION> <OPTION value=\"sx7\">ÎçÂí</OPTION> <OPTION value=\"sx8\">Î´Ñò</OPTION> <OPTION value=\"sx9\">Éêºï</OPTION> <OPTION value=\"sx10\">ÓÏ¼¦</OPTION> <OPTION value=\"sx11\">Ğç¹·</OPTION> <OPTION value=\"sx12\">º¥Öí</OPTION></SELECT> <IMG border=0 name=usersxs src=$imagesurl/sx/$usersx.gif align=absmiddle>
        </TD></TR>
	~;
        $sxhtml =~ s/value=\"$usersx\"/value=\"$usersx\" selected/;
        if ($avatars eq "on") {
	    if (($personalavatar)&&($personalwidth)&&($personalheight)) { #×Ô¶¨ÒåÍ·Ïñ´æÔÚ
	    	$personalavatar =~ s/\$imagesurl/${imagesurl}/o;
	        if (($personalavatar =~ /\.swf$/i)&&($flashavatar eq "yes")) {
	            $personalavatar=uri_escape($personalavatar);
		    $useravatar = qq(<br>&nbsp; <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$personalwidth HEIGHT=$personalheight><PARAM NAME=MOVIE VALUE=$personalavatar><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$personalavatar WIDTH=$personalwidth HEIGHT=$personalheight PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT>¡¡[ <a href="$thisprog?action=deleteavatar&member=$inmemberencode">É¾ ³ı Í· Ïñ</a> ]);
	        }
	        else {
	            $personalavatar=uri_escape($personalavatar);
		    $useravatar = qq(<br>&nbsp; <img src=$personalavatar border=0 width=$personalwidth height=$personalheight>¡¡[ <a href="$thisprog?action=deleteavatar&member=$inmemberencode">É¾ ³ı Í· Ïñ</a> ]);
	        }
	    }
            elsif (($useravatar ne "noavatar") && ($useravatar)) {
		$useravatar=uri_escape($useravatar);
                $useravatar = qq(<br>&nbsp; <img src="$imagesurl/avatars/$useravatar.gif" border=0 $defaultwidth $defaultheight>);
            }
            else {$useravatar="Ã»ÓĞ"; }
        }
   $inmembert=$inmember;
   $inmembert=~tr/A-Z/a-z/;
   $inbox = "${lbdir}$msgdir/in/$inmembert\_msg.cgi";
   open(FILE,"$inbox");
   @inboxmsg=<FILE>;
   close(FILE);
   $inboxmsg=@inboxmsg;
   $outbox = "${lbdir}$msgdir/out/$inmembert\_out.cgi";
   open(FILE,"$outbox");
   @outboxmsg=<FILE>;
   close(FILE);
   $outboxmsg=@outboxmsg;

  $signature=~s/<br>/\n/g; 
  if ($oldmembercode eq "ad") {
       my $notshowsignaturefile = "$lbdir" . "data/notshowsignature.cgi"; 
       if(open(FILE,"$notshowsignaturefile")){ 
       $notshowsignaturemember = <FILE>; 
       close(FILE); 
       } 
       $notshowsignaturemember=~s/^\t//; 
       $notshowsignaturemember=~s/\t$//; 
       $notshowsignaturemember="\t$notshowsignaturemember\t"; 
       $nsscheck=($notshowsignaturemember !~/\t$inmember\t/i)?"":" checked"; 
    print qq~
    <form action="$thisprog" method=post name="creator">
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>Òª±à¼­µÄÓÃ»§Ãû³Æ£º </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ÓÃ»§Í·ÏÎ£º</b><br>Äú¿ÉÒÔ×Ô¶¨ÒåÒ»¸öÍ·ÏÎ£¬<br>Ä¬ÈÏ Member ±íÊ¾ÎŞÍ·ÏÎ</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>·¢±í×ÜÊı£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofposts" value="$numberofposts"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>»Ø¸´×ÜÊı£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="numberofreplys" value="$numberofreplys"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>Ìù×Ó±»É¾³ıÊı£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="postdel" value="$postdel"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ÃÜÂë(Èç²»ĞŞ¸ÄÇëÁô¿Õ)£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ÓÊ¼şµØÖ·/MSNµØÖ·£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="emailaddress" value="$emailaddress"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>Ö÷Ò³µØÖ·£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="homepage" value="$homepage"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>OICQ ºÅ£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="oicqnumber" value="$oicqnumber"></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ICQ ºÅ£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="icqnumber" value="$icqnumber"></td>
    </tr>$flaghtml<tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>À´×ÔºÎ·½£º</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="location" value="$location" maxlength=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>½­ºşÃÅÅÉ:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>¸öÈËÍşÍû:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 µ½ $maxweiwang Ö®¼ä)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>»ı·Ö:</b></td>
    <td bgcolor=#FFFFFF><input type=text name="jifen" value="$jifen" maxlength=12 size=12></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>¸öÈËÇ©Ãû£º</b></td>
    <td bgcolor=#FFFFFF><textarea name="newsignature" cols="60" rows="8">$signature</textarea><br><input type="checkbox" name="notshowsignature" value="yes" $nsscheck>ÆÁ±Î´ËÓÃ»§Ç©Ãû£¿</td>
    </tr><tr>
	~;

        $tempoutput = "<select name=\"sex\" size=\"1\"><option value=\"no\">±£ÃÜ </option><option value=\"m\">Ë§¸ç </option><option value=\"f\">ÃÀÅ® </option></select>\n";
        $tempoutput =~ s/value=\"$sex\"/value=\"$sex\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>ĞÔ±ğ£º</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"education\" size=\"1\"><option value=\"±£ÃÜ\">±£ÃÜ </option><option value=\"Ğ¡Ñ§\">Ğ¡Ñ§ </option><option value=\"³õÖĞ\">³õÖĞ </option><option value=\"¸ßÖĞ\">¸ßÖĞ</option><option value=\"ÖĞ×¨\">ÖĞ×¨</option><option value=\"´ó×¨\">´ó×¨</option><option value=\"±¾¿Æ\">±¾¿Æ</option><option value=\"Ë¶Ê¿\">Ë¶Ê¿</option><option value=\"²©Ê¿\">²©Ê¿</option><option value=\"²©Ê¿ºó\">²©Ê¿ºó</option></select>\n";
        $tempoutput =~ s/value=\"$education\"/value=\"$education\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>×î¸ßÑ§Àú£º</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"marry\" size=\"1\"><option value=\"±£ÃÜ\">±£ÃÜ </option><option value=\"Î´»é\">Î´»é </option><option value=\"ÒÑ»é\">ÒÑ»é </option><option value=\"Àë»é\">Àë»é </option><option value=\"É¥Å¼\">É¥Å¼ </option></select>\n";
        $tempoutput =~ s/value=\"$marry\"/value=\"$marry\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>»éÒö×´¿ö£º</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;

        $tempoutput = "<select name=\"work\" size=\"1\"><option value=\"±£ÃÜ\">±£ÃÜ </option><option value=\"¼ÆËã»úÒµ\">¼ÆËã»úÒµ </option><option value=\"½ğÈÚÒµ\">½ğÈÚÒµ </option><option value=\"ÉÌÒµ\">ÉÌÒµ </option><option value=\"·şÎñĞĞÒµ\">·şÎñĞĞÒµ </option><option value=\"½ÌÓıÒµ\">½ÌÓıÒµ </option><option value=\"Ñ§Éú\">Ñ§Éú </option><option value=\"¹¤³ÌÊ¦\">¹¤³ÌÊ¦ </option><option value=\"Ö÷¹Ü£¬¾­Àí\">Ö÷¹Ü£¬¾­Àí </option><option value=\"Õş¸®²¿ÃÅ\">Õş¸®²¿ÃÅ </option><option value=\"ÖÆÔìÒµ\">ÖÆÔìÒµ </option><option value=\"ÏúÊÛ/¹ã¸æ/ÊĞ³¡\">ÏúÊÛ/¹ã¸æ/ÊĞ³¡ </option><option value=\"Ê§ÒµÖĞ\">Ê§ÒµÖĞ </option></select>\n";
        $tempoutput =~ s/value=\"$work\"/value=\"$work\" selected/;
	
    print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>Ö°Òµ×´¿ö£º</b></td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc>$tempoutput</font></td>
	</tr>
	~;
	($year, $month, $day) = split(/\//, $born);
        $tempoutput1 = "<select name=\"month\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option></select>\n";
        $tempoutput1 =~ s/value=\"$month\"/value=\"$month\" selected/;

        $tempoutput2 = "<select name=\"day\"><option value=\"\" selected></option><option value=\"01\">01</option><option value=\"02\">02</option><option value=\"03\">03</option><option value=\"04\">04</option><option value=\"05\">05</option><option value=\"06\">06</option><option value=\"07\">07</option><option value=\"08\">08</option><option value=\"09\">09</option><option value=\"10\">10</option><option value=\"11\">11</option><option value=\"12\">12</option><option value=\"13\">13</option><option value=\"14\">14</option><option value=\"15\">15</option><option value=\"16\">16</option><option value=\"17\">17</option><option value=\"18\">18</option><option value=\"19\">19</option><option value=\"20\">20</option><option value=\"21\">21</option><option value=\"22\">22</option><option value=\"23\">23</option><option value=\"24\">24</option><option value=\"25\">25</option><option value=\"26\">26</option><option value=\"27\">27</option><option value=\"28\">28</option><option value=\"29\">29</option><option value=\"30\">30</option><option value=\"31\">31</option></select>\n";
        $tempoutput2 =~ s/value=\"$day\"/value=\"$day\" selected/;
	
 print qq~
	<tr>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><b>ÉúÈÕ£º</b>Èç²»ÏëÌîĞ´£¬ÇëÈ«²¿Áô¿Õ¡£</td>
	<td bgcolor=#FFFFFF><font color=$fontcolormisc><input type="text" name="year" size=4 maxlength=4 value="$year">Äê$tempoutput1ÔÂ$tempoutput2ÈÕ</font></td>
	</tr>$xzhtml
        </tr>$sxhtml
	~;
	if (open(FILE2,"${lbdir}data/cityawards.cgi")) {
   @tempawards = <FILE2>;
   close(FILE2);
   foreach $tempaward (@tempawards) {
   chomp $tempaward;
           next if ($tempaward eq "");
   ($tempawardname,$tempawardurl,$tempawardinfo,$tempawardorder,$tempawardpic) = split(/\t/,$tempaward);
   $awardselect1.=qq~<option value="$tempawardname">$tempawardname~;
   $awardselect2.=qq~<option value="$tempawardname">$tempawardname~;
   $awardselect3.=qq~<option value="$tempawardname">$tempawardname~;
   $awardselect4.=qq~<option value="$tempawardname">$tempawardname~;
   $awardselect5.=qq~<option value="$tempawardname">$tempawardname~;   
   $awardselect6.=qq~<option value="$tempawardname">$tempawardname~;   
}
($tuseradd1, $tuseradd2, $tuseradd3, $tuseradd4, $tuseradd5, $tuseradd6) = split (/:/,$awards);
   $awardselect1 =~ s/value=\"$tuseradd1\"/value=\"$tuseradd1\" selected/;
   $awardselect2 =~ s/value=\"$tuseradd2\"/value=\"$tuseradd2\" selected/;
   $awardselect3 =~ s/value=\"$tuseradd3\"/value=\"$tuseradd3\" selected/;
   $awardselect4 =~ s/value=\"$tuseradd4\"/value=\"$tuseradd4\" selected/;
   $awardselect5 =~ s/value=\"$tuseradd5\"/value=\"$tuseradd5\" selected/;   
   $awardselect6 =~ s/value=\"$tuseradd6\"/value=\"$tuseradd6\" selected/;   
}
undef @tempawards;
   print qq~
   <td bgcolor=#FFFFFF><font color=#333333><b>ÂÛÌ³Ñ«ÕÂ£º</b></td>
   <td bgcolor=#FFFFFF>Ñ«ÕÂÒ»£º
   <select name="tuseradd1">
   <option value="">Ã»ÓĞÑ«ÕÂ
   $awardselect1
   </select> Ñ«ÕÂ¶ş£º
   <select name="tuseradd2">
   <option value="">Ã»ÓĞÑ«ÕÂ
   $awardselect2
   </select><br>Ñ«ÕÂÈı£º
   <select name="tuseradd3">
   <option value="">Ã»ÓĞÑ«ÕÂ
   $awardselect3
   </select> Ñ«ÕÂËÄ£º
   <select name="tuseradd4">
   <option value="">Ã»ÓĞÑ«ÕÂ
   $awardselect4
   </select><br>Ñ«ÕÂÎå£º
   <select name="tuseradd5">
   <option value="">Ã»ÓĞÑ«ÕÂ
   $awardselect5
   </select> Ñ«ÕÂÁù£º
   <select name="tuseradd6">
   <option value="">Ã»ÓĞÑ«ÕÂ
   $awardselect6
    </select></td>
   </tr><tr>
   ~;
    $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

    print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>¶îÍâ½ğÇ®£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="mymoney" value="$mymoney" maxlength=12 size=12> Ä¿Ç°ÏÖ½ğ£º$mymoney1 $moneyname</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>·ÃÎÊ´ÎÊı£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="visitno" value="$visitno" maxlength=7 size=7></td>
    </tr><tr>
    ~;
   $timedifference = 0 if ($timedifference eq '');
   $tempoutput = "<select name=\"timedifference\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
   $tempoutput =~ s/value=\"$timedifference\"/value=\"$timedifference\" selected/;
   $joineddate = $lastgone if ($joineddate eq "");
   $joineddate1 = $joineddate;
   $joineddate = &dateformat($joineddate);
   if ($lastgone ne "") {$lastgone   = &dateformat($lastgone); } else {$lastgone = $joineddate; }
   print qq~
    <td bgcolor=#FFFFFF><font color=#333333><b>Ê±²î£º</b></td>
    <td bgcolor=#FFFFFF>$tempoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>Ë½ÓĞÂÛÌ³·ÃÎÊÈ¨ÏŞ£º</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ÓÃ»§ÀàĞÍ£º</b><br>×¢Òâ£ºÌ³Ö÷ÎªÂÛÌ³¹ÜÀíÔ±£¬ÓĞ¾ø¶Ô¸ßµÄÈ¨ÏŞ¡£<br>ËùÒÔÎñ±ØÉÙÌí¼Ó´ËÀàĞÍµÄÓÃ»§¡£<br>×Ü°æÖ÷ÔÚÈÎºÎÂÛÌ³¶¼¾ßÓĞ°æÖ÷È¨ÏŞ£¬<br>ÔÚ¹ÜÀíÖĞĞÄÖ»ÓĞÒ»¶¨È¨ÏŞ¡£</td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>×¢²áÊ±¼ä£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>×¢²áÊ±µÄ IP µØÖ·£º</b></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOISĞÅÏ¢"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">ÕÒÏàÍ¬£É£ĞµÄÓÃ»§</a>)</td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>×îºó·ÃÎÊÊ±¼ä£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ÔÚÏßÊ±¼ä£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333><input type=text size=12 name="onlinetime" value="$onlinetime" maxlength=12> Ãë</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ÓÃ»§Í·Ïñ£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ÓÃ»§¶ÌÑ¶Ï¢£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>
      ÊÕ¼şÏä¹² $inboxmsg Ìõ¡¡[ <a href="$thisprog?action=boxaction&box=inbox&checkaction=delete&member=$inmemberencode">É¾³ıÊÕ¼şÏä</a> ]¡¡[ <a href="$thisprog?action=boxaction&box=inbox&checkaction=viewbox&member=$inmemberencode">¼ìÊÓÊÕ¼şÏä</a> ]<br>
      ·¢¼şÏä¹² $outboxmsg Ìõ¡¡[ <a href="$thisprog?action=boxaction&box=outbox&checkaction=delete&member=$inmemberencode">É¾³ı·¢¼şÏä</a> ]¡¡[ <a href="$thisprog?action=boxaction&box=outbox&checkaction=viewbox&member=$inmemberencode">¼ìÊÓ·¢¼şÏä</a> ]</font></td></tr>

    <input type=hidden name="joineddate" value="$joineddate1">
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmemberencode">É¾ ³ı ´Ë ÓÃ »§</a> ]</td>
    </tr>
    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="Ìá ½»" name=submit></form></td>
    </tr>
    ~;
  }
  else {
    my $memteam1 = qq~<option value="rz1">$defrz1(ÈÏÖ¤ÓÃ»§)~ if ($defrz1 ne "");
    my $memteam2 = qq~<option value="rz2">$defrz2(ÈÏÖ¤ÓÃ»§)~ if ($defrz2 ne "");
    my $memteam3 = qq~<option value="rz3">$defrz3(ÈÏÖ¤ÓÃ»§)~ if ($defrz3 ne "");
    my $memteam4 = qq~<option value="rz4">$defrz4(ÈÏÖ¤ÓÃ»§)~ if ($defrz4 ne "");
    my $memteam5 = qq~<option value="rz5">$defrz5(ÈÏÖ¤ÓÃ»§)~ if ($defrz5 ne "");
    $memberstateoutput = qq~<select name="membercode"><option value="me">Ò»°ãÓÃ»§$memteam1$memteam2$memteam3$memteam4$memteam5<option value="rz">ÈÏÖ¤ÓÃ»§<option value="banned">½ûÖ¹´ËÓÃ»§·¢ÑÔ<option value="masked">ÆÁ±Î´ËÓÃ»§Ìù×Ó</select>~;
    $memberstateoutput =~ s/value=\"$membercode\"/value=\"$membercode\" selected/g;
    ($year, $month, $day) = split(/\//, $born);
    if ($lastgone ne "") {$lastgone   = &dateformat($lastgone); } else {$lastgone = $joineddate; }
    $joineddate = $lastgone if ($joineddate eq "");
    $mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
    print qq~
    <form action="$thisprog" method=post>
    <input type=hidden name="action" value="edit">
    <input type=hidden name="checkaction" value="yes">
    <input type=hidden name="member" value="$inmember">
    <input type=hidden name="numberofposts" value="$numberofposts">
    <input type=hidden name="numberofreplys" value="$numberofreplys">
    <input type=hidden name="postdel" value="$postdel">
    <input type=hidden name="emailaddress" value="$emailaddress">
    <input type=hidden name="homepage" value="$homepage">
    <input type=hidden name="oicqnumber" value="$oicqnumber">
    <input type=hidden name="icqnumber" value="$icqnumber">
    <input type=hidden name="location" value="$location">
    <input type=hidden name="sex" value="$sex">
    <input type=hidden name="education" value="$education">
    <input type=hidden name="marry" value="$marry">
    <input type=hidden name="work" value="$work">
    <input type=hidden name="month" value="$month">
    <input type=hidden name="day" value="$day">
    <input type=hidden name="year" value="$year">
    <input type=hidden name="visitno" value="$visitno">
    <input type=hidden name="mymoney" value="$mymoney">
    <input type=hidden name="joineddate" value="$joineddate">
    <input type=hidden name="userflag" value="$userflag">
    <input type=hidden name="usersx" value="$usersx">
    <input type=hidden name="userxz" value="$userxz">
    <input type=hidden name="timedifference" value="$timedifference">
    <input type=hidden name="jifen" value="$jifen">

    <tr>
    <td bgcolor=#EEEEEE colspan=2><font color=#333333><b>Òª±à¼­µÄÓÃ»§Ãû³Æ£º </b>$membername</td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ÓÃ»§Í·ÏÎ£º</b><br>Äú¿ÉÒÔ×Ô¶¨ÒåÒ»¸öÍ·ÏÎ£¬<br>Ä¬ÈÏ Member ±íÊ¾ÎŞÍ·ÏÎ</td>
    <td bgcolor=#FFFFFF><input type=text name="membertitle" value="$membertitle" maxlength=20></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ÃÜÂë(Èç²»ĞŞ¸ÄÇëÁô¿Õ)£º</b></td>
    <td bgcolor=#FFFFFF><input type=text name="password"></td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>½­ºşÃÅÅÉ:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="jhmp" value="$jhmp" maxlength=20></td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>¸öÈËÍşÍû:</b></td>
    <td bgcolor=#FFFFFF><input type=text size=20 name="rating" value="$rating" maxlength=2> (-5 µ½ $maxweiwang Ö®¼ä)</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>¸öÈËÇ©Ãû£º</b></td>
    <td bgcolor=#FFFFFF><textarea name="newsignature" cols="60" rows="8">$signature</textarea></td>
    </tr><tr>
    ~;
   $joineddate = &dateformat($joineddate);
   print qq~
    <td bgcolor=#FFFFFF colspan=2><font color=#333333><b>Ë½ÓĞÂÛÌ³·ÃÎÊÈ¨ÏŞ£º</b><br>
    $privateoutput</td>
    </tr><tr>
    <td bgcolor=#FFFFFF><font color=#333333><b>ÓÃ»§ÀàĞÍ£º</b></td>
    <td bgcolor=#FFFFFF>$memberstateoutput</td>
    </tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>×¢²áÊ±¼ä£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$joineddate</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>×¢²áÊ±µÄ IP µØÖ·£º</b></td>
    <td bgcolor=#FFFFFF><span style=cursor:hand onClick="javascript:openScript('lbip.cgi?q=$ipaddress',420,320)" title="LB WHOISĞÅÏ¢"><font color=#333333>$ipaddress</font></span> (<a href="$thisprog?action=viewip&letter=$ipaddress">ÕÒÏàÍ¬£É£ĞµÄÓÃ»§</a>)</td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>×îºó·ÃÎÊÊ±¼ä£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$lastgone</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ÔÚÏßÊ±¼ä£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333><input type=text size=10 name="onlinetime" value="$onlinetime" maxlength=10> Ãë</font></td></tr>
    <tr><td bgcolor=#FFFFFF><font color=#333333><b>ÓÃ»§Í·Ïñ£º</b></td>
    <td bgcolor=#FFFFFF><font color=#333333>$useravatar</font></td></tr>
    <tr>
    <td colspan=2 bgcolor=#FFFFFF align=center>[ <a href="$thisprog?action=deletemember&member=$inmemberencode">É¾ ³ı ´Ë ÓÃ »§</a> ]</td>
    </tr>

    <tr>
    <td colspan=2 bgcolor=#EEEEEE align=center><input type=submit value="Ìá ½»" name=submit></form></td>
    </tr>
    ~;
  	
  }  
 } # end else
    
} # endroute


############### delete member

sub deletemember {

    $oldmembercode = $membercode;
    &getmember("$inmember");
    my ($mystatus, $mysaves, $mysavetime, $myloan, $myloantime, $myloanrating, $bankadd1, $bankadd2, $bankadd3, $bankadd4, $bankadd5) = split(/,/, $ebankdata);

    if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>×Ü°ßÖñÎŞÈ¨É¾³ıÌ³Ö÷ºÍ°ßÖñ×ÊÁÏ£¡</b></td></tr>";
            exit;
    }
    if ($inmembername eq $inmember) {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>×Ô¼º²»ÄÜÉ¾³ı×Ô¼ºµÄ×ÊÁÏÓ´£¡</b></td></tr>";
            exit;
    }

if ($checkaction eq "yes") {
####################################################
    # Check to see if they were the last member to register

    require "$lbdir" . "data/boardstats.cgi";
        
    if($inmember eq "$lastregisteredmember") { #start

        $dirtoopen = "$lbdir" . "$memdir";
        opendir (DIR, "$dirtoopen"); 
        @filedata = readdir(DIR);
        closedir (DIR);
        @inmembers = grep(/cgi$/i,@filedata);

        local($highest) = 0;

        foreach (@inmembers) {
            $_ =~ s/\.cgi$//g;
            &getmember("$_");
            if (($joineddate > $highest) && ($inmember ne $membername)) {
                $highest = $joineddate;
                $memberkeep = $membername;
                }
        }
        
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers--;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$memberkeep\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if new/delete member

    else {
        require "$lbdir" . "data/boardstats.cgi";

        $filetomake = "$lbdir" . "data/boardstats.cgi";
        $totalmembers--;
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$totalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
        } # end if else

    opendir (DIRS, "$lbdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^\w+?$/i, @files);
    my @recorddir = grep(/^record/i, @files);
    $recorddir = $recorddir[0];
    my @memfavdir = grep(/^memfav/i, @files);
    $memfavdir = $memfavdir[0];
    my @searchdir = grep(/^search/i, @files);
    $searchdir = $searchdir[0];

	&getmember("$inmember","no");

    $inmembername = $inmember;
        $inmembername =~ s/ /\_/isg;
	$inmembername =~ tr/A-Z/a-z/;

        # Delete the database for the member
	my $namenumber = &getnamenumber($inmembername);
	&checkmemfile($inmembername,$namenumber);
        unlink ("${lbdir}$searchdir/$inmembername\_sch.cgi");
        unlink ("${lbdir}$searchdir/$inmembername\_sav.cgi");
        unlink ("${lbdir}$memdir/$namenumber/$inmembername.cgi");
        unlink ("${lbdir}$memdir/old/$inmembername.cgi");
        unlink ("${lbdir}$msgdir/in/${inmembername}_msg.cgi");
        unlink ("${lbdir}$msgdir/out/${inmembername}_out.cgi");
        unlink ("${lbdir}$msgdir/main/${inmembername}_mian.cgi");
        unlink ("${lbdir}$memfavdir/$inmembername.cgi");
        unlink ("${lbdir}$memfavdir/open/$inmembername.cgi");
        unlink ("${lbdir}$memfavdir/close/$inmembername.cgi");
        unlink ("${lbdir}memfriend/$inmembername.cgi");
        unlink ("${lbdir}$recorddir/post/$inmembername.cgi");
        unlink ("${lbdir}$recorddir/reply/$inmembername.cgi");
        unlink ("${lbdir}memblock/$inmembername.cgi");
    	unlink ("${imagesdir}usravatars/$inmembername.gif");
    	unlink ("${imagesdir}usravatars/$inmembername.png");
    	unlink ("${imagesdir}usravatars/$inmembername.jpg");
    	unlink ("${imagesdir}usravatars/$inmembername.swf");
    	unlink ("${imagesdir}usravatars/$inmembername.bmp");
	unlink ("${lbdir}ebankdata/log/" . $inmembername . ".cgi");
	unlink ("${lbdir}cache/meminfo/$inmembername.pl");
	unlink ("${lbdir}cache/myinfo/$inmembername.pl");
	unlink ("${lbdir}cache/id/$inmembername.pl");
    	$memberfiletitletemp = unpack("H*","$inmembername");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.gif");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.png");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.jpg");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.swf");
    	unlink ("${imagesdir}usravatars/$memberfiletitletemp.bmp");

	&updateallsave(-1, -$mysaves) if ($mystatus);

	my $charone = substr($emailaddress, 0, 1);
	$charone = lc($charone);
	$charone = ord($charone);

	$/ = "";
	open (MEMFILE, "${lbdir}data/lbemail/$charone.cgi");
 	my $allmemberemails = <MEMFILE>;
 	close(MEMFILE);
	$/ = "\n";
	$allmemberemails =~ s/$emailaddress\t.+?\n//isg;
   	if (open (MEMFILE, ">${lbdir}data/lbemail/$charone.cgi")) {
	    print MEMFILE "$allmemberemails";
	    close (MEMFILE);
   	}

        $filetoopen = "$lbdir" . "data/banemaillist.cgi";
        open(FILE,"$filetoopen");
        $emaildata = <FILE>;
        close(FILE);
        @emaildata = split(/\t/,$emaildata);
        open(FILE,">$filetoopen");
        foreach (@emaildata) {
            chomp $_;
            print FILE "$_\t" if ($emailaddress ne $_);
	}
        close(FILE);

        $filetoopen = "$lbdir" . "data/baniplist.cgi";
        open(FILE,"$filetoopen");
        $ipdata = <FILE>;
        close(FILE);
        @ipdata = split(/\t/,$ipdata);
        open(FILE,">$filetoopen");
        foreach (@ipdata) {
            chomp $_;
            print FILE "$_\t" if ($ipaddress ne $_);
	}
        close(FILE);

        open(FILE,"${lbdir}data/lbmember.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE,">${lbdir}data/lbmember.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak,$no) = split(/\t/,$_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
	}
        close(FILE);
        open(FILE,"${lbdir}data/lbmember3.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE,">${lbdir}data/lbmember3.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak,$no) = split(/\t/,$_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
	}
        close(FILE);
        open(FILE,"${lbdir}data/lbmember4.cgi");
        @members = <FILE>;
        close(FILE);
        open(FILE,">${lbdir}data/lbmember4.cgi");
        foreach (@members) {
            chomp $_;
            my ($usernamerbak,$no) = split(/\t/,$_);
            print FILE "$_\n" if ($usernamerbak ne $inmember);
	}
        close(FILE);

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>ÓÃ»§ÒÑ¾­´ÓÊı¾İ¿âÖĞÍêÈ«É¾³ıÁË</b>
        </td></tr>
         ~;


} # end checkaction else

else {

        $cleanedmember = $inmember;
        $cleanedmember =~ s/\_/ /g;
	$inmember = uri_escape($inmember);

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>¾¯¸æ£¡£¡</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>Ö»ÓĞµã»÷ÏÂÃæµÄÁ´½Ó²Å¿ÉÒÔÉ¾³ıÓÃ»§<b>"$cleanedmember"</b><p>
        >> <a href="$thisprog?action=deletemember&checkaction=yes&member=$inmember">É¾³ıÓÃ»§</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
        }

} # end routine

sub unban {

        &getmember("$inmember");
    
    if ($membercode ne "banned") {
            print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>$inmember Ã»ÓĞ±»½ûÖ¹·¢ÑÔ°¡£¡</b></td></tr>";
            exit;
    }

        $memberfiletitle = $inmember;
        $memberfiletitle =~ s/ /\_/isg;
	$memberfiletitle =~ tr/A-Z/a-z/;
        unlink ("${lbdir}cache/meminfo/$memberfiletitle.pl");

        # Remove from ban lists

        $filetoopen = "$lbdir" . "data/banemaillist.cgi";
        open(FILE,"$filetoopen");
        $emaildata = <FILE>;
        close(FILE);
        @emaildata = split(/\t/,$emaildata);
        open(FILE,">$filetoopen");
        foreach (@emaildata) {
            chomp $_;
            print FILE "$_\t" if ($emailaddress ne $_);
	}
        close(FILE);

        $filetoopen = "$lbdir" . "data/baniplist.cgi";
        open(FILE,"$filetoopen");
        $ipdata = <FILE>;
        close(FILE);
        @ipdata = split(/\t/,$ipdata);
        open(FILE,">$filetoopen");
        foreach (@ipdata) {
            chomp $_;
            print FILE "$_\t" if ($ipaddress ne $_);
	}
        close(FILE);

        my $namenumber = &getnamenumber($memberfiletitle);
        &checkmemfile($memberfiletitle,$namenumber);
        $filetomake = "$lbdir" . "$memdir/$memberfiletitle.cgi";
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "$membername\t$password\t$membertitle\tme\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$allowedforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#333333><b>$membername ÒÑ¾­È¡Ïû½ûÖ¹·¢ÑÔ</b>
        </td></tr>
        ~;

} # end route

sub viewdelmembers { 
unless ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
print qq~ 
<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000> 
<b>´íÎó</b><p> 
<font color=#333333>ÄãÃ»ÓĞÈ¨ÏŞÊ¹ÓÃÕâ¸ö¹¦ÄÜ£¡</font> 
</td> 
</tr> 
~; 
exit; 
} 
print qq~ 
<tr> 
<td bgcolor=#FFFFFF colspan=2><br> 
~; 

$filetoopen = "$lbdir" . "data/delmember.cgi"; 
open(FILE,"$filetoopen"); 
flock (FILE, 1) if ($OS_USED eq "Unix"); 
@memberfiles = <FILE>; 
close(FILE); 
$i=-1; 
print qq~ 
<table width=100% border=0> 
<tr>~; 
foreach $memtypedata (@memberfiles) { 
if ($i > -1) { 
chomp $memtypedata; 
($username, $membertype) = split(/\t/,$memtypedata); 
$username=~ s/.cgi//isg; 
&getmember("$username");
$membername = $username if ($membername eq "");
print qq~ 
<td width=10%><a href="setmembers.cgi?action=undelmember&undelname=$membername" title="½«»áÔ± $membername ´ÓÔ¤É¾³ıÖĞÈ¡Ïû">$membername</a></td>~; ### ß@ĞĞ×òÌìÅªåeÒÑĞŞ¸Ä , Ö®Ç°ÓĞĞŞ¸Äß^µÄÈËÕˆ¸üĞÂÒ»ÏÂ 
} 
$i++; 
if ($i / 5 eq int($i/5)) {print qq~</tr><tr>~; 
} 
} 
print qq~</table> 
<br><br> 
<b><center>¹²ÓĞ $i Ãû»áÔ±·ûºÏÔ¤É¾³ı×Ê¸ñ</center></b><br> 
</td></tr> 
~; 
} 

sub undelmember { 
unless ((($membercode eq "ad")||($membercode eq "smo")) && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) { 
print qq~ 
<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000> 
<b>´íÎó</b><p> 
<font color=#333333>ÄãÃ»ÓĞÈ¨ÏŞÊ¹ÓÃÕâ¸ö¹¦ÄÜ£¡</font> 
</td> 
</tr> 
~; 
exit; 
} 
print qq~ 
<tr> 
<td bgcolor=#FFFFFF colspan=2><br> 
~; 
$filetoopen = "$lbdir" . "data/delmember.cgi"; 
open(FILE,"$filetoopen"); 
flock (FILE, 1) if ($OS_USED eq "Unix"); 
@memberfiles = <FILE>; 
close(FILE); 
$pretime=$memberfiles[0]; 
$i=0; 
open (FILE, ">${lbdir}data/delmember.cgi"); 
print FILE "$pretime"; 
close (FILE); 
foreach $memtypedata (@memberfiles) { 
if ($i > "0") { 
chomp $memtypedata; 
($username, $membertype) = split(/\t/,$memtypedata); 
$username=~ s/.cgi//isg; 
&getmember("$username"); 
if ($undelname ne $membername) { 
open (FILE, ">>${lbdir}data/delmember.cgi"); 
flock (FILE, 1) if ($OS_USED eq "Unix"); 
print FILE "$username\t$membertype\t\n"; 
close (FILE); 
} 
} 
$i++; 
} 
close(FILE); 
print qq~</table> 
<br><br> 
<b><center>»áÔ± $undelname ÒÑ´ÓÔ¤É¾³ıÃûµ¥ÖĞÈ¡Ïû</center></b><br> 
</td></tr> 
~; 
} 

sub boxaction {

   $oldmembercode = $membercode;
   &getmember("$inmember");
   if ((($membercode eq "ad")||($membercode eq "smo")||($membercode eq "cmo")||($membercode eq "amo")||($membercode eq "mo"))&&($oldmembercode eq "smo")) {
           print "<tr><td bgcolor=#EEEEEE colspan=2 align=center><font color=#333333><b>×Ü°ßÖñÎŞÈ¨²é¿´Ì³Ö÷ºÍ°ßÖñ×ÊÁÏ£¡</b></td></tr>";
           exit;
   }
   $inmembert=$inmember;
   $inmembert=~tr/A-Z/a-z/;
   if($box eq "inbox"){
   $filepath = "${lbdir}$msgdir/in/$inmembert\_msg.cgi";
   $boxname = "ÊÕ¼şÏä";
   }else{
   $filepath = "${lbdir}$msgdir/out/$inmembert\_out.cgi";
   $boxname = "·¢¼şÏä";
   }
   if($checkaction eq "delete"){
   unlink $filepath;
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>ÓÃ»§$boxnameÒÑ¾­É¾³ıÁË</b>
    </td></tr>
    ~;
   }else{
    open (FILE, "$filepath");
    my @messanges = <FILE>;
close (FILE);
    print qq~
<script>function HighlightAll(theField) {
var tempval=eval("document."+theField)
tempval.focus()
tempval.select()
therange=tempval.createTextRange()
therange.execCommand("Copy")}
</script>
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#333333><b>ÓÃ»§$boxnameµÄÑ¶Ï¢</b></td></tr>
    <tr>
    <form name="form2"><td bgcolor=#FFFFFF align=center colspan=2>
    <TEXTAREA name=inpost rows=12 style="width:90%">~;
$current_time=localtime;
foreach (@messanges) {
$messangeswords = $_;
($usrname, $msgread, $msgtime, $msgtitle, $msgwords) = split(/\t/,$_);
$usrname =~ s/^£ª£££¡£¦£ª//isg;
$usrname =~ s/ /\_/g;
$usrname =~ tr/A-Z/a-z/;
$msgwords =~ s/\r//ig;
$msgwords =~ s/ / /g;
$msgwords =~ s/"/\&quot;/g;
$msgwords =~ s/\s+/ /g;
$msgwords =~ s/<br>/\n/g;
$msgwords =~ s/<p>/\n/g;
$msgtime = $msgtime + ($timedifferencevalue*3600) + ($timezone*3600);
$msgtime = &dateformat("$msgtime");
    print qq~[ÊÕ·¢¶ÔÏó]£º$usrname\n[ÊÕ·¢Ê±¼ä]£º$msgtime\n[¶ÌĞÅ±êÌâ]£º$msgtitle\n[¶ÌĞÅÄÚÈİ]£º$msgwords\n\n~;
}
    print qq~</TEXTAREA><br>>> <a href="javascript:HighlightAll('form2.inpost')">¸´ÖÆµ½¼ôÌù°å <<</a></td></form></tr>~;
   }


}

sub updateallsave #ÀûÓÃ±ä»¯Á¿À´¸üĞÂ×ÜÁ¿ĞÅÏ¢
{
	my ($callusers, $callsaves) = @_;

	my $filetoopen = $lbdir . "ebankdata/allsaves.cgi";
	my $allusers = 0;
	my $allsaves = 0;
	&winlock($filetoopen) if ($OS_USED eq "Nt");
	if (-e $filetoopen)
	{
		open(FILE, $lbdir . "ebankdata/allsaves.cgi");
		flock(FILE, 1) if ($OS_USED eq "Unix");
		my $allinfo = <FILE>;
		close(FILE);
		chomp($allinfo);
		($allusers, $allsaves) = split(/,/, $allinfo);
	}

	$allusers += $callusers;
	$allsaves += $callsaves;

	if (open(FILE, ">$filetoopen"))
	{
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "$allusers,$allsaves";
		close(FILE);
	}
	&winunlock($filetoopen) if ($OS_USED eq "Nt");

	return;
}

print qq~</td></tr></table></body></html>~;
exit;
