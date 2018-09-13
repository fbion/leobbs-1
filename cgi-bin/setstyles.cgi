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
    $startingtime = (times)[0] + (times)[1];
    foreach ($0, $ENV{'PATH_TRANSLATED'}, $ENV{'SCRIPT_FILENAME'}) {
        my $LBPATH = $_;
        next if ($LBPATH eq '');
        $LBPATH =~ s/\\/\//g;
        $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC, $LBPATH);
    }
}

use warnings;
use strict;
use diagnostics;
use LBCGI;
$LBCGI::POST_MAX = 500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "setstyles.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

$query = new LBCGI;
#&ipbanned; #封杀一些 ip

@params = $query->param;
foreach (@params) {
    $theparam = $query->param($_);
    $theparam =~ s/\\/\\\\/g;
    $theparam =~ s/\@/\\\@/g;

    if (($_ eq 'maintopicad') || ($_ eq 'replytopicad')) {
        $theparam =~ s/[\f\n\r]+/\n/ig;
        $theparam =~ s/[\r \n]+$/\n/ig;
        $theparam =~ s/^[\r\n ]+/\n/ig;
        $theparam =~ s/\n\n/\n/ig;
        $theparam =~ s/\n/\[br\]/ig;
        $theparam =~ s/ \&nbsp;/  /g
    }

    $theparam = &unHTML("$theparam");

    if ($_ eq "footmark" || $_ eq "headmark" || $_ eq "footmark1" || $_ eq "headmark1") {
        $theparam =~ s/[\f\n\r]+/\n/ig;
        $theparam =~ s/[\r \n]+$/\n/ig;
        $theparam =~ s/^[\r\n ]+/\n/ig;
        $theparam =~ s/\n\n/\n/ig;
        $theparam =~ s/\n/\[br\]/ig;
        $theparam =~ s/ \&nbsp;/  /g
    }

    ${$_} = $theparam;
    if ($_ ne 'action' && $_ ne 'yxz') {
        $_ =~ s/[\a\f\n\e\0\r]//isg;
        $theparam =~ s/[\a\f\n\e\0\r]//isg;
        $printme .= "\$" . "$_ = \"$theparam\"\;\n" if (($_ ne "") && ($theparam ne ""));
    }
}
$in_member_name = $query->cookie("adminname");
$in_password = $query->cookie("adminpass");
$in_member_name =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$in_password =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");
&admintitle;

&getmember("$in_member_name", "no");

if (($member_code eq "ad") && ($in_password eq $password) && ($password ne "") && ($in_member_name ne "") && (lc($in_member_name) eq lc($membername))) {
    if ($action eq "process") {

        $membergone = $query->param('membergone');
        if (($membergone > 180) || ($membergone < 5)) {
            print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 风格设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>错误</b><br><br><br><br>在线时间不能小于５分钟或者超过180分钟！！！<br><Br><Br>
                    </td></tr></table></td></tr></table>
                    ~;
            exit;
        }
        $printme .= "1\;\n";

        $filetomake = "$lbdir" . "data/styles.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE, ">$filetomake");
        flock(FILE, 2) if ($OS_USED eq "Unix");

        @yxz = $query->param('yxz');
        print FILE "\$yxz=\"";
        $temp = 0;
        foreach (@yxz) {
            chomp;
            print FILE ",$_";
            $temp = 1;
        }
        if ($temp eq "1") {
            print FILE ",\";\n";
        }
        else {
            print FILE "\";\n";
        }

        print FILE "$printme";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        opendir(CATDIR, "${lbdir}cache");
        @dirdata = readdir(CATDIR);
        closedir(CATDIR);
        @dirdata1 = grep (/^forumstoptopic/, @dirdata);
        foreach (@dirdata1) {unlink("${lbdir}cache/$_");}
        @dirdata1 = grep (/^forumshead/, @dirdata);
        foreach (@dirdata1) {unlink("${lbdir}cache/$_");}
        @dirdata1 = grep (/^forumstitle/, @dirdata);
        foreach (@dirdata1) {unlink("${lbdir}cache/$_");}
        @dirdata1 = grep (/^forumstopic/, @dirdata);
        foreach (@dirdata1) {unlink("${lbdir}cache/$_");}
        @dirdata1 = grep (/^plcache/, @dirdata);
        foreach (@dirdata1) {unlink("${lbdir}cache/$_");}

        if (-e $filetomake && -w $filetomake) {
            print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 风格设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE colspan=2>
                <font color=#333333><center><b>以下的信息全部成功保存</b><br><br>
                </center>~;

            print "\$yxz=\"";
            $temp = 0;
            foreach (@yxz) {
                chomp;
                print ",$_";
                $temp = 1;
            }
            if ($temp eq "1") {
                print ",\";<BR>";
            }
            else {
                print "\";<BR>";
            }

            $printme =~ s/\n/\<br>/g;
            $printme =~ s/\"//g;
            $printme =~ s/\$//g;
            $printme =~ s/\\\@/\@/g;
            $printme =~ s/1\;//g;
            print $printme;

            print qq~
                </td></tr></table></td></tr></table>
                ~;
        }
        else {
            print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 风格设置</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>所有信息没有保存</b><br>文件或者目录不可写，请设置属性为 777 ！
                    </td></tr></table></td></tr></table>
                    ~;
        }

    }
    else {

        $dirtoopen = "$lbdir" . "data/skin";
        opendir(DIR, "$dirtoopen");
        @dirdata = readdir(DIR);
        closedir(DIR);
        my $myskin = "";
        @thd = grep (/\.cgi$/, @dirdata);
        $topiccount = @thd;
        @thd = sort @thd;
        for (my $i = 0; $i < $topiccount; $i++) {
            $thd[$i] =~ s/\.cgi//isg;
            $myskin .= qq~<option value="$thd[$i]">皮肤 [ $thd[$i] ]~;
        }
        $myskin =~ s/value=\"$skin_selected\"/value=\"$skin_selected\" selected/;
        $in_member_name =~ s/\_/ /g;

        print qq~
                <tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 皮肤设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#333333><b>设定皮肤风格</b>
                </td></tr>
		~;
        if ($cssname ne "") {print qq~<tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>皮肤名称</font></td><td bgcolor=#FFFFFF><input type=text name="cssname" size=10 value="$cssname"></td></tr><tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>配色作者</font></td><td bgcolor=#FFFFFF><input type=text name="cssmaker" size=10 value="$cssmaker"></td></tr><tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>配色简介</font></td><td bgcolor=#FFFFFF><textarea cols=40 name="cssreadme" rows=2>$cssreadme</textarea>
</td></tr>~};


        print qq~
                <form action="$thisprog" method="post" name=FORM>
                <input type=hidden name="action" value="process">

                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>使用系统自带的皮肤风格</b><br>你选择某个风格后，此页面中的和颜色相关的设置一律无效<BR>如果要让此页面内的设置生效,请选择[默认风格]</font></td>
                <td bgcolor=#FFFFFF>
                <select name="skinselected">
                <option value="">默认风格$myskin
                </select>
                </td></tr>
~;

        $tempoutput = "<select name=\"usesuperannounce\">\n<option value=\"0\">不使用\n<option value=\"1\">使用\n</select>\n";
        $tempoutput =~ s/value=\"$usesuperannounce\"/value=\"$usesuperannounce\" selected/;
        print qq~
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=宋体 color=#333333><b>是否使用论坛超级公告</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>超级公告内容</b><br>(支持HTML格式，显示给所有用户)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="superannounce" cols="40">$superannounce</textarea><BR>
                </td>
                </tr>
		~;
        $footmark =~ s/\[br\]/\n/isg;
        $headmark =~ s/\[br\]/\n/isg;
        $footmark1 =~ s/\[br\]/\n/isg;
        $headmark1 =~ s/\[br\]/\n/isg;

        $tempoutput = "<select name=\"superannouncedisp\">\n<option value=\"oncepersession\">每个进程只显示一次\n<option value=\"always\">总是显示\n<option value=\"2\">50%显示几率\n<option value=\"3\">33%显示几率\n<option value=\"4\">25%显示几率\n<option value=\"10\">10%显示几率\n<option value=\"20\">5%显示几率\n<option value=\"50\">2%显示几率\n<option value=\"100\">1%显示几率\n</select>\n";
        $tempoutput =~ s/value=\"$superannouncedisp\"/value=\"$superannouncedisp\" selected/;

        $tempoutput1 = "<select name=\"superannouncehide\">\n<option value=\"yes\">二十秒后自动隐藏\n<option value=\"no\">一直显示\n</select>\n";
        $tempoutput1 =~ s/value=\"$superannouncehide\"/value=\"$superannouncehide\" selected/;
        print qq~
               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font face=宋体 color=#333333><b>论坛超级公告选项</b></font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput $tempoutput1</td> 
               </tr> 

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛BODY标签</b>
                </font></td>
                </tr>

                <input type=hidden name="skin" value="$skin" size=10 maxlength=10>
                <input type=hidden name="cssmaker" value="$cssmaker">
                <input type=hidden name="cssname" value="$cssname">
                <input type=hidden name="cssurl" value="$cssurl">
                <input type=hidden name="cssprogrammaker" value="$cssprogrammaker">
                <input type=hidden name="cssprogrammakerurl" value="$cssprogrammakerurl">
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>控制整个论坛风格的背景颜色或者背景图片等</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>默认：bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛页眉和页脚</b>
                </font></td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>首页独立页眉</b><br>(独立显示在首页面最上方，HTML格式)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="headmark1" cols="40">$headmark1</textarea><BR>
                </td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>首页独立页脚</b><br>(独立显示在首版权信息下方，HTML格式)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="footmark1" cols="40">$footmark1</textarea><BR>
                </td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>页眉</b><br>(显示在页面最上方，HTML格式)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="headmark" cols="40">$headmark</textarea><BR>
                </td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>页脚</b><br>(显示在版权信息下方，HTML格式)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="footmark" cols="40">$footmark</textarea><BR>
                </td>
                </tr>

		<tr>
                <td bgcolor=#FFFFFF valign=middle align=left width=40%>
                <font color=#333333><b>导航栏格外链接</b><br>(显示在导航栏的中间)</font></td>
                <td></td><td bgcolor=#FFFFFF>
                <textarea name="navadd" cols="40">$navadd</textarea><BR>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否显示原版页眉</font></td>
                <td bgcolor=#FFFFFF>
		~;
        $tempoutput = "<select name=\"usetopm\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select><p>\n";
        $tempoutput =~ s/value=\"$usetopm\"/value=\"$usetopm\" selected/;
        print qq~
                $tempoutput</td>
		</tr>
<script>
function selcolor(obj,obj2){
var arr = showModalDialog("$imagesurl/editor/selcolor.html", "", "dialogWidth:18.5em; dialogHeight:17.5em; status:0");
obj.value=arr;
obj2.style.backgroundColor=arr;
}
</script>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛页首菜单</b>
                </font></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带字体颜色</font></td>
                <td bgcolor=$menufontcolor width=12 id=menufontcolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menufontcolor" value="$menufontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,menufontcolor2)" style="cursor:hand">　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带背景颜色</font></td>
                <td bgcolor=$menubackground  width=12 id=menubackground2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackground" value="$menubackground" size=7 maxlength=7 onclick="javascript:selcolor(this,menubackground2)" style="cursor:hand">　默认：#DDDDDD</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>菜单带背景图片</font><BR>请输入图片名称，此图必须在 images 目录下的 $skin 里</td>
                <td background=$imagesurl/images/$skin/$menubackpic width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackpic" value="$menubackpic"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>菜单带边界颜色</font></td>
                <td bgcolor=$titleborder width=12 id=titleborder2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titleborder" value="$titleborder" size=7 maxlength=7 onclick="javascript:selcolor(this,titleborder2)" style="cursor:hand">　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>字体外观和颜色</b>(如果修改，那么请修改后到论坛初始化中清空 Cache 一次)
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>主字体外观</font></td>
                <td bgcolor=#FFFFFF>
                ~;
        $tempoutput = "<select name=\"font\">\n<option value=\"宋体\">宋体\n<option value=\"仿宋_UTF-8\">仿宋\n<option value=\"楷体_UTF-8\">楷体\n<option value=\"黑体\">黑体\n<option value=\"隶书\">隶书\n<option value=\"幼圆\">幼圆\n</select><p>\n";
        $tempoutput =~ s/value=\"$font\"/value=\"$font\" selected/;
        print qq~
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"最后发贴者"字体颜色</font></td>
                <td bgcolor=$lastpostfontcolor width=12 id=lastpostfontcolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lastpostfontcolor" value="$lastpostfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,lastpostfontcolor2)" style="cursor:hand">　默认：#000000</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"加重区"字体颜色</font></td>
                <td bgcolor=$fonthighlight  width=12 id=fonthighlight2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fonthighlight" value="$fonthighlight" size=7 maxlength=7 onclick="javascript:selcolor(this,fonthighlight2)" style="cursor:hand">　默认：#990000</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>查看时发表者名称字体</font></td>
                <td bgcolor=#FFFFFF>
                ~;
        $tempoutput = "<select name=\"posternamefont\">\n<option value=\"宋体\">宋体\n<option value=\"仿宋_UTF-8\">仿宋\n<option value=\"楷体_UTF-8\">楷体\n<option value=\"黑体\">黑体\n<option value=\"隶书\">隶书\n<option value=\"幼圆\">幼圆\n</select><p>\n";
        $tempoutput =~ s/value=\"$posternamefont\"/value=\"$posternamefont\" selected/;
        print qq~
                $tempoutput</td>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>一般用户名称字体颜色</font></td>
                <td bgcolor=$posternamecolor  width=12 id=posternamecolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="posternamecolor" value="$posternamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,posternamecolor2)" style="cursor:hand">　默认：#000066</td>
                </tr>

		<tr>
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>一般用户名称上的光晕颜色</font></td>
		<td bgcolor=$memglow  width=12 id=memglow2>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="memglow" value="$memglow" size=7 maxlength=7 onclick="javascript:selcolor(this,memglow2)" style="cursor:hand">　默认：#9898BA</td>
		</tr>
               
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>坛主名称字体颜色</font></td>
                <td bgcolor=$adminnamecolor  width=12 id=adminnamecolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="adminnamecolor" value="$adminnamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,adminnamecolor2)" style="cursor:hand">　默认：#990000</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>坛主名称上的光晕颜色</font></td>
		<td bgcolor=$adminglow  width=12 id=adminglow2>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="adminglow" value="$adminglow" size=7 maxlength=7 onclick="javascript:selcolor(this,adminglow2)" style="cursor:hand">　默认：#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>总版主名称字体颜色</font></td>
                <td bgcolor=$smonamecolor  width=12 id=smonamecolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="smonamecolor" value="$smonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,smonamecolor2)" style="cursor:hand">　默认：#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>总版主名称上的光晕颜色</font></td>
		<td bgcolor=$smoglow  width=12 id=smoglow2>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="smoglow" value="$smoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,smoglow2)" style="cursor:hand">　默认：#9898BA</td>
		</tr>
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类区版主名称字体颜色</font></td>
                <td bgcolor=$cmonamecolor  width=12 id=cmonamecolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="cmonamecolor" value="$cmonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,cmonamecolor2)" style="cursor:hand">　默认：#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>分类区版主名称上的光晕颜色</font></td>
		<td bgcolor=$cmoglow  width=12 id=cmoglow2>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="cmoglow" value="$cmoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,cmoglow2)" style="cursor:hand">　默认：#9898BA</td>
		</tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>版主名称字体颜色</font></td>
                <td bgcolor=$teamnamecolor  width=12 id=teamnamecolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="teamnamecolor" value="$teamnamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,teamnamecolor2)" style="cursor:hand">　默认：#0000ff</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>版主名称上的光晕颜色</font></td>
		<td bgcolor=$teamglow  width=12 id=teamglow2>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="teamglow" value="$teamglow" size=7 maxlength=7 onclick="javascript:selcolor(this,teamglow2)" style="cursor:hand">　默认：#9898BA</td>
		</tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>副版主名称字体颜色</font></td>
                <td bgcolor=$amonamecolor  width=12 id=amonamecolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="amonamecolor" value="$amonamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,amonamecolor2)" style="cursor:hand">　默认：#009900</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>副版主名称上的光晕颜色</font></td>
		<td bgcolor=$amoglow  width=12 id=amoglow2>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="amoglow" value="$amoglow" size=7 maxlength=7 onclick="javascript:selcolor(this,amoglow2)" style="cursor:hand">　默认：#9898BA</td>
		</tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>认证用户名称字体颜色</font></td>
                <td bgcolor=$rznamecolor  width=12 id=rznamecolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="rznamecolor" value="$rznamecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,rznamecolor2)" style="cursor:hand">　默认：#44ff00</td>
                </tr>

		<td bgcolor=#FFFFFF>
		<font color=#333333>认证用户名称上的光晕颜色</font></td>
		<td bgcolor=$rzglow  width=12 id=rzglow2>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="rzglow" value="$rzglow" size=7 maxlength=7 onclick="javascript:selcolor(this,rzglow2)" style="cursor:hand">　默认：#008736</td>
		</tr>
		
		<td bgcolor=#FFFFFF>
		<font face=verdana color=#333333>过滤和禁言用户名称上的光晕颜色</font></td>
		<td bgcolor=$banglow  width=12 id=banglow2>　</td>
		<td bgcolor=#FFFFFF>
		<input type=text name="banglow" value="$banglow" size=7 maxlength=7 onclick="javascript:selcolor(this,banglow2)" style="cursor:hand">　默认：none</td>
		</tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>所有页面颜色</center></b>
                <font color=#333333>这些颜色配置将用于每个页面。用于注册、登录、在线以及其他页面。
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>主字体颜色一</font></td>
                <td bgcolor=$fontcolormisc  width=12 id=fontcolormisc3>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fontcolormisc" value="$fontcolormisc" size=7 maxlength=7 onclick="javascript:selcolor(this,fontcolormisc3)" style="cursor:hand">　默认：#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>主字体颜色二</font></td>
                <td bgcolor=$fontcolormisc2  width=12 id=fontcolormisc4>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="fontcolormisc2" value="$fontcolormisc2" size=7 maxlength=7 onclick="javascript:selcolor(this,fontcolormisc4)" style="cursor:hand">　默认：#444444</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色一</font></td>
                <td bgcolor=$miscbackone  width=12 id=miscbackone2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbackone" value="$miscbackone" size=7 maxlength=7 onclick="javascript:selcolor(this,miscbackone2)" style="cursor:hand">　默认：#FFFFFF</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>其他背景颜色二</font></td>
                <td bgcolor=$miscbacktwo  width=12 id=miscbacktwo2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="miscbacktwo" value="$miscbacktwo" size=7 maxlength=7 onclick="javascript:selcolor(this,miscbacktwo2)" style="cursor:hand">　默认：#EEEEEE</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>表格颜色</center></b>
                <font color=#333333>这些颜色大部分用于leobbs.cgi，forums.cgi和topic.cgi
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带背景颜色</font></td>
                <td bgcolor=$catback  width=12 id=catback2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catback" value="$catback" size=7 maxlength=7 onclick="javascript:selcolor(this,catback2)" style="cursor:hand">　默认：#ebebFF</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>标题栏背景图片</font><BR>请输入图片名称，此图必须在 images 目录下的 $skin 里</td>
                <td background=$imagesurl/images/$skin/$catbackpic  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带背景图片</font><BR>请输入图片名称，此图必须在 images 目录下的 $skin 里</td>
                <td background=$imagesurl/images/$skin/$catsbackpicinfo  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catsbackpicinfo" value="$catsbackpicinfo"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带字体颜色</font></td>
                <td bgcolor=$catfontcolor  width=12 id=catfontcolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catfontcolor" value="$catfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,catfontcolor2)" style="cursor:hand">　默认：#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>所有表格边界颜色</font></td>
                <td bgcolor=$tablebordercolor  width=12 id=tablebordercolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablebordercolor" value="$tablebordercolor" size=7 maxlength=7 onclick="javascript:selcolor(this,tablebordercolor2)" style="cursor:hand">　默认：#000000</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>所有表格宽度</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="tablewidth" value="$tablewidth" size=5 maxlength=5>　默认：750</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>导航栏颜色</center></b>
                <font color=#333333>这里颜色配置用于设置快捷操作导航栏的颜色
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>导航栏边线颜色</font></td>
                <td bgcolor=$navborder width=12 id=navborder2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navborder" value="$navborder" size=7 maxlength=7 onclick="javascript:selcolor(this,navborder2)" style="cursor:hand">　默认：#E6E6E6</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>导航栏背景颜色</font></td>
                <td bgcolor=$navbackground width=12 id=navbackground2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navbackground" value="$navbackground" size=7 maxlength=7 onclick="javascript:selcolor(this,navbackground2)" style="cursor:hand">　默认：#F7F7F7</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>导航栏字体颜色</font></td>
                <td bgcolor=$navfontcolor width=12 id=navfontcolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="navfontcolor" value="$navfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,navfontcolor2)" style="cursor:hand">　默认：#4D76B3</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>标题颜色</center></b>
                <font color=#333333>这里颜色配置用于发表第一个主题的标题
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏背景颜色</font></td>
                <td bgcolor=$titlecolor  width=12 id=titlecolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlecolor" value="$titlecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,titlecolor2)" style="cursor:hand">　默认：#acbded</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>论坛/主题的标题栏字体颜色</font></td>
                <td bgcolor=$titlefontcolor  width=12 id=titlefontcolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titlefontcolor" value="$titlefontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,titlefontcolor2)" style="cursor:hand">　默认：#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛内容颜色</center></b>
                <font color=#333333>查看论坛内容时颜色 (forums.cgi)
                </td></tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色一</font></td>
                <td bgcolor=$forumcolorone  width=12 id=forumcolorone2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolorone" value="$forumcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,forumcolorone2)" style="cursor:hand">　默认：#f0F3Fa</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容颜色二</font></td>
                <td bgcolor=$forumcolortwo  width=12 id=forumcolortwo2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumcolortwo" value="$forumcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,forumcolortwo2)" style="cursor:hand">　默认：#F2F8FF</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>内容字体颜色</font></td>
                <td bgcolor=$forumfontcolor  width=12 id=forumfontcolor2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="forumfontcolor" value="$forumfontcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,forumfontcolor2)" style="cursor:hand">　默认：#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>回复颜色</center></b>
                <font color=#333333>回复贴子颜色(topic.cgi)
                </td></tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色一</font></td>
                <td bgcolor=$postcolorone  width=12 id=postcolorone2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolorone" value="$postcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,postcolorone2)" style="cursor:hand">　默认：#EFF3F9</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复颜色二</font></td>
                <td bgcolor=$postcolortwo  width=12 id=postcolortwo2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcolortwo" value="$postcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,postcolortwo2)" style="cursor:hand">　默认：#F2F4EF</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色一</font></td>
                <td bgcolor=$postfontcolorone  width=12 id=postfontcolorone2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolorone" value="$postfontcolorone" size=7 maxlength=7 onclick="javascript:selcolor(this,postfontcolorone2)" style="cursor:hand">　默认：#333333</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>回复字体颜色二</font></td>
                <td bgcolor=$postfontcolortwo  width=12 id=postfontcolortwo2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postfontcolortwo" value="$postfontcolortwo" size=7 maxlength=7 onclick="javascript:selcolor(this,postfontcolortwo2)" style="cursor:hand">　默认：#555555</td>
                </tr>
                
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>页面跨度</center></b><br>
                <font color=#333333>每页显示主题的回复数，当一篇主题回复超过一定数量时分页显示 (topic.cgi)
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每页主题数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxthreads" value="$maxthreads" size=3 maxlength=3>　一般为 20 -- 30</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每主题每页的回复数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtopics" value="$maxtopics" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复数超过多少后就是热门贴？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hottopicmark" value="$hottopicmark" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>投票数超过多少后就是热门投票贴？</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hotpollmark" value="$hotpollmark" size=3 maxlength=3>　一般为 10 -- 15</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"usehigest\"><option value=\"yes\">突出<option value=\"no\">不突出</select>\n";
        $tempoutput =~ s/value=\"$usehigest\"/value=\"$usehigest\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>是否突出最高票数的顶目？</font></td> 
               <td bgcolor=#FFFFFF>$tempoutput</td> 
               </tr> 

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>突出最高票数的顶目的文字颜色</font></td> 
               <td bgcolor=#FFFFFF> 
               <input type=text name="higestcolor" value="$higestcolor" size=7 maxlength=7 onclick="javascript:selcolor(this,higestcolor)" style="cursor:hand;background-color:$higestcolor">  默认：#0000FF</td> 
               </tr> 
               ~;

        $tempoutput = "<select name=\"higestsize\">\n<option value=\"3\">3\n<option value=\"4\">4\n<option value=\"5\">5\n<option value=\"6\">6\n</select>\n";
        $tempoutput =~ s/value=\"$higestsize\"/value=\"$higestsize\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>突出最高票数的顶目的文字大小</font></td> 
               <td bgcolor=#FFFFFF>$tempoutput  默认：3</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每页显示的表情图个数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxoneemot" value="$maxoneemot" size=3 maxlength=3>　默认为 15，如果不想分页，就设置为999</td>
                </tr>
               ~;

        print qq~
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>LeoBBS 标签设置</center></b>(坛主和版主不受此限)<br>
                </td></tr>
                ~;

        $tempoutput = "<select name=\"arrawpostpic\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawpostpic\"/value=\"$arrawpostpic\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许贴图？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawpostflash\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawpostflash\"/value=\"$arrawpostflash\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许 Flash？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawpostreal\"><option value=\"off\">不允许<option value=\"on\" >允许</select>\n";
        $tempoutput =~ s/value=\"$arrawpostreal\"/value=\"$arrawpostreal\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许 Real 文件？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawpostmedia\"><option value=\"off\">不允许<option value=\"on\" >允许</select>\n";
        $tempoutput =~ s/value=\"$arrawpostmedia\"/value=\"$arrawpostmedia\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许 Media 文件？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput
		</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawpostsound\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawpostsound\"/value=\"$arrawpostsound\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许声音文件？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawautoplay\">\n<option value=\"1\">允许\n<option value=\"0\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawautoplay\"/value=\"$arrawautoplay\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中的多媒体文件是否允许自动播放？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawpostfontsize\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawpostfontsize\"/value=\"$arrawpostfontsize\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子中是否允许改变文字大小？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"openiframe\">\n<option value=\"no\">不允许\n<option value=\"yes\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$openiframe\"/value=\"$openiframe\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333>论坛是否允许 Iframe 标签</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"boarddispsign\">\n<option value=\"yes\">默认显示\n<option value=\"noselect\">默认不显示\n<option value=\"no\">禁止显示\n</select>\n";
        $tempoutput =~ s/value=\"$boarddispsign\"/value=\"$boarddispsign\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否显示贴子中的签名？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawsignpic\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawsignpic\"/value=\"$arrawsignpic\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许贴图？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
        $tempoutput = "<select name=\"arrawsignflash\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawsignflash\"/value=\"$arrawsignflash\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许 Flash？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawsignsound\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawsignsound\"/value=\"$arrawsignsound\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许声音？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawsignfontsize\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrawsignfontsize\"/value=\"$arrawsignfontsize\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名中是否允许改变文字大小？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>帖子和签名中 Flash 默认大小</font></td>
                <td bgcolor=#FFFFFF>
                宽度： <input type=text name="defaultflashwidth" value="$defaultflashwidth" size=3 maxlength=3>　默认 410 像数<BR>
                高度： <input type=text name="defaultflashheight" value="$defaultflashheight" size=3 maxlength=3>　默认 280 像数</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛图像设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>自定义头像最大宽度</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxposticonwidth" value="$maxposticonwidth" size=3 maxlength=3>　请不要超过 110</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>自定义头像最大高度</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxposticonheight" value="$maxposticonheight" size=3 maxlength=3>　请不要超过 130</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>头像库默认图像宽度(为空则不限)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultwidth" value="$defaultwidth" size=3 maxlength=3>　默认 32 像数，如果为空，则不限制</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>头像库默认图像高度(为空则不限)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultheight" value="$defaultheight" size=3 maxlength=3>　默认 32 像数，如果为空，则不限制</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>表情符图像默认宽度(为空则不限)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsmilewidth" value="$defaultsmilewidth" size=3 maxlength=3>　默认 13 像数，如果为空，则不限制</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>表情符图像默认高度(为空则不限)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsmileheight" value="$defaultsmileheight" size=3 maxlength=3>　默认 13 像数，如果为空，则不限制</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否启用缩略图模式</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
        $tempoutput = qq~<select name=imgslt><option value="">不启用</option><option value="Disp">启用</option></select>~;
        $tempoutput =~ s/value=\"$imgslt\"/value=\"$imgslt\" selected/;
        print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>缩略图默认宽度(为空则默认为60)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsltwidth" value="$defaultsltwidth" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>缩略图像默认高度(为空则默认为60)</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="defaultsltheight" value="$defaultsltheight" size=3 maxlength=3></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>缩略图每行数量</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
        $tempoutput = qq~<select name=sltnoperline><option value="3">3</option><option value="1">1</option><option value="2">2</option><option value="4">4</option><option value="5">5</option><option value="6">6</option></select>~;
        $tempoutput =~ s/value=\"$sltnoperline\"/value=\"$sltnoperline\" selected/;
        print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>论坛特殊样式设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子文字显示大小</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
        $tempoutput = qq~<select name=postfontsize><option value="12">默认</option><option value="15">稍大</option><option value="18">普通</option><option value="21">较大</option><option value="24">很大</option><option value="30">最大</option></select>~;
        $tempoutput =~ s/value=\"$postfontsize\"/value=\"$postfontsize\" selected/;
        print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子段落间距调整</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
        $tempoutput = "<select name=\"paraspace\">\n<option value=\"130\">默认间距<option value=\"100\">单倍行距<option value=\"150\">1.5倍行距<option value=\"200\">双倍行距";
        $tempoutput =~ s/value=\"$paraspace\"/value=\"$paraspace\" selected/;
        print qq~
                $tempoutput
                </td>
                </tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>贴子字间距调整</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                ~;
        $tempoutput = "<select name=\"wordspace\">\n<option value=\"0\">默认间距<option value=\"-1\">紧缩<option value=\"+2\">扩充<option value=\"+4\">加宽";
        $wordspace =~ s/\+/\\+/;
        $tempoutput =~ s/value=\"$wordspace\"/value=\"$wordspace\" selected/;
        print qq~
                $tempoutput
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复时候默认列出的最后回复个数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxlistpost" value="$maxlistpost" size=2 maxlength=2>　一般 5 -- 8 个左右啦</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许加重帖子标题的主题数？<br>可以加重几个重要帖子的标题。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxhightopic" value="$maxhightopic" size=2 maxlength=2>　一般 10 -- 20 个左右啦</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>可以设定加重帖子的标题颜色!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_hightopic" value="$color_of_hightopic" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_hightopic)" style="cursor:hand;background-color:$color_of_hightopic">　推荐选择#990000</td>
              </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许总固定在所有论坛顶端的主题数？<br>可以总固定几个重要话题在所有论坛的最上面。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="absmaxtoptopic" value="$absmaxtoptopic" size=2 maxlength=2>　一般 1 -- 5 个左右啦</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>可以设定总固定贴子的主题颜色!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_absontop" value="$color_of_absontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_absontop)" style="cursor:hand;background-color:$color_of_absontop">　推荐选择#990000</td>
              </tr>
		~;

        $tempoutput = "<select name=\"abstopshake\">\n<option value=\"\">不采用任何方式\n<option value=\"1\">晃动\n<option value=\"2\">变色\n<option value=\"3\">反色\n</select>\n";
        $tempoutput =~ s/value=\"$abstopshake\"/value=\"$abstopshake\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>总固定贴子采用什么醒目方式？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许固定在某个区顶端的主题数？<br>可以区固定几个重要话题在区中所有论坛的最上面。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="absmaxcantopic" value="$absmaxcantopic" size=2 maxlength=2>　一般 1 -- 5 个左右啦</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>可以设定区固定贴子的主题颜色!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_quontop" value="$color_of_quontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_quontop)" style="cursor:hand;background-color:$color_of_quontop">　推荐选择#e7840d</td>
              </tr>
		~;

        $tempoutput = "<select name=\"cattopshake\">\n<option value=\"\">不采用任何方式\n<option value=\"1\">晃动\n<option value=\"2\">变色\n<option value=\"3\">反色\n</select>\n";
        $tempoutput =~ s/value=\"$cattopshake\"/value=\"$cattopshake\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>区固定贴子采用什么醒目方式？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
              <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许固定在顶端的主题数？<br>可以固定几个重要话题在论坛的最上面。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxtoptopic" value="$maxtoptopic" size=2 maxlength=2>　一般 1 -- 5 个左右啦</td>
                </tr>
		<tr>
              <td bgcolor=#FFFFFF colspan=2>
              <font color=#333333>可以设定固定贴子的主题颜色!</font></td>
              <td bgcolor=#FFFFFF>
              <input type=text name="color_of_ontop" value="$color_of_ontop" size=7 maxlength=7 onclick="javascript:selcolor(this,color_of_ontop)" style="cursor:hand;background-color:$color_of_ontop">　推荐选择#002299</td>
              </tr>
		~;

        $tempoutput = "<select name=\"topshake\">\n<option value=\"\">不采用任何方式\n<option value=\"1\">晃动\n<option value=\"2\">变色\n<option value=\"3\">反色\n</select>\n";
        $tempoutput =~ s/value=\"$topshake\"/value=\"$topshake\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>固定贴子采用什么醒目方式？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名允许的行数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsignline" value="$maxsignline" size=5 maxlength=2>　一般 5 行(和下面参数配合使用)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>签名的最多字符数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxsignlegth" value="$maxsignlegth" size=5 maxlength=4>　一般 200 个字</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>个人简介允许的行数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxinsline" value="$maxinsline" size=5 maxlength=2>　一般  5 行(和下面参数配合使用)</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>个人简介的最多字符数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxinslegth" value="$maxinslegth" size=5 maxlength=4>　一般 100 个字</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛投票贴子中允许的最大项目数</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpollitem" value="$maxpollitem" size=2 maxlength=2>　请设置 5 - 50 之间</td>
                </tr>

<tr>
<td bgcolor=#EEEEEE align=center colspan=3>
<font color=#990000><center><b>初始化特效设置</b> (leobbs.cgi & Forums.cgi)</center><br>
</font></td>
</tr>
~;

        $tempoutput = "<select name=\"pagechange\">\n<option value=\"no\">NO\n<option value=\"yes\">YES\n</select>\n";
        $tempoutput =~ s/value=\"$pagechange\"/value=\"$pagechange\" selected/;
        print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>调入页面时是否使用特效?</b><br>IE 4.0 以上版本浏览器有效</font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

        $tempoutput = "<select name=\"cinoption\">\n
<option value=\"0\">盒状收缩\n
<option value=\"1\">盒状放射\n
<option value=\"2\">圆形收缩\n
<option value=\"3\">圆形放射\n
<option value=\"4\">向上擦除\n
<option value=\"5\">向下擦除\n
<option value=\"6\">向右擦除\n
<option value=\"7\">向左擦除\n
<option value=\"8\">垂直遮蔽\n
<option value=\"9\">水平遮蔽\n
<option value=\"10\">横向棋盘式\n
<option value=\"11\">纵向棋盘式\n
<option value=\"12\">随机分解\n
<option value=\"13\">左右向中央缩进\n
<option value=\"14\">中央向左右扩展\n
<option value=\"15\">上下向中央缩进\n
<option value=\"16\">中央向上下扩展\n
<option value=\"17\">从左下抽出\n
<option value=\"18\">从左上抽出\n
<option value=\"29\">从右下抽出\n
<option value=\"20\">从右上抽出\n
<option value=\"21\">随机水平线条\n
<option value=\"22\">随机垂直线条\n
<option value=\"23\">随机(上面任何一种)\n
</select>\n";
        $tempoutput =~ s/value=\"$cinoption\"/value=\"$cinoption\" selected/;
        print qq~
<tr>
<td bgcolor=#FFFFFF colspan=2>
<font color=#333333><b>特效类型?</b></font></td>
<td bgcolor=#FFFFFF>
$tempoutput</td>
</tr>
~;

        print qq~

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b><center>其他设置</center></b><br>
                </td></tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认用户在线时间是多少分钟？<BR>如果用户超过这个时间还没有动作则默认用户已经离开了论坛。</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="membergone" value="$membergone" size=3 maxlength=3>　一般为 5 -- 15</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每天允许最多删除贴子次数？(对坛主无效)<br>如果不想限制,请设置为 999.</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxdeloneday" value="$maxdeloneday" size=3 maxlength=3>　一般 5 - 10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>每天允许最多移动帖子次数？(对坛主无效)<br>如果不想限制,请设置为 999.</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxmoveoneday" value="$maxmoveoneday" size=3 maxlength=3>  一般 5 - 10</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>多少小时内的新贴后面加 new 标志？<BR>(如果不想要，可以设置为 0)</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="newmarktime" value="$newmarktime" size=3 maxlength=3>　一般 12 - 24 小时</td>
                </tr>
		~;

        $tempoutput = "<select name=\"usetodayforumreply\">\n<option value=\"yes\">是的，记录\n<option value=\"no\">不，不记录\n</select>\n";
        $tempoutput =~ s/value=\"$usetodayforumreply\"/value=\"$usetodayforumreply\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>分论坛的今日新贴统计是否把回复也记录上</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"usejhpoint\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$usejhpoint\"/value=\"$usejhpoint\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>是否使用在精华帖子使用标记？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

        $tempoutput = "<select name=\"nodispown\">\n<option value=\"no\">不使用\n<option value=\"yes\">使用\n</select>\n";
        $tempoutput =~ s/value=\"$nodispown\"/value=\"$nodispown\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>是否标志显示自己发的帖子？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

        $tempoutput = "<select name=\"cancmodoutput\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
        $tempoutput =~ s/value=\"$cancmodoutput\"/value=\"$cancmodoutput\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>在首页是否显示区斑竹名单？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

        $tempoutput = "<select name=\"canuseview\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$canuseview\"/value=\"$canuseview\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>论坛是否允许新闻方式快速阅读？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;

        $tempoutput = "<select name=\"canusetreeview\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$canusetreeview\"/value=\"$canusetreeview\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>论坛是否允许使用快速展开回复？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
                ~;
        $maintopicad =~ s/\[br\]/\n/isg;
        $replytopicad =~ s/\[br\]/\n/isg;

        $tempoutput = "<select name=\"useads\">\n<option value=\"no\">不允许\n<option value=\"yes\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$useads\"/value=\"$useads\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>是否允许论坛帖子随机广告？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>帖子主题广告书写(如果没有，请留空)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="maintopicad" rows="5" cols="40">$maintopicad</textarea>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>帖子回复广告书写(如果没有，请留空)</font></td>
                <td bgcolor=#FFFFFF>
                <textarea name="replytopicad" rows="5" cols="40">$replytopicad</textarea>
                </td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许刷新论坛的时间间隔(秒)<BR>可以有效防止恶意刷新</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="banfreshtime" value="$banfreshtime" size=3 maxlength=3>　如果无需，请设置 0</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"look\">\n<option value=\"on\">开放\n<option value=\"off\">不开放\n</select>\n";
        $tempoutput =~ s/value=\"$look\"/value=\"$look\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否开放论坛配色？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"showskin\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$showskin\"/value=\"$showskin\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许用户自定义浏览论坛时的风格？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"announcemove\">\n<option value=\"on\">移动\n<option value=\"off\">不移动\n</select>\n";
        $tempoutput =~ s/value=\"$announcemove\"/value=\"$announcemove\" selected/;
        print qq~

               	<tr>
               	<td bgcolor=#FFFFFF colspan=2>
               	<font color=#333333>论坛公告是否采用移动风格？</font></td>
               	<td bgcolor=#FFFFFF>
               	$tempoutput</td>
               	</tr>
               	~;

        $tempoutput = "<select name=\"newmsgpop\"><option value=\"off\">不提示<option value=\"popup\">弹出<option value=\"light\">闪烁<option value=\"on\">两者均要</select>\n";
        $tempoutput =~ s/value=\"$newmsgpop\"/value=\"$newmsgpop\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>有新的短消息采用何种提示？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"payopen\"><option value=\"no\">不允许支付宝交易帖<option value=\"yes\">可以支付宝交易帖</select>\n";
        $tempoutput =~ s/value=\"$payopen\"/value=\"$payopen\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>打开论坛支付宝交易帖功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"pollopen\"><option value=\"yes\">打开投票<option value=\"no\">关闭投票</select>\n";
        $tempoutput =~ s/value=\"$pollopen\"/value=\"$pollopen\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>打开论坛投票功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"xzbopen\"><option value=\"yes\">打开小字报<option value=\"no\">关闭小字报</select>\n";
        $tempoutput =~ s/value=\"$xzbopen\"/value=\"$xzbopen\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>打开论坛小字报功能？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>允许发表的小字报的最多字数</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="hownews" value="$hownews" size=4 maxlength=4>　默认：100</td>
                </tr>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333><B>超过多少天的帖子不允许回复？</B></font><BR>以帖子最后一次回复时间计算</td>
               <td bgcolor=#FFFFFF>
               <input type=text name="rdays" value="$rdays" size=4 maxlength=4>　天 (如果无需，请留空)</td>
               </tr>
                ~;

        $tempoutput = "<select name=\"infosopen\"><option value=\"0\">任何人可以查看<option value=\"1\">注册用户可以查看<option value=\"2\">坛主和版主可以查看<option value=\"3\">只有坛主可以查看</select>\n";
        $tempoutput =~ s/value=\"$infosopen\"/value=\"$infosopen\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>列表排名资料查看开放方式？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"searchopen\">\n<option value=\"0\">允许任何人搜索\n<option value=\"1\">只允许注册会员以上级别搜索\n<option value=\"2\">只允许认证会员以上级别搜索<option value=\"3\">只允许版主以上级别搜索<option value=\"4\">只允许坛主搜索<option value=\"99\">关闭搜索</select>\n";
        $tempoutput =~ s/value=\"$searchopen\"/value=\"$searchopen\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>搜索帖子功能开放方式</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"searchall\">\n<option value=\"yes\">允许全文搜索\n<option value=\"no\">不允许全文搜索</select>\n";
        $tempoutput =~ s/value=\"$searchall\"/value=\"$searchall\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许全文搜索</font> 允许的话，全文搜索将很消耗资源(对坛主无限制)</td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"viewadminlog\">\n<option value=\"0\">允许任何人查看\n<option value=\"1\">只允许注册会员以上级别查看\n<option value=\"2\">只允许认证会员以上级别查看<option value=\"3\">只允许版主以上级别查看</select>\n";
        $tempoutput =~ s/value=\"$viewadminlog\"/value=\"$viewadminlog\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>版务日志功能开放方式</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"regaccess\"><option value=\"off\">不，允许任何人访问<option value=\"on\">是，必须登录后才能访问</select>\n";
        $tempoutput =~ s/value=\"$regaccess\"/value=\"$regaccess\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
                <font face=宋体 color=#333333>论坛只有注册用户可以访问？</font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"allowsearch\"><option value=\"no\">不允许<option value=\"yes\">允许</select>\n";
        $tempoutput =~ s/value=\"$allowsearch\"/value=\"$allowsearch\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
                <font face=宋体 color=#333333><B>是否允许搜索引擎直接访问？</B></font><BR>如果允许，那么即使设置了论坛只有注册用户<BR>才可以访问，但搜索引擎仍然能够搜索到论坛<br>非私有版块的内容以便提高新用户通过搜索引擎<br>访问到论坛的机会，此设定也可能会带来伪装<br>成搜索引擎身份的用户的访问!</td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"guestregistered\"><option value=\"on\">可以<option value=\"off\">不能</select>\n";
        $tempoutput =~ s/value=\"$guestregistered\"/value=\"$guestregistered\" selected/;
        print qq~
		<tr>
		<td bgcolor=#FFFFFF valign=middle align=left  colspan=2>
		<font face=宋体 color=#333333>客人能否查看贴子内容？</font></td>
		<td bgcolor=#FFFFFF valign=middle align=left>
		$tempoutput</td>
		</tr>
		~;

        $tempoutput = "<select name=\"pvtip\">\n<option value=\"on\">显示 IP 和鉴定\n<option value=\"off\">保密 IP 和鉴定\n</select>\n";
        $tempoutput =~ s/value=\"$pvtip\"/value=\"$pvtip\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><B>是否保密 IP 和鉴定？</B><BR>即使选择的是显示 IP，但普通用户还是<BR>只能看见 IP 的前两位</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对坛主无效</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"smocanseeip\">\n<option value=\"yes\">有效\n<option value=\"no\">无效\n</select>\n";
        $tempoutput =~ s/value=\"$smocanseeip\"/value=\"$smocanseeip\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333><b>保密 IP 和鉴定对总斑竹是否有效？</B><BR>如选择无效，则总版主可查看所有的 IP<BR>而不受上面 IP 保密的限制</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrowupload\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrowupload\"/value=\"$arrowupload\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>主题贴子是否允许上传？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对版主和坛主无效</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"allowattachment\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$allowattachment\"/value=\"$allowattachment\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>回复贴子是否允许上传？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能对版主和坛主无效</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛上传文件允许的最大值(单位：KB)<br>如果设置了不允许上传，则此项无效！</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxupload" value="$maxupload" size=5 maxlength=5>　不要加 KB，建议不要超过 500</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>用户上传文件必须达到的发贴总数<br>只对普通注册用户有效！坛主、斑竹和认证用户都不受此限制！</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="uploadreqire" value="$uploadreqire" size=4 maxlength=4>　如果不想限制，可以设置为0。</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"mastpostatt\">\n<option value=\"no\">可以不带附件\n<option value=\"yes\">必须带附件\n</select>\n";
        $tempoutput =~ s/value=\"$mastpostatt\"/value=\"$mastpostatt\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>新主题贴是否必须带附件？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput　此功能主要用于制作 BT 发布区</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发贴至少字符数，防止灌水<br>只对普通注册用户有效！坛主、斑竹和认证用户都不受此限制！</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="minpoststr" value="$minpoststr" size=2 maxlength=2>　如不想限制，可留空，不得多于 50。</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发贴允许的最多字符数<br>只对普通注册用户有效！坛主、斑竹和认证用户都不受此限制！</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="maxpoststr" value="$maxpoststr" size=5 maxlength=5>　如不想限制，可留空，不得少于 100。</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发短消息的最少在线时间<br>在线时间少于这个的无法发送短消息</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="onlinemessage" value="$onlinemessage" size=8 maxlength=8>　单位：秒，建议设置 600，如不想限制，就留空。</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发贴的最少在线时间<br>在线时间少于这个的无法发贴</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="onlinepost" value="$onlinepost" size=8 maxlength=8>　单位：秒，建议设置 600，如不想限制，就留空。</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrawrecordclick\">\n<option value=\"no\">不允许\n<option value=\"yes\">允许\n</select>";
        $tempoutput =~ s/value=\"$arrawrecordclick\"/value=\"$arrawrecordclick\" selected/;
        print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333>是否允许记录帖子访问情况</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>               
               ~;

        $tempoutput = "<select name=\"nowater\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n</select>";
        $tempoutput =~ s/value=\"$nowater\"/value=\"$nowater\" selected/;
        print qq~
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font color=#333333>是否允许发贴者对灌水进行限制</font></td>
               <td bgcolor=#FFFFFF>
               $tempoutput</td>
               </tr>               
               
	       <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=宋体 color=#333333><b>少于多少字符算灌水？</font></b><BR>如果上面选择不允许限制，那么此项无效！</td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="gsnum" value="$gsnum" size=5 maxlength=5>　不要加 byte，建议不要超过 50。</td>
               </tr>      
               ~;

        $tempoutput = "<select name=\"defaulttopicshow\"><option value=>查看所有的主题<option value=\"1\">查看一天内的主题<option value=\"2\">查看两天内的主题<option value=\"7\">查看一星期内的主题<option value=\"15\">查看半个月内的主题<option value=\"30\">查看一个月内的主题<option value=\"60\">查看两个月内的主题<option value=\"180\">查看半年内的主题</select>\n";
        $tempoutput =~ s/value=\"$defaulttopicshow\"/value=\"$defaulttopicshow\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认显示主题数</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"arrowavaupload\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrowavaupload\"/value=\"$arrowavaupload\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许上传自定义头像？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"arrowuserdel\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$arrowuserdel\"/value=\"$arrowuserdel\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许注册用户自己锁定或删除自己的贴子？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"usereditpost\"><option value=\"yes\">可以编辑自己的贴子<option value=\"no\">不可以编辑自己的贴子</select>\n";
        $tempoutput =~ s/value=\"$usereditpost\"/value=\"$usereditpost\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>论坛是否允许编辑？(对坛主、斑竹无效)</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"allowamoedit\">\n<option value=\"no\">不允许\n<option value=\"yes\">允许\n</select>\n";
        $tempoutput =~ s/value=\"$allowamoedit\"/value=\"$allowamoedit\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>副版主是否允许编辑本论坛下的帖子？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"onlineview\">\n<option value=\"1\">显示\n<option value=\"0\">不显示\n</select>\n";
        $tempoutput =~ s/value=\"$onlineview\"/value=\"$onlineview\" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认是否显示在线用户详细列表？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"advreg\">\n<option value=\"0\">简洁模式\n<option value=\"1\">高级模式\n</select>\n";
        $tempoutput =~ s/value=\"$advreg\"/value=\"$advreg\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>默认注册模式？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
               ~;

        $tempoutput = "<select name=\"advlogin\">\n<option value=\"0\">简洁模式\n<option value=\"1\">高级模式\n</select>\n";
        $tempoutput =~ s/value=\"$advlogin\"/value=\"$advlogin\" selected/;
        print qq~

               <tr> 
               <td bgcolor=#FFFFFF colspan=2> 
               <font color=#333333>默认登录模式？</font></td> 
               <td bgcolor=#FFFFFF> 
               $tempoutput</td> 
               </tr> 
               ~;

        $tempoutput = "<select name=\"sendwelcomemessage\">\n<option value=\"yes\">发送\n<option value=\"no\">不发送\n</select>\n";
        $tempoutput =~ s/value=\"$sendwelcomemessage\"/value=\"$sendwelcomemessage" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否发欢迎消息给新注册用户？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;

        $tempoutput = "<select name=\"refreshforum\">\n<option value=\"off\">不要自动刷新\n<option value=\"on\">要自动刷新\n</select>\n";
        $tempoutput =~ s/value=\"$refreshforum\"/value=\"$refreshforum" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>分论坛是否自动刷新(请在下面设置间隔时间)？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>自动刷新论坛的时间间隔(秒)<BR>配合上面参数一起使用</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="autofreshtime" value="$autofreshtime" size= 5 maxlength=5>　一般设置 5 分钟，就是 300 秒。</td>
                </tr>
		~;

        $tempoutput = "<select name=\"editusertitleself\">\n<option value=\"off\">不允许\n<option value=\"on\">允许\n<option value=\"post\">允许，但需要达到下面的积分数\n</select>\n";
        $tempoutput =~ s/value=\"$editusertitleself\"/value=\"$editusertitleself" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许用户自行修改个人头衔？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		<tr>
		<td bgcolor=#FFFFFF colspan=2>
		<font color=#333333>允许会员自行修改个人头衔需要达到的积分数</font></td>
		<td bgcolor=#FFFFFF>
		<input type=text name="needpoststitle" value="$needpoststitle" size=5 maxlength=5> 配合上一个的设置使用</td>
		</tr>
		~;

        $tempoutput = "<select name=\"editjhmpself\">\n<option value=\"off\">不允许\n<option value=\"system\">允许，但需从系统中选择\n<option value=\"on\">允许\n<option value=\"post\">允许，但需要达到下面的发言数\n</select>\n";
        $tempoutput =~ s/value=\"$editjhmpself\"/value=\"$editjhmpself" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否允许用户自行修改江湖门派？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		<tr>
		<td bgcolor=#FFFFFF colspan=2>
		<font color=#333333>允许会员自行修改江湖门派需要达到的发言数</font></td>
		<td bgcolor=#FFFFFF>
		<input type=text name="needpostsjhmp" value="$needpostsjhmp" size=5 maxlength=5> 配合上一个的设置使用</td>
		</tr>
		~;

        $tempoutput = "<select name=\"usenoimg\">\n<option value=\"no\">不使用\n<option value=\"yes\">使用\n</select>\n";
        $tempoutput =~ s/value=\"$usenoimg\"/value=\"$usenoimg" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否启用图片错误时自动修正？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"usefastpost\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$usefastpost\"/value=\"$usefastpost" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否启用快速发表主题？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"dispquickreply\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$dispquickreply\"/value=\"$dispquickreply" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>是否启用快速回复？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"waterwhenguest\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$waterwhenguest\"/value=\"$waterwhenguest" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>当客人浏览时，自动加水印？(同时将无法复制帖子)</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"sendmanageinfo\">\n<option value=\"no\">不通知用户\n<option value=\"yes\">通知用户\n</select>\n";
        $tempoutput =~ s/value=\"$sendmanageinfo\"/value=\"$sendmanageinfo" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>管理帖子（删除、移动、锁定、屏蔽等）后，<BR>是否发短消息通知用户？</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"treeview\">\n<option value=\"no\">平板显示贴子\n<option value=\"yes\">树形显示贴子\n</select>\n";
        $tempoutput =~ s/value=\"$treeview\"/value=\"$treeview" selected/;
        print qq~

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>默认帖子显示风格。</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"dispjump\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
        $tempoutput =~ s/value=\"$dispjump\"/value=\"$dispjump\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333>是否显示论坛跳转</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"dispchildforumnum\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
        $tempoutput =~ s/value=\"$dispchildforumnum\"/value=\"$dispchildforumnum\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333>是否在首页面显示子论坛个数</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"dispview\">\n<option value=\"yes\">显示\n<option value=\"no\">不显示\n</select>\n";
        $tempoutput =~ s/value=\"$dispview\"/value=\"$dispview\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>是否显示论坛图例</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"addtopictime\">\n<option value=\"no\">不添加\n<option value=\"yes\">添加\n</select>\n";
        $tempoutput =~ s/value=\"$addtopictime\"/value=\"$addtopictime\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>是否自动在主题前添加日期？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"abslink\">\n<option value=\"no\">不直接下载\n<option value=\"yes\">直接下载\n</select>\n";
        $tempoutput =~ s/value=\"$abslink\"/value=\"$abslink\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>图片附件是否使用直接下载方式？</b>此设置只针对图片，如果选择“直接下载”，那么防盗链和图片水印设置将无效！</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"pvtdown\">\n<option value=\"yes\">保护\n<option value=\"no\">不保护\n</select>\n";
        $tempoutput =~ s/value=\"$pvtdown\"/value=\"$pvtdown\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>是否保护附件下载地址，防止盗链？</b></font></td>
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

            $tempoutput = "<select name=\"picwater\">\n<option value=\"no\">不加水印\n<option value=\"yes\">加上水印\n</select>\n";
            $tempoutput =~ s/value=\"$picwater\"/value=\"$picwater\" selected/;
            print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>上传的 JPG 图片是否加上水印</b><BR>小于 200*40 的图片自动不加水印</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

            $watername = "http://bbs.leobbs.com/" if ($watername eq "");

            $tempoutput = "<select name=\"picwaterman\">\n<option value=\"0\">只对客人显示\n<option value=\"1\">对客人和普通用户显示\n<option value=\"2\">对客人、普通用户和认证用户显示<option value=\"3\">除了坛主外，其他用户都显示\n</select>\n";
            $tempoutput =~ s/value=\"$picwaterman\"/value=\"$picwaterman\" selected/;
            print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>显示水印对象的附加设置</b><BR>只有打开水印功能后，此项目才有效</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
            if ($picwaterplace1 eq "yes") {$checked1 = "checked";}
            else {$checked1 = "";}
            if ($picwaterplace2 eq "yes") {$checked2 = "checked";}
            else {$checked2 = "";}
            if ($picwaterplace3 eq "yes") {$checked3 = "checked";}
            else {$checked3 = "";}
            if ($picwaterplace4 eq "yes") {$checked4 = "checked";}
            else {$checked4 = "";}
            $tempoutput = qq~<input type="checkbox" name="picwaterplace1" value="yes" $checked1> 左上角　　<input type="checkbox" name="picwaterplace2" value="yes" $checked2> 左下角<BR><input type="checkbox" name="picwaterplace3" value="yes" $checked3> 右上角　　<input type="checkbox" name="picwaterplace4" value="yes" $checked4> 右下角<BR>~;
            print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>水印显示的位置</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
        <tr>
        <td bgcolor=#FFFFFF colspan=2>
        <font color=#333333>图片水印名称<BR>注：水印图必须为 PNG 格式，如果留空则使用文字水印<br>请输入图片名称，此图必须在 myimages 目录下<BR><b>请不要包含 URL 地址或绝对路径！</b></font></td>
        <td bgcolor=#FFFFFF>
        <input type=text size=20 name="waterpic" value="$waterpic">
~;

            opendir(DIR, "${imagesdir}myimages");
            @thd = readdir(DIR);
            closedir(DIR);
            @thd = grep (/png$/i, @thd);
            my $myimages = "";
            $topiccount = @thd;
            @thd = sort @thd;
            for (my $i = 0; $i < $topiccount; $i++) {
                next if (($thd[$i] eq ".") || ($thd[$i] eq ".."));
                $myimages .= qq~<option value="$thd[$i]">$thd[$i]~;
            }
            $myimages =~ s/value=\"$action\"/value=\"$action\" selected/;
            print qq~
<script>
function select(){
document.FORM.waterpic.value=FORM.image.value;
if (FORM.waterpic.value != "") {
document.bbsimg.src = "$imagesurl/myimages/"+FORM.image.value;
} else {
document.bbsimg.src = "$imagesurl/myimages/blank.gif";
}
}
</script>
<select name="image" onChange=select()><option value="">不使用图片水印$myimages</select><BR>
<IMG border=0 name=bbsimg src="$imagesurl/myimages/blank.gif" align="absmiddle" onload="javascript:if(this.width>document.body.clientWidth-333)this.width=document.body.clientWidth-333">
<script>
if (FORM.waterpic.value != "") {
document.bbsimg.src = "$imagesurl/myimages/"+FORM.waterpic.value;
}
</script>

</td>
        </tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>上传的 JPG 图片上水印的文字<BR>注：<font color=red>不能用中文</font>，也不要过长，否则影响效果<BR>如果上面图片水印名称存在，则此设置无效</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="watername" value="$watername" size=30></td>
                </tr>
		~;
        }
        else {
            print qq~<input type=hidden name="picwater" value="no">~;
        }
        $tempoutput = "<select name=\"wwjf\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$wwjf\"/value=\"$wwjf\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>论坛是否使用威望限制制度</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
                ~;
        $tempoutput = "<select name=\"cansale\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$cansale\"/value=\"$cansale\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>分论坛是否使用帖子买卖制度</b></font></td>
                <td bgcolor=#FFFFFF valign=middle align=left>
                $tempoutput</td>
                </tr>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=宋体 color=#333333><b>帖子买卖最大数目</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="moneymax" value="$moneymax" size=6 maxlength=6> 默认 99999，最大 999999 </td>
               </tr>
               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=宋体 color=#333333><b>帖子买卖交纳税率</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="postcess" value="$postcess" size=5 maxlength=5> %</td>
               </tr>
               ~;

        $tempoutput = "<select name=\"postjf\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$postjf\"/value=\"$postjf\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>论坛是否使用发帖量标签</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"jfmark\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$jfmark\"/value=\"$jfmark\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>论坛是否使用积分查看标签</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"noviewjf\">\n<option value=\"no\">可以进入，但无法看保密的内容\n<option value=\"yes\">无法进入该帖\n</select>\n";
        $tempoutput =~ s/value=\"$noviewjf\"/value=\"$noviewjf\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>当主帖含有积分标签，那么达不到积分要求的会员．．？</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"hidejf\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$hidejf\"/value=\"$hidejf\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>论坛是否使用保密帖子标签</b>（回复后才能看到帖子内容）</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"usewm\">\n<option value=\"yes\">使用\n<option value=\"no\">不使用\n</select>\n";
        $tempoutput =~ s/value=\"$usewm\"/value=\"$usewm\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>论坛是否使用自动水印</b>（帖子标题含原创字样时自动加水印）</font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"usecurl\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$usecurl\"/value=\"$usecurl\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>论坛是否允许使用加密链接</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"rssinfo\">\n<option value=\"yes\">允许\n<option value=\"no\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$rssinfo\"/value=\"$rssinfo\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>论坛是否允许使用 RSS 功能</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>
		~;

        $tempoutput = "<select name=\"magicface\">\n<option value=\"on\">允许\n<option value=\"off\">不允许\n</select>\n";
        $tempoutput =~ s/value=\"$magicface\"/value=\"$magicface\" selected/;
        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font face=宋体 color=#333333><b>论坛是否允许使用魔法表情功能</b></font></td>
                <td bgcolor=#FFFFFF>
                $tempoutput</td>
                </tr>

               <tr>
               <td bgcolor=#FFFFFF colspan=2>
               <font face=宋体 color=#333333><b>一次奖惩积分最大数量</b></font></td>
               <td bgcolor=#FFFFFF valign=middle align=left>
               <input type=text name="max1jf" value="$max1jf" size=3 maxlength=3> 默认： 50</td>
               </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发表主帖的最小积分数<BR>小于此积分的，不能发帖，注意：这个数字必须是大于 0 的。</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postminjf" value="$postminjf" size=10 maxlength=10>　注意用半角，前后不要有空格，如不想限制，就留空或设 0 。</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发表回复的最小积分数<BR>小于此积分的，不能回复，注意：这个数字必须是大于 0 的。</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="replyminjf" value="$replyminjf" size=10 maxlength=10>　注意用半角，前后不要有空格，如不想限制，就留空或设 0 。</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>发起投票的最小积分数<BR>小于此积分的，不能发投票帖，注意：这个数字必须是大于 0 的。</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="pollminjf" value="$pollminjf" size=10 maxlength=10>　注意用半角，前后不要有空格，如不想限制，就留空或设 0 。</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>进行投票的最小积分数<BR>小于此积分的，不能对投票帖进行投票，注意：这个数字必须是大于 0 的。</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="polledminjf" value="$polledminjf" size=10 maxlength=10>　注意用半角，前后不要有空格，如不想限制，就留空或设 0 。</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>帖子中的签名上方加入文章版权的文字<BR>如果不需要，请设置为空白</font><BR><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="postcopyright" value="$postcopyright" size=30>　<BR>默认：版权所有，不得擅自转载</td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>主论坛标题图片(支持 Flash) <br>此图必须在 myimages 目录下，只能是名称，不可以加 URL 地址或绝对路径</font><BR></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="boardlogo" value="$boardlogo"><BR></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>主论坛标题 Flash 图片大小<BR>(仅当标题图片是 Flash 时有效，控制在 160*60 以内)<BR></td>
                <td bgcolor=#FFFFFF>
                宽度：<input type=text name="boardlogow" value="$boardlogow" size=3 maxlength=3>　 高度：<input type=text name="boardlogoh" value="$boardlogoh" size=3 maxlength=3><BR></td>
                </tr>
               <tr>
               <td bgcolor=#EEEEEE align=center colspan=3>
               <font color=#990000><b><center>自定义认证用户分类(如果不需要，请全部留空)</center></b>
               </td></tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员名称一</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz1" value="$defrz1"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员在线图例一</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline1" value="$defrzonline1" onChange="definerz1.src='$imagesurl/images/'+this.value"> <img id=definerz1 src=$imagesurl/images/$defrzonline1> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员团队图案一</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic1" value="$defrzpic1" onChange="definerz11.src='$imagesurl/images/'+this.value"> <img id=definerz11 src=$imagesurl/images/$defrzpic1> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员名称二</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz2" value="$defrz2"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员在线图例二</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline2" value="$defrzonline2" onChange="definerz2.src='$imagesurl/images/'+this.value"> <img id=definerz2 src=$imagesurl/images/$defrzonline2> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员团队图案二</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic2" value="$defrzpic2" onChange="definerz22.src='$imagesurl/images/'+this.value"> <img id=definerz22 src=$imagesurl/images/$defrzpic2> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员名称三</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz3" value="$defrz3"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员在线图例三</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline3" value="$defrzonline3" onChange="definerz3.src='$imagesurl/images/'+this.value"> <img id=definerz3 src=$imagesurl/images/$defrzonline3> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员团队图案三</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic3" value="$defrzpic3" onChange="definerz33.src='$imagesurl/images/'+this.value"> <img id=definerz33 src=$imagesurl/images/$defrzpic3> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员名称四</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz4" value="$defrz4"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员在线图例四</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline4" value="$defrzonline4" onChange="definerz4.src='$imagesurl/images/'+this.value"> <img id=definerz4 src=$imagesurl/images/$defrzonline4> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员团队图案四</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic4" value="$defrzpic4" onChange="definerz44.src='$imagesurl/images/'+this.value"> <img id=definerz44 src=$imagesurl/images/$defrzpic4> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员名称五</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrz5" value="$defrz5"></td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员在线图例五</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzonline5" value="$defrzonline5" onChange="definerz5.src='$imagesurl/images/'+this.value"> <img id=definerz5 src=$imagesurl/images/$defrzonline5> 必须放置于 non-cgi/images下</td>
               </tr>

               <tr>
               <td bgcolor=#FFFFFF>
               <font face=宋体 color=#333333><b>认证会员团队图案五</b></font></td>
               <td bgcolor=#FFFFFF colspan=2>
               <input type=text size=20 name="defrzpic5" value="$defrzpic5" onChange="definerz55.src='$imagesurl/images/'+this.value"> <img id=definerz55 src=$imagesurl/images/$defrzpic5> 必须放置于 non-cgi/images下</td>
               </tr>
<tr>
              <td bgcolor=#EEEEEE align=center colspan=3>
              <font color=#990000><b><center>社区版块权限管理</center></b>
              </td></tr>

              <tr>
              <td bgcolor=#FFFFFF>
              <font face=宋体 color=#333333><b>允许访问论坛的成员组</b><br>适合所有版块，如要设置单独版块，请进入“论坛设置和管理”/“添加该区风格”<BR>如果不需要这个功能，请全部不要选择(或者全部选择，效果一样)！</font></td>
              <td bgcolor=#FFFFFF colspan=2>~;
        my $memteam1 = qq~<input type=checkbox name="yxz" value="rz1">$defrz1(认证用户)<br>~ if ($defrz1 ne "");
        my $memteam2 = qq~<input type=checkbox name="yxz" value="rz2">$defrz2(认证用户)<br>~ if ($defrz2 ne "");
        my $memteam3 = qq~<input type=checkbox name="yxz" value="rz3">$defrz3(认证用户)<br>~ if ($defrz3 ne "");
        my $memteam4 = qq~<input type=checkbox name="yxz" value="rz4">$defrz4(认证用户)<br>~ if ($defrz4 ne "");
        my $memteam5 = qq~<input type=checkbox name="yxz" value="rz5">$defrz5(认证用户)<br>~ if ($defrz5 ne "");
        $all = qq~<input type=checkbox name="yxz" value="">客人<br><input type=checkbox name="yxz" value="me">一般用户<br>$memteam1$memteam2$memteam3$memteam4$memteam5
<input type=checkbox name="yxz" value="rz">认证用户<br>
<input type=checkbox name="yxz" value="banned">禁止此用户发言<br>
<input type=checkbox name="yxz" value="masked">屏蔽此用户贴子<br>
<input type=checkbox name="yxz" value="mo">论坛版主<br>
<input type=checkbox name="yxz" value="amo">论坛副版主<br>
<input type=checkbox name="yxz" value="cmo">分类区版主<br>
<input type=checkbox name="yxz" value="smo">论坛总版主<br>
<input type=checkbox name="yxz" value="ad">坛主<br>~;
        my @yxz = split(/\,/, $yxz);
        foreach (@yxz) {
            chomp;
            next if ($_ eq '');
            $all =~ s/<input type=checkbox name="yxz" value="$_"/<input type=checkbox name="yxz" value="$_" checked/g;
        }
        print qq~
$all
              </td>
              </tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <input type=submit value="提 交"></td></form></tr></table></td></tr></table>
                ~;
    }
}
else {
    &adminlogin;
}

print qq~</td></tr></table></body></html>~;
exit;
