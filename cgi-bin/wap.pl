#########################
# 手机论坛WAP版
# By Maiweb 
# 2005-11-08
# leobbs-vip.com
#########################
$plug="By Maiweb V060803"; #请不要去除!!!
##############基本设置##########################
# 由于手机屏幕的大小特殊性，请尽量保持默认设置
$pre = 10 ; # 版块列表数量
$topicpre=3;# 帖子显示每卡片显示的回复数量
$pre_index=16;#首页论坛列表每页显示的行数
$mastnum =125;#帖子显示处，每个主题或者回复显示的长度
$mastnum2=340;#单独主题每页现实的长度
#############完毕#################################
use UTF8simple;
$uref = new UTF8simple;
$maiweb_sl = "off";
sub waptitle{
print "Content-type: text/vnd.wap.wml;charset=utf-8\n\n";
print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"; 
print "<!DOCTYPE wml PUBLIC \"-//WAPFORUM//DTD WML 1.1//EN\"
\"http://www.wapforum.org/DTD/wml_1.1.xml\">\n";
print "<wml>";
}
sub wapfoot{
my ($no,$min,$hour)= localtime(time+(3600*$time_hour));
if($hour<10){$hour="0".$hour;}
if($min<10){$min="0".$min;}
$show.= "<p><br/>报时:$hour:$min</p></card></wml>\n";
$u=$uref->toUTF8("gb2312",$show);
print $u;
exit;
}
sub errorout{
my $a=shift();
my($a,$b)=split(/\&/,$a);
$show.= qq~<p>$a<br/><br/>$b<br/><a href="wap_login.cgi">「登录」</a>  <a href="wap_reg.cgi">「注册」</a></p></card></wml>~;
$u=$uref->toUTF8("gb2312",$show);
print $u ;exit;
}
sub msg{
	my ($memberfilename,$p) = @_;
	return if($inmembername eq '客人'||$inmembername eq '');
	open (MSGIN, "${lbdir}$msgdir/in/${memberfilename}_msg.cgi");
	sysread(MSGIN, $totalmessages,(stat(MSGIN))[7]);
	close (MSGIN);
	$totalmessages =~ s/\r//isg;
	my @allmessages = split (/\n/, $totalmessages);
	$totalmessages = @allmessages;
	my @newmessages=grep(/^(.+)\tno\t/,@allmessages);
	my $unread = @newmessages;
	$memberfilename=uri_escape($memberfilename);
	my $r= ($unread >0)?"<a href=\"wap_sms.cgi?lid=$lid\">您有$unread条新的短消息</a><br/>":"";
	return $r;
}
sub check{
	#my $af=shift;
$lid =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
	if(-e "${lbdir}wap/$lid" && $lid ne 'a'){
		open(file,"${lbdir}wap/$lid");
		my $bf=<file>;
		close(file);
		($inmembername,$xh2,$pre,$topicpre,$pre_index,$mastnum,$mastnum2,$city1,$where)=split(/\,/,$bf);
		if($xh2 ne $ENV{'REMOTE_ADDR'}){
		$inmembername = '客人';unlink "${lbdir}wap/$lid";$lid='a';
		}
	}else{
		$inmembername = '客人';$lid='a';
	}
}