#! /usr/bin/perl

#
# 程序编制：清凉
# 这是一个单独的转换程序，结合我以前发表的一山论坛用户数据到LeoBBS转换程序，可以把原一山论坛
# 比较完整地移植到LeoBBS。
#
# 具体做法： 
#   把该程序上传到论坛的主目录，设置权限为755，然后修改其中的$key_input="5";，把其中的“5”
#   改为你要转换的论坛的具体哪个栏目对应的数字，然后执行即可。程序会自动在该目录下创建trans子
#   目录，如果转换的栏目数字是5，还会自动在trans目录下创建5子目录。转换后的数据就放在里面。
#   转换结束后会提示应该转换多少，实际转换多少，如果两数字保持一致，基本就转换成功了。 
#   然后在 LeoBBS 里通过管理中心创建一个论坛，譬如创建一个论坛，名称为“波动心弦”，对应的
#   目录为forum21。把转换后的数据设法拷贝到forum21目录里，设置该目录里所有文件权限为666。 
#   进入管理中心，重新整理该论坛即可。最后重新统计一下整个论坛的文章数，就可以用了。 
#   在程序里有一个函数可能对大家有用，就是t2t。如果大家使用了localtime函数，对时间进行过分解。
#   再想要把分解过后的时间还原成time函数生成的时间串，可以参照里面的t2t函数。直接把两个相关
#   子函数拷贝到你的程序里，然后在程序开始的地方加入use Time::Local; 就行了。 
#
#   最后，要注意的是：该程序是在命令行方式下执行的，即：perl ys2leobbs_thread.cgi
#   如果论坛数据量大可能时间会长一点，不过转换过程中有提示转换多少的。
#

use Time::Local;
require "config.pl";

	$key_input="5";
	my $transdir="$filehead"."trans";
	my $filedata="$filehead$key_input/";
	my $maxsavepost=14;
	
	mkdir("$transdir",0777);
	mkdir("$transdir/$key_input",0777);

	dbmopen(%USERFILE,"$filedata$userfile",0666);
       	%TEMP=%USERFILE;      
   	dbmclose(%USERFILE);
	@wennototal=keys %TEMP;
	@wennototal=sort @wennototal;
	$wennototal=$#wennototal+1;

	foreach $usernotemp(@wennototal){
		($marktemp,$usernametemp,$useremailtemp,$userurltemp,$usertitletemp,$emailtruetemp,$userpasstemp,$userclicktemp,$usernumberstemp,$userhometemp,$vtemp,$datentimentemp,$markendtemp,$lasttemp)=split(/‖/,$TEMP{$usernotemp});
#		print "-$marktemp-$usernametemp--$usertitletemp-$markendtemp-\n";
		if (($marktemp eq "start") && ($markendtemp eq "end")) {
			if ($userhometemp==0){
				push(@usernotmp,$usernotemp);
			}
		}
	}
	@usernotmp=sort @usernotmp;
	$usertotalall=$#usernotmp+1;

   	$wennowno=0; $wentotal=0;
	foreach $userno(@usernotmp) {
		$plfilename="${wennowno}.pl"; $cgifilename="${wennowno}.thd.cgi";
		$wennowno +=1;
		$theplfile=""; $thecgifile="";
   		if ($TEMP{$userno}) {
   	   		($mark,$username,$useremail,$userurl,$usertitle,$emailtrue,$userpass,$userclick,$usernumbers,$userhome,$v,$datentimen,$markend,$last)=split(/‖/,$TEMP{$userno});
      			if (($mark eq "start") && ($markend eq "end")) {
       			} 
   		}
   		
   		open (FILE, "$filedata$userno");
		$userinfo=<FILE>;
		close (FILE);
		$wentotal++;
		$ttime=t2t($datentimen);
		$thecgifile="$username\t$usertitle\t\tyes\tyes\t$ttime\t$userinfo\t\t\n";
	
		@usernototal=keys %TEMP;
		@usernototal=sort @usernototal;
		$usernototal=$#usernototal+1;
		foreach $userno1(@usernototal){
			($mark,$username1,$useremail1,$userurl1,$usertitle1,$emailtrue1,$userpass1,$userclick1,$usernumbers1,$userhome1,$vv,$datentimen1,$markend,$last)=split(/‖/,$TEMP{$userno1});
			if (($mark eq "start") && ($markend eq "end")) {
				if (($usernumbers1 == $usernumbers)&&($userhome1 !=0 )){
					push(@list5,$userno1);
				}
			}
				}
		@list5=sort @list5;
		$no1=@list5;
	######################################################################
		foreach $userno2(@list5){
			if ($TEMP{$userno2}) {
                		($mark,$username2,$useremail2,$userurl2,$usertitle2,$emailtrue2,$userpass2,$userclick2,$usernumbers2,$userhome2,$vvv,$datentimen2,$markend,$last)=split(/‖/,$TEMP{$userno2});
                		open (FILE, "${filedata}${userno2}");
				my $userinfo2=<FILE>;
				close (FILE);
				$wentotal++;
				my $ttime2=t2t($datentimen2);
				$thecgifile .="$username2\t$usertitle\t\tyes\tyes\t$ttime2\t$userinfo2\t\t\n";
			}
		}
		undef(@list5);
		my $theinfo=weninfo($userinfo2);
		$theplfile="$wennowno\t$usertitle\t\topen\t$no1\t$userclick\t$username\t$ttime\t$username2\t$ttime2\t$theinfo\t";

#		print "$transdir/$key_input/${wennowno}.pl---$theplfile--\n";
		open(FILE,">$transdir/$key_input/${wennowno}.pl");
		print FILE $theplfile;
		close FILE;

		open(FILE,">$transdir/$key_input/${wennowno}.thd.cgi");
		print FILE $thecgifile;
		close FILE;
		
		print "已转换 $wennowno 个主题\n";
	}
	print "转换专栏 $key_input 结束.\n";
	print "应转换 $wennowno 个主题，实际转换 $usertotalall 个主题.\n";
	print "应转换 $wennototal 篇文章，实际转换 $wentotal 篇文章.\n";
	print "请到 $transdir/$key_input 目录里查看转换是否正确。\n";
sub t2t{
#转换之前的日期格式为2001/04/28(13:04:04)，
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