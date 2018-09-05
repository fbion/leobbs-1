#####################################################
#  LEO SuperCool BBS / LeoBBS X / é›·å‚²æé…·è¶…çº§è®ºå›  #
#####################################################
# åŸºäºå±±é¹°(ç³Š)ã€èŠ±æ— ç¼ºåˆ¶ä½œçš„ LB5000 XP 2.30 å…è´¹ç‰ˆ  #
#   æ–°ç‰ˆç¨‹åºåˆ¶ä½œ & ç‰ˆæƒæ‰€æœ‰: é›·å‚²ç§‘æŠ€ (C)(R)2004    #
#####################################################
#      ä¸»é¡µåœ°å€ï¼š http://www.LeoBBS.com/            #
#      è®ºå›åœ°å€ï¼š http://bbs.LeoBBS.com/            #
#####################################################

    if ($startnewthreads eq "onlysub") {&error("å‘è¡¨&å¯¹ä¸èµ·ï¼Œè¿™é‡Œæ˜¯çº¯å­è®ºå›åŒºï¼Œä¸å…è®¸å‘è¨€ï¼"); }
    if (($floodcontrol eq "on") && ($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'amo') && ($membercode ne 'cmo') && ($membercode ne "mo") && ($inmembmod ne "yes")) {
	($lastpost, $posturl, $posttopic) = split(/\%\%\%/,$lastpostdate);
	$lastpost = $lastpost + $floodcontrollimit;
	if ($lastpost > $currenttime)  {
	    my $lastpost1 = $lastpost - $currenttime;
	    &error("å‘è¡¨æ–°ä¸»é¢˜&çŒæ°´é¢„é˜²æœºåˆ¶å·²ç»ä½¿ç”¨ï¼Œæ‚¨å¿…é¡»å†ç­‰å¾… $lastpost1 ç§’é’Ÿæ‰èƒ½å†æ¬¡å‘è¡¨ï¼");
	}
    }
    if (($inhiddentopic eq "yes") && ($moneyhidden eq "yes")) { &error("å‘è¡¨ä¸»é¢˜&è¯·ä¸è¦åœ¨ä¸€ä¸ªå¸–å­å†…åŒæ—¶ä½¿ç”¨å¨æœ›å’Œé‡‘é’±åŠ å¯†ï¼"); }
    if ((($inhiddentopic eq "yes")||($moneyhidden eq "yes")) && ($userregistered eq "no")) { &error("å‘è¡¨ä¸»é¢˜&æœªæ³¨å†Œç”¨æˆ·æ— æƒè¿›è¡Œå¨æœ›å’Œé‡‘é’±åŠ å¯†ï¼"); }

    &error("å‘è¡¨æˆ–å›å¤ä¸»é¢˜&å¯¹ä¸èµ·ï¼Œæœ¬è®ºå›ä¸å…è®¸å‘è¡¨æˆ–å›å¤è¶…è¿‡ <B>$maxpoststr</B> ä¸ªå­—ç¬¦çš„æ–‡ç« ï¼") if ((length($inpost) > $maxpoststr)&&($maxpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));
    &error("å‘è¡¨æˆ–å›å¤ä¸»é¢˜&å¯¹ä¸èµ·ï¼Œæœ¬è®ºå›ä¸å…è®¸å‘è¡¨æˆ–å›å¤å°‘äº <B>$minpoststr</B> ä¸ªå­—ç¬¦çš„æ–‡ç« ï¼") if ((length($inpost) < $minpoststr)&&($minpoststr ne "")&&($membercode ne "ad")&&($membercode ne 'smo')&&($membercode ne 'cmo') && ($membercode ne "mo") && ($membercode ne "amo") && ($membercode !~ /^rz/) && ($inmembmod ne "yes"));

    if ($postopen eq "no") { &error("å‘è¡¨æˆ–å›å¤ä¸»é¢˜&å¯¹ä¸èµ·ï¼Œæœ¬è®ºå›ä¸å…è®¸å‘è¡¨æˆ–å›å¤ä¸»é¢˜ï¼"); }

    my $filetoopens = "$lbdir" . "data/onlinedata.cgi";
    $filetoopens = &lockfilename($filetoopens);
    if (!(-e "$filetoopens.lck")) {
	if ($privateforum ne "yes") { &whosonline("$inmembername\t$forumname\tnone\tå‘è¡¨æ–°ä¸»é¢˜\t"); }
	                       else { &whosonline("$inmembername\t$forumname(å¯†)\tnone\tå‘è¡¨æ–°çš„ä¿å¯†ä¸»é¢˜\t"); }
    }

    if ((($onlinetime + $onlinetimeadd) < $onlinepost)&&($onlinepost ne "")&&($membercode ne "ad")&&($membercode ne "smo")&&($membercode ne "cmo")&&($membercode ne "mo")&&($membercode ne "amo")&&($membercode !~ /^rz/))     { $onlinetime = $onlinetime + $onlinetimeadd; &error("å‘è¡¨æ–°ä¸»é¢˜&å¯¹ä¸èµ·ï¼Œæœ¬è®ºå›ä¸å…è®¸åœ¨çº¿æ—¶é—´å°‘äº $onlinepost ç§’çš„ç”¨æˆ·å‘è¡¨ä¸»é¢˜ï¼ä½ ç›®å‰å·²ç»åœ¨çº¿ $onlinetime ç§’ï¼<BR>å¦‚æœåœ¨çº¿æ—¶é—´ç»Ÿè®¡ä¸æ­£ç¡®,è¯·é‡æ–°ç™»é™†è®ºå›ä¸€æ¬¡å³å¯è§£å†³ï¼"); }

    if (($userregistered eq "no")&&(length($inmembername) > 12)) { &error("å‘è¡¨æ–°ä¸»é¢˜&æ‚¨è¾“å…¥çš„ç”¨æˆ·åå¤ªé•¿ï¼Œè¯·æ§åˆ¶åœ¨6ä¸ªæ±‰å­—å†…ï¼");   }
    if (($userregistered eq "no")&&($inmembername =~ /^å®¢äºº/)) { &error("å‘è¡¨æ–°ä¸»é¢˜&è¯·ä¸è¦åœ¨ç”¨æˆ·åçš„å¼€å¤´ä¸­ä½¿ç”¨å®¢äººå­—æ ·ï¼");   }
    if ($inmembername eq "å®¢äºº") { &error("å‘è¡¨æ–°ä¸»é¢˜&è¯·ä¸è¦åœ¨ç”¨æˆ·åçš„å¼€å¤´ä¸­ä½¿ç”¨å®¢äººå­—æ ·ï¼");   }
    if (($userregistered eq "no")&&($startnewthreads ne "all")) { &error("å‘è¡¨æ–°ä¸»é¢˜&æ‚¨æ²¡æœ‰æ³¨å†Œï¼");   }
    elsif ((($inpassword ne $password)&&($userregistered ne "no"))||(($inpassword ne "")&&($userregistered eq "no"))) { &error("å‘è¡¨æ–°ä¸»é¢˜&æ‚¨çš„å¯†ç é”™è¯¯ï¼"); }
    elsif (($membercode eq "banned")||($membercode eq "masked"))      { &error("æ·»åŠ å›å¤&æ‚¨è¢«ç¦æ­¢å‘è¨€æˆ–è€…å‘è¨€è¢«å±è”½ï¼Œè¯·è”ç³»ç®¡ç†å‘˜è§£å†³ï¼"); }
    elsif ($intopictitle eq "ï¼Šï¼ƒï¼ï¼†ï¼Š") { &error("å‘è¡¨æ–°ä¸»é¢˜&å¿…é¡»è¾“å…¥ä¸»é¢˜æ ‡é¢˜ï¼"); }
    elsif (length($intopictitle) > 92)   { &error("å‘è¡¨æ–°ä¸»é¢˜&ä¸»é¢˜æ ‡é¢˜è¿‡é•¿ï¼"); }
    else  {
#	&error("å‘è¡¨æ–°ä¸»é¢˜&æ­¤åŒºæ–°ä¸»é¢˜å¿…é¡»å¸¦é™„ä»¶ï¼Œè¯·è¿”å›é‡è¯•ï¼") if (($addme eq "")&&($mastpostatt eq "yes")&&($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"));
#	@allforums = @forums;
	$intopictitle =~ s/\(æ— å†…å®¹\)$//;
	if (($inpost eq "")&&($addme eq "")) { $intopictitle.=" (æ— å†…å®¹)"; }
        $intopictitle =~ s/()+//isg;
	my $tempintopictitle = $intopictitle;
	$tempintopictitle =~ s/ //g;
	$tempintopictitle =~ s/\&nbsp\;//g;
        $tempintopictitle =~ s/ã€€//isg;
        $tempintopictitle =~ s/rror("·¢±í&¶Ô²»Æğ£¬Äú²»ÔÊĞíÔÚ´ËÂÛÌ³·¢±í£¡"); }

	if ($startnewthreads eq "no") {
            unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes") { &error("·¢±íĞÂÖ÷Ìâ&ÔÚ´ËÂÛÌ³ÖĞÖ»ÄÜÓÉÌ³Ö÷»òÕß±¾°æ°æÖ÷·¢±íĞÂÖ÷Ìâ£¡"); }
	}
	elsif ($startnewthreads eq "cert") {
            unless ($membercode eq "ad" ||$membercode eq 'smo'|| $inmembmod eq "yes"||$membercode eq 'cmo'||$membercode eq 'mo'||$membercode eq 'amo'||$membercode =~ /^rz/) { &error("·¢±íĞÂÖ÷Ìâ&ÔÚ´ËÂÛÌ³ÖĞÖ»ÄÜÓÉÌ³Ö÷¡¢°æÖ÷ºÍÈÏÖ¤»áÔ±·¢±íĞÂÖ÷Ìâ£¡"); }
	}
	elsif (($startnewthreads eq "follow") &&($action eq "addnew")) {
            unless ($membercode eq "ad" ||$membercode eq 'smo'||$membercode eq 'cmo' ||$membercode eq 'mo'||$membercode eq 'amo'|| $inmembmod eq "yes") { &error("·¢±íĞÂÖ÷Ìâ&ÔÚ´ËÂÛÌ³ÖĞÖ»ÄÜÓÉÌ³Ö÷»òÕß°æÖ÷·¢±íĞÂÖ÷Ìâ£¡"); }
	}
	elsif (($startnewthreads eq "all")&&($userregistered eq "no")) { $inmembername = "$inmembername(¿Í)"; }

	if ($deletepercent > 0 && $numberofposts + $numberofreplys > 0 && $membercode ne "ad" && $membercode ne "smo" && $membercode ne "cmo" && $membercode ne "mo" && $membercode ne "amo" && $inmembmod ne "yes") {
	    &error("·¢±íĞÂÖ÷Ìâ&¶Ô²»Æğ£¬ÄãµÄÉ¾ÌùÂÊ³¬¹ıÁË<b>$deletepercent</b>%£¬¹ÜÀíÔ±²»ÔÊĞíÄã·¢±íĞÂÖ÷Ìâ£¡ÇëÁªÏµÌ³Ö÷½â¾ö£¡") if ($postdel / ($numberofposts + $numberofreplys) >= $deletepercent / 100);
	}

        $inpost =~ s/\[Õâ¸ö(.+?)×îºóÓÉ(.+?)±à¼­\]//isg;
	$inpost = "\[watermark\]$inpost\[\/watermark\]" if (($intopictitle =~ /\[Ô­´´\]/)&&($usewm ne "no"));

        if ($emote && $inpost =~ m/\/\/\//) {
	    study ($inpost);
 	    my @pairs1 = split(/\&/,$emote);
	    foreach (@pairs1) {
		my ($toemote, $beemote) = split(/=/,$_);
		chomp $beemote;
		$beemote =~ s/¶ÔÏó/¡¼$inmembername¡½/isg;
		$inpost =~ s/$toemote/$beemote/isg;
		last unless ($inpost =~ m/\/\/\//);
	    }
	}

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
	    	&error("·¢±íĞÂÖ÷Ìâ&Çë²»ÒªÖØ¸´·¢Ìû×Ó£¬ÒÑ¾­´æÔÚÓë´ËÌû×ÓÖ÷ÌâÏàÍ¬»òÕßÄÚÈİÏàÍ¬µÄ¶øÇÒÊÇÄã·¢µÄÌû×ÓÁË£¡");
	    }
	}

	my $temp = &dofilter("$intopictitle\t$inpost");
	($intopictitle,$inpost) = split(/\t/,$temp);
	$intopictitle =~ s/(a|A)N(d|D)/$1&#78;$2/sg;
	$intopictitle =~ s/(a|A)n(d|D)/$1&#110;$2/sg;
	$intopictitle =~ s/(o|O)R/$1&#82;/sg;
	$intopictitle =~ s/(o|O)r/$1&#114;/sg;
#	$intopictitle  =~ s/\\/&#92;/isg;
	
	$inpost =~ s/\[UploadFile.{0,6}=(.+?)\]//isg unless (($arrowupload ne "no")||($membercode eq "ad")||($membercode eq 'smo')||($inmembmod eq "yes"));
	
	$inpost =~ s/(ev)a(l)/$1&#97;$2/isg;

        $addme= &upfileonpost(\$inpost,$inforum,$newthreadnumber);#´¦ÀíÉÏ´«£¬·µ»ØÊıÖµ¸øBTÇø×öÅĞ¶Ï
	&error("·¢±íĞÂÖ÷Ìâ&´ËÇøĞÂÖ÷Ìâ±ØĞë´ø¸½¼ş£¬Çë·µ»ØÖØÊÔ£¡") if (($addme eq "0")&&($mastpostatt eq "yes")&&($membercode ne "ad")&&($membercode ne 'smo')&&($inmembmod ne "yes"));
	$addme = "" if ($addme eq "0");
	$intopictitletemp = $intopictitle ;
	$intopictitletemp =~ s/^£ª£££¡£¦£ª//;

        if ($moneyhidden eq "yes") { $inposttemp = "(±£ÃÜ)"; $inpost="LBSALE[$moneypost]LBSALE".$inpost;}

	if ($inhiddentopic eq "yes") { $inposttemp = "(±£ÃÜ)"; $inpost="LBHIDDEN[$postweiwang]LBHIDDEN".$inpost; }
	
	if ($inposttemp ne "(±£ÃÜ)") {
	    $inposttemp = $inpost;
	    $inposttemp = &temppost($inposttemp);
	    chomp $inposttemp;
            $inposttemp = &lbhz($inposttemp,50);
        }

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
			    $temptopic =~ s/^£ª£££¡£¦£ª//;
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
			    &error("³ö´í&ÓÉÓÚÄãÔÚ¶àÇø·¢ËÍ¹ã¸æ£¬ËùÒÔÄãÒÑ¾­±»½ûÖ¹·¢ÑÔ£¡");
			}
		    }

		    $recentposts=@recentposts;
		    $maxpostreport = 31;
		    if ($recentposts<$maxpostreport) { $maxpostreport=$recentposts;} else { $maxpostreport--; }
		    
		    if (open (FILE, ">$filetomakeopen")) {
			flock (FILE, 2) if ($OS_USED eq "Unix");
			print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inposticon\t$inmembername\t\n";
			for ($i=0;$i<$maxpostreport;$i++) { print FILE $recentposts[$i]; }
			close(FILE);
		    }
		    &winunlock($filetomakeopen) if ($OS_USED eq "Nt");
		} else {
      		    if (open (FILE, ">$filetomakeopen")) {
      			print FILE "$inforum\t$newthreadnumber\t$intopictitletemp\t$currenttime\t$inposticon\t$inmembername\t\n";
      			close(FILE);
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

	if ($jifen eq "") {
		require "data/cityinfo.cgi" if ($addmoney eq "" || $replymoney eq "" || $moneyname eq "");
		$jifen = $numberofposts * $ttojf + $numberofreplys * $rtojf - $postdel * $deltojf;
  }
        
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
            if ($threads < 10) {
    opendir (CATDIR, "${lbdir}cache");
    @dirdata = readdir(CATDIR);
    closedir (CATDIR);
    @dirdata = grep(/forumcache/,@dirdata);
    foreach (@dirdata) { unlink ("${lbdir}cache/$_"); }
            }
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

        if (($emailfunctions eq "on") && ($innotify eq "yes")) {
            if (open (FILE, ">${lbdir}forum$inforum/$newthreadnumber.mal.pl")) {
                print FILE "$inmembername\t$emailaddress\t\n";
                close (FILE);
            }
        }

        &mischeader("ĞÂÖ÷Ìâ·¢±í³É¹¦");

opendir (CATDIR, "${lbdir}cache");
@dirdata = readdir(CATDIR);
closedir (CATDIR);

unlink ("${lbdir}cache/plcache$inforum\_0.pl");

        if ($refreshurl == 1) { $relocurl = "topic.cgi?forum=$inforum&topic=$newthreadnumber"; }
	                 else { $relocurl = "forums.cgi?forum=$inforum"; }
        $output .= qq~<SCRIPT>valigntop()</SCRIPT><table cellpadding=0 cellspacing=0 width=$tablewidth bgcolor=$tablebordercolor align=center>
<tr><td><table cellpadding=6 cellspacing=1 width=100%>
<tr><td bgcolor=$titlecolor $catbackpic align=center><font color=$fontcolormisc><b>Ğ»Ğ»£¬$inmembername£¡ÄúµÄĞÂÖ÷ÌâÒÑ¾­·¢±í³É¹¦£¡</b></font></td></tr>
<tr><td bgcolor=$miscbackone><font color=$fontcolormisc>Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯·µ»Ø£¬Çëµã»÷ÏÂÃæµÄÁ´½Ó£¡
<ul><li><a href="topic.cgi?forum=$inforum&topic=$newthreadnumber">·µ»ØĞÂÖ÷Ìâ</a>
<li><a href="forums.cgi?forum=$inforum">·µ»ØÂÛÌ³</a>
<li><a href="leobbs.cgi">·µ»ØÂÛÌ³Ê×Ò³</a>
<li><a href="postings.cgi?action=locktop&forum=$inforum&topic=$newthreadnumber">ĞÂÖ÷Ìâ¹Ì¶¥</a>
<li><a href="postings.cgi?action=catlocktop&forum=$inforum&topic=$newthreadnumber">ĞÂÖ÷ÌâÇø¹Ì¶¥</a>
<li><a href="postings.cgi?action=abslocktop&forum=$inforum&topic=$newthreadnumber">ĞÂÖ÷Ìâ×Ü¹Ì¶¥</a>
</ul></tr></td></table></td></tr></table>
<SCRIPT>valignend()</SCRIPT>
<meta http-equiv="refresh" content="3; url=$relocurl">
	~;
    }
1;
