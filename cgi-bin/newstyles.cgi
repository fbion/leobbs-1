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
$LBCGI::POST_MAX=50000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
$query = new LBCGI;

require "admin.lib.pl";
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";

$|++;

$thisprog = "newstyles.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");

	@params = $query->param;
	foreach (@params) {
		$theparam = $query->param($_);
	$theparam =~ s/\\/\\\\/g;
        $theparam =~ s/\@/\\\@/g;
        $theparam =~ s/"//g;
        $theparam = &unHTML("$theparam");
		${$_} = $theparam;
        if ($_ ne 'action') {
        	$_ =~ s/[\n\r]//isg;
        	$theparam =~ s/[\n\r]//isg;
            $printme .= "\$" . "$_ = \'$theparam\'\;\n" if ($_ ne "");
            }
	}

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;

&getmember("$inmembername","no");
        

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
            
    if ($action eq "delstyle") {
        print qq~
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>警告！！</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=#333333>将删除您所选定的名称为 <b>$skinname</b> 的论坛风格，不可恢复<p>
        <p>
        >> <a href="$thisprog?action=delstyleok&skinname=$skinname">确定删除</a> <<
        </td></tr>
        </table></td></tr></table>
        ~;
    }
    elsif ($action eq "delstyleok") {
        $filetomake = "$lbdir" . "data/skin/$skinname.cgi";
    	unlink $filetomake;
                    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 风格删除</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#EEEEEE align=center colspan=2>
                    <font color=#333333><b>所有信息已经保存</b><br>该风格已经完全删除。
                    </td></tr></table></td></tr></table>
                    ~;

    }

    elsif ($action eq "process") {

        $savename=$query->param('savename');
        if ($savename eq "") {$savename=$query->param('skin')}

        $printme .= "1\;\n";
	$printme =~ s/\$skin.+?\n/\$skin = \"$savename\";\n/isg;

        $filetomake = "$lbdir" . "data/skin/$savename.cgi";

        &winlock($filetomake) if ($OS_USED eq "Nt");
        open(FILE,">$filetomake");
        flock(FILE,2) if ($OS_USED eq "Unix");
        print FILE "$printme";
        close(FILE);
        &winunlock($filetomake) if ($OS_USED eq "Nt");

        if (-e $filetomake && -w $filetomake) {
                print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 风格设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE colspan=2>
                <font color=#333333><center><b>所有设置已经成功保存！</b><br><br>
                </center></td></tr></table></td></tr></table>~;
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
                if ($action ne ""){
                $stylefile = "$lbdir" . "data/skin/$action.cgi";
                if (-e $stylefile) {
         	require $stylefile;
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
        $myskin.=qq~<option value="$thd[$i]">皮肤 [ $thd[$i] ]~;
        }
        $myskin =~ s/value=\"$action\"/value=\"$action\" selected/;
                $inmembername =~ s/\_/ /g;
	$skinname=$query->param('action');
                print qq~
                <tr><td bgcolor=#2159C9 colspan=3><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 风格设置</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#333333><b>新建设定风格</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF width=40% colspan=2>
                <font color=#333333><b>引用系统自带的风格</b><br>您选择后，需要正式确定引用才生效</font></td>
                <td bgcolor=#FFFFFF>
                <form action="$thisprog" method="post" name=skin>
                <select name="action">
                <option value="">默认风格$myskin
                </select>
                <input type=submit value="引 用">　<input type=button value="删 除" onclick="location.href='$thisprog?action=delstyle&skinname=$skinname'">
                </form>
                </td></tr>
                <form action="$thisprog" method="post">
                <input type=hidden name="action" value="process">
                <input type=hidden name="skin" value=$skinname>
<tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>配色名称</font></td><td bgcolor=#FFFFFF><input type=text name="cssname" size=10 value="$cssname"></td></tr><tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>配色作者</font></td><td bgcolor=#FFFFFF><input type=text name="cssmaker" size=10 value="$cssmaker"></td></tr><tr><td bgcolor=#FcFcFc colspan=2 align=right><font color=#333333>配色简介</font></td><td bgcolor=#FFFFFF><textarea cols=40 name="cssreadme" rows=2>$cssreadme</textarea>
</td></tr>
                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>论坛BODY标签</b>
                </font></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>控制整个论坛风格的背景颜色或者背景图片等</font></td>
                <td bgcolor=#FFFFFF>
                <input type=text name="lbbody" size=40 value="$lbbody"><br>默认：bgcolor=#FFFFFF  alink=#333333 vlink=#333333 link=#333333 topmargin=0 leftmargin=0</td>
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
                <td bgcolor=$menufontcolor  width=12 id=menufontcolor2>　</td>
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
                <font color=#333333>菜单带背景图片</font><BR>请输入图片名称，此图必须在 myimages 目录下</td>
                <td background=$imagesurl/myimages/$menubackpic  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="menubackpic" value="$menubackpic"></td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF width=40%>
                <font color=#333333>菜单带边界颜色</font></td>
                <td bgcolor=$titleborder  width=12 id=titleborder2>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="titleborder" value="$titleborder" size=7 maxlength=7 onclick="javascript:selcolor(this,titleborder2)" style="cursor:hand">　默认：#333333</td>
                </tr>

                <tr>
                <td bgcolor=#EEEEEE align=center colspan=3>
                <font color=#990000><b>字体外观和颜色</b>
                </font></td>
                </tr>
                
                
                <tr>
                <td bgcolor=#FFFFFF colspan=2>
                <font color=#333333>主字体外观</font></td>
                <td bgcolor=#FFFFFF>
                ~;
                $tempoutput = "<select name=\"font\">\n<option value=\"宋体\">宋体\n<option value=\"仿宋\">仿宋\n<option value=\"楷体\">楷体\n<option value=\"黑体\">黑体\n<option value=\"隶书\">隶书\n<option value=\"幼圆\">幼圆\n</select><p>\n";
                $tempoutput =~ s/value=\"$font\"/value=\"$font\" selected/;
                print qq~
                $tempoutput</td>
                </tr>
                
                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>"最后发贴者"字体颜色</font></td>
                <td bgcolor=$lastpostfontcolor  width=12 id=lastpostfontcolor2>　</td>
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
                $tempoutput = "<select name=\"posternamefont\">\n<option value=\"宋体\">宋体\n<option value=\"仿宋\">仿宋\n<option value=\"楷体\">楷体\n<option value=\"黑体\">黑体\n<option value=\"隶书\">隶书\n<option value=\"幼圆\">幼圆\n</select><p>\n";
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
                <font color=#990000><b><center>所有页面颜色</center></b><br>
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
                <font color=#990000><b><center>表格颜色</center></b><br>
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
                <font color=#333333>标题栏背景图片</font><BR>请输入图片名称，此图必须在 myimages 目录下</td>
                <td background=$imagesurl/myimages/$catbackpic  width=12>　</td>
                <td bgcolor=#FFFFFF>
                <input type=text name="catbackpic" value="$catbackpic"></td>
                </tr>

                <tr>
                <td bgcolor=#FFFFFF>
                <font color=#333333>分类带背景图片</font><BR>请输入图片名称，此图必须在 myimages 目录下</td>
                <td background=$imagesurl/myimages/$catsbackpicinfo  width=12>　</td>
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
                <font color=#990000><b><center>标题颜色</center></b><br>
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
                <font color=#990000><b><center>论坛内容颜色</center></b><br>
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
                <font color=#990000><b><center>回复颜色</center></b><br>
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
<b>另存为风格名称</b> <input type=text name=savename size=16> (如不填写则为修改该配色)<br>
                <input type=submit value="确 定">　<input type=button value="取 消"></td></form></tr></table></td></tr></table>
                ~;
                }
                }
                else {
                    &adminlogin;
                    }
        
print qq~</td></tr></table></body></html>~;
exit;
