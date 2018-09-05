#!/usr/bin/perl
#####################################################
#  LEO SuperCool BBS / LeoBBS X / é›·å‚²æé…·è¶…çº§è®ºå›  #
#####################################################
# åŸºäºå±±é¹°(ç³Š)ã€èŠ±æ— ç¼ºåˆ¶ä½œçš„ LB5000 XP 2.30 å…è´¹ç‰ˆ  #
#   æ–°ç‰ˆç¨‹åºåˆ¶ä½œ & ç‰ˆæƒæ‰€æœ‰: é›·å‚²ç§‘æŠ€ (C)(R)2004    #
#####################################################
#      ä¸»é¡µåœ°å€ï¼š http://www.LeoBBS.com/            #
#      è®ºå›åœ°å€ï¼š http://bbs.LeoBBS.com/            #
#####################################################
# 2005-07-1 maiweb å¤§ä¿®æ­£ -------- For leobbs 0926 ä»¥åçš„ç‰ˆæœ¬
# 1ï¼Œä¿®æ­£ä¼šå‘˜èµ„æ–™å¤‡ä»½ã€æ¢å¤Bug ------ä»…ä»…å¤‡ä»½ oldç›®å½•ä¸‹é¢çš„å†…å®¹
# 2ï¼Œä¿®æ­£å¤šé™„ä»¶å¤šç›®å½•å¤‡ä»½bug
# 3ï¼Œæ¿å—å¸–å­æ¢å¤ä¹‹åï¼Œéœ€è¦è¿›å…¥åå°é‡æ–°ç»Ÿè®¡ä¸€æ¬¡ï¼
# 4ï¼Œä¿®æ­£ç³»ç»Ÿé…ç½®å¤‡ä»½å®Œå…¨
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
use Archive::Tar;
use Cwd;
use File::DosGlob 'glob';
use File::Copy;
$loadcopymo = 1;

$LBCGI::POST_MAX=200000;
$LBCGI::DISABLE_UPLOADS = 1;
$LBCGI::HEADERS_ONCE = 1;
require "data/boardinfo.cgi";
require "admin.lib.pl";
require "bbs.lib.pl";
$|++;

$thisprog = "adbackup.cgi";

$query = new LBCGI;

$action          = $query -> param('action');
$action          = &unHTML("$action");
@dirtoopen     = $query -> param('dirtoopen');

$inmembername = $query->cookie("adminname");
$inpassword   = $query->cookie("adminpass");
$inmembername =~ s/[\a\f\n\e\0\r\t\`\~\!\@\#\$\%\^\&\*\(\)\+\=\\\{\}\;\'\:\"\,\.\/\<\>\?]//isg;
$inpassword =~ s/[\a\f\n\e\0\r\t\|\@\;\#\{\}\$]//isg;

$attachement  = $query-> param('attachement');
$fn=            $query-> param('fn');
$an=            $query-> param('an');
$mn=            $query-> param('mn');
$un=            $query-> param('un');
$comeon=        $query-> param('comeon');
$step=        $query-> param('step');
$ttarnum=        $query-> param('ttarnum');
$atarnum=        $query-> param('atarnum');
$mtarnum=        $query-> param('mtarnum');
$utarnum=        $query-> param('utarnum');
$tarname=        $query-> param('tarname');
$totalnum=        $query-> param('totalnum');
$currentnum=        $query-> param('currentnum');
$oldversion=        $query-> param('oldversion');
$packall=        $query-> param('packall');
$mgn=  $query-> param('mgn');

##########æ¢å¤å˜é‡
@restorelist=        $query-> param('restorelist');
$toopen=        $query-> param('toopen');

if ($memdir ne "")
 {$memberdir=$memdir;} elsif ($memberdir eq "") {$memberdir="members";}

&getadmincheck;
print header(-charset=>gb2312 , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");       
&admintitle;
        
&getmember("$inmembername","no");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>æ¬¢è¿æ¥åˆ°è®ºå›ç®¡ç†ä¸­å¿ƒ / è®ºå›æ•°æ®å¤‡ä»½</b>
            </td></tr>
            ~;
            
            my %Mode = ( 
            'prebackup'             =>    \&prebackup,
            'delete'            =>    \&delete,
            'restore'            =>    \&restore,
            'dorestore'            =>    \&dorestore,
            'backup'              =>     \&backup,
            'select'           =>       \&memberoptions1,
            'untar'              =>       \&untar
            );


            if($Mode{$action}) { 
               $Mode{$action}->();
               }
                else { &memberoptions; }
            
            print qq~</table></td></tr></table>~;
            }
                
            else {
               &adminlogin;
               }
        

sub restore {
print qq~
    <form action="$thisprog" method=post name=form>
    <input type=hidden name="action" value="dorestore">
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>è¯·è¾“å…¥ä½ è¦è¿˜åŸçš„å¤‡ä»½æ–‡ä»¶åç§°</b>    
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <div align=center><font color=#333333><BR>è¯·è¾“å…¥ä½ è¦è¿˜åŸçš„å¤‡ä»½æ–‡ä»¶åç§°ï¼Œå¹¶ä¸”ç¡®è®¤ä½ å·²ç»ç”¨FTPä¸Šä¼ åˆ°ä½ çš„$lbdirå½“å‰ç›®å½•ï¼ <br><br><B><input type=input size=40 name="dirtoopen" value="xqlb.tar"></B><p></div>
    >***å¦‚æœä½ è¦è¿˜åŸçš„é¡¹ç›®ï¼Œæ‰“åŒ…æ—¶æœªé€‰å–<font color=blue>æ±‡æ€»æ‰“åŒ…</font>é€‰é¡¹ï¼Œè¯·å°†æ‰€æœ‰çš„ä¸‹è½½æ–‡ä»¶ç½®äºä½ çš„$lbdirå½“å‰ç›®å½•ï¼Œå¹¶åœ¨è¾“å…¥æ¡†ä¸­è¾“å…¥<font color=blue>tarfilelist.txt</font>***
    <br><Br>
    <div align=center>
    <input type="checkbox" name="oldversion" value="yes"><font color=red>æ—§ç‰ˆæœ¬è§£åŒ…</font><br>
    å¦‚æœä½ çš„æ–‡ä»¶åŒ…ä¸æ˜¯ä½¿ç”¨æ–°ç‰ˆæœ¬å¤‡ä»½ç¨‹åºåˆ¶ä½œçš„ï¼Œè¯·åŠ¡å¿…é€‰å–æ­¤é¡¹ï¼‰
    <p>
    <input type="submit" name="Submit" value="ç¡®è®¤è¿˜åŸå¤‡ä»½"></div>
    <p>
    </td>
    </tr>
    
    </form>
    
   
   ~;           
}

sub dorestore
{
  
   chdir $lbdir;
   if ($oldversion eq "yes") 
   {&oldrestore;} 
   else #new restore
   {
    $toopen=@dirtoopen[0];
    if (-e "${lbdir}$toopen") #do
    {
      #################### æœªæ±‡æ€»å¤„ç† ##   
      if ($toopen eq "tarfilelist.txt")
      {
       $packall="no";
       chdir $lbdir;
       open(FILE,"$toopen"); 
       @tarinfo=<FILE>;
       chomp(@tarinfo);
       close(FILE);        
       (my $a,$tarname)=split(/\t/,$tarinfo[1]) ;
       @tarfile=glob("$tarname*.tar");
       unshift(@tarfile,"$toopen");                         
      }
      
      
      
      
      if ($packall ne "no")
      
      {
      my $tar =  Archive::Tar->new();
      unless ($tar->read("${lbdir}$toopen", 0)) {
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopenä¸èƒ½è¯»å–ï¼Œè¯·æ£€æŸ¥æ˜¯å¦ä½¿ç”¨äºŒè¿›åˆ¶æ¨¡å¼ä¸Šä¼ (ä¸€å®šè¦è¿™ä¸ªæ¨¡å¼ä¸Šä¼ è¿™ä¸ªå‹ç¼©åŒ…)</td></tr>~;
            exit;
        }                                        
      @tarfile=$tar->list_files(); 
      chdir $lbdir;
      $tar->extract($tarfile[0],$lbdir);
      }  
     

       	     

      if ($tarfile[0] eq "tarfilelist.txt")
      {       
         
       open(FILE,">tarfileindex.txt");
       foreach(@tarfile)
        {
        print FILE "$_";
        print FILE "\n";
       }
       close(FILE);
                  
       ################## è¯»å–åŒ…ä¿¡æ¯
       open(FILE,"tarfilelist.txt"); 
       @tarinfo=<FILE>;
       chomp(@tarinfo);
       close(FILE);
        
       (my $a,$tartime)=split(/\t/,$tarinfo[0]) ;
       (my $a,$tarname)=split(/\t/,$tarinfo[1]) ;
       (my $a,$totalnum)=split(/\t/,$tarinfo[2]);
       (my $a,$havemember)=split(/\t/,$tarinfo[3]);
       (my $a,$haveavatar)=split(/\t/,$tarinfo[4]);
       (my $a,$havesystem)=split(/\t/,$tarinfo[5]);
       (my $a,$havetopic)=split(/\t/,$tarinfo[6]);
       (my $a,$haveattachement)=split(/\t/,$tarinfo[7]);
       (my $a,$havemsg1)=split(/\t/,$tarinfo[8]);
       (my $a,$havemsg2)=split(/\t/,$tarinfo[9]);

       if ($havemember>0)
       {
       	$showmember="<input type='checkbox' name='restorelist' value='memdir'>ç”¨æˆ·èµ„æ–™æ–‡ä»¶";
       	}
       if ($havemsg1>0)
       {
       $showmsg="<input type='checkbox' name='restorelist' value='msg'>çŸ­æ¶ˆæ¯æ–‡ä»¶";
       }
       if ($havemsg2>0)
       {
       $showmsg="<input type='checkbox' name='restorelist' value='msg'>çŸ­æ¶ˆæ¯æ–‡ä»¶";
       }
       if ($haveavatar>0)
       {
       	$showavatar="<input type='checkbox' name='restorelist' value='avatar'>ç”¨æˆ·è‡ªå®šä¹‰å¤´åƒ";
       	}
       if ($havesystem>0)
       {
       $showsystem="<input type='checkbox' name='restorelist' value='system'>ç³»ç»Ÿé…ç½®æ–‡ä»¶";
       }
       
       if ($havetopic>0)
       {
       @forumlist=();
       for ($i=13;$i<$#tarinfo;$i++)
        {
 
        if ($tarinfo[$i] =~ m/forum/) 
        
        {push(@forumlist,$tarinfo[$i]);}
        }
       chomp(@forumlist);
       $showforum="<table width=97% align=center>";
       $ii=0;
       foreach(@forumlist)
        {
          ($forumid,$forumname)=split(/\t/,$_);
          ($a,$forumid)=split(/m/,$forumid);
                    
          $showforum.="<tr>" if ($ii==0);
          $showforum=$showforum."<td><p><input type='checkbox' name='restorelist' value=$forumid>${forumname}</td><td>è¿˜åŸè‡³$forumidå·ç‰ˆé¢</td>";
          $showforum.="</tr>" if ($ii==2);
          $ii=($ii>2)?0:++$i;
        }
        $showforum.="</table>";
        }
        else
        {
        $showforum="<p>è¯¥åŒ…ä¸­æ²¡æœ‰å¤‡ä»½è®ºå›ç‰ˆé¢è´´å­<p>";
        }
      if($haveattachement>0)
       {
       $showattachement="<input type='checkbox' name='restorelist' value='attachement' checked>è¿˜åŸç‰ˆé¢åŒæ—¶æ¢å¤è¯¥ç‰ˆé¢é™„ä»¶<br>"
       }
       else
       {
       $showattachement="è¯¥åŒ…ä¸­æ²¡æœ‰å¤‡ä»½è®ºå›ç‰ˆé¢è´´å­é™„ä»¶";
       }
       
      print qq~
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="untar">
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>è¯·é€‰æ‹©ä½ è¦è¿˜åŸçš„é¡¹ç›®</b>
        <p>
        å¤‡ä»½æ—¶é—´:$tartime
        </td>
        </tr>          
        

                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <p>
    <font color=red>ç³»ç»Ÿæ•°æ®ï¼š</font>
    <hr>
    $showmember &nbsp $showmsg &nbsp $showavatar &nbsp $showsystem
    <p>
    <font color=red>éœ€è¦æ¢å¤çš„ç‰ˆé¢</font>
    <hr>
    $showforum
    <p>
    <div align=center>$showattachement</div>
    <hr>
    <div align=center>
                <input type=hidden name="tarname" value="$tarname">
                <input type=hidden name="step" value="preuntar">
                <input type=hidden name="toopen" value="$toopen">
                <input type=hidden name="packall" value="$packall">
                <input type=hidden name="totalnum" value="$totalnum">
                <input type="submit" name="Submit" value="æ¢å¤æ–‡ä»¶é¢„å¤„ç†">
                <input type="reset" name="Submit2" value="é‡æ–°é€‰æ‹©">

    </td>
    </tr>
    </form>
~; 
        
        
        
        
   
       print "</td></tr>";
      } 
      else
      {
           print qq~	
      <tr>
    <td bgcolor=#FFFFFF colspan=2>
    æ— æ³•æ‰¾åˆ°ç´¢å¼•æ–‡ä»¶.(å‡ºé”™åŸå› :å¾ˆæœ‰å¯èƒ½è¿™ä¸ªæ–‡ä»¶ä¸æ˜¯ä½¿ç”¨æœ¬ç‰ˆæœ¬æ‰“åŒ…....!æˆ–è€….æ–‡ä»¶è¢«æ›´æ”¹è¿‡) 
     </td>
      </tr>
      ~;
     exit;
      
      } 
       
         
      
      } # end if do 
     else  #abc
     {
     
     print qq~	
      <tr>
    <td bgcolor=#FFFFFF colspan=2>
    å¤‡ä»½èµ„æ–™æ²¡æ‰¾åˆ°æ‰¾åˆ°ï¼Œè¯·æ£€æŸ¥è¾“å…¥çš„æ–‡ä»¶åå’Œæ˜¯å¦å·²ç»ä¸Šä¼ ï¼
     </td>
      </tr>
      ~;
     exit;
     
     
     }  #end else abc
   
   }
}


sub untar
{

opendir (DIRS, "$lbdir");
my @files2 = readdir(DIRS);
closedir (DIRS);
@files2 = grep(/^\w+?$/i, @files2);
my @msgdir = grep(/^messages/i, @files2);
$msgdir = $msgdir[0];
       
       chdir $lbdir;
       if ($step eq "preuntar")
        {
        print qq~
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="untar">
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>è§£åŒ…é¢„å¤„ç†</b>
        </td>
        </tr>
        <tr>       
        <td align=center colspan=2>
         ~;        
         if (-e "tarfileindex.txt")
         {
         
         open(FILE,"tarfileindex.txt");
         @filelist=<FILE>;
         chomp(@filelist);
         close(FILE);
         if($restorelist[$#restorelist] eq "attachement")
         {
         $attachement="yes";
         pop(@restorelist);
         }
         
         @needtotar=();
         foreach $rl (@restorelist)
         {
          
           if($rl eq "memdir")  
               {
               	foreach $fl (@filelist)
               	   {
               	      $a=$tarname."m";
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${lbdir}${memberdir}/old");# ä¿®æ­£by maiweb
               	      }
               	   }
               	}
           elsif($rl eq "msg")  
                {
                     	foreach $fl (@filelist)
               	   {
               	      $a=$tarname."gin";
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${lbdir}$msgdir/in");}
               	   }
                     	foreach $fl (@filelist)
               	   {
               	      $a=$tarname."gout";
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${lbdir}$msgdir/out");}
               	   }
                }
           elsif($rl eq "avatar")  
                {
                     	foreach $fl (@filelist)
               	   {
               	      $a=$tarname."u";
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${imagesdir}usravatars");}
               	   }
                }
           elsif($rl eq "system")  
               {
               		foreach $fl (@filelist)
               	   {
               	      $a=$tarname."s";
               	      if ($fl =~m /$a/) {push(@needtotar,"$fl\t${lbdir}data");}
               	   }
               	}
           elsif ($rl=~ /\d/)
           {
                  
                
                  foreach $fl (@filelist)
                     {
                     $a=$tarname."t_".$rl."_";
                     $b=$tarname."a_".$rl."_";
                     if ($fl =~m /$a/) {push(@needtotar,"$fl\t${lbdir}forum$rl");}
                     if ($attachement eq "yes")
                     {
                     if ($fl =~m /$b/) {push(@needtotar,"$fl\t${imagesdir}$usrdir/$rl");}
                     }
                    
                     }
                   
           
           }  #end elsif.....
           
        
           } #end foreach(@restorelist)
            
           chomp(@needtotar);
           open(FILE,">needtotar.txt");
           foreach(@needtotar)
           {
           print FILE "$_";
           print FILE "\n";
           }
           close(FILE);
          
           if ($packall ne "no")
           {
           my $tar =  Archive::Tar->new();
           unless ($tar->read("${lbdir}$toopen", 0)) {
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopenä¸èƒ½è¯»å–ï¼Œè¯·æ£€æŸ¥æ˜¯å¦ä½¿ç”¨äºŒè¿›åˆ¶æ¨¡å¼ä¸Šä¼ (ä¸€å®šè¦è¿™ä¸ªæ¨¡å¼ä¸Šä¼ è¿™ä¸ªå‹ç¼©åŒ…)</td></tr>~;
            exit;
           }           
        
           @needtotar1=();
           foreach(@needtotar)
           {
           ($a,$b)=split(/\t/,$_);
           push(@needtotar1,$a);
           }
           
           
           chdir $lbdir;
           $tar->extract(@needtotar1, $lbdir);
           }
           
          $error="no";
          $status="<div align=left><p><font color=red>";
          foreach(@needtotar)
          {
            (my $isok,my $dirname)=split(/\t/,$_);
             if  (-e "$isok")  {$status.="$isok åˆ†åŒ…æˆåŠŸ<br>";} else {$status.="$isok åˆ†åŒ…<font color=blue>æœªæˆåŠŸ</font>ã€‚è¯·æ£€æŸ¥æ˜¯å¦ä½¿ç”¨äºŒè¿›åˆ¶æ¨¡å¼ä¸Šä¼ ï¼<br>";$error="yes";}   
             if  (opendir(DIR,"$dirname")) {$status.="$dirname å­˜åœ¨<br>";} 
                   else {$status.="$dirname <font color=blue>ä¸å­˜åœ¨</font>";
                         if (mkdir("$dirname",777)) {
							 chmod(0777,"$dirname");
							 $status.="&nbsp ç›®å½•åˆ›å»ºæˆåŠŸ<br>";}
                            else{$status.="&nbspç›®å½•åˆ›å»ºå¤±è´¥<br>";$error="yes";}                         
                         } #else 
         
          
          }                  
          
          $status.="</font></div>";
          chdir $lbdir;
          open(FILE,">restorestatus.txt");
          print FILE "<div align=left><p>";
          close(FILE);
          
          print qq~
          $status
          <p>
          <div align=center>é¢„å¤„ç†å®Œæ¯•</div>
          <p>
          ~;
           if ($error eq "yes")
           {
             print qq~
          <p><font color=red>
          <div align=center>é¢„å¤„ç†é”™è¯¯ï¼Œè¯·æ ¹æ®é”™è¯¯æç¤ºï¼Œé‡æ–°æ£€æŸ¥ä¸€éã€‚</font>
          </td></tr>
          ~;
          exit;
           
           }
           
           
           
           
         }
         else
         {
         print qq~
         <p><font color=red>
         <div align=center>é¢„å¤„ç†é”™è¯¯ï¼Œè¯·è¿”å›ï¼Œé‡è¯•ä¸€éã€‚</font>
         </td></tr>
         ~;
         exit;
         }
        
        
        
        
      print qq~      
            <div align=center>
                <input type=hidden name="currentnum" value="0">
                <input type=hidden name="tarname" value="$tarname">
                <input type=hidden name="step" value="untar">
                <input type=hidden name="totalnum" value="$totalnum">
                <input type=hidden name="packall" value="$packall">
                <input type="submit" name="Submit" value="æ¢å¤æ–‡ä»¶">
        </form>
        </td>
        </tr>
        ~;
        }
       
        elsif ($step eq "untar")
        {
        print qq~
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="untar">
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>è§£åŒ…æ¢å¤ä¸­ã€‚ã€‚ã€‚ã€‚ã€‚</b>
        </td>
        </tr>
        <tr>       
        <td align=center colspan=2>
         ~;        
        chdir $lbdir;
        open(FILE,"needtotar.txt");
        @needtotar=<FILE>;
        close(FILE);
        chomp(@needtotar);
        $totar=shift(@needtotar);
        ($name,$dir)=split(/\t/,$totar);
		chdir $dir;
          my $tar =  Archive::Tar->new();
           $status="${lbdir}$nameè¿˜åŸå®Œæ¯•ã€‚";         
           unless ($tar->read("${lbdir}$name", 0)) {
	        print qq~
	        ${lbdir}$nameä¸èƒ½è¯»å–ï¼Œè¯·æ£€æŸ¥æ˜¯å¦ä½¿ç”¨äºŒè¿›åˆ¶æ¨¡å¼ä¸Šä¼ (ä¸€å®šè¦è¿™ä¸ªæ¨¡å¼ä¸Šä¼ è¿™ä¸ªå‹ç¼©åŒ…)
	        ~;
                $status="${lbdir}$nameä¸èƒ½è¯»å–ï¼Œè¯·æ£€æŸ¥æ˜¯å¦ä½¿ç”¨äºŒè¿›åˆ¶æ¨¡å¼ä¸Šä¼ (ä¸€å®šè¦è¿™ä¸ªæ¨¡å¼ä¸Šä¼ è¿™ä¸ªå‹ç¼©åŒ…)";

           }
        
            my @files = $tar->list_files();
            chdir $dir;
            $tar->extract(@files, $dir);
            $currentnum=$currentnum+$#files+1;
            chdir $lbdir;
            
            if ($packall ne "no") {
            	unlink("$name");
		$forumid = $name;
		$forumid =~ s/^$tarname//;
            	if ($forumid =~ /^t\_/i) {
		    $forumid =~ s/^t\_(\d+)\_(\d+)\.tar/$1/;
	    copy("${lbdir}forum$forumid/list$forumid.cgi","${lbdir}boarddata/listno$forumid.cgi");
	    copy("${lbdir}forum$forumid/xzb$forumid.cgi","${lbdir}boarddata/xzb$forumid.cgi");
	    copy("${lbdir}forum$forumid/xzbs$forumid.cgi","${lbdir}boarddata/xzbs$forumid.cgi");
	    copy("${lbdir}forum$forumid/lastnum$forumid.cgi","${lbdir}boarddata/lastnum$forumid.cgi");
	    copy("${lbdir}forum$forumid/ontop$forumid.cgi","${lbdir}boarddata/ontop$forumid.cgi");
	    copy("${lbdir}forum$forumid/jinghua$forumid.cgi","${lbdir}boarddata/jinghua$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/listno$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/xzb$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/xzbs$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/lastnum$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/ontop$forumid.cgi");
	    chmod(0666,"${lbdir}boarddata/jinghua$forumid.cgi");
	    unlink "${lbdir}forum$forumid/list$forumid.cgi";
	    unlink "${lbdir}forum$forumid/xzb$forumid.cgi";
	    unlink "${lbdir}forum$forumid/xzbs$forumid.cgi";
	    unlink "${lbdir}forum$forumid/lastnum$forumid.cgi";
	    unlink "${lbdir}forum$forumid/ontop$forumid.cgi";
	    unlink "${lbdir}forum$forumid/jinghua$forumid.cgi";
            	}
            }
         if ($#needtotar>=0)
         {
         open(FILE,">needtotar.txt");
         foreach(@needtotar)
         {
         print FILE "$_";
         print FILE "\n";
         }
                       chdir $lbdir;
                       open(FILE,">>restorestatus.txt");
                       print FILE "$status <br>";
                       close(FILES);
         
         }        
        
                              else { 
                              	
                       chdir $lbdir;
                       open(FILE,">>restorestatus.txt");
                       print FILE "$status <br>";
                       close(FILES);
                       
                       
                              	    print qq~      
                 <div align=center>
                
                <input type=hidden name="packall" value="$packall">
                <input type=hidden name="tarname" value="$tarname">
                <input type=hidden name="step" value="finish">
                <input type=hidden name="totalnum" value="$totalnum">
                <input type="submit" name="Submit" value="æ¢å¤æ–‡ä»¶">
        <script>
        setTimeout('document.form.submit()',2000);
        </script>
                   </div>
        
        
               </form>
               </td>
               </tr>
               ~;
                              	
                   exit;           	
                              	
                              	}
        
        $percent=int(($currentnum/$totalnum)*100);
        $percent1=int(100-$percent);                  
        
             print qq~      
           
            
            <div align=center>
                  <b>è¿˜åŸè¿›åº¦</b><br>
       (è¿˜åŸè¿›åº¦ä½“ç°çš„æ˜¯ä»¥è¿˜åŸæ–‡ä»¶åœ¨æ€»æ–‡ä»¶æ•°ä¸­çš„æ¯”ä¾‹,ä¸èƒ½ä»¥æ­¤ä½œä¸ºè¿˜åŸèŠ±è´¹æ—¶é—´çš„æ¨æ–­)
       <table width=80% board=0 height=20>
       <tr>
       <td width=$percent% bgcolor=blue></td>
       <td width=$percent1%></td>
       </tr>
       </table>
           
                <input type=hidden name="packall" value="$packall">
                <input type=hidden name="currentnum" value="$currentnum">
                <input type=hidden name="tarname" value="$tarname">
                <input type=hidden name="step" value="untar">
                <input type=hidden name="totalnum" value="$totalnum">
                <input type="submit" name="Submit" value="æ¢å¤æ–‡ä»¶">
        <script>
        setTimeout('document.form.submit()',2000);
        </script>
            </div>
        
        
        </form>
        </td>
        </tr>
        ~;
        
        
        
        
        }               
        elsif($step eq "finish")
        {
        chdir $lbdir;      
        open (FILE,"restorestatus.txt");
        @status=<FILE>;
        close(FILE);        
        chomp(@status);
        unlink("restorestatus.txt");
        unlink("tarfileindex.txt");
        unlink("needtotar.txt");
        unlink("tarfilelist.txt") if ($packall ne "no"); 
        
        
        print qq~
        <tr>
        <td>
        è¿˜åŸç»“æŸ..çŠ¶æ€å¦‚ä¸‹:
        @status
        </td>
        </tr>
        ~;
        }
        
        
        
       
         

}




sub oldrestore {
$toopen=@dirtoopen[0];
if (-e "${lbdir}$toopen"){
print qq~
<tr>
    <td bgcolor=#FFFFFF colspan=2>
    å¤‡ä»½èµ„æ–™æ‰¾åˆ°ï¼Œç°åœ¨å¼€å§‹è¿˜åŸï¼
</td>
</tr>
~;
{
        my $cwd = cwd();
        my $tar =  Archive::Tar->new();
        unless ($tar->read("${lbdir}$toopen", 0)) {
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopenä¸èƒ½è¯»å–ï¼Œè¯·æ£€æŸ¥æ˜¯å¦ä½¿ç”¨äºŒè¿›åˆ¶æ¨¡å¼ä¸Šä¼ (ä¸€å®šè¦è¿™ä¸ªæ¨¡å¼ä¸Šä¼ è¿™ä¸ªå‹ç¼©åŒ…)</td></tr>~;
            exit;
        }
        chdir $lbdir;
        my @files = $tar->list_files();
        $tar->extract(@files, $lbdir);
        chdir $cwd;
}
print qq~
<tr>
    <td bgcolor=#FFFFFF colspan=2>
    è¿˜åŸå®Œæˆï¼
</td>
</tr>
~;
}else {
print qq~	
<tr>
    <td bgcolor=#FFFFFF colspan=2>
    å¤‡ä»½èµ„æ–™æ²¡æ‰¾åˆ°æ‰¾åˆ°ï¼Œè¯·æ£€æŸ¥è¾“å…¥çš„æ–‡ä»¶åå’Œæ˜¯å¦å·²ç»ä¸Šä¼ ï¼ 
</td>
</tr>
~;
exit;
}

}	
sub memberoptions
{
chdir $lbdir; 
    $dirtoopen = "${imagesdir}";
    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = grep(/\.tar$/,@filedata);
    
    $backupfile = @sortedfile;
    if ($backupfile > 0) {
    	$last_backup = "æ®‹ç•™å¤‡ä»½æ–‡ä»¶å­˜åœ¨ï¼Œè¯·åŠæ—¶åˆ é™¤!";
           $bakuptrue = 0;
    }
    else {
           $last_backup = "æ®‹ç•™å¤‡ä»½æ–‡ä»¶æ²¡æœ‰æ‰¾åˆ°ï¼Œè®ºå›å®‰å…¨";
           $bakuptrue = 1;
    }   


     
    print qq~

    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>è¯·é€‰æ‹©ä½ è¦å¤‡ä»½çš„å†…å®¹</b>
    </td>
    </tr>          
        
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><BR>æ£€æŸ¥æ®‹ç•™å¤‡ä»½æ–‡ä»¶ï¼š <B>$last_backup</B><BR>
    <font color=red>æœ¬æ£€æŸ¥åªæœç´¢ $imagesdir ä¸‹æ˜¯å¦æœ‰æ®‹å­˜çš„å¤‡ä»½æ–‡ä»¶ã€‚</font>
    <BR>
     
    </td>
    </tr>
~;
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=delete">åˆ é™¤æ®‹ç•™å¤‡ä»½æ–‡ä»¶</a></b>ã€€<font color=#990000>(ä¸ºäº†å®‰å…¨èµ·è§ï¼Œè¯·åŠæ—¶åˆ é™¤æ®‹ç•™å¤‡ä»½æ–‡ä»¶ï¼)</font><br>
     æ³¨æ„ï¼šä¸€èˆ¬å¤‡ä»½åˆ°æœ¬åœ°å®Œæˆåï¼Œåº”è¯¥ç›´æ¥åˆ é™¤æ®‹ç•™å¤‡ä»½æ–‡ä»¶ï¼Œé¿å…ä¸å¿…è¦çš„å®‰å…¨æ¼æ´ã€‚<BR><BR>
    </td>
    </tr>
    ~ if ($bakuptrue == 0);
    
    print qq~
    <tr>
    <td colspan=2>
    <hr>
    <br>
    <div align=center>ä½¿ç”¨è¯´æ˜<br></div>
    <p>
    &nbsp&nbsp&nbsp&nbspæœ¬ç¨‹åºçš„ç›®çš„æ˜¯ä¸ºäº†è§£å†³ç”±äºæ–‡ä»¶å°ºå¯¸è¿‡å°è€Œå¯¼è‡´çš„è®ºå›æ•°æ® ä¸Šä¼ ã€ä¸‹è½½ æ•ˆç‡ä½ä¸‹çš„é—®é¢˜ã€‚<p>
    &nbsp&nbsp&nbsp&nbspè¯·åœ¨ä½¿ç”¨å‰æ³¨æ„ä»¥ä¸‹å‡ ç‚¹ï¼š<p>
    <table width=70% align=center>
    <tr>
    <td>
    1ã€åŸºæœ¬å˜é‡è®¾ç½®ä¸­ï¼Œè·¯å¾„çš„é…ç½®æ˜¯å¦ä½¿ç”¨ç»å¯¹è·¯å¾„ã€‚å¦‚æœæ²¡æœ‰ï¼Œè¯·æ”¹æˆç»å¯¹è·¯å¾„ã€‚
    <p>
    2ã€$lbdir <br> $imagesdir <br>${lbdir}backup/ <br>ä¸‰ä¸ªç›®å½•æ˜¯å¦è®¾ç½®æˆå¯å†™ã€‚å¦‚æœæ²¡æœ‰ï¼Œè¯·è®¾ä¸ºå¯å†™ã€‚
    <p>
    3ã€åœ¨ç¨‹åºå¤‡ä»½æˆ–è¿˜åŸçš„æ“ä½œä¸­ï¼Œä¸è¦å› ä¸ºç¨‹åºçš„è‡ªåŠ¨åˆ·æ–°è€Œå…³é—­æµè§ˆå™¨ï¼Œæ­¤æ—¶ç¨‹åºæ­£åœ¨è¿›è¡Œã€‚
    <p>
    4ã€å¦‚æœåœ¨ç¨‹åºæ‰§è¡Œçš„è¿‡ç¨‹ä¸­å‡ºç°ç™½å±ã€æˆ–å±å¹•ä¸Šæ˜¾ç¤º time out ã€memory out ç­‰å­—æ ·ï¼Œä¸è¦æƒŠæ…Œï¼Œè¯·è¯•ç€è°ƒæ•´ä¸€ä¸‹å‚æ•°ï¼Œé€šå¸¸éƒ½å¯ä»¥è§£å†³ã€‚
    <p>
    </td>
    </tr>
    </table>
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2 align=center>
    <p><p>
    <hr>
    <font color=#333333><a href=$thisprog?action=restore>--[è¿˜åŸ]--</a>&nbsp&nbsp&nbsp<a href=$thisprog?action=select>--[å¤‡ä»½]--
    <hr>
    <p><p>
    </td>
    </tr>

~;
}
sub memberoptions1 {
print qq~
    <form action="$thisprog" method=post name=form>
    <input type=hidden name="action" value="prebackup">
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>è¯·é€‰æ‹©ä½ è¦å¤‡ä»½çš„å†…å®¹</b>
    </td>
    </tr>
  ~;      

print qq~    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    
                    <font color=red>è¯·é€‰æ‹©è¦å¤‡ä»½çš„ç³»ç»Ÿæ•°æ®èµ„æ–™ï¼š</font>
                    <hr>
                    <p> 
                      <input type="checkbox" name="dirtoopen" value="memdir">ç”¨æˆ·èµ„æ–™æ–‡ä»¶&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="message">ç”¨æˆ·çŸ­æ¶ˆæ¯æ–‡ä»¶&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="avatar">ç”¨æˆ·è‡ªå®šä¹‰å¤´åƒ&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="system">ç³»ç»Ÿé…ç½®æ–‡ä»¶
                      
                    <p><font color=red>è¯·é€‰æ‹©è¦å¤‡ä»½çš„ç‰ˆé¢ï¼š</font><hr>
    ~;
my $filetoopen = "$lbdir" . "data/allforums.cgi";
flock(FILE, 2) if ($OS_USED eq "Unix");
open(FILE, "$filetoopen");
my @forums = <FILE>;
close(FILE);                 
$ii=0;
print "<table width=97% align=center>";
foreach my $forum (@forums) { #start foreach @forums
    chomp $forum;
    next if ($forum eq "");
    (my $forumid, my $category, my $categoryplace, my $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp) = split(/\t/,$forum);
print "<tr>" if ($ii==0);
print qq~
<td width=33%>
<input type="checkbox" name="dirtoopen" value="forum$forumid">
                      $forumname</p>
</td>
~; 
print "</tr>" if ($ii==2);
if ($ii<2)
{$ii++;} else {$ii=0;}
}
print "</table>";                      
    print qq~
                     
                    <hr>
                    <div align=center><input type="checkbox" name="attachement" value="yes" checked>åŒæ—¶å¤‡ä»½å¸–å­ä¸­æ‰€åŒ…å«é™„ä»¶æ–‡ä»¶&nbsp&nbsp&nbsp<input type="checkbox" name="packall" value="yes" checked>æ±‡æ€»æˆä¸€ä¸ªå¤§åŒ…ä¸‹è½½<br>
                    
                    <font color=red>(æ¨èä½¿ç”¨æ±‡æ€»æ‰“åŒ…ï¼Œå¦‚æœå› ä¸ºä½ çš„æœåŠ¡å•†æä¾›çš„èµ„æºé—®é¢˜ï¼Œæˆ–ç”±äºè®ºå›ç‰ˆé¢èµ„æ–™è¿‡å¤šå¼•èµ·çš„æ— æ³•è¿›è¡Œï¼Œè¯·å–æ¶ˆè¯¥é¡¹)</font>                  
                    </div>
                    *å°æŠ€å·§ï¼šè¯·æ ¹æ®ä½ çš„å®é™…æƒ…å†µé€‰å–ä¸€æ¬¡æ‰“åŒ…çš„å¤šå°‘ã€æ˜¯å¦æ±‡æ€»ã€è°ƒæ•´åˆ†åŒ…æ•°æ®ç­‰ã€‚å¤šè°ƒæ•´å‡ æ¬¡ï¼Œå¿…ç„¶å¯ä»¥æˆåŠŸå¤‡ä»½ã€‚
                    
                    <hr>
                    åˆ†åŒ…é™åˆ¶(æ¯ä¸ªåˆ†åŒ…ä»…åŒ…å«ä»¥ä¸‹ä¸€ä¸ªé¡¹ç›®)ï¼š<br>
                    <input type=text size=4 name="fn" value="500">ä¸ªå¸–å­æ–‡ä»¶&nbsp&nbsp<input type=text size=4 name="an" value="50">ä¸ªé™„ä»¶æ–‡ä»¶&nbsp&nbsp<input type=text size=4 name="mn" value="500">ä¸ªç”¨æˆ·èµ„æ–™æ–‡ä»¶&nbsp&nbsp<input type=text size=4 name="un" value="50">ä¸ªç”¨æˆ·è‡ªå®šä¹‰å¤´åƒæ–‡ä»¶&nbsp&nbsp<input type=text size=4 name="mgn" value="500">ä¸ªçŸ­æ¶ˆæ¯æ–‡ä»¶<br>
                    <font color=red>(è¿™ä¸ªæ˜¯ç”¨æ¥è®¾ç½®æ¯ä¸ªåˆ†å‹ç¼©åŒ…ä¸­åŒ…å«æ–‡ä»¶æ•°é‡çš„ï¼Œè¯·æ ¹æ®è‡ªå·±çš„æœåŠ¡å™¨è®¾ç½®ï¼Œé€šå¸¸ç¼ºçœå³å¯)</font>
                    <hr>
                    <div align=center>
                      <input type="submit" name="Submit" value="å¤‡ä»½æ–‡ä»¶å¤„ç†">
                      <input type="reset" name="Submit2" value="é‡æ–°é€‰æ‹©">
                    </div>
                    </p>
    
    </td>
    </tr>                
                  </form>
    ~;
    

}

sub prebackup {
	
print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        <b>æ‰“åŒ…å¤‡ä»½å‡†å¤‡</b><p>
~;        	
        chdir $lbdir;
        
        if (-e "tarfilelist.txt") {unlink("tarfilelist.txt");}
        @del=glob("backup*.temp");
        foreach(@del)
        {
        unlink("$_");
        }
        
@avatardata=();
@systemdata=();
@emoticondata=();
@attachedata=();
@memberdata=();
@msgdatain=();
@msgdataout=();

$step="unknow";

if ($dirtoopen[0] eq "memdir")
{
chdir "$lbdir$memberdir/old/";
@memberdata=glob("*");
shift(@dirtoopen);
chdir $lbdir;
$step="member";
}

if ($dirtoopen[0] eq "message")
{
chdir "${lbdir}$msgdir/in";
@msgdatain=glob("*");

chdir "${lbdir}$msgdir/out";
@msgdataout=glob("*");

shift(@dirtoopen);
chdir $lbdir;
$step="msgin" if ($step eq "unknow");
}

if ($dirtoopen[0] eq "avatar")
{
chdir "${imagesdir}usravatars";
@avatardata=glob("*");
shift(@dirtoopen);
chdir $lbdir;
$step="avatar" if ($step eq "unknow");
}

if ($dirtoopen[0] eq "system")
{
chdir "${lbdir}data";

# ä¿®æ­£ by maiweb begin
    	@systemdata=glob("*\.*");     
    	foreach $adas(@systemdata){
        next if ($adas=~/\./);
        @temp223=glob("$adas/*");
        push(@systemdata,@temp223);
        }# ä¿®æ­£ By maiweb end
shift(@dirtoopen);
chdir $lbdir;
$step="system" if ($step eq "unknow");
}

if ($dirtoopen[0	
print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        <b>\n";
        }
        close(FILE);
        }
                         
        if ($#msgdatain>=0)
        {
        open(FILE,">backupmsgin.temp");
        foreach(@msgdatain)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if ($#msgdataout>=0)
        {
        open(FILE,">backupmsgout.temp");
        foreach(@msgdataout)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if ($#memberdata>=0)
        {
        open(FILE,">backupmember.temp");
        foreach(@memberdata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }

        if($#emoticondata>=0)
        {
        open(FILE,">backuptopic.temp");
        foreach(@emoticondata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if($#attachedata>=0)
        {
        open(FILE,">backupattachement.temp");
        foreach(@attachedata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if ($atotal<=0) {$aa=0;} else {$aa=$atotal;}
        if ($ttotal<=0) {$bb=0;} else {$bb=$ttotal;}
        if ($#memberdata<0) {$cc=0;} else {$cc=$#memberdata+1;}
        if ($#systemdata<0) {$dd=0;} else {$dd=$#systemdata+1;}
        if ($#avatardata<0) {$ee=0;} else {$ee=$#avatardata+1;}
        if ($#msgdatain<0) {$ff=0;} else {$ff=$#msgdatain+1;}
        if ($#msgdataout<0) {$gg=0;} else {$gg=$#msgdataout+1;}
        
        $totalnum=$aa+$bb+$cc+$dd+$ee+$ff+$gg;       
        
        my $time=time;
        $current_time=$time;
        $time=crypt($time,"lb");
        $time=~s /\///isg;
        $time=~s /\.//isg;
        $tarname=$time;        
        $current_time = &dateformatshort($current_time + ($timezone*3600) + ($timedifferencevalue*3600));

       chdir "${lbdir}data";
        
        
        chdir $imagesdir;
        open (FILE,">tarfilelist.txt");
        print FILE "±¸·İÊ±¼ä£º\t$current_time\n";
        print FILE "ÎÄ¼şÃû£º\t$tarname\n";
        print FILE "´Ë´Î±¸·İ×ÜÎÄ¼şÊı:\t$totalnum\n";     
        print FILE "ÓÃ»§×ÊÁÏÎÄ¼şÊı:\t$cc\n";
        print FILE "ÓÃ»§×Ô¶¨ÒåÍ·ÏñÊı:\t$ee\n";
        print FILE "ÏµÍ³ÅäÖÃÎÄ¼şÊı:\t$dd\n";
        print FILE "Ìù×ÓÎÄ¼şÊı:\t$bb\n";
        print FILE "¸½¼şÎÄ¼şÊı:\t$aa\n";
        print FILE "¶ÌÏûÏ¢·¢¼şÏäÎÄ¼şÊı:\t$ff\n";
        print FILE "¶ÌÏûÏ¢ÊÕ¼şÏäÎÄ¼şÊı:\t$gg\n";
        print FILE "\n\n\n";  #ÎªÒÔºóÔ¤Áô
        print FILE "±¸·İµÄÂÛÌ³ÈçÏÂ£º\n";
#########È¡ÂÛÌ³Ãû
       open(FILE1, "${lbdir}/data/allforums.cgi");
       flock(FILE1, 1) if ($OS_USED eq "Unix");
       my @forums = <FILE1>;
       close(FILE1);

                        
     
        if ($#forumtotar>=0)
        {
        foreach $forumtotar (@forumtotar)
        {
        foreach $forum (@forums) { #start foreach @forums
         chomp $forum;
         next if ($forum eq "");
       (my $forumid, my $category, my $categoryplace, $forumname, my $forumdescription, my $tmp , $tmp , $tmp , $tmp,  $tmp , $tmp , $tmp,  $tmp,  $tmp,  $tmp, $tmp, $tmp, $tmp,my $hiddenforum,$tmp) = split(/\t/,$forum);
         my $tfu="forum".$forumid;
         if ($forumtotar eq $tfu) {last;}
        } 
        
        print FILE "$forumtotar";
        print FILE "\t";
        print FILE "$forumname";
        print FILE "\n";
        }
        }
        print FILE "ÇëÎñ±Ø±£³Ö°üÎÄ¼şÍêÕû¡£¡£²»Òª¸Ä¶¯±¾ÎÄ¼ş";
        close(FILE);
        chdir $lbdir;


        if ($step ne "unknow")
        {
        print qq~
        </td></tr>
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=red><div align=center>ËùÓĞÎÄ¼ş±¸·İ×¼±¸½áÊø£¡</div></font>
       <p>
       ´Ë´Î±¸·İ¹²ÓĞ $totalnum ¸öÎÄ¼ş:
       <p>
       ÓÃ»§×ÊÁÏÎÄ¼ş $cc ¸ö<br>
       ¶ÌÏûÏ¢·¢¼şÏäÎÄ¼ş $ff ¸ö<br>
       ¶ÌÏûÏ¢ÊÕ¼şÏäÎÄ¼ş $gg ¸ö<br>
       ÓÃ»§×Ô¶¨ÒåÍ·Ïñ $ee ¸ö<br>
       ÏµÍ³ÅäÖÃÎÄ¼ş $dd¸ö<br>
       Ìù×ÓÎÄ¼ş $bb ¸ö<br>
       ¸½¼şÎÄ¼ş $aa ¸ö
       <p>
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="backup">
       <input type=hidden name="fn" value="$fn">
       <input type=hidden name="packall" value="$packall">
       <input type=hidden name="an" value="$an">
       <input type=hidden name="mn" value="$mn">
       <input type=hidden name="un" value="$un">
       <input type=hidden name="mgn" value="$mgn">     
       <input type=hidden name="step" value="$step">
       <input type=hidden name="ttarnum" value="1">
       <input type=hidden name="atarnum" value="1">
       <input type=hidden name="mtarnum" value="1">
       <input type=hidden name="utarnum" value="1">
       <input type=hidden name="totalnum" value="$totalnum">
       <input type=hidden name="currentnum" value="0">
       <input type=hidden name="tarname" value="$tarname">
       <input type=hidden name="attachement" value="$attachement">
       <input type="submit" name="Submit" value="±¸·İÎÄ¼ş">
      </p>

        </td></tr>
         ~;
        }
        else
        {
        
        print qq~
        <p>
        <div align=center><font color=red>
        ÇëÖÁÉÙÑ¡ÔñÒ»¸ö±¸·İÏîÄ¿.....
        </font></div>
        </td></tr></tr>
        ~;
        
        }
         
     } # end routine


sub backup
{
print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        
        ~;
       chdir $lbdir;
       
    if (($step eq "member")&&(-e "backupmember.temp"))  #member backup
        {
        @untarname=();
        chdir $lbdir;
        open(FILE,"backupmember.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$mn);
        
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "$lbdir$memberdir/old";#ĞŞÕı By maiweb
        
        if ($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}m_$ttarnum.tar");
        $ttarnum++;
        }
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">backupmember.temp");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        $step="member";
        print qq~
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>ÓÃ»§×ÊÁÏ±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>        
        ~;
        $step="msgin";    
        $ttarnum=1;
        }   
        goto COMEON;
        chdir $lbdir;
        }
       else
        {
        $step="msgin" if ($step eq "member")
        }
#############################################

print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        
        ~;
       chdir $lbdir;
       
    if (($step eq "msgin")&&(-e "backupmsgin.temp"))  #member backup
        {
        @untarname=();
        chdir $lbdir;
        open(FILE,"backupmsgin.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$mgn);
        
        $currentnum=($#untarname>=0)?$currentnum+$mgn:$currentnum+$#filename;
        chdir "${lbdir}$msgdir/in";
        
        if ($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}gin_$ttarnum.tar");
        $ttarnum++;
        }
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">backupmsgin.temp");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        $step="msgin";
        print qq~
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>¶ÌÏûÏ¢×ÊÁÏ±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>        
        ~;
        $step="msgout";    
        $ttarnum=1;
        }   
        goto COMEON;
        chdir $lbdir;
        }
       else
        {
        $step="msgout" if ($step eq "msgin")
        }

#############################################

print qq~
        <tr>
       <tr>
        <td bgcolor=#FFFFFF align=left colspan=2>
        <font color=#990000>
                    
        
        ~;
       chdir $lbdir;
       
    if (($step eq "msgout")&&(-e "backupmsgout.temp"))  #member backup
        {
        @untarname=();
        chdir $lbdir;
        open(FILE,"backupmsgout.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$mgn);
        
        $currentnum=($#untarname>=0)?$currentnum+$mgn:$currentnum+$#filename;
        chdir "${lbdir}$msgdir/out";
        
        if ($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}gout_$ttarnum.tar");
        $ttarnum++;
        }
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">backupmsgout.temp");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        $step="msgout";
        print qq~
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>¶ÌÏûÏ¢×ÊÁÏ±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>        
        ~;
        $step="avatar";    
        $ttarnum=1;
        }   
        goto COMEON;
        chdir $lbdir;
        }
       else
        {
        $step="avatar" if ($step eq "msgout")
        }







        #####################################
        
       if (($step eq "avatar")&&(-e "backupavatar.temp"))  #member backup
        {
        @untarname=();
        chdir $lbdir;
        open(FILE,"backupavatar.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$un);
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "${imagesdir}usravatars";
        
        if ($#filename>0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}u_$ttarnum.tar");
        }
        
        $ttarnum++;
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">backupavatar.temp");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        $step="avatar";
        print qq~
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>ÓÃ»§×Ô¶¨ÒåÍ·ÏñÎÄ¼ş±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
        $step="system";    
        $ttarnum=1;
        }   
        $skip=1;
        chdir $lbdir;
        goto COMEON;
        }
        else
        {
        $step="system" if ($step eq "avatar")
        }

        
        
        #####################################
        
       if (($step eq "system")&&(-e "backupsystem.temp"))  #member backup
        {
        chdir $lbdir;
        open(FILE,"backupsystem.temp");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=();
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "${lbdir}data";
        if($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}s.tar");
        }
        chdir $lbdir;

      
print qq~
        <p>
        <font color=red><div align=center>ÏµÍ³ÅäÖÃÎÄ¼şÎÄ¼ş±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
                

        chdir $lbdir;
        $step="topic";
        goto COMEON;
        }
        else
        {
        $step="topic" if ($step eq "system");
        }
        
        
        
        #####################################
        if (($step eq "topic")&&(-e "backuptopic.temp"))  #topic backup
        {

        @untarname=();
        chdir $lbdir;
     ################# È¡ÎÄ¼şÁĞ±í
        open(FILE,"backuptopic.temp");
        @filelist=<FILE>;
        chomp @filelist;
        close(FILE);
        
        if ($#filelist>=0)
        
        {
        ($aa,$bb)=split(/\./,$filelist[0]);
        ($bb,$fid)=split(/\_/,$aa);
        open(FILE,"$filelist[0]");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$fn);
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "${lbdir}forum${fid}";
        if($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}t_${fid}_${ttarnum}.tar");
        }
        $ttarnum++;
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">$filelist[0]");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);

        print qq~
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
          } #end if $#untarname>=0
         else
         {
        open(FILE,"backuptopic.temp");
        @filelist=<FILE>;
        chomp @filelist;
        close(FILE);
        shift(@filelist);
        if ($#filelist>=0)
        {
        open(FILE,">backuptopic.temp");
        foreach(@filelist)
        {
          print FILE "$_";
          print FILE "\n";
        }
        close(FILE);
        $ttarnum=1;
         print qq~
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
        }
        else 
          {
        chdir "${lbdir}boarddata";
        @filename =();
	@data1=glob("list${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("xzb${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("xzbs${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("ontop${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("lastnum${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
	@data1=glob("jinghua${fid}.cgi");
	push (@filename, @data1) if($#data1>=0);
#        my $ttarnum1 =$ttarnum-1;
        if($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}t_${fid}_${ttarnum}.tar");
        }
          	$step="attachement";          
              print qq~
             <p>
             <font color=red><div align=center>ÂÛÌ³Ìù×Ó×ÊÁÏ±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
             <p>
             <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;   
          }
         }
         
         }#end if filelist>=0
        else
        {
        $step="attachement";          
        print qq~
        <p>
        <font color=red><div align=center>ÂÛÌ³Ìù×Ó×ÊÁÏ±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;       
        }
        chdir $lbdir;
        goto COMEON;
        }
        else
        {
        $step="tarall" if ($step eq "topic")
        }
        


        ############################

        if (($step eq "attachement")&&(-e "backupattachement.temp")&&($attachement eq "yes"))  #attachement backup
        {
        @untarname=();
        chdir $lbdir;
        
        open(FILE,"backupattachement.temp");
        @filelist=<FILE>;
        chomp @filelist;
        close(FILE);
        
        if ($#filelist>=0)
        
        {
        
        ($aa,$bb)=split(/\./,$filelist[0]);
        ($bb,$fid)=split(/\_/,$aa);
        
        open(FILE,"$filelist[0]");
        @filename=<FILE>;
        chomp @filename;
        close(FILE); 
        @untarname=splice(@filename,$an);
        $currentnum=($#untarname>=0)?$currentnum+$mn:$currentnum+$#filename;
        chdir "${imagesdir}$usrdir/$fid";       
        if ($#filename>=0)
        {
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}${tarname}a_${fid}_${atarnum}.tar");
        }
        $atarnum++;
        chdir $lbdir;
        if ($#untarname>=0)
        {
        open(FILE,">$filelist[0]");
        foreach(@untarname)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        
        print qq~
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
        } # end untarname>=0
        else
        {
        open(FILE,"backupattachement.temp");
        @filelist=<FILE>;
        chomp @filelist;
        close(FILE);
        shift(@filelist);
        if ($#filelist>=0)
        {
        open(FILE,">backupattachement.temp");
        foreach(@filelist)
        {
          print FILE "$_";
          print FILE "\n";
        }
        close(FILE);
        $atarnum=1;
         print qq~
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;
        }
        else 
          {
          	$step="tarall";
          	$skip="yes";          
              print qq~
             <p>
             <font color=red><div align=center>ÂÛÌ³Ìù×Ó¸½¼ş±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
             <p>
             <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;   
          }
         }
        
         }# end filelist
        else
        {
        
        $step="tarall";
        $skip="yes";
        print qq~
        <p>
        <font color=red><div align=center>ÂÛÌ³Ìù×Ó¸½¼ş±¸·İÍê±Ï¡£¡£Çë¼ÌĞø</div></font>
        <p>
        <div align=center>³ÌĞòÔÚ2Ãë»á×Ô¶¯½øĞĞ£¬Èç¹ûä¯ÀÀÆ÷Ã»ÓĞ×Ô¶¯ÏòÇ°½øĞĞ£¬Çëµã»÷ ¼ÌĞø±¸·İÎÄ¼ş °´Å¥</div>
        ~;       
        }
        chdir $lbdir;
        }
       else
        {
        $step="tarall" if ($step eq "attachement")
        }

COMEON:{
        ###################################3
        if (($step eq "tarall")&&($skip ne "yes"))  #make together
        {
        chdir $lbdir;
        @filetodel=glob("back*.temp");
        foreach(@filetodel) {unlink("$_");}
        
               
        if($packall eq "yes")                                                                               
        {
        chdir $imagesdir;
        @filename=glob("${tarname}*.tar");
        unshift(@filename,"tarfilelist.txt");
        $tar = Archive::Tar->new();
        $tar->add_files(@filename);
        $tar->write("${imagesdir}xq${tarname}.tar");
        foreach(@filename)
        {
        unlink("$_");
        }
        if (-e "tarfilelist.txt") {unlink("tarfilelist.txt");}
 
 print qq~     
        <a href=$imagesurl/xq${tarname}.tar>µãÕâ¶ùÏÂÔØµ½±¾µØ</a><br>
        <a href=$thisprog?action=delete>µãÕâ¶ùÉ¾³ı±¸·İ<font color=red>Îñ±Ø²Ù×÷</font></a><Br>
~;        
        }
        else
        {
         chdir $imagesdir;
        @filename=glob("${tarname}*.tar");
        unshift(@filename,"tarfilelist.txt");
       
        foreach $fn (@filename)
         {
             print "<a href=$imagesurl/$fn>ÎÄ¼ş $fn µãÕâ¶ùÏÂÔØµ½±¾µØ</a><br>";
         }
         $nn=$#filename+1;
         print "<p><div align=center><font color=red>¹²ÓĞ $nn ¸öÎÄ¼ş¡£ÇëÏÂÔØºóÍ³Ò»±£¹Ü£¬ÎğË½×Ô¸Ä¶¯ÆäÖĞÄÚÈİ»òÎÄ¼şÃû¡£»Ö¸´Ê±Ò»²¢ÉÏ´«</font></div><p>";       
         print "<a href=$thisprog?action=delete>µãÕâ¶ùÉ¾³ı±¸·İ<font color=red>Îñ±Ø²Ù×÷</font></a><Br>";
         print qq~</div>~;
        }
        
        
        
        }

        else
        {

$percent=int(($currentnum/$totalnum)*100);
$percent1=int(100-$percent);


print qq~
       <b>±¸·İÖĞ¡£¡£¡£¡£¡£</b><p>
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="backup">
       <input type=hidden name="fn" value="$fn">
       <input type=hidden name="an" value="$an">
       <input type=hidden name="mn" value="$mn">
       <input type=hidden name="un" value="$un">
       <input type=hidden name="mgn" value="$mgn">
       <input type=hidden name="step" value="$step">
       <input type=hidden name="ttarnum" value="$ttarnum">
       <input type=hidden name="packall" value="$packall">
       <input type=hidden name="atarnum" value="$atarnum">
       <input type=hidden name="mtarnum" value="$mtarnum">
       <input type=hidden name="utarnum" value="$utarnum">
       <input type=hidden name="tarname" value="$tarname">
       <input type=hidden name="currentnum" value="$currentnum">
       <input type=hidden name="totalnum" value="$totalnum">
       <input type=hidden name="attachement" value="$attachement">
       <div align=center><input type="submit" name="Submit" value="¼ÌĞø±¸·İÎÄ¼ş"></div>
       </p>
      
       <div align=center>
       <b>±¸·İ½ø¶È</b><br>
       (±¸·İ½ø¶ÈÌåÏÖµÄÊÇÒÔ±¸·İÎÄ¼şÔÚ×ÜÎÄ¼şÊıÖĞµÄ±ÈÀı,²»ÄÜÒÔ´Ë×÷Îª±¸·İ»¨·ÑÊ±¼äµÄÍÆ¶Ï)
       <table width=80% board=0 height=20>
       <tr>
       <td width=$percent% bgcolor=blue></td>
       <td width=$percent1%></td>
       </tr>
       </table>
       
       </div>
        <script>
        setTimeout('document.form.submit()',2000);
        </script>
        ~;
        }


}


print qq~     
       
        </td>
       </tr>
       </tr>
      ~;   



}

sub delete {
   $dirtoopen = "${imagesdir}";
    opendir (DIR, "$dirtoopen"); 
    @filedata = readdir(DIR);
    closedir (DIR);

    @sortedfile = grep(/\.tar$/,@filedata);
    
    foreach $backupfile (@sortedfile){
    
    if (-e "${imagesdir}$backupfile") {
     unlink "${imagesdir}$backupfile";
     print "<tr><td bgcolor=#FFFFFF align=left colspan=2>É¾³ı²ĞÁô±¸·İÎÄ¼ş${imagesdir}$backupfile³É¹¦!<br></td></tr>";
    }
}
if (-e "${imagesdir}tarfilelist.txt") {
     unlink "${imagesdir}tarfilelist.txt";
     print "<tr><td bgcolor=#FFFFFF align=left colspan=2>É¾³ı²ĞÁô±¸·İÎÄ¼ş${imagesdir}tarfilelist.txt³É¹¦!<br></td></tr>";
    }
print qq~
<tr><td bgcolor=#FFFFFF align=left colspan=2>
<b>²ĞÁô±¸·İÎÄ¼şÒÑ¾­È«²¿É¾³ı!</b>
</td></tr>
~;

}

print qq~</td></tr></table></body></html>~;
exit;
