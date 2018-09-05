#!/usr/bin/perl
#########################
# 手机论坛WAP版
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
require "data/boardinfo.cgi";
require "wap.pl";
$check = $query -> param('check');
$lid = $query -> param('lid');
&waptitle;
$show.= qq~<card  title="$boardname-登陆">~;
if($check eq 'loginout'){
	unlink "${lbdir}wap/$lid";
	$show.= qq~<p>成功注销$inmembername，您过去的书签将不能再直接免登陆</p><p><a href='wap.cgi'>返回首页</a></p>~;&wapfoot;
}
my $xh2 = $ENV{'REMOTE_ADDR'};
$show.=  qq~<p><b>登录$boardname</b> <br/>您的手机IP：$xh2<br/>如果您在手机上无法输入ID进行登陆，请记住上面IP，进入论坛（loginwap.cgi）生成免登陆Url。<br/>\n</p><p>账号：<input type="text" name="n1" value="$a1"/><br/>\n</p><p>密码：<input type='password' name="p" value="$b1"/><br/>\n</p><p>
<anchor>[登录]<go href="wap_index.cgi" method="post">
<postfield name="n1" value="\$(n1)"/>
<postfield name="p" value="\$(p)"/>
</go>
</anchor> <a href="wap_index.cgi">[客人]</a> <a href="wap_reg.cgi">[注册]</a>~;
$show.=  qq~
</p>~;
&wapfoot;
