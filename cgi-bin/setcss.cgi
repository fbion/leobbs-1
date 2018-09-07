#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
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
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setcss.cgi";

$query = new LBCGI;

$action              = $query -> param('action');
$oldmembersdir       = $query -> param('oldmembersdir');
$membersdir          = $query -> param('membersdir');

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");


if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {

    print qq~
<script language='Javascript'>
 function do_css() {
    var theForm = document.css_form;
    var theName = theForm.NAME.value;
    var theFont = theForm.FONT.value;
    var theSize = theForm.SIZE.value;
    var theSizeT = theForm.SIZE_TYPE.value;
    var theWeight = theForm.WEIGHT.value;
    var theColor  = theForm.COLOUR.value;
    var theBG     = theForm.BGCOLOUR.value;
    var theBW     = theForm.BWEIGHT.value;
    var theBC     = theForm.BCOLOUR.value;
    var theSpace  = theForm.SPACE.value;
    var theSpaceT = theForm.SPACING.value;
    var theLSpace = theForm.LSPACE.value;
    var tmp_style = \"solid\";
    var tmp_col   = \"black\";
    var tmp_thick = \"1px\";
    var msg = \"\";
    
    if (theName == \"\") { msg = \"你必须要写一个 CSS 的名字\"; }
    if (msg != \"\") {
        alert(msg);
        return;
    }
    var thecss = \"#\" + theName + \" {\\n\";
    if (theFont != \"\") {
     thecss += \"\t font-family: \" + theFont + \";\\n\";
    }
    if (theSize != \"\") {
     thecss += \"\t font-size: \" + theSize + theSizeT + \";\\n\";
    }
    if (theWeight != \"normal\") {
     thecss += \"\t font-weight: \" +  theWeight + \";\\n\";
    }
    if (theColor != \"\") {
     thecss += \"\t color: \" +  theColor + \";\\n\";
    }
    if (theBG != \"\") {
     thecss += \"\t background-color: \" +  theBG + \";\\n\";
    }
    if (theBW != \"\") {
     tmp_thick    = theBW + \"px\";
    }
    if (theBC != \"\") {
     tmp_col  = theBC;
    }
    if (theBW != \"\" && theBC != \"\") {
     thecss += \"\t border: \" + tmp_style + \" \" + tmp_col + \" \" + tmp_thick + \";\\n\";
    }
    if (theSpace != \"\") {
     thecss += \"\t line-height: \" + theSpace + theSpaceT + \";\\n\";
    }
    if (theLSpace != \"\") {
     thecss += \"\t letter-spacing: \" + theLSpace + \"px;\\n\";
    }
    thecss += \"}\";
    
    theForm.CSS.value = thecss;
    return;
    
   }
    function preview() {
       var theCSS = document.css_form.CSS.value;
       var theID  = document.css_form.NAME.value;
       var Template = \"<html><head><title>testing CSS</title><style type=\\"text/css\\">\"+theCSS+\"</style></head>\\n<body bgcolor='#FFFFFF'>\\n\";
       Template += \"<span id='\"+theID+\"'>极酷超级论坛 LeoBBS ！<br>CSS 预览......</span>\";
       Template += \"\\n</body></html>\";
       var newWin = window.open( '', 'PREVIEW', 'width=500,height=200,top=0,left=0,resizable=1,scrollbars=1,location=no,directories=no,status=no,menubar=no,toolbar=no');
       newWin.document.write(Template);
   }    
 </script>
                     <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 用户 CSS 自动生成</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE valign=middle align=center colspan=2><font face=宋体 color=#333333>
  <br><br>
 <form name='css_form'>
 <table width='95%' align='center' border='0' bgcolor='#000000' cellspacing='1' cellpadding='0'>
 <tr>
  <td>
   <table width='100%' align='center' border='0' bgcolor='#EFEFEF' cellspacing='0' cellpadding='4'>
   <tr>
    <td width='40%'><b>要生成的 CSS 的名字?</b></td>
    <td width='60%'><input type='text' name='NAME'></td>
   </tr>
   <tr>
    <td width='40%'><b>字体名称 (多个字体可以用逗号隔开)</b></td>
    <td width='60%'><input type='text' name='FONT'></td>
   </tr>
   <tr>
    <td width='40%'><b>字体大小</b></td>
    <td width='60%'><input type='text' name='SIZE' size='5'>&nbsp;<select name='SIZE_TYPE'><option value='px'>像素<option value='pt'>点<option value='em'>em</select></td>
   </tr>
   <tr>
    <td width='40%'><b>字体宽度</b></td>
    <td width='60%'><select name='WEIGHT'><option value='normal'>正常<option value='bold'>粗体<option value='bolder'>更粗</select></td>
   </tr>
   <tr>
    <td width='40%'><b>字体颜色</b></td>
    <td width='60%'><input type='text' name='COLOUR'></td>
   </tr>
   <tr>
    <td width='40%'><b>背景颜色</b></td>
    <td width='60%'><input type='text' name='BGCOLOUR'></td>
   </tr>
   <tr>
    <td width='40%'><b>边框</b></td>
    <td width='60%'>宽度<input type='text' name='BWEIGHT' size='5'>&nbsp;&nbsp;&nbsp;颜色<input type='text' name='BCOLOUR' size='15'></td>
   </tr>
   <tr>
    <td width='40%'><b>行间距</b></td>
    <td width='60%'><input type='text' name='SPACE' size='5'>&nbsp;<select name='SPACING'><option value='px'>像素<option value='pt'>点<option value='%'>%</select></td>
   </tr>
   <tr>
    <td width='40%'><b>字母间距</b></td>
    <td width='60%'><input type='text' name='LSPACE' size='5'>&nbsp;点</td>
   </tr>
   <tr>
   <td colspan='2' align='center'><input type='button' onClick='do_css();' value='自动生成相应的 CSS 代码'></td>
   </tr>
 </table>
</td>
</tr>
</table>

<br><br><br><center>生成的 CSS 代码如下：<br><textarea name='CSS' rows='10' cols='70' wrap='soft'></textarea><BR><BR>
<input type='button' onClick='preview();' value='风格预览'></center>
</form>
                ~;

            }
            else {
                 &adminlogin;
                 }

print qq~</td></tr></table></body></html>~;
exit;
