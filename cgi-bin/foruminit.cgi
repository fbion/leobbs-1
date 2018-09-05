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
use File::Copy;
$loadcopymo = 1;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
require "data/cityinfo.cgi";

$|++;

$thisprog = "foruminit.cgi";

$query = new LBCGI;

$action          = $query -> param('action');
$inmember        = $query -> param('member');
$inmember        = &unHTML("$inmember");
$action          = &unHTML("$action");

$noofone         = $query -> param('noofone');
$noofone         = &unHTML("$noofone");
$beginone        = $query -> param('beginone');
$beginone        = &unHTML("$beginone");

$noofone      = 2000 if ($noofone !~ /^[0-9]+$/);
$beginone     = 0 if ($beginone !~ /^[0-9]+$/);

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
        
&getmember("$inmembername","no");
        
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / è®ºå›åˆå§‹åŒ–</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'updatecount'        =>    \&docount,
            'uptop'       	 =>    \&dotop,
            'uptopnext'       	 =>    \&dotopnext,
            'upemot'       	 =>    \&doemot,
            'upuser'       	 =>    \&doava,
            'delxzb'             =>    \&dodelallxzb,
            'shareforums'      	 =>    \&doshareforums,
            'dellock'      	 =>    \&dodellock,
            'changedir'		 =>    \&dochangedir,
            'uponlineuser'     	 =>    \&douponlineuser,
            'upconter'		 =>    \&doupconter,
            'init'        	 =>    \&doinit,
            'upupload'        	 =>    \&doupload,
            'uppost'        	 =>    \&dopost,
            'upmessage'        	 =>    \&domessage,
            'delmessage'         =>    \&dodalmessage,
            'delcache'           =>    \&dodelcache,
            'delans'             =>    \&dodelans,
            'dogetold'           =>    \&dogetold,
            'dogetoldnext'       =>    \&dogetoldnext,
            'upskinselect'       =>    \&upskinselect,

            );


            if($Mode{$action}) { 
               $Mode{$action}->();
            }
            else { &doinit; }
            
            print qq~</table></td></tr></table>~;
        }
        else {
            &adminlogin;
        }
        

sub upskinselect {
opendir (DIR, "${lbdir}data/skin"); 
my @dirdata = readdir(DIR);
closedir (DIR);
my @skinselectdata = grep(/\.(cgi)$/i,@dirdata);
map(s/\.cgi$//is, @skinselectdata);
    $skincount = @skinselectdata;
    my $userskin = qq~<div class="menuitems">&nbsp;<a href="index.cgi?action=change_skin&thisprog=' + url + '&skin="><font color=#000000>é»˜è®¤é£æ ¼</font></a>&nbsp;</div>~;
    for (my $i=0;$i<$skincount;$i++){
    	eval{ require "${lbdir}data/skin/$skinselectdata[$i].cgi"; };
    	next if ($@);
    	if ($cssname ne "") { $skinnames = $cssname; } else { $skinnames = $skinselectdata[$i]; }
        $skinselectdata[$i] = uri_escape($skinselectdata[$i]);
        $userskin.= qq~<div class="menuitems">&nbsp;<a href="index.cgi?action=change_skin&thisprog=' + url + '&skin=$skinselectdata[$i]"><font color=#000000>$skinnames</font></a>&nbsp;</div>~;
        $cssname = "";
    }

    $userskins = qq~
<script>
var url = new String (window.document.location);
url = url.replace (/&/g, "%26");
url = url.replace (/\\\\//g, "%2F");
url = url.replace (/:/g, "%3A");
url = url.replace (/\\\\?/g, "%3F");
url = url.replace (/=/g, "%3D");
linkset[3]='$userskin'</script>~;

$skinselect = qq~<img src=\$imagesurl/images/fg.gif width=1> <span style=cursor:hand onMouseover="showmenu(event,linkset[3])" onMouseout="delayhidemenu()">è®ºå›é£æ ¼&nbsp;</span>~;
			open(FILE, ">${lbdir}data/skinselect.pl");
    print FILE qq(\$userskins = qq~$userskins~;\n);
    print FILE qq(\$skinselect = qq~$skinselect~;\n);
    print FILE "1;\n";
			close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>åˆå§‹åŒ–è®ºå›é£æ ¼é€‰æ‹©åˆ—è¡¨</b><p>
                    
        <font color=#333333>æ‰€æœ‰è®ºå›é£æ ¼é€‰æ‹©åˆ—è¡¨å·²ç»æ›´æ–°ï¼</font>
                    
        </td></tr>
         ~;
}

sub doupload {
    chmod (0777,"$imagesdir");
    chmod (0777,"${imagesdir}$usrdir");
    chmod (0777,"${imagesdir}usravatars");
    chmod (0777,"${lbdir}FileCount");

    chmod (0777,"${lbdir}boarddata");
    chmod (0777,"${lbdir}lock");
    chmod (0777,"${lbdir}$saledir");
    chmod (0777,"${lbdir}memfav");
    chmod (0777,"${lbdir}memfriend");
    chmod (0777,"${lbdir}search");
    chmod (0777,"${lbdir}data");
    chmod (0777,"${lbdir}$memdir");
    chmod (0777,"${lbdir}$memdir/old");
    chmod (0777,"${lbdir}$msgdir");
    $filetoopen = "$lbdir" . "data/allforums.cgi";
    if (-e "$filetoopen") {
        open(FILE,"$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);
        
        foreach $_ (@allforums) {
            chomp $_;
            (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription,my $no) = split(/\t/,$_);
            next if (($forumid eq "")||($forumid !~ /^[0-9]+$/)||($category eq "")||($categoryplace eq "")||($forumname eq "")||($forumdescription eq ""));
            $dirtomake = "$lbdir" . "FileCount/$forumid";
            mkdir ("$dirtomake", 0777) if (!(-e "$dirtomake"));
            chmod (0777,"$dirtomake");
            $dirtomake = "$imagesdir" . "$usrdir/$forumid";
            mkdir ("$dirtomake", 0777) if (!(-e "$dirtomake"));
            chmod (0777,"$dirtomake");

	    &changemod("${lbdir}FileCount/$forumid");
	    &changemod("${imagesdir}$usrdir/$forumid");
	}
    }
    require "autochangeusrdir.pl";
    print qq~<tr>
<td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>æ–‡ä»¶ä¸Šä¼ ç›®å½•å±æ€§åˆå§‹åŒ–å®Œæˆï¼</b><p>
<font color=#333333>è¯·ç«‹å³æµ‹è¯•ä¸Šä¼ åŠŸèƒ½æ˜¯å¦å·²ç»æ­£å¸¸ï¼Œå¦‚æœè¿˜ä¸æ­£å¸¸ï¼Œè¯·å‚ç…§è®ºå›çš„å±æ€§è¯´æ˜æ–‡æ¡£ç”¨ FTP è½¯ä»¶è‡ªè¡Œè®¾ç½®ï¼ï¼</font>
</td></tr>
~;
}

sub dodelcache { 
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/\.pl$/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }

    opendir (DIRS, "${lbdir}");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^CGItemp/i, @files);
    foreach (@files) {unlink ("${lbdir}$_") if ((-M "${lbdir}$_") *86400 > 600);}

    opendir (DIRS, "${lbdir}cache/meminfo");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/meminfo/$_");
    }
    opendir (DIRS, "${lbdir}cache/mymsg");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/mymsg/$_");
    }

    opendir (DIRS, "${lbdir}cache/myinfo");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/myinfo/$_");
    }
    opendir (DIRS, "${lbdir}cache/id");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/id/$_");
    }
    opendir (DIRS, "${lbdir}cache/online");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/online/$_");
    }
   print qq~<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000><b>è®ºå›ç¼“å­˜å·²ç»å…¨éƒ¨æ¸…ç©ºï¼</b><p> 
</td></tr> 
~; 
}

sub dodalmessage { 
   $inbox = "${lbdir}$msgdir/in"; 
   opendir (DIR, "$inbox"); 
   my @inboxdata = readdir(DIR); 
   closedir (DIR);
   $inboxcount = @inboxdata;
   $inboxcount = $inboxcount - 2;
   foreach $filename(@inboxdata){ 
   $filepath=$inbox."/".$filename; 
   unlink ($filepath); 
   } 
   $outbox = "${lbdir}$msgdir/out"; 
   opendir (DIR, "$outbox"); 
   my @outboxdata = readdir(DIR); 
   closedir (DIR); 
   $outboxcount = @outboxdata;
   $outboxcount = $outboxcount - 2;
   foreach $filename(@outboxdata){ 
   $filepath=$outbox."/".$filename; 
   unlink ($filepath); 
   } 
   $outbox = "${lbdir}$msgdir/main"; 
   opendir (DIR, "$outbox"); 
   my @outboxdata = readdir(DIR); 
   closedir (DIR); 
   foreach $filename(@outboxdata){ 
   $filepath=$outbox."/".$filename; 
   unlink ($filepath); 
   } 
    opendir (DIRS, "${lbdir}cache/mymsg");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	unlink ("${lbdir}cache/mymsg/$_");
    }
   print qq~<tr> 
<td bgcolor=#FFFFFF align=center colspan=2> 
<font color=#990000><b>çŸ­æ¶ˆæ¯æ–‡ä»¶æ¸…ç©ºå®Œæˆï¼</b><p> 
<font color=#333333>æ”¶ä»¶ç®±å…±åˆ é™¤ $inboxcount ä¸ª,å‘ä»¶ç®±å…±åˆ é™¤ $outboxcount ä¸ª</font> 
</td></tr> 
~; 
}

sub domessage {

    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod (0777,"${lbdir}$msgdir");
    mkdir ("${lbdir}$msgdir/in", 0777) if (!(-e "${lbdir}$msgdir/in"));
    mkdir ("${lbdir}$msgdir/out", 0777) if (!(-e "${lbdir}$msgdir/out"));
    mkdir ("${lbdir}$msgdir/main", 0777) if (!(-e "${lbdir}$msgdir/main"));
    chmod (0777,"${lbdir}$msgdir/in");
    chmod (0777,"${lbdir}$msgdir/out");
    chmod (0777,"${lbdir}$msgdir/main");

    $dirtoopen = "${lbdir}$msgdir";
    opendir (DIR, "$dirtoopen");
    my @dirdata = readdir(DIR);
    closedir (DIR);
	
    @data1 = grep(/\_msg\.cgi/i,@dirdata);
    foreach (@data1) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/in/$_");
    }
    @data1 = grep(/\_out\.cgi/i,@dirdata);
    foreach (@data1) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/out/$_");
    }
    @data1 = grep(/\_main\.cgi/i,@dirdata);
    foreach (@data1) {
	copy("${lbdir}$msgdir/$_","${lbdir}$msgdir/main/$_");
    }

    $dirtoopen = "${lbdir}$msgdir";
    opendir (DIR, "$dirtoopen");
    my @files = readdir(DIR);
    closedir (DIR);
    foreach (@files) {
        chomp $_;
        unlink ("${lbdir}$msgdir/$_");
    }

    &changemod("${lbdir}$msgdir/in");
    &changemod("${lbdir}$msgdir/out");
    &changemod("${lbdir}$msgdir/main");

    print qq~<tr>
<td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>çŸ­æ¶ˆæ¯ç›®å½•å’Œæ–‡ä»¶å±æ€§åˆå§‹åŒ–å®Œæˆï¼</b><p>
<font color=#333333>è¯·ç«‹å³æµ‹è¯•çŸ­æ¶ˆæ¯åŠŸèƒ½æ˜¯å¦å·²ç»æ­£å¸¸ï¼Œå¦‚æœè¿˜ä¸æ­£å¸¸ï¼Œè¯·å‚ç…§è®ºå›çš„å±æ€§è¯´æ˜æ–‡æ¡£ç”¨ FTP è½¯ä»¶è‡ªè¡Œè®¾ç½®ï¼ï¼</font>
</td></tr>
~;
}

sub dopost {

    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod (0777,"${lbdir}boarddata");
    chmod (0777,"${lbdir}lock");
    chmod (0777,"${lbdir}$saledir");
    chmod (0777,"${lbdir}memfav");
    chmod (0777,"${lbdir}memfriend");
    chmod (0777,"${lbdir}search");
    chmod (0777,"${lbdir}data");
    chmod (0777,"${lbdir}data/skin");
    chmod (0777,"${lbdir}$memdir");
    chmod (0777,"${lbdir}$memdir/old");

    chmod (0777,"${lbdir}FileCount");
    chmod (0777,"${lbdir}$msgdir");
    chmod (0777,"$imagesdir");
    chmod (0777,"${imagesdir}$usrdir");
    chmod (0777,"${imagesdir}usravatars");


    &changemod("${lbdir}boarddata");
    &changemod("${lbdir}lock");
    &changemod("${lbdir}$saledir");
    &changemod("${lbdir}memfav");
    &changemod("${lbdir}memfriend");
    &changemod("${lbdir}search");
    &changemod("${lbdir}data");
    &changemod("${lbdir}data/skin");
    &changemod("${lbdir}$memdir");
    &changemod("${lbdir}$memdir/old");
   chmod (0777,"${lbdir}data/lbmail");
   chmod (0777,"${lbdir}data/myskin");
   chmod (0777,"${lbdir}data/skin");
   chmod (0777,"${lbdir}data/template");

    $filetoopen = "$lbdir" . "data/allforums.cgi";
    if (-e "$filetoopen") {
        &winlock($filetoopen) if ($OS_USED eq "Nt");
        open(FILE,"$filetoopen");
        flock(FILE, 1) if ($OS_USED eq "Unix");
        @allforums = <FILE>;
        close(FILE);
        &winunlock($filetoopen) if ($OS_USED eq "Nt");
        
        foreach $_ (@allforums) {
            chomp $_;
            (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription,my $no) = split(/\t/,$_);
            next if (($forumid eq "")||($forumid !~ /^[0-9]+$/)||($category eq "")||($categoryplace eq "")||($forumname eq "")||($forumdescription eq ""));
            $dirtomake = "$lbdir" . "forum$forumid";
            mkdir ("$dirtomake", 0777) if (!(-e "$dirtomake"));
            chmod (0777,"$dirtomake");
	    &changemod("${lbdir}forum$forumid");
	}
    }
    print qq~<tr>
<td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>è®ºå›å¸–å­ç›®å½•å’Œæ•°æ®æ–‡ä»¶å±æ€§åˆå§‹åŒ–å®Œæˆï¼</b><p>
<font color=#333333>è¯·ç«‹å³æµ‹è¯•è®ºå›æ•°æ®æ˜¯å¦å·²ç»æ­£å¸¸ï¼Œå¦‚æœè¿˜ä¸æ­£å¸¸ï¼Œè¯·å‚ç…§è®ºå›çš„å±æ€§è¯´æ˜æ–‡æ¡£ç”¨ FTP è½¯ä»¶è‡ªè¡Œè®¾ç½®ï¼ï¼</font>
</td></tr>
~;
}

sub changemod {
    my $dirname =shift;
    opendir (DIR, $dirname);
    my @dirdata = readdir(DIR);
    closedir (DIR);
    foreach (@dirdata) {
    	chomp $_;
    	next if (($_ eq ".")||($_ eq ".."));
        chmod (0666, "$dirname/$_");
    }
    return;
}

sub docount {

    opendir (DIR, "${lbdir}$memdir/old"); 
    @filedata = readdir(DIR);
    closedir (DIR);
    @countvar = grep(/\.cgi$/i,@filedata);
    $newtotalmembers = @countvar;

        require "$lbdir" . "data/boardstats.cgi";
        
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        
        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");
        print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
        print FILE "\$totalmembers = \'$newtotalmembers\'\;\n";
        print FILE "\$totalthreads = \'$totalthreads\'\;\n";
        print FILE "\$totalposts = \'$totalposts\'\;\n";
        print FILE "\n1\;";
        close (FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");
    
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>è®¡ç®—ç”¨æˆ·æ€»æ•°</b><p>
                    
        <font color=#333333>å½“å‰å…±æœ‰ $newtotalmembers ä¸ªæ³¨å†Œç”¨æˆ·ï¼Œæ•°æ®å·²ç»æ›´æ–°ï¼</font>
                    
        </td></tr>
         ~;

}

sub dogetold {

    chmod (0777,"${lbdir}$memdir");
    mkdir ("${lbdir}$memdir/old", 0777) if (!(-e "${lbdir}$memdir/old"));
    chmod (0777,"${lbdir}$memdir/old");

    opendir (DIR, "${lbdir}$memdir"); 
    @filedata = readdir(DIR);
    closedir (DIR);
    @countvar = grep(/\.cgi$/i,@filedata);
    
    open(FILE,">${lbdir}data/allname.pl");
    foreach (@countvar) {
        print FILE "$_\n";
    }
    $totaluserdata = @countvar;

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>æ³¨å†Œç”¨æˆ·æ•´ç†</b><br>
                    
        <font color=#333333><B>å½“å‰å…±æœ‰ $totaluserdata ä¸ªæ³¨å†Œç”¨æˆ·éœ€è¦æ•´ç†ï¼Œå‡†å¤‡å·¥ä½œå·²ç»å®Œæˆã€‚</b><BR><BR><BR>
	<form action="foruminit.cgi" method=get>
        <input type=hidden name="action" value="dogetoldnext">è¾“å…¥æ¯æ¬¡è¿›è¡Œæ•´ç†çš„ç”¨æˆ·æ•° 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=3 maxlength=3 value=300>
        <input type=submit value="å¼€å§‹æ•´ç†">
        </form>
	ä¸ºäº†å‡å°‘èµ„æºå ç”¨ï¼Œè¯·è¾“å…¥æ¯æ¬¡è¿›è¡Œæ’åçš„ç”¨æˆ·æ•°ï¼Œé»˜è®¤ 300ï¼Œ<BR>ä¸€èˆ¬ä¸è¦è¶…è¿‡ 600ï¼Œå¦‚æœå‘ç°è¿›è¡Œæ’åæ— æ³•æ­£å¸¸å®Œæˆï¼Œè¯·å°½é‡å‡å°‘è¿™ä¸ªæ•°ç›®ï¼Œå»¶é•¿æ’åæ—¶é—´ã€‚
	<BR><BR>

        </td></tr>
         ~;
} # end routine

sub dogetoldnext {

    open(FILE,"${lbdir}data/allname.pl");
    @allname = <FILE>;
    close(FILE);
    $allnamenum = @allname;
    $currenttime = time;
    
    if ($beginone < $allnamenum) {
        $lastone = $beginone + $noofone;
        $lastone = $allnamenum if ($lastone > $allnamenum);

	for ($i = $beginone; $i < $lastone; $i ++) {
	    $memberfile = $allname[$i];
	    chomp $memberfile;
	    ($memberfile, $no) = split(/\./,$memberfile);
	    my $namenumber = &getnamenumber($memberfile);
	    &checkmemfile($memberfile,$namenumber);
	    $usrfileopen = "${lbdir}$memdir/$namenumber/$memberfile.cgi";

	        open (FILE, "$usrfileopen");
	        $line = <FILE>;
	        close (FILE);
	        chomp $line;
	        @memberdaten = split(/\t/,$line);
	        $lastgone = $memberdaten[26] + 6*3600*24;
    	        open(FILE,">${lbdir}$memdir/old/$memberfile.cgi");
	        print FILE "$line\n";
	        close(FILE);
	} 

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>ç”¨æˆ·æ•´ç†</b><p>
        <font color=#333333><B>å½“å‰å…±æœ‰ $allnamenum ä¸ªæ³¨å†Œç”¨æˆ·éœ€è¦æ•´ç†ï¼Œå·²ç»è¿›è¡Œæ•´ç†äº† $lastone ä¸ªç”¨æˆ·ã€‚ã€‚ã€‚</b><BR><BR><BR>
        <font color=#333333>å¦‚æœæ— æ³•è‡ªåŠ¨å¼€å§‹ä¸‹ $noofone ä¸ªç”¨æˆ·çš„æ•´ç†ï¼Œè¯·ç‚¹å‡»ä¸‹é¢çš„é“¾æ¥ç»§ç»­<p>
        >> <a href="$thisprog?action=dogetoldnext&beginone=$lastone&noofone=$noofone">ç»§ç»­è¿›è¡Œç”¨æˆ·æ•´ç†</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=dogetoldnext&beginone=$lastone&noofone=$noofone">
	<BR><BR>

        </td></tr>
         ~;
     }
     else {

    opendir (DIR, "${lbdir}$memdir"); 
    @filedata = readdir(DIR);
    closedir (DIR);
    @countvar = grep(/\.cgi$/i,@filedata);
    $totaluserdata = @countvar;
    
    unlink ("${lbdir}data/allname.pl");

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>ç”¨æˆ·æ•´ç†</b><p>
                    
        <font color=#333333>ç”¨æˆ·æ•´ç†å·²ç»ç»“æŸï¼<BR><BR>
        </td></tr>
         ~;
     }

}

sub dotop {
	
    opendir (DIR, "${lbdir}$memdir/old");
    @filedata = readdir(DIR);
    closedir (DIR);
    @countvar = grep(/\.cgi$/i,@filedata);
    $totaluserdata = @countvar;
    
    open(FILE,">${lbdir}$memdir/allname.pl");
    foreach (@countvar) {
        print FILE "$_\n";
    }
    close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>ç”¨æˆ·æ’ååˆå§‹åŒ–</b><br>
                    
        <font color=#333333><B>å½“å‰å…±æœ‰ $totaluserdata ä¸ªæ³¨å†Œç”¨æˆ·ï¼Œå‡†å¤‡å·¥ä½œå·²ç»å®Œæˆã€‚</b><BR><BR><BR>
	<form action="foruminit.cgi" method=get>
        <input type=hidden name="action" value="uptopnext">è¾“å…¥æ¯æ¬¡è¿›è¡Œæ’åçš„ç”¨æˆ·æ•° 
        <input type=hidden name="beginone" value=0>
        <input type=text name="noofone" size=4 maxlength=4 value=2000>
        <input type=submit value="å¼€å§‹æ’å">
        </form>
	ä¸ºäº†å‡å°‘èµ„æºå ç”¨ï¼Œè¯·è¾“å…¥æ¯æ¬¡è¿›è¡Œæ’åçš„ç”¨æˆ·æ•°ï¼Œé»˜è®¤ 2000ï¼Œ<BR>ä¸€èˆ¬ä¸è¦è¶…è¿‡ 3000ï¼Œå¦‚æœå‘ç°è¿›è¡Œæ’åæ— æ³•æ­£å¸¸å®Œæˆï¼Œè¯·å°½é‡å‡å°‘è¿™ä¸ªæ•°ç›®ï¼Œå»¶é•¿æ’åæ—¶é—´ã€‚
	<BR><BR>

        </td></tr>
         ~;
} # end routine

sub dotopnext {

    $filename = "alluser.pl";
    open(FILE,"${lbdir}$memdir/allname.pl");
    @allname = <FILE>;
    close(FILE);
    $allnamenum = @allname;
    if ($beginone < $allnamenum) {
        $lastone = $beginone + $noofone;
        $lastone = $allnamenum if ($lastone > $allnamenum);

        if ($beginone == 0) {
            unlink ("${lbdir}data/lbmember.cgi")  ;
            unlink ("${lbdir}data/lbmember0.cgi")  ;
            unlink ("${lbdir}data/lbmember1.cgi") ;
            unlink ("${lbdir}data/lbmember3.cgi") ;
            unlink ("${lbdir}data/lbmember4.cgi") ;
        }

	open  (MEMFILE, ">>${lbdir}data/lbmember.cgi");
	flock (MEMFILE, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE0, ">>${lbdir}data/lbmember0.cgi");
	flock (MEMFILE0, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE1, ">>${lbdir}data/lbmember1.cgi");
	flock (MEMFILE1, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE3, ">>${lbdir}data/lbmember3.cgi");
	flock (MEMFILE3, 2) if ($OS_USED eq "Unix");
	open  (MEMFILE4, ">>${lbdir}data/lbmember4.cgi");
	flock (MEMFILE4, 2) if ($OS_USED eq "Unix");

	for ($i = $beginone; $i < $lastone; $i ++) {
	    $memberfile = $allname[$i];
	    chomp $memberfile;
	    ($memberfile, $no) = split(/\./,$memberfile);
	    my $namenumber = &getnamenumber($memberfile);
	    &checkmemfile($memberfile,$namenumber);
	    
	    my $usrfileopen = "${lbdir}$memdir/$namenumber/$memberfile.cgi";
	    open (FILE, "$usrfileopen");
	    flock (FILE, 1) if ($OS_USED eq "Unix");
	    $line = <FILE>;
	    close (FILE);
	    chomp $line;
	    @memberdaten = split(/\t/,$line);
	    $username =$memberdaten[0];   
	    $userad=$memberdaten[3];
	    $anzahl = $memberdaten[4];
	    ($anzahl1, $anzahl2) = split(/\|/,$anzahl);
	    $anzahl1 = 0 if ($anzahl1 eq "");
	    $anzahl2 = 0 if ($anzahl2 eq "");
	    $anzahl   = $anzahl1 + $anzahl2;
	    $useremail=$memberdaten[5];
	    $date1    = $memberdaten[13];
	    $logtime = $memberdaten[27];
	    $jifen   = $memberdaten[45];
	    $mymoney = $memberdaten[30];
	    $postdel = $memberdaten[31];
	    $jhcount = $memberdaten[40];
	    $jifen = $memberdaten[45];

	    $logtime = 0 if ($logtime eq "");
	    $mymoney = 0 if ($mymoney eq "");
	    $postdel = 0 if ($postdel eq "");
	    $jhcount = 0 if ($jhcount eq "");

	if ($jifen eq "") {
		$jifen = $anzahl1 * $ttojf + $anzahl2 * $rtojf - $postdel * $deltojf;
  }

    $mymoney = $anzahl1 * $addmoney + $anzahl2 * $replymoney + $logtime * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;

	    $birthday = $memberdaten[36];

	    print MEMFILE  "$username\t$userad\t$anzahl\t$date1\t$useremail\t$mymoney\t$jhcount\t$jifen\t\n";   
	    print MEMFILE0 "$username\t$anzahl\t\n" if ($anzahl > 0);   
	    print MEMFILE1 "$useremail\t$username\n";   
	    print MEMFILE3 "$username\t$birthday\t\n" if (($birthday ne "")&&($birthday ne "//"));  
	    print MEMFILE4 "$username\t".$memberdaten[7]."\t\n" if ($memberdaten[7] =~/^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$/);  
	} 
	close(MEMFILE4);
	close(MEMFILE3);
	close(MEMFILE1);
	close(MEMFILE0);
	close(MEMFILE);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
        <b>è®¡ç®—ç”¨æˆ·æ’å</b><p>
        <font color=#333333><B>å½“å‰å…±æœ‰ $allnamenum ä¸ªæ³¨å†Œç”¨æˆ·ï¼Œå·²ç»è¿›è¡Œæ’åäº† $lastone ä¸ªç”¨æˆ·ã€‚ã€‚ã€‚</b><BR><BR><BR>
        <font color=#333333>å¦‚æœæ— æ³•è‡ªåŠ¨å¼€å§‹ä¸‹ $noofone ä¸ªç”¨æˆ·çš„æ’åï¼Œè¯·ç‚¹å‡»ä¸‹é¢çš„é“¾æ¥ç»§ç»­<p>
        >> <a href="$thisprog?action=uptopnext&beginone=$lastone&noofone=$noofone">ç»§ç»­è¿›è¡Œæ’åç”¨æˆ·</a> <<
	<meta http-equiv="refresh" content="2; url=$thisprog?action=uptopnext&beginone=$lastone&noofone=$noofone">
	<BR><BR>

        </td></tr>
         ~;
     }
     else {


open (FILE, "$lbdir/data/lbmember0.cgi");
flock(FILE, 1) if ($OS_USED eq "Unix");
my @file = <FILE>;
close (FILE);
foreach my $line (@file) {
my @tmpuserdetail = split (/\t/, $line);
chomp @tmpuserdetail;
$postundmember {"$tmpuserdetail[0]"} = $tmpuserdetail[1];
}
my @sortiert = reverse sort { $postundmember{$a} <=> $postundmember{$b} } keys(%postundmember);

open  (MEMFILE0, ">${lbdir}data/lbmember0.cgi");
flock (MEMFILE0, 2) if ($OS_USED eq "Unix");
foreach my $member (@sortiert[0 ... 99]) {
    next if ($member eq "");
    print MEMFILE0 "$member\t$postundmember{\"$member\"}\t\n";
}
close(MEMFILE0);

open (MEMFILE, "${lbdir}data/lbmember3.cgi");
@birthdaydata = <MEMFILE>;
close (MEMFILE);
foreach(@birthdaydata){
chomp $_;
next if($_ eq "");
(my $biruser, my $borns) = split(/\t/,$_);
(my $biryear, my $birmon, my $birday) = split(/\//, $borns);
$birmon = $birmon - 0;
next if ($birmon > 12 || $birmon < 1);
$birdayinfo[$birmon] = "$birdayinfo[$birmon]$_\n";
}
for ($i=1;$i<=12;$i++) {
open(FILE, ">${lbdir}calendar/borninfo$i.cgi");
print FILE "$birdayinfo[$i]";
close(FILE);
}

mkdir("${lbdir}data/lbemail",0777) unless (-e "${lbdir}data/lbemail");
chmod(0777,"${lbdir}data/lbemail");

open(MEMFILE, "${lbdir}data/lbmember1.cgi");
my @emails = <MEMFILE>;
close(MEMFILE);
for (0..255)
{
       my $char = chr($_);
       next if ($char =~ /[\ \a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|A-Z]/);
       $char = '\$char' if ($char eq '[' || $char eq ']' || $char eq '.');
       my @thismails = grep(m/^$char/i, @emails);
       open(FILE, ">${lbdir}data/lbemail/$_.cgi");
       foreach (@thismails) {print FILE $_;}
       close(FILE);
}

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>è®¡ç®—ç”¨æˆ·æ’å</b><p>
                    
        <font color=#333333>å½“å‰å…±æœ‰ $allnamenum ä¸ªæ³¨å†Œç”¨æˆ·ï¼Œè®¡ç®—ç”¨æˆ·æ’åå·²ç»ç»“æŸï¼<BR><BR>
        </td></tr>
         ~;
     }

}

sub doemot {

$dirtoopen = "$imagesdir" . "emot";
opendir (DIR, "$dirtoopen"); 
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/\.(gif|jpg)$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbemot.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);
			open(FILE, "${lbdir}data/lbemot.cgi");
			my @emoticondata = <FILE>;
			close(FILE);
			chomp(@emoticondata);
			map(s/\.gif$//is, @emoticondata);

			$emoticoncode = join('|', @emoticondata);
			$emoticoncode = "\$\$post =~ s/\\:($emoticoncode)\\:/<img src=\${imagesurl}\\/emot\\/\$1\\.gif>/isg;";

			open(FILE, ">${lbdir}data/emot.pl");
			print FILE $emoticoncode;
			close(FILE);

$dirtoopen = "$imagesdir" . "posticons";
opendir (DIR, "$dirtoopen");
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/\.(gif|jpg)$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbpost.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);
        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>åˆå§‹åŒ–EMOTå’ŒPOSTå›¾ç‰‡</b><p>
                    
        <font color=#333333>æ‰€æœ‰EMOTå’Œè¡¨æƒ…å›¾ç‰‡å·²ç»æ›´æ–°ï¼</font>
                    
        </td></tr>
         ~;
}         
     
sub doava {
$dirtoopen = "$imagesdir" . "avatars";
opendir (DIR, "$dirtoopen");
my @dirdata = readdir(DIR);
closedir (DIR);
my @emoticondata = grep(/\.(gif|jpg)$/i,@dirdata);

open (EMFILE, ">${lbdir}data/lbava.cgi");
foreach $picture (@emoticondata) { 
    print EMFILE "$picture\n";   
    }  
close(EMFILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>åˆå§‹åŒ–ç”¨æˆ·å¤´åƒå›¾ç‰‡</b><p>
                    
        <font color=#333333>æ‰€æœ‰ç”¨æˆ·å¤´åƒå›¾ç‰‡å·²ç»æ›´æ–°ï¼</font>
                    
        </td></tr>
         ~;

}

sub doupconter {
	my $onlinemaxtime = time;
	my $filetomake = "$lbdir" . "data/counter.cgi";
	open(FILE,">$filetomake");
        print FILE "1\t1\t1\t$onlinemaxtime\t";
	close(FILE);

        print qq~
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#990000>
                    
        <b>åˆå§‹åŒ–åœ¨çº¿ç»Ÿè®¡åŠè®¿é—®æ¬¡æ•°</b><p>
                    
        <font color=#333333>è®¿é—®æ¬¡æ•°æ•°æ®å·²ç»åˆå§‹åŒ–ï¼</font>
                    
        </td></tr>
         ~;

}
	
sub douponlineuser {
	$currenttime = time;
        open(FILES,">${lbdir}data/onlinedata.cgi");
	print FILES "$inmembername\t$currenttime\t$currenttime\tç®¡ç†åŒº\tä¿å¯†\tä¿å¯†\tä¿å¯†\tç®¡ç†åŒº\tä¿å¯†\t$membercode\t" ;
	close (FILES);
        open(FILES,">${lbdir}data/onlinedata.cgi.cgi");
	print FILES "$inmembername\t$currenttime\t$currenttime\tç®¡ç†åŒº\tä¿å¯†\tä¿å¯†\tä¿å¯†\tç®¡ç†åŒº\tä¿å¯†\t$membercode\t" ;
	close (FILES);

        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>åˆå§‹åŒ–åœ¨çº¿ç»Ÿè®¡åŠè®¿é—®æ¬¡æ•°</b><p>
<font color=#333333>åœ¨çº¿äººæ•°ç»Ÿè®¡æ•°æ®å·²ç»åˆå§‹åŒ–ï¼</font></td></tr>
~;
}

sub dodelallxzb {
    opendir (DIRS, "${lbdir}boarddata");
    my @files = readdir(DIRS);
    closedir (DIRS);
    my @files = grep(/^xzb/i, @files);
    foreach (@files) {
    	chomp $_;
	unlink ("${lbdir}boarddata/$_");
    }
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>åˆå§‹åŒ–æ‰€æœ‰è®ºå›çš„å°å­—æŠ¥</b><p>
<font color=#333333>æ‰€æœ‰è®ºå›çš„å°å­—æŠ¥å·²ç»åˆå§‹åŒ–ï¼</font>
</td></tr>
~;
}

sub dodelans {
    opendir (DIRS, "${lbdir}data");
    my @files = readdir(DIRS);
    closedir (DIRS);
    my @files = grep(/^new/i, @files);
    foreach (@files) {
    	chomp $_;
	unlink ("${lbdir}data/$_");
    }
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>åˆå§‹åŒ–æ‰€æœ‰è®ºå›çš„å…¬å‘Š</b><p>
<font color=#333333>æ‰€æœ‰è®ºå›çš„å…¬å‘Šå·²ç»åˆå§‹åŒ–ï¼</font>
</td></tr>
~;

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata = grep(/^announce/,@dirdata);
foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
}	

sub doshareforums {
	my $filetoopen = "$lbdir" . "data/shareforums.cgi";
	open(FILE, ">$filetoopen");
	print FILE "é›·å‚²ç§‘æŠ€\thttp:\/\/www.leoBBS.com\/\tLeoBBS æœ€æ–°ç‰ˆæœ¬ä»‹ç»ï¼Œæœ€æ–°ç‰ˆæœ¬å…è´¹ä¸‹è½½ï¼Œè®ºå›æŠ€æœ¯æ”¯æŒï¼Œè™šæ‹Ÿä¸»æœºä»¥åŠåŸŸåç”³è¯·ç­‰ã€‚ã€‚\t1\t$imagesurl\/images\/leotech8831.gif\t\n";
	print FILE "æé…·è¶…çº§è®ºå›\thttp:\/\/bbs.leobbs.com\/\tæœ€æ–°è½¯ä»¶ã€å½±è§†ã€éŸ³ä¹ã€ç½‘ç»œå®‰å…¨ã€å›¾å½¢è‰ºæœ¯ã€æ¸¸æˆã€CGI çŸ¥è¯†ç­‰ç»¼åˆè®ºå›ï¼Œè¿˜å¯ä»¥èŠå¤©ã€‚ã€‚ã€‚\t2\t$imagesurl\/images\/leobbs8831.gif\t\n";
	close(FILE);
        print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>åˆå§‹åŒ–è®ºå›è”ç›Ÿæ•°æ®ä¸ºç©º</b><p>
<font color=#333333>åœ¨çº¿è”ç›Ÿæ•°æ®å·²ç»åˆå§‹åŒ–ï¼</font>
</td></tr>
~;

if (open(SFFILE,"${lbdir}data/shareforums.cgi")) {
#    flock(SFFILE, 1) if ($OS_USED eq "Unix");
    @lmforums = <SFFILE>;
    close(SFFILE);
    $lmforums = @lmforums;
}
$uniontitle="<font color=$fontcolormisc>ï¼ˆå…±æœ‰ $lmforums ä¸ªè”ç›Ÿè®ºå›ï¼‰</font>";
$unionoutput = "";
  if (($lmforums ne "")&&($lmforums > 0)) {
    $unionoutput .= qq~
<tr><td bgcolor=\$titlecolor colspan=2  \$catbackpic>
<font color=\$titlefontcolor><b>-=> è”ç›Ÿè®ºå› $uniontitle</b>ã€€ [<a href=leobbs.cgi?action=union><font color=$fontcolormisc>\$unionview</font></a>]ã€€ [<span style="cursor:hand" onClick="javascript:openScript('lmcode.cgi',480,240)">è®ºå›è”ç›Ÿä»£ç </span>]
</td></tr>~;

$unionoutput1 = "";
	$lmtexts = "";
	$lmlogos = "";
	foreach $lmforum (@lmforums) {
	    chomp $lmforum;
            next if ($lmforum eq "");
            ($lmforumname,$lmforumurl,$lmforuminfo,$lmfogn=right><a href=http://bbs.leobbs.com/ target=_blank><img src=$imagesurl/images/leobbs8831.gif width=88 height=31 border=0 title="¼«¿á³¬¼¶ÂÛÌ³×îĞÂÈí¼ş¡¢Ó°ÊÓ¡¢ÒôÀÖ¡¢ÍøÂç°²È«¡¢Í¼ĞÎÒÕÊõ¡¢ÓÎÏ·¡¢CGI ÖªÊ¶µÈ×ÛºÏÂÛÌ³£¬»¹¿ÉÒÔÁÄÌì¡£¡£¡£"></a></td></tr></table></td></tr>~ if ($lmlogos ne "");
	$unionoutput1 .= qq~<tr><td bgcolor=\$forumcolorone width=26 align=center><img src=$imagesurl/images/\$skin/shareforum.gif width=16></td><td bgcolor=\$forumcolortwo width=*><table width=100% cellpadding=0 cellspacing=0><tr><td width=100%><img src=\$imagesurl/images/none.gif width=500 height=1><BR><marquee name="lmforum1" id="lmforum1"  behavior="alternate" direction="left" scrollamount="4" scrolldelay="1" hspace="0" vspace="0">$lmtexts</marquee></td></tr></table></td></tr>~ if ($lmtexts ne "");

  }

mkdir ("${lbdir}cache", 0777) if (!(-e "${lbdir}cache"));
open (FILE, ">${lbdir}data/unionoutput.pl");
$unionoutput   =~ s/\(/\\\(/isg;
$unionoutput   =~ s/\)/\\\)/isg;
$unionoutput1  =~ s/\(/\\\(/isg;
$unionoutput1  =~ s/\)/\\\)/isg;
print FILE qq~if (\$union==0) { \$unionview="ÏÔÊ¾ÁªÃËÁĞ±í"; } else { \$unionview="¹Ø±ÕÁªÃËÁĞ±í"; }\n
\$output .= qq($unionoutput);\n
\$output .= qq($unionoutput1) if (\$union == 1);
~;
print FILE "1;\n";
close (FILE);

}
sub dochangedir {

    my $x = &myrand(1000000000);
    $x = crypt($x, aun);
    $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
    $x =~ s/[^\w\d]//g;
    $x = substr($x, 2, 9);
    $memdir    = "members$x"  if (rename("$lbdir$memdir",     "${lbdir}members$x"));
    $msgdir    = "messages$x" if (rename("$lbdir$msgdir",     "${lbdir}messages$x"));

    opendir (DIRS, "$lbdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^\w+?$/i, @files);
    my @ftpdir = grep(/^ftpdata/i, @files);
    $ftpdir = $ftpdir[0];
    my @memfavdir = grep(/^memfav/i, @files);
    $memfavdir = $memfavdir[0];
    my @saledir = grep(/^sale/i, @files);
    $saledir = $saledir[0];
    my @searchdir = grep(/^search/i, @files);
    $searchdir = $searchdir[0];
    my @recorddir = grep(/^record/i, @files);
    $recorddir = $recorddir[0];
    my $x = &myrand(1000000000);
    $x = crypt($x, aun);
    $x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
    $x =~ s/[^\w\d]//g;
    $x = substr($x, 2, 9);
    $searchdir = "search$x"   if (rename("$lbdir$searchdir",  "${lbdir}search$x"));
    $ftpdir    = "ftpdata$x"  if (rename("$lbdir$ftpdir",     "${lbdir}ftpdata$x"));
    $memfavdir = "memfav$x"   if (rename("$lbdir$memfavdir",  "${lbdir}memfav$x"));
    $recorddir = "record$x"   if (rename("$lbdir$recorddir",  "${lbdir}record$x"));
    $saledir   = "sale$x"     if (rename("$lbdir$saledir",    "${lbdir}sale$x"));

my $x = &myrand(1000000000);
$x = crypt($x, aun);
$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
$x =~ s/[^\w\d]//g;
$x = substr($x, 2, 9);
$usrdir    = "usr$x"      if (rename("$imagesdir$usrdir", "${imagesdir}usr$x"));

    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>ÖØÒªÄ¿Â¼Ãû³Æ±ä»»</b><p>
<font color=#333333>ËùÓĞÖØÒªÄ¿Â¼µÄÃû³Æ¶¼ÒÑ¾­±ä»¯Íê³É£¡</font>
</td></tr>
~;

}

sub dodellock {
    opendir (DIRS, "${lbdir}lock");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	chomp $_;
	unlink ("${lbdir}lock/$_");
    }
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>³õÊ¼»¯Ëø¶¨ÎÄ¼ş</b><p>
<font color=#333333>ËùÓĞËø¶¨ÎÄ¼şÒÑ¾­³õÊ¼»¯£¡</font>
</td></tr>
~;
}

sub doinit  {
    print qq~<tr><td bgcolor=#FFFFFF align=center colspan=2>
<font color=#990000><b>³õÊ¼»¯ÂÛÌ³Êı¾İ</b><p>
<font color=#333333>Ê×´ÎÔËĞĞÂÛÌ³±ØĞëÔËĞĞ£¬ÒÔºóÈç¹û¸üĞÂÁËÂÛÌ³±íÇéÍ¼Æ¬µÈ£¬Ò²ĞèÒªÔËĞĞ£¡<BR>Ã»ÓĞÌØ±ğËµÃ÷µÄ³õÊ¼»¯ÊÇ²»»á¶ªÊ§Êı¾İµÄ£¬Çë·ÅĞÄÊ¹ÓÃ£¡</font><BR><BR>
</td></tr>
<tr>
    <td bgcolor=#FFFFFF colspan=2>

    <font color=#333333>* <b><a href="$thisprog?action=upskinselect">³õÊ¼»¯³õÊ¼»¯ÂÛÌ³·ç¸ñÑ¡ÔñÁĞ±í</a></b>¡¡ <font color=red>(µÚÒ»´Î°²×°ºó±ØĞëÔËĞĞÒ»´Î)</font><br>
    ³õÊ¼»¯ÂÛÌ³·ç¸ñÑ¡ÔñÁĞ±íÆäÊµ²»»á×Ô¶¯¸üĞÂµÄ£¬³ı·ÇÄãÔÚÕâ¶ù¸üĞÂÒ»ÏÂ¡£Èç¹û¸üĞÂÂÛÌ³·ç¸ñ£¬Ò²ĞèÒªÔËĞĞ£¡<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>1£®<b><a href="$thisprog?action=uptop">³õÊ¼»¯ÓÃ»§ÅÅÃû</a></b>¡¡ <font color=red>(µÚÒ»´Î°²×°ºó±ØĞëÔËĞĞÒ»´Î)</font><br>
    ÓÃ»§ÅÅÃûÆäÊµ²»»á×Ô¶¯¸üĞÂµÄ£¬³ı·ÇÄãÔÚÕâ¶ù¸üĞÂÒ»ÏÂ¡£<BR><BR>
    </td>
    </tr>
    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>2£®<b><a href="$thisprog?action=dogetold">ÓÃ»§Êı¾İÕûÀí</a></b>¡¡ <font color=red>(µÚÒ»´Î°²×°ºó±ØĞëÔËĞĞÒ»´Î)</font><br>
    ¶ÔÓÃ»§Êı¾İ½øĞĞÕûÀí£¬±£Ö¤ÂÛÌ³¸ßËÙÔËĞĞ¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>3£®<b><a href="$thisprog?action=upemot">³õÊ¼»¯±íÇéÍ¼Æ¬ºÍ EMOT Í¼Æ¬</a></b>¡¡ <font color=red>(µÚÒ»´Î°²×°ºó±ØĞëÔËĞĞÒ»´Î)</font><br>
    ±íÇéÍ¼Æ¬ºÍ EMOT ÆäÊµ²»»á×Ô¶¯¸üĞÂµÄ£¬³ı·ÇÄãÔÚÕâ¶ù¸üĞÂÒ»ÏÂ¡£<BR><BR>
    </td>
    </tr>
    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>4£®<b><a href="$thisprog?action=upuser">³õÊ¼»¯ÓÃ»§Í·ÏñÍ¼Æ¬</a></b>¡¡ <font color=red>(µÚÒ»´Î°²×°ºó±ØĞëÔËĞĞÒ»´Î)</font><br>
    ÓÃ»§Í·ÏñÆäÊµ²»»á×Ô¶¯¸üĞÂµÄ£¬³ı·ÇÄãÔÚÕâ¶ù¸üĞÂÒ»ÏÂ¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>5£®<b><a href="$thisprog?action=upupload">³õÊ¼»¯ÎÄ¼şÉÏ´«Ä¿Â¼ÊôĞÔ£¡</a></b>¡¡ <font color=red>(µÚÒ»´Î°²×°ºó±ØĞëÔËĞĞÒ»´Î)</font><br>
    Èç¹ûÄúµÄÂÛÌ³ÎŞ·¨Õı³£Ö§³ÖÌû×ÓÄÚÌùÎÄ¼şÉÏ´«¡¢ÉÏ´«Í·ÏñÎÄ¼ş¡¢ÎÄ¼şÏÂÔØ¼ÆÊıÊ±£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ£¬´ó²¿·ÖÎÊÌâ¶¼¿ÉÒÔ½â¾ö(Èç¹ûÂÛÌ³µÄÎÄ¼şÉÏ´«Õı³£µÄ»°£¬ÔòÎŞĞëÔËĞĞ´Ë²½)¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>6£®<b><a href="$thisprog?action=uppost">³õÊ¼»¯ÂÛÌ³Ìû×ÓÄ¿Â¼ºÍÊı¾İÎÄ¼şÊôĞÔ</a></b>¡¡ <font color=red>(µÚÒ»´Î°²×°ºó±ØĞëÔËĞĞÒ»´Î)</font><br>
    Èç¹ûÄúµÄÂÛÌ³ÓĞĞ©Êı¾İÎŞ·¨¸üĞÂ¡¢Ìû×ÓÎŞ·¨·¢±í»ò»Ø¸´Ö®ÀàÊ±£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ£¬´ó²¿·ÖÎÊÌâ¶¼¿ÉÒÔ½â¾ö(Èç¹ûÂÛÌ³µÄÊı¾İÕı³£µÄ»°£¬ÔòÎŞĞëÔËĞĞ´Ë²½)¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>7£®<b><a href="$thisprog?action=upmessage">³õÊ¼»¯¶ÌÏûÏ¢Ä¿Â¼ºÍÎÄ¼şÊôĞÔ</a></b>¡¡ <font color=red>(µÚÒ»´Î°²×°ºó±ØĞëÔËĞĞÒ»´Î)</font><br>
    Èç¹ûÄúµÄÂÛÌ³¶ÌÏûÏ¢µÄÊÕ·¢ÓĞÎÊÌâÊ±£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ£¬´ó²¿·ÖÎÊÌâ¶¼¿ÉÒÔ½â¾ö(Èç¹ûÂÛÌ³µÄ¶ÌÏûÏ¢ÊÕ·¢Õı³£µÄ»°£¬ÔòÎŞĞëÔËĞĞ´Ë²½)¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>8£®<b><a href="$thisprog?action=dellock">³õÊ¼»¯Ëø¶¨ÎÄ¼ş</a></b><br>
    Èç¹ûÄãµÄËø¶¨ÎÄ¼şÄ¿Â¼ÖĞÓĞ¶àÓàµÄ»òÕßÉ¾³ı²»µôµÄËø¶¨ÎÄ¼şµÄ»°£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>9£®<b><a href="$thisprog?action=changedir">ÖØÒªÄ¿Â¼Ãû³Æ±ä»¯</a></b><br>
    ÖØÒªÄ¿Â¼µÄÃû³ÆÔÚ°²×°Ö®Ê±¾ÍÒÑ¾­±ä»¯±£ÃÜ£¬ÎªÁË¸ü¼Ó±£Ö¤°²È«£¬Äú¿ÉÒÔÔÚÕâÀïÖØĞÂ±ä»¯Ä¿Â¼Ãû³Æ¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>10£®<b><a href="$thisprog?action=uponlineuser" OnClick="return confirm('´Ë²Ù×÷ÊÇ²»¿É»Ö¸´µÄ£¬È·¶¨Ã´£¿');">³õÊ¼»¯ÔÚÏßÍ³¼Æ</a></b><br>
    Èç¹ûÄãµÄÔÚÏßÈËÊıÍ³¼ÆÊı¾İ³ö´íµÄ»°(±ÈÈç×ÜÊÇÖ»ÓĞÄãÒ»¸öÈËÔÚÏß)£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ(ËùÓĞµÄÓÃ»§½«È«²¿±»ÊÓÎª²»ÔÚÏß)¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>11£®<b><a href="$thisprog?action=upconter" OnClick="return confirm('´Ë²Ù×÷ÊÇ²»¿É»Ö¸´µÄ£¬È·¶¨Ã´£¿');">³õÊ¼»¯·ÃÎÊ´ÎÊı</a></b><br>
    Èç¹ûÄãµÄ·ÃÎÊ´ÎÊıÍ³¼ÆºÍ×î´óÔÚÏßÈËÊıµÈÊı¾İ³ö´íµÄ»°(±ÈÈç·ÃÎÊ´ÎÊı×ÜÊÇ1)£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ(·ÃÎÊ´ÎÊıÍ³¼ÆºÍ×î´óÔÚÏßÈËÊı¶¼½«Çå¿Õ)¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>12£®<b><a href="$thisprog?action=shareforums" OnClick="return confirm('´Ë²Ù×÷ÊÇ²»¿É»Ö¸´µÄ£¬È·¶¨Ã´£¿');">³õÊ¼»¯ÁªÃËÊı¾İ</a></b><br>
    Èç¹ûÄãµÄÁªÃËÊı¾İÉ¾³ı²»µô»òÊÇ³ö´íµÄ»°£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ¡£(ËùÓĞµÄÁªÃËÊı¾İ½«È«²¿¶ªÊ§)<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>13£®<b><a href="$thisprog?action=delxzb" OnClick="return confirm('´Ë²Ù×÷ÊÇ²»¿É»Ö¸´µÄ£¬È·¶¨Ã´£¿');">³õÊ¼»¯ËùÓĞÂÛÌ³µÄĞ¡×Ö±¨</a></b><br>
    Èç¹ûÄúÒªÇå³ıËùÓĞÂÛÌ³µÄĞ¡×Ö±¨Ê±£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ(ËùÓĞµÄĞ¡×Ö±¨½«È«²¿¶ªÊ§)¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>14£®<b><a href="$thisprog?action=delans" OnClick="return confirm('´Ë²Ù×÷ÊÇ²»¿É»Ö¸´µÄ£¬È·¶¨Ã´£¿');">³õÊ¼»¯ËùÓĞÂÛÌ³µÄ¹«¸æ</a></b><br>
    Èç¹ûÄúÒªÇå³ıËùÓĞÂÛÌ³µÄ¹«¸æÊ±£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ(ËùÓĞµÄ¹«¸æ½«È«²¿¶ªÊ§)¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>15£®<b><a href="$thisprog?action=delmessage" OnClick="return confirm('´Ë²Ù×÷ÊÇ²»¿É»Ö¸´µÄ£¬È·¶¨Ã´£¿');">Çå¿ÕËùÓĞ¶ÌÏûÏ¢</a></b><br>
    Èç¹ûÄúÒªÇå³ıËùÓĞµÄ¶ÌÏûÏ¢Ê±£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ(ËùÓĞµÄ¶ÌÏûÏ¢½«È«²¿¶ªÊ§)¡£<BR><BR>
    </td>
    </tr>

    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333>16£®<b><a href="$thisprog?action=delcache">Çå¿ÕËùÓĞ»º´æ</a></b><br>
    Èç¹ûÄúÒªÇå³ıËùÓĞµÄ»º´æÊ±£¬¿ÉÒÔÔÚÕâÀï³õÊ¼»¯Ò»ÏÂ(ÎªÁËÌá¸ßÏµÍ³Ğ§ÂÊ£¬×îºÃ10-20Ìì¶¨ÆÚÇå¿ÕÒ»´Î)¡£<BR><BR>
    </td>
    </tr>
         ~;
}     

print qq~</td></tr></table></body></html>~;
exit;
