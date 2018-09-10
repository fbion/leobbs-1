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
require "bbs.lib.pl";

$|++;

$thisprog = "setad.cgi";

$query = new LBCGI;

#&ipbanned; #封杀一些 ip

$inmembername = $query->cookie("adminname");
$inpassword = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

@params = $query->param;
foreach $param (@params) {
    $theparam = $query->param($param);
    $theparam = &cleaninput("$theparam");
    $PARAM{$param} = $theparam;
}

$action = $PARAM{'action'};
$adsid = $PARAM{'forum'};

$new_adtype = $PARAM{'adtype'};
$new_adstypecolor = $PARAM{'adstypecolor'};
$new_adsinfo = $PARAM{'adsinfo'};
$new_adscolor = $PARAM{'adscolor'};
$new_adstyle = $PARAM{'adstyle'};
$new_adsurl = $PARAM{'adsurl'};
$new_adsmessage = $PARAM{'adsmessage'};
$new_adsmessage =~ s/<P>/<BR><BR>/isg;
$new_adsmessage =~ s/<BR>$//isg;
$new_adtypestyle = $PARAM{'adtypestyle'};
$checkaction = $PARAM{'checkaction'};

&getadmincheck;
print header(-charset => "UTF-8", -expires => "$EXP_MODE", -cache => "$CACHE_MODES");

&admintitle;

&getmember("$inmembername", "no");

if (($membercode eq "ad") && ($inpassword eq $password) && ($password ne "") && ($inmembername ne "") && (lc($inmembername) eq lc($membername))) {
    #s1

    my %Mode = (
        'addads'     => \&addads,
        'processnew' => \&createads,
        'edit'       => \&editads,
        'doedit'     => \&doedit,
    );

    if ($Mode{$action}) {
        $Mode{$action}->();
    }
    elsif (($action eq "delete") && ($checkaction ne "yes")) {&warning;}
    elsif (($action eq "delete") && ($checkaction eq "yes")) {&deleteads;}
    else {&adslist;}

} #e1

else {
    &adminlogin;
}

sub adslist {
    print qq~
    <tr><td bgcolor=#2159C9 colspan=3><font face=宋体 color=#FFFFFF>
    <b>欢迎来到论坛管理中心 / 论坛广告管理</b>
    </td></tr>
    <tr><td bgcolor=#FFFFFF colspan=3><font face=宋体 color=#333333>
    <b>注意事项：</b><br><br>
    在下面，您将看到目前所有的论坛广告(以实际效果显示)。<BR>
    您可以编辑论坛广告名或是增加一个新的论坛广告。 也可以编辑或删除目前存在的论坛广告。<br>
    </td></tr>
            <tr>
            <td bgcolor=#FFFFFF colspan=3 ><font face=宋体 color=#333333><hr noshade>
            </td></tr>
            <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=宋体 color=#333333>
       <a href="$thisprog?action=addads">增加新的论坛广告</a></font></td>
            </td></tr>
       
       ~;

    $filetoopen = "$lbdir" . "data/ads.cgi";
    open(FILE, "$filetoopen");
    my @bbsads = <FILE>;
    close(FILE);

    foreach $bbsads (@bbsads) {
        #start foreach @finalsortedforums
        $adtypestyle1 = $adtypestyle2 = $adstyle1 = $adstyle2 = "";
        ($adtype, $adstypecolor, $adtypestyle, $adsinfo, $adscolor, $adstyle, $adsurl, $adsmessage) = split(/\t/, $bbsads);
        $adsnum++;
        $adsinfo = &HTML("$adsinfo");
        $adsmessage = $adsinfo if ($adsinfo eq "");
        $adtypestyle1 = "<$adtypestyle>" if ($adtypestyle ne "");
        $adtypestyle2 = "</$adtypestyle>" if ($adtypestyle ne "");
        $adstyle1 = "<$adstyle>" if ($adstyle ne "");
        $adstyle2 = "</$adstyle>" if ($adstyle ne "");
        $adsinfo =~ s/\'/\\\'/isg;
        $adsmessage =~ s/\'/\\\'/isg;
        $adtype =~ s/\'/\\\'/isg;
        $adsmessage =~ s/<br>/\n/isg;
        $adtype = "<font color=$adstypecolor>${adtypestyle1}[$adtype]${adtypestyle2}</font> " if ($adtype ne "");

        print qq~
                <tr>
                <td bgcolor=#FFFFFF colspan=3 align=left><hr noshade width=70%><font face=宋体 color=#333333>
                <b>论坛广告内容</b>： $adtype<a href=$adsurl title="$adsmessage">$adstyle1<font color=$adscolor>$adsinfo</font>$adstyle2</a><BR><b>论坛广告 URL</b>： $adsurl<br>
                <br><a href="$thisprog?action=edit&forum=$adsnum">编辑此论坛广告</a> | <font face=宋体 color=#333333><a href="$thisprog?action=delete&forum=$adsnum">删除此论坛广告</a> </font></td>
                </font></td></tr>
                ~;

    } # end foreach


    print qq~
        <td bgcolor=#FFFFFF colspan=3 ><font face=宋体 color=#333333><hr noshade>
        </td></tr>
             <tr>
            <td bgcolor=#EEEEEE width=20% nowrap><font face=宋体 color=#333333>
       <a href="$thisprog?action=addads">增加新的论坛广告</a></font></td>
            </td></tr>
        </tr></table></td></tr></table>~;

} # end routine.

sub addads {

    print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 增加论坛广告</b>
        </td></tr>
        ~;

    print qq~
<script>
function selcolor(obj,obj2){
var arr = showModalDialog("$imagesurl/editor/selcolor.html", "", "dialogWidth:18.5em; dialogHeight:17.5em; status:0");
obj.value=arr;
obj2.style.backgroundColor=arr;
}
</script>
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="processnew">       
	<tr>
	<td bgcolor=#FFFFFF valign=middle align=left width=40%>
	<font color=#333333><b>广告类型</b><br>请输入广告类型，一般2-4个字，可留空<BR></font></td>
	<td bgcolor=#FFFFFF valign=middle align=left>
	<input type=text size=8 maxlength=8 name="adtype" value="广告"></td>
	</tr>
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40% id=adstypecolor>
        <font face=宋体 color=#333333><b>广告类型的颜色</b><br></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text name="adstypecolor" value="$adstypecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,adstypecolor)" style="cursor:hand; background-color:$adstypecolor"></td>
        </tr>
	<tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40% id=adscolor>
        <font face=宋体 color=#333333><b>广告类型样式</b><br>将作为广告类型显示的样式</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
	<input type=radio name="adtypestyle" value="" checked>正常 
	<input type=radio name="adtypestyle" value="b"><b>粗体</b> 
	<input type=radio name="adtypestyle" value="u"><u>下滑线</u> 
	<input type=radio name="adtypestyle" value="i"><i>斜体</i></td>
	</tr>
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>广告的简介</b><br>注意：支持 HTML 格式书写</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="adsinfo" value=""></td>
        </tr>       
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40% id=adscolor>
        <font face=宋体 color=#333333><b>广告简介的颜色</b><br></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text name="adscolor" value="$adscolor" size=7 maxlength=7 onclick="javascript:selcolor(this,adscolor)" style="cursor:hand; background-color:$adscolor"></td>
        </tr>
	<tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40% id=adscolor>
        <font face=宋体 color=#333333><b>简介样式</b><br>将作为广告简介显示的样式</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
	<input type=radio name="adstyle" value="" checked>正常 
	<input type=radio name="adstyle" value="b"><b>粗体</b> 
	<input type=radio name="adstyle" value="u"><u>下滑线</u> 
	<input type=radio name="adstyle" value="i"><i>斜体</i></td>
	</tr>
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>广告连接的 URL</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="adsurl" value="http://"></td>
        </tr>   
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>广告说明</b></font><BR>如果为空，则等于广告的简介</td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <textarea cols="40" rows="4" name="adsmessage">$adsmessage</textarea></td>
        </tr>   
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
        ~;

} # end route   


##################################################################################
######## Subroutes ( Create Forum )


sub createads {
    &errorout("广告的内容不能为空！！") if ($new_adsinfo eq "");
    $new_adsurl =~ s!http://!!ig;
    $new_adsurl =~ s! !!ig;
    &errorout("广告地址不能空！！") if ($new_adsurl eq "");
    $new_adsurl = "http://" . $new_adsurl;
    $filetoopen = "$lbdir" . "data/ads.cgi";
    open(FILE, "$filetoopen");
    my @forums = <FILE>;
    close(FILE);
    $new_adsmessage = $new_adsinfo if ($new_adsmessage eq "");

    open(FILE, ">$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    foreach $line (@forums) {
        chomp $line;
        print FILE "$line\n";
    }
    print FILE "$new_adtype\t$new_adstypecolor\t$new_adtypestyle\t$new_adsinfo\t$new_adscolor\t$new_adstyle\t$new_adsurl\t$new_adsmessage\t";
    close(FILE);
    &createadsjs;
    print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 增加论坛广告结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                <font face=宋体 color=#333333>
                ~;

    print "<b>详细资料</b><p>\n";
    print "<ul>\n";

    print "新论坛广告已经建立！";

    print "</ul></td></tr></table></td></tr></table>\n";

} ######## end routine

##################################################################################
######## Subroutes ( Warning of Delete Forum )  

sub warning { #start

    print qq~
        <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 删除论坛广告</b>
        </td></tr>
        <tr>
        <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
        <font face=宋体 color=#990000><b>警告！！</b>
        </td></tr>
        
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <font face=宋体 color=#333333>如果您确定要删除这个论坛广告，那么请点击下面链接<p>
        >> <a href="$thisprog?action=delete&checkaction=yes&forum=$adsid">删除论坛广告</a> <<
        </td></tr>
        </table></td></tr></table>
        
        ~;

} # end routine     

##################################################################################
######## Subroutes ( Deletion of a Forum )  

sub deleteads {
    #start

    $filetoopen = "$lbdir" . "data/ads.cgi";
    open(FILE, "$filetoopen");
    my @forums = <FILE>;
    close(FILE);

    open(FILE, ">$filetoopen");
    $forumname = 0;
    foreach $forum (@forums) {
        chomp $forum;
        next if ($forum eq "");
        $forumname++;
        unless ($adsid eq $forumname) {
            print FILE "$forum\n";
        }
    }
    close(FILE);

    &createadsjs;

    print qq~
                    <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                    <b>欢迎来到论坛管理中心 / 删除广告结果</b>
                    </td></tr>
                    <tr>
                    <td bgcolor=#FFFFFF valign=middle align=left colspan=2>
                    <font face=宋体 color=#990000>
                    
                    <center><b>此论坛广告已被删除</b>，请刷新论坛广告管理页后再继续操作！</center><p>
                    
                  
                                    
                    </td></tr></table></td></tr></table>
                    ~;

} # routine ends

######## Subroutes ( Editing of a Forum )   
sub editads {

    $filetoopen = "$lbdir" . "data/ads.cgi";
    open(FILE, "$filetoopen");
    flock(FILE, 2) if ($OS_USED eq "Unix");
    @ads = <FILE>;
    close(FILE);
    ($adtype, $adstypecolor, $adtypestyle, $adsinfo, $adscolor, $adstyle, $adsurl, $adsmessage) = split(/\t/, $ads[$adsid - 1]);

    $adstyle{$adstyle} = " checked";
    $adtypestyle{$adtypestyle} = " checked";
    $adsmessage =~ s/<br>/\n/isg;

    print qq~
<script>
function selcolor(obj,obj2){
var arr = showModalDialog("$imagesurl/editor/selcolor.html", "", "dialogWidth:18.5em; dialogHeight:17.5em; status:0");
obj.value=arr;
obj2.style.backgroundColor=arr;
}
</script>
        <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
        <b>欢迎来到论坛管理中心 / 编辑论坛广告</b>
        </td></tr>
       
                
        <form action="$thisprog" method="post">
        <input type=hidden name="action" value="doedit">
        <input type=hidden name="forum" value="$adsid">
	<tr>
	<td bgcolor=#FFFFFF valign=middle align=left width=40%>
	<font color=#333333><b>广告类型</b><br>请输入广告类型，一般2-4个字，可留空<BR></font></td>
	<td bgcolor=#FFFFFF valign=middle align=left>
	<input type=text size=8 maxlength=8 name="adtype" value="$adtype"></td>
	</tr>
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40% id=adstypecolor>
        <font face=宋体 color=#333333><b>广告类型的颜色</b><br></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text name="adstypecolor" value="$adstypecolor" size=7 maxlength=7 onclick="javascript:selcolor(this,adstypecolor)" style="cursor:hand; background-color:$adstypecolor"></td>
        </tr>
	<tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40% id=adscolor>
        <font face=宋体 color=#333333><b>广告类型样式</b><br>将作为广告类型显示的样式</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
	<input type=radio name="adtypestyle" value="" checked>正常 
	<input type=radio name="adtypestyle" value="b"$adtypestyle{b}><b>粗体</b> 
	<input type=radio name="adtypestyle" value="u"$adtypestyle{u}><u>下滑线</u> 
	<input type=radio name="adtypestyle" value="i"$adtypestyle{i}><i>斜体</i></td>
	</tr>
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>广告的简介</b><br>注意：支持 HTML 格式书写</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 maxlength=50 name="adsinfo" value="$adsinfo"></td>
        </tr>       
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40% id=adscolor>
        <font face=宋体 color=#333333><b>广告简介的颜色</b><br></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text name="adscolor" value="$adscolor" size=7 maxlength=7 onclick="javascript:selcolor(this,adscolor)" style="cursor:hand; background-color:$adscolor"></td>
        </tr>
	<tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40% id=adscolor>
        <font face=宋体 color=#333333><b>简介样式</b><br>将作为广告简介显示的样式</font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
	<input type=radio name="adstyle" value="" checked>正常 
	<input type=radio name="adstyle" value="b"$adstyle{b}><b>粗体</b> 
	<input type=radio name="adstyle" value="u"$adstyle{u}><u>下滑线</u> 
	<input type=radio name="adstyle" value="i"$adstyle{i}><i>斜体</i></td>
	</tr>
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>广告连接的 URL</b></font></td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <input type=text size=40 name="adsurl" value="$adsurl"></td>
        </tr>   
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=left width=40%>
        <font face=宋体 color=#333333><b>广告说明</b></font><BR>如果为空，则等于广告的简介</td>
        <td bgcolor=#FFFFFF valign=middle align=left>
        <textarea cols="40" rows="4" name="adsmessage">$adsmessage</textarea></td>
        </tr>   
        <tr>
        <td bgcolor=#FFFFFF valign=middle align=center colspan=2>
        <input type=submit value="提 交"></form></td></tr></table></td></tr></table>
        ~;

} # end route   

##################################################################################
######## Subroutes ( Processing the edit of a forum)    


sub doedit {
    &errorout("广告的内容不能为空！！") if ($new_adsinfo eq "");
    $new_adsurl =~ s!http://!!ig;
    $new_adsurl =~ s! !!ig;
    &errorout("广告地址不能空！！") if ($new_adsurl eq "");
    $new_adsurl = "http://" . $new_adsurl;
    $new_adsmessage = $new_adsinfo if ($new_adsmessage eq "");

    $filetoopen = "$lbdir" . "data/ads.cgi";
    open(FILE, "$filetoopen");
    my @ads = <FILE>;
    close(FILE);

    $editedline = "$new_adtype\t$new_adstypecolor\t$new_adtypestyle\t$new_adsinfo\t$new_adscolor\t$new_adstyle\t$new_adsurl\t$new_adsmessage\t";
    chomp $editedline;

    $filetoopen = "$lbdir" . "data/ads.cgi";
    open(FILE, ">$filetoopen");
    $tempadsid = 0;
    foreach $ads (@ads) {
        chomp $ads;
        $tempadsid++;
        if ($tempadsid eq $adsid) {
            print FILE "$editedline\n";
        }
        else {
            print FILE "$ads\n";
        }
    }
    close(FILE);
    &createadsjs;

    print qq~
                <tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
                <b>欢迎来到论坛管理中心 / 编辑论坛广告结果</b>
                </td></tr>
                <tr>
                <td bgcolor=#EEEEEE valign=middle align=center colspan=2>
                <font face=宋体 color=#333333><b>所有信息已经保存</b><p>
                
                </td></tr></table></td></tr></table>
                ~;

} # end routine


print qq~</td></tr></table></body></html>~;
exit;

sub errorout {
    print qq~
<tr><td bgcolor=#2159C9 colspan=2><font face=宋体 color=#FFFFFF>
<b>欢迎来到论坛管理中心 / 发生错误</b>
</td></tr><tr>
<td bgcolor=#FFFFFF valign=middle align=left colspan=2>
<font face=宋体 color=#333333>
<font face=宋体 color=#333333><b>$_[0]</b>
</td></tr></table></td></tr></table>
~;
    exit;
}

sub createadsjs {
    open(FILE, "${lbdir}data/ads.cgi");
    my @ads = <FILE>;
    close(FILE);
    $adsnum = @ads;
    if ($adsnum >= 1) {
        $adsjscode = qq~var arNews = [~;

        foreach $ads (@ads) {
            chomp $ads;
            next if ($ads eq "");
            $adtypestyle1 = $adtypestyle2 = $adstyle1 = $adstyle2 = "";
            ($adtype, $adstypecolor, $adtypestyle, $adsinfo, $adscolor, $adstyle, $adsurl, $adsmessage) = split(/\t/, $ads);
            $adsinfo = &HTML("$adsinfo");
            $adsmessage = $adsinfo if ($adsinfo eq "");
            $adtypestyle1 = "<$adtypestyle>" if ($adtypestyle ne "");
            $adtypestyle2 = "</$adtypestyle>" if ($adtypestyle ne "");
            $adstyle1 = "<$adstyle>" if ($adstyle ne "");
            $adstyle2 = "</$adstyle>" if ($adstyle ne "");
            $adsmessage =~ s/<br>/\\n/isg;
            $adtype = "<font color=$adstypecolor>${adtypestyle1}[$adtype]${adtypestyle2}</font> " if ($adtype ne "");

            $adsjscode .= qq~'$adtype<a href=$adsurl title="$adsmessage" target=_blank>$adstyle1<font color=$adscolor>$adsinfo</font>$adstyle2</a>',~;
        }
        chop($adsjscode);
        $adsjscode .= qq~];
var status = 0;
function LeoShow(){
for (i=0;i<LeoBBSgg.length;i++){
var addisplay=LeoBBSgg[i];
if (status==0){
var place=Math.round(Math.random()*(arNews.length)-0.5);addisplay.innerHTML = arNews[place];
}
else{
addisplay.innerHTML="<!-- -->";
}}
if (status==0){
status = 1;setTimeout("LeoShow()",4000);
}
else{
status = 0;setTimeout("LeoShow()",600);
}}
LeoShow();
~;

        open(FILE, ">${imagesdir}leogg.js");
        print FILE $adsjscode;
        close(FILE);
    }
    else {unlink("${imagesdir}leogg.js");}
}
