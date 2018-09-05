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
require "data/boardinfo.cgi";
require "wap.pl";
&waptitle;
$show.= qq~\n<card  title="$boardname-注册">\n ~;
$show.= qq~<p><b>在$boardname注册</b>\n</p><p>注册账号：<input type="text" name="n"/>\n</p><p>注册密码：<input type='password' name="p"/>\n</p><p>重复密码：<input type='password' name="p1"/>\n</p><p>邮件地址：<input type='text' name="email"/>\n</p><p>
<anchor>[注册]<go href="wap_save_reg.cgi" method="post">\n
<postfield name="n" value="\$(n)"/>\n
<postfield name="p" value="\$(p)"/>\n
<postfield name="p1" value="\$(p1)"/>\n
<postfield name="email" value="\$(email)"/>\n
</go>\n
</anchor>\n <a href="wap_index.cgi">[客人]</a> <a href="wap.cgi">[登录]</a>\n~;
$show.= qq~
</p>~;
&wapfoot;
