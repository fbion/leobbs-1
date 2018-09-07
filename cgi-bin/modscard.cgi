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
require "code.cgi";
require "bbs.lib.pl";

$|++;

$thisprog  = "modscard.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");
$prog_dir  = "${lbdir}${msgdir}/modscarddata/";
mkdir($prog_dir,0777) if (!(-e $prog_dir));
$query	= new LBCGI;
$adscript="";
if ($COOKIE_USED eq 2 && $mycookiepath ne "") { $cookiepath = $mycookiepath; } elsif ($COOKIE_USED eq 1) { $cookiepath =""; }
else {
	$boardurltemp	= $boardurl;
	$boardurltemp	=~ s/http\:\/\/(\S+?)\/(.*)/\/$2/;
	$cookiepath	= $boardurltemp;
	$cookiepath	=~ s/\/$//;
#	$cookiepath	=~ tr/A-Z/a-z/;
}
$currenttime = time;
if($lbbody !~/margin/i){
	$lbbody .=' topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0"';
}else{
	if($lbbody !~/topmargin/i){
		$lbbody .=' topmargin="0"';
	}else{
		$lbbody=~s/topmargin="?[0-9]+"?/topmargin="0"/i;
	}
	if($lbbody !~/leftmargin/i){
		$lbbody .=' leftmargin="0"';
	}else{
		$lbbody=~s/leftmargin="?[0-9]+"?/leftmargin="0"/i;
	}
	if($lbbody !~/rightmargin/i){
		$lbbody .=' rightmargin="0"';
	}else{
		$lbbody=~s/rightmargin="?[0-9]+"?/rightmargin="0"/i;
	}
	if($lbbody !~/bottommargin/i){
		$lbbody .=' bottommargin="0"';
	}else{
		$lbbody=~s/bottommargin="?[0-9]+"?/bottommargin="0"/i;
	}
}
if($lbbody !~/scroll/i){
	$lbbody .=' scroll="no"';
}else{
	$lbbody=~s/scroll="?[A-Z]+"?/scroll="no"/i;
}


#IP 禁止
&ipbanned;

#變數：取得所需变数
$action		= &cleaninput($query -> param('action'));		#模式
$checkaction	= $query -> param('checkaction');				#检查动作
$checkaction	= &cleaninput($checkaction);
$start_page	= int($query -> param('start_page'));			#现在页数
$otheraction_a	= $query -> param('otheraction_a');				#其他动作
$otheraction_a	= &cleaninput($otheraction_a);
$otheraction_b	= $query -> param('otheraction_b');				#其他动作
$otheraction_b	= &cleaninput($otheraction_b);
$otheraction_c	= $query -> param('otheraction_c');				#其他动作
$otheraction_c	= &cleaninput($otheraction_c);
$inselectstyle   = $query->cookie("selectstyle");
$inselectstyle   = $skinselected if ($inselectstyle eq "");

&error("普通错误&老大，别乱黑我的程序呀！") if (($inselectstyle =~  m/\//)||($inselectstyle =~ m/\\/)||($inselectstyle =~ m/\.\./));
if (($inselectstyle ne "")&&(-e "${lbdir}data/skin/${inselectstyle}.cgi")) { require "${lbdir}data/skin/${inselectstyle}.cgi"; }
if ($catbackpic ne "")  { $catbackpic = "background=$imagesurl/images/$skin/$catbackpic"; }

#取得会员资料
$inmembername	= $query -> cookie("amembernamecookie");
$inpassword		= $query -> cookie("apasswordcookie");
&page_error("普通错误","老大，别乱黑我的程序呀！") if(($inmembername =~  m/\//)||($inmembername =~ m/\\/)||($inmembername =~ m/\.\./));

if ((!$inmembername) or ($inmembername eq "客人")){
	&page_error("普通错误","您不是论坛的管理团队！");
}else{
	&getmember($inmembername, "no");
	&page_error("普通错误","密码与用户名不相符，请重新登录！") if($inpassword ne $password);
	&page_error("普通错误","用户没有登录或注册！") if($userregistered eq "no");
	&page_error("普通错误","您不是论坛的管理团队！") unless($membercode eq "ad" || $membercode eq "smo" || $membercode eq "cmo" || $membercode eq "mo" || $membercode eq "amo");
	$inmembername = $membername;
	$forum_ad = ($membercode eq "ad")?1:0;
}
$addtime = $mytimeadd * 3600 + $timezone * 3600;

my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
$filetoopens = &lockfilename($filetoopens);
&whosonline("$inmembername\t版主签到\tboth\t论坛版主签到\t") unless(-e "$filetoopens.lck");

$today_date = &longdate($currenttime+$addtime);
$output = "";
if($action eq "set_ad_announce" || $action eq "pcard_status" || $action eq "pcard_search" || $action eq "pcard_search_a"){
	&$action;
}else{
	&top_page;
}

#输出：页面资料

print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");

&output("$boardname - 论坛版主签到",\$output,'msg');

sub top_page{
	my ($ad_announce,$ad_ann_date);
	if("${prog_dir}ad_announcement.cgi"){
		open(FILE,"${prog_dir}ad_announcement.cgi");
		$ad_ann_date = &fulldatetime((stat(FILE))[9]);
		$/="";
		$ad_announce = <FILE>;
		$/="\n";
		close(FILE);
		&lbcode(\$ad_announce);
		&doemoticons(\$ad_announce);
		&smilecode(\$ad_announce);
		chomp $ad_announce;
	}
	$ad_announce = "<br><br><br><center><i>暂时没有任何公告</i></center>" if($ad_announce eq "");
	$ad_ann_date = "" if ($ad_ann_date eq "1970年01月01日 08:00am");
	my $today_log = "${prog_dir}$today_date.cgi";
	$pcard_or_not = 0;
	my (@get_today_log,$get_today_log_list);
	if(-e $today_log){
		open(FILE,$today_log);
		$/="";
		$get_today_log = <FILE>;
		$/="\n";
		close(FILE);
		$get_today_log =~s/[\n\r]/\_/g;
		$get_today_log =~s/^\_+//;
		$get_today_log =~s/\_+$//;
		$get_today_log = "\_$get_today_log\_";
		$pcard_or_not = 1 if($get_today_log=~/\_$inmembername\_/i);
		$get_today_log_list = $get_today_log;
		$get_today_log_list =~s/^\_+//;
		$get_today_log_list =~s/(.+?)\_/<option>$1<\/option>/gi;
	}
	if(!$pcard_or_not && $checkaction eq "pcard"){
		open(FILE,">>$today_log");
		print FILE "$inmembername\n";
		close(FILE);
		$pcard_or_not = 1;
		$get_today_log_list.=qq~<option>$inmembername</option>~;
	}
	
	$td_height = ($forum_ad)?163:238;
	$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$titlecolor" align="center" colspan="2" $catbackpic><font color="$fontcolormisc"><b>坛主公告</b></font></td></tr>
<tr><td bgcolor="$miscbackone" valign="top" colspan="2" align="right">
<span style="height:$td_height;overflow:auto;padding:2px;color:$fontcolormisc;width:100%;text-align:left">
$ad_announce
</span><i>$ad_ann_date</i>
</td></tr>
<tr><td bgcolor="$miscbacktwo" align="center" colspan="2"><font color="$fontcolormisc"><b>打卡签到</b></font></td></tr>~;
	if($pcard_or_not){
		$output .= qq~
<tr>
<td bgcolor="$miscbackone"><font color="$fontcolormisc">日期：<i>$today_date<i></font></td>
<td bgcolor="$miscbackone" align="center"><b><font color="$fonthighlight">已经签到</font></b></td>
</tr>~;
	}else{
		$output .= qq~
<form action="$thisprog" method="GET">
<input type="hidden" name="checkaction" value="pcard">
<tr>
<td bgcolor="$miscbackone"><font color="$fontcolormisc">日期：<i>$today_date<i></font></td>
<td bgcolor="$miscbackone" align="center"><input type="submit" value="签到"></td>
</tr>
</form>~;
	}
	if($forum_ad){
		$output .= qq~
<tr>
<td bgcolor="$miscbacktwo"><select style="width:100%;background-color:$miscbacktwo"><option style="color:$fonthighlight;">今天已签到管理员</option>$get_today_log_list</select></td>
<td bgcolor="$miscbacktwo" align="center"><font color="$fontcolormisc"><b>坛主管理</b></font></td>
</tr>
<form action="$thisprog" method="GET">
<input type="hidden" name="checkaction" value="pcard">
<tr>
<td bgcolor="$miscbackone" align="center" colspan="2">[<b><a href="$thisprog?action=set_ad_announce" target="_self">更改坛主公告</a></b>] [<b><a href="$thisprog?action=pcard_status" target="_self">查看签到记录</a></b>]</td>
</tr>
</form>~;
	}
	$output .= qq~
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}

sub set_ad_announce{
	&page_error("签到记录","只允许坛主更改公告！") unless($forum_ad);
	my $ad_announcement = "${prog_dir}ad_announcement.cgi";
	if($start_page != 0){
		open(FILE,">$ad_announcement");
		print FILE $checkaction;
		close(FILE);
		unlink($ad_announcement) if($checkaction eq "");
		$output = qq~<script>location.href="$thisprog";</script>~;
	}
	my ($ad_announce,$ad_ann_date);
	if(-e $ad_announcement){
		open(FILE,$ad_announcement);
		$ad_announce = <FILE>;
		close(FILE);
		$ad_announce =~s/<p>/\n\n/g;
		$ad_announce =~s/<br>/\n/g;
	}
	$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$titlecolor" align="center" colspan="2" $catbackpic><font color="$fontcolormisc"><b>坛主公告</b></font></td></tr>
<form action="$thisprog" method="POST">
<input type="hidden" name="start_page" value="1">
<input type="hidden" name="action" value="set_ad_announce">
<tr><td bgcolor="$miscbackone" valign="top" align="center" colspan="2">
<textarea cols="60" rows="16" name="checkaction">$ad_announce</textarea><br>
※可以使用 LBCODE　※不能使用 HTML
</td></tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50">
<< <a href="$thisprog">返回</a>
</td>
<td bgcolor="$miscbackone" align="center" width="350"><input type="submit" value="更改公告" style="width:120px"></td>
</tr>
</form>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}

sub pcard_status{
	&page_error("签到记录","只允许坛主查看签到记录！") unless($forum_ad);
	$checkaction = ($checkaction =~/^[0-9]{4,4}年[0-9]{2,2}月[0-9]{2,2}日$/)?$checkaction:$today_date;
	my $that_day_log = "${prog_dir}$checkaction.cgi";
	if($start_page == -1) {
		$start_page = 0;
		unlink($that_day_log);
	}
	$no_log_that_day = (-e $that_day_log)?0:1;
	my $log_date_list = "";
	opendir(DIR,$prog_dir);
	foreach(readdir(DIR)){
		my $file_full_path = "${prog_dir}$_";
		unlink($file_full_path) if($_ =~/\_search.cgi/i && (stat($file_full_path))[9] < (time - 30*60));
		next if($_ eq "." || $_ eq ".." || $_ eq "index.html" || $_ eq "ad_announcement.cgi" || $_ eq "" || $_ =~/\_search.cgi/i);
		$_ =~s/\.cgi$//i;
		$log_date_list .=qq~<option value="$_">$_</option>~;
		if($no_log_that_day){
			$that_day_log = "${prog_dir}$_.cgi";
			$checkaction = $_;
		}
	}
	closedir(DIR);
	$checkaction_link = uri_escape($checkaction);
	$log_date_list =~s/value="$checkaction"/value="$checkaction" selected/;
	
	&page_error("签到记录","没有任何签到记录！") unless(-e $that_day_log);
	
	if($otheraction_a eq "search"){
		$that_day_log = "${prog_dir}$inmembername\_search.cgi";
		$checkaction = "搜寻签到记录";
		$checkaction_link = "";
	}
	open(FILE,$that_day_log);
	my @memberdata = <FILE>;
	close(FILE);
	chomp @memberdata;
	my %memberdata = ();
	if($otheraction_a eq "search"){
		my @memberdata_b =@memberdata;
		foreach(@memberdata_b){
			my ($membername,$pcard_result) = split(/\t/,$_);
			next if($membername eq "");
			$memberdata{$membername}.="<u>$pcard_result</u><br>";
		}
		@memberdata = keys %memberdata;
	}
	@memberdata = sort alphabetically @memberdata;
	$total_member = @memberdata;
	&page_error("签到记录","没有任何签到记录！") unless($total_member);
	%membernameimg = ();
	$membernameimg{'ad'} = "<img src=$imagesurl/images/teamad.gif alt=此人为坛主 width=16 align='absmiddle'>";
	$membernameimg{'mo'} = "<img src=$imagesurl/images/teammo.gif alt=此人为版主 width=16 align='absmiddle'>";
	$membernameimg{'amo'} = "<img src=$imagesurl/images/teamamo.gif alt=此人为副版主 width=16 align='absmiddle'>";
	$membernameimg{'smo'} = "<img src=$imagesurl/images/teamsmo.gif alt=此人为总版主 width=16 align='absmiddle'>";
	$membernameimg{'cmo'} = "<img src=$imagesurl/images/teamcmo.gif alt=此人为区版主 width=16 align='absmiddle'>";
	
	$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr>
<td bgcolor="$titlecolor" align="center" $catbackpic><a href="$thisprog?action=pcard_search"><font color="$fontcolormisc">[搜寻]</font></a></td>
<td bgcolor="$titlecolor" align="center" $catbackpic><font color="$fontcolormisc"><b>签到记录 - $checkaction</b></font></td>
</tr>
<tr><td bgcolor="$miscbackone" valign="top" align="right" colspan="2">
<span style="height:230;overflow:auto;padding:2px;color:$fontcolormisc;width:100%;text-align:left">~;
	my $last_membername = 0;
	for($i=$start_page;($i<$start_page+5)&&($i<$total_member);$i++){
		my ($membername,$pcard_result) = split(/\t/,$memberdata[$i]);
		$pcard_result = '<font color="'.$fonthighlight.'">此版主有在本日签到</font>' if($pcard_result eq "" || $otheraction_a ne "search");
		my $memberlinkname = uri_escape($membername);
		my $memberfilename = $membername;
		$memberfilename =~s/ /_/g;
		$memberfilename =~ tr/A-Z/a-z/;
		my $namenumber = &getnamenumber($memberfilename);
		&checkmemfile($memberfilename,$namenumber);
    		my $filetoopen = "${lbdir}$memdir/$namenumber/$memberfilename.cgi";
		open (FILE, "$filetoopen");
		$memberline = <FILE>;
		close (FILE);
		@userdetail = split (/\t/, $memberline);
		chomp @userdetail;
		undef $useravatar;
		if ($avatars eq "on") {
			if (($userdetail[22])&&($userdetail[23])&&($userdetail[24])) { #自定义头像存在
				$userdetail[22] =~ s/\$imagesurl/${imagesurl}/o;
				if (($userdetail[22] =~ /\.swf$/i)&&($flashavatar eq "yes")) {
					$userdetail[22]=&uri_escape($userdetail[22]);
					$useravatar = qq(<OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" WIDTH=$userdetail[23] HEIGHT=$userdetail[24]><PARAM NAME=MOVIE VALUE=$userdetail[22]><PARAM NAME=PLAY VALUE=TRUE><PARAM NAME=LOOP VALUE=TRUE><PARAM NAME=QUALITY VALUE=HIGH><EMBED SRC=$userdetail[22] WIDTH=$userdetail[23] HEIGHT=$userdetail[24] PLAY=TRUE LOOP=TRUE QUALITY=HIGH></EMBED></OBJECT></td>);
				}else{
					$userdetail[22]=&uri_escape($userdetail[22]);
					$useravatar = qq(<img src=$userdetail[22] border=0 width=$userdetail[23] height=$userdetail[24]>);
				}
			}elsif (($userdetail[18] ne "noavatar") && ($userdetail[18])) {
				$userdetail[18]=&uri_escape($userdetail[18]);
				$useravatar = qq(<img src="$imagesurl/avatars/$userdetail[18].gif" border="0">);
            }
            $useravatar = qq~<td rowspan="4" width="$maxposticonwidth" align="center">$useravatar</td>~ if(defined $useravatar);
        }
		$userdetail[13] = $userdetail[13] + ($userdetail[16] * 3600) + ($timezone * 3600);
		if ($userdetail[13]) { $userdetail[13] = &longdate ($userdetail[13]) } else { $userdetail[13] = "Unknown"; }
		$lastgone   = $userdetail[26];
		$lastgone   = $joineddate if($lastgone eq "");
		$today      = time-$lastgone;
		$novisitdate = int($today/(3600*24));
		$lastgone   = &dateformat($lastgone + ($timedifferencevalue*3600) + ($timezone*3600));
		if($novisitdate < 2){
			$visitresult=qq(此版主比较勤快);
		}elsif($novisitdate < 7){
			$visitresult=qq(此版主 ７ 天之内有访问);
		}elsif($novisitdate < 15){
			$visitresult=qq(此版主 １５ 天之内有访问);
		}else{
			$visitresult=qq(此版主已有很久未访问论坛);
		}
		my $emailgraphic	= qq~<img src=$imagesurl/images/email.gif border=0 width=16 align=absmiddle style=filter:gray><font style=color:#444444 disabled>邮件</font>~;
		my $homepagegraphic= qq~<img src=$imagesurl/images/homepage.gif border=0 width=16 align=absmiddle style=filter:gray><font style=color:#444444 disabled>主页</font>~;
		my $oicqgraphic	= qq~<img src=$imagesurl/images/oicq.gif border=0 width=16 align=absmiddle style=filter:gray><font style=color:#444444 disabled>QQ</font>~;
		my $icqgraphic		= qq~<img src=$imagesurl/images/icq.gif border=0 width=16 align=absmiddle style=filter:gray><font style=color:#444444 disabled>ICQ</font>~;
	        $userdetail[5] = &encodeemail($userdetail[5]);
	        $userdetail[6] = "no" if ($dispmememail eq "no");
		if ($userdetail[6] eq "yes") { 
			$emailgraphic = qq~<a href=mailto:$userdetail[5] title=电子邮件地址><img src=$imagesurl/images/email.gif border=0 width=16 align=absmiddle>邮件</a>~;
		} elsif ($userdetail[6] eq "msn") {
			$emailgraphic = qq~<a href=mailto:$userdetail[5] title="MSN 地址"><img src=$imagesurl/images/msn.gif border=0 width=16 align=absmiddle>MSN</a>~;
		} elsif ($userdetail[6] eq "popo"){
                       $emailgraphic = qq~<a href=mailto:$userdetail[5] title="泡泡地址"><img src=$imagesurl/images/popo.gif border=0 width=16 align=absmiddle>泡泡</a>~;
		}
		if ($userdetail[8]=~/^([a-z]+?:\/\/){1}([a-z0-9\-\.,\?!%\*_\#:;~\\&$@\/=\+\(\)]+)/i) {
			$homepagegraphic = qq~<a href="$userdetail[8]" target=_blank title="访问 $membername 的主页"><img src=$imagesurl/images/homepage.gif border=0 width=16 align=absmiddle>主页</a>~;
		}
		if (($userdetail[9]) && ($userdetail[9] =~ /^[0-9]+$/)) {
			$oicqgraphic = qq~<a href=http://search.tencent.com/cgi-bin/friend/user_show_info?ln=$userdetail[9] target=_blank title="查看 QQ:$userdetail[9] 的资料"><img src=$imagesurl/images/oicq.gif border=0 width=16 align=absmiddle>QQ</a>~;
		}
		if (($userdetail[10]) && ($userdetail[10] =~ /^[0-9]+$/)) {
			$icqgraphic = qq~<span style="cursor:hand" onClick="javascript:openScript('misc.cgi?action=icq&UIN=$userdetail[10]',450,300)" title="给 ICQ:$userdetail[10] 发个消息"><img src=$imagesurl/images/icq.gif border=0 width=16 align=absmiddle>ICQ</span>~;
		}
		if($otheraction_a ne "search"){
		$output .= qq~
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="$maxposticonheight" style="border:1 solid $tablebordercolor">
<tr>$useravatar<td>$membernameimg{$userdetail[3]} <b><a href="profile.cgi?action=show&member=$memberlinkname" title="查看$membername的个人资料" target=_blank><u>$membername</u></a></b></td></tr>
<tr>
<td>
<font color="$fontcolormisc">最后来访：<i>$lastgone</i><br>
失踪天数：共 <b>$novisitdate</b> 天<br>
评定结果：<b><font color="$fonthighlight">$visitresult</font></b></font></td>
</tr>
<tr>
<td><font color="$fontcolormisc">$homepagegraphic $emailgraphic $oicqgraphic $icqgraphic</font></td>
</tr>
<tr>
<td><u>$pcard_result</u></td>
</tr>
</table><br>~;
		}else{
				$output .= qq~
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="$maxposticonheight" style="border:1 solid $tablebordercolor">
<tr>$useravatar<td>$membernameimg{$userdetail[3]} <b><a href="profile.cgi?action=show&member=$memberlinkname" title="查看$membername的个人资料"><u>$membername</u></a></b></td></tr>
<tr>
<td><span style="height:100;overflow:auto;padding:2px;color:$fontcolormisc;width:100%;">$memberdata{$membername}</span></td>
</tr>
</table><br>~;
		}
	}
	$page_link = &page_link_gen($total_member,8,$start_page,5,"start_page","action=pcard_status&checkaction=$checkaction_link&otheraction_a=$otheraction_a",$thisprog,$fontcolormisc,$fonthighlight);
	$output .= qq~
</span>$page_link
</td></tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50">
<< <a href="$thisprog">返回</a>
</td>
<form action="$thisprog" method="GET">
<input type="hidden" name="action" value="pcard_status">
<td bgcolor="$miscbackone" align="center" width="350">
<select name="checkaction" style="width:120px">$log_date_list</select> <input type="submit" value="查看签到记录"> 
[<a href="$thisprog?action=pcard_status&checkaction=$checkaction_link&start_page=-1" target="_self">删除记录</a>]
</td>
</form>
</tr>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}

sub pcard_search{
	my $log_date_list = "";
	my $log_date_list_b = "";
	opendir(DIR,$prog_dir);
	foreach(readdir(DIR)){
		next if($_ eq "." || $_ eq ".." || $_ eq "index.html" || $_ eq "ad_announcement.cgi" || $_ eq "" || $_ =~/\_search.cgi/i);
		$_ =~s/\.cgi$//i;
		$log_date_list .=qq~<option value="$_">$_的记录</option>~;
		$log_date_list_b .=qq~<option value="$_">$_</option>~;
	}
	closedir(DIR);
	$output .= qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$titlecolor" align="center" colspan="2" $catbackpic><font color="$fontcolormisc"><b>类型搜寻</b></font></td></tr>
<form action="$thisprog" method="POST">
<input type="hidden" name="start_page" value="1">
<input type="hidden" name="action" value="pcard_search_a">
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>记录</b></td>
<td bgcolor="$miscbackone" align="left" width="350"><select name="checkaction" style="width:150px"><option value="所有">搜寻所有记录</option>$log_date_list</select></td>
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>类型</b></td>
<td bgcolor="$miscbackone" align="left" width="350"><input type="checkbox" name="otheraction_a" value="ad"> 坛主 <input type="checkbox" name="otheraction_a" value="smo"> 总版主 <input type="checkbox" name="otheraction_a" value="cmo"> 区版主 <input type="checkbox" name="otheraction_a" value="mo"> 版主 <input type="checkbox" name="otheraction_a" value="amo"> 副版主 </td>
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>方式</b></td>
<td bgcolor="$miscbackone" align="left" width="350">
<input type="radio" name="otheraction_b" value="1" checked> 在所选记录中搜寻有签到的所选类型<br>
<input type="radio" name="otheraction_b" value="2"> 在所选记录中搜寻没有签到的所选类型<br>
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" colspan="2"><input type="submit" value="开始搜寻" style="width:120px"></td>
</tr>
</form>
<tr><td bgcolor="$titlecolor" align="center" colspan="2" $catbackpic><font color="$fontcolormisc"><b>会员搜寻</b></font></td></tr>
<form action="$thisprog" method="POST">
<input type="hidden" name="start_page" value="2">
<input type="hidden" name="action" value="pcard_search_a">
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>会员</b></td>
<td bgcolor="$miscbackone" align="left" width="350"><input type="text" name="otheraction_a" value="" size="30"> 以半形逗号(,)分隔
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" width="50"><b>方式</b></td>
<td bgcolor="$miscbackone" align="left" width="350">
<input type="radio" name="otheraction_b" value="1" checked> 在所有记录中搜寻有签到的输入会员<br>
<input type="radio" name="otheraction_b" value="2"> 在所有记录中搜寻没有签到的输入会员<br>
</tr>
<tr>
<td bgcolor="$miscbackone" align="center" colspan="2"><input type="submit" value="开始搜寻" style="width:120px"></td>
</tr>
</form>
<tr>
<td bgcolor="$miscbackone" align="center" width="50">
<< <a href="$thisprog">返回</a>
</td>
<form action="$thisprog" method="GET">
<input type="hidden" name="action" value="pcard_status">
<td bgcolor="$miscbackone" align="center" width="350">
<select name="checkaction" style="width:120px">$log_date_list_b</select> <input type="submit" value="查看签到记录"> 
</td>
</form>
</tr>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}
sub pcard_search_a{
	if($start_page == 1){
		#要 SEARCH 的類型
		my @otheraction_a = $query -> param('otheraction_a');
		my $otheraction_a = join("\_",@otheraction_a);
		$otheraction_a = &cleaninput($otheraction_a);
		$otheraction_a .="\_";
		my @memberdata;
		#選出那(些)類型
		my %membernamecode = ('ad' => 1,'smo' => 2,'cmo' => 3,'mo' => 4,'amo' => 5);
		open (FILE, "$lbdir/data/lbmember.cgi");
		while(<FILE>){
			my @tmpuserdetail = split (/\t/, $_);
			chomp @tmpuserdetail;
			next unless(defined $membernamecode{$tmpuserdetail[1]});
			push(@memberdata,$tmpuserdetail[0]) if($otheraction_a=~/$tmpuserdetail[1]\_/i);
		}
		chomp @memberdata;
		close (FILE);
		#要 SEARCH 的記錄
		my (@log_selected);
		if($checkaction eq "所有"){
			opendir(DIR,$prog_dir);
			foreach(readdir(DIR)){
				next if($_ eq "." || $_ eq ".." || $_ eq "index.html" || $_ eq "ad_announcement.cgi" || $_ eq "" || $_ =~/\_search.cgi/i);
				push(@log_selected,$_);
			}
			closedir(DIR);
		}else{
			my $that_day_log = "${prog_dir}$checkaction.cgi";
			push(@log_selected,"$checkaction\.cgi") if(-e $that_day_log);
		}
		#開始 SEARCH
		my $i=0;
		my (@have_pcard,@have_not_pcard);
		my $search_file = "${prog_dir}$inmembername\_search.cgi";
		unlink $search_file;
		foreach $log_file(@log_selected){
			my $log_file_date = substr($log_file,0,-4);
			my $that_day_log = "${prog_dir}$log_file";
			next unless(-e $that_day_log);
			open(FILE,$that_day_log);
			$/="";
			my $get_that_day_log = <FILE>;
			$/="\n";
			close(FILE);
			$get_that_day_log =~s/[\n\r]/\_/g;
			$get_that_day_log =~s/^\_+//;
			$get_that_day_log =~s/\_+$//;
			
			$get_that_day_log = "\_$get_that_day_log\_";
			open(SFILE,">>$search_file");
			foreach $membername(@memberdata){
				if($get_that_day_log=~/\_$membername\_/i){
					print SFILE "$membername\t<font color=\"$fonthighlight\">此版主有在$log_file_date签到</font>\n" if($otheraction_b == 1);
				}else{
					print SFILE "$membername\t<font color=\"$fontcolormisc\">此版主没有在$log_file_date签到</font>\n" if($otheraction_b == 2);
				}
			}
			close(SFILE);
			$i++;
		}
		&page_error("签到记录","没有任何签到记录！") unless($i);
	}else{
		#要 SEARCH 的会员
		my @otheraction_a = split(/\,/,$otheraction_a);
		my @memberdata;
		my %membernamecode = ('ad' => 1,'smo' => 2,'cmo' => 3,'mo' => 4,'amo' => 5);
		foreach $membername(@otheraction_a){
			my $memberfilename = $membername;
			$memberfilename =~s/ /_/g;
			$memberfilename =~ tr/A-Z/a-z/;
			my $namenumber = &getnamenumber($memberfilename);
			&checkmemfile($memberfilename,$namenumber);
	    		my $filetoopen = "${lbdir}$memdir/$namenumber/$memberfilename.cgi";
			open (FILE, "$filetoopen");
			$memberline = <FILE>;
			close (FILE);
			@userdetail = split (/\t/, $memberline);
			chomp @userdetail;
			push(@memberdata,$userdetail[0]) if(defined $membernamecode{$userdetail[3]});
		}
		#要 SEARCH 的記錄
		my @log_selected;
		opendir(DIR,$prog_dir);
		foreach(readdir(DIR)){
			next if($_ eq "." || $_ eq ".." || $_ eq "index.html" || $_ eq "ad_announcement.cgi" || $_ eq "" || $_ =~/\_search.cgi/i);
			push(@log_selected,$_);
		}
		closedir(DIR);
		#開始 SEARCH
		my $i=0;
		my (@have_pcard,@have_not_pcard);
		my $search_file = "${prog_dir}$inmembername\_search.cgi";
		unlink $search_file;
		foreach $log_file(@log_selected){
			my $log_file_date = substr($log_file,0,-4);
			my $that_day_log = "${prog_dir}$log_file";
			next unless(-e $that_day_log);
			open(FILE,$that_day_log);
			$/="";
			my $get_that_day_log = <FILE>;
			$/="\n";
			close(FILE);
			$get_that_day_log =~s/[\n\r]/\_/g;
			$get_that_day_log =~s/^\_+//;
			$get_that_day_log =~s/\_+$//;
			
			$get_that_day_log = "\_$get_that_day_log\_";
			open(SFILE,">>$search_file");
			foreach $membername(@memberdata){
				if($get_that_day_log=~/\_$membername\_/i){
					print SFILE "$membername\t<font color=\"$fonthighlight\">此版主有在$log_file_date签到</font>\n" if($otheraction_b == 1);
				}else{
					print SFILE "$membername\t<font color=\"$fontcolormisc\">此版主没有在$log_file_date签到</font>\n" if($otheraction_b == 2);
				}
			}
			close(SFILE);
			$i++;
		}
		&page_error("签到记录","没有任何签到记录！") unless($i);
	}
	$output = qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="5" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$miscbacktwo" align="center" height="20" $catbackpic><font color="$fontcolormisc"><b>搜寻完成</b></font></td></tr>
<tr><td bgcolor="$miscbackone" valign="top">
<font color="$fontcolormisc">
<b>已经完成搜寻：</b>
<ul>
<li><b>已经建立需要的搜寻记录</b>
<li><a href="$thisprog?action=pcard_status&checkaction=$checkaction_link&otheraction_a=search">如果您的浏览器没有自动跳页，请按这里</a>
</ul>
<meta http-equiv="refresh" content="2; url=$thisprog?action=pcard_status&checkaction=$checkaction_link&otheraction_a=search">
</font>
</td></tr>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
}

sub page_error{
	my ($where,$errormsg) = @_;

	$output = qq~<SCRIPT>valigntop()</SCRIPT>
<table cellPadding="0" cellSpacing="0" border="0" width=$tablewidth bgColor="$tablebordercolor" align="center" height="320">
<tr><td>
<table cellPadding="2" cellSpacing="1" border="0" width="100%" height="100%">
<tr><td bgcolor="$miscbacktwo" align="center" $catbackpic><font color="$fontcolormisc"><b>错误： $where</b></font></td></tr>
<tr><td bgcolor="$miscbackone" valign="top">
<font color="$fontcolormisc">
<b>关于$where的详细原因：</b>
<ul>
<li><b>$errormsg</b>
<li>您是否需要查看<span style="cursor:hand" onClick="javascript:openScript('help.cgi',500,400)">帮助文件</span>?
</ul>
<b>产生$where错误的可能原因：</b>
<ul>
<li>密码错误
<li>用户名错误
<li>您不是<a href="register.cgi" target="_blank">注册</a>用户
</ul>
<br><br><center><font color=$fontcolormisc> << <a href="javascript:history.go(-1)">返回上一页</a></center>
</font>
</td></tr>
</table>
</td></tr>
</table><SCRIPT>valignend()</SCRIPT>~;
	print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
	&output("$boardname - 论坛版主签到",\$output,'msg');
	exit;
}

sub page_link_gen{
	#引数：项目总数，显示数量，现时位置，ＯＦＦＳＥＴ，变数名，传递变数，程序名称，通常颜色，加重颜色，连结目标，文字样式
	my ($total_count,$disp_count,$now_count,$each_count,$var_this,$var_add,$this_prog,$color_a,$color_b,$link_target,$link_temp) = @_;
	#初始化：所有需要值
	my ($link_s,$link_e,$this_count,$this_dec,$i,$count,$uplink_page,$downlink_page,$link_of_page,$now_page);
	$total_count= int($total_count);				#变数处理：项目总数（數值化）
	$disp_count	= int($disp_count);					#变数处理：显示数量（數值化）
	$now_count	= int($now_count);					#变数处理：现时位置（數值化）
	$var_this	=~s/[^A-Za-z0-9\_]//g;				#变数处理：变数名　（删除英数字以外字串）
	$color_a	= "#333333" if($color_a eq "");		#变数处理：通常颜色（默认：#333333）
	$color_b	= "#990000" if($color_b eq "");		#变数处理：加重颜色（默认：#990000）
	$link_target= "_self" if($link_target eq "");	#变数处理：连结目标（默认为目前框）
	#检查必需值，如无（任何）返回：显示数量，ＯＦＦＳＥＴ，变数名
	goto RETURN if($disp_count < 0 || $each_count < 0 || $var_this eq "");
	#設定文字样式：文字样式的预设值
	$link_temp		= qq~<font color="$color_a"><b>共 <font color="$color_b">%d</font> 页</b> %s [ %s ] %s</font>~ unless(defined $link_temp && $link_temp=~/\%d.*\%s.*%s.*%s/);
	#取得目前程序名称：程序名称的预设值
	$this_prog		= substr($ENV{'SCRIPT_NAME'},rindex($ENV{'SCRIPT_NAME'},"/")+1) unless(defined $this_prog && $this_prog ne "");
	#现所在页
	$now_page= ($now_count/$each_count)+1;
	#总页数
	($this_count,$this_dec) = split(/\./,($total_count/$each_count));	#计算总页数：项目总数除ＯＦＦＳＥＴ
	$this_count++ if($this_dec > 0);									#进位：无条件
	$this_count=1 if(!$this_count);										#正数化：最少１
	#回圈条件：
	$link_s = $now_page-int($disp_count/2);#开始
	$link_e = $now_page+int($disp_count/2);#结束
	#回圈条件处理：开始条件少於总页数
	if($link_s < 0){
		$link_e += (0 - $link_s);
		$link_s = 0;
	}
	#回圈条件处理：结束条件大於０
	if($link_e > $this_count){
		$link_s -= ($link_e - $this_count);
		$link_e = $this_count;
	}
	#处理：跳页显示
	my @PARRAY = ($link_s..$link_e);
	$link_of_page = join("  ",@PARRAY);
	$link_of_page =~s/^\s+//;
	$link_of_page =~s/\s+$//;
	$link_of_page = " $link_of_page ";
	$link_of_page =~s/ (-?[0-9]+) /
		my $i=$1;
		my $return_t="";
		my $link_c= $i*$each_count;							#页ＯＦＦＳＥＴ
		my $page_c= $i+1;									#处理页数
		if($link_c != $now_count){
			#不等於现ＯＦＦＳＥＴ：显示数字连结
			$return_t=qq~<a href="$this_prog?$var_this=$link_c&$var_add" title="第 $page_c 页" style="color:$color_a" target="$link_target"><b>$page_c<\/b><\/a> ~;
		}else{
			#相等於现ＯＦＦＳＥＴ：显示纯数字
			$return_t=qq~<font color="$color_b"><b>$page_c<\/b><\/font> ~;
		}
		$count++;#递增：现显示数
		$return_t="" if($count > $disp_count || $i >= $this_count || $i < 0);
		$return_t;
		/ge;
	#除去最尾的空格
	chop $link_of_page;
	#处理：向上跳页
	$uplink_page		= qq~<font color="$color_b" face="webdings">9</font> <font color="$color_b" face="webdings">7</font>~;
	if($now_count > 0){
		#不於首页，加上向上跳页的连结
		my $perv_page = $now_page-1;
		my $perv_page_count = ($perv_page-1)*$each_count;
		$uplink_page=qq~<a href="$this_prog?$var_this=0&$var_add" title="首 页" target="$link_target"><font face="webdings" color="$color_a">9</font></a> <a href="$this_prog?$var_this=$perv_page_count&$var_add" title="第 $perv_page 页" target="$link_target"><font face="webdings" color="$color_a">7</font></a>~;
	}
	#处理：向下跳页
	$downlink_page	= qq~<font color="$color_b" face="webdings">8</font> <font color="$color_b" face="webdings">:</font>~;
	if($now_count < ($this_count-1)*$each_count){
		#不於尾页，加上向下跳页的连结
		my $last_page_count = ($this_count-1)*$each_count;
		my $next_page = $now_page+1;
		my $next_page_count = ($next_page-1)*$each_count;
		$downlink_page=qq~<a href="$this_prog?$var_this=$next_page_count&$var_add" title="第 $next_page 页" target="$link_target"><font face="webdings" color="$color_a">8</font></a> <a href="$this_prog?$var_this=$last_page_count&$var_add" title="尾 页" target="$link_target"><font face="webdings" color="$color_a">:</font></a>~;
	}
	$link_of_page = sprintf($link_temp,$this_count,$uplink_page,$link_of_page,$downlink_page);
	#返回：连结页资料
	RETURN:
	return $link_of_page;
}
