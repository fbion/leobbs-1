#!/usr/bin/perl
#########################
# æ‰‹æœºè®ºå›WAPç‰ˆ
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
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
$query = new LBCGI;
$LBCGI::POST_MAX = 2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "wap.lib.pl";
require "data/styles.cgi";
require "wap.pl";
$|++;
&waptitle;
$show.= qq~
<card  title="$boardname">~;
$inmembername   = $query -> param('n');
$inmembername= $uref->fromUTF8("gb2312",$inmembername);
$password     = $query -> param('p');
$password2     = $query -> param('p1');
$emailaddress     = $query -> param('email');
$emailaddress  = lc($emailaddress);
if (($inmembername eq "")||($emailaddress eq "")) {
        &errorout("ç”¨æˆ·æ³¨å†Œ&è¯·è¾“å…¥ç”¨æˆ·åå’Œé‚®ä»¶åœ°å€ï¼Œè¿™äº›æ˜¯å¿…éœ€çš„ï¼");
    }
$ipaddress     = $ENV{'REMOTE_ADDR'};
    my $trueipaddress = $ENV{'HTTP_X_FORWARDED_FOR'};
    $trueipaddress = $ipaddress if ($trueipaddress eq "" || $trueipaddress eq "unknown" || $trueipaddress =~ m/^192\.168\./ || $trueipaddress =~ m/^10\./);
    my $trueipaddress1 = $ENV{'HTTP_CLIENT_IP'};
    $trueipaddress = $trueipaddress1 if ($trueipaddress1 ne "" && $trueipaddress1 ne "unknown" && $trueipaddress1 !~ m/^192\.168\./ && $trueipaddress1 !~ m/^10\./);
    $ipaddress = $trueipaddress;
my $charone = substr($emailaddress, 0, 1);
	$charone = lc($charone);
	$charone = ord($charone);
	if ($oneaccountperemail eq "yes") {
	    mkdir ("${lbdir}data/lbemail", 0777) if (!(-e "${lbdir}data/lbemail"));
	    chmod(0777,"${lbdir}data/lbemail");
	    $/ = "";
	    open (MEMFILE, "${lbdir}data/lbemail/$charone.cgi");
 	    my $allmemberemails = <MEMFILE>;
 	    close(MEMFILE);
	    $/ = "\n";
	    $allmemberemails = "\n$allmemberemails\n";
	    chomp($allmemberemails);
	    $allmemberemails = "\t$allmemberemails";

	    if ($allmemberemails =~ /\n$emailaddress\t(.+?)\n/i) {
		&errorout("ç”¨æˆ·æ³¨å†Œ&å¯¹ä¸èµ·ï¼Œè¿™è¾“å…¥çš„ Email å·²ç»è¢«æ³¨å†Œç”¨æˆ·ï¼š<u>$1</u> ä½¿ç”¨äº†");
	    }
	}
	 &errorout("ç”¨æˆ·æ³¨å†Œ&å¯¹ä¸èµ·ï¼Œæ‚¨è¾“å…¥çš„ç”¨æˆ·åï¼ˆ$inmembernameï¼‰æœ‰é—®é¢˜ï¼Œè¯·ä¸è¦åœ¨ç”¨æˆ·åä¸­åŒ…å«\@\#\$\%\^\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]è¿™ç±»å­—ç¬¦ï¼") if ($inmembername =~ /[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]/);
    if($inmembername =~ /_/)  { &errorout("ç”¨æˆ·æ³¨å†Œ&è¯·ä¸è¦åœ¨ç”¨æˆ·åä¸­ä½¿ç”¨ä¸‹åˆ’çº¿ï¼"); }
    $inmembername =~ s/\&nbsp\;//ig;
    $inmembername =~ s/ã€€/ /g;
    $inmembername =~ s/;
    $inmembername =~ s/ÿ//isg;
    $inmembername =~ s///isg;
    $inmembername =~ s/¡¡//isg;
    $inmembername =~ s/©¡//isg;
    $inmembername =~ s/()+//isg;
    $inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]//isg;
    $inmembername =~ s/\s*$//g;
    $inmembername =~ s/^\s*//g;
    &errorout("ÓÃ»§×¢²á&¶Ô²»Æğ£¬ÄúÊäÈëµÄÓÃ»§ÃûÓĞÎÊÌâ") if ($inmembername =~ /^q(.+?)-/ig || $inmembername =~ /^q(.+?)q/ig);
	$bannedmember = "no";
    open(FILE,"${lbdir}data/banemaillist.cgi");
    my $bannedemail = <FILE>;
    close(FILE);
    chomp $bannedemail;
    $bannedemail = "\t$bannedemail\t";
    $bannedemail =~ s/\t\t/\t/isg;
    my $emailaddresstemp = "\t$emailaddress\t";
    $bannedmember = "yes" if ($bannedemail =~ /$emailaddresstemp/i);
    $filetoopen = "$lbdir" . "data/baniplist.cgi";
    open(FILE,"${lbdir}data/baniplist.cgi");
    my $bannedips = <FILE>;
    close(FILE);
    chomp $bannedips;
    $bannedips = "\t$bannedips\t";
    $bannedips =~ s/\t\t/\t/isg;
    
    (my $ipaddresstemp = $ipaddress) =~ s/\./\\\./g;
    $ipaddresstemp =~ /^((((.*?\\\.).*?\\\.).*?\\\.).*?)$/;
    $bannedmember = "yes" if ($bannedips =~ /\t($1|$2|$3|$4)\t/);
    $bannedmember = "yes" if (($inmembername =~ /^m-/i)||($inmembername =~ /^s-/i)||($inmembername =~ /tr-/i)||($inmembername =~ /^y-/i)||($inmembername =~ /×¢²á/i)||($inmembername =~ /guest/i)||($inmembername =~ /qq-/i)||($inmembername =~ /qq/i)||($inmembername =~ /qw/i)||($inmembername =~ /q-/i)||($inmembername =~ /qx-/i)||($inmembername =~ /qw-/i)||($inmembername =~ /qr-/i)||($inmembername =~ /^È«Ìå/i)||($inmembername =~ /register/i)||($inmembername =~ /³ÏÆ¸ÖĞ/i)||($inmembername =~ /°ßÖñ/i)||($inmembername =~ /¹ÜÀíÏµÍ³Ñ¶Ï¢/i)||($inmembername =~ /leobbs/i)||($inmembername =~ /leoboard/i)||($inmembername =~ /À×°Á/i)||($inmembername =~ /LB5000/i)||($inmembername =~ /È«Ìå¹ÜÀíÈËÔ±/i)||($inmembername =~ /¹ÜÀíÔ±/i)||($inmembername =~ /ÒşÉí/i)||($inmembername =~ /¶ÌÏûÏ¢¹ã²¥/i)||($inmembername =~ /ÔİÊ±¿ÕÈ±/i)||($inmembername =~ /£ª£££¡£¦£ª/i)||($inmembername =~ /°æÖ÷/i)||($inmembername =~ /Ì³Ö÷/i)||($inmembername =~ /nodisplay/i)||($inmembername =~ /^system/i)||($inmembername =~ /---/i)||($inmembername eq "admin")||($inmembername eq "root")||($inmembername eq "copy")||($inmembername =~ /^sub/)||($inmembername =~ /^exec/)||($inmembername =~ /\@ARGV/i)||($inmembername =~ /^require/)||($inmembername =~ /^rename/i)||($inmembername =~ /^dir/i)||($inmembername =~ /^print/i)||($inmembername =~ /^con/i)||($inmembername =~ /^nul/i)||($inmembername =~ /^aux/i)||($inmembername =~ /^com/i)||($inmembername =~ /^lpt/i));
    if ($bannedmember eq "yes") { &errorout("ÓÃ»§×¢²á&²»ÔÊĞí×¢²á£¬ÄãÌîĞ´µÄÓÃ»§Ãû¡¢Email »òµ±Ç°µÄ IP ±»Ì³Ö÷ÉèÖÃ³É½ûÖ¹×¢²áĞÂÓÃ»§ÁË£¬Çë¸ü»»»òÕßÁªÏµÌ³Ö÷ÒÔ±ã½â¾ö£¡"); }
    open(THEFILE,"${lbdir}data/noreglist.cgi");
    $userarray = <THEFILE>;
    close(THEFILE);
    chomp $userarray;
    @saveduserarray = split(/\t/,$userarray);
    $noreg = "no";
    foreach (@saveduserarray) {
	chomp $_;
	$_ =~ s/\|/\\\|/isg;
	if ($inmembername =~ m/$_/isg) {
	    $noreg = "yes";
	    last;
	}
    }
    &errorout("ÓÃ»§×¢²á&¶Ô²»Æğ£¬ÄãËù×¢²áµÄÓÃ»§ÃûÒÑ¾­±»±£Áô»òÕß±»½ûÖ¹×¢²á£¬Çë¸ü»»Ò»¸öÓÃ»§Ãû£¡") if ($noreg eq "yes");
    if($inmembername =~ /\t/) { &errorout("ÓÃ»§×¢²á&Çë²»ÒªÔÚÓÃ»§ÃûÖĞÊ¹ÓÃÌØÊâ×Ö·û£¡"); }
    if($password =~ /[^a-zA-Z0-9]/)     { &errorout("ÓÃ»§×¢²á&ÂÛÌ³ÃÜÂëÖ»ÔÊĞí´óĞ¡Ğ´×ÖÄ¸ºÍÊı×ÖµÄ×éºÏ£¡£¡"); }
    if($password =~ /^lEO/)     { &errorout("ÓÃ»§×¢²á&ÂÛÌ³ÃÜÂë²»ÔÊĞíÊÇ lEO ¿ªÍ·£¬Çë¸ü»»£¡£¡"); }
    $tempinmembername =$inmembername;
    $tempinmembername =~ s/ //g;
    $tempinmembername =~ s/¡¡//g;
    if ($tempinmembername eq "")  { &errorout("ÓÃ»§×¢²á&ÄãµÄÓÃ»§ÃûÓĞµãÎÊÌâÓ´£¬»»Ò»¸ö£¡"); }
    if ($inmembername =~ /^¿ÍÈË/) { &errorout("ÓÃ»§×¢²á&Çë²»ÒªÔÚÓÃ»§ÃûµÄ¿ªÍ·ÖĞÊ¹ÓÃ¿ÍÈË×ÖÑù£¡"); }
    if (length($inmembername)>12) { &errorout("ÓÃ»§×¢²á&ÓÃ»§ÃûÌ«³¤£¬Çë²»Òª³¬¹ı12¸ö×Ö·û£¨6¸öºº×Ö£©£¡"); }
    if (length($inmembername)<2)  { &errorout("ÓÃ»§×¢²á&ÓÃ»§ÃûÌ«¶ÌÁË£¬Çë²»ÒªÉÙì¶2¸ö×Ö·û£¨1¸öºº×Ö£©£¡"); }
    if (length($newlocation)>12)  { &errorout("ÓÃ»§×¢²á&À´×ÔµØÇø¹ı³¤£¬Çë²»Òª³¬¹ı12¸ö×Ö·û£¨6¸öºº×Ö£©£¡"); }
    if (($inmembername =~ m/_/)||(!$inmembername)) { &errorout("ÓÃ»§×¢²á&ÓÃ»§ÃûÖĞº¬ÓĞ·Ç·¨×Ö·û£¡"); }
    if ($passwordverification eq "no"){
	if ($password ne $password2) { &errorout("ÓÃ»§×¢²á&¶Ô²»Æğ£¬ÄãÊäÈëµÄÁ½´ÎÂÛÌ³ÃÜÂë²»ÏàÍ¬£¡");   }
        if(length($password)<8)      { &errorout("ÓÃ»§×¢²á&ÂÛÌ³ÃÜÂëÌ«¶ÌÁË£¬Çë¸ü»»£¡ÂÛÌ³ÃÜÂë±ØĞë 8 Î»ÒÔÉÏ£¡"); }
#       if ($password =~ /^[0-9]+$/) { &errorout("ÓÃ»§×¢²á&ÂÛÌ³ÃÜÂëÇë²»ÒªÈ«²¿ÎªÊı×Ö£¬Çë¸ü»»£¡"); }
    }
    if ($inmembername eq $password) { &errorout("ÓÃ»§×¢²á&ÇëÎğ½«ÓÃ»§ÃûºÍÂÛÌ³ÃÜÂëÉèÖÃ³ÉÏàÍ¬£¡"); } 
    if($emailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,4})(\]?)$/) { &errorout("ÓÃ»§×¢²á&ÓÊ¼şµØÖ·´íÎó£¡"); }
    $emailaddress =~ s/[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
    &getmember("$inmembername","no");
    if ($userregistered ne "no") { &errorout("ÓÃ»§×¢²á&¸ÃÓÃ»§ÒÑ¾­´æÔÚ£¬ÇëÖØĞÂÊäÈëÒ»¸öĞÂµÄÓÃ»§Ãû£¡"); }
    $membercode    = "me";
    $memberfiletitle = $inmembername;
    $memberfiletitle =~ y/ /_/;
    $memberfiletitle =~ tr/A-Z/a-z/;
    $memberfiletitletemp = unpack("H*","$memberfiletitle");
    $joineddate=time;
    
    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod(0777,"${lbdir}$memdir/old");
    my $namenumber = &getnamenumber($memberfiletitle);
    $filetomake = "$lbdir" . "$memdir/$namenumber/$memberfiletitle.cgi";
    if (open(FILE, ">$filetomake")) {
        print FILE "$inmembername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$addjy\t$meili\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t\t\t$soccerdata\t0\t";
        close(FILE);
    }
    $filetomake = "$lbdir" . "$memdir/old/$memberfiletitle.cgi";
    if (open(FILE, ">$filetomake")) {
        print FILE "$inmembername\t$password\t$membertitle\t$membercode\t$numberofposts\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$newlocation\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t0\t$lastgone\t1\t$addjy\t$meili\t$mymoney\t0\t$sex\t$education\t$marry\t$work\t$born\t\t\t\t\t\t\t$userquestion\t\t\t\t$soccerdata\t0\t";
        close(FILE);
    }

    $filetomakeopen = "${lbdir}data/lbmember.cgi";
    if (open (MEMFILE, ">>$filetomakeopen")) {
	print MEMFILE "$inmembername\t$membercode\t0\t$joineddate\t$emailaddress\t\n";
	close (MEMFILE);
    }

   $filetomakeopen = "${lbdir}data/lbemail/$charone.cgi";
   if (open (MEMFILE, ">>$filetomakeopen")) {
	print MEMFILE "$emailaddress\t$inmembername\n";
	close (MEMFILE);
   }


    $filetomakeopen = "${lbdir}data/lbmember4.cgi";
    if (open (MEMFILE, ">>$filetomakeopen")) {
	print MEMFILE "$inmembername\t$ipaddress\t\n";
	close (MEMFILE);
    }
    
require "$lbdir" . "data/boardstats.cgi";
    $filetomake = "$lbdir" . "data/boardstats.cgi";
    my $filetoopens = &lockfilename($filetomake);
    if (!(-e "$filetoopens.lck")) {
	$totalmembers++;
	&winlock($filetomake) if ($OS_USED eq "Nt");
	if (open(FILE, ">$filetomake")) {
	    flock(FILE, 2) if ($OS_USED eq "Unix");
	    print FILE "\$lastregisteredmember = \'$inmembername\'\;\n";
	    print FILE "\$totalmembers = \'$totalmembers\'\;\n";
	    print FILE "\$totalthreads = \'$totalthreads\'\;\n";
	    print FILE "\$totalposts = \'$totalposts\'\;\n";
	    print FILE "\n1\;";
	    close (FILE);
	}
	&winunlock($filetomake) if ($OS_USED eq "Nt");
    }
    else {
    	unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
    }
    	FILE:my $x = &myrand(1000000000);
    $x = crypt($x, aun);
    $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
    $x =~ s/[^\w\d]//g;
    $x = substr($x, 2, 9);  
    if(-e "${lbdir}wap/$x"){goto FILE;}
    my $xh2 = $ENV{'REMOTE_ADDR'};
    open(file,">${lbdir}wap/$x");
    print file "$inmembername,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2";
    close(file);
    
    open(file,"${lbdir}wap/all.h");
    my @s=<file>;
    close(file);
    
    open(file,">${lbdir}wap/all.h");
    foreach(@s){
    	chomp;
    	my($n,$s)=split(/\,/,$_);
    	if($inmembername eq $n){
    		unlink "${lbdir}wap/$s";
    	}else{print file "$_\n";}
    }
    print file "$inmembername,$x\n";
    close(file);
$show.= qq~<p>
	×¢²á³É¹¦£¬ÄúµÄĞÒÔËIDÎª£º$x,ÄúµÄIPÎª£º$xh2£¬Çë²»ÒªĞ¹Â©ÄúµÄĞÒÔËID¸øÈÎºÎÈË£¡Èç¹ûÄúÊÇÓÃÊÖ»ú·ÃÎÊÇÒÊÖ»úÎªË½ÓĞ£¬Çë°ÑÏÂÃæ½øÈëµÄÊ×Ò³µØÖ·¼ÓÈëÊéÇ©(ÊéÇ©µØÖ·£º$boardurl/wap.cgi?lid=$x £¬¼ÓÈëÖ®ºó¿ÉÃâµÇÂ½) ¡£·ñÔòÇë²»Òª¼ÓÈëÊéÇ©£¡</p><p><a href="wap.cgi?lid=$x">µã»÷´Ë´¦½øÈëÊ×Ò³</a>
	</p>~;
&wapfoot;