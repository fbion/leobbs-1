#####################################################
#  LEO SuperCool BBS / LeoBBS X / 雷傲极酷超级论坛  #
#####################################################
# 基于山鹰(糊)、花无缺制作的 LB5000 XP 2.30 免费版  #
#   新版程序制作 & 版权所有: 雷傲科技 (C)(R)2004    #
#####################################################
#      主页地址： http://www.LeoBBS.com/            #
#      论坛地址： http://bbs.LeoBBS.com/            #
#####################################################

    if ($startnewthreads eq "onlysub") {&error("发表&对不起，这里是纯子论坛区，不允许发言！"); }
    if (($floodcontrol eq "on") && ($membercode ne "ad") && ($membercode ne 'smo') && ($membercode ne 'amo') && ($membercode ne 'cmo') && ($membercode ne "amo") && ($membercode ne "mo") && ($inmembmod ne "yes")) {
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = $lastpost + $floodcontrollimit;
	if ($lastpost > $currenttime)  {
	    my $lastpost1 = $lastpost - $currenttime;
	    &error("发表回复&灌水预防机制已经使用，您必须再等待 $lastpost1 秒钟才能再次发表！");
	}
    }
    if (($inhiddentopic eq "yes") && ($moneyhidden eq "yes")) { &error("发表回复&请不要在一个帖子内同时使用威望和金钱加密！"); }
    if ((($inhiddentopic eq "yes")||($moneyhidden eq "yes")) && ($userregistered eq "no")) { &error("发表回复&未注册用户无权进行威望和金钱加密！"); }

    &error("发表或回复主题&对不起，本论坛不允许发表或回复超过 <B>$maxpoststr</B> 个字符的文章！") if ((length($inpost) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("发表或回复主题&对不起，本论坛不允许发表或回复少于 <B>$minpoststr</B> 个字符的文章！") if ((length($inpost) < $minpoststr)&&($minpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    if ($postopen eq "no") { &error("发表或回复主题&对不起，本论坛不允许发表或回复主题！"); }

    if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	&error("发表回复&对不起，你的删贴率超过了<b>$deletepercent</b>%，管理员不允许你发表回复！请联系坛主解决！") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
    }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") {
     	    &whosonline("$inmembername\t$forumname\tnone\t回复<a href=\"topic.cgi?forum=$inforum&topic=$intopic\"><b>$topictitle</b></a>\t") if ($topictitle ne "");
	}
	else {
            &whosonline("$inmembername\t$forumname(密)\tnone\t回复保密帖子\t");
	}
    }

    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     { $onlinetime = $onlinetime + $onlinetimeadd;  &error("回复主题&对不起，本论坛不允许在线时间少于 $onlinepost 秒的用户回复主题！你目前已经在线 $onlinetime 秒！<BR>如果在线时间统计不正确,请重新登陆论坛一次即可解决！"); }

    if (($userregistered eq "no")&&(length($inmembername) > 12)) { &error("发表新回复&您输入的用户名太长，请控制在6个汉字内！");   }
    if (($userregistered eq "no")&&($inmembername =~ /^客人/)) { &error("发表新回复&请不要在用户名的开头中使用客人字样！");   }
    if ($inmembername eq "客人") { &error("发表新回复&请不要在用户名的开头中使用客人字样！");   }
    if (($userregistered eq "no")&&($startnewthreads ne "all")) { &error("发表新回复&您没有注册！");   }
    elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &error("发表新回复&您的密码错误！"); }
    elsif (($membercode eq "banned")||($membercode eq "masked"))  { &error("发表&已被禁止发言或者发言被屏蔽，请联系管理员解决！"); }
    elsif ($inpost eq "")            { &error("发表新回复&必须输入内容！"); }
    else {
#	@allforums = @forums;

	if ($startnewthreads eq "no") {
            unless ($membercode eq "ad" || $membercode eq 'smo' || $inmembmod eq "yes") {&error("发表新回复&在此论坛中只能由坛主或者本版版主发表新回复！");}
        }
        elsif ($startnewthreads eq "cert"){
	    unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes"||$membercode eq 'cmo'||$membercode eq 'amo'||$membercode eq 'mo'||$membercode =~ /^rz/) { &error("发表新回复&在此论坛中只能由坛主、版主和认证会员发表新回复！"); }
	}
	$tempaccess = "forumsallowed". "$inforum";
	$testentry = $query->cookie("$tempaccess");

	if ((($testentry eq $forumpass)&&($testentry ne ""))||($allowedentry{$inforum} eq "yes")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes")) { $allowed = "yes"; }
        if (($privateforum eq "yes") && ($allowed ne "yes")) { &error("发表&对不起，您不允许在此论坛发表！"); }
 	if (($startnewthreads eq "all")&&($userregistered eq "no")) { $inmembername = "$inmembername(客)"; }

        $inpost =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;

        $filetoopen = "$lbdir" . "forum$inforum/$intopic.thd.cgi";
        if (-e $filetoopen) {
           &winlock($filetoopen) if ($OS_USED eq "Nt");
           open(FILE, "$filetoopen");
           flock(FILE, 1) if ($OS_USED eq "Unix");
	   sysread(FILE, $allmessages,(stat(FILE))[7]);
           close(FILE);
	   $allmessages =~ s/\r//isg;
           &winunlock($filetoopen) if ($OS_USED eq "Nt");
           @allmessages=split(/\n/,$allmessages);
        }
	else { unlink ("$lbdir" . "forum$inforum/$intopic.pl"); &error("回复&这个主题不存在！可能已经被删除！"); }

if ($floor ne "") {
unless ($floor=~ /^[0-9]+$/) {&error("引用回复出错&输入的引用回复楼层数字中含有非法字符！");} 
if ($floor <= 0){&error("引用回复出错&输入的引用回复楼层数字不能为零或负数！");}
if ($floor != int($floor)){&error("引用回复出错&输入的引用回复楼层数字不是整数");}
$kate=@allmessages;
if($floor>$kate){&error("引用回复出错&可能原因没有$floor这个楼层，你仔细看看是不是你填写的数字大了呢？或者如果你不想引用回复，请不要在表单里面填写数据");}
($membername2, undef, undef, undef, undef ,$postdate2, $post2, undef) = split(/\t/, $allmessages[$floor-1]);

   if  ($post2=~/LBHIDDEN\[(.*?)\]LBHIDDEN/sg){
	$post2="(保密帖子)";
   }
   if  ($post2=~/LBSALE\[(.*?)\]LBSALE/sg){
	$post2="(保密帖子)";
   }

    $post2 =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg;
    $post2 =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
    $post2 =~ s/\[hide\](.+?)\[\/hide\]//isg;
    $post2 =~ s/\[watermark\](.+?)\[\/watermark\]/\n\(水印部分不能引用\)\n/isg;
    $post2 =~ s/(\&\#35\;|#)Moderation Mode//isg;
    $post2 =~ s/\<p\>/\n\n/ig;
    $post2 =~ s/\<br\>/\n/ig;
    $post2 =~ s/ \&nbsp;/  /ig;
    $post2 =~ s/\[curl=\s*(http|https|ftp):\/\/(.*?)\s*\]/\[加密连结\]/isg if ($usecurl ne "no");
    $post2 =~ s/\[DISABLELBCODE\]//isg;
    $post2 =~ s/\[ADMINOPE=(.+?)\]//isg;
    $post2 =~ s/ \n/\n/isg;
    $post2 =~ s/　\n/\n/isg;
    if ($post2 =~ /\[POSTISDELETE=(.+?)\]/) {
    	if ($1 ne " ") { $presult = "屏蔽理由：$1"; } else { $presult = "<BR>"; }
        $post2 = "此帖子内容已经被单独屏蔽！$presult";
    }

   $membernametemp2=$membername2;

   $postdate2 = $postdate2 + ($timedifferencevalue + $timezone)*3600;
   $postdate2 = &dateformat("$postdate2");
   $rawpost = $post2;

    $rawpost =~ s/\[这个(.+?)最后由(.+?)编辑\]\n//isg;
    $rawpost =~ s/LBHIDDEN\[(.*?)\]LBHIDDEN//sg;
    $rawpost =~ s/LBSALE\[(.*?)\]LBSALE//sg;
    $rawpost =~ s/\[quote\](.*)\[quote\](.*)\[\/quote](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[quote\](.*)\[\/quote\]//isg;
    $rawpost =~ s/\[equote\](.*)\[\/equote\]//isg;
    $rawpost =~ s/\[fquote\](.*)\[\/fquote\]//isg;
    $rawpost =~ s/\[hide\](.*)\[hide\](.*)\[\/hide](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[hide\](.*)\[\/hide\]//isg; 
    $rawpost =~ s/\[jf=(.+?)\](.+?)\[\/jf\]//isg;
    $rawpost =~ s/\[jf=(.+?)\](.+?)\[\/jf\](.*)\[jf=(.+?)\](.+?)\[\/jf\]//isg; 
    $rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\](.*)\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[post=(.+?)\](.+?)\[\/post\]//isg; 
    $rawpost =~ s/\[\s*(.*?)\s*\]\s*(.*?)\s*\[\s*(.*?)\s*\]/$2/isg;
    $rawpost =~ s/\:.{0,20}\://isg;
    $rawpost =~ s/\<img\s*(.*?)\s*\>//isg;
    $rawpost =~ s/(http|https|ftp):\/\/(.*?)\.(png|jpg|jpeg|bmp|gif|swf)/($2\.$3)/isg;
    $rawpost =~ s/\&nbsp;/ /ig;
    $rawpost =~ s/( )+$//isg;
    $rawpost =~ s/^( )+//isg;
    $rawpost =~ s/\[.+?\]//g;
    $rawpost =~ s/(\n)+/\n/isg;
    $rawpost =~ s/ \n/\n/isg;
    $rawpost =~ s/　\n/\n/isg;
    $rawpost =~ s/\n\n/\n/isg;
    $rawpost =~ s/^\n//isg;
    $rawpost =~ s/\n$//isg;
    $rawpost =~ s/\n/<BR>/isg;
    chomp $rawpost;

   my @postall = split(/\n/,$rawpost);
   my $postall = @postall;
   if ($postall > 4) { $rawpost = "$postall[0]\n$postall[1]\n$postall[2]\n$postall[3]\n..."; }
   $rawpost = &lbhz($rawpost,200);

   $inpost = qq~\[quote\]\[b\]下面引用由\[u\]$membernametemp2\[\/u\]在 \[i\]$postdate2\[\/i\] 发表的内容：\[\/b\]<br>$rawpost<br>\[\/quote\]<br>$inpost~;
}

        my $file = "$lbdir" . "forum$inforum/$intopic.pl";
        &winlock($file) if ($OS_USED eq "Nt");
        open (ENT, $file);
        flock(ENT, 2) if ($OS_USED eq "Unix");
        $in = <ENT>;
        close (ENT);
	&winunlock($file) if ($OS_USED eq "Nt");
        ($topicid, $topictitle, $topicdescription, $threadstate, $threadposts ,$threadviews, $startedby, $startedpostdate, $lastposter, $lastpostdate, $posticon, my $no, $addmetype) = split(/\t/,$in);
        if (($threadstate eq "closed")||($threadstate eq "pollclosed")) { &error("发表回复&对不起，这个主题已经被锁定！"); }
        $numberofitems = $threadposts+ 1; 
	if (($rdays ne '')&&($membercode ne "ad")&&($membercode ne "smo")) { &error("发表回复&超过 $rdays 天的帖子不允许再回复！") if ($currenttime - $lastpostdate > $rdays * 86400); }

        $inpost = &dofilter("$inpost");

        if ($emote && $inpost =~ m/\/\/\//) {
	    study ($inpost);
 	    my @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		my ($toemote, $beemote) = split(/=/,$_);
		chomp $beemote;
		$beemote =~ s/对象/〖$inmembername〗/isg;
		$inpost =~ s/$toemote/$beemote/isg;
		last unless ($inpost =~ m/\/\/\//);
	    }
	}

        ($trash, $topictitle, $trash, $trash, $trash, $trash, $post, $trash,my $water) = split(/\t/,$allmessages[0]);

	if (($nowater eq "on")&&($water eq "no")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'amo')&&($membercode ne 'cmo')&&($membercode ne 'mo')&&($inmembmod ne "yes")) {
	    my $inposttemp = $inpost;
	    $inposttemp =~ s/\[这个(.+?)最后由(.+?)编辑\]\<BR\>\<BR\>//isg;
	    $inposttemp =~ s/\[这个(.+?)最后由(.+?)编辑\]\<BR\>//isg;
	    $inposttemp =~ s/\[这个(.+?)最后由(.+?)编辑\]//isg;
	    $inposttemp =~ s/\[quote\]\[b\]下面引用由\[u\].+?\[\/u\]在 \[i\].+?\[\/i\] 发表的内容：\[\/b\].+?\[\/quote\]\<br\>//isg;
	    $inposttemp =~ s/\[quote\]\[b\]下面引用由\[u\].+?\[\/u\]在 \[i\].+?\[\/i\] 发表的内容：\[\/b\].+?\[\/quote\]//isg;
	    if ((length($inposttemp) < $gsnum)&&($gsnum > 0)) {
	        &error("发表回复&请不要灌水，本主题禁止 $gsnum 字节以下的灌水！");
	    }
	}

	$inpost =~ s/\[UploadFile.{0,6}=(.+?)\]//isg unless (($allowattachment ne "no")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"));

        $addme= &upfileonpost(\$inpost,$inforum,$intopic);#处理上传，返回数值给BT区做判断
#	&error("发表新主题&此区新主题必须带附件，请返回重试！") if (($addme eq "0")&&($mastpostatt eq "yes")&&($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"));

        if ($moneyhidden eq "yes") { $inposttemp = "(保密)"; $inpost="LBSALE[$moneypost]LBSALE".$inpost;}

	if ($inhiddentopic eq "yes") { $inposttemp = "(保密)"; $inpost="LBHIDDEN[$postweiwang]LBHIDDEN".$inpost; }

	if ($inposttemp ne "(保密)") {
	    $inposttemp = $inpost;
	    $inposttemp = &temppost($inposttemp);
            chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp,50);
	}
	$lastreplymessgae = $allmessages[-1];
        (my $ainmembername,my $no,my $no,my $no,my $no,my $no,my $ainpost,my $no) = split(/\t/,$lastreplymessgae);
 	if (($inmembername eq $ainmembername)&&($inpost eq $ainpost)) {
    	    &error("发表回复&请不要重复回复，已经存在与此回复内容相同的而且是你发的回复了！");
	}

        &winlock($filetoopen) if ($OS_USED eq "Nt");
        if (open(FILE, ">>$filetoopen")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$inmembername\t$topictitle\t$postipaddress\t$inshowemoticons\t$inshowsignature\t$currenttime\t$inpost\t$inposticon\t\n";
            close(FILE);
        }
        &winunlock($filetoopen) if ($OS_USED eq "Nt");

        $threadposts = @allmessages;
        $threadviews = $threadposts if ($threadviews < $threadposts);
#	$threadviews = 9999 if ($threadviews > 10000);

        my $topictitletemp = $topictitle;
        $topictitletemp =~ s/^＊＃！＆＊//;
        &winlock($file) if ($OS_USED eq "Nt");
        if (open(FILE, ">$file")) {
            flock(FILE, 2) if ($OS_USED eq "Unix");
            print FILE "$intopic\t＊＃！＆＊$topictitletemp\t$topicdescription\t$threadstate\t$threadposts\t$threadviews\t$startedby\t$startedpostdate\t$inmembername\t$currenttime\t$posticon\t$inposttemp\t$addmetype\t";
        close(FILE);
        }
        &winunlock($file) if ($OS_USED eq "Nt");
        
	$file = "$lbdir" . "boarddata/listno$inforum.cgi";
        &winlock($file) if ($OS_USED eq "Nt");
        open (LIST, "$file");
        flock (LIST, 2) if ($OS_USED eq "Unix");
	sysread(LIST, $listall,(stat(LIST))[7]);
        close (LIST);
	$listall =~ s/\r//isg;
        $listall =~ s/(.*)(^|\n)$intopic\n(.*)/$1$2$3/;
        
	if (length($listall) > 500) {
	    if (open (LIST, ">$file")) {
        	flock (LIST, 2) if ($OS_USED eq "Unix");
        	print LIST "$intopic\n$listall";
        	close (LIST);
            }
            &winunlock($file) if ($OS_USED eq "Nt");
    	} else {
            &winunlock($file) if ($OS_USED eq "Nt");
	    require "rebuildlist.pl";
            my $truenumber = rebuildLIST(-Forum=>"$inforum");
            ($tpost,$treply) = split (/\|/,$truenumber);
	}

        $cleanmembername = $inmembername;
        $cleanmembername =~ s/ /\_/isg;
	$cleanmembername =~ tr/A-Z/a-z/;

      $maxpersontopic = 25;
      if ($maxpersontopic && $userregistered ne "no") {
              $cleanstart = $startedby;
              $cleanstart =~ s/ /\_/isg;
              $cleanstart =~ tr/A-Z/a-z/;
              &addmytopic("reply", $cleanmembername, $inforum, $intopic, $topictitletemp, $currenttime, $posticon);
              &addmytopic("post", $cleanstart, $inforum, $intopic, $topictitletemp, $currenttime, $posticon) if ($cleanmembername ne $cleanstart);
      }

	if ($jifen eq "") {
		require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
		$jifen = $numberofposts * $ttojf + $numberofreplys * $rtojf - $postdel * $deltojf;
  }

      if ($forumallowcount ne "no") {
	  $numberofreplys++;
	  $mymoney += $forumreplymoney - $replymoney if ($forumreplymoney ne "");
          if ($forumreplyjf ne "") { $jifen += $forumreplyjf; } else { $jifen += $rtojf; }
      }
        $lastpostdate = "$currenttime\%\%\%topic.cgi?forum=$inforum&topic=$intopic\%\%\%$topictitletemp" if ($privateforum ne "yes");
        chomp $lastpostdate;

    if (($userregistered ne "no")&&($password ne "")) {
	my $namenumber = &getnamenumber($cleanmembername);
	&checkmemfile($cleanmembername,$namenumber);
        $filetomake = "$lbdir" . "$memdir/$namenumber/$cleanmembername.cgi";
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
    
    my $nowtime = &shortdate($currenttime + $timezone*3600);

    my $filetoopens = "$lbdir/data/todaypost.cgi";
    $filetoopens = &lockfilename($filetoopens);

    if (($usetodaypostreply ne "no")&&(!(-e "$filetoopens.lck"))) {
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
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
            	$nowtoday = $nowtime;
            	$yestdaypost = $todaypostno;
            	$todaypostno = 1;
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
            } else { $posts++; }
            if ($usetodayforumreply eq "yes") {
		($todayforumpost, $todayforumposttime) = split(/\|/,$todayforumpost);
		if (($nowtime ne $todayforumposttime)||($todayforumpost eq "")) { $todayforumpost = 1; } else { $todayforumpost++; }
                $todayforumpost = "$todayforumpost|$nowtime";
            }
            $lastposttime = "$lastposttime\%\%\%$intopic\%\%\%$topictitletemp";
	    
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
        $totalposts++;
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

    if ($emailfunctions eq "on") {
	eval("use MAILPROG qw(sendmail);");
	$filetoopen = "$lbdir" . "forum$inforum/$intopic.mal.pl";
	open (FILE, "$filetoopen");
	my @maildata = <FILE>;
	close (FILE);

	$mailall = "$inmembername\t$emailaddress\t";
	if ($innotify eq "yes") {
	    if (open (FILE, ">$filetoopen")) {
                print FILE "$mailall\n";
                foreach (@maildata) {
                    chomp $_;
                    print FILE "$_\n" if ($mailall ne $line);
                }
                close (FILE);
	    }
	}
	$toemail = '';
	foreach (@maildata) {
	    chomp $_;
	    ($postersname,$posteremailaddress) = split(/\t/,$_);
            if ($lastemailsent ne $postersname) {
                if ($inmembername eq $postersname) { next; }
                next if ($posteremailaddress eq "");
        	$posteremailaddress =~ s/[\a\f\n\e\0\r\t\`\~\!\$\%\^\&\*\(\)\=\+\\\{\}\;\'\:\"\,\/\<\>\?\|]//isg;
        	next if ($posteremailaddress !~ /^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/);
            	if ($toemail eq "") {$toemail = $posteremailaddress;} else {$toemail .= ", $posteremailaddress";}
                $lastemailsent = $postersname;
	    }
	}

	$output .= "\n\n<!-- 处理 Email 发送 --> \n\n";
	chomp $toemail;
	$toemail =~ s/\\//g;
	$fromemail = $adminemail_out;
	chomp $fromemail;
	$fromemail =~ s/\\//g;
	$topictitle =~ s/&quot\;/\"/g;
        $topictitle =~ s/^＊＃！＆＊//;

	$to = $toemail;
	$from = $fromemail;
	$subject = "[$forumname] 回复通知";
        $message .= "$boardname <br>\n";
	$message .= "$boardurl/leobbs.cgi <br>\n";
        $message .= "---------------------------------------------------------------------\n<br><br>\n";
        $message .= "你好, 你的帖子有了一个新回复！\n <br><br>\n";
        $message .= "回复人： $inmembername <br>\n";
        $message .= "分类： $category <br>\n";
        $message .= "论坛： $forumname <br>\n";
        $message .= "主题： $topictitle <br>\n";
        $message .= "点击下面的链接去查看详细内容：\n <br><br>\n";
        $message .= "$boardurl/topic.cgi?forum=$inforum&topic=$intopic\n <br><br>\n";
        $message .= "---------------------------------------------------------------------<br>\n";

        &sendmail($from, $emailaddress, $to, $subject, $message);
    }

    $numberofitems++;
    $postend = int($numberofitems / $maxtopics)*$maxtopics; 
    $pagestoshow = "";
    $numberofpages = $numberofitems / $maxtopics;
    if ($numberofitems > $maxtopics) {
        if ($maxtopics < $numberofitems) {
            ($integer,$decimal) = split(/\./,$numberofpages);
            if ($decimal > 0) { $numberofpages = $integer + 1; }
            $pagestart = 0;
            $counter = 0;
            while ($numberofpages > $counter) {
                $counter++;
                $threadpages .= qq~ <a href="topic.cgi?forum=$inforum&topic=$intopic&start=$pagestart">$counter</a> ~;
                $pagestart = $pagestart + $maxtopics;
            }
        }
	$pagestoshow = qq~<font color=$forumfontcolor> &nbsp;[ 第$threadpages页 ]~;
    }

    &mischeader("回复成功");

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);

unlink ("${lbdir}cache/plcache$inforum\_0.pl");

    if ($refreshurl == 1) { $relocurl = "topic.cgi?forum=$inforum&topic=$intopic&start=$postend#bottom"; }
                     else { $relocurl = "forums.cgi?forum=$inforum"; }
    $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>谢谢！您的回复已经成功发表！</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>如果浏览器没有自动返回，请点击下面的链接！：
<ul><li><a href="topic.cgi?forum=$inforum&topic=$intopic">返回主题</a>  $pagestoshow
<li><a href="forums.cgi?forum=$inforum">返回论坛</a><li><a href="leobbs.cgi">返回论坛首页</a>
<li><a href="postings.cgi?action=lock&forum=$inforum&topic=$intopic&checked=yes">锁定帖子</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
    }
1;
