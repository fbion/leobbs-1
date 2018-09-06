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
$LBCGI::POST_MAX = 200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;

$versionnumber = "LeoBBS X Build060331";

$|++;
$query = new LBCGI;
$action = $query->param('action');

$mypath = mypath(); #    	返回当前的绝对路径 (正确) 最后没有 /
$myurl  = myurl();  #    	返回当前的 URL 路径 (正确) 最后没有 /
($html_dir, $html_url) = split(/\|/,myimgdir()); # 返回当前图像目录的绝对路径和 url 路径 (不一定正确) 最后没有 /

if (-e "$mypath/data/install.lock") {
    &output("<BR><BR><BR><font size=+1 color=red><center>警告！！安装程序被锁定，无法重复安装。<BR><BR><BR>请手工删除 data 目录下的 install.lock 文件后重新运行。</center></font><BR><BR><BR>");
    exit;
}

if ($action eq "") {
    $output = qq~
<script>
function selectimg(){
document.bbsimg.src = FORM.imagesurl.value+"/images/teamad.gif";}
</script>
<BR>
　　在进行安装前，请先确定您已经完整上传了整个论坛程序和图片文件，并已经按照要求设置好了所有目录和文件的属性。<BR>
　　下面 1 和 2 中的默认设置是由程序自动判断生成的，适用于大部分安装本程序的客户，如果有错误，请自行修改成正确的值。<BR><BR>
　　☆ <a href=http://www.leobbs.com/leobbs/buy.asp target=_blank><B>如果因为您水平有限而无法正常安装和使用本论坛，请按此注册本论坛商业版，获得安装使用协助等技术支持与服务。</B></a><BR><BR>
<form action="install.cgi" method=POST name=FORM>
<input name=action type=hidden value="proceed">
　<font color=red><B>1.</B> </font><font color=blue>设置程序脚本的路径（一般情况下，自动判断程序获得这里的数据都是正确的）</font><BR>
　脚本程序(cgi-bin)的安装路径　　<input name=lbdir type=text size=55 value="$mypath/">　<font color=red>结尾有 "/"</font><br>
　脚本程序(cgi-bin)的 URL 路径　 <input name=boardurl type=text size=55 value="$myurl">　<font color=red>结尾没有 "/"</font><br>
<br><br>
　<font color=red><B>2.</B> </font><font color=blue>设置图像文件的路径（如果第二行的最后有笑脸图的话，就说明第二行填写的数据是正确的，否则请自行修改填写）</font><BR>
　图像文件(non-cgi)的安装路径　　<input name=imagesdir type=text size=55 value="$html_dir/">　　　<font color=red>结尾有 "/"</font><br>
　图像文件(non-cgi) URL 路径　 　<input name=imagesurl type=text size=55 value="$html_url" onChange=selectimg() onkeydown=selectimg() onkeyup=selectimg() onselect=selectimg()> <img name=bbsimg src=$html_url/images/teamad.gif width=16 height=14 title=如果你能看到这张笑脸图的话，就说明这里填写的数据是正确的>　<font color=red>结尾没有 "/"</font><br>
<br><br><br>
　<font color=red><B>3.</B> </font><font color=blue>设置初始化管理员（如果是升级安装的话，那么这里是无需填写的，请务必留空）</font><BR>
　初始管理员用户名　　<input name=adminname type=text size=14 maxlenght=12>　　　　开头不要使用客人字样，也不要超过12个字符（6个汉字）<br>
　初始管理员密码　　　<input name=adminpass type=password size=20>　只允许大小写字母和数字的组合，不能全部是数字，并不得少于8个字符<br>
　初始管理员密码　　　<input name=adminpass1 type=password size=20>　请按照上一行再重新输一遍，以便确定！<br>
<br><BR>
<center><input type=submit value=" 设 定 完 毕 " OnClick="return confirm('确定设置正确并保存么？');"></form>
~;
   &output("$output");
   exit;
}

if ($action eq "proceed") {
	$lbdir     = $query->param("lbdir");
	$lbdir     =~ s/\/$//isg;
	$mypath    = $lbdir;
	$lbdir     = "${lbdir}/";
	$boardurl  = $query->param("boardurl");
	$boardurl  =~ s/\/$//isg;
	$imagesdir = $query->param("imagesdir");
	$imagesdir =~ s/\/$//isg;
	$imagesdir = "${imagesdir}/";
	$imagesurl = $query->param("imagesurl");
	$imagesurl =~ s/\/$//isg;
	$adminname = $query->param("adminname");
	$adminpass = $query->param("adminpass");
	$adminpass1= $query->param("adminpass1");

	unlink ("$mypath/record.cgi");
	opendir (DIRS, "$mypath");
	my @files = readdir(DIRS);
	closedir (DIRS);
	my @searchdir = grep(/^search/i, @files);
	$searchdir = @searchdir;
	my @memdir = grep(/^members/i, @files);
	$memdir = @memdir;
	my @msgdir = grep(/^messages/i, @files);
	$msgdir = @msgdir;
	my @recorddir = grep(/^record/i, @files);
	$recorddir = @recorddir;
	my @ftpdir = grep(/^ftpdata/i, @files);
	$ftpdir = @ftpdir;
	my @memfavdir = grep(/^memfav/i, @files);
	$memfavdir = @memfavdir;

	if (($searchdir > 2)||($memdir > 1)||($msgdir > 1)||($recorddir > 1)||($ftpdir > 1)||($memfavdir > 1)) {
	    if ($searchdir > 2)    { $output = "search 开头的目录有两个或两个以上"; }
	    elsif ($memdir > 1)    { $output = "members 开头的目录有两个或两个以上"; }
	    elsif ($recorddir > 1) { $output = "record 开头的目录有两个或两个以上"; }
	    elsif ($ftpdir > 1)    { $output = "ftpdata 开头的目录有两个或两个以上"; }
	    elsif ($msgdir > 1)    { $output = "messages 开头的目录有两个或两个以上"; }
	    elsif ($memfavdir > 1) { $output = "memfav 开头的目录有两个或两个以上"; }
	    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>$mypath 目录下的以 $output，<BR><BR>请删除多余的，保持此相关目录只有一个，然后重新运行安装程序一次。</font><BR><BR><BR>");
	    exit;
	}

	$memdir = $memdir[0];
	$msgdir = $msgdir[0];
	$memfavdir = $memfavdir[0];
	&changemod($mypath, $html_dir);
	chmod(0777,"$mypath/$memdir");
	mkdir("$mypath/$memdir/old",0777) unless (-e "$mypath/$memdir/old");
	chmod(0777,"$mypath/$memdir/old");
	chmod(0777,"$mypath/data");
	$memdirwritabler = $memdirwritabler1 = $datadirwritabler ="";
	$makefile = "$mypath/$memdir/test.txt";
	open (TEST, ">$makefile") or $memdirwritabler = "目录 $mypath/$memdir 为不可写，请改变属性为 777 。<BR>";
	print TEST "-";
	close (TEST);
	$memdirwritabler = "目录 $mypath/$memdir 为不可写，请改变属性为 777 。<BR>" if (!(-e "$makefile"));
	unlink "$makefile";
	$makefile = "$mypath/$memdir/old/test.txt";
	open (TEST, ">$makefile") or $memdirwritabler1 = "目录 $mypath/$memdir/old 为不可写，请改变属性为 777 。<BR>";
	print TEST "-";
	close (TEST);
	$memdirwritabler1 = "目录 $mypath/$memdir/old 为不可写，请改变属性为 777 。<BR>" if (!(-e "$makefile"));
	unlink "$makefile";
	$makefile = "$mypath/data/test.txt";
	open (TEST, ">$makefile") or $datadirwritabler = "目录 $mypath/data 为不可写，请改变属性为 777 。<BR>";
	print TEST "-";
	close (TEST);
	$datadirwritabler = "目录 $mypath/data 为不可写，请改变属性为 777 。<BR>" if (!(-e "$makefile"));
	unlink "$makefile";
	if (($memdirwritabler ne "")||($memdirwritabler1 ne "")||($datadirwritabler)) {
	    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>$datadirwritabler$memdirwritabler$memdirwritabler1</font><BR><BR><BR>");
	    exit;
	}

	chmod(0666,"${lbdir}data/boardinfo.cgi");

	if (!(-e "${lbdir}data/boardinfo.cgi")) {
	    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>未发现 ${lbdir}data/boardinfo.cgi 文件，可能您输入的 *.cgi 脚本的安装路径错误，请返回重新输入。</font><BR><BR><BR>");
   	    exit;
	}
	if (!(-e "${imagesdir}images/logo.gif")) {
	    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>未发现 ${imagesdir}images/logo.gif 文件，可能您输入的 image 图像文件的安装路径错误，请返回重新输入。</font><BR><BR><BR>");
   	    exit;
	}

	if (($adminname ne "")&&($adminpass ne "")) {
		$adminnametemp = $adminname;
		$adminname =~ s/\&nbsp\;//ig;
		$adminname =~ s/　/ /g;
		$adminname =~ s// /g;
		$adminname =~ s/[ ]+/ /g;
		$adminname =~ s/[ ]+/_/;
		$adminname =~ s/[_]+/_/;
		$adminname =~ s/�//isg;
		$adminname =~ s///isg;
		$adminname =~ s/　//isg;
		$adminname =~ s///isg;
		$adminname =~ s/()+//isg;
		$adminname =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?\[\]]//isg;
		$adminname =~ s/\s*$//g;
		$adminname =~ s/^\s*//g;
		if ($adminnametemp ne $adminname) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>您输入的管理员用户名有问题，请返回重新输入！</font><BR><BR><BR>");
   		    exit;
		}
		if ($adminname =~ /^客人/) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>请不要在管理员用户名的开头中使用客人字样，请返回重新输入！</font><BR><BR><BR>");
   		    exit;
		}
    		if (length($adminname)>12) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>管理员用户名太长，请不要超过12个字符（6个汉字），请返回重新输入！</font><BR><BR><BR>");
   		    exit;
    		}
    		if (length($adminname)<2)  {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>管理员用户名太短了，请不要少於2个字符（1个汉字），请返回重新输入！</font><BR><BR><BR>");
   		    exit;
    		}

	        if ($adminpass =~ /[^a-zA-Z0-9]/) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>管理员密码只允许大小写字母和数字的组合，请返回后更换！</font><BR><BR><BR>");
   		    exit;
	        }
		if ($adminpass =~ /^lEO/) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>管理员密码不允许是 lEO 开头，请返回后更换！</font><BR><BR><BR>");
   		    exit;
		}
	        if (length($adminpass)<8) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>管理员密码太短了，请返回后更换（密码必须 8 位以上）！</font><BR><BR><BR>");
   		    exit;
	        }
		if ($adminpass =~ /^[0-9]+$/) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>管理员密码不能全部为数字，请返回后更换！</font><BR><BR><BR>");
   		    exit;
		}
		if ($adminname eq $adminpass) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>不要将管理员用户名和管理员密码设置成相同的，请返回后更换！</font><BR><BR><BR>");
   		    exit;
		}
		if ($adminpass ne $adminpass1) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>对不起，您输入的两次管理员密码不相同，请返回重新输入！</font><BR><BR><BR>");
   		    exit;
		}
	}
	
	open(FILE, "${lbdir}data/boardinfo.cgi");
	@info = <FILE>;
	close(FILE);

	if (open(FILE, ">${lbdir}data/boardinfo.cgi")) {
	    print FILE "\$lbdir = '$lbdir';\n";
	    print FILE "\$boardurl = '$boardurl';\n";
	    print FILE "\$imagesdir = '$imagesdir';\n";
	    print FILE "\$imagesurl = '$imagesurl';\n";

	    eval('flock(FILE, 2);');
	    print FILE $@ ne '' ? "\$OS_USED = 'Nt';\n" : "\$OS_USED = 'Unix';\n";

	    foreach (@info) {
		chomp;
		next if (($_ =~ /^\$lbdir/)||($_ =~ /^\$imagesdir/)||($_ =~ /^\$boardurl/)||($_ =~ /^\$imagesurl/)||($_ =~ /^\$OS_USED/)||($_ eq ""));
		print FILE "$_\n";
	    }
	    print FILE "\n";
	    close(FILE);
	} else {
	    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>${lbdir}data/boardinfo.cgi 文件不可写，请手工设置其属性为 666 ，然后刷新本页面继续。</font><BR><BR><BR>");
   	    exit;
	}

	if (($adminname ne "")&&($adminpass ne "")) {
		$oldadminname = $adminname;
		$adminname =~ s/ /\_/g;
		$adminname =~ tr/A-Z/a-z/;
	        my $namenumber = ((ord(substr($adminname,0,1))&0x3c)<<3)|((ord(substr($adminname,1,1))&0x7c)>>2);
#		my $namenumber = int((ord(substr($adminname,0,1))+ord(substr($adminname,1,1)))/2);
		mkdir ("${lbdir}$memdir/$namenumber", 0777) if (!(-e "${lbdir}$memdir/$namenumber"));
		chmod(0777,"${lbdir}$memdir/$namenumber");
		if ((-e "$lbdir$memdir/$namenumber/$adminname.cgi")||(-e "$lbdir$memdir/old/$adminname.cgi")) {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>管理员账号 $oldadminname 已经存在，请返回更换！</font><BR><BR><BR>");
   		    exit;
		}
	        eval {$adminpass = md5_hex($adminpass);};
	        if ($@) {eval('use Digest::MD5 qw(md5_hex);$adminpass = md5_hex($adminpass);');}
	        unless ($@) {$adminpass = "lEO$adminpass";}

		opendir(DIR, $lbdir);
		@files = readdir(DIR);
		closedir(DIR);
		@memdirs = grep(/^members/i, @files);
		$memdir = $memdirs[0];
		chmod(0777,"$lbdir$memdir");
		mkdir("$lbdir$memdir/old",0777) unless (-e "$lbdir$memdir/old");
		chmod(0777,"$lbdir$memdir/old");
		my $currenttime = time;
		
		if (open(FILE, ">$lbdir$memdir/$namenumber/$adminname.cgi")) {
		    print FILE "$adminname\t$adminpass\tmember\tad\t0|0\t\tno\t保密\t\t\t\t\t\t$currenttime\t\t";
		    close(FILE);
		} else {
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>${lbdir}$memdir 目录不可写，请手工设置其属性为 777 ，然后刷新本页面继续。</font><BR><BR><BR>");
   		    exit;
		}
		if (open(FILE, ">$lbdir$memdir/old/$adminname.cgi")) {
		    print FILE "$adminname\t$adminpass\tmember\tad\t0|0\t\tno\t保密\t\t\t\t\t\t$currenttime\t\t";
		    close(FILE);
		} else {
		    unlink("$lbdir$memdir/$namenumber/$adminname.cgi");
		    &output("<BR><font size=+1 color=red><center>安装程序发现错误！</font><BR><BR><BR>${lbdir}$memdir/old 目录不可写，请手工设置其属性为 777 ，然后刷新本页面继续。</font><BR><BR><BR>");
   		    exit;
		}
		$output = "管理员账号 $oldadminname　建立成功！";
	}

	open(LOCK, ">${lbdir}data/install.lock");
	print LOCK "www.LeoBBS.com";
	close(LOCK);
	unlink("${lbdir}install.cgi") if (!(-e "${lbdir}data/install.lock"));
	&changedirname();  # 更改用户关键目录的名称
        &output("<BR><font size=+1 color=red><center>论坛安装完成！$output</font><BR><BR><BR>论坛安装已经顺利完成！目前安装程序已经自动锁定，无法再次执行，但我们还是强烈建议您直接将其从服务器上删除。<BR><BR>如果需要再次运行安装程序，请先手工将 data 目录下的 install.lock 文件删除，然后再运行安装程序！<BR><BR><BR>现在您可以使用管理员账号和密码进入 <a href=admin.cgi><B>论坛管理中心</B></a> 重新设置所有基本变量和风格参数。<BR><BR><BR>");
        $versionnumber =~ s/\<(.+?)\>//isg;
	&sendurlinfo("www.leobbs.com","download/reg.cgi","ver=$versionnumber&url=$boardurl") if (($boardurl ne "")&&($boardurl !~ m/localhost/i)&&($boardurl !~ m/127\.0\.0\./i)&&($boardurl !~ m/192\.168\./i));
        exit;
}

# 参数不对．
&output("<BR><BR><BR><font size=+1 color=red><center>请不要胡乱运行本程序，谢谢合作！</center></font><BR><BR><BR>");
exit;

sub output {
    my $outputinfo = shift;
    print header(-charset=>UTF-8 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
    print qq~
<html>
  <head>
    <meta charset="UTF-8">
    <title>LeoBBS X 安装程序</title>
    <style type="text/css">
    A:visited{TEXT-DECORATION: none}
    A:active{TEXT-DECORATION: none}
    A:hover{TEXT-DECORATION: underline overline}
    A:link{text-decoration: none;}
    .h        { font-family: 宋体; font-size: 12px; color: #FF0000 }
    .t        { font-family: 宋体; font-size: 11px; color: #000003 }
    .ti       { font-family: 宋体; font-size: 12px; color: #000003; font-weight: bold }
    .l        { font-family: 宋体; font-size: 14px; font-weight: bold; color: #FFFFFF }
    BODY{FONT-FAMILY: 宋体; FONT-SIZE: 9pt;}
    caption,TD,DIV,form ,OPTION,P,TD,BR{FONT-FAMILY: 宋体; FONT-SIZE: 9pt} 
    INPUT, SUBMIT { font-family: 宋体; font-size: 9pt; font-family: 宋体; vertical-align:middle; background-color: #CCCCCC; }
    a:active, a:link, a:visited { color:#000099 }
    </style>
  </head>
  <body marginheight='0' marginwidth='0' leftmargin='0' topmargin='10' bgcolor='#EEEEEE'>
  <table cellspacing='0' cellpadding='0' width=770 align='center' border='0' height='100%'>
  <tr>
    <td valign='middle' align=center class='l'>
      <table cellspacing='1' cellpadding='0' width='100%' align='center' border='0' bgcolor='#000000'>
       <tr>
        <td>
          <table cellspacing='0' cellpadding='4' width='100%' align='center' border='0'>
          <tr>
            <td bgcolor='#666699' class='l' align='center'>雷傲极酷超级论坛 LeoBBS X 安装程序</td>
          </tr>
          <tr>
            <td bgcolor='#8888AA' class='l' align='left'><span style='font-size:6pt;color:#8888AA'>.</span></td>
          </tr>
          <tr>
            <td valign='top' bgcolor='#FFFFFFF'><span font-family: 宋体; font-size: 9pt;>
		$outputinfo<BR>
	　　☆ <a href=http://www.leobbs.com/leobbs/buy.asp target=_blank><B>如果因为您水平有限而无法正常安装和使用本论坛，请按此注册本论坛商业版，获得安装使用协助等技术支持与服务。</B></a><BR><BR>
            </td>
          </tr>
          </table>
         </td>
        </tr>
      </table>
      <BR><BR><hr width=500><font color=black>版权所有：<a href=http://www.leobbs.com target=_blank>雷傲科技</a> & <a href=http://bbs.leobbs.com target=_blank>雷傲极酷超级论坛</a>　　Copyright 2003-2004<BR>
    </td>
   </tr>
  </table>
 </body>
</html>
~;
}

sub changemod {
    my ($cgibinpath, $noncgipath) = @_;
    opendir (DIRS, "$noncgipath");
    my @files = readdir(DIRS);
    closedir (DIRS);
    my @usrdir = grep(/^usr/i, @files);
    my $usrdir = $usrdir[0];
    $usrdir = $usrdir[1] if (lc($usrdir) eq 'usravatars');
    chmod(0777,"$noncgipath/$usrdir");
    chmod(0777,"$noncgipath/myimage");
    chmod(0777,"$noncgipath/usravatars");
    chmod(0777,"$noncgipath/face");
    chmod(0777,"$noncgipath/face/js");
    opendir (DIRS, "$cgibinpath");
    my @files = readdir(DIRS);
    closedir (DIRS);
    foreach (@files) { chmod(0777,"$cgibinpath/$_") if ($_ !~ /\./); }
    my @files1 = grep(/\.cgi/i, @files);
    foreach (@files1) { chmod(0755,"$cgibinpath/$_"); }
    @files1 = grep(/\.pl/i, @files);
    foreach (@files1) { chmod(0755,"$cgibinpath/$_"); }
    @files1 = grep(/\.pm/i, @files);
    foreach (@files1) { chmod(0755,"$cgibinpath/$_"); }
    mkdir("$cgibinpath/$memdir/old",0777) unless (-e "$cgibinpath/$memdir/old");
    chmod(0777,"$cgibinpath/$memdir/old");
    mkdir("$cgibinpath/$msgdir/in",0777) unless (-e "$cgibinpath/$msgdir/in");
    chmod(0777,"$cgibinpath/$msgdir/in");
    mkdir("$cgibinpath/$msgdir/main",0777) unless (-e "$cgibinpath/$msgdir/main");
    chmod(0777,"$cgibinpath/$msgdir/main");
    mkdir("$cgibinpath/$msgdir/out",0777) unless (-e "$cgibinpath/$msgdir/out");
    chmod(0777,"$cgibinpath/$msgdir/out");
    mkdir("$cgibinpath/$msgdir/modscarddata",0777) unless (-e "$cgibinpath/$msgdir/modscarddata");
    chmod(0777,"$cgibinpath/$msgdir/modscarddata");
    mkdir("$cgibinpath/$memfavdir/open",0777) unless (-e "$cgibinpath/$memfavdir/open");
    chmod(0777,"$cgibinpath/$memfavdir/open");
    mkdir("$cgibinpath/$memfavdir/close",0777) unless (-e "$cgibinpath/$memfavdir/close");
    chmod(0777,"$cgibinpath/$memfavdir/close");
    mkdir("$cgibinpath/verifynum",0777) unless (-e "$cgibinpath/verifynum");
    chmod(0777,"$cgibinpath/verifynum");
    mkdir("$cgibinpath/verifynum/login",0777) unless (-e "$cgibinpath/verifynum/login");
    chmod(0777,"$cgibinpath/verifynum/login");
}

sub sendurlinfo {
    eval("use Socket;");
    return if ($@ ne "");
    ($host,$path,$content) = @_;
    $host =~ s/^http:\/\///isg;
    $port = 80;
    $path = "/$path" if ($path !~ /^\//);
    my ($name, $aliases, $type, $len, @thataddr, $a, $b, $c, $d, $that);
    my ($name, $aliases, $type, $len, @thataddr) = gethostbyname($host);
    my ($a, $b, $c, $d) = unpack("C4", $thataddr[0]);
    my $that = pack('S n C4 x8', 2, $port, $a, $b, $c, $d);
    return unless (socket(S, 2, 1, 0));
    select(S);
    $| = 1;
    select(STDOUT);
    return unless (connect(S, $that));
    print S "POST http://$host/$path HTTP/1.0\n";
    print S "Content-type: application/x-www-form-urlencoded\n";
    my $contentLength = length $content;
    print S "Content-length: $contentLength\n";
    print S "\n";
    print S "$content";
    @results = <S>;
    close(S);
    undef $|;
    return;
}

# 测试绝对路径
sub mypath {
    local $temp;
    if ($ENV{'SERVER_SOFTWARE'} =~ /apache/i) {
        if ($ENV{'SCRIPT_FILENAME'}=~ /cgiwrap/i) {
            $temp=$ENV{'PATH_TRANSLATED'};
        }
        else {
            $temp=$ENV{'SCRIPT_FILENAME'};
        }
        $temp=~ s/\\/\//g if ($temp=~/\\/);
        $mypath=substr($temp,0,rindex($temp,"/"));
    }
    else {
    	$ENV{'PATH_TRANSLATED'} = $ENV{'SCRIPT_FILENAME'} if ($ENV{'PATH_TRANSLATED'} eq "");
        $mypath=substr($ENV{'PATH_TRANSLATED'},0,rindex($ENV{'PATH_TRANSLATED'},"\\"));
        $mypath=~ s/\\/\//g;
    }
    return $mypath;
}

# 测试 URL 路径
sub myurl {
    local $server_port,$fullurl;
    $server_port = ":$ENV{'SERVER_PORT'}" if ($ENV{'SERVER_PORT'} ne '80');
    if ($ENV{'HTTP_HOST'} ne "") { $fullurl = $ENV{'HTTP_HOST'}; } else { $fullurl = $ENV{'SERVER_NAME'}; }
    $fullurl = "$fullurl$server_port" if ($fullurl !~ /\:/);
    $fullurl = "http://$fullurl$ENV{'SCRIPT_NAME'}";
    $myurl   = substr($fullurl,0,rindex($fullurl,"/"));
    return $myurl;
}

# 测试图像目录的绝对路径和 url 路径
sub myimgdir {
  my $html_dir = $html_url = $base = $base1 = "";
  $base  = $mypath;
  $base1 = $myurl;
    if (-e "$base/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi";
	$html_url = "$base1/non-cgi";
    } elsif (-e "$base/lb5000/editor/selcolor.html") {
	$html_dir = "$base/lb5000";
	$html_url = "$base1/lb5000";
    } elsif (-e "$base/ib2000/editor/selcolor.html") {
	$html_dir = "$base/ib2000";
	$html_url = "$base1/ib2000";
    } elsif (-e "$base/lb/editor/selcolor.html") {
	$html_dir = "$base/lb";
	$html_url = "$base1/lb";
    } elsif (-e "$base/ib/editor/selcolor.html") {
	$html_dir = "$base/ib";
	$html_url = "$base1/ib";
    } elsif (-e "$base/bbs/editor/selcolor.html") {
	$html_dir = "$base/bbs";
	$html_url = "$base1/bbs";
    } elsif (-e "$base/leobbs/editor/selcolor.html") {
	$html_dir = "$base/leobbs";
	$html_url = "$base1/leobbs";
    } elsif (-e "$base/leo/editor/selcolor.html") {
	$html_dir = "$base/leo";
	$html_url = "$base1/leo";
    } elsif (-e "$base/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/lb5000/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/lb5000/non-cgi";
	$html_url = "$base1/lb5000/non-cgi";
    } elsif (-e "$base/ib2000/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/ib2000/non-cgi";
	$html_url = "$base1/ib2000/non-cgi";
    } elsif (-e "$base/lb/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/lb/non-cgi";
	$html_url = "$base1/lb/non-cgi";
    } elsif (-e "$base/ib/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/ib/non-cgi";
	$html_url = "$base1/ib/non-cgi";
    } elsif (-e "$base/bbs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/bbs/non-cgi";
	$html_url = "$base1/bbs/non-cgi";
    } elsif (-e "$base/leobbs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/leobbs/non-cgi";
	$html_url = "$base1/leobbs/non-cgi";
    } elsif (-e "$base/leo/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/leo/non-cgi";
	$html_url = "$base1/leo/non-cgi";
    } elsif (-e "$base/non-cgi/bbs/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/bbs";
	$html_url = "$base1/non-cgi/bbs";
    } elsif (-e "$base/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/non-cgi/lb/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/lb";
	$html_url = "$base1/non-cgi/lb";
    } elsif (-e "$base/non-cgi/lb5000/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/lb5000";
	$html_url = "$base1/non-cgi/lb5000";
    } elsif (-e "$base/non-cgi/ib2000/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/ib2000";
	$html_url = "$base1/non-cgi/ib2000";
    } elsif (-e "$base/non-cgi/ib/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/ib";
	$html_url = "$base1/non-cgi/ib";
    } elsif (-e "$base/non-cgi/leo/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/leo";
	$html_url = "$base1/non-cgi/leo";
    } elsif (-e "$base/non-cgi/leobbs/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/leobbs";
	$html_url = "$base1/non-cgi/leobbs";
    } elsif (-e "$base/htdocs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi";
	$html_url = "$base1/non-cgi";
    } elsif (-e "$base/htdocs/lb5000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/lb5000";
	$html_url = "$base1/lb5000";
    } elsif (-e "$base/htdocs/ib2000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/ib2000";
	$html_url = "$base1/ib2000";
    } elsif (-e "$base/htdocs/lb/editor/selcolor.html") {
	$html_dir = "$base/htdocs/lb";
	$html_url = "$base1/lb";
    } elsif (-e "$base/htdocs/ib/editor/selcolor.html") {
	$html_dir = "$base/htdocs/ib";
	$html_url = "$base1/ib";
    } elsif (-e "$base/htdocs/bbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/bbs";
	$html_url = "$base1/bbs";
    } elsif (-e "$base/htdocs/leobbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/leobbs";
	$html_url = "$base1/leobbs";
    } elsif (-e "$base/htdocs/leo/editor/selcolor.html") {
	$html_dir = "$base/htdocs/leo";
	$html_url = "$base1/leo";
    } elsif (-e "$base/htdocs/non-cgi/bbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/bbs";
	$html_url = "$base1/non-cgi/bbs";
    } elsif (-e "$base/htdocs/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/htdocs/non-cgi/lb/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/lb";
	$html_url = "$base1/non-cgi/lb";
    } elsif (-e "$base/htdocs/non-cgi/lb5000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/lb5000";
	$html_url = "$base1/non-cgi/lb5000";
    } elsif (-e "$base/htdocs/non-cgi/ib2000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/ib2000";
	$html_url = "$base1/non-cgi/ib2000";
    } elsif (-e "$base/htdocs/non-cgi/ib/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/ib";
	$html_url = "$base1/non-cgi/ib";
    } elsif (-e "$base/htdocs/non-cgi/leo/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/leo";
	$html_url = "$base1/non-cgi/leo";
    } elsif (-e "$base/htdocs/non-cgi/leobbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/leobbs";
	$html_url = "$base1/non-cgi/leobbs";
    }

  if (($html_dir eq "")||(!(-e "$html_dir/images/board.js"))) {
    if ($base =~ m|(.*)/(.+?)|) { $base  = $1; } else { $base  = $mypath; }
    if ($base1 =~ m|(.*)/(.+?)|)  { $base1 = $1; } else { $base1 = $myurl;  }
    if (-e "$base/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi";
	$html_url = "$base1/non-cgi";
    } elsif (-e "$base/lb5000/editor/selcolor.html") {
	$html_dir = "$base/lb5000";
	$html_url = "$base1/lb5000";
    } elsif (-e "$base/ib2000/editor/selcolor.html") {
	$html_dir = "$base/ib2000";
	$html_url = "$base1/ib2000";
    } elsif (-e "$base/lb/editor/selcolor.html") {
	$html_dir = "$base/lb";
	$html_url = "$base1/lb";
    } elsif (-e "$base/ib/editor/selcolor.html") {
	$html_dir = "$base/ib";
	$html_url = "$base1/ib";
    } elsif (-e "$base/bbs/editor/selcolor.html") {
	$html_dir = "$base/bbs";
	$html_url = "$base1/bbs";
    } elsif (-e "$base/leobbs/editor/selcolor.html") {
	$html_dir = "$base/leobbs";
	$html_url = "$base1/leobbs";
    } elsif (-e "$base/leo/editor/selcolor.html") {
	$html_dir = "$base/leo";
	$html_url = "$base1/leo";
    } elsif (-e "$base/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/lb5000/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/lb5000/non-cgi";
	$html_url = "$base1/lb5000/non-cgi";
    } elsif (-e "$base/ib2000/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/ib2000/non-cgi";
	$html_url = "$base1/ib2000/non-cgi";
    } elsif (-e "$base/lb/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/lb/non-cgi";
	$html_url = "$base1/lb/non-cgi";
    } elsif (-e "$base/ib/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/ib/non-cgi";
	$html_url = "$base1/ib/non-cgi";
    } elsif (-e "$base/bbs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/bbs/non-cgi";
	$html_url = "$base1/bbs/non-cgi";
    } elsif (-e "$base/leobbs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/leobbs/non-cgi";
	$html_url = "$base1/leobbs/non-cgi";
    } elsif (-e "$base/leo/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/leo/non-cgi";
	$html_url = "$base1/leo/non-cgi";
    } elsif (-e "$base/non-cgi/bbs/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/bbs";
	$html_url = "$base1/non-cgi/bbs";
    } elsif (-e "$base/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/non-cgi/lb/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/lb";
	$html_url = "$base1/non-cgi/lb";
    } elsif (-e "$base/non-cgi/lb5000/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/lb5000";
	$html_url = "$base1/non-cgi/lb5000";
    } elsif (-e "$base/non-cgi/ib2000/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/ib2000";
	$html_url = "$base1/non-cgi/ib2000";
    } elsif (-e "$base/non-cgi/ib/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/ib";
	$html_url = "$base1/non-cgi/ib";
    } elsif (-e "$base/non-cgi/leo/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/leo";
	$html_url = "$base1/non-cgi/leo";
    } elsif (-e "$base/non-cgi/leobbs/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/leobbs";
	$html_url = "$base1/non-cgi/leobbs";
    } elsif (-e "$base/htdocs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi";
	$html_url = "$base1/non-cgi";
    } elsif (-e "$base/htdocs/lb5000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/lb5000";
	$html_url = "$base1/lb5000";
    } elsif (-e "$base/htdocs/ib2000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/ib2000";
	$html_url = "$base1/ib2000";
    } elsif (-e "$base/htdocs/lb/editor/selcolor.html") {
	$html_dir = "$base/htdocs/lb";
	$html_url = "$base1/lb";
    } elsif (-e "$base/htdocs/ib/editor/selcolor.html") {
	$html_dir = "$base/htdocs/ib";
	$html_url = "$base1/ib";
    } elsif (-e "$base/htdocs/bbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/bbs";
	$html_url = "$base1/bbs";
    } elsif (-e "$base/htdocs/leobbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/leobbs";
	$html_url = "$base1/leobbs";
    } elsif (-e "$base/htdocs/leo/editor/selcolor.html") {
	$html_dir = "$base/htdocs/leo";
	$html_url = "$base1/leo";
    } elsif (-e "$base/htdocs/non-cgi/bbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/bbs";
	$html_url = "$base1/non-cgi/bbs";
    } elsif (-e "$base/htdocs/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/htdocs/non-cgi/lb/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/lb";
	$html_url = "$base1/non-cgi/lb";
    } elsif (-e "$base/htdocs/non-cgi/lb5000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/lb5000";
	$html_url = "$base1/non-cgi/lb5000";
    } elsif (-e "$base/htdocs/non-cgi/ib2000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/ib2000";
	$html_url = "$base1/non-cgi/ib2000";
    } elsif (-e "$base/htdocs/non-cgi/ib/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/ib";
	$html_url = "$base1/non-cgi/ib";
    } elsif (-e "$base/htdocs/non-cgi/leo/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/leo";
	$html_url = "$base1/non-cgi/leo";
    } elsif (-e "$base/htdocs/non-cgi/leobbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/leobbs";
	$html_url = "$base1/non-cgi/leobbs";
    }
  }
  if (($html_dir eq "")||(!(-e "$html_dir/images/board.js"))) {
    if ($base =~ m|(.*)/(.+?)|) { $base  = $1; } else { $base  = $mypath; }
    if ($base1 =~ m|(.*)/(.+?)|)  { $base1 = $1; } else { $base1 = $myurl;  }
    if (-e "$base/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi";
	$html_url = "$base1/non-cgi";
    } elsif (-e "$base/lb5000/editor/selcolor.html") {
	$html_dir = "$base/lb5000";
	$html_url = "$base1/lb5000";
    } elsif (-e "$base/ib2000/editor/selcolor.html") {
	$html_dir = "$base/ib2000";
	$html_url = "$base1/ib2000";
    } elsif (-e "$base/lb/editor/selcolor.html") {
	$html_dir = "$base/lb";
	$html_url = "$base1/lb";
    } elsif (-e "$base/ib/editor/selcolor.html") {
	$html_dir = "$base/ib";
	$html_url = "$base1/ib";
    } elsif (-e "$base/bbs/editor/selcolor.html") {
	$html_dir = "$base/bbs";
	$html_url = "$base1/bbs";
    } elsif (-e "$base/leobbs/editor/selcolor.html") {
	$html_dir = "$base/leobbs";
	$html_url = "$base1/leobbs";
    } elsif (-e "$base/leo/editor/selcolor.html") {
	$html_dir = "$base/leo";
	$html_url = "$base1/leo";
    } elsif (-e "$base/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/lb5000/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/lb5000/non-cgi";
	$html_url = "$base1/lb5000/non-cgi";
    } elsif (-e "$base/ib2000/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/ib2000/non-cgi";
	$html_url = "$base1/ib2000/non-cgi";
    } elsif (-e "$base/lb/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/lb/non-cgi";
	$html_url = "$base1/lb/non-cgi";
    } elsif (-e "$base/ib/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/ib/non-cgi";
	$html_url = "$base1/ib/non-cgi";
    } elsif (-e "$base/bbs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/bbs/non-cgi";
	$html_url = "$base1/bbs/non-cgi";
    } elsif (-e "$base/leobbs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/leobbs/non-cgi";
	$html_url = "$base1/leobbs/non-cgi";
    } elsif (-e "$base/leo/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/leo/non-cgi";
	$html_url = "$base1/leo/non-cgi";
    } elsif (-e "$base/non-cgi/bbs/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/bbs";
	$html_url = "$base1/non-cgi/bbs";
    } elsif (-e "$base/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/non-cgi/lb/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/lb";
	$html_url = "$base1/non-cgi/lb";
    } elsif (-e "$base/non-cgi/lb5000/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/lb5000";
	$html_url = "$base1/non-cgi/lb5000";
    } elsif (-e "$base/non-cgi/ib2000/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/ib2000";
	$html_url = "$base1/non-cgi/ib2000";
    } elsif (-e "$base/non-cgi/ib/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/ib";
	$html_url = "$base1/non-cgi/ib";
    } elsif (-e "$base/non-cgi/leo/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/leo";
	$html_url = "$base1/non-cgi/leo";
    } elsif (-e "$base/non-cgi/leobbs/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/leobbs";
	$html_url = "$base1/non-cgi/leobbs";
    } elsif (-e "$base/htdocs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi";
	$html_url = "$base1/non-cgi";
    } elsif (-e "$base/htdocs/lb5000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/lb5000";
	$html_url = "$base1/lb5000";
    } elsif (-e "$base/htdocs/ib2000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/ib2000";
	$html_url = "$base1/ib2000";
    } elsif (-e "$base/htdocs/lb/editor/selcolor.html") {
	$html_dir = "$base/htdocs/lb";
	$html_url = "$base1/lb";
    } elsif (-e "$base/htdocs/ib/editor/selcolor.html") {
	$html_dir = "$base/htdocs/ib";
	$html_url = "$base1/ib";
    } elsif (-e "$base/htdocs/bbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/bbs";
	$html_url = "$base1/bbs";
    } elsif (-e "$base/htdocs/leobbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/leobbs";
	$html_url = "$base1/leobbs";
    } elsif (-e "$base/htdocs/leo/editor/selcolor.html") {
	$html_dir = "$base/htdocs/leo";
	$html_url = "$base1/leo";
    } elsif (-e "$base/htdocs/non-cgi/bbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/bbs";
	$html_url = "$base1/non-cgi/bbs";
    } elsif (-e "$base/htdocs/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/htdocs/non-cgi/lb/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/lb";
	$html_url = "$base1/non-cgi/lb";
    } elsif (-e "$base/htdocs/non-cgi/lb5000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/lb5000";
	$html_url = "$base1/non-cgi/lb5000";
    } elsif (-e "$base/htdocs/non-cgi/ib2000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/ib2000";
	$html_url = "$base1/non-cgi/ib2000";
    } elsif (-e "$base/htdocs/non-cgi/ib/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/ib";
	$html_url = "$base1/non-cgi/ib";
    } elsif (-e "$base/htdocs/non-cgi/leo/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/leo";
	$html_url = "$base1/non-cgi/leo";
    } elsif (-e "$base/htdocs/non-cgi/leobbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/leobbs";
	$html_url = "$base1/non-cgi/leobbs";
    }
  }
  if (($html_dir eq "")||(!(-e "$html_dir/images/board.js"))) {
    if ($base =~ m|(.*)/(.+?)|) { $base  = $1; } else { $base  = $mypath; }
    if ($base1 =~ m|(.*)/(.+?)|)  { $base1 = $1; } else { $base1 = $myurl;  }
    if (-e "$base/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi";
	$html_url = "$base1/non-cgi";
    } elsif (-e "$base/lb5000/editor/selcolor.html") {
	$html_dir = "$base/lb5000";
	$html_url = "$base1/lb5000";
    } elsif (-e "$base/ib2000/editor/selcolor.html") {
	$html_dir = "$base/ib2000";
	$html_url = "$base1/ib2000";
    } elsif (-e "$base/lb/editor/selcolor.html") {
	$html_dir = "$base/lb";
	$html_url = "$base1/lb";
    } elsif (-e "$base/ib/editor/selcolor.html") {
	$html_dir = "$base/ib";
	$html_url = "$base1/ib";
    } elsif (-e "$base/bbs/editor/selcolor.html") {
	$html_dir = "$base/bbs";
	$html_url = "$base1/bbs";
    } elsif (-e "$base/leobbs/editor/selcolor.html") {
	$html_dir = "$base/leobbs";
	$html_url = "$base1/leobbs";
    } elsif (-e "$base/leo/editor/selcolor.html") {
	$html_dir = "$base/leo";
	$html_url = "$base1/leo";
    } elsif (-e "$base/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/lb5000/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/lb5000/non-cgi";
	$html_url = "$base1/lb5000/non-cgi";
    } elsif (-e "$base/ib2000/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/ib2000/non-cgi";
	$html_url = "$base1/ib2000/non-cgi";
    } elsif (-e "$base/lb/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/lb/non-cgi";
	$html_url = "$base1/lb/non-cgi";
    } elsif (-e "$base/ib/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/ib/non-cgi";
	$html_url = "$base1/ib/non-cgi";
    } elsif (-e "$base/bbs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/bbs/non-cgi";
	$html_url = "$base1/bbs/non-cgi";
    } elsif (-e "$base/leobbs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/leobbs/non-cgi";
	$html_url = "$base1/leobbs/non-cgi";
    } elsif (-e "$base/leo/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/leo/non-cgi";
	$html_url = "$base1/leo/non-cgi";
    } elsif (-e "$base/non-cgi/bbs/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/bbs";
	$html_url = "$base1/non-cgi/bbs";
    } elsif (-e "$base/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/non-cgi/lb/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/lb";
	$html_url = "$base1/non-cgi/lb";
    } elsif (-e "$base/non-cgi/lb5000/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/lb5000";
	$html_url = "$base1/non-cgi/lb5000";
    } elsif (-e "$base/non-cgi/ib2000/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/ib2000";
	$html_url = "$base1/non-cgi/ib2000";
    } elsif (-e "$base/non-cgi/ib/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/ib";
	$html_url = "$base1/non-cgi/ib";
    } elsif (-e "$base/non-cgi/leo/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/leo";
	$html_url = "$base1/non-cgi/leo";
    } elsif (-e "$base/non-cgi/leobbs/editor/selcolor.html") {
	$html_dir = "$base/non-cgi/leobbs";
	$html_url = "$base1/non-cgi/leobbs";
    } elsif (-e "$base/htdocs/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi";
	$html_url = "$base1/non-cgi";
    } elsif (-e "$base/htdocs/lb5000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/lb5000";
	$html_url = "$base1/lb5000";
    } elsif (-e "$base/htdocs/ib2000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/ib2000";
	$html_url = "$base1/ib2000";
    } elsif (-e "$base/htdocs/lb/editor/selcolor.html") {
	$html_dir = "$base/htdocs/lb";
	$html_url = "$base1/lb";
    } elsif (-e "$base/htdocs/ib/editor/selcolor.html") {
	$html_dir = "$base/htdocs/ib";
	$html_url = "$base1/ib";
    } elsif (-e "$base/htdocs/bbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/bbs";
	$html_url = "$base1/bbs";
    } elsif (-e "$base/htdocs/leobbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/leobbs";
	$html_url = "$base1/leobbs";
    } elsif (-e "$base/htdocs/leo/editor/selcolor.html") {
	$html_dir = "$base/htdocs/leo";
	$html_url = "$base1/leo";
    } elsif (-e "$base/htdocs/non-cgi/bbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/bbs";
	$html_url = "$base1/non-cgi/bbs";
    } elsif (-e "$base/htdocs/non-cgi/non-cgi/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/non-cgi";
	$html_url = "$base1/non-cgi/non-cgi";
    } elsif (-e "$base/htdocs/non-cgi/lb/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/lb";
	$html_url = "$base1/non-cgi/lb";
    } elsif (-e "$base/htdocs/non-cgi/lb5000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/lb5000";
	$html_url = "$base1/non-cgi/lb5000";
    } elsif (-e "$base/htdocs/non-cgi/ib2000/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/ib2000";
	$html_url = "$base1/non-cgi/ib2000";
    } elsif (-e "$base/htdocs/non-cgi/ib/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/ib";
	$html_url = "$base1/non-cgi/ib";
    } elsif (-e "$base/htdocs/non-cgi/leo/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/leo";
	$html_url = "$base1/non-cgi/leo";
    } elsif (-e "$base/htdocs/non-cgi/leobbs/editor/selcolor.html") {
	$html_dir = "$base/htdocs/non-cgi/leobbs";
	$html_url = "$base1/non-cgi/leobbs";
    }
  }
  $html_dir = $mypath if ($html_dir eq "");
  $html_url = $myurl  if ($html_url eq "");
  return "$html_dir|$html_url|";
}

sub changedirname {
    opendir (DIRS, "$lbdir");
    my @files = readdir(DIRS);
    closedir (DIRS);
    @files = grep(/^\w+?$/i, @files);
    my @searchdir = grep(/^search/i, @files);
    my $searchdir = $searchdir[0];
    my @memdir = grep(/^members/i, @files);
    my $memdir = $memdir[0];
    my @msgdir = grep(/^messages/i, @files);
    my $msgdir = $msgdir[0];
    my @memfavdir = grep(/^memfav/i, @files);
    my $memfavdir = $memfavdir[0];
    my @recorddir = grep(/^record/i, @files);
    my $recorddir = $recorddir[0];
    my @saledir = grep(/^sale/i, @files);
    my $saledir = $saledir[0];
   my @ftpdir = grep(/^ftpdata/i, @files);
   my $ftpdir = $ftpdir[0];
   opendir(DIRS, $imagesdir);
   my @files = readdir(DIRS);
   closedir(DIRS);
   @files = grep(/^\w+?$/i, @files);
   my @usrdir = grep(/^usr/i, @files);
   my $usrdir = $usrdir[0];
   $usrdir = $usrdir[1] if (lc($usrdir) eq 'usravatars');

	my $x = &myrand(1000000000);
	$x = crypt($x, aun);
	$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
	$x =~ s/[^\w\d]//g;
	$x = substr($x, 2, 9);
	$usrdir    = "usr$x"      if (rename("$imagesdir$usrdir", "${imagesdir}usr$x"));
	$recorddir = "record$x"   if (rename("$lbdir$recorddir",  "${lbdir}record$x"));
	$saledir = "sale$x"   if (rename("$lbdir$saledir",  "${lbdir}sale$x"));

	my $x = &myrand(1000000000);
	$x = crypt($x, aun);
	$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
	$x =~ s/[^\w\d]//g;
	$x = substr($x, 2, 9);
	$memdir    = "members$x"  if (rename("$lbdir$memdir",     "${lbdir}members$x"));
	$msgdir    = "messages$x" if (rename("$lbdir$msgdir",     "${lbdir}messages$x"));

	my $x = &myrand(1000000000);
	$x = crypt($x, aun);
	$x =~ s/%([a-fA-F0-9]{2})/pack("C", hex($1))/eg;
	$x =~ s/[^\w\d]//g;
	$x = substr($x, 2, 9);
	$searchdir = "search$x"   if (rename("$lbdir$searchdir",  "${lbdir}search$x"));
	$ftpdir    = "ftpdata$x"  if (rename("$lbdir$ftpdir",     "${lbdir}ftpdata$x"));
	$memfavdir = "memfav$x"   if (rename("$lbdir$memfavdir",  "${lbdir}memfav$x"));
}