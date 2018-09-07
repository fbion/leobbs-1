#!/usr/bin/perl
#####################################################
#  首页Js调用向导
#  By maiweb 2005-08-05
#  leobbs-vip.com
#####################################################

BEGIN {
	push @INC, '.';
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use LBCGI;
use strict;
use warnings;
$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "admin.lib.pl";
require "data/boardinfo.cgi";
require "bbs.lib.pl";
$|++;

$thisprog = "indexshow.cgi";

$query = new LBCGI;

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&getadmincheck;
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&admintitle;
          
    &getmember("$inmembername","no");
    if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
    	for('allnews','news','newsjh','mainlogin','showmem','info','getanc','getanc2')
    	{
    		if(!(-e "${lbdir}$_.cgi")){$$_=0;}else{$$_=1;}
    	$a.="var $_ = $$_;\n";
    	}
    	
    	require "${lbdir}data/outputbutton.pl" if (-e "${lbdir}data/outputbutton.pl");
		$outputbutton =~ s/\<\!\-\-h (.+?) \-\-\>/$1/isg;
		$outputbutton =~ s/\<\!\-\-c (.+?) \-\-\>/$1/isg;
    	$outputbutton =~s/"//isg;
    	$outputbutton =~s/\n//isg;
print qq~<script>
var realurl = '';
$a
	function selcolor(obj2){
		var arr = showModalDialog("$imagesurl/editor/selcolor.html", "", "dialogWidth:18.5em; dialogHeight:17.5em; status:0");
		arr = arr.replace(/#/g,"");
		obj2.value=arr;
	}
	function nextstep(){
		FORM.outScript.value='';
		var aad = eval(FORM.D1.value);
		if(aad==0){
		ts.innerHTML ='<font color=red>你所要调用的功能缺少文件！请把你在官方下载的完整压缩包里面的addon目录下面的<b><u>'+FORM.D1.value+'.cgi</u></b>文件上传到cgi-bin目录下面，然后<b>刷新</b>本页继续！</font>';
		formshow.innerHTML ='';
		FORM.tj.disabled = true;
		return false;
		}else{
		ts.innerHTML ='请根据下面的步骤一步步进行！';
		FORM.tj.disabled = false;
		}
		
		if(FORM.D1.value =='news'||FORM.D1.value =='newsjh'){
			formshow.innerHTML ='2，选择要调用的版块<br><br><select size="1" name="forum"><option value="">选择要调用的版块$outputbutton</select><br><br>';
		}
		else if(FORM.D1.value =='allnews'){
			formshow.innerHTML ='2，帖子后面是否显示作者<br><br><select size="1" name="name"><option value="">帖子后面是否显示作者<option value=1>显示发帖者<option value=0>不显示发帖者</select><br><br>';
		}
		else if(FORM.D1.value =='getanc'){
		formshow.innerHTML ='2，输入调用的公告长度<br><br><input type=text size=4 name=max><br><br>';return;
		}
		else if(FORM.D1.value =='showmem'){
		formshow.innerHTML ='2，输入调用的会员数目<br><br><input type=text size=4 name=show><br><br>';return;
		}
		else if(FORM.D1.value =='getanc2'){
		formshow.innerHTML ='2，选择要调用的版块<br><br><select size="1" name="forum"><option value="">选择要调用的版块$outputbutton</select><br><br>3，公告的标题长度<br><br><input type=text size=2 name=maxlength><br><br>4，显示的公告数量<br><br><input type=text size=2 name=max><br><br>';return;
		}
		else{
			formshow.innerHTML ='';return;
		}
			formshow.innerHTML +='3，输入调用的数量:<input type=text size=4 name=max>';
			formshow.innerHTML +=' 4，帖子标题长度:<input type=text size=4 name=maxlength><br><br>';
			formshow.innerHTML +='5，帖子后面是否显示发表时间<br><br><select size="1" name="display"><option value=1>显示发帖时间<option value=0>不显示发帖时间</select><br><br>';
			formshow.innerHTML +='6，打开模式<br><br><select size="1" name="mode"><option value=view>新闻模式<option value=topic>论坛模式</select><br><br>';
			formshow.innerHTML +='7，颜色<br><br>超链接的颜色:<input type=text size=6 name=link  onclick="javascript:selcolor(link)"> 已访问过的超链接:<input type=text size=6 name=vlink  onclick="javascript:selcolor(vlink)"> 当前超链接:<input type=text size=6 name=alink  onclick="javascript:selcolor(alink)"><br><br>';
	}
	function checkForm(thisform){
		var baseurl = '$boardurl/'+thisform.D1.value+'.cgi';
		realurl = baseurl;
		if(thisform.D1.value=='news'||thisform.D1.value=='newsjh'||thisform.D1.value=='getanc2'){
		if(thisform.forum.value==''){
		alert('请务必选择调用的版块！');
		thisform.forum.focus();
		return false;
		}
		else{
		realurl +='?forum='+ thisform.forum.value;}
		}
		if(thisform.D1.value=='allnews'){
		if(thisform.name.value==''){
		alert('请务必选择调用是否选择发帖作者！');
		thisform.name.focus();
		return false;
		}else{
		realurl +='?name='+ thisform.name.value;}
		}
		if(thisform.D1.value=='getanc2'){
		if(thisform.maxlength.value==''){
		alert('请务必输入调用的公告标题长度！如 30');
		thisform.maxlength.focus();
		return false;
		}else{
		realurl +='?maxlength='+thisform.maxlength.value;
		}
		if(thisform.max.value==''){
		alert('请务必输入调用的公告数量！ 如 10');
		thisform.max.focus();
		return false;
		}else{
		realurl +='&show='+thisform.max.value;
		}
		}
		if(thisform.D1.value!='mainlogin'&&thisform.D1.value!='getanc2'&&thisform.D1.value!='info'){
		if(thisform.D1.value=='showmem'){
		if(thisform.show.value==''){
		alert('请务必输入调用的会员数目！如 10');
		thisform.show.focus();
		return false;
		}else{
		realurl +='?show='+thisform.show.value;
		}}else{
		if(thisform.D1.value=='getanc'){
		if(thisform.max.value==''){
		alert('请务必输入调用的公告长度！如 500');
		thisform.max.focus();
		return false;
		}else{
		realurl +='?max='+thisform.max.value;
		}
		}else{
		if(thisform.max.value==''){
		alert('请务必输入调用的帖子数量！如 10');
		thisform.max.focus();
		return false;
		}else{
		realurl +='&max='+thisform.max.value;
		}
		if(thisform.maxlength.value==''){
		alert('请务必输入调用的帖子长度！如 30');
		thisform.maxlength.focus();
		return false;
		}else{
		realurl +='&maxlength='+thisform.maxlength.value;
		}
		realurl +='&display='+thisform.display.value;
		realurl +='&mode='+thisform.mode.value;
		if(thisform.link.value !=''){
		realurl +='&link='+thisform.link.value;
		}
		if(thisform.vlink.value !=''){
		realurl +='&vlink='+thisform.vlink.value;
		}
		if(thisform.alink.value !=''){
		realurl +='&alink='+thisform.alink.value;
		}}
		}
		}
		var tmp = '<scr';
		tmp += 'ipt type="text/javasc';
		tmp += 'ript" src="'+realurl+'"></s';
		tmp += 'cript>';
		realurl = tmp; 
		thisform.outScript.value = realurl; return false;
	} 
	function HighlightAll(theField) {
		var tempval=eval("document."+theField)
		tempval.select()
		therange=tempval.createTextRange()
		therange.execCommand("Copy")
		alert('Copy ok!')
	}
</SCRIPT>
	<tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
                <b>欢迎来到论坛管理中心</b>
                </td></tr>
                <tr>
                <td bgcolor=#FFFFFF colspan=2>	<form onsubmit="return checkForm(this);" method=post name=FORM>
    <b>提示：</b><br><span id=ts>请根据下面的步骤一步步进行！</span><p>
   1，请选择你要调用的类型：<p>
                <select size="1" name="D1" onchange="if(this.options[this.selectedIndex].value!=''){nextstep();}">
  <option selected value=''>选择你要调用的类别</option>
  <option value="allnews">全论坛最新帖子调用</option>
  <option value="news">分论坛最新帖子调用</option>
  <option value="newsjh">分论坛精华帖子调用</option>
  <option value="mainlogin">论坛登陆框调用</option>
  <option value="getanc">论坛最新公告调用</option>
  <option value="getanc2">分论坛最新公告调用</option>
  <option value="info">论坛基本信息调用</option>
  <option value="showmem">论坛发帖排行</option></p>
  &nbsp;
</select><p><span id=formshow></span><textarea rows="5" name="outScript" cols="28" readonly disabled></textarea><br>
<br>
<button type=submit name=tj disabled>生成代码</button> <button name=copy onClick=HighlightAll('FORM.outScript')>拷贝代码</button>
</form><p><br><br></p><p align=center>&copy CopyRight By Maiweb 2005-08-05</p></td></tr>~;
	}
	else {
	    &adminlogin;
	}
print qq~</td></tr></table></body></html>~;
exit;
