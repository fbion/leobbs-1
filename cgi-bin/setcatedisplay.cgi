#!/usr/bin/perl
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

#################--- Begin the program ---###################
$thisprog = "setcatedisplay.cgi";
eval ('$complevel = 9 if ($complevel eq ""); use WebGzip($complevel); $gzipused = 1;') if ($usegzip eq "yes");
$query = new LBCGI;
&ipbanned; #封杀一些 ip

$action	   = $query -> param('action');
$action        = &cleaninput("$action");
#Global
$selectid	  = $query -> param("select");
@selectid	  = $query -> param("select") if(defined $selectid && $selectid);
$pselectid	  = $query -> param("pselect");
@pselectid	  = $query -> param("pselect") if(defined $pselectid && $pselectid);


$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

my %Mode = ('modify' => \&modify);
#################--- Main program ---###################
&getadmincheck;
print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
&getmember("$inmembername","no");
if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
	print qq~
	<tr><td bgcolor="#2159C9" colspan=4><font color=#FFFFFF>
	<b>欢迎来到论坛管理中心 / 分类显示方式</b>
	</td></tr>~;
	if($Mode{$action}) { 
		$Mode{$action}->();
		print qq~<tr><td bgcolor="#FFFFFF" align="center" valign="middle" colspan="2" height="50">--<a href="$thisprog?">返回</a>--</td></tr>~;
	} else {
		&toppage;
	}
	print qq~<tr><td bgcolor=#FFFFFF align=right valign="bottom" colspan=4 height="80"><a href="http://www.LeoHacks.com" target="_blank" title="官方LeoBoard Hacks开发站点"><font color=#bbbbbb>CATEDT for LeoBBS X Beta 1.0</font></a><br><font color=#bbbbbb>Copyright &copy; 2002 RoyRoy All rights reserved</font></td></tr></table></td></tr></table>~;
} else {
	&adminlogin;
}
sub toppage{
	my $filetoopen = "$lbdir" . "data/allforums.cgi";
	$filetoopen = &stripMETA($filetoopen);
	open(FILE, "$filetoopen");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	my @forums = <FILE>;
	close(FILE);
	$forumlist="";
	require "${lbdir}data/category_display.cgi" if(-e "${lbdir}data/category_display.cgi");
	%CATEDISPLAY_SET = ();
	%PARENTDISPLAY_SET = ();
	%THIS_IS_PARENT = ();
	$forumlist = join("\n",@forums);
	$forumlist =~s/\n+$//;
	$forumlist .= "\n";
	$pforumlist = $forumlist;
	$forumlist =~s/(.+?)\t(.+?)\t(.+?)\t(.+?)\t.+?\n/
		my ($categoryid,$categoryname) = ($3,$2);
		my $temp;
		if(!defined $CATEDISPLAY_SET{$categoryid}){
			$CATEDISPLAY_SET{$categoryid} = 'DIS';
			my %temp_a;
			if($category_display_type{$categoryid} eq "basic"){
				$temp_a{'basic'} = " checked";
			}else{
				$temp_a{'adv'} = " checked";
			}
			$temp = qq(<input type="hidden" name="select" value="$categoryid"><tr bgcolor="#FFFFFF" onmouseover="this.bgColor='#F7F7F7';" onmouseout="this.bgColor='#FFFFFF';">
		<td style="border:1 solid #DDDDDD;border-top:0px;">[$categoryid]$categoryname<\/td>
		<td style="border:1 solid #DDDDDD;border-top:0px;border-left:0px;">
		<input type="radio" name="display_type[$categoryid]" value="basic"$temp_a{'basic'}> 简易方式
		<input type="radio" name="display_type[$categoryid]" value="adv"$temp_a{'adv'}> 详细方式
		<\/td><\/tr>\n);
		}
		$temp;
	/ge;
	$pforumlist =~s/(.+?)\t(.+?)\t(.+?)\t(.+?)\t.+?\n/
		my ($pforumid,$pforumname,$parentname) = ($1,$4,$2);
		my $temp;
		if(substr($parentname,0,11) eq 'childforum-'){
			$THIS_IS_PARENT{substr($parentname,11)} = $pforumid;
		}elsif(!defined $PARENTDISPLAY_SET{$pforumid}){
			$PARENTDISPLAY_SET{$pforumid} = 'DIS';
			$temp = $pforumid."\t".$pforumname."\t\n";
		}
		$temp;
	/ge;
	$pforumlist =~s/(.+?)\t(.+?)\t\n/
		my ($pforumid,$pforumname) = ($1,$2);
		my $temp;
		if(defined $THIS_IS_PARENT{$pforumid}){
			my %temp_a;
			if($pforum_display_type{$pforumid} eq "basic"){
				$temp_a{'basic'} = " checked";
			}else{
				$temp_a{'adv'} = " checked";
			}
			$temp = qq(<input type="hidden" name="pselect" value="$pforumid"><tr bgcolor="#FFFFFF" onmouseover="this.bgColor='#F7F7F7';" onmouseout="this.bgColor='#FFFFFF';">
		<td style="border:1 solid #DDDDDD;border-top:0px;">[$pforumid]$pforumname<\/td>
		<td style="border:1 solid #DDDDDD;border-top:0px;border-left:0px;">
		<input type="radio" name="pdisplay_type[$pforumid]" value="basic"$temp_a{'basic'}> 简易方式
		<input type="radio" name="pdisplay_type[$pforumid]" value="adv"$temp_a{'adv'}> 详细方式
		<\/td><\/tr>\n);
		}
		$temp;
	/ge;
	
	$forumlist =~s/\n+//g;
	$pforumlist =~s/\n+//g;
	print qq~
	<tr>
	<td bgcolor=#EEEEEE align=center colspan=4>
	<font color=#990000><b>使用说明</b>
	</td>
	</tr>
	<tr>
	<td bgcolor=#FFFFFF align=center colspan=4>
	<table width=80% align=center>
	<tr><td><ol type="1">
	<li>本程序可以修改各分类于首页显示时的显示方式。
	<li>也可以修改各子论坛于分论坛页的显示方式。
	</td></tr>
	</table>
	</td>
	</tr>
	<form action="$thisprog" method=post name=form><input type="hidden" name="action" value="modify">
	<tr>
	<td bgcolor=#EEEEEE align=center colspan=4>
	<font color=#990000><b>分类一览表</b>
	</td>
	</tr>
	<tr>
	<td bgcolor=#FFFFFF align=center colspan=4>
	<table width="80%" align="center" cellspacing="0" cellpadding="5" border="0">
	<tr bgcolor="#DDDDDD"><td><font color=blue>分类名称</font></td><td width="60%"><font color=blue>显示方式</font></td></tr>
	$forumlist
	</table>
	</td>
	</tr>
	<tr>
	<td bgcolor=#EEEEEE align=center colspan=4>
	<font color=#990000><b>分论坛一览表(包含子论坛的)</b>
	</td>
	</tr>
	<tr>
	<td bgcolor=#FFFFFF align=center colspan=4>
	<table width="80%" align="center" cellspacing="0" cellpadding="5" border="0">
	<tr bgcolor="#DDDDDD"><td><font color=blue>分论坛名称</font></td><td width="60%"><font color=blue>显示方式</font></td></tr>
	$pforumlist
	</table>
	</td>
	</tr>
	<tr>
	<td bgcolor=#FFFFFF align=center colspan=2>
	<input type=submit value="提 交">
	</td>
	</tr>
	</form>
	~;
}
sub modify{
	print qq~
	<tr>
	<td bgcolor=#EEEEEE align=center colspan=4>
	<font color=#990000><b>显示方式设定完毕</b>
	</td>
	</tr>
	~;
	unlink "${lbdir}data/category_display.cgi" if(-e "${lbdir}data/category_display.cgi");
	chomp @selectid;
	chomp @pselectid;
	$category_count = 0;
	$parent_count = 0;
	%CATEDISPLAY_SET = ();
	%PARENTDISPLAY_SET = ();
	open(FILE, ">${lbdir}data/category_display.cgi");
	flock(FILE, 2) if ($OS_USED eq "Unix");
	print FILE "\%category_display_type=(\n";
	foreach $categoryid (@selectid) {
		next unless ($categoryid =~ /^[0-9]+$/);
		if(!defined $CATEDISPLAY_SET{$categoryid}){
			$CATEDISPLAY_SET{$categoryid} = 'DIS';
			my $displaytype = $query->param('display_type['.$categoryid.']');
			$displaytype = ($displaytype eq "basic")?"basic":"adv";
			print FILE ",\n" if($category_count);
			print FILE "\t'".$categoryid."' => '".$displaytype."'";
			$category_count++;
		}
	}
	print FILE "\n";
	print FILE ");\n";
	print FILE "\%pforum_display_type=(\n";
	foreach $pforumid (@pselectid) {
		next unless ($pforumid =~ /^[0-9]+$/);
		if(!defined $PARENTDISPLAY_SET{$pforumid}){
			$PARENTDISPLAY_SET{$categoryid} = 'DIS';
			my $displaytype = $query->param('pdisplay_type['.$pforumid.']');
			$displaytype = ($displaytype eq "basic")?"basic":"adv";
			print FILE ",\n" if($parent_count);
			print FILE "\t'".$pforumid."' => '".$displaytype."'";
			$parent_count++;
		}
	}
	print FILE "\n";
	print FILE ");\n";
	print FILE "1;\n";
	close(FILE);
	if($category_count){
		print qq~
	<tr>
	<td bgcolor=#FFFFFF colspan="4" align="center" height="50" valign="middle">已经设定了 $category_count 个分类的显示方式</td>
	</tr>
	~;
	}
	if($parent_count){
		print qq~
	<tr>
	<td bgcolor=#FFFFFF colspan="4" align="center" height="50" valign="middle">已经设定了 $parent_count 个母论坛的显示子论坛方式</td>
	</tr>
	~;
	}
}

sub errorout{
	$errormsg = shift;
	print qq~
	<tr>
	<td bgcolor=#EEEEEE align=center colspan=4>
	<font color=#990000><b>设定程式出错</b>
	</td>
	</tr>
	<tr>
	<td bgcolor=#FFFFFF colspan="4" align="center"><font color=red>$errormsg</font></td>
	</tr>
	<tr>
	<td bgcolor=#FFFFFF colspan="4" align="center" height="100" valign="bottom">-- <a href="$thisprog">返回</a> --</td>
	</tr>
	~;
}