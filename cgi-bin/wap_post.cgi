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
$LBCGI::POST_MAX = 2000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "bbs.lib.pl";
require "wap.pl";
require "data/styles.cgi";
$|++;
&waptitle;
$show.= qq~<card  title="$boardname-发表主题">~;
$lid = $query -> param('lid');
&check($lid);
$inforum        = $query -> param('f');
$intopictitle        = $query -> param('title');
if ($inmembername eq "" || $inmembername eq "客人" ) {
    $inmembername = "客人";
} else {
    &getmember("$inmembername");
}   
if (-e "${lbdir}data/style${inforum}.cgi") { require "${lbdir}data/style${inforum}.cgi"; }           
$inpost        = $query -> param('inpost');
$inpost=$uref->fromUTF8("gb2312",$inpost);
$intopictitle=$uref->fromUTF8("gb2312",$intopictitle);
$inpost = &cleaninput("$inpost");
$intopictitle = &cleaninput("$intopictitle");
$currenttime   = time;
$postipaddress = &myip();
$inpost        =~ s/LBHIDDEN/LBHIDD\&\#069\;N/sg;
$inpost        =~ s/\[br\]/<br>/g;
$inpost        =~ s/LBSALE/LBSAL\&\#069\;/sg;
$inpost        =~ s/USECHGFONTE/USECHGFONT\&\#069\;/sg;
$inpost        =~ s/\[DISABLELBCODE\]/\[DISABLELBCOD\&\#069\;\]/sg;
$inpost        =~ s/\[POSTISDELETE=(.+?)\]/\[POSTISDELET\&\#069\;=$1\]/sg;
$inpost        =~ s/\[ADMINOPE=(.+?)\]/\[ADMINOP\&\#069\;=$1\]/sg;
&moderator("$inforum");
$myinmembmod = $inmembmod;
if ($allowusers ne ''){
    &errorout('进入论坛&你不允许进入该论坛！') if (",$allowusers," !~ /,$inmembername,/i && $membercode ne 'ad');
}
if ($membercode ne 'ad' && $membercode ne 'smo' && $inmembmod ne 'yes') {
    &errorout("进入论坛&你不允许进入该论坛，你的威望为 $rating，而本论坛只有威望大于等于 $enterminweiwang 的才能进入！") if ($enterminweiwang > 0 && $rating < $enterminweiwang);
    if ($enterminmony > 0 || $enterminjf > 0 ) {
	require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
	$mymoney1 = $numberofposts * $addmoney + $numberofreplys * $replymoney + $visitno * $loginmoney + $mymoney - $postdel * $delmoney + $jhcount * $addjhhb;
	&errorout("进入论坛&你不允许进入该论坛，你的金钱为 $mymoney1，而本论坛只有金钱大于等于 $enterminmony 的才能进入！") if ($enterminmony > 0 && $mymoney1 < $enterminmony);
	&errorout("进入论坛&你不允许进入该论坛，你的积分为 $jifen，而本论坛只有积分大于等于 $enterminjf 的才能进入！") if ($enterminjf > 0 && $jifen < $enterminjf);
    }
}
if ($startnewthreads eq "onlysub") {&errorout("发表&对不起，这里是纯子论坛区，不允许发言！"); }

    if (($floodcontrol eq "on") && ($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'amo') && ($membercode ne 'cmo') && ($membercode ne "mo") && ($inmembmod ne "yes")) {
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = $lastpost + $floodcontrollimit;
	if ($lastpost > $currenttime)  {
	    my $lastpost1 = $lastpost - $currenttime;
	    &errorout("发表新主题&灌水预防机制已经使用，您必须再等待 $lastpost1 秒钟才能再次发表！");
	}
    }
    if ($postopen eq "no") { &errorout("发表或回复主题&对不起，本论坛不允许发表或回复主题！"); }
    if (($userregistered eq "no")&&(length($inmembername) > 12)) { &errorout("发表新主题&您输入的用户名太长，请控制在6个汉字内！");   }
    if (($userregistered eq "no")&&($inmembername =~ /^客人/)) { &errorout("发表新主题&请不要在用户名的开头中使用客人字样！");   }
    if ($inmembername eq "客人") { &errorout("发表新主题&请不要在用户名的开头中使用客人字样！");   }
    if (($userregistered eq "no")&&($startnewthreads ne "all")) { &errorout("发表新主题&您没有注册！");   }
   # elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &errorout("发表新主题&您的密码错误！"); }
    elsif (($membercode eq "banned")||($membercode eq "masked"))      { &errorout("添加回复&您被禁止发言或者发言被屏蔽，请联系管理员解决！"); }
    elsif ($intopictitle eq "＊＃！＆＊") { &errorout("发表新主题&必须输入主题标题！"); }
    elsif (length($intopictitle) > 92)   { &errorout("发表新主题&主题标题过长！"); }
    else  {
	$intopictitle =~ s/\(无内容\)$//;
	if (($inpost eq "")&&($addme eq "")) { $intopictitle.=" (无内容)"; }}
        $intopictitle =~ s/()+//isg;
	my $tempintopictitle = $intopictitle;
	$tempintopictitle =~ s/ //g;
	$tempintopictitle =~ s/\&nbsp\;//g;
        $tempintopictitle =~ s/　//isg;
        $tempintopictitle =~ s///isg;
        $tempintopictitle =~ s/^＊＃！＆＊//;
	if ($tempintopictitle eq "") { &errorout("发表新主题&主题标题有问题！"); }

        $tempaccess = "forumsallowed". "$inforum";
        $testentry = $query->cookie("$tempaccess");
        if (($allowedentry{$inforum} eq "yes")||(($testentry eq $forumpass)&&($testentry ne ""))||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
        if (($privateforum eq "yes") && ($allowed ne "yes")) { &errorout("发表&对不起，您不允许在此论坛发表！"); }

	if ($startnewthreads eq "no") {
            unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes") { &errorout("发表新主题&在此论坛中只能由坛主或者本版版主发表新主题！"); }
	}
	elsif ($startnewthreads eq "cert") {
            unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes"||$membercode eq 'cmo'||$membercode eq 'mo'||$membercode eq 'amo'||$membercode =~ /^rz/) { &errorout("发表新主题&在此论坛中只能由坛主、版主和认证会员发表新主题！"); }
	}
	elsif (($startnewthreads eq "follow") &&($action eq "addnew")) {
            unless ($membercode eq "ad" ||$membercode eq 'smo'||$membercode eq 'cmo' ||$membercode eq 'mo'||$membercode eq 'amo'|| $inmembmod eq "yes") { &errorout("发表新主题&在此论坛中只能由坛主或者版主发表新主题！"); }
	}
	elsif (($startnewthreads eq "all")&&($userregistered eq "no")) { $inmembername = "$inmembername(客)"; }

	if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	    &errorout("发表新主题&对不起，你的删贴率超过了<b>$deletepercent</b>%，管理员不允许你发表新主题！请联系坛主解决！") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
	}
        $inpost =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;
        	$inpost ="<img src='$imagesurl/images/sj.gif' width='22' alt='由手机 WAP 发送' /> ".$inpost;
	undef $newthreadnumber;
	$filetoopen = "$lbdir" . "boarddata/lastnum$inforum.cgi";
	if (open(FILE, "$filetoopen")) {
	    $newthreadnumber = <FILE>;
            close(FILE);
            chomp $newthreadnumber;
	    $newthreadnumber ++;
	}
	
	if ((!(-e "${lbdir}forum$inforum/$newthreadnumber.pl"))&&($newthreadnumber =~ /^[0-9]+$/)) {
	    if (open(FILE, ">$filetoopen")) {
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE $newthreadnumber;
		close(FILE);
            }
	}
	else {
            opendir (DIR, "${lbdir}forum$inforum");
            my @dirdata = readdir(DIR);
            closedir (DIR);
            @dirdata = grep(/.thd.cgi$/,@dirdata);
            @dirdata = sort { $b <=> $a } (@dirdata);
            $highest = $dirdata[0];
            $highest =~ s/.thd.cgi$//;
            $newthreadnumber = $highest + 1;
            if (open(FILE, ">$filetoopen")) {
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE $newthreadnumber;
		close(FILE);
	    }
	}

	my $oldthreadnumber = $newthreadnumber - 1;
        if (open(FILE, "${lbdir}forum$inforum/$oldthreadnumber.thd.cgi")) {
            flock(FILE, 1) if ($OS_USED eq "Unix");
            my $threaddata =<FILE>;
            close(FILE);
            (my $amembername,my $atopictitle,my $no,my $no,my $no,my $no,my $apost,my $no) = split(/\t/, $threaddata);
	    if (($amembername eq $inmembername)&&((($apost eq $inpost)&&($apost ne "")&&($inpost ne ""))||($atopictitle eq $intopictitle))) {
	        if (open(FILE, ">${lbdir}boarddata/lastnum$inforum.cgi")) {
        	    flock(FILE, 2) if ($OS_USED eq "Unix");
        	    print FILE $oldthreadnumber;
        	    close(FILE);
        	}
	    	&errorout("发表新主题&请不要重复发帖子，已经存在与此帖子主题相同或者内容相同的而且是你发的帖子了！");
	    }
	}

	my $temp = &dofilter("$intopictitle\t$inpost");
	($intopictitle,$inpost) = split(/\t/,$temp);
	$intopictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
	$intopictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
	$intopictitle =~ s/(o|O)R/$1&#82;/sg;
	$intopictitle =~ s/(o|O)r/$1&#114;/sg;
	$intopictitle  =~ s/\\/&#92;/isg;
        $intopictitle =~ s/E/\&\#69\;/g;
        $intopictitle =~ s/e/\&\#101\;/g;
	
	$intopictitletemp = $intopictitle ;
	$intopictitletemp =~ s/^＊＃！＆＊//;


        if (open(FILE, ">${lbdir}forum$inforum/$newthreadnumber.pl")) {
            print FILE "$newthreadnumber\t$intopictitle\t\topen\t0\t0\t$inmembername\t$currenttime\t\t$currenttime\t$inposticon\t$inposttemp\t$addme\t";
            close(FILE);
        }

        if (open(FILE, ">${lbdir}forum$inforum/$newthreadnumber.thd.cgi")) {
            print FILE "$inmembername\t$intopictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t$inwater\t\n";
            close(FILE);
        }
        	if ($privateforum ne "yes") {
	    $filetomakeopen = "$lbdir" . "data/recentpost.cgi";
	    my $filetoopens = &lockfilename($filetomakeopen);
	    if (!(-e "$filetoopens.lck")) {
		if (-e $filetomakeopen) {
		    &winlock($filetomakeopen) if ($OS_USED eq "Nt");
		    open(FILE, "$filetomakeopen");
		    flock (FILE, 1) if ($OS_USED eq "Unix");
		    my @recentposts=<FILE>;
		    close(FILE);
		    my $checknumber = 0;
		    $maxadpost = 3 if ($maxadpost < 3);
		    if (($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/)) {
		        foreach (@recentposts) {
			    (my $no,$no,my $temptopic,$no,$no,my $tempmembername) = split(/\t/,$_);
			    $temptopic =~ s/^＊＃！＆＊//;
			    $checknumber ++ if (($intopictitletemp eq $temptopic)&&(lc($tempmembername) eq lc($inmembername)));
		        }

		        if ($checknumber >= $maxadpost) {
			    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
			    unlink ("${lbdir}forum$inforum/$newthreadnumber.pl");
			    unlink ("${lbdir}forum$inforum/$newthreadnumber.thd.cgi");
	                    unlink ("${imagesdir}$usrdir/$inforum/$inforum\_${newthreadnumber}.$up_ext");

			    if (($inmembername ne "")&&($userregistered ne "no")&&($password ne "")) {
			        $memberfiletitle = $inmembername;
			        $memberfiletitle =~ s/ /\_/isg;
			        $memberfiletitle =~ tr/A-Z/a-z/;
			        my $namenumber = &getnamenumber($memberfiletitle);
			        &checkmemfile($memberfiletitle,$namenumber);
			        if (open(MEMFILE, ">${lbdir}$memdir/$namenumber/$memberfiletitle.cgi")) {
			            print MEMFILE "$inmembername\t$password\t$membertitle\tmasked\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
			            close(MEMFILE);
			        }
		                unlink ("${lbdir}cache/myinfo/$memberfiletitle.pl");
		                unlink ("${lbdir}cache/meminfo/$memberfiletitle.pl");
			    }
		            $filetomake = "$lbdir" . "data/idbans.cgi";
		            open (FILE, ">>$filetomake");
        		    print FILE "$inmembername\t";
		            close (FILE);
			    &errorout("出错&由于你在多区发送广告，所以你已经被禁止发言！");
			}
		    }

		    $recentposts=@recentposts;
		    $maxpostreport = 31;
		    if ($recentposts<$maxpostreport) { $maxpostreport=$recentposts;} 
		    else { $maxpostreport--; }
		    if($maiweb_sl eq 'off'){
		    if (open (FILE, ">$filetomakeopen")) {
			flock (FILE, 2) if ($OS_USED eq "Unix");
			print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inposticon\t$inmembername\t\n";
			for ($i=0;$i<$maxpostreport;$i++) { print FILE $recentposts[$i]; }
			close(FILE);
		    }
		    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
		    }else{
		    $topictitle3=$intopictitletemp;
                    $topictitle3=~s/~/\.\./g;
                    $topictitle22=&lbhz("$topictitle3",30);
                        $postdate=$currenttime;
                        $postdate = &shortdate($postdate+$addtimes);
                    if (open (FILE, ">$filetomakeopen")) {
                    open(PSF2,">$lbdir/data/recentpost.pl");
                        print PSF2 "\$allnew=qq~";
                        flock (FILE, 2) if ($OS_USED eq "Unix");
                        print FILE "$inforum\t$newthreadnumber\t$topictitle3\t$postdate\t\t$inmembername\t$topictitle22\n";
                        print PSF2 "·<a href=topic.cgi?forum=$inforum&topic=$newthreadnumber title='$topictitle3\n作者：$inmembername\n时间：$postdate'>$topictitle22</a>";
                        for ($i=0;$i<9;$i++) { 
                        chomp $recentposts[$i];
                        if ($recentposts[$i] ne ''){
                        my ($d1,$d2,$d3,$d4,$no,$d5,$d6)=split(/\t/,$recentposts[$i]);
                        next if($d6 eq '');
                        print PSF2 "<br>·<a href=topic.cgi?forum=$d1&topic=$d2  title='$d3\n作者：$d5\n时间：$d4'>$d6</a>";
                        print FILE "$recentposts[$i]\n"; }}
                        print PSF2 "~;\n1;";
                        close(PSF2);
                        close(FILE);
                    }
                    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
		    }
		} else {
			if($maiweb_sl eq 'off'){
      		    if (open (FILE, ">$filetomakeopen")) {
      			print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inposticon\t$inmembername\t\n";
      			close(FILE);
      		    }
      		}else{
      		if (open (FILE, ">$filetomakeopen")) {
                          	  $topictitle3=$intopictitletemp;
                              $topictitle3=~s/~/\.\./g;
                               $topictitle22=&lbhz("$topictitle3",30);
                              $postdate=$currenttime;
                        		$postdate = &shortdate($postdate+$addtimes);
                              print FILE "$inforum\t$newthreadnumber\t$topictitle3\t$postdate\t$inposticon\t$inmembername\t$topictitle22\n";
                              close(FILE);
                          }
      		}
   		}
 	    }
	    else {
    		unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
	    }
	}
    my $nowtime = &shortdate($currenttime + $timezone*3600);

    my $filetoopens = "$lbdir/data/todaypost.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
    	&winlock("$lbdir/data/todaypost.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
        if (-e "$lbdir/data/todaypost.cgi") {
            open (FILE,"+<$lbdir/data/todaypost.cgi");
            $todaypost=<FILE>;
            chomp $todaypost;
            my ($nowtoday,$todaypostno,$maxday,$maxdaypost,$yestdaypost)=split(/\t/,$todaypost);
            if ($nowtoday eq $nowtime) {
            	$todaypostno ++;
            	if ($todaypostno > $maxdaypost) {
            	    $maxday     = $nowtime;
            	    $maxdaypost = $todaypostno;
            	}
            }
            else {
            	$nowtoday = $nowtime;
            	$yestdaypost = $todaypostno;
            	$todaypostno = 1;
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
            }
            seek(FILE,0,0);
            print FILE "$nowtoday\t$todaypostno\t$maxday\t$maxdaypost\t$yestdaypost\t";
            close (FILE);
        }
        else {
            open (FILE,">$lbdir/data/todaypost.cgi");
            print FILE "$nowtime\t1\t$nowtime\t1\t0\t";
            close (FILE);
        }
    	&winunlock("$lbdir/data/todaypost.cgi") if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
    }

        $file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
        flock (LIST, 2) if ($OS_USED eq "Unix");
 	sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;

    	if (length($listall) > 500) {
	    if (open (LIST, ">$file")) {
        	flock (LIST, 2) if ($OS_USED eq "Unix");
		print LIST "$newthreadnumber\n$listall";
		close (LIST);
	    }
            &winunlock($file) if ($OS_USED eq "Nt");
            if (open (LIST, ">>${lbdir}boarddata/listall$inforum.cgi")) {
                print LIST "$newthreadnumber\t$intopictitletemp\t$inmembername\t$currenttime\t\n";
            	close (LIST);
            }
	}
	else {
            &winunlock($file) if ($OS_USED eq "Nt");
	    require "rebuildlist.pl";
            my $truenumber = rebuildLIST(-Forum=>"$inforum");
            ($tpost,$treply) = split (/\|/,$truenumber);
	}

        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
	$cleanmembername =~ tr/A-Z/a-z/;

        $jifen = $numberofposts * 2 + $numberofposts - $postdel * 5 if ($jifen eq "");
        
        if ($forumallowcount ne "no") {
	    $numberofposts++;
	    $mymoney += $forumpostmoney - $addmoney if ($forumpostmoney ne "");
	    if ($forumpostjf ne "") { $jifen += $forumpostjf; } else { $jifen += $ttojf; }
	}
        $lastpostdate = "$currenttime\%\%\%topic.cgi?forum=$inforum&topic=$newthreadnumber\%\%\%$intopictitletemp" if ($privateforum ne "yes");
        chomp $lastpostdate;

    	if (($userregistered ne "no")&&($password ne "")) {
	    $filetomake = "$lbdir" . "$memdir/$cleanmembername.cgi";
            &winlock($filetomake) if ($OS_USED eq "Nt");
            if ((open(FILE, ">$filetomake"))&&($inmembername ne "")) {
        	flock(FILE, 2) if ($OS_USED eq "Unix");
        	print FILE "$membername\t$password\t$membertitle\t$membercode\t$numberofposts|$numberofreplys\t$emailaddress\t$showemail\t$ipaddress\t$homepage\t$oicqnumber\t$icqnumber\t$location\t$interests\t$joineddate\t$lastpostdate\t$signature\t$timedifference\t$privateforums\t$useravatar\t$userflag\t$userxz\t$usersx\t$personalavatar\t$personalwidth\t$personalheight\t$rating\t$lastgone\t$visitno\t$useradd04\t$useradd02\t$mymoney\t$postdel\t$sex\t$education\t$marry\t$work\t$born\t$chatlevel\t$chattime\t$jhmp\t$jhcount\t$ebankdata\t$onlinetime\t$userquestion\t$awards\t$jifen\t$userface\t$soccerdata\t$useradd5\t";
        	close(FILE);
            }
            &winunlock($filetomake) if ($OS_USED eq "Nt");
            unlink ("${lbdir}cache/myinfo/$cleanmembername.pl");
            if (((-M "${lbdir}cache/meminfo/$cleanmembername.pl") *86400 > 60*2)||(!(-e "${lbdir}cache/meminfo/$cleanmembername.pl"))) {
                require "getnameinfo.pl" if ($onloadinfopl ne 1);
                &getmemberinfo($cleanmembername);
            }
	}

	$filetoopen = "${lbdir}boarddata/foruminfo$inforum.cgi";
	my $filetoopens = &lockfilename($filetoopen);
	if (!(-e "$filetoopens.lck")) {
            &winlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
            open(FILE, "+<$filetoopen");
            ($no, $threads, $posts, $todayforumpost, $lastposter) = split(/\t/,<FILE>);

            $lastposter   = $inmembername;
            $lastposttime = $currenttime;
            if (($tpost ne "")&&($treply ne "")) {
                $threads = $tpost;
                $posts   = $treply;
            } else { $threads++; }
	    my ($todayforumpost, $todayforumposttime) = split(/\|/,$todayforumpost);
	    if (($nowtime ne $todayforumposttime)||($todayforumpost eq "")) { $todayforumpost = 1; } else { $todayforumpost++; }
            $todayforumpost = "$todayforumpost|$nowtime";
            $lastposttime = "$lastposttime\%\%\%$newthreadnumber\%\%\%$intopictitletemp";
	    seek(FILE,0,0);
            print FILE "$lastposttime\t$threads\t$posts\t$todayforumpost\t$lastposter\t\n";
            close(FILE);

	    $posts = 0 if ($posts eq "");$threads = 0 if ($threads eq "");
	    open(FILE, ">${lbdir}boarddata/forumposts$inforum.pl");
	    print FILE "\$threads = $threads;\n\$posts = $posts;\n\$todayforumpost = \"$todayforumpost\";\n1;\n";
            close(FILE);
            &winunlock($filetoopen) if ($OS_USED eq "Nt" || $OS_USED eq "Unix");
}
        else {
    	    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
	}
	
        require "$lbdir" . "data/boardstats.cgi";
        $filetomake = "$lbdir" . "data/boardstats.cgi";
        my $filetoopens = &lockfilename($filetomake);
	if (!(-e "$filetoopens.lck")) {
	    $totalthreads++;
	    &winlock($filetomake) if ($OS_USED eq "Nt");
	    if (open(FILE, ">$filetomake")) {
		flock(FILE, 2) if ($OS_USED eq "Unix");
		print FILE "\$lastregisteredmember = \'$lastregisteredmember\'\;\n";
		print FILE "\$totalmembers = \'$totalmembers\'\;\n";
		print FILE "\$totalthreads = \'$totalthreads\'\;\n";
		print FILE "\$totalposts = \'$totalposts\'\;\n";
		print FILE "\n1\;";
		close (FILE);
	    }
            &winunlock($filetomake) if ($OS_USED eq "Nt");
	}
    	else {
    	    unlink ("$filetoopens.lck") if ((-M "$filetoopens.lck") *86400 > 30);
    	}
    	
opendir (CATDIR, "${lbdir}cache");
my @dirdata = readdir(CATDIR);
closedir (CATDIR);
unlink ("${lbdir}cache/plcache$inforum\_0.pl");
    $show.= qq~<p>新主题发表成功..<br/><a href="wap_forum.cgi?forum=$inforum&amp;lid=$lid&amp;paGe=$pa">返回列表..</a></p><p><a href="wap_topic.cgi?f=$inforum&amp;lid=$lid&amp;t=$newthreadnumber">返回帖子..</a></p>~;
&wapfoot;