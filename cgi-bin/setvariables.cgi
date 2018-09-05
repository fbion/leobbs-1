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
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setvariables.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;');

$query = new LBCGI;
#&ipbanned; #å°æ€ä¸€äº› ip

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);

        if (($_ eq 'adfoot')||($_ eq 'adscript')||($_ eq 'adscriptmain')||($_ eq 'adlinks')||($_ eq 'topicad')) {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}
	$theparam = &unHTML("$theparam");

	$theparam  = sprintf("%02d",$theparam) if (($_ eq 'createmon')||($_ eq 'createday'));
	if ($_ eq 'createyear') { $theparam = sprintf("%02d", $theparam); $theparam = 1900+$theparam if ($theparam<100); }

	${$_} = $theparam;
        if ($_ ne 'action') {
            $theparam =~ s/[\a\f\n\e\0\r]//isg;
            $printme .= "\$" . "$_ = \'$theparam\'\;\n" if ($_ ne "");
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
        
$maxweiwang = 5 if (($maxweiwang < 5)||($maxweiwang eq ""));

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {

    if ($action eq "process") {

        
        $endprint = "1\;\n";

        $filetomake = "$lbdir" . "data/boardinfo.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

$lbdirbak = $lbdir ;

eval{ require "data/boardinfo.cgi"; };
if ($@) {

    open(FILE,"${lbdirbak}data/boardinfobak.cgi");
    my @ddd = <FILE>;
    close(FILE);
    open(FILE,">${lbdirbak}data/boardinfo.cgi");
    foreach (@ddd) {
    	chomp $_;
        print FILE "$_\n";
    }
    close(FILE);

                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=å®‹ä½“ color=#FFFFFF>
                    <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / å˜é‡è®¾ç½®</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=å®‹ä½“ color=#333333><b>æ‰€æœ‰ä¿¡æ¯æ²¡æœ‰ä¿å­˜</b><br>ä½ è¾“å…¥çš„æ•°æ®ä¸­ï¼Œæœ‰éæ­£å¸¸çš„å†…å®¹ï¼Œå¯¼è‡´æ•°æ®å‡ºé”™ï¼Œè¯·æ’æŸ¥ï¼
                    </td></tr></table></td></tr></table>
                    ~;
		print qq~</td></tr></table></body></html>~;
		exit;
}

        $filetomake = "$lbdir" . "data/boardinfobak.cgi";
        open(FILE,">$filetomake");
        print FILE "$printme";
        print FILE $endprint;
        close(FILE);

    opendir (DIRS, "${lbdir}cache/id");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) {
    	$_ =~ s/\.cgi//isg;
    	unlink ("${lbdir}cache/id/$_\.cgi");
    }

        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=å®‹ä½“ color=#FFFFFF>
                <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / å˜é‡ç»“æ„</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle colspan=2>
                <font face=å®‹ä½“ color=#333333><center><b>ä»¥ä¸‹ä¿¡æ¯å·²ç»æˆåŠŸä¿å­˜</b><br><br>
                </center>~;
                $printme =~ s/\n/\<br>/g;
                $printme =~ s/\"//g;
                $printme =~ s/\$//g;
                $printme =~ s/\\\@/\@/g;
                $printme =~ s/\\\'/\'/g;
                print $printme;
                print qq~
                </td></tr></table></td></tr></table>
                ~;
                }
                else {
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=å®‹ä½“ color=#FFFFFF>
                    <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / å˜é‡è®¾ç½®</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                    <font face=å®‹ä½“ color=#333333><b>æ‰€æœ‰ä¿¡æ¯æ²¡æœ‰ä¿å­˜</b><br>æ–‡ä»¶æˆ–è€…ç›®å½•ä¸å¯å†™<br>è¯·æ£€æµ‹ä½ çš„ data ç›®å½•å’Œ boardinfo.cgi æ–‡ä»¶çš„å±æ€§ï¼
                    </td></tr></table></td></tr></table>
                    ~;
                    }
                
            }
            else {
                $inmembername =~ s/\_/ /g;
                
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=å®‹ä½“ color=#FFFFFF>
                <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / å˜é‡è®¾ç½®</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=å®‹ä½“ color=#990000><b>è®ºå›å˜é‡è®¾ç½®</b>
                </td></tr>
                
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <input type=hidden name="noads" value="$noads">
                <input type=hidden name="regerid" value="$regerid">
                ~;
                $tempoutput1 = "<select name=\"mainoff\">\n<option value=\"0\">è®ºå›å¼€æ”¾\n<option value=\"1\">è®ºå›å…³é—­\n<option value=\"2\">è‡ªåŠ¨å®šæœŸå¼€æ”¾\n</select>\n";
                $tempoutput1 =~ s/value=\"$mainoff\"/value=\"$mainoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333 ><b>è®ºå›çŠ¶æ€</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1</td>
                </tr>
                ~;
	$tempoutput1 = "<select name=\"mainauto\">\n<option value=\"day\">æ¯å¤©\n<option value=\"week\">æ¯æ˜ŸæœŸ\n<option value=\"month\">æ¯æœˆ\n</select>\n";
        $tempoutput1 =~ s/value=\"$mainauto\"/value=\"$mainauto\" selected/;
      	print qq~
              <tr>
              <td bgcolor=#FFFFFF width=40%>
              <font face=å®‹ä½“ color=#333333 ><b>è‡ªåŠ¨å¼€æ”¾è®ºå›äº</b><br>(åªæœ‰é€‰æ‹©è‡ªåŠ¨å®šæœŸå¼€æ”¾æ­¤é¡¹æœ‰æ•ˆ)</font></td>
              <td bgcolor=#FFFFFF>
              $tempoutput1 <input name=mainautovalue value="$mainautovalue" size=8><br>æ³¨: å¯ä»¥ä½¿ç”¨å•ä¸€æ•°å­—æˆ–æ˜¯èŒƒå›´ï¼Œå¦‚æ¯å¤©6, æ¯å¤©0-6, æ¯æ˜ŸæœŸ6, æ¯æœˆ10-15</td>
              </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333 ><b>ç»´æŠ¤è¯´æ˜</b> (æ”¯æŒ HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="line1" cols="40">$line1</textarea><BR><BR></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"regonoff\">\n<option value=\"0\">å…è®¸ç”¨æˆ·æ³¨å†Œ\n<option value=\"1\">ä¸å…è®¸ç”¨æˆ·æ³¨å†Œ\n<option value=\"2\">è‡ªåŠ¨å®šæœŸå¼€æ”¾\n</select>\n";
                $tempoutput1 =~ s/value=\"$regonoff\"/value=\"$regonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333 ><b>æ˜¯å¦å…è®¸ç”¨æˆ·æ³¨å†Œ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                ~;
		$tempoutput1 = "<select name=\"regauto\">\n<option value=\"day\">æ¯å¤©\n<option value=\"week\">æ¯æ˜ŸæœŸ\n<option value=\"month\">æ¯æœˆ\n</select>\n";
		$tempoutput1 =~ s/value=\"$regauto\"/value=\"$regauto\" selected/;
		print qq~
               <tr>
               <td bgcolor=#FFFFFF width=40%>
               <font face=å®‹ä½“ color=#333333 ><b>è‡ªåŠ¨å¼€æ”¾æ³¨å†Œäº</b><br>(åªæœ‰ä¸Šé¢é€‰æ‹©è‡ªåŠ¨å®šæœŸå¼€æ”¾æ­¤é¡¹æ‰æœ‰æ•ˆ)</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput1 <input name=regautovalue value="$regautovalue" size=8><br>æ³¨: å¯ä»¥ä½¿ç”¨å•ä¸€æ•°å­—æˆ–æ˜¯èŒƒå›´ï¼Œå¦‚æ¯å¤©6, æ¯å¤©0-6, æ¯æ˜ŸæœŸ6, æ¯æœˆ10-15</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333 ><b>ä¸å…è®¸æ³¨å†Œè¯´æ˜</b> (æ”¯æŒ HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="noregwhynot" cols="40">$noregwhynot</textarea><BR><BR></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"regdisptime\">\n<option value=\"15\">15\n<option value=\"1\">1\n<option value=\"3\">3\n<option value=\"5\">5\n<option value=\"8\">8\n<option value=\"10\">10\n<option value=\"12\">12\n<option value=\"17\">17\n<option value=\"20\">20\n<option value=\"25\">25\n<option value=\"30\">30\n<option value=\"40\">40\n<option value=\"45\">45\n<option value=\"50\">50\n<option value=\"60\">60\n<option value=\"90\">90\n<option value=\"120\">120\n<option value=\"150\">150\n<option value=\"200\">200\n</select> ç§’\n";
                $tempoutput1 =~ s/value=\"$regdisptime\"/value=\"$regdisptime\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333 ><b>æ³¨å†Œå£°æ˜æ—¶é—´æ˜¾ç¤ºå¤šå°‘ç§’åæ‰èƒ½ç¡®å®š</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                ~;

                $tempoutput1 = "<select name=\"regpuonoff\">\n<option value=\"ontop\">é¦–é¡µå¼¹å‡º\n<option value=\"oneach\">æ¯é¡µå¼¹å‡º\n<option value=\"off\">ä¸å¼¹å‡º\n</select>\n";
                $tempoutput1 =~ s/value=\"$regpuonoff\"/value=\"$regpuonoff\" selected/;
                if(!$popupmsg){$popupmsg=qq~è¯·å…ˆæ³¨å†Œä»¥é¿å…æ­¤è§†çª—å‡ºç°~;}
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333 ><b>æ˜¯å¦å¼¹å‡ºæé†’æ³¨å†Œè§†çª—</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput1<BR><BR></td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333 ><b>æé†’è®¿å®¢æ³¨å†Œè§†çª—å†…å®¹</b> (æ”¯æ´ HTML,ä¸éœ€è¦æ³¨å†Œç”»é¢çš„è¿ç»“)<BR><BR></font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="popupmsg" cols="40">$popupmsg</textarea><BR><BR></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›åç§°</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardname" value="$boardname"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›æè¿°</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boarddescription" value="$boarddescription"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå› LOGO</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardlogos" value="$boardlogos"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå› URL åœ°å€</b><br>ç»“å°¾ä¸è¦åŠ  "/"ï¼Œæ›´ä¸è¦åŠ  leobbs.cgi ä¹‹ç±»çš„å“¦</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="boardurl" value="$boardurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>ä¸»é¡µåç§°</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homename" value="$homename"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>ç‰ˆæƒä¿¡æ¯</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›å¤‡æ¡ˆä¿¡æ¯ï¼Œåªéœ€å¡«å…¥ç¼–å·å°±å¯ä»¥ï¼Œ<BR>ä¸è¦å¡«å…¶ä»–å¤šä½™çš„å†…å®¹ï¼Œå¦‚æœæ²¡æœ‰è¯·ç•™ç©ºï¼</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=18 name="beian" value="$beian" maxlength=18> æ¯”å¦‚ï¼šæ²ªICPå¤‡05023323å·</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›çŠ¶æ€æ æ˜¾ç¤º</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="statusbar" value="$statusbar"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>ä¸»é¡µåœ°å€</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>å›¾ç‰‡ç›®å½• URL</b><br>åœ¨ç»“å°¾ä¸è¦åŠ  "/images"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="imagesurl" value="$imagesurl"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>å›¾ç‰‡ç»å¯¹è·¯å¾„</b><br>ç»“å°¾åŠ  "/"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="imagesdir" value="$imagesdir"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>ç¨‹åºç»å¯¹è·¯å¾„</b><br>ç»“å°¾åŠ  "/"</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="lbdir" value="$lbdir"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emoticons\">\n<option value=\"off\">ä¸ä½¿ç”¨\n<option value=\"on\">ä½¿ç”¨\n</select>\n";
                $tempoutput =~ s/value=\"$emoticons\"/value=\"$emoticons\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ä½¿ç”¨è¡¨æƒ…å­—ç¬¦è½¬æ¢ï¼Ÿ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"canchgfont\">\n<option value=\"yes\">ä½¿ç”¨\n<option value=\"no\">ä¸ä½¿ç”¨\n</select>\n";
                $tempoutput =~ s/value=\"$canchgfont\"/value=\"$canchgfont\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ä½¿ç”¨æ–‡å­—å­—ä½“è½¬æ¢ï¼Ÿ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"avatars\">\n<option value=\"off\">ä¸ä½¿ç”¨\n<option value=\"on\">ä½¿ç”¨\n</select>\n";
                $tempoutput =~ s/value=\"$avatars\"/value=\"$avatars\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ä½¿ç”¨ä¸ªæ€§å›¾ç‰‡</b><br>ä½¿ç”¨ä¸ªæ€§åŒ–å›¾ç‰‡ï¼Œæ¯ä¸ªç”¨æˆ·å°†æ‹¥æœ‰æœ‰è‡ªå·±ç‰¹è‰²çš„å¤´åƒã€‚</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›å…³é”®å­—</b><br>è¾“å…¥å’Œä½ è®ºå›ç›¸å…³çš„å…³é”®å­—ï¼Œæ¯ä¸ªå…³é”®å­—ä¹‹é—´ç”¨è‹±æ–‡çš„é€—å·éš”å¼€ ï¼</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newkeywords" value="$newkeywords" size=40 maxlength=100></td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=å®‹ä½“ color=#990000><b>çŸ­æ¶ˆæ¯åŠŸèƒ½</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"allowusemsg\">\n<option value=\"on\">ä½¿ç”¨\n<option value=\"off\">ä¸ä½¿ç”¨\n</select>";
                $tempoutput =~ s/value=\"$allowusemsg\"/value=\"$allowusemsg\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦å¼€å¯è®ºå›çŸ­æ¶ˆæ¯åŠŸèƒ½ï¼Ÿ</b><br>å¼€å¯çŸ­æ¶ˆæ¯åŠŸèƒ½ï¼Œå¯ä½¿æ‚¨åŠæ‚¨çš„ä¼šå‘˜ä¾¿äºäº’ç›¸æ²Ÿé€šã€‚</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>ä¸€æ¬¡ç¾¤å‘è®¯æ¯æœ€é«˜æ•°é‡</font></b><br>å¦‚ä¸é™åˆ¶ï¼Œè¯·ç•™ç©º</td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxsend" value="$maxsend" maxlength=3> æ­¤åŠŸèƒ½å¯¹ç‰ˆä¸»å’Œå›ä¸»æ— æ•ˆ</td>
                </tr>                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>çŸ­æ¶ˆæ¯æ”¶ä»¶ç®±æ¶ˆæ¯æ¡æ•°é™åˆ¶</font></b><br>å¦‚ä¸é™åˆ¶ï¼Œè¯·ç•™ç©º</td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxmsgno" value="$maxmsgno" maxlength=3> æ­¤åŠŸèƒ½å¯¹ç‰ˆä¸»å’Œå›ä¸»æ— æ•ˆ</td>
                </tr>                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ¯é¡µæ˜¾ç¤ºå¤šå°‘çŸ­æ¶ˆæ¯</font></b></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="maxthread" value="$maxthread" maxlength=3> é»˜è®¤: 9 </td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è‡ªåŠ¨åˆ·æ–°çŸ­æ¶ˆæ¯çª—å£æ—¶é—´</font></b></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="infofreshtime" value="$infofreshtime" maxlength=3> ç§’(ç•™ç©ºä¸ºä¸éœ€è¦)</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"allowmsgattachment\">\n<option value=\"yes\">ä½¿ç”¨\n<option value=\"no\">ä¸ä½¿ç”¨\n</select>";
                $tempoutput =~ s/value=\"$allowmsgattachment\"/value=\"$allowmsgattachment\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦å¼€å¯è®ºå›çŸ­æ¶ˆæ¯é™„ä»¶åŠŸèƒ½ï¼Ÿ</b><br>é™„ä»¶æœ€å¤§ 60KBï¼Œä¸å¯è®¾ã€‚</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=å®‹ä½“ color=#990000><b>é‚®ä»¶åŠŸèƒ½</b>
                </font></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emailfunctions\">\n<option value=\"off\">ä¸ä½¿ç”¨\n<option value=\"on\">ä½¿ç”¨\n</select>\n";
                $tempoutput =~ s/value=\"$emailfunctions\"/value=\"$emailfunctions\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ä½¿ç”¨é‚®ä»¶åŠŸèƒ½ï¼Ÿ</b><br>æ¨èä½ ä½¿ç”¨</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
		$sendmailprog = mailprogram();

                $tempoutput = "<select name=\"emailtype\">\n<option value=\"smtp_mail\">SMTP\n<option value=\"esmtp_mail\">ESMTP\n<option value=\"directmail\">94cool ç‰¹å¿«ä¸“é€’\n<option value=\"send_mail\">Sendmail\n<option value=\"blat_mail\">Blat\n</select>\n";
                $tempoutput =~ s/value=\"$emailtype\"/value=\"$emailtype\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è¯·é€‰æ‹©ä¸€ä¸ªå¯ä»¥ä½¿ç”¨çš„é‚®ä»¶åè®®</b><br>æ¨èä½¿ç”¨ SMTPï¼Œå¯ä»¥åŒæ—¶åœ¨ NT å’Œ UNIX ä¸‹ä½¿ç”¨ã€‚è€Œ SENDMAIL åªèƒ½åœ¨ UNIX ä¸­ç”¨ï¼ŒBlat åªèƒ½åœ¨ NT ä¸­ç”¨ã€‚ä½ ä¹Ÿå¯ä»¥ç”¨ 94cool ç‰¹å¿«ä¸“é€’ï¼Œä»–å¯ä»¥ç›´æ¥æŠŠä¿¡ä»¶æäº¤åˆ°å¯¹æ–¹ä¿¡ç®±ï¼Œç±»ä¼¼ Foxmail çš„ç‰¹å¿«ä¸“é€’ï¼Œé€Ÿåº¦ç›¸å½“å¿«(æ³¨æ„çš„æ˜¯ï¼Œå¦‚æœä½ ä¸»æœºæœ‰é™åˆ¶ï¼Œå¯èƒ½ä¼šæ— æ³•ä½¿ç”¨è¯¥åŠŸèƒ½ï¼Œè¯·æµ‹è¯•åå†ç¡®å®š)ã€‚</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>å‘é€é‚®ä»¶ç¨‹åºä½ç½®</b><br>å¦‚æœæ‚¨ä½¿ç”¨çš„ä¸æ˜¯ Sendmailï¼Œè¯·ä¸è¦å¡«å†™</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=30 name="SEND_MAIL" value="$SEND_MAIL"> æµ‹è¯•ç»“æœï¼š$sendmailprog</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>SMTP çš„ä½ç½®</b><br>å¦‚æœæ‚¨ä½¿ç”¨çš„ä¸æ˜¯ SMTPï¼Œè¯·ä¸è¦å¡«å†™ï¼Œä¸€èˆ¬å¡«å†™ä½  ISP æä¾›çš„å‘ä¿¡æœåŠ¡å™¨åœ°å€</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTP_SERVER" value="$SMTP_SERVER"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>SMTP çš„ç«¯å£</b><br>å¦‚æœæ‚¨ä½¿ç”¨çš„ä¸æ˜¯ SMTPï¼Œè¯·ä¸è¦å¡«å†™ï¼Œé»˜è®¤ä¸º 25</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="SMTP_PORT" value="$SMTP_PORT" maxlength=6></td>
                </tr>
				
				<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>ESMTP çš„ç”¨æˆ·å</b><br>å¦‚æœæ‚¨ä½¿ç”¨çš„ä¸æ˜¯ ESMTPï¼Œè¯·ä¸è¦å¡«å†™</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTPUSER" value="$SMTPUSER"></td>
                </tr>

                <tr>
				<td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>ESMTP çš„å¯†ç </b><br>å¦‚æœæ‚¨ä½¿ç”¨çš„ä¸æ˜¯ ESMTPï¼Œè¯·ä¸è¦å¡«å†™</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="SMTPPASS" value="$SMTPPASS"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>å›ä¸»æ¥æ”¶é‚®ä»¶ä½¿ç”¨çš„ä¿¡ç®±</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adminemail_in" value="$adminemail_in"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>å›ä¸»å‘é€é‚®ä»¶ä½¿ç”¨çš„ä¿¡ç®±</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adminemail_out" value="$adminemail_out"></td>
                </tr>
                ~;
                $tempoutput = "<select name=\"passwordverification\">\n<option value=\"no\">å¦\n<option value=\"yes\">æ˜¯\n</select>\n";
                $tempoutput =~ s/value=\"$passwordverification\"/value=\"$passwordverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ç”¨é‚®ä»¶é€šçŸ¥ç”¨æˆ·å¯†ç ï¼Ÿ</b><br>å»ºè®®ä¸ä½¿ç”¨ã€‚è‹¥è¦ä½¿ç”¨ï¼Œè¯·ç¡®å®šæ‰“å¼€äº†ä¸Šé¢çš„â€œæ˜¯å¦ä½¿ç”¨é‚®ä»¶åŠŸèƒ½ï¼Ÿâ€ï¼Œå¹¶ä¿è¯ä½ å‘é€é‚®ä»¶æ˜¯æ²¡æœ‰é—®é¢˜çš„ã€‚</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"adminverification\">\n<option value=\"no\">å¦\n<option value=\"yes\">æ˜¯\n</select>\n";
                $tempoutput =~ s/value=\"$adminverification\"/value=\"$adminverification\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æ–°ç”¨æˆ·æ³¨å†Œï¼Œæ˜¯å¦å¿…é¡»ç®¡ç†å‘˜è®¤è¯ï¼Ÿ</b><br>å»ºè®®ä¸ä½¿ç”¨ã€‚è‹¥è¦ä½¿ç”¨ï¼Œ1,è¯·ç¡®å®šæ‰“å¼€äº†ä¸Šé¢çš„â€œæ˜¯å¦ä½¿ç”¨é‚®ä»¶åŠŸèƒ½ï¼Ÿâ€ï¼Œå¹¶ä¿è¯ä½ å‘é€é‚®ä»¶æ˜¯æ²¡æœ‰é—®é¢˜çš„ã€‚2,ç¡®è®¤å·²ç»æ‰“å¼€ä¸Šé¢çš„é‚®ä»¶é€šçŸ¥ç”¨æˆ·å¯†ç !</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"newusernotify\">\n<option value=\"no\">å¦\n<option value=\"yes\">æ˜¯\n</select>\n";
                $tempoutput =~ s/value=\"$newusernotify\"/value=\"$newusernotify\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>æœ‰æ–°ç”¨æˆ·æ³¨å†Œæ˜¯å¦ç”¨é‚®ä»¶é€šçŸ¥æ‚¨ï¼Ÿ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"oneaccountperemail\">\n<option value=\"no\">å¦\n<option value=\"yes\">æ˜¯\n</select>\n";
                $tempoutput =~ s/value=\"$oneaccountperemail\"/value=\"$oneaccountperemail\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>ä¸€ä¸ª Email åªèƒ½æ³¨å†Œä¸€ä¸ªè´¦å·ï¼Ÿ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=å®‹ä½“ color=#990000><b>å¹¿å‘Šé€‰é¡¹</b>
                </font></td>
                </tr>
		~;
	$adscript   =~ s/\[br\]/\n/isg;
	$adscriptmain   =~ s/\[br\]/\n/isg;
	$adfoot   =~ s/\[br\]/\n/isg;

               $tempoutput = "<select name=\"useadscript\">\n<option value=\"0\">ä¸ä½¿ç”¨\n<option value=\"1\">ä½¿ç”¨\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadscript\"/value=\"$useadscript\" selected/; 
               print qq~ 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›é¦–é¡µç‹¬ç«‹å¹¿å‘Šä¹¦å†™(å¦‚æœæ²¡æœ‰ï¼Œè¯·ç•™ç©º)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adscriptmain" rows="5" cols="40">$adscriptmain</textarea>
                </td>
                </tr>

               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ä½¿ç”¨è®ºå›é¦–é¡µå¹¿å‘Š</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›é¦–é¡µå¹¿å‘Šä¹¦å†™</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adscript" rows="5" cols="40">$adscript</textarea>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useadfoot\">\n<option value=\"0\">ä¸ä½¿ç”¨\n<option value=\"1\">ä½¿ç”¨\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadfoot\"/value=\"$useadfoot\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ä½¿ç”¨è®ºå›é¦–é¡µå°¾éƒ¨ä»£ç </b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›é¦–é¡µå°¾éƒ¨ä»£ç ä¹¦å†™</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useimagead\">\n<option value=\"0\">ä¸ä½¿ç”¨\n<option value=\"1\">ä½¿ç”¨\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimagead\"/value=\"$useimagead\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ä½¿ç”¨è®ºå›é¦–é¡µæµ®åŠ¨å¹¿å‘Š</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›é¦–é¡µæµ®åŠ¨å¹¿å‘Šå›¾ç‰‡(Flash) URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›é¦–é¡µæµ®åŠ¨å¹¿å‘Šè¿æ¥ç›®æ ‡ç½‘å€</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›é¦–é¡µæµ®åŠ¨å¹¿å‘Šå›¾ç‰‡å®½åº¦</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;åƒç´ </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=å®‹ä½“ color=#333333><b>è®ºå›é¦–é¡µæµ®åŠ¨å¹¿å‘Šå›¾ç‰‡é«˜åº¦</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;åƒç´ </td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum\">\n<option value=\"0\">ä¸ä½¿ç”¨\n<option value=\"1\">ä½¿ç”¨\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum\"/value=\"$useimageadforum\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%>      <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ç€¹       <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³Ê×Ò³ÓÒÏÂ¹Ì¶¨¹ã¸æÍ¼Æ¬¸ß¶È</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;ÏñËØ</td>
                </tr>
                ~;
                
               $tempoutput = "<select name=\"useimageadforum1\">\n<option value=\"0\">²»Ê¹ÓÃ\n<option value=\"1\">Ê¹ÓÃ\n</select>\n"; 
               $tempoutput =~ s/value=\"$useimageadforum1\"/value=\"$useimageadforum1\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF width=40%> 
               <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³ÊÇ·ñÊ¹ÓÃ´ËÓÒÏÂ¹Ì¶¨¹ã¸æ</b><BR>Èç¹û·ÖÂÛÌ³ÓĞ×Ô¶¨ÒåµÄÓÒÏÂ¹Ì¶¨¹ã¸æ£¬<BR>ÄÇÃ´´ËÑ¡ÏîÎŞĞ§</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=ËÎÌå color=#990000><b>ÆäËûÑ¡Ïî</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Ö§³ÖÉÏ´«µÄ¸½¼şÀàĞÍ</b><br>ÓÃ,·Ö¸î</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="addtype" value="$addtype"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>×î´óÃ¿´ÎÉÏ´«¼¸¸ö¸½¼ş</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=2 name="maxaddnum" value="$maxaddnum"> ½¨Òé²»Òª³¬¹ı10¡£</td>
                </tr>
                
                ~;
                $tempoutput = "<select name=\"COOKIE_USED\">\n<option value=\"0\">ÍêÕûÂ·¾¶Ä£Ê½\n<option value=\"1\">¸ùÄ¿Â¼Ä£Ê½\n<option value=\"2\">¹Ì¶¨Ä£Ê½\n</select>\n";
                #<option value=\"0\">×Ô¶¯Õì²âÄ¿Â¼Ä£Ê½\n
                $tempoutput =~ s/value=\"$COOKIE_USED\"/value=\"$COOKIE_USED\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÇëÑ¡Ôñ Cookie Ê¹ÓÃ·½Ê½£¡</B><br>Ä¬ÈÏÊ¹ÓÃÍêÕûÂ·¾¶Ä£Ê½£¬Èç¹ûÄã·¢ÏÖÂÛÌ³<BR>ÓÃ»§µÇÂ¼ºó»¹ÊÇ¿ÍÈËµÄ»°£¬ÇëÊ¹ÓÃ<BR>¸ùÄ¿Â¼Ä£Ê½»ò¹Ì¶¨Ä£Ê½(¹Ì¶¨Ä£Ê½±ØĞëÅäºÏÏÂÃæÒ»¸ö²ÎÊıÊ¹ÓÃ)¡£</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Cookie ¹Ì¶¨Ä£Ê½ÄÚÈİ</b><br>ÊäÈë¹Ì¶¨µÄÓòÃûºÍÂ·¾¶£¬Ö»ÓĞµ±ÉÏÃæÑ¡ÏîÉèÖÃÎª¹Ì¶¨Ä£Ê½²ÅÓĞĞ§</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="mycookiepath" value="$mycookiepath"> <BR>(ÓòÃûÇ°²»Òª¼Ó http://£¬×îºó²»Òª¼Ó / ºÅ£¬ÀıÈç£ºwww.abc.com )</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"EXP_MODE\">\n<option value=\"\">±ê×¼Ä£Ê½\n<option value=\"0\">ÔöÇ¿Ä£Ê½\n</select>\n";
                $tempoutput =~ s/value=\"$EXP_MODE\"/value=\"$EXP_MODE\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÇëÑ¡ÔñÒ³Ãæ¸üĞÂ·½Ê½£¡</B><br>Ä¬ÈÏÊ¹ÓÃ±ê×¼Ä£Ê½£¬Èç¹ûÄã·¢ÏÖÂÛÌ³Ë½ÃÜÇø½øÈëÊ±£¬<BR>ÊäÈëÕıÈ·ÃÜÂëºó»¹±ØĞëË¢ĞÂµÄ»°£¬ÇëĞŞ¸ÄÎªÔöÇ¿Ä£Ê½¡£<BR>µ«Èç¹ûÉèÖÃÎªÔöÇ¿Ä£Ê½ºó·¢ÏÖÒ»Ğ©Ææ¹ÖµÄÏÖÏó£¬Çë¸Ä»Ø£¡</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"CACHE_MODES\">\n<option value=\"\">¿ª·ÅÄ£Ê½\n<option value=\"no\">¾Ü¾øÄ£Ê½\n</select>\n";
                $tempoutput =~ s/value=\"$CACHE_MODES\"/value=\"$CACHE_MODES\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÇëÑ¡ÔñÒ³ÃæÊÇ·ñ±£³Ö»º´æ£¡</B><br>Ä¬ÈÏÊ¹ÓÃ¿ª·ÅÄ£Ê½£¬Èç¹û·¢ÏÖÂÛÌ³³öÏÖÆæ¹ÖµÄ»ìÂÒÏÖÏó£¬<BR>±ØĞëÊÖ¹¤Ë¢ĞÂ²ÅÄÜ½â¾öµÄ»°£¬ÇëĞŞ¸ÄÎª¾Ü¾øÄ£Ê½¡£<BR>µ«Èç¹ûÉèÖÃÎª¾Ü¾øÄ£Ê½ºó·¢ÏÖÒ»Ğ©Ææ¹ÖµÄÏÖÏó£¬Çë¸Ä»Ø£¡</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

    unless (WebGzip::getStatus()) {
	$gzipfunc = qq~Gzip Ä£¿é¿ÉÒÔÊ¹ÓÃ~;
    }
    else {
    	$e = WebGzip::getStatus();
    	$gzipfunc = qq~<BR><font color=#FF0000>Gzip Ä£¿é²»¿ÉÓÃ£¡</font> $e~ 
    }

                $tempoutput = "<select name=\"usegzip\">\n<option value=\"no\">¹Ø±Õ\n<option value=\"yes\">´ò¿ª\n</select>\n ²âÊÔ½á¹û£º$gzipfunc";
                $tempoutput =~ s/value=\"$usegzip\"/value=\"$usegzip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÇëÑ¡ÔñÊÇ·ñ²ÉÓÃGzipÑ¹Ëõ£¡</B><br>Ä¬ÈÏ¿ª·Å£¬Gzip ¿ÉÒÔÓĞĞ§µÄÑ¹Ëõ´«ÊäµÄÒ³Ãæ£¬ÈÃÒ³Ãæ´«ÊäµÄ¸ü¿ì£¬µ«Ò²»á¶àÏûºÄ²¿·Ö×ÊÔ´£¡Èç¹ûÄã¶Ô×ÊÔ´ÒªÇóºÜÑÏ£¬ÄÇÃ´ÇëÑ¡Ôñ¹Ø±Õ£¡</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"complevel\">\n<option value=\"9\">9\n<option value=\"8\">8\n<option value=\"7\">7\n<option value=\"6\">6\n<option value=\"5\">5\n<option value=\"4\">4\n<option value=\"3\">3\n<option value=\"2\">2\n<option value=\"1\">1\n</select>\n";
                $tempoutput =~ s/value=\"$complevel\"/value=\"$complevel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÇëÑ¡ÔñGzipÑ¹Ëõ¼¶±ğ£¡</B><br>9 ±íÊ¾Ñ¹ËõÂÊ×î¸ß£¬1±íÊ¾Ñ¹ËõÂÊ×îµÍ£¬ÅäºÏÉÏÃæÑ¡ÏîÊ¹ÓÃ£¡</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"OS_USED\">\n<option value=\"Nt\">Windows ÏµÁĞ\n<option value=\"Unix\">Unix ÏµÁĞ\n<option value=\"No\">²»¼ÓËø\n</select>\n";
                $tempoutput =~ s/value=\"$OS_USED\"/value=\"$OS_USED\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÇëÑ¡Ôñ²Ù×÷ÏµÍ³Æ½Ì¨ÓÃÓÚÎÄ¼ş¼ÓËø</b><BR>ÇëÇ§Íò²»ÒªÑ¡´í£¬Èç¹ûÄã²»ÄÜÈ·¶¨£¬ÇëÑ¡Ôñ Windows ÏµÁĞ£¡£¡<BR>ÎÄ¼ş¼ÓËø¿ÉÒÔÓĞĞ§µÄ·ÀÖ¹Ìù×ÓÊı¾İ¶ªÊ§µÈÎÊÌâ£¬µ«»áÓ°ÏìËÙ¶È£¬Çë×Ô¼ººâÁ¿£¡<br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"canotherlink\">\n<option value=\"no\">²»ÔÊĞíÍâ²¿Á¬½Ó\n<option value=\"yes\">ÔÊĞíÍâ²¿Á¬½Ó\n</select>\n";
                $tempoutput =~ s/value=\"$canotherlink\"/value=\"$canotherlink\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñ½ûÖ¹Íâ²¿Á¬½Ó³ÌĞò¶ÔÂÛÌ³²Ù×÷</b><BR>´ò¿ªµÄ»°£¬¿ÉÓĞĞ§·ÀÖ¹Íâ²¿Á¬½ÓµÄ³ÌĞò¹àË®ºäÕ¨»úµÄÉ§ÈÅ£¬µ«ÓĞ¿ÉÄÜ»áºÍ·À»ğÇ½³åÍ»<br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;
                $tempoutput = "<select name=\"useverify\">\n<option value=\"no\">²»ÔÊĞíÊ¹ÓÃ\n<option value=\"yes\">ÔÊĞíÊ¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$useverify\"/value=\"$useverify\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃÑéÖ¤ÂëĞ£Ñé</b><br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                ~;

eval ('use GD;');
if ($@) {
    $gdfunc = 0;
}
else {
    $gdfunc = 1;
}
if ($gdfunc eq "1") {
                $tempoutput = "<select name=\"verifyusegd\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$verifyusegd\"/value=\"$verifyusegd\" selected/;
                print qq~


                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃ GD À´ÏÔÊ¾ÑéÖ¤Âë</b><br></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
} else {
	print qq~<input type=hidden name="verifyusegd" value="no">~;
}

                $tempoutput = "<select name=\"floodcontrol\">\n<option value=\"off\">·ñ\n<option value=\"on\">ÊÇ\n</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñ¹àË®Ô¤·À»úÖÆ£¿</b><br>Ç¿ÁÒÍÆ¼öÊ¹ÓÃ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÓÃ»§·¢ÌùµÄÏà¸ôÊ±¼ä</b><br>¹àË®Ô¤·À»úÖÆ²»»áÓ°Ïìµ½Ì³Ö÷»ò°æÖ÷</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=5 name="floodcontrollimit" value="$floodcontrollimit" maxlength=4> Ãë (Ò»°ãÉèÖÃ 30 ×óÓÒ)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Í¬ IP µÄ×¢²á×îĞ¡Ïà¸ôÊ±¼ä</b><br>¿ÉÒÔÓĞĞ§·ÀÖ¹¹àË®×¢²á»ú</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=5 name="regcontrollimit" value="$regcontrollimit" maxlength=4> Ãë (Ò»°ãÉèÖÃ 30 ×óÓÒ)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÏÔÊ¾±à¼­¼ÆÊıµÄ×îĞ¡Ê±¼ä</b><br>ÔÚ¸ÃÊ±¼äÄÚ¶ÔÌù×ÓµÄ±à¼­²»¼ÆÊı</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="noaddedittime" value="$noaddedittime" maxlength=5> Ãë (Ä¬ÈÏ 60 Ãë)</td>
                </tr>
                
               <tr>
               <td bgcolor=#FFFFFF width=40%>
               <font face=ËÎÌå color=#333333><b>³¬¹ı¶àÉÙĞ¡Ê±µÄÌù×Ó²»ÔÊĞíÔÙ±à¼­</b><br>°æÖ÷ÒÔÉÏ¼¶±ğ²»ÏŞÖÆ</font></td>
               <td bgcolor=#FFFFFF>
               <input type=text size=3 name="noedittime" value="$noedittime" maxlength=2> Ğ¡Ê± (Áô¿Õ²»ÏŞÖÆ)</td>
               </tr>
               
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>É¾ÌùÂÊÔÚ¶àÉÙÒÔÉÏµÄ»áÔ±²»ÔÊĞí·¢±íĞÂÖ÷Ìâ</b><br>´ËÉè¶¨²»»áÓ°Ïìµ½Ì³Ö÷»ò°æÖ÷</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="deletepercent" value="$deletepercent" maxlength=3> % (Ò»°ãÉèÖÃ 20% ×óÓÒ£¬Èô²»ÏëÏŞÖÆ£¬ÔòÉèÖÃ 0 »ò¿Õ°×)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÔÊĞíµÄ×î´óÔÚÏßÈËÊı</b><br>¿ÉÒÔ¿ØÖÆ·şÎñÆ÷µÄ×ÊÔ´Ê¹ÓÃ</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=6 name="arrowonlinemax" value="$arrowonlinemax" maxlength=5> ÈË (Ò»°ãÉè 500 ×óÓÒ£¬Èô²»ÏëÏŞÖÆ£¬ÔòÉèÖÃ 99999)</td>
                </tr>
                ~;
                
                $tempoutput = "<select name=\"timezone\"><option value=\"-23\">- 23<option value=\"-22\">- 22<option value=\"-21\">- 21<option value=\"-20\">- 20<option value=\"-19\">- 19<option value=\"-18\">- 18<option value=\"-17\">- 17<option value=\"-16\">- 16<option value=\"-15\">- 15<option value=\"-14\">- 14<option value=\"-13\">- 13<option value=\"-12\">- 12<option value=\"-11\">- 11<option value=\"-10\">- 10<option value=\"-9\">- 9<option value=\"-8\">- 8<option value=\"-7\">- 7<option value=\"-6\">- 6<option value=\"-5\">- 5<option value=\"-4\">- 4<option value=\"-3\">- 3<option value=\"-2\">- 2<option value=\"-1\">- 1<option value=\"0\">0<option value=\"1\">+ 1<option value=\"2\">+ 2<option value=\"3\">+ 3<option value=\"4\">+ 4<option value=\"5\">+ 5<option value=\"6\">+ 6<option value=\"7\">+ 7<option value=\"8\">+ 8<option value=\"9\">+ 9<option value=\"10\">+ 10<option value=\"11\">+ 11<option value=\"12\">+ 12<option value=\"13\">+ 13<option value=\"14\">+ 14<option value=\"15\">+ 15<option value=\"16\">+ 16<option value=\"17\">+ 17<option value=\"18\">+ 18<option value=\"19\">+ 19<option value=\"20\">+ 20<option value=\"21\">+ 21<option value=\"22\">+ 22<option value=\"23\">+ 23</select>";
                $tempoutput =~ s/value=\"$timezone\"/value=\"$timezone\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>·şÎñÆ÷Ê±²î</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ËùÔÚµÄÊ±Çø</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="basetimes" value="$basetimes"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÓÃ»§ÍşÍû×î´ó¶àÉÙ£¿</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 name="maxweiwang" value="$maxweiwang" maxlength=3> Ä¬ÈÏ: 10(²»ÄÜĞ¡ÓÚ5)</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÔÚ¶àÉÙÇø·¢ËÍÏàÍ¬Ìù×Ó¾Í²é·â£¿</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 name="maxadpost" value="$maxadpost" maxlength=3> Ä¬ÈÏ: 4(²»ÄÜĞ¡ÓÚ3)£¬Èç¹ûÒªÈ¡Ïû£¬ÇëÉèÖÃ 999</td>
                </tr>
                ~;
		
		$tempoutput = "<select name=\"coolclickdisp\">\n<option value=\"0\">²»Ê¹ÓÃ\n<option value=\"1\">Ê¹ÓÃ\n</select>\n";
		$tempoutput =~ s/value=\"$coolclickdisp\"/value=\"$coolclickdisp\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃ LeoBBS µã»÷·ç¸ñ£¿Ê¹ÓÃµÄ»°£¬µã»÷½«»áÏÈÏÔÊ¾Ò»¸ö½ø³ÌÌõ£¡</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		~;
		
		$tempoutput = "<select name=\"friendonlinepop\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
		$tempoutput =~ s/value=\"$friendonlinepop\"/value=\"$friendonlinepop\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=ËÎÌå color=#333333><b>ºÃÓÑÉÏÏßÊÇ·ñÍ¨Öª£¿</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		~;

		$tempoutput = "<select name=\"cpudisp\">\n<option value=\"0\">²»ÏÔÊ¾\n<option value=\"1\">ÏÔÊ¾\n</select>\n";
		$tempoutput =~ s/value=\"$cpudisp\"/value=\"$cpudisp\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF width=40%>
		<font face=ËÎÌå color=#333333><b>ÊÇ·ñÏÔÊ¾ÂÛÌ³ CPU Õ¼ÓÃÊ±¼ä¡£(´ËÉèÖÃ¶ÔÌ³Ö÷ÎŞĞ§)</font></td>
		<td bgcolor=#FFFFFF>
		$tempoutput</td>
		</tr>
		
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÏÔÊ¾ÂÛÌ³ CPU Õ¼ÓÃÊ±¼äµÄ×ÖÌåÑÕÉ«</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=8 maxlength=7 name="cpudispcolor" value="$cpudispcolor"> Ä¬ÈÏ£º#c0c0c0</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"useemote\">\n<option value=\"no\">²»Ê¹ÓÃ\n<option value=\"yes\">Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃ EMOTE ±êÇ©</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"announcements\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃÂÛÌ³¹«¸æ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
		
                $tempoutput = "<select name=\"refreshurl\">\n<option value=\"0\">×Ô¶¯·µ»Øµ±Ç°ÂÛÌ³\n<option value=\"1\">×Ô¶¯·µ»Øµ±Ç°Ìù×Ó\n</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>·¢±í¡¢»Ø¸´Ìù×Óºó×Ô¶¯×ªÒÆµ½£¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"dispboardonline\">\n<option value=\"no\">²»ÏÔÊ¾\n<option value=\"yes\">ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardonline\"/value=\"$dispboardonline\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÔÚÊ×Ò³ÏÔÊ¾·ÖÂÛÌ³ÏêÏ¸ÔÚÏßÇé¿ö</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"adminstyle\">\n<option value=\"2\">ÏÂÀ­²Ëµ¥ÏÔÊ¾\n<option value=\"1\">Æ½°åÏÔÊ¾\n<option value=\"3\">×Ô¶¯ÅĞ¶Ï\n</select>\n";
                $tempoutput =~ s/value=\"$adminstyle\"/value=\"$adminstyle\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³°æÖ÷ÏÔÊ¾ÑùÊ½</b><BR>Èç¹ûÑ¡ÔñÆ½°åÏÔÊ¾£¬Ö»ÄÜÏÔÊ¾Ç°£³¸ö°æÖ÷£¬ÉèÖÃºó£¬ĞèÒªÇå¿Õ»º´æÒ»´Î</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"disphideboard\">\n<option value=\"no\">²»ÏÔÊ¾\n<option value=\"yes\">ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$disphideboard\"/value=\"$disphideboard\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Ìø×ªÂÛÌ³À¸ÖĞÊÇ·ñÏÔÊ¾Òşº¬ÂÛÌ³</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispchildjump\">\n<option value=\"no\">²»ÏÔÊ¾\n<option value=\"yes\">ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispchildjump\"/value=\"$dispchildjump\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Ìø×ªÂÛÌ³À¸ÖĞÊÇ·ñÏÔÊ¾×ÓÂÛÌ³</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispboardsm\">\n<option value=\"yes\">ÏÔÊ¾\n<option value=\"no\">²»ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispboardsm\"/value=\"$dispboardsm\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÔÚ×îÏÂÃæÏÔÊ¾ÂÛÌ³ÉùÃ÷</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"dispborn\">\n<option value=\"yes\">ÏÔÊ¾\n<option value=\"no\">²»ÏÔÊ¾\n<option value=\"auto\">ÓĞ²ÅÏÔÊ¾£¬ÎŞÔò²»ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispborn\"/value=\"$dispborn\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Ê×Ò³ÊÇ·ñÏÔÊ¾µ±ÌìÉúÈÕÓÃ»§</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"sendtobirthday\">\n<option value=\"no\">²»·¢ËÍ\n<option value=\"yes\">·¢ËÍ\n</select>\n";
                $tempoutput =~ s/value=\"$sendtobirthday\"/value=\"$sendtobirthday\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñ¸øµ±ÌìÉúÈÕÓÃ»§·¢ËÍ×£ºØĞÅÏ¢</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"usetodaypostreply\">\n<option value=\"yes\">ÊÇµÄ£¬¼ÇÂ¼\n<option value=\"no\">²»£¬²»¼ÇÂ¼\n</select>\n";
                $tempoutput =~ s/value=\"$usetodaypostreply\"/value=\"$usetodaypostreply\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñ°Ñ»Ø¸´Ò²¼ÇÂ¼ÔÚÃ¿ÈÕ·¢ÌùÊıÉÏ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"dispinfos\">\n<option value=\"yes\">ÏÔÊ¾\n<option value=\"no\">²»ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispinfos\"/value=\"$dispinfos\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Ê×Ò³ÊÇ·ñÏÔÊ¾¸öÈË×´Ì¬»òÕß¿ìËÙµÇÂ¼</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"displink\">\n<option value=\"no\">²»ÏÔÊ¾\n<option value=\"yes\">ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$displink\"/value=\"$displink\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Ê×Ò³ÊÇ·ñÏÔÊ¾Ê×Ò³Á¬½Ó</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"displinkaddr\">\n<option value=\"1\">Ê×Ò³ÏÂ·½\n<option value=\"2\">Ê×Ò³ÉÏ·½\n</select>\n";
                $tempoutput =~ s/value=\"$displinkaddr\"/value=\"$displinkaddr\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÏÔÊ¾Ê×Ò³Á¬½ÓµÄÎ»ÖÃ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Ê×Ò³Á¬½Ó</b><br>ÓÃ HTML Óï·¨ÊéĞ´£¡</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="links" cols="40" rows="6">$links</textarea><BR>
                </td>
                </tr>
                ~;

	$adlinks   =~ s/\[br\]/\n/isg;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³¹ã¸æÇø</b><br>ÓÃ HTML Óï·¨ÊéĞ´£¡</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adlinks" cols="40" rows="10">$adlinks</textarea><BR>
                </td>
                </tr>
                ~;


	$topicad   =~ s/\[br\]/\n/isg;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>¿´Ìù¹ã¸æÇø</b><br>ÓÃ HTML Óï·¨ÊéĞ´£¡</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="topicad" cols="40" rows="10">$topicad</textarea><BR>
                </td>
                </tr>
                ~;

		print qq~
		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³´´½¨µÄÈÕÆÚ</b><BR>ÇëÌîĞ´ÍêÕû£¬ÄêÔÂÈÕ²»¿ÉÈ±ÈÎºÎÒ»¸ö£¡</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="createyear" value="$createyear" size=4>Äê<input type=text name="createmon" value="$createmon" size=2>ÔÂ<input type=text name="createday" value="$createday" size=2>ÈÕ¡£(ÇëÓÃ±ê×¼ÄêÔÂÈÕ¸ñÊ½£¬ÄêÓÃËÄÎ»±íÊ¾)</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"dispprofile\">\n<option value=\"yes\">ÔÊĞí\n<option value=\"no\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$dispprofile\"/value=\"$dispprofile\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÔÊĞí¿ÍÈË²é¿´ÓÃ»§×ÊÁÏ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"forumnamedisp\">\n<option value=\"0\">²»ÏÔÊ¾\n<option value=\"1\">ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$forumnamedisp\"/value=\"$forumnamedisp\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³Ê×Ò³ÊÇ·ñÏÔÊ¾Ö±½Ó·¢Ìù°´Å¥</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"canhidden\">\n<option value=\"yes\">ÔÊĞí\n<option value=\"no\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$canhidden\"/value=\"$canhidden\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÊÇ·ñÔÊĞíÓÃ»§ÒşÉí£¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispguest\">\n<option value=\"1\">ÊÓÏµÍ³¸ººÉ¶ø¶¨\n<option value=\"2\">ÓÀÔ¶ÏÔÊ¾\n<option value=\"3\">ÓÀÔ¶²»ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispguest\"/value=\"$dispguest\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÔÚÏßÁĞ±íÖĞÊÇ·ñÏÔÊ¾¿ÍÈË£¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"userincert\">\n<option value=\"yes\">ÔÊĞí\n<option value=\"no\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$userincert\"/value=\"$userincert\" selected/;
                print qq~

		<tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>·ÃÎÊÂÛÌ³µÄ×î´ó¿ÍÈËÊı(³¬¹ı´ËÊıÄ¿µÄ¿ÍÈË½«±ØĞë×¢²á²Å¿ÉÒÔ·ÃÎÊ¡£´ò¿ª´Ë¹¦ÄÜºó£¬¼ÇµÃÔÚÄ¬ÈÏ·ç¸ñÉèÖÃÖĞ°Ñ¡°ÊÇ·ñÔÊĞíËÑË÷ÒıÇæÖ±½Ó·ÃÎÊ£¿¡±¿ª·Å£¬·ñÔòËÑË÷ÒıÇæ¿ÉÄÜ»áÒòÎª¿ÍÈËÊı³¬¹ıµ¼ÖÂÎŞ·¨¶ÔÄãÂÛÌ³½øĞĞÕıÈ·µÄË÷Òı)</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=4 maxlength=4 name="maxguests" value="$maxguests"> Èç²»ĞèÒª´Ë¹¦ÄÜ£¬ÇëÉèÖÃÎª¿Õ»ò0</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÈÏÖ¤ÂÛÌ³ÊÇ·ñÔÊĞíÆÕÍ¨ÓÃ»§½øÈë£¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispmememail\">\n<option value=\"yes\">¸ù¾İÓÃ»§ÉèÖÃÒªÇó¾ö¶¨ÏÔÊ¾\n<option value=\"no\">Ç¿ÖÆ²»ÏÔÊ¾ËùÓĞµÄ Email µØÖ·\n</select>\n";
                $tempoutput =~ s/value=\"$dispmememail\"/value=\"$dispmememail\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÖĞÊÇ·ñ±£ÃÜËùÓĞµÄÓÃ»§ Email £¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"flashavatar\">\n<option value=\"no\">²»Ö§³Ö\n<option value=\"yes\">Ö§³Ö\n</select>\n";
                $tempoutput =~ s/value=\"$flashavatar\"/value=\"$flashavatar\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÉÏ´«Í·ÏñÊÇ·ñÖ§³Ö FLASH ¸ñÊ½</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÉÏ´«Í·ÏñÎÄ¼şÔÊĞíµÄ×î´óÖµ(µ¥Î»£ºKB)</b><br>Ä¬ÈÏÔÊĞí×î´ó 200KB £¡</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxuploadava" value="$maxuploadava" size=5 maxlength=5>¡¡²»Òª¼Ó KB£¬½¨Òé²»Òª³¬¹ı 200</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333><b>ÂÛÌ³Ê×Ò³ÒôÀÖÃû³Æ</b>(Èç¹ûÃ»ÓĞÇëÁô¿Õ)<br>ÇëÊäÈë±³¾°ÒôÀÖÃû³Æ£¬±³¾°ÒôÀÖ<BR>Ó¦ÉÏ´«ÓÚ non-cgi/midi Ä¿Â¼ÏÂ¡£<br><b>²»Òª°üº¬ URL µØÖ·»ò¾ø¶ÔÂ·¾¶£¡</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="midiaddr2" value="$midiaddr2">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr2";
                print qq~¡¡<EMBED src="$imagesurl/midi/$midiaddr2" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr2 ne ""));
                print qq~
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>Ö»ÔÊĞí½øÈëÂÛÌ³µÄµØÇø</b><br>·ÇÔÊĞíµØÇøµÄ IP ½«ÎŞ·¨½øÈëÂÛÌ³£¬ÓÉÓÚÀûÓÃµÄÊÇÂÛÌ³ÄÚ²¿µÄ IP µØÖ·¿â£¬ÓĞÎóÅĞ¶ÏµÄ¿ÉÄÜĞÔ£¬<B>¶øÇÒ´ËÑ¡Ïî»¹ÊÜ IP ½ûÖ¹µÄÔ¼Êø</B>£¡</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="arrowformwhere" value="$arrowformwhere" size=20>¡¡¶à¸öµØÇøÓÃ¶ººÅ¸ô¿ª£¬ÒÔÊĞ»òÊ¡Îªµ¥Î»</td>
                </tr>
		~;

                $tempoutput = "<select name=\"usefake\">\n<option value=\"no\">²»Ê¹ÓÃ\n<option value=\"yes\">Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$usefake\"/value=\"$usefake\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñ²ÉÓÃÎ±¾²Ì¬·½Ê½£¨¾ßÌå¿´ËµÃ÷£¬·şÎñÆ÷²»Ö§³ÖµÄ»°£¬Ç§Íò²»ÒªÓÃ£©</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput <a href=leobbs.htm target=_blank>°´´Ë²âÊÔ</a>£¬Èç¹ûÄÜ¿´µ½ÂÛÌ³Ê×Ò³£¬ËµÃ÷·şÎñÆ÷ÉèÖÃÕıÈ·£¡<BR>ÈçÌáÊ¾ÎÄ¼şÃ»ÓĞÕÒµ½£¬ÄÇ¾ÍËµÃ÷Î´ÉèÖÃÕıÈ·£¬Çë²Î¿¼ËµÃ÷ÎÄµµÖØĞÂÉèÖÃ£¡</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <input type=submit value="Ìá ½»"></form></td></tr></table></td></tr></table>
                ~;
                
                }
            }
            else {
                 &adminlogin;
                 }
      
print qq~</td></tr></table></body></html>~;
exit;

# ²âÊÔ SENDMAIL Â·¾¶
sub mailprogram
{
    $mailprogram='/usr/sbin/sendmail';
    if (!(-e $mailprogram)) {$mailprogram='/usr/bin/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/bin/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/lib/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/usr/slib/sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='sendmail';} 
    if (!(-e $mailprogram)) {$mailprogram='/usr/lib/sendmail';};
    if (!(-e $mailprogram)) {$mailprogram='perlmail';}; 
    if (!(-e $mailprogram)) {$mailprogram="Unknow";};
    return $mailprogram;
}
