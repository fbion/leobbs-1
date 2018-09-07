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
$LBCGI::POST_MAX=500000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "data/styles.cgi";
require "bbs.lib.pl";
require "face/config.pl";
$|++;
$query = new LBCGI;
$thisprog = "editface.cgi";

if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
    $boardurltemp =$boardurl;
    $boardurltemp =~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
    $cookiepath = $boardurltemp;
    $cookiepath =~ s/\/$//;
}

$inmembername = $query->cookie("amembernamecookie");
$inpassword   = $query->cookie("apasswordcookie");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

&error("普通错误&老大，别乱黑我的程序呀！") if (($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));

if ($inmembername eq "" || $inmembername eq "客人" ) {
    &error("不能进入 $plugname &你目前的身份是访客，请先登陆!");
    exit;
} else {
#    &getmember("$inmembername");
    &getmember("$inmembername","no");
    &error("普通错误&此用户根本不存在！") if ($userregistered eq "no");
     if ($inpassword ne $password) {
	$namecookie  = cookie(-name => "amembernamecookie", -value => "", -path => "$cookiepath/");
	$passcookie  = cookie(-name => "apasswordcookie",   -value => "", -path => "$cookiepath/");
        print header(-cookie=>[$namecookie, $passcookie] , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
        &error("普通错误&密码与用户名不相符，请重新登录！");
     }
}

$tempmembername = $membername;
$tempmembername =~ s/ /\_/g;
$tempmembername =~ tr/A-Z/a-z/;
$admin_user =~ s/ /\_/g;
$admin_user =~ tr/A-Z/a-z/;

&error("$plugname 编辑管理&只有论坛坛主与插件管理员才能进入此区！") if (($membercode ne "ad")&&($admin_user ne "$tempmembername"));

print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
print qq~
<html>
<head>
<title>$plugname - 编辑管理</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style>
A:visited{TEXT-DECORATION: none}
A:active{TEXT-DECORATION: none}
A:hover{TEXT-DECORATION: underline overline}
A:link{text-decoration: none;}
.t{LINE-HEIGHT: 1.4}
TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: 宋体; FONT-SIZE: 9pt} 
INPUT{BORDER-TOP-WIDTH: 1px; PADDING-RIGHT: 1px; PADDING-LEFT: 1px; BORDER-LEFT-WIDTH: 1px; FONT-SIZE: 9pt; BORDER-LEFT-COLOR: #cccccc; BORDER-BOTTOM-WIDTH: 1px; BORDER-BOTTOM-COLOR: #cccccc; PADDING-BOTTOM: 1px; BORDER-TOP-COLOR: #cccccc; PADDING-TOP: 1px; HEIGHT: 18px; BORDER-RIGHT-WIDTH: 1px; BORDER-RIGHT-COLOR: #cccccc}
textarea, select {border-width: 1; border-color: #000000; background-color: #efefef; font-family: 宋体; font-size: 9pt; font-style: bold;}
</style>
</head>
<body bgcolor="#ffffff" topmargin=0 leftmargin=0>
<table width=100% cellpadding=6 cellspacing=0 style="border:1 solid #555555;">~;
$action = $query -> param('action');

my %Mode = ('edit_sp' => \&edit_sp,'editok' => \&editok,'del_sp' => \&del_sp);

if ($Mode{$action})
{$Mode{$action} -> ();}
else{&error("$plugname&老大，别乱黑我的程序呀！");}

sub edit_sp
{
    $num       = $query -> param('num');	# 商品类别文件
    $id        = $query -> param('id');		# 商品的ID号
$num =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$id =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$num.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    $numid = $num;

    &errorout("1","找不到指定的商品！") if($sort !~ /$id\t(.*)/);	# 找到指定的商品ID

    ($sp_name,$sp_money,$sp_description,$sp_wear,$sp_fitherd,$sp_graphic,$sp_sxgraphic,$x,$x)=split(/\t/,$1);

    print qq~<tr><td bgcolor="#333333" height="20"><font color=#FFFFFF><b>虚拟形象管理 / 编辑商品</b></td></tr></table>~;

    if($sp_suit eq 'Y')
    {
	@taoinfo=split(/\_/,$sp_suitid);
	$numid = @taoinfo[0];
    }
    $tempoutput = "<input type=radio name=newfit value=\"m\"> 男 <input type=radio name=newfit value=\"f\"> 女 <input type=radio name=newfit value=\"t\"> 通用";
    $tempoutput =~ s/value=\"$sp_fitherd\"/value=\"$sp_fitherd\" checked/;

    opendir (DIR, "${imagesdir}face/$numid");
    @thd = readdir(DIR);
    closedir (DIR);
    my $myimages="";
    $topiccount = @thd;
    @thd=sort @thd;
    for (my $i=0;$i<$topiccount;$i++){
        next if (($thd[$i] eq ".")||($thd[$i] eq ".."));
        $myimages.=qq~<option value="$thd[$i]">$thd[$i]~;
    }
    $myimages =~ s/value=\"$action\"/value=\"$action\" selected/;        

    print qq~
<script>
function select(){
document.FORM.newgraphic.value=FORM.image.value;
document.dtdemo.src = "$imagesurl/face/$numid/"+FORM.image.value;}
function select1(){
document.FORM.newsxgraphic.value=FORM.image2.value;
document.xtdemo.src = "$imagesurl/face/$numid/"+FORM.image2.value;}
</script>
<table cellPadding=0 cellSpacing=2 width=100%>
<form action="$thisprog" method="post" name=FORM>
<input type=hidden name="action" value="editok">
<input type=hidden name="class" value="$num">
<input type=hidden name="id" value="$id">
  <TR bgColor=#eeeeee align=center><TD width=84>小图</TD><TD width=140>大图</TD><TD>商品资料</TD></TR>
  <TR bgColor=#eeeeee>
    <TD rowSpan=9><img border=0 name=xtdemo src=$imagesurl/face/$numid/$sp_sxgraphic width=84 hegiht=84></TD>
    <TD rowSpan=9><img border=0 name=dtdemo src=$imagesurl/face/$numid/$sp_graphic width=140 hegiht=226></TD>
    <TD height=20>商品名称：<input type=text size=20 name=newname value="$sp_name"></TD>
  </TR>
  <TR><TD bgColor=#eeeeee height=20>商品描述：<input type=text size=20 name=newdescription value="$sp_description"></TD></TR>
  <TR><TD bgColor=#eeeeee height=20>商品单价：<input type=text size=20 name=newmoney value="$sp_money"></TD></TR>
  <TR><TD bgColor=#eeeeee height=20>适用人群：$tempoutput</TD></TR>
  <TR><TD bgColor=#eeeeee height=20>商品图片：<input type=text size=10 name=newgraphic value="$sp_graphic">
<select name="image" onChange=select()><option value="$sp_graphic">选择图片$myimages</select></TD></TR>
  <TR><TD bgColor=#eeeeee height=20>商品小图：<input type=text size=10 name=newsxgraphic value="$sp_sxgraphic">
<select name="image2" onChange=select1()><option value="$sp_sxgraphic">选择图片$myimages</select></TD></TR>
  <TR><TD bgColor=#eeeeee height=20 align=center><input type=submit value="我 要 修 改"> <input type=reset value=重　置></TD></TR>
</form>
</TABLE>~;
#  <TR><TD bgColor=#eeeeee height=20>商品寿命：<input type=text size=20 name=newwear value="$sp_wear"></TD></TR>
}

sub editok{
    $class	= $query -> param('class');		# 商品类别号
    $id		= $query -> param('id');		# 商品ID号
$class =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$id =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    $newname	= $query -> param('newname');			# 商品名称
    $newmoney	= $query -> param('newmoney');			# 商品价格
    $newdescription	= $query -> param('newdescription');	# 商品描述
    $newdescription	= &unHTML("$newdescription");
    $newwear	= $query -> param('newwear');			# 商品寿命
    $newwear	= &unHTML("$newwear");
    $newfit	= $query -> param('newfit');			# 适合人群
    $newgraphic	= $query -> param('newgraphic');		# 商品大图
    $newgraphic	= &unHTML("$newgraphic");
    $newsxgraphic	= $query -> param('newsxgraphic');	# 商品小图
    $newsxgraphic	= &unHTML("$newsxgraphic");

    &errorout("0","商品的名称不能为空！") if ($newname eq '');
    &errorout("0","商品的价格不能为空！") if ($newmoney eq '');
    &errorout("0","商品价格中含有非法字符或不是整数！") unless ($newmoney=~ /^[0-9]+$/);
    &errorout("0","请正确输入商品单价！价格不能为负数！") if($newmoney < 0);
    &errorout("0","商品描述不能为空！") if ($newdescription eq '');
#    &errorout("0","商品耐久字中含有非法字符或不是整数！") unless ($newwear=~ /^[0-9]+$/);
#    &errorout("0","请正确输入商品的耐久度！不能为零或负数！") if($newwear <= 0);
    &errorout("0","商品的图片地址不能为空！") if ($newgraphic eq '');
    &errorout("0","商品的图片地址不能为空！") if ($newsxgraphic eq '');

    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$class.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    if($sort =~ /$id\t(.*)/)	# 找到指定的商品ID
    {
	$sort =~ s/$1/$newname\t$newmoney\t$newdescription\t$newwear\t$newfit\t$newgraphic\t$newsxgraphic\t\t/;
	open(FILE,">$filetoopen");
	print FILE $sort;
	close(FILE);
    }

print qq~
<script>opener.location.reload();</script>
<tr>
<td bgcolor=#EEEEEE align=center>
<font color=#990000 size=1><b>修改成功！3秒后返回！</b></font>
</td>
</tr></table><meta http-equiv="refresh" content="3; url=$thisprog?action=edit_sp&num=$class&id=$id">~;
exit;
}

sub del_sp
{
    $num        = $query -> param('num');	# 商品类别文件
    $id        = $query -> param('id');		# 商品的ID号
$num =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$id =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;

    $/="";
    my $filetoopen = "$lbdir" . "face/wpdata/$num.pl";
    open(FILE,"$filetoopen");
    my $sort=<FILE>;
    close(FILE);
    $/="\n";

    if($sort =~ s/$id\t(.*)\n//)	# 找到指定的商品ID
    {
	open(FILE,">$filetoopen");
	print FILE $sort;
	close(FILE);
    }
    else
    {
	&errorout("1","这件商品已经不存在！");
    }

    print qq~<script>opener.location.reload();setTimeout("self.close()",3000);</script>
<tr><td bgcolor=#EEEEEE align=center><font color=#990000 size=1><b>删除成功！3秒后本窗口自动关闭！</b></font></td></tr>
</table>~;
    exit;
}

sub errorout{
    my($errortype,$errormsg)=@_;
    if($errortype eq 1)
    {
	print qq~<script>alert("$errormsg");self.close();</script>~;
    }
    else
    {
	print qq~<script>alert("$errormsg");history.back();</script>~;
    }
    exit;
}