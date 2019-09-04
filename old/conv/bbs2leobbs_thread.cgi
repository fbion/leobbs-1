#!/usr/bin/perl

#
# 程序编制：清凉
#  这是一个单独的转换程序，结合BBS3000用户数据到LeoBBS转换程序，可以把原BBS3000的数据
#  比较完整地移植到LeoBBS。
#  具体做法： 
#   把该程序上传到论坛的主目录，设置权限为755，然后修改其中的$id="admin";，把其中的“admin”
#   改为你要转换的论坛的具体哪个栏目对应的$id，把$filepath= "/home/httpd/cgi-bin/bbs3000"； 
#   按照提示做特定的修改。然后把BBS3000主目录，也就是$filepath对应的目录权限设置为777，再
#   执行即可。程序会自动在该目录下创建trans子目录，如果转换的id是admin，还会自动在trans目录
#   下创建admin子目录。转换后的数据就放在里面。转换结束后会提示应该转换多少，实际转换多少，
#   如果两数字保持一致，基本就转换成功了。 
#   然后在LB5000里通过管理中心创建一个论坛，譬如创建一个论坛，名称为“波动心弦”，对应的目录
#   为forum21。把转换后的数据设法拷贝到forum21目录里，设置该目录里所有文件权限为666。
#   进入管理中心，重新整理该论坛即可。最后重新统计一下整个论坛的文章数，就可以用了。
#   在程序里有一个函数可能对大家有用，就是t2t。如果大家使用了localtime函数，对时间进行过分解。
#   再想要把分解过后的时间还原成time函数生成的时间串，可以参照里面的t2t函数。直接把两个相关
#   子函数拷贝到你的程序里，然后在程序开始的地方加入use Time::Local; 就行了。 

#   还有，那个$id,不是LeoBBS里的东东，是BBS3000里的论坛ID，譬如，有个“CGI论坛”吗，你看它的
#   连接是http://www.yuzi.net/cgi-bin/bbs3000/bbs.cgi?id=yuzi，这个里面红的yuzi就是$id，也就
#   是说如果想转换这个CGI论坛（当然它只是整个论坛里的一个子论坛），那么应该这么设置$id="yuzi";。
#   如果能够申请，我用“清凉”名字申请一个，那么对应我的论坛的
#   URL就是http://www.yuzi.net/cgi-bin/bbs3000/bbs.cgi?id=清凉，那么设置就应该是$id="清凉"; 



use Time::Local;
print ("Content-type: text/html\n\n"); 

my $filepath     = "/home/httpd/cgi-bin/bbs3000";   # 和BBS3000中的$filepath内容保持一致

my $id="admin"; # 为要转换的论坛代号

my $transdir="${filepath}/trans";
my $maxsavepost=14;

mkdir("$transdir",0777);
mkdir("$transdir/$id",0777);



$wennowno=0; $wentotal=0;

open(TITLES,"$filepath/list/$id/bbs");
@hastitles=<TITLES>;
close(TITLES);
@hastitles=sort @hastitles;
$usertotalall=@hastitles;

foreach $wentitletmp(@hastitles) {
	$wentitletmp=~ s/\n//g;
	if($wentitletmp ne "") {
		$wentitle=substr($wentitletmp,0,14);
	}

	$wennowno +=1;
	$theplfile=""; $thecgifile="";

	$wen="$filepath/list/$id/$wentitle";
	if (-f $wen){
   		open (FILE, "$wen");
		$weninfo=<FILE>;
		close (FILE);
		($rtitles,$rthistime,$rusername,$nr,$rfrom,$rhasreply,$remote,$rlastname,$rlasttime,$re,$rhassee,$jing,$lock)=split(/\t/,$weninfo);
	}
	
	$wentotal++;
	$ttime=t2t($rthistime);
	$thecgifile="$rusername\t$rtitles\t\tyes\tyes\t$ttime\t$nr\t\t\n";
	$ttimelast=t2t($rlasttime);

	if($rhasreply > 0){
		$wenre="$filepath/list/$id/$re";
		if (-f $wenre){
			open(REPLY,"$wenre");
			@hasreply=<REPLY>;
			close(REPLY);
			@hasreply=sort @hasreply;
			$no1=@hasreply;
			foreach $m (@hasreply){
				$m=~ s/\n//g;
				if($m ne ""){
					($rtime2,$rthistime2,$rusername2,$rcomment2,$rfrom2,$remote2,$retitles2)=split(/\t/,$m);
					if ($rtime2 eq $wentitle) {
						$wentotal++;
						$ttime2=t2t($rthistime2);
						$thecgifile .="$rusername2\t$rtitles\t\tyes\tyes\t$ttime2\t$rcomment2\t\t\n";
					}
				}
			}
			undef(@hasreply);
		}
	}
	my $theinfo=weninfo($rcomment2);
	$theplfile="$wennowno\t$rtitles\t\topen\t$no1\t$rhassee\t$rusername\t$ttime\t$rlastname\t$ttimelast\t$theinfo\t";

	open(FILE,">$transdir/$id/${wennowno}.pl");
	print FILE $theplfile;
	close FILE;

	open(FILE,">$transdir/$id/${wennowno}.thd.cgi");
	print FILE $thecgifile;
	close FILE;
		
	print "已转换 $wennowno 个主题\n";
}
print "转换专栏 $id 结束.\n";
print "应转换 $usertotalall 个主题，实际转换 $wennowno 个主题.\n";
print "实际转换 $wentotal 篇文章.\n";
print "请到 $transdir/$id 目录里查看转换是否正确。\n";


sub t2t{
#转换之前的日期格式为2001-05-08.00:15:38,
#其他的日期如果具备这几项内容,按照格式对下面时间的定位做一些修改，就可以用这个函数
	my $ntime=shift;
	my($secn,$minn,$hourn,$dayn,$monn,$yearn);
	$yearn=substr($ntime,0,4); $monn=substr($ntime,5,2); $dayn=substr($ntime,8,2);
	$hourn=substr($ntime,11,2); $minn=substr($ntime,14,2); $secn=substr($ntime,17,2);
	$yearn=int($yearn)-1900;   
	$monn=dotime($monn)-1;
	$dayn=dotime($dayn);
	$hourn=dotime($hourn);
	$minn=dotime($minn);
	$secn=dotime($secn);
	$time = timelocal($secn,$minn,$hourn,$dayn,$monn,$yearn);
	return $time;
}

sub dotime {
	my $dtime=shift;
	$dtime=substr($dtime,1,1) if(substr($dtime,0,1) eq "0");
	$dtime=int($dtime);
	$dtime=1 if($dtime<1);
	return $dtime;
}

sub weninfo {
	my $inposttemp=shift;
        if (length($inposttemp)>$maxsavepost) {
            $inposttemp = substr($inposttemp,0,$maxsavepost)."  ...";
        }
        return $inposttemp;
}