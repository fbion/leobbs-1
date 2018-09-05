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
require "data/mpic.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "forumstyles.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

@params = $query->param;
foreach $param(@params) {
    $theparam = $query->param($param);

        if (($_ eq 'maintopicad')||($_ eq 'replytopicad')) {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}

    $theparam = &unHTML("$theparam");

        if ($_ eq "footmark" || $_ eq "headmark" || $_ eq "adfoot" || $_ eq "adscript") {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}
    $PARAM{$param} = $theparam;
}

$action      =  $PARAM{'action'};
$inforum     =  $PARAM{'forum'};
$incategory  =  $PARAM{'category'};

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) { #s1

            my %Mode = (
            'style'               =>    \&styleform,
            'dostyle'             =>    \&dostyle,
            );


    if($Mode{$action}) {
        $Mode{$action}->();
    }
    else {

    if ($action eq "delstyle") {
        print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / åˆ†è®ºå›é£æ ¼åˆ é™¤</b>
                    </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>è­¦å‘Šï¼ï¼</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>å®Œå…¨åˆ é™¤æ­¤åˆ†è®ºå›çš„æ‰€æœ‰è‡ªå®šä¹‰é£æ ¼ï¼Œä¸å¯æ¢å¤<p>
        <p>
        >> <a href="$thisprog?action=delstyleok&forum=$inforum">å¼€å§‹åˆ é™¤</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
    }
    elsif ($action eq "delstyleok") {
        $filetomake = "$lbdir" . "data/style$inforum.cgi";
    	unlink $filetomake;
        $filetomake = "${imagesdir}css/style$inforum.cgi";
    	unlink $filetomake;
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / åˆ†è®ºå›é£æ ¼åˆ é™¤</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>æ‰€æœ‰ä¿¡æ¯å·²ç»ä¿å­˜</b><br>æ­¤åˆ†è®ºå›çš„é£æ ¼å·²ç»å®Œå…¨åˆ é™¤ã€‚
                    </td></tr></table></td></tr></table>
                    ~;

    }
    	
   }
}
else {
    &adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;

##################################################################################

sub styleform {

        if ($incategory ne "main"){
         $filerequire = "$lbdir" . "data/style${inforum}.cgi";
        if (-e $filerequire) {
         	require $filerequire;
                }
        if ($incategory ne ""){
        $stylefile = "$lbdir" . "data/skin/$incategory.cgi";
                if (-e $stylefile) {
         	require $stylefile;
        }
        }
        }


        $dirtoopen = "$lbdir" . "data/skin";
        opendir (DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir (DIR);
        my $myskin="";
        @thd = grep(/\.cgi$/,@dirdata);
        $topiccount = @thd;
        @thd=sort @thd;
        for (my $i=0;$i<$topiccount;$i++){
       	$thd[$i]=~s /\.cgi//isg;
        $myskin.=qq~<option value="$thd[$i]">çš®è‚¤ [ $thd[$i] ]~;
        }
        $myskin =~ s/value=\"$skinselected\"/value=\"$skinselected\" selected/;

&getoneforum("$inforum");

	$footmark   =~ s/\[br\]/\n/isg;
	$headmark   =~ s/\[br\]/\n/isg;
	$adfoot   =~ s/\[br\]/\n/isg;
	$adscript   =~ s/\[br\]/\n/isg;
	$maintopicad   =~ s/\[br\]/\n/isg;
	$replytopicad   =~ s/\[br\]/\n/isg;

print qq~
        <tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF>
        <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / ç¼–è¾‘åˆ†è®ºå›çš®è‚¤é£æ ¼</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=3>
        <font color=#000000><b>ç¼–è¾‘ $forumname çš„åˆ†è®ºå›çš®è‚¤é£æ ¼,<Br>å¦‚æœä½ ä¸æƒ³æ›´æ”¹ï¼Œè¯·ç•™ç©ºé€‰é¡¹ï¼Œä¸å¡«å†™ï¼ï¼ï¼</b>
        </td></tr>
        <tr><td bgcolor=#FFFFFF align=center colspan=3><font color=#ffffff>LeoBBS</font></td></tr>

        <tr>
        <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>è®ºå›é£æ ¼é€‰æ‹©</b>
                </font></td>
                </tr>

        <form name=MAINFORM action="$thisprog" method="post">
        <input type=hidden name="action" value="dostyle">
        <input type=hidden name="forum" value="$inforum">
        <input type=hidden name="skin" value="$skin" size=10 maxlength=10>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ç³»ç»Ÿè‡ªå¸¦çš„çš®è‚¤é£æ ¼</b><br>ä½ é€‰æ‹©åï¼Œéœ€è¦æ­£å¼ç¡®è®¤æäº¤æ‰ç”Ÿæ•ˆ</font></td>
                <td bgcolor=#FFFFFF>
                <select name="skinselected">
                <option value="">é»˜è®¤é£æ ¼$myskin
                </select>
                </td></tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>è®ºå›çŠ¶æ€è®¾ç½®</b>
                </font></td>
                </tr>
                ~;
                $tempoutput1 = "<select name=\"mainonoff\">\n<option value=\"0\">è®ºå›å¼€æ”¾\n<option value=\"1\">è®ºå›å…³é—­\n<option value=\"2\">è‡ªåŠ¨å®šæœŸå¼€æ”¾\n</select>\n";
                $tempoutput1 =~ s/value=\"$mainonoff\"/value=\"$mainonoff\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font face=å®‹ä½“ color=#333333 ><b>è®ºå›çŠ¶æ€</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput1</td>
                </tr>
                ~;
	$tempoutput1 = "<select name=\"mainauto1\">\n<option value=\"day\">æ¯å¤©\n<option value=\"week\">æ¯æ˜ŸæœŸ\n<option value=\"month\">æ¯æœˆ\n</select>\n";
	$tempoutput1 =~ s/value=\"$mainauto1\"/value=\"$mainauto1\" selected/;
	print qq~
              <tr>
              <td bgcolor=#FFFFFF width=40% colspan=2>
              <font face=å®‹ä½“ color=#333333 ><b>è‡ªåŠ¨å¼€æ”¾è®ºå›äº</b><br>(åªæœ‰é€‰æ‹©è‡ªåŠ¨å®šæœŸå¼€æ”¾æ­¤é¡¹æœ‰æ•ˆ)</font></td>
              <td bgcolor=#FFFFFF>
              $tempoutput1 <input name=mainautovalue1 value="$mainautovalue1" size=8><br>æ³¨: å¯ä»¥ä½¿ç”¨å•ä¸€æ•°å­—æˆ–æ˜¯èŒƒå›´ï¼Œå¦‚æ¯å¤©6, æ¯å¤©0-6, æ¯æ˜ŸæœŸ6, æ¯æœˆ10-15</td>
              </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font face=å®‹ä½“ color=#333333 ><b>ç»´æŠ¤è¯´æ˜</b> (æ”¯æŒ HTML)<BR><BR></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                <textarea name="line1" cols="40">$line1</textarea><BR><BR></td>
                </tr>
		~;
               $tempoutput = "<select name=\"usesuperannounce\">\n<option value=\"0\">ä¸ä½¿ç”¨\n<option value=\"1\">ä½¿ç”¨\n</select>\n"; 
               $tempoutput =~ s/value=\"$usesuperannounce\"/value=\"$usesuperannounce\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=å®‹ä½“ color=#333333><b>æ˜¯å¦ä½¿ç”¨è®ºå›è¶…çº§å…¬å‘Š</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>è¶…çº§å…¬å‘Šå†…å®¹</b><br>(æ”¯æŒHTMLæ ¼å¼ï¼Œæ˜¾ç¤ºç»™æ‰€æœ‰ç”¨æˆ·)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="superannounce" cols="40">$superannounce</textarea><BR>
                </td>
                </tr>
		~;

               $tempoutput = "<select name=\"superannouncedisp\">\n<option value=\"oncepersession\">æ¯ä¸ªè¿›ç¨‹åªæ˜¾ç¤ºä¸€æ¬¡\n<option value=\"always\">æ€»æ˜¯æ˜¾ç¤º\n<option value=\"2\">50%æ˜¾ç¤ºå‡ ç‡\n<option value=\"3\">33%æ˜¾ç¤ºå‡ ç‡\n<option value=\"4\">25%æ˜¾ç¤ºå‡ ç‡\n<option value=\"10\">10%æ˜¾ç¤ºå‡ ç‡\n<option value=\"20\">5%æ˜¾ç¤ºå‡ ç‡\n<option value=\"50\">2%æ˜¾ç¤ºå‡ ç‡\n<option value=\"100\">1%æ˜¾ç¤ºå‡ ç‡\n</select>\n"; 
               $tempoutput =~ s/value=\"$superannouncedisp\"/value=\"$superannouncedisp\" selected/; 

               $tempoutput1 = "<select name=\"superannouncehide\">\n<option value=\"yes\">äºŒåç§’åè‡ªåŠ¨éšè—\n<option value=\"no\">ä¸€ç›´æ˜¾ç¤º\n</select>\n"; 
               $tempoutput1 =~ s/value=\"$superannouncehide\"/value=\"$superannouncehide\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=å®‹ä½“ color=#333333><b>è®ºå›è¶…çº§å…¬å‘Šé€‰é¡¹</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput $tempoutput1</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>è®ºå›BODYæ ‡ç­¾</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>æ§åˆ¶æ•´ä¸ªè®ºå›é£æ ¼çš„èƒŒæ™¯é¢œè‰²æˆ–è€…èƒŒæ™¯å›¾ç‰‡ç­‰</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>é»˜è®¤ï¼šbgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ä¸»é¡µåœ°å€</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="homeurl" value="$homeurl"></td>
                </tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b>è®ºå›é¡µçœ‰å’Œé¡µè„š</b>
</font></td>
</tr>

		<tr>
<td bgcolor=#FFFFFF valign=middle align=left width=40%>
<font color=#333333><b>é¡µçœ‰</b><br>(æ˜¾ç¤ºåœ¨é¡µé¢æœ€ä¸Šæ–¹ï¼ŒHTMLæ ¼å¼)</font></td>
<td></td><td bgcolor=#FFFFFF>
<textarea name="headmark" cols="40">$headmark</textarea><BR>
</td>
</tr>

		<tr>
<td bgcolor=#FFFFFF valign=middle align=left width=40%>
<font color=#333333><b>é¡µè„š</b><br>(æ˜¾ç¤ºåœ¨ç‰ˆæƒä¿¡æ¯ä¸‹æ–¹ï¼ŒHTMLæ ¼å¼)</font></td>
<td></td><td bgcolor=#FFFFFF>
<textarea name="footmark" cols="40">$footmark</textarea><BR>
</td>
</tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>æ˜¯å¦æ˜¾ç¤ºåŸç‰ˆé¡µçœ‰</font></td>
                <td bgcolor=#FFFFFF>
		~;
                $tempoutput = "<select name=\"usetopm\">\n<option value=\"yes\">æ˜¾ç¤º\n<option value=\"no\">ä¸æ˜¾ç¤º\n</select><p>\n";
                $tempoutput =~ s/value=\"$usetopm\"/value=\"$usetopm\" selected/;
                print qq~
                $tempoutput</td>
		</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b>è®ºå›é¡µé¦–èœå•</b>
</font></td>
</tr>
<script>
function selcolor(obj,obj2){
var arr = showModalDialog("$imagesurl/editor/selcolor.html", "", "dialogWidth:18.5em; dialogHeight:17.5em; status:0");
obj.value=arr;
obj2.style.backgroundColor=arr;
}
</script>
<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>èœå•å¸¦å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$menufontcolor  width=12 id=menufontcolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="menufontcolor" value="$menufontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,menufontcolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#333333</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>èœå•å¸¦èƒŒæ™¯é¢œè‰²</font></td>
<td bgcolor=$menubackground  width=12 id=menubackground2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="menubackground" value="$menubackground" size=7 maxlength=7 onclick="javascript:selcolor(this,menubackground2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#DDDDDD</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>èœå•å¸¦èƒŒæ™¯å›¾ç‰‡</font><BR>è¯·è¾“å…¥å›¾ç‰‡åç§°ï¼Œæ­¤å›¾å¿…é¡»åœ¨ images ç›®å½•ä¸‹çš„ $skin é‡Œ</td>
<td background=$imagesurl/images/$skin/$menubackpic  width=12>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="menubackpic" value="$menubackpic"></td>
</tr>

<tr>
<td bgcolor=#FFFFFF width=40%>
<font color=#333333>èœå•å¸¦è¾¹ç•Œé¢œè‰²</font></td>
<td bgcolor=$titleborder  width=12 id=titleborder2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="titleborder" value="$titleborder" size=7 maxlength=7 onclick="javascript:selcolor(this,titleborder2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#333333</td>
</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b>å­—ä½“å¤–è§‚å’Œé¢œè‰²</b>
</font></td>
</tr>


<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333>ä¸»å­—ä½“å¤–è§‚</font></td>
<td bgcolor=#FFFFFF>
~;
$tempoutput = "<select name=\"font\">\n<option value=\"å®‹ä½“\">å®‹ä½“\n<option value=\"ä»¿å®‹_gb2312\">ä»¿å®‹\n<option value=\"æ¥·ä½“_gb2312\">æ¥·ä½“\n<option value=\"é»‘ä½“\">é»‘ä½“\n<option value=\"éš¶ä¹¦\">éš¶ä¹¦\n<option value=\"å¹¼åœ†\">å¹¼åœ†\n</select><p>\n";
$tempoutput =~ s/value=\"$font\"/value=\"$font\" selected/;
print qq~
$tempoutput</td>
</tr>


<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>"æœ€åå‘è´´è€…"å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$lastpostfontcolor  width=12 id=lastpostfontcolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="lastpostfontcolor" value="$lastpostfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,lastpostfontcolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#000000</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>"åŠ é‡åŒº"å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$fonthighlight  width=12 id=fonthighlight2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="fonthighlight" value="$fonthighlight" size=7 maxlength=7 onclick="javascript:selcolor(this,fonthighlight2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#990000</td>
</tr>

<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333>æŸ¥çœ‹æ—¶å‘è¡¨è€…åç§°å­—ä½“</font></td>
<td bgcolor=#FFFFFF>
~;
$tempoutput = "<select name=\"posternamefont\">\n<option value=\"å®‹ä½“\">å®‹ä½“\n<option value=\"ä»¿å®‹_gb2312\">ä»¿å®‹\n<option value=\"æ¥·ä½“_gb2312\">æ¥·ä½“\n<option value=\"é»‘ä½“\">é»‘ä½“\n<option value=\"éš¶ä¹¦\">éš¶ä¹¦\n<option value=\"å¹¼åœ†\">å¹¼åœ†\n</select><p>\n";
$tempoutput =~ s/value=\"$posternamefont\"/value=\"$posternamefont\" selected/;
print qq~
$tempoutput</td>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>ä¸€èˆ¬ç”¨æˆ·åç§°å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$posternamecolor  width=12 id=posternamecolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="posternamecolor" value="$posternamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,posternamecolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#000066</td>
</tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font color=#333333>ä¸€èˆ¬ç”¨æˆ·åç§°ä¸Šçš„å…‰æ™•é¢œè‰²</font></td>
		<td bgcolor=$memglow  width=12 id=memglow2>ã€€</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="memglow" value="$memglow" size=7 maxlength=7 onclick="javascript:selcolor(this,memglow2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#9898BA</td>
		</tr>
               
<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å›ä¸»åç§°å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$adminnamecolor  width=12 id=adminnamecolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="adminnamecolor" value="$adminnamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,adminnamecolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#990000</td>
</tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>å›ä¸»åç§°ä¸Šçš„å…‰æ™•é¢œè‰²</font></td>
		<td bgcolor=$adminglow  width=12 id=adminglow2>ã€€</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="adminglow" value="$adminglow" size=7 maxlength=7 onclick="javascript:selcolor(this,adminglow2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#9898BA</td>
		</tr>
<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>æ€»ç‰ˆä¸»åç§°å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$smonamecolor  width=12 id=smonamecolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="smonamecolor" value="$smonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,smonamecolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#009900</td>
</tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>æ€»ç‰ˆä¸»åç§°ä¸Šçš„å…‰æ™•é¢œè‰²</font></td>
		<td bgcolor=$smoglow  width=12 id=smoglow2>ã€€</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="smoglow" value="$smoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,smoglow2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#9898BA</td>
		</tr>
<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>åˆ†ç±»åŒºç‰ˆä¸»åç§°å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$cmonamecolor  width=12 id=cmonamecolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="cmonamecolor" value="$cmonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,cmonamecolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#009900</td>
</tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>åˆ†ç±»åŒºç‰ˆä¸»åç§°ä¸Šçš„å…‰æ™•é¢œè‰²</font></td>
		<td bgcolor=$cmoglow  width=12 id=cmoglow2>ã€€</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="cmoglow" value="$cmoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,cmoglow2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#9898BA</td>
		</tr>
<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>ç‰ˆä¸»åç§°å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$teamnamecolor  width=12 id=teamnamecolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="teamnamecolor" value="$teamnamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,teamnamecolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#0000ff</td>
</tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>ç‰ˆä¸»åç§°ä¸Šçš„å…‰æ™•é¢œè‰²</font></td>
		<td bgcolor=$teamglow  width=12 id=teamglow2>ã€€</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="teamglow" value="$teamglow" size=7 maxlength=7 onclick="javascript:selcolor(this,teamglow2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#9898BA</td>
		</tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>å‰¯ç‰ˆä¸»åç§°å­—ä½“é¢œè‰²</font></td>
                <td bgcolor=$amonamecolor  width=12 id=amonamecolor2>ã€€</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="amonamecolor" value="$amonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,amonamecolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>å‰¯ç‰ˆä¸»åç§°ä¸Šçš„å…‰æ™•é¢œè‰²</font></td>
		<td bgcolor=$amoglow  width=12 id=amoglow2>ã€€</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="amoglow" value="$amoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,amoglow2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#9898BA</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>è®¤è¯ç”¨æˆ·åç§°å­—ä½“é¢œè‰²</font></td>
                <td bgcolor=$rznamecolor  width=12 id=rznamecolor2>ã€€</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="rznamecolor" value="$rznamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,rznamecolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#44ff00</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>è®¤è¯ç”¨æˆ·åç§°ä¸Šçš„å…‰æ™•é¢œè‰²</font></td>
		<td bgcolor=$rzglow  width=12 id=rzglow2>ã€€</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="rzglow" value="$rzglow" size=7 maxlength=7 onclick="javascript:selcolor(this,rzglow2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#008736</td>
		</tr>
		
		<td bgcolor=#FFFFFF>
		<font color=#333333>è¿‡æ»¤å’Œç¦è¨€ç”¨æˆ·åç§°ä¸Šçš„å…‰æ™•é¢œè‰²</font></td>
		<td bgcolor=$banglow  width=12 id=banglow2>ã€€</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="banglow" value="$banglow" size=7 maxlength=7 onclick="javascript:selcolor(this,banglow2)" style="cursor:hand">ã€€é»˜è®¤ï¼šnone</td>
		</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b><center>æ‰€æœ‰é¡µé¢é¢œè‰²</center></b><br>
<font color=#333333>è¿™äº›é¢œè‰²é…ç½®å°†ç”¨äºæ¯ä¸ªé¡µé¢ã€‚ç”¨äºæ³¨å†Œã€ç™»å½•ã€åœ¨çº¿ä»¥åŠå…¶ä»–é¡µé¢ã€‚
</font></td>
</tr>

<tr>
<td bgcolor=#FFFFFF width=40%>
<font color=#333333>ä¸»å­—ä½“é¢œè‰²ä¸€</font></td>
<td bgcolor=$fontcolormisc  width=12 id=fontcolormisc3>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="fontcolormisc" value="$fontcolormisc" size=7 maxlength=7 onclick="javascript:selcolor(this,fontcolormisc3)" style="cursor:hand">ã€€é»˜è®¤ï¼š#333333</td>
</tr>

<tr>
<td bgcolor=#FFFFFF width=40%>
<font color=#333333>ä¸»å­—ä½“é¢œè‰²äºŒ</font></td>
<td bgcolor=$fontcolormisc2  width=12 id=fontcolormisc4>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="fontcolormisc2" value="$fontcolormisc2" size=7 maxlength=7 onclick="javascript:selcolor(this,fontcolormisc4)" style="cursor:hand">ã€€é»˜è®¤ï¼š#444444</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å…¶ä»–èƒŒæ™¯é¢œè‰²ä¸€</font></td>
<td bgcolor=$miscbackone  width=12 id=miscbackone2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="miscbackone" value="$miscbackone" size=7 maxlength=7 onclick="javascript:selcolor(this,miscbackone2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#FFFFFF</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å…¶ä»–èƒŒæ™¯é¢œè‰²äºŒ</font></td>
<td bgcolor=$miscbacktwo  width=12 id=miscbacktwo2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="miscbacktwo" value="$miscbacktwo" size=7 maxlength=7 onclick="javascript:selcolor(this,miscbacktwo2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#EEEEEE</td>
</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b><center>è¡¨æ ¼é¢œè‰²</center></b><br>
<font color=#333333>è¿™äº›é¢œè‰²å¤§éƒ¨åˆ†ç”¨äºleobbs.cgiï¼Œforums.cgiå’Œtopic.cgi
</td></tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>æ‰€æœ‰è¡¨æ ¼è¾¹ç•Œé¢œè‰²</font></td>
<td bgcolor=$tablebordercolor  width=12 id=tablebordercolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="tablebordercolor" value="$tablebordercolor" size=7 maxlength=7 onclick="javascript:selcolor(this,tablebordercolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#000000</td>
</tr>

<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333>æ‰€æœ‰è¡¨æ ¼å®½åº¦</font></td>
<td bgcolor=#FFFFFF>
<input type=text name="tablewidth" value="$tablewidth" size=5 maxlength=5>ã€€é»˜è®¤ï¼š750</td>
</tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>å¯¼èˆªæ é¢œè‰²</center></b>
                <font color=#333333>è¿™é‡Œé¢œè‰²é…ç½®ç”¨äºè®¾ç½®å¿«æ·æ“ä½œå¯¼èˆªæ çš„é¢œè‰²
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>å¯¼èˆªæ è¾¹çº¿é¢œè‰²</font></td>
                <td bgcolor=$navborder width=12 id=navborder2>ã€€</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navborder" value="$navborder" size=7 maxlength=7 onclick="javascript:selcolor(this,navborder2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#E6E6E6</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>å¯¼èˆªæ èƒŒæ™¯é¢œè‰²</font></td>
                <td bgcolor=$navbackground width=12 id=navbackground2>ã€€</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navbackground" value="$navbackground" size=7 maxlength=7 onclick="javascript:selcolor(this,navbackground2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#F7F7F7</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>å¯¼èˆªæ å­—ä½“é¢œè‰²</font></td>
                <td bgcolor=$navfontcolor width=12 id=navfontcolor2>ã€€</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navfontcolor" value="$navfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,navfontcolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#4D76B3</td>
                </tr>
                
<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b><center>æ ‡é¢˜é¢œè‰²</center></b><br>
<font color=#333333>è¿™é‡Œé¢œè‰²é…ç½®ç”¨äºå‘è¡¨ç¬¬ä¸€ä¸ªä¸»é¢˜çš„æ ‡é¢˜
</td></tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>è®ºå›/ä¸»é¢˜çš„æ ‡é¢˜æ èƒŒæ™¯é¢œè‰²</font></td>
<td bgcolor=$titlecolor  width=12 id=titlecolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="titlecolor" value="$titlecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,titlecolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#acbded</td>
</tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>æ ‡é¢˜æ èƒŒæ™¯å›¾ç‰‡</font><BR>è¯·è¾“å…¥å›¾ç‰‡åç§°ï¼Œæ­¤å›¾å¿…é¡»åœ¨ images ç›®å½•ä¸‹çš„ $skin é‡Œ</td>
                <td background=$imagesurl/images/$skin/$catbackpic  width=12>ã€€</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
                </tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>è®ºå›/ä¸»é¢˜çš„æ ‡é¢˜æ å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$titlefontcolor  width=12 id=titlefontcolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="titlefontcolor" value="$titlefontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,titlefontcolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#333333</td>
</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b><center>è®ºå›å†…å®¹é¢œè‰²</center></b><br>
<font color=#333333>æŸ¥çœ‹è®ºå›å†…å®¹æ—¶é¢œè‰² (forums.cgi)
</td></tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å†…å®¹é¢œè‰²ä¸€</font></td>
<td bgcolor=$forumcolorone  width=12 id=forumcolorone2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="forumcolorone" value="$forumcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,forumcolorone2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#f0F3Fa</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å†…å®¹é¢œè‰²äºŒ</font></td>
<td bgcolor=$forumcolortwo  width=12 id=forumcolortwo2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="forumcolortwo" value="$forumcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,forumcolortwo2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#F2F8FF</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å†…å®¹å­—ä½“é¢œè‰²</font></td>
<td bgcolor=$forumfontcolor  width=12 id=forumfontcolor2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="forumfontcolor" value="$forumfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,forumfontcolor2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#333333</td>
</tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><b><center>å›å¤é¢œè‰²</center></b><br>
<font color=#333333>å›å¤è´´å­é¢œè‰²(topic.cgi)
</td></tr>


<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å›å¤é¢œè‰²ä¸€</font></td>
<td bgcolor=$postcolorone  width=12 id=postcolorone2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="postcolorone" value="$postcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,postcolorone2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#EFF3F9</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å›å¤é¢œè‰²äºŒ</font></td>
<td bgcolor=$postcolortwo  width=12 id=postcolortwo2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="postcolortwo" value="$postcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,postcolortwo2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#F2F4EF</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å›å¤å­—ä½“é¢œè‰²ä¸€</font></td>
<td bgcolor=$postfontcolorone  width=12 id=postfontcolorone2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="postfontcolorone" value="$postfontcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,postfontcolorone2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#333333</td>
</tr>

<tr>
<td bgcolor=#FFFFFF>
<font color=#333333>å›å¤å­—ä½“é¢œè‰²äºŒ</font></td>
<td bgcolor=$postfontcolortwo  width=12 id=postfontcolortwo2>ã€€</td>
<td bgcolor=#FFFFFF>
<input type=text name="postfontcolortwo" value="$postfontcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,postfontcolortwo2)" style="cursor:hand">ã€€é»˜è®¤ï¼š#555555</td>
</tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>é¡µé¢è·¨åº¦</center></b><br>
                <font color=#333333>æ¯é¡µæ˜¾ç¤ºä¸»é¢˜çš„å›å¤æ•°ï¼Œå½“ä¸€ç¯‡ä¸»é¢˜å›å¤è¶…è¿‡ä¸€å®šæ•°é‡æ—¶åˆ†é¡µæ˜¾ç¤º (topic.cgi)
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>æ¯é¡µä¸»é¢˜æ•°</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxthreads" value="$maxthreads" size=3 maxlength=3>ã€€ä¸€èˆ¬ä¸º 20 -- 30</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>æ¯ä¸»é¢˜æ¯é¡µçš„å›å¤æ•°</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtopics" value="$maxtopics" size=3 maxlength=3>ã€€ä¸€èˆ¬ä¸º 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>å›å¤æ•°è¶…è¿‡å¤šå°‘åå°±æ˜¯çƒ­é—¨è´´ï¼Ÿ</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hottopicmark" value="$hottopicmark" size=3 maxlength=3>ã€€ä¸€èˆ¬ä¸º 10 -- 15</td>
                </tr>
                <tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>æŠ•ç¥¨æ•°è¶…è¿‡å¤šå°‘åå°±æ˜¯çƒ­é—¨æŠ•ç¥¨è´´ï¼Ÿ</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hotpollmark" value="$hotpollmark" size=3 maxlength=3>ã€€ä¸€èˆ¬ä¸º 10 -- 15</td>
                </tr>
                ~;

			   $tempoutput = "<select name=\"usehigest\"><option value=\"yes\">çªå‡º<option value=\"no\">ä¸çªå‡º</select>\n"; 
               $tempoutput =~ s/value=\"$usehigest\"/value=\"$usehigest\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>æ˜¯å¦çªå‡ºæœ€         <font color=#333333>å§£ <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>LeoBBS ±êÇ©ÉèÖÃ</center></b>(Ì³Ö÷ºÍ°æÖ÷²»ÊÜ´ËÏŞ)<br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×ÓÖĞÊÇ·ñÔÊĞíÌùÍ¼£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostflash\"><option value=\"off\">²»ÔÊĞí<option value=\"on\" >ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawpostflash\"/value=\"$arrawpostflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×ÓÖĞÊÇ·ñÔÊĞí Flash£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostreal\"><option value=\"off\">²»ÔÊĞí<option value=\"on\" >ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawpostreal\"/value=\"$arrawpostreal\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×ÓÖĞÊÇ·ñÔÊĞí Real ÎÄ¼ş£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	        $tempoutput = "<select name=\"arrawpostmedia\"><option value=\"off\">²»ÔÊĞí<option value=\"on\" >ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawpostmedia\"/value=\"$arrawpostmedia\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×ÓÖĞÊÇ·ñÔÊĞí Media ÎÄ¼ş£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

	            $tempoutput = "<select name=\"arrawpostsound\"><option value=\"off\">²»ÔÊĞí<option value=\"on\" >ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawpostsound\"/value=\"$arrawpostsound\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×ÓÖĞÊÇ·ñÔÊĞíÉùÒôÎÄ¼ş£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		        </td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawautoplay\">\n<option value=\"1\">ÔÊĞí\n<option value=\"0\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$arrawautoplay\"/value=\"$arrawautoplay\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×ÓÖĞµÄ¶àÃ½ÌåÎÄ¼şÊÇ·ñÔÊĞí×Ô¶¯²¥·Å£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrawpostfontsize\"><option value=\"off\">²»ÔÊĞí<option value=\"on\">ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawpostfontsize\"/value=\"$arrawpostfontsize\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×ÓÖĞÊÇ·ñÔÊĞí¸Ä±äÎÄ×Ö´óĞ¡£¿</font></td>
                <td bgcolor=#FFFFFF>
                 $tempoutput
		         </td>
                </tr>
		~;
		
                $tempoutput = "<select name=\"openiframe\">\n<option value=\"no\">²»ÔÊĞí\n<option value=\"yes\">ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$openiframe\"/value=\"$openiframe\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333>ÂÛÌ³ÊÇ·ñÔÊĞí Iframe ±êÇ©</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                
		$tempoutput = "<select name=\"arrawsignpic\"><option value=\"off\">²»ÔÊĞí<option value=\"on\">ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawsignpic\"/value=\"$arrawsignpic\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ç©ÃûÖĞÊÇ·ñÔÊĞíÌùÍ¼£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;
		$tempoutput = "<select name=\"arrawsignflash\"><option value=\"off\">²»ÔÊĞí<option value=\"on\">ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawsignflash\"/value=\"$arrawsignflash\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ç©ÃûÖĞÊÇ·ñÔÊĞí Flash£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;


		$tempoutput = "<select name=\"arrawsignsound\"><option value=\"off\">²»ÔÊĞí<option value=\"on\">ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawsignsound\"/value=\"$arrawsignsound\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ç©ÃûÖĞÊÇ·ñÔÊĞíÉùÒô£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"arrawsignfontsize\"><option value=\"off\">²»ÔÊĞí<option value=\"on\">ÔÊĞí</select>\n";
                $tempoutput =~ s/value=\"$arrawsignfontsize\"/value=\"$arrawsignfontsize\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ç©ÃûÖĞÊÇ·ñÔÊĞí¸Ä±äÎÄ×Ö´óĞ¡£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìû×ÓºÍÇ©ÃûÖĞ Flash Ä¬ÈÏ´óĞ¡</font></td>
                <td bgcolor=#FFFFFF>
                ¿í¶È£º <input type=text name="defaultflashwidth" value="$defaultflashwidth" size=3 maxlength=3>¡¡Ä¬ÈÏ 410 ÏñÊı<BR>
                ¸ß¶È£º <input type=text name="defaultflashheight" value="$defaultflashheight" size=3 maxlength=3>¡¡Ä¬ÈÏ 280 ÏñÊı</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÊÇ·ñÆôÓÃËõÂÔÍ¼Ä£Ê½</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = qq~<select name=imgslt><option value="">²»ÆôÓÃ</option><option value="Disp">ÆôÓÃ</option></select>~;
                $tempoutput =~ s/value=\"$imgslt\"/value=\"$imgslt\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ËõÂÔÍ¼Ä¬ÈÏ¿í¶È(Îª¿ÕÔòÄ¬ÈÏÎª60)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsltwidth" value="$defaultsltwidth" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ËõÂÔÍ¼ÏñÄ¬ÈÏ¸ß¶È(Îª¿ÕÔòÄ¬ÈÏÎª60)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsltheight" value="$defaultsltheight" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ËõÂÔÍ¼Ã¿ĞĞÊıÁ¿</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = qq~<select name=sltnoperline><option value="1">1</option><option value="2>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option></select>~;
                $tempoutput =~ s/value=\"$sltnoperline\"/value=\"$sltnoperline\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

		<tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>ÂÛÌ³°´Å¥ÉèÖÃ</b> (Ä¬ÈÏ´ËÍ¼±ØĞëÔÚ images/$skin Ä¿Â¼ÏÂ£¬Ö»ÄÜÊÇÃû³Æ£¬²»¿ÉÒÔ¼Ó URL µØÖ·»ò¾ø¶ÔÂ·¾¶)<br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>·¢ĞÂÌû°´Å¥Í¼±ê</font>¡¡(´óĞ¡£º99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newthreadlogo" value="$newthreadlogo" onblur="document.images.i_newthreadlogo.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$newthreadlogo name="i_newthreadlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>·¢ÆğÍ¶Æ±°´Å¥Í¼±ê</font>¡¡(´óĞ¡£º99*25)</td>
                <td bgcolor=#FFFFFF>
		<input type=text name="newpolllogo" value="$newpolllogo" onblur="document.images.i_newpolllogo.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$newpolllogo name="i_newpolllogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ğ¡×Ö±¨°´Å¥Í¼±ê</font>¡¡(´óĞ¡£º99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newxzblogo" value="$newxzblogo" onblur="document.images.i_newxzblogo.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$newxzblogo name="i_newxzblogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>»Ø¸´Ìû×Ó°´Å¥Í¼±ê</font>¡¡(´óĞ¡£º99*25)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newreplylogo" value="$newreplylogo" onblur="document.images.i_newreplylogo.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$newreplylogo name="i_newreplylogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ô­´°¿Ú°´Å¥Í¼±ê</font>¡¡(´óĞ¡£º74*21)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="wlogo" value="$wlogo" onblur="document.images.i_wlogo.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$wlogo name="i_wlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ĞÂ´°¿Ú°´Å¥Í¼±ê</font>¡¡(´óĞ¡£º74*21)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="nwlogo" value="$nwlogo" onblur="document.images.i_nwlogo.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$nwlogo name="i_nwlogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>°ïÖú°´Å¥Í¼±ê</font>¡¡(´óĞ¡£º²»ÏŞ)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="help_blogo" value="$help_blogo" onblur="document.images.i_help_blogo.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$help_blogo name="i_help_blogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ĞÂÌù×îºóµÄ new Í¼±ê</font>¡¡(´óĞ¡£º²»ÏŞ)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="new_blogo" value="$new_blogo" onblur="document.images.i_new_blogo.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$new_blogo name="i_new_blogo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>×Ô¼ºÊÇ·¢ÌûÈËµÄ±ê¼ÇÍ¼Ê¾</font>¡¡(´óĞ¡£º²»ÏŞ)</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="mypost_blogo" value="$mypost_blogo" onblur="document.images.i_new_mypost.src='$imagesurl/images/$skin/'+this.value;">¡¡
                <img src=$imagesurl/images/$skin/$mypost_blogo name="i_new_mypost"></td>
                </tr>
				
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>¾«»ªÌû×ÓµÄ±ê¼ÇÍ¼Ê¾</font>  (´óĞ¡£º²»ÏŞ)</td> 
               <td bgcolor=#FFFFFF> 
               <input type=text name="new_JH" value="$new_JH" onblur="document.images.i_new_JH.src='$imagesurl/images/$skin/'+this.value;">¡¡
               <img src=$imagesurl/images/$skin/$new_JH name="i_new_JH"></td> 
               </tr> 


                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>ÂÛÌ³ÌØÊâÑùÊ½ÉèÖÃ</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×ÓÎÄ×ÖÏÔÊ¾´óĞ¡</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = qq~<select name=postfontsize><option value="12">Ä¬ÈÏ</option><option value="15">ÉÔ´ó</option><option value="18">ÆÕÍ¨</option><option value="21">½Ï´ó</option><option value="24">ºÜ´ó</option><option value="30">×î´ó</option></select>~;
                $tempoutput =~ s/value=\"$postfontsize\"/value=\"$postfontsize\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×Ó¶ÎÂä¼ä¾àµ÷Õû</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"paraspace\">\n<option value=\"130\">Ä¬ÈÏ¼ä¾à<option value=\"100\">µ¥±¶ĞĞ¾à<option value=\"150\">1.5±¶ĞĞ¾à<option value=\"200\">Ë«±¶ĞĞ¾à";
                $tempoutput =~ s/value=\"$paraspace\"/value=\"$paraspace\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìù×Ó×Ö¼ä¾àµ÷Õû</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"wordspace\">\n<option value=\"0\">Ä¬ÈÏ¼ä¾à<option value=\"-1\">½ôËõ<option value=\"+2\">À©³ä<option value=\"+4\">¼Ó¿í";
                $wordspace =~ s/\+/\\+/;
                $tempoutput =~ s/value=\"$wordspace\"/value=\"$wordspace\" selected/;
                print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>»Ø¸´Ê±ºòÄ¬ÈÏÁĞ³öµÄ×îºó»Ø¸´¸öÊı</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxlistpost" value="$maxlistpost" size=2 maxlength=2>¡¡Ò»°ã 5 -- 8 ¸ö×óÓÒÀ²</td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"dispabstop\">\n<option value=\"1\">ÏÔÊ¾\n<option value=\"0\">²»ÏÔÊ¾\n</select>\n"; 
               $tempoutput =~ s/value=\"$dispabstop\"/value=\"$dispabstop\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=ËÎÌå color=#333333><b>ÊÇ·ñÔÊĞíÏÔÊ¾×Ü¹Ì¶¥£¿</b></font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr> 
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>¿ÉÒÔÉè¶¨×Ü¹Ì¶¨Ìù×ÓµÄÖ÷ÌâÑÕÉ«!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_absontop" value="$color_of_absontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_absontop)" style="cursor:hand;background-color:$color_of_absontop">¡¡ÍÆ¼öÑ¡Ôñ#990000</td>
              </tr>
		~;

               $tempoutput = "<select name=\"abstopshake\">\n<option value=\"\">²»²ÉÓÃÈÎºÎ·½Ê½\n<option value=\"1\">»Î¶¯\n<option value=\"2\">±äÉ«\n<option value=\"3\">·´É«\n</select>\n"; 
               $tempoutput =~ s/value=\"$abstopshake\"/value=\"$abstopshake\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>×Ü¹Ì¶¨Ìù×Ó²ÉÓÃÊ²Ã´ĞÑÄ¿·½Ê½£¿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
		~;
               
               $tempoutput = "<select name=\"dispcattop\">\n<option value=\"1\">ÏÔÊ¾\n<option value=\"0\">²»ÏÔÊ¾\n</select>\n"; 
               $tempoutput =~ s/value=\"$dispcattop\"/value=\"$dispcattop\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=ËÎÌå color=#333333><b>ÊÇ·ñÔÊĞíÏÔÊ¾Çø¹Ì¶¥£¿</b></font></td> 
               <td bgcolor=#FFFFFF valign=middle align=left> 
               $tempoutput</td> 
               </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>¿ÉÒÔÉè¶¨Çø¹Ì¶¨Ìù×ÓµÄÖ÷ÌâÑÕÉ«!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_quontop" value="$color_of_quontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_quontop)" style="cursor:hand;background-color:$color_of_quontop">¡¡ÍÆ¼öÑ¡Ôñ#e7840d</td>
              </tr>
		~;

               $tempoutput = "<select name=\"cattopshake\">\n<option value=\"\">²»²ÉÓÃÈÎºÎ·½Ê½\n<option value=\"1\">»Î¶¯\n<option value=\"2\">±äÉ«\n<option value=\"3\">·´É«\n</select>\n"; 
               $tempoutput =~ s/value=\"$cattopshake\"/value=\"$cattopshake\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>Çø¹Ì¶¨Ìù×Ó²ÉÓÃÊ²Ã´ĞÑÄ¿·½Ê½£¿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÔÊĞí¹Ì¶¨ÔÚ¶¥¶ËµÄÖ÷ÌâÊı£¿</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtoptopic" value="$maxtoptopic" size=2 maxlength=2>¡¡Ò»°ã 1 -- 5 ¸ö×óÓÒÀ²</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>¿ÉÒÔÉè¶¨¹Ì¶¨Ìù×ÓµÄÖ÷ÌâÑÕÉ«!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_ontop" value="$color_of_ontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_ontop)" style="cursor:hand;background-color:$color_of_ontop">¡¡ÍÆ¼öÑ¡Ôñ#002299</td>
              </tr>
		~;

               $tempoutput = "<select name=\"topshake\">\n<option value=\"\">²»²ÉÓÃÈÎºÎ·½Ê½\n<option value=\"1\">»Î¶¯\n<option value=\"2\">±äÉ«\n<option value=\"3\">·´É«\n</select>\n"; 
               $tempoutput =~ s/value=\"$topshake\"/value=\"$topshake\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>¹Ì¶¨Ìù×Ó²ÉÓÃÊ²Ã´ĞÑÄ¿·½Ê½£¿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÔÊĞí¼ÓÖØÌû×Ó±êÌâµÄÖ÷ÌâÊı£¿<br>¿ÉÒÔ¼ÓÖØ¼¸¸öÖØÒªÌû×ÓµÄ±êÌâ¡£</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxhightopic" value="$maxhightopic" size=2 maxlength=2>¡¡Ò»°ã 10 -- 20 ¸ö×óÓÒÀ²</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>¿ÉÒÔÉè¶¨¼ÓÖØÌû×ÓµÄ±êÌâÑÕÉ«!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_hightopic" value="$color_of_hightopic" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_hightopic)" style="cursor:hand;background-color:$color_of_hightopic">¡¡ÍÆ¼öÑ¡Ôñ#990000</td>
              </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÂÛÌ³Í¶Æ±Ìù×ÓÖĞÔÊĞíµÄ×î´óÏîÄ¿Êı</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpollitem" value="$maxpollitem" size=2 maxlength=2>¡¡ÇëÉèÖÃ 5 - 50 Ö®¼ä</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"emoticons\">\n<option value=\"off\">²»Ê¹ÓÃ\n<option value=\"on\">Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$emoticons\"/value=\"$emoticons\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃ±íÇé×Ö·û×ª»»£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"canchgfont\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$canchgfont\"/value=\"$canchgfont\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃÎÄ×Ö×ÖÌå×ª»»£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>¹ã¸æÉèÖÃ</center></b><br>
                </td></tr>
		~;
	$adscript   =~ s/\[br\]/\n/isg;
	$adfoot   =~ s/\[br\]/\n/isg;

               $tempoutput = "<select name=\"useadscript\">\n<option value=\"0\">²»Ê¹ÓÃ\n<option value=\"1\">Ê¹ÓÃ\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadscript\"/value=\"$useadscript\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃÂÛÌ³¹ã¸æ</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                    
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³¹ã¸æÊéĞ´</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adscript" rows="5" cols="40">$adscript</textarea>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"useadfoot\">\n<option value=\"0\">²»Ê¹ÓÃ\n<option value=\"1\">Ê¹ÓÃ\n</select>\n"; 
               $tempoutput =~ s/value=\"$useadfoot\"/value=\"$useadfoot\" selected/; 
               print qq~ 
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃÂÛÌ³Î²²¿´úÂë</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³Î²²¿´úÂëÊéĞ´</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="adfoot" rows="5" cols="40">$adfoot</textarea><BR><BR>
                </td>
                </tr>
		~;
               
               $tempoutput = "<select name=\"forumimagead\">\n<option value=\"0\">²»Ê¹ÓÃ\n<option value=\"1\">Ê¹ÓÃ\n</select>\n";
               $tempoutput =~ s/value=\"$forumimagead\"/value=\"$forumimagead\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃ·ÖÂÛÌ³¸¡¶¯¹ã¸æ</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³¸¡¶¯¹ã¸æÍ¼Æ¬ URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage" value="$adimage"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³¸¡¶¯¹ã¸æÁ¬½ÓÄ¿±êÍøÖ·</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink" value="$adimagelink"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³¸¡¶¯¹ã¸æÍ¼Æ¬¿í¶È</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth" value="$adimagewidth" maxlength=3>&nbsp;ÏñËØ</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³¸¡¶¯¹ã¸æÍ¼Æ¬¸ß¶È</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight" value="$adimageheight" maxlength=3>&nbsp;ÏñËØ</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"useimageadtopic\">\n<option value=\"0\">²»Ê¹ÓÃ\n<option value=\"1\">Ê¹ÓÃ\n</select>\n";
               $tempoutput =~ s/value=\"$useimageadtopic\"/value=\"$useimageadtopic\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=ËÎÌå color=#333333><b>²é¿´´Ë·ÖÂÛÌ³µÄÌù×ÓÊ±ÊÇ·ñ<BR>Ê¹ÓÃ´Ë¸¡¶¯¹ã¸æ</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutputÈç¹ûÉÏÃæÉèÖÃÁË<BR>·ÖÂÛÌ³²»Ê¹ÓÃ¸¡¶¯¹ã¸æµÄ»°£¬´ËÑ¡ÏîÎŞĞ§<BR><BR></td>
               </tr>
		~;
        
               $tempoutput = "<select name=\"forumimagead1\">\n<option value=\"0\">²»Ê¹ÓÃ\n<option value=\"1\">Ê¹ÓÃ\n</select>\n";
               $tempoutput =~ s/value=\"$forumimagead1\"/value=\"$forumimagead1\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=ËÎÌå color=#333333><b>ÊÇ·ñÊ¹ÓÃ·ÖÂÛÌ³ÓÒÏÂ¹Ì¶¨¹ã¸æ</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³ÓÒÏÂ¹Ì¶¨¹ã¸æÍ¼Æ¬ URL</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimage1" value="$adimage1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³ÓÒÏÂ¹Ì¶¨¹ã¸æÁ¬½ÓÄ¿±êÍøÖ·</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="adimagelink1" value="$adimagelink1"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³ÓÒÏÂ¹Ì¶¨¹ã¸æÍ¼Æ¬¿í¶È</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimagewidth1" value="$adimagewidth1" maxlength=3>&nbsp;ÏñËØ</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³ÓÒÏÂ¹Ì¶¨¹ã¸æÍ¼Æ¬¸ß¶È</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=3 name="adimageheight1" value="$adimageheight1" maxlength=3>&nbsp;ÏñËØ</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"useimageadtopic1\">\n<option value=\"0\">²»Ê¹ÓÃ\n<option value=\"1\">Ê¹ÓÃ\n</select>\n";
               $tempoutput =~ s/value=\"$useimageadtopic1\"/value=\"$useimageadtopic1\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=ËÎÌå color=#333333><b>²é¿´´Ë·ÖÂÛÌ³µÄÌù×ÓÊ±ÊÇ·ñ<BR>Ê¹ÓÃ´ËÓÒÏÂ¹Ì¶¨¹ã¸æ</b></font></td>
               <td bgcolor=#FFFFFF>
               $tempoutputÈç¹ûÉÏÃæÉèÖÃÁË<BR>·ÖÂÛÌ³²»Ê¹ÓÃÓÒÏÂ¹Ì¶¨¹ã¸æµÄ»°£¬´ËÑ¡ÏîÎŞĞ§</td>
               </tr>

		<tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>¿´Ìù¹ã¸æÇø</b><br>ÓÃ HTML Óï·¨ÊéĞ´£¡</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="topicad" cols="40" rows="10">$topicad</textarea><BR>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>Ìû×ÓÖ÷Ìâ¹ã¸æÊéĞ´(Èç¹ûÃ»ÓĞ£¬ÇëÁô¿Õ)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="maintopicad" rows="5" cols="40">$maintopicad</textarea>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>Ìû×Ó»Ø¸´¹ã¸æÊéĞ´(Èç¹ûÃ»ÓĞ£¬ÇëÁô¿Õ)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="replytopicad" rows="5" cols="40">$replytopicad</textarea>
                </td>
                </tr>


<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><center><b>³õÊ¼»¯ÌØĞ§ÉèÖÃ</b> (leobbs.cgi & Forums.cgi)</center><br>
</font></td>
</tr>
~;


$tempoutput = "<select name=\"pagechange\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
$tempoutput =~ s/value=\"$pagechange\"/value=\"$pagechange\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>µ÷ÈëÒ³ÃæÊ±ÊÇ·ñÊ¹ÓÃÌØĞ§?</b><br>IE 4.0 ÒÔÉÏ°æ±¾ä¯ÀÀÆ÷ÓĞĞ§</font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

$tempoutput = "<select name=\"cinoption\">\n
<option value=\"0\">ºĞ×´ÊÕËõ\n
<option value=\"1\">ºĞ×´·ÅÉä\n
<option value=\"2\">Ô²ĞÎÊÕËõ\n
<option value=\"3\">Ô²ĞÎ·ÅÉä\n
<option value=\"4\">ÏòÉÏ²Á³ı\n
<option value=\"5\">ÏòÏÂ²Á³ı\n
<option value=\"6\">ÏòÓÒ²Á³ı\n
<option value=\"7\">Ïò×ó²Á³ı\n
<option value=\"8\">´¹Ö±ÕÚ±Î\n
<option value=\"9\">Ë®Æ½ÕÚ±Î\n
<option value=\"10\">ºáÏòÆåÅÌÊ½\n
<option value=\"11\">×İÏòÆåÅÌÊ½\n
<option value=\"12\">Ëæ»ú·Ö½â\n
<option value=\"13\">×óÓÒÏòÖĞÑëËõ½ø\n
<option value=\"14\">ÖĞÑëÏò×óÓÒÀ©Õ¹\n
<option value=\"15\">ÉÏÏÂÏòÖĞÑëËõ½ø\n
<option value=\"16\">ÖĞÑëÏòÉÏÏÂÀ©Õ¹\n
<option value=\"17\">´Ó×óÏÂ³é³ö\n
<option value=\"18\">´Ó×óÉÏ³é³ö\n
<option value=\"29\">´ÓÓÒÏÂ³é³ö\n
<option value=\"20\">´ÓÓÒÉÏ³é³ö\n
<option value=\"21\">Ëæ»úË®Æ½ÏßÌõ\n
<option value=\"22\">Ëæ»ú´¹Ö±ÏßÌõ\n
<option value=\"23\">Ëæ»ú(ÉÏÃæÈÎºÎÒ»ÖÖ)\n
</select>\n";
$tempoutput =~ s/value=\"$cinoption\"/value=\"$cinoption\" selected/;
print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>ÌØĞ§ÀàĞÍ?</b></font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

	print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>ÆäËûÉèÖÃ</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>°æÈ¨ĞÅÏ¢</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="copyrightinfo" value="$copyrightinfo"></td>
                </tr>
                 ~;

                $tempoutput = "<select name=\"floodcontrol\"><option value=\"off\">·ñ<option value=\"on\">ÊÇ</select>\n";
                $tempoutput =~ s/value=\"$floodcontrol\"/value=\"$floodcontrol\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ÊÇ·ñ¹àË®Ô¤·À»úÖÆ£¿</b><br>Ç¿ÁÒÍÆ¼öÊ¹ÓÃ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ÓÃ»§·¢ÌùµÄÏà¸ôÊ±¼ä</b><br>¹àË®Ô¤·À»úÖÆ²»»áÓ°Ïìµ½Ì³Ö÷»ò°æÖ÷</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="floodcontrollimit" value="$floodcontrollimit" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333>¶àÉÙĞ¡Ê±ÄÚµÄĞÂÌùºóÃæ¼Ó new ±êÖ¾£¿<BR>(Èç¹û²»ÏëÒª£¬¿ÉÒÔÉèÖÃÎª 0)</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newmarktime" value="$newmarktime" size=3 maxlength=3>¡¡Ò»°ã 12 - 24 Ğ¡Ê±</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"usetodayforumreply\">\n<option value=\"yes\">ÊÇµÄ£¬¼ÇÂ¼\n<option value=\"no\">²»£¬²»¼ÇÂ¼\n</select>\n";
                $tempoutput =~ s/value=\"$usetodayforumreply\"/value=\"$usetodayforumreply\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>·ÖÂÛÌ³µÄ½ñÈÕĞÂÌùÍ³¼ÆÊÇ·ñ°Ñ»Ø¸´Ò²¼ÇÂ¼ÉÏ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"usejhpoint\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n"; 
               $tempoutput =~ s/value=\"$usejhpoint\"/value=\"$usejhpoint\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>ÊÇ·ñÊ¹ÓÃÔÚ¾«»ªÌû×ÓÊ¹ÓÃ±ê¼Ç£¿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
               ~; 

		$tempoutput = "<select name=\"nodispown\">\n<option value=\"no\">²»ÏÔÊ¾\n<option value=\"yes\">ÏÔÊ¾\n</select>\n"; 
               $tempoutput =~ s/value=\"$nodispown\"/value=\"$nodispown\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>ÊÇ·ñ±êÖ¾ÏÔÊ¾×Ô¼º·¢µÄÌû×Ó£¿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
               ~; 

		$tempoutput = "<select name=\"canuseview\">\n<option value=\"yes\">ÔÊĞí\n<option value=\"no\">²»ÔÊĞí\n</select>\n"; 
               $tempoutput =~ s/value=\"$canuseview\"/value=\"$canuseview\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>ÂÛÌ³ÊÇ·ñÔÊĞíĞÂÎÅ·½Ê½¿ìËÙÔÄ¶Á£¿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
               ~; 

		$tempoutput = "<select name=\"canusetreeview\">\n<option value=\"yes\">ÔÊĞí\n<option value=\"no\">²»ÔÊĞí\n</select>\n"; 
               $tempoutput =~ s/value=\"$canusetreeview\"/value=\"$canusetreeview\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>ÂÛÌ³ÊÇ·ñÔÊĞíÊ¹ÓÃ¿ìËÙÕ¹¿ª»Ø¸´£¿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

               $tempoutput = "<select name=\"useads\">\n<option value=\"no\">²»ÔÊĞí\n<option value=\"yes\">ÔÊĞí\n</select>\n"; 
               $tempoutput =~ s/value=\"$useads\"/value=\"$useads\" selected/; 
               print qq~ 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>ÊÇ·ñÔÊĞíÂÛÌ³Ìû×ÓËæ»ú¹ã¸æ£¿</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
		~;
		
                $tempoutput = "<select name=\"look\">\n<option value=\"on\">¿ª·Å\n<option value=\"off\">²»¿ª·Å\n</select>\n";
                $tempoutput =~ s/value=\"$look\"/value=\"$look\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÊÇ·ñ¿ª·Å±¾°æÅäÉ«¹¦ÄÜ£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"wwjf\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$wwjf\"/value=\"$wwjf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³ÊÇ·ñÊ¹ÓÃÍşÍûÏŞÖÆÖÆ¶È</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;
                $tempoutput = "<select name=\"cansale\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$cansale\"/value=\"$cansale\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>·ÖÂÛÌ³ÊÇ·ñÊ¹ÓÃÌû×ÓÂòÂôÖÆ¶È</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=ËÎÌå color=#333333><b>Ìû×ÓÂòÂô½»ÄÉË°ÂÊ</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="postcess" value="$postcess" size=5 maxlength=5> %  : ±ØĞëÊÇ 1 - 100 Ö®¼ä£¬²»ÏëÊ¹ÓÃÔòÉèÖÃ¿Õ°×</td>
               </tr>
		~;
		
		$tempoutput = "<select name=\"postjf\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$postjf\"/value=\"$postjf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÊÇ·ñÊ¹ÓÃ·¢ÌûÁ¿±êÇ©</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"jfmark\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$jfmark\"/value=\"$jfmark\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÊÇ·ñÊ¹ÓÃ»ı·Ö²é¿´±êÇ©</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"noviewjf\">\n<option value=\"no\">¿ÉÒÔ½øÈë£¬µ«ÎŞ·¨¿´±£ÃÜµÄÄÚÈİ\n<option value=\"yes\">ÎŞ·¨½øÈë¸ÃÌû\n</select>\n";
                $tempoutput =~ s/value=\"$noviewjf\"/value=\"$noviewjf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>µ±Ö÷Ìûº¬ÓĞ»ı·Ö±êÇ©£¬ÄÇÃ´´ï²»µ½»ı·ÖÒªÇóµÄ»áÔ±£®£®£¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"hidejf\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$hidejf\"/value=\"$hidejf\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÊÇ·ñÊ¹ÓÃ±£ÃÜÌû×Ó±êÇ©</b>£¨»Ø¸´ºó²ÅÄÜ¿´µ½Ìû×ÓÄÚÈİ£©</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>

               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=ËÎÌå color=#333333><b>Ò»´Î½±³Í»ı·Ö×î´óÊıÁ¿</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="max1jf" value="$max1jf" size=3 maxlength=3> Ä¬ÈÏ£º 50</td>
               </tr>
		~;
		
		$tempoutput = "<select name=\"usewm\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$usewm\"/value=\"$usewm\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÊÇ·ñÊ¹ÓÃ×Ô¶¯Ë®Ó¡</b>£¨Ìû×Ó±êÌâº¬Ô­´´×ÖÑùÊ±×Ô¶¯¼ÓË®Ó¡£©</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

		$tempoutput = "<select name=\"usecurl\">\n<option value=\"yes\">ÔÊĞí\n<option value=\"no\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$usecurl\"/value=\"$usecurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÊÇ·ñÔÊĞíÊ¹ÓÃ¼ÓÃÜÁ´½Ó</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"magicface\">\n<option value=\"on\">ÔÊĞí\n<option value=\"off\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$magicface\"/value=\"$magicface\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÊÇ·ñÔÊĞíÊ¹ÓÃÄ§·¨±íÇé¹¦ÄÜ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

       		$tempoutput = "<select name=\"announcemove\">\n<option value=\"on\">ÒÆ¶¯\n<option value=\"off\">²»ÒÆ¶¯\n</select>\n";
               	$tempoutput =~ s/value=\"$announcemove\"/value=\"$announcemove\" selected/;
               	print qq~

               	<tr>
               	<td bgcolor=#FFFFFF colspan=2>
               	<font color=#333333>ÂÛÌ³¹«¸æÊÇ·ñ²ÉÓÃÒÆ¶¯·ç¸ñ£¿</font></td>
               	<td bgcolor=#FFFFFF>
               	$tempoutput</td>
               	</tr>
               	~;

                $tempoutput = "<select name=\"announcements\"><option value=\"no\">²»Ê¹ÓÃ<option value=\"yes\">Ê¹ÓÃ</select>\n";
                $tempoutput =~ s/value=\"$announcements\"/value=\"$announcements\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>ÊÇ·ñÊ¹ÓÃ¹«¸æÂÛÌ³</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
                </td>
                </tr>
                ~;

		$tempoutput = "<select name=\"refreshurl\"><option value=\"0\">×Ô¶¯·µ»Øµ±Ç°ÂÛÌ³<option value=\"1\">×Ô¶¯·µ»Øµ±Ç°Ìù×Ó</select>\n";
                $tempoutput =~ s/value=\"$refreshurl\"/value=\"$refreshurl\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>·¢±í¡¢»Ø¸´¡¢±à¼­Ìù×Óºó×Ô¶¯×ªÒÆµ½£¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"payopen\"><option value=\"no\">²»ÔÊĞíÖ§¸¶±¦½»Ò×Ìû<option value=\"yes\">¿ÉÒÔÖ§¸¶±¦½»Ò×Ìû</select>\n";
                $tempoutput =~ s/value=\"$payopen\"/value=\"$payopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>´ò¿ªÂÛÌ³Ö§¸¶±¦½»Ò×Ìû¹¦ÄÜ£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"postopen\"><option value=\"yes\">¿ÉÒÔ·¢±í»ò»Ø¸´Ö÷Ìâ<option value=\"no\">²»ÔÊĞí·¢±í»ò»Ø¸´Ö÷Ìâ</select>\n";
                $tempoutput =~ s/value=\"$postopen\"/value=\"$postopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>´ò¿ªÂÛÌ³·¢±í»ò»Ø¸´Ö÷Ìâ¹¦ÄÜ£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pollopen\"><option value=\"yes\">´ò¿ªÍ¶Æ±<option value=\"no\">¹Ø±ÕÍ¶Æ±</select>\n";
                $tempoutput =~ s/value=\"$pollopen\"/value=\"$pollopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>´ò¿ªÂÛÌ³Í¶Æ±¹¦ÄÜ£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"xzbopen\"><option value=\"yes\">´ò¿ªĞ¡×Ö±¨<option value=\"no\">¹Ø±ÕĞ¡×Ö±¨</select>\n";
                $tempoutput =~ s/value=\"$xzbopen\"/value=\"$xzbopen\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>´ò¿ªÂÛÌ³Ğ¡×Ö±¨¹¦ÄÜ£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÔÊĞí·¢±íµÄĞ¡×Ö±¨µÄ×î¶à×ÖÊı</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hownews" value="$hownews" size=4 maxlength=4>¡¡Ä¬ÈÏ£º100</td>
                </tr>
                <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333><B>³¬¹ı¶àÉÙÌìµÄÌû×Ó²»ÔÊĞí»Ø¸´£¿</B></font><BR>ÒÔÌû×Ó×îºóÒ»´Î»Ø¸´Ê±¼ä¼ÆËã</td>
               <td bgcolor=#FFFFFF>
               <input type=text name="rdays" value="$rdays" size=4 maxlength=4>¡¡Ìì (Èç¹ûÎŞĞè£¬ÇëÁô¿Õ)</td>
               </tr>
               ~;

                $tempoutput = "<select name=\"useemote\"><option value=\"yes\">Ê¹ÓÃ<option value=\"no\">²»Ê¹ÓÃ</select>\n";
                $tempoutput =~ s/value=\"$useemote\"/value=\"$useemote\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÊÇ·ñÊ¹ÓÃ EMOTE ±êÇ©£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"regaccess\"><option value=\"off\">²»£¬ÔÊĞíÈÎºÎÈË·ÃÎÊ<option value=\"on\">ÊÇ£¬±ØĞëµÇÂ¼ºó²ÅÄÜ·ÃÎÊ</select>\n";
                $tempoutput =~ s/value=\"$regaccess\"/value=\"$regaccess\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÂÛÌ³Ö»ÓĞ×¢²áÓÃ»§¿ÉÒÔ·ÃÎÊ£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"guestregistered\"><option value=\"on\">¿ÉÒÔ<option value=\"off\">²»ÄÜ</select>\n";
		$tempoutput =~ s/value=\"$guestregistered\"/value=\"$guestregistered\" selected/;
		print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
		<font face=ËÎÌå color=#333333>¿ÍÈËÄÜ·ñ²é¿´Ìù×ÓÄÚÈİ£¿</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>
		~;
		
                $tempoutput = "<select name=\"viewadminlog\">\n<option value=\"0\">ÔÊĞíÈÎºÎÈË²é¿´\n<option value=\"1\">Ö»ÔÊĞí×¢²á»áÔ±ÒÔÉÏ¼¶±ğ²é¿´\n<option value=\"2\">Ö»ÔÊĞíÈÏÖ¤»áÔ±ÒÔÉÏ¼¶±ğ²é¿´<option value=\"3\">Ö»ÔÊĞí°æÖ÷ÒÔÉÏ¼¶±ğ²é¿´</select>\n";
                $tempoutput =~ s/value=\"$viewadminlog\"/value=\"$viewadminlog\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>°æÎñÈÕÖ¾¹¦ÄÜ¿ª·Å·½Ê½</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"arrowuserdel\">\n<option value=\"on\">ÔÊĞí\n<option value=\"off\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$arrowuserdel\"/value=\"$arrowuserdel\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÊÇ·ñÔÊĞí×¢²áÓÃ»§×Ô¼ºÉ¾³ı×Ô¼ºµÄÌù×Ó£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"usereditpost\"><option value=\"yes\">¿ÉÒÔ±à¼­×Ô¼ºµÄÌù×Ó<option value=\"no\">²»¿ÉÒÔ±à¼­×Ô¼ºµÄÌù×Ó</select>\n";
                $tempoutput =~ s/value=\"$usereditpost\"/value=\"$usereditpost\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÂÛÌ³ÊÇ·ñÔÊĞí±à¼­£¿(¶ÔÌ³Ö÷¡¢°ßÖñÎŞĞ§)</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"allowamoedit\">\n<option value=\"no\">²»ÔÊĞí\n<option value=\"yes\">ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$allowamoedit\"/value=\"$allowamoedit\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>¸±°æÖ÷ÊÇ·ñÔÊĞí±à¼­±¾ÂÛÌ³ÏÂµÄÌû×Ó£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

		$tempoutput = "<select name=\"newmsgpop\"><option value=\"off\">²»ÌáÊ¾<option value=\"popup\">µ¯³ö<option value=\"light\">ÉÁË¸<option value=\"on\">Á½Õß¾ùÒª</select>\n";
                $tempoutput =~ s/value=\"$newmsgpop\"/value=\"$newmsgpop\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÓĞĞÂµÄ¶ÌÏûÏ¢²ÉÓÃºÎÖÖÌáÊ¾£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"pvtip\">\n<option value=\"on\">ÏÔÊ¾ IP ºÍ¼ø¶¨\n<option value=\"off\">±£ÃÜ IP ºÍ¼ø¶¨\n</select>\n";
                $tempoutput =~ s/value=\"$pvtip\"/value=\"$pvtip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>ÊÇ·ñ±£ÃÜ IP ºÍ¼ø¶¨£¿</b><BR>¼´Ê¹Ñ¡ÔñµÄÊÇÏÔÊ¾ IP£¬µ«ÆÕÍ¨ÓÃ»§»¹ÊÇ<BR>Ö»ÄÜ¿´¼û IP µÄÇ°Á½Î»</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput¡¡´Ë¹¦ÄÜ¶ÔÌ³Ö÷ÎŞĞ§</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"smocanseeip\">\n<option value=\"yes\">ÓĞĞ§\n<option value=\"no\">ÎŞĞ§\n</select>\n";
                $tempoutput =~ s/value=\"$smocanseeip\"/value=\"$smocanseeip\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>±£ÃÜ IP ºÍ¼ø¶¨¶Ô×Ü°ßÖñÊÇ·ñÓĞĞ§£¿</b><BR>ÈçÑ¡ÔñÎŞĞ§£¬Ôò×Ü°æÖ÷¿É²é¿´ËùÓĞµÄ IP<BR>¶ø²»ÊÜÉÏÃæ IP ±£ÃÜµÄÏŞÖÆ</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>Ö§³ÖÉÏ´«µÄ¸½¼şÀàĞÍ</b><br>ÓÃ,·Ö¸î</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=40 name="addtype" value="$addtype"></td>
                </tr>
		~;

                $tempoutput = "<select name=\"arrowupload\">\n<option value=\"on\">ÔÊĞí\n<option value=\"off\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$arrowupload\"/value=\"$arrowupload\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ö÷ÌâÌù×ÓÊÇ·ñÔÊĞíÉÏ´«£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput¡¡´Ë¹¦ÄÜ¶Ô°æÖ÷ºÍÌ³Ö÷ÎŞĞ§</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"allowattachment\">\n<option value=\"yes\">ÔÊĞí\n<option value=\"no\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$allowattachment\"/value=\"$allowattachment\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>»Ø¸´Ìù×ÓÊÇ·ñÔÊĞíÉÏ´«£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput¡¡´Ë¹¦ÄÜ¶Ô°æÖ÷ºÍÌ³Ö÷ÎŞĞ§</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÂÛÌ³ÉÏ´«ÎÄ¼şÔÊĞíµÄ×î´óÖµ(µ¥Î»£ºKB)<br>Èç¹ûÉèÖÃÁË²»ÔÊĞíÉÏ´«£¬Ôò´ËÏîÎŞĞ§£¡</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxupload" value="$maxupload" size=5 maxlength=5>¡¡²»Òª¼Ó KB ×ÖÑù£¬½¨Òé²»Òª³¬¹ı 500 £¡</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÓÃ»§ÉÏ´«ÎÄ¼ş±ØĞë´ïµ½µÄ·¢Ìù×ÜÊı<br>Ö»¶ÔÆÕÍ¨×¢²áÓÃ»§ÓĞĞ§£¡Ì³Ö÷¡¢°ßÖñºÍÈÏÖ¤ÓÃ»§¶¼²»ÊÜ´ËÏŞÖÆ£¡</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="uploadreqire" value="$uploadreqire" size=4 maxlength=4>¡¡Èç¹û²»ÏëÏŞÖÆ£¬¿ÉÒÔÉèÖÃÎª0¡£</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"addtopictime\">\n<option value=\"no\">²»Ìí¼Ó\n<option value=\"yes\">Ìí¼Ó\n</select>\n";
                $tempoutput =~ s/value=\"$addtopictime\"/value=\"$addtopictime\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñ×Ô¶¯ÔÚÖ÷ÌâÇ°Ìí¼ÓÈÕÆÚ£¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"abslink\">\n<option value=\"no\">²»Ö±½ÓÏÂÔØ\n<option value=\"yes\">Ö±½ÓÏÂÔØ\n</select>\n";
                $tempoutput =~ s/value=\"$abslink\"/value=\"$abslink\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>Í¼Æ¬¸½¼şÊÇ·ñÊ¹ÓÃÖ±½ÓÏÂÔØ·½Ê½£¿</b>´ËÉèÖÃÖ»Õë¶ÔÍ¼Æ¬£¬Èç¹ûÑ¡Ôñ¡°Ö±½ÓÏÂÔØ¡±£¬ÄÇÃ´·ÀµÁÁ´ºÍÍ¼Æ¬Ë®Ó¡ÉèÖÃ½«ÎŞĞ§£¡</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"pvtdown\">\n<option value=\"yes\">±£»¤\n<option value=\"no\">²»±£»¤\n</select>\n";
                $tempoutput =~ s/value=\"$pvtdown\"/value=\"$pvtdown\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñ±£»¤¸½¼şÏÂÔØµØÖ·£¬·ÀÖ¹µÁÁ´£¿</b></font></td>
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

		$tempoutput = "<select name=\"picwater\">\n<option value=\"no\">²»¼ÓË®Ó¡\n<option value=\"yes\">¼ÓÉÏË®Ó¡\n</select>\n";
                $tempoutput =~ s/value=\"$picwater\"/value=\"$picwater\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÉÏ´«µÄ JPG Í¼Æ¬ÊÇ·ñ¼ÓÉÏË®Ó¡</b><BR>Ğ¡ÓÚ 200*40 µÄÍ¼Æ¬×Ô¶¯²»¼ÓË®Ó¡</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

$watername = "http://bbs.leobbs.com/" if ($watername eq "");

		$tempoutput = "<select name=\"picwaterman\">\n<option value=\"0\">Ö»¶Ô¿ÍÈËÏÔÊ¾\n<option value=\"1\">¶Ô¿ÍÈËºÍÆÕÍ¨ÓÃ»§ÏÔÊ¾\n<option value=\"2\">¶Ô¿ÍÈË¡¢ÆÕÍ¨ÓÃ»§ºÍÈÏÖ¤ÓÃ»§ÏÔÊ¾<option value=\"3\">³ıÁËÌ³Ö÷Íâ£¬ÆäËûÓÃ»§¶¼ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$picwaterman\"/value=\"$picwaterman\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÏÔÊ¾Ë®Ó¡¶ÔÏóµÄ¸½¼ÓÉèÖÃ</b><BR>Ö»ÓĞ´ò¿ªË®Ó¡¹¦ÄÜºó£¬´ËÏîÄ¿²ÅÓĞĞ§</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
                if ($picwaterplace1 eq "yes") { $checked1 = "checked" ; } else { $checked1 = "" ; }
                if ($picwaterplace2 eq "yes") { $checked2 = "checked" ; } else { $checked2 = "" ; }
                if ($picwaterplace3 eq "yes") { $checked3 = "checked" ; } else { $checked3 = "" ; }
                if ($picwaterplace4 eq "yes") { $checked4 = "checked" ; } else { $checked4 = "" ; }
		$tempoutput = qq~<input type="checkbox" name="picwaterplace1" value="yes" $checked1> ×óÉÏ½Ç¡¡¡¡<input type="checkbox" name="picwaterplace2" value="yes" $checked2> ×óÏÂ½Ç<BR><input type="checkbox" name="picwaterplace3" value="yes" $checked3> ÓÒÉÏ½Ç¡¡¡¡<input type="checkbox" name="picwaterplace4" value="yes" $checked4> ÓÒÏÂ½Ç<BR>~;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>Ë®Ó¡ÏÔÊ¾µÄÎ»ÖÃ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÉÏ´«µÄ JPG Í¼Æ¬ÉÏË®Ó¡µÄÎÄ×Ö<BR>×¢£º<font color=red>²»ÄÜÓÃÖĞÎÄ</font>£¬Ò²²»Òª¹ı³¤£¬·ñÔòÓ°ÏìĞ§¹û</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="watername" value="$watername" size=30></td>
                </tr>
		~;
} else {
	print qq~<input type=hidden name="picwater" value="no">~;
}

                $tempoutput = "<select name=\"mastpostatt\">\n<option value=\"no\">¿ÉÒÔ²»´ø¸½¼ş\n<option value=\"yes\">±ØĞë´ø¸½¼ş\n</select>\n";
                $tempoutput =~ s/value=\"$mastpostatt\"/value=\"$mastpostatt\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ĞÂÖ÷ÌâÌùÊÇ·ñ±ØĞë´ø¸½¼ş£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput¡¡´Ë¹¦ÄÜÖ÷ÒªÓÃÓÚÖÆ×÷ BT ·¢²¼Çø</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>·¢ÌùÖÁÉÙ×Ö·ûÊı£¬·ÀÖ¹¹àË®<br>Ö»¶ÔÆÕÍ¨×¢²áÓÃ»§ÓĞĞ§£¡Ì³Ö÷¡¢°ßÖñºÍÈÏÖ¤ÓÃ»§¶¼²»ÊÜ´ËÏŞÖÆ£¡</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="minpoststr" value="$minpoststr" size=2 maxlength=2>¡¡Èç²»ÏëÏŞÖÆ£¬¿ÉÁô¿Õ£¬²»µÃ¶àÓÚ 50¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>·¢ÌùÔÊĞíµÄ×î¶à×Ö·ûÊı<br>Ö»¶ÔÆÕÍ¨×¢²áÓÃ»§ÓĞĞ§£¡Ì³Ö÷¡¢°ßÖñºÍÈÏÖ¤ÓÃ»§¶¼²»ÊÜ´ËÏŞÖÆ£¡</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpoststr" value="$maxpoststr" size=5 maxlength=5>¡¡Èç²»ÏëÏŞÖÆ£¬¿ÉÁô¿Õ£¬²»µÃÉÙÓÚ 100¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>·¢ÌùµÄ×îÉÙÔÚÏßÊ±¼ä<br>ÔÚÏßÊ±¼äÉÙÓÚÕâ¸öµÄÎŞ·¨·¢Ìù</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="onlinepost" value="$onlinepost" size=8 maxlength=8>¡¡µ¥Î»£ºÃë£¬½¨ÒéÉèÖÃ 600£¬Èç²»ÏëÏŞÖÆ£¬¾ÍÁô¿Õ»òÉè 0¡£</td>
                </tr>
                ~;

               $tempoutput = "<select name=\"arrawrecordclick\">\n<option value=\"no\">²»ÔÊĞí\n<option value=\"yes\">ÔÊĞí\n</select>";
               $tempoutput =~ s/value=\"$arrawrecordclick\"/value=\"$arrawrecordclick\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333>ÊÇ·ñÔÊĞí¼ÇÂ¼Ìû×Ó·ÃÎÊÇé¿ö</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>               
               ~;
               
               $tempoutput = "<select name=\"nowater\">\n<option value=\"off\">²»ÔÊĞí\n<option value=\"on\">ÔÊĞí\n</select>";
               $tempoutput =~ s/value=\"$nowater\"/value=\"$nowater\" selected/;
               print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333>ÊÇ·ñÔÊĞí·¢ÌùÕß¶Ô¹àË®½øĞĞÏŞÖÆ</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>               
               
	       <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=ËÎÌå color=#333333><b>ÉÙÓÚ¶àÉÙ×Ö·ûËã¹àË®£¿</font></b><BR>Èç¹ûÉÏÃæÑ¡Ôñ²»ÔÊĞíÏŞÖÆ£¬ÄÇÃ´´ËÏîÎŞĞ§£¡</td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="gsnum" value="$gsnum" size=5 maxlength=5>¡¡²»Òª¼Ó byte£¬½¨Òé²»Òª³¬¹ı 50¡£</td>
               </tr>      
               ~;

                $tempoutput = "<select name=\"defaulttopicshow\"><option value=>²é¿´ËùÓĞµÄÖ÷Ìâ<option value=\"1\">²é¿´Ò»ÌìÄÚµÄÖ÷Ìâ<option value=\"2\">²é¿´Á½ÌìÄÚµÄÖ÷Ìâ<option value=\"7\">²é¿´Ò»ĞÇÆÚÄÚµÄÖ÷Ìâ<option value=\"15\">²é¿´°ë¸öÔÂÄÚµÄÖ÷Ìâ<option value=\"30\">²é¿´Ò»¸öÔÂÄÚµÄÖ÷Ìâ<option value=\"60\">²é¿´Á½¸öÔÂÄÚµÄÖ÷Ìâ<option value=\"180\">²é¿´°ëÄêÄÚµÄÖ÷Ìâ</select>\n";
                $tempoutput =~ s/value=\"$defaulttopicshow\"/value=\"$defaulttopicshow\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ä¬ÈÏÏÔÊ¾Ö÷ÌâÊı</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"onlineview\">\n<option value=\"1\">ÏÔÊ¾\n<option value=\"0\">²»ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$onlineview\"/value=\"$onlineview\" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ä¬ÈÏÊÇ·ñÏÔÊ¾ÔÚÏßÓÃ»§ÏêÏ¸ÁĞ±í£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

                $tempoutput = "<select name=\"usefastpost\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$usefastpost\"/value=\"$usefastpost" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÊÇ·ñÆôÓÃ¿ìËÙ·¢²¼Ö÷Ìâ£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispquickreply\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$dispquickreply\"/value=\"$dispquickreply" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÊÇ·ñÆôÓÃ¿ìËÙ»Ø¸´£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"usenoimg\">\n<option value=\"no\">²»Ê¹ÓÃ\n<option value=\"yes\">Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$usenoimg\"/value=\"$usenoimg" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>ÊÇ·ñÆôÓÃÍ¼Æ¬´íÎóÊ±×Ô¶¯ĞŞÕı£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"waterwhenguest\">\n<option value=\"yes\">Ê¹ÓÃ\n<option value=\"no\">²»Ê¹ÓÃ\n</select>\n";
                $tempoutput =~ s/value=\"$waterwhenguest\"/value=\"$waterwhenguest" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>µ±¿ÍÈËä¯ÀÀÊ±£¬×Ô¶¯¼ÓË®Ó¡£¿(Í¬Ê±½«ÎŞ·¨¸´ÖÆÌû×Ó)</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispguest\">\n<option value=\"1\">ÊÓÏµÍ³¸ººÉ¶ø¶¨\n<option value=\"2\">ÓÀÔ¶ÏÔÊ¾\n<option value=\"3\">ÓÀÔ¶²»ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispguest\"/value=\"$dispguest\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÔÚÏßÁĞ±íÖĞÊÇ·ñÏÔÊ¾¿ÍÈË£¿</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"sendmanageinfo\">\n<option value=\"no\">²»Í¨ÖªÓÃ»§\n<option value=\"yes\">Í¨ÖªÓÃ»§\n</select>\n";
                $tempoutput =~ s/value=\"$sendmanageinfo\"/value=\"$sendmanageinfo" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>¹ÜÀíÌû×Ó£¨É¾³ı¡¢ÒÆ¶¯¡¢Ëø¶¨¡¢ÆÁ±ÎµÈ£©ºó£¬<BR>ÊÇ·ñ·¢¶ÌÏûÏ¢Í¨ÖªÓÃ»§£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"treeview\">\n<option value=\"no\">Æ½°åÏÔÊ¾Ìù×Ó\n<option value=\"yes\">Ê÷ĞÎÏÔÊ¾Ìù×Ó\n</select>\n";
                $tempoutput =~ s/value=\"$treeview\"/value=\"$treeview" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ä¬ÈÏÌû×ÓÏÔÊ¾·ç¸ñ¡£</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispjump\">\n<option value=\"yes\">ÏÔÊ¾\n<option value=\"no\">²»ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispjump\"/value=\"$dispjump\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333>ÊÇ·ñÏÔÊ¾ÂÛÌ³Ìø×ª</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"dispview\">\n<option value=\"yes\">ÏÔÊ¾\n<option value=\"no\">²»ÏÔÊ¾\n</select>\n";
                $tempoutput =~ s/value=\"$dispview\"/value=\"$dispview\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÊÇ·ñÏÔÊ¾ÂÛÌ³Í¼Àı</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>Ìû×ÓÖĞµÄÇ©ÃûÉÏ·½¼ÓÈëÎÄÕÂ°æÈ¨µÄÎÄ×Ö<BR>Èç¹û²»ĞèÒª£¬ÇëÉèÖÃÎª¿Õ°×</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcopyright" value="$postcopyright" size=30>¡¡<BR>Ä¬ÈÏ£º°æÈ¨ËùÓĞ£¬²»µÃÉÃ×Ô×ªÔØ</td>
                </tr>
		~;
		
		$tempoutput = "<select name=\"rssinfo\">\n<option value=\"yes\">ÔÊĞí\n<option value=\"no\">²»ÔÊĞí\n</select>\n";
                $tempoutput =~ s/value=\"$rssinfo\"/value=\"$rssinfo\" selected/;
                print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=ËÎÌå color=#333333><b>ÂÛÌ³ÊÇ·ñÔÊĞíÊ¹ÓÃ RSS ¹¦ÄÜ</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

                $tempoutput = "<select name=\"refreshforum\">\n<option value=\"off\">²»Òª×Ô¶¯Ë¢ĞÂ\n<option value=\"on\">Òª×Ô¶¯Ë¢ĞÂ\n</select>\n";
                $tempoutput =~ s/value=\"$refreshforum\"/value=\"$refreshforum" selected/;
                print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>±¾·ÖÂÛÌ³ÊÇ·ñ×Ô¶¯Ë¢ĞÂ(ÇëÔÚÏÂÃæÉèÖÃ¼ä¸ôÊ±¼ä)£¿</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>×Ô¶¯Ë¢ĞÂÂÛÌ³µÄÊ±¼ä¼ä¸ô(Ãë)<BR>ÅäºÏÉÏÃæ²ÎÊıÒ»ÆğÊ¹ÓÃ</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="autofreshtime" value="$autofreshtime" size= 5 maxlength=4>¡¡Ò»°ãÉèÖÃ 5 ·ÖÖÓ£¬¾ÍÊÇ 300 Ãë¡£</td>
                </tr>
		<tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>±¾°æ·¢ÌûÔö¼ÓµÄÉçÇø»õ±Ò (Áô¿ÕÔòÊ¹ÓÃÉçÇøÄ¬ÈÏ£¬Èç¹ûÑ¡ÔñÁË±¾°æ·¢Ìû²»¼ÆÈëÔò´ËÏîÎŞĞ§)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumpostmoney" value="$forumpostmoney" size= 8 maxlength=7></td>
             </tr>

             <tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>±¾°æ»ØÌûÔö¼ÓµÄÉçÇø»õ±Ò (Áô¿ÕÔòÊ¹ÓÃÉçÇøÄ¬ÈÏ£¬Èç¹ûÑ¡ÔñÁË±¾°æ·¢Ìû²»¼ÆÈëÔò´ËÏîÎŞĞ§)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumreplymoney" value="$forumreplymoney" size= 8 maxlength=7></td>
             </tr>

             <tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>±¾°æ±»É¾Ìù¼õÈ¥µÄÉçÇø»õ±Ò (Áô¿ÕÔòÊ¹ÓÃÉçÇøÄ¬ÈÏ£¬Èç¹ûÑ¡ÔñÁË±¾°æÉ¾Ìû²»¼ÆÈëÔò´ËÏîÎŞĞ§)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumdelmoney" value="$forumdelmoney" size= 8 maxlength=7></td>
             </tr>
		<tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>±¾°æ·¢ÌûÔö¼ÓµÄ»ı·Ö (Áô¿ÕÔòÊ¹ÓÃÉçÇøÄ¬ÈÏ£¬Èç¹ûÑ¡ÔñÁË±¾°æ·¢Ìû²»¼ÆÈëÔò´ËÏîÎŞĞ§)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumpostjf" value="$forumpostjf" size= 8 maxlength=7></td>
             </tr>

             <tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>±¾°æ»ØÌûÔö¼ÓµÄ»ı·Ö (Áô¿ÕÔòÊ¹ÓÃÉçÇøÄ¬ÈÏ£¬Èç¹ûÑ¡ÔñÁË±¾°æ·¢Ìû²»¼ÆÈëÔò´ËÏîÎŞĞ§)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumreplyjf" value="$forumreplyjf" size= 8 maxlength=7></td>
             </tr>

             <tr>
             <td bgcolor=#FFFFFF colspan=2>
             <font color=#333333>±¾°æ±»É¾Ìù¼õÈ¥µÄ»ı·Ö (Áô¿ÕÔòÊ¹ÓÃÉçÇøÄ¬ÈÏ£¬Èç¹ûÑ¡ÔñÁË±¾°æÉ¾Ìû²»¼ÆÈëÔò´ËÏîÎŞĞ§)</font></td>
             <td bgcolor=#FFFFFF>
             <input type=text name="forumdeljf" value="$forumdeljf" size= 8 maxlength=7></td>
             </tr>
<script>
function AddAllow()
{
	if (name = prompt("ÇëÊäÈëÒªÌí¼ÓµÄÖ»ÔÊĞí½øÈëµÄÓÃ»§µÄID£º", ""))
	{
		if (MAINFORM.allowusers.innerText) MAINFORM.allowusers.innerText += "," + name;
		else MAINFORM.allowusers.innerText = name;
	}
}
function DeleteAllow()
{
	if (name = prompt("ÇëÊäÈëÒªÈ¥³ıµÄÖ»ÔÊĞí½øÈëµÄÓÃ»§µÄID£º", ""))
	{
var myString = new String("," + window.MAINform.allowusers.innerText + ",");
var replaceString = eval("myString.replace(/," + name + ",/ig, ',')");
window.MAINform.allowusers.innerText = replaceString.substr(1, replaceString.length - 2);
	}
}
function ClearAllow()
{
	if (confirm("ÄãÈ·¶¨ÒªÇå¿ÕËùÓĞÖ»ÔÊĞí½øÈëµÄÓÃ»§ID£¿"))
		MAINFORM.allowusers.innerText = "";
}
</script>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333><b>Ö»ÔÊĞíÒÔÏÂÓÃ»§½øÈë±¾°æÃæ</b><BR>Èç¹ûÏ£ÍûÏòÈ«Ìå¿ª·Å£¬Çë²»ÒªÌîĞ´<BR>¶ÔÈÎºÎÓÃ»§¶¼ÓĞĞ§µÄ£¬°üÀ¨¹ÜÀíÔ±</font></td>
               <td bgcolor=#FFFFFF>
               <textarea name="allowusers" rows=6 cols=40 readonly=true>$allowusers</textarea><br><input type=button value=Ìí¼Ó OnClick="AddAllow();">¡¡<input type=button value=É¾³ı OnClick="DeleteAllow();">¡¡<input type=button value=Çå³ı OnClick="ClearAllow();"></td>
               </tr>~;

		$tempoutput = "<select name=\"forumallowcount\">\n<option value=\"yes\">¼ÆÈë·¢ÌùÊı\n<option value=\"no\">²»¼ÆÈë·¢ÌùÊı\n</select>\n";
              	$tempoutput =~ s/value=\"$forumallowcount\"/value=\"$forumallowcount" selected/;

		print qq~
		<tr>
              	<td bgcolor=#FFFFFF colspan=2>
              	<font color=#333333>±¾°æ·¢ÌûÊÇ·ñ¼ÆÈë×÷Õß·¢ÌûÊı</font></td>
              	<td bgcolor=#FFFFFF>
              	$tempoutput</td>
              	</tr>
		~;

		$tempoutput = "<select name=\"forumreplyallowcount\">\n<option value=\"yes\">¼ÆÈë»Ø¸´Êı\n<option value=\"no\">²»¼ÆÈë»Ø¸´Êı\n</select>\n";
              	$tempoutput =~ s/value=\"$forumreplyallowcount\"/value=\"$forumreplyallowcount" selected/;

		print qq~
		<tr>
              	<td bgcolor=#FFFFFF colspan=2>
              	<font color=#333333>±¾°æ»Ø¸´ÊÇ·ñ¼ÆÈë×÷Õß»Ø¸´Êı</font></td>
              	<td bgcolor=#FFFFFF>
              	$tempoutput</td>
              	</tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>½øÈëÂÛÌ³µÄ×îĞ¡ÍşÍûÊı<BR>Ğ¡ÓÚ´ËÍşÍûµÄ£¬²»ÄÜ½øÈë£¬×¢Òâ£ºÕâ¸öÊı×Ö±ØĞëÊÇ´óÓÚ 0 µÄ¡£</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="enterminweiwang" value="$enterminweiwang" size=3 maxlength=3>¡¡×¢ÒâÓÃ°ë½Ç£¬Ç°ºó²»ÒªÓĞ¿Õ¸ñ£¬Èç²»ÏëÏŞÖÆ£¬¾ÍÁô¿Õ»òÉè 0 ¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>½øÈëÂÛÌ³µÄ×îĞ¡½ğÇ®Êı<BR>Ğ¡ÓÚ´Ë½ğÇ®µÄ£¬²»ÄÜ½øÈë£¬×¢Òâ£ºÕâ¸öÊı×Ö±ØĞëÊÇ´óÓÚ 0 µÄ¡£</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="enterminmony" value="$enterminmony" size=10 maxlength=10>¡¡×¢ÒâÓÃ°ë½Ç£¬Ç°ºó²»ÒªÓĞ¿Õ¸ñ£¬Èç²»ÏëÏŞÖÆ£¬¾ÍÁô¿Õ»òÉè 0¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>½øÈëÂÛÌ³µÄ×îĞ¡»ı·ÖÊı<BR>Ğ¡ÓÚ´Ë»ı·ÖµÄ£¬²»ÄÜ½øÈë£¬×¢Òâ£ºÕâ¸öÊı×Ö±ØĞëÊÇ´óÓÚ 0 µÄ¡£</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="enterminjf" value="$enterminjf" size=10 maxlength=10>¡¡×¢ÒâÓÃ°ë½Ç£¬Ç°ºó²»ÒªÓĞ¿Õ¸ñ£¬Èç²»ÏëÏŞÖÆ£¬¾ÍÁô¿Õ»òÉè 0¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>·¢±íÖ÷ÌûµÄ×îĞ¡»ı·ÖÊı<BR>Ğ¡ÓÚ´Ë»ı·ÖµÄ£¬²»ÄÜ·¢Ìû£¬×¢Òâ£ºÕâ¸öÊı×Ö±ØĞëÊÇ´óÓÚ 0 µÄ¡£</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postminjf" value="$postminjf" size=10 maxlength=10>¡¡×¢ÒâÓÃ°ë½Ç£¬Ç°ºó²»ÒªÓĞ¿Õ¸ñ£¬Èç²»ÏëÏŞÖÆ£¬¾ÍÁô¿Õ»òÉè 0 ¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>·¢±í»Ø¸´µÄ×îĞ¡»ı·ÖÊı<BR>Ğ¡ÓÚ´Ë»ı·ÖµÄ£¬²»ÄÜ»Ø¸´£¬×¢Òâ£ºÕâ¸öÊı×Ö±ØĞëÊÇ´óÓÚ 0 µÄ¡£</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="replyminjf" value="$replyminjf" size=10 maxlength=10>¡¡×¢ÒâÓÃ°ë½Ç£¬Ç°ºó²»ÒªÓĞ¿Õ¸ñ£¬Èç²»ÏëÏŞÖÆ£¬¾ÍÁô¿Õ»òÉè 0 ¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>·¢ÆğÍ¶Æ±µÄ×îĞ¡»ı·ÖÊı<BR>Ğ¡ÓÚ´Ë»ı·ÖµÄ£¬²»ÄÜ·¢Í¶Æ±Ìû£¬×¢Òâ£ºÕâ¸öÊı×Ö±ØĞëÊÇ´óÓÚ 0 µÄ¡£</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="pollminjf" value="$pollminjf" size=10 maxlength=10>¡¡×¢ÒâÓÃ°ë½Ç£¬Ç°ºó²»ÒªÓĞ¿Õ¸ñ£¬Èç²»ÏëÏŞÖÆ£¬¾ÍÁô¿Õ»òÉè 0 ¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>½øĞĞÍ¶Æ±µÄ×îĞ¡»ı·ÖÊı<BR>Ğ¡ÓÚ´Ë»ı·ÖµÄ£¬²»ÄÜ¶ÔÍ¶Æ±Ìû½øĞĞÍ¶Æ±£¬×¢Òâ£ºÕâ¸öÊı×Ö±ØĞëÊÇ´óÓÚ 0 µÄ¡£</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="polledminjf" value="$polledminjf" size=10 maxlength=10>¡¡×¢ÒâÓÃ°ë½Ç£¬Ç°ºó²»ÒªÓĞ¿Õ¸ñ£¬Èç²»ÏëÏŞÖÆ£¬¾ÍÁô¿Õ»òÉè 0 ¡£</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>·ÖÂÛÌ³±³¾°ÒôÀÖÃû³Æ</b>(Èç¹ûÃ»ÓĞÇëÁô¿Õ)<br>ÇëÊäÈë±³¾°ÒôÀÖÃû³Æ£¬±³¾°ÒôÀÖ<BR>Ó¦ÉÏ´«ÓÚ non-cgi/midi Ä¿Â¼ÏÂ¡£<br><b>²»Òª°üº¬ URL µØÖ·»ò¾ø¶ÔÂ·¾¶£¡</b></font></td>
                <td bgcolor=#FFFFFF>
                <input type=text size=20 name="midiaddr" value="$midiaddr">~;
                $midiabsaddr = "$imagesdir" . "midi/$midiaddr";
                print qq~¡¡<EMBED src="$imagesurl/midi/$midiaddr" autostart="false" width=70 height=25 loop="true" align=absmiddle>~ if ((-e "$midiabsaddr")&&($midiaddr ne ""));
                print qq~
                </td>
<tr>
              <td bgcolor=#EEEEEE align=center colspan=3>
              <font color=#990000><b><center>ÉçÇø°æ¿éÈ¨ÏŞ¹ÜÀí</center></b>
              </td></tr>

              <tr>
              <td bgcolor=#FFFFFF>
              <font face=ËÎÌå color=#333333><b>ÔÊĞí·ÃÎÊÂÛÌ³µÄ³ÉÔ±×é</b><br>Èç¹û²»ĞèÒªÕâ¸ö¹¦ÄÜ£¬ÇëÈ«²¿²»ÒªÑ¡Ôñ(»òÕßÈ«²¿Ñ¡Ôñ£¬Ğ§¹ûÒ»Ñù)£¡</font></td>
              <td bgcolor=#FFFFFF colspan=2>~;
              my $memteam1 = qq~<input type=checkbox name="yxz" value="rz1">$defrz1(ÈÏÖ¤ÓÃ»§)<br>~ if ($defrz1 ne "");
   my $memteam2 = qq~<input type=checkbox name="yxz" value="rz2">$defrz2(ÈÏÖ¤ÓÃ»§)<br>~ if ($defrz2 ne "");
   my $memteam3 = qq~<input type=checkbox name="yxz" value="rz3">$defrz3(ÈÏÖ¤ÓÃ»§)<br>~ if ($defrz3 ne "");
   my $memteam4 = qq~<input type=checkbox name="yxz" value="rz4">$defrz4(ÈÏÖ¤ÓÃ»§)<br>~ if ($defrz4 ne "");
   my $memteam5 = qq~<input type=checkbox name="yxz" value="rz5">$defrz5(ÈÏÖ¤ÓÃ»§)<br>~ if ($defrz5 ne "");
              $all=qq~<input type=checkbox name="yxz" value="">¿ÍÈË<br><input type=checkbox name="yxz" value="me">Ò»°ãÓÃ»§<br>$memteam1$memteam2$memteam3$memteam4$memteam5
<input type=checkbox name="yxz" value="rz">ÈÏÖ¤ÓÃ»§<br>
<input type=checkbox name="yxz" value="banned">½ûÖ¹´ËÓÃ»§·¢ÑÔ<br>
<input type=checkbox name="yxz" value="masked">ÆÁ±Î´ËÓÃ»§Ìù×Ó<br>
<input type=checkbox name="yxz" value="mo">ÂÛÌ³°æÖ÷<br>
<input type=checkbox name="yxz" value="amo">ÂÛÌ³¸±°æÖ÷<br>
<input type=checkbox name="yxz" value="cmo">·ÖÀàÇø°æÖ÷<br>
<input type=checkbox name="yxz" value="smo">ÂÛÌ³×Ü°æÖ÷<br>
<input type=checkbox name="yxz" value="ad">Ì³Ö÷<br>~;
              my @yxz = split(/\,/,$yxz);
              foreach(@yxz){
              chomp;
              next if ($_ eq '');
              $all=~s/<input type=checkbox name="yxz" value="$_"/<input type=checkbox name="yxz" value="$_" checked/g;
              }
              print qq~
$all
              </td>
              </tr>
                </tr>
                <td bgcolor=#FFFFFF align=center colspan=3>
                <input type=submit value="Ìá ½»"></form></td></tr></table></td></tr></table>
                ~;

}

sub dostyle {
    $filerequire = "$lbdir" . "data/style${inforum}.cgi";
    foreach (@params) {
	$theparam = $query->param($_);
	$theparam =~ s/\\/\\\\/g;
        $theparam =~ s/\@/\\\@/g;

        if (($_ eq 'maintopicad')||($_ eq 'replytopicad')) {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g
	}

        $theparam = &unHTML("$theparam");

        if ($_ eq "footmark" || $_ eq "headmark" || $_ eq "adfoot" || $_ eq "adscript") {
	    $theparam =~ s/[\f\n\r]+/\n/ig;
	    $theparam =~ s/[\r \n]+$/\n/ig;
	    $theparam =~ s/^[\r\n ]+/\n/ig;
            $theparam =~ s/\n\n/\n/ig;
            $theparam =~ s/\n/\[br\]/ig;
            $theparam =~ s/ \&nbsp;/  /g;
	}


	${$_} = $theparam;
	
        if (($_ ne 'action')&&($_ ne 'forum')&&($_ ne 'yxz')&&($theparam ne "")) {
        	$_ =~ s/[\a\f\n\e\0\r]//isg;
        	$theparam =~ s/[\a\f\n\e\0\r]//isg;
            $printme .= "\$" . "$_ = \"$theparam\"\;\n" if (($_ ne "")&&($theparam ne ""));
        }
    }
    $endprint = "1\;\n";
    open(FILE,">$filerequire");

	@yxz = $query -> param('yxz');
	print FILE "\$yxz=\"";
	$temp = 0;
	foreach(@yxz){
	    chomp;
	    print FILE ",$_";
	    $temp=1;
	}
	if ($temp eq "1") {
	    print FILE ",\";\n";
	} else {
	    print FILE "\";\n";
	}

    print FILE "$printme";
    print FILE $endprint;
    close(FILE);

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);
@dirdata1 = grep(/^forumstoptopic$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumshead$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstitle$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^forumstopic$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }
@dirdata1 = grep(/^plcache$inforum/,@dirdata);
foreach (@dirdata1) { unlink ("${lbdir}cache/$_"); }

    if (-e $filerequire && -w $filerequire) {
        print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>»¶Ó­À´µ½ÂÛÌ³¹ÜÀíÖĞĞÄ / ·ÖÂÛÌ³·ç¸ñÉè¶¨</b></td></tr>
<tr><td bgcolor=#EEEEEE colspan=2><font color=#333333><center><b>ÒÔÏÂĞÅÏ¢ÒÑ¾­³É¹¦±£´æ</b><br><br>
</center>~;

	print "\$yxz=\"";
	$temp = 0;
	foreach(@yxz){
	    chomp;
	    print ",$_";
	    $temp=1;
	}
	if ($temp eq "1") {
	    print ",\";<BR>";
	} else {
	    print "\";<BR>";
	}
	$printme =~ s/\n/\<br>/g;
        $printme =~ s/\"//g;
        $printme =~ s/\$//g;
        $printme =~ s/\\\@/\@/g;
        print $printme;
        print qq~</td></tr></table></td></tr></table>~;
    }
    else {
	print qq~<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF><b>»¶Ó­À´µ½ÂÛÌ³¹ÜÀíÖĞĞÄ / ·ÖÂÛÌ³·ç¸ñÉè¶¨</b></td></tr>
<tr><td bgcolor=#EEEEEE align=center colspan=2>
<font color=#333333><b>ËùÓĞĞÅÏ¢Ã»ÓĞ±£´æ</b><br>ÎÄ¼ş»òÕßÄ¿Â¼²»¿ÉĞ´<br>Çë¼ì²âÄãµÄ data Ä¿Â¼ºÍ styles*.cgi ÎÄ¼şµÄÊôĞÔ£¡
</td></tr></table></td></tr></table>
~;
    }
}
