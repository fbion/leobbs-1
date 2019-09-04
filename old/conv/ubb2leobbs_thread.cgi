#!/usr/bin/perl
###############################################
#  Ubb X.XX => LeoBBS 贴子转化
###############################################
#使用帮助：
#
#设置$ubbnoncgi目录为ubb的noncgi目录
#
#设置$leobbspath目录为LeoBBS的cgi-bin目录
#
#设置["$ubbnoncgi/Forum4","4"],修改前面的Forum4
#中的4是你要转化的ubb论坛目录id,后面的4是LeoBBS
#的论坛id，要转化多个论坛，请用多行，别忘记后
#面的逗号
#
#设置$truetime是否采用time模块，有些机器不支持，
#如果不支持选0, 但是所有发贴和回复时间为当前时间，
#支持选1，可以自己测试
#
###############################################
use CGI qw(:standard);
$CGI::POST_MAX=1024;
$CGI::DISABLE_UPLOADS = 1;
$CGI::HEADERS_ONCE = 1;
use Time::Local;

$ubbnoncgi ='/home/public_html/non'; #UBB 目录，最后不要遗漏 / 
$leobbspath='/home/cgi-bin/leobbs';  #LeoBBS 主目录，最后不要遗漏 / ，注意设置 777 属性

$convertdata=
[
	["$ubbnoncgi/Forum12","1"],
	["$ubbnoncgi/Forum13","2"],
	["$ubbnoncgi/Forum4","3"],
	["$ubbnoncgi/Forum9","4"],
	["$ubbnoncgi/Forum10","5"],
	["$ubbnoncgi/Forum11","6"],
	["$ubbnoncgi/Forum5","7"],
	["$ubbnoncgi/Forum6","8"],
	["$ubbnoncgi/Forum7","9"],
	["$ubbnoncgi/Forum8","10"],
	["$ubbnoncgi/Forum1","11"],
	["$ubbnoncgi/Forum2","12"]
	
	
];
 

###每100个打印一个信息
$hz=100;
$truetime=1;#设置是否采用time模块，我发现有些机器不支持，如果不支持选0, 但是所有发贴和回复时间为当前时间

print "Content-type: text/html\n\n";

print "转化开始 ",time(),"<br><br><hr>\n\n";


foreach $tempturn (@$convertdata)
{
	$oldforumpost=$tempturn->[0];
	$newboardid=$tempturn->[1];
	print "old:$oldforumpost  new:$newboardid\n<br>";	
		
	opendir(CURDIR,$oldforumpost) || die "forum path read error";
	@postfiles=readdir(CURDIR);
	close(CURDIR);
	
	mkdir("$leobbspath/forum$newboardid",0777);
	
	$i=0;
	
	print "转化 $oldforumpost 到 $newboardid 开始 " ,time()," <br><br>","\n";
	$count=0;
	foreach $temp(@postfiles)
	{
		
		if($temp=~/(\d{6})\.cgi/)
		{	
			
			$id=$1;
			$count++; 
			open(TEMPF,"$oldforumpost/$temp");		
			@filelines=<TEMPF>;
			close(TEMPF);
			
			
			$startline=$filelines[0];
			if($startline=~/^A/)
			{			
				
				###table ut_topics
				### id  subject boardId top locked lockMoveTitle lockMoveText 
				### PostNum lastPostTime lastPostName lastPostId
				
				###第一行:A||帖子状态||回复总数||用户名||主题||归档的信息||表情图||注释(例如被转移)
				###下面:  Z||回复编号||回复用户名||回复日期||回复时间||邮件||回复信息||IP地址||是否注册||表情图标
				($subject,$locked)=('','open');
				
					
				@startlines=split(/\|\|/,$startline);
				$subject=$startlines[4];
				$locked="closed" if($startlines[1]=~/X/);
				$PostNum=$startlines[2]||1;
				$postname=$startlines[3];
				
				$lastline=$filelines[1];
				
				@lastlines=split(/\|\|/,$lastline);
				$posttime=&get_time($lastlines[3],$lastlines[4]);
				
				$tempcount=@filelines;
				$lastline=$filelines[$tempcount-1];
				@lastlines=split(/\|\|/,$lastline);
				$lastPostTime=&get_time($lastlines[3],$lastlines[4]);
				
				$lastPostName=$lastlines[2];
				
				
				
				open(TEMPT,">$leobbspath/forum$newboardid/$count.pl");		
				print TEMPT "$count\t$subject\t\t$locked\t$PostNum\t0\t$postname\t$posttime\t$lastPostName\t$lastPostTime\t\n";
				close(TEMPT);
				
				
				
				### table ut_posts
				###id userId userNameBak postSubject boardid topicId parentId 
				###ip postTime &&body&& 
				###下面:  Z||回复编号||回复用户名||回复日期||回复时间||邮件||回复信息||IP地址||是否注册||表情图标
				#               1           2         3        4        5        6       7        8         9
				open(TEMPT,">$leobbspath/forum$newboardid/$count.thd.cgi");
				foreach $eachline (@filelines)
				{
					if($eachline=~/^Z/){
					
					@eachlines=split(/\|\|/,$eachline);
					
					
					$userNameBak=$eachlines[2];
					$ip=$eachlines[7];
					$postTime=&get_time($eachlines[3],$eachlines[4]);
					
					$body=$eachlines[6];			
					$body=$body;
								
				print TEMPT "$userNameBak\t$subject\t$ip=\tyes\tyes\t$postTime\t$body\t\t\n";
				}
									
				}
				close(TEMPT);	
				
			}
			$i++;
			if(($i/$hz)==0)	{print "现在转化 $i 结束,开始新的转化 ...\n<br>";}
		}
	}
	
	
	print "总共 $i 个贴子,转化完成 ",time(),"<br><hr>\n\n";

}



print "转化全部完成 ",time(),"\n<br>";


exit;

#=====================================

sub  get_time
{
	
	($datestr,$timestr)=@_;
	
	($month,$day,$year)=split(/\-/,$datestr);
	($temp,$ampm)=split(/\s/,$timestr);
	($hour,$minute)=split(/\:/,$temp);
	$month=&getridzero($month);
	$day=&getridzero($day);
	$hour=&getridzero($hour);
	$minute=&getridzero($minute);
	$ss=0;
		
		
	###$year=int($year)-1900;
    	if ($truetime ==1){
    	$time = timelocal($ss,$minute,$hour,$day,$month-1,$year);
    	}else{
    	$time=time();
    	}
    	
    	return($time);	
    	
}

sub getridzero
{
	
    $str=shift;
    $str=~s/^0//;
    return($str);    
}






sub htmlhead
{
   if (!$htmlhead)
   {
      print "Content-type: text/html\n\n";
   }
   $htmlhead = 1;
}


1;

