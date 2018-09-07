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
# 2005-07-1 maiweb 大修正 -------- For leobbs 0926 以后的版本
# 1，修正会员资料备份、恢复Bug ------仅仅备份 old目录下面的内容
# 2，修正多附件多目录备份bug
# 3，板块帖子恢复之后，需要进入后台重新统计一次！
# 4，修正系统配置备份完全
BEGIN {
    $startingtime=(times)[0]+(times)[1];
    foreach ($0,$ENV{'PATH_TRANSLATED'},$ENV{'SCRIPT_FILENAME'}){
    	my $LBPATH = $_;
    	next if ($LBPATH eq '');
    	$LBPATH =~ s/\\/\//g; $LBPATH =~ s/\/[^\/]+$//o;
        unshift(@INC,$LBPATH);
    }
}

use strict;
use strict;
use warnings;
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

##########恢复变量
@restorelist=        $query-> param('restorelist');
$toopen=        $query-> param('toopen');

if ($memdir ne "")
 {$memberdir=$memdir;} elsif ($memberdir eq "") {$memberdir="members";}

&getadmincheck;
print header(-charset=>"UTF-8" , -expires=>"$EXP_MODE" , -cache=>"$CACHE_MODES");
&admintitle;
        
&getmember("$inmembername","no");
        
        if (($membercode eq "ad") && ($inpassword eq $password) && (lc($inmembername) eq lc($membername))) {
            
            print qq~
            <tr><td bgcolor=#2159C9 colspan=2><font color=#FFFFFF>
            <b>欢迎来到论坛管理中心 / 论坛数据备份</b>
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
    <font color=#990000><b>请输入你要还原的备份文件名称</b>    
    </td>
    </tr>
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <div align=center><font color=#333333><BR>请输入你要还原的备份文件名称，并且确认你已经用FTP上传到你的$lbdir当前目录！ <br><br><B><input type=input size=40 name="dirtoopen" value="xqlb.tar"></B><p></div>
    >***如果你要还原的项目，打包时未选取<font color=blue>汇总打包</font>选项，请将所有的下载文件置于你的$lbdir当前目录，并在输入框中输入<font color=blue>tarfilelist.txt</font>***
    <br><Br>
    <div align=center>
    <input type="checkbox" name="oldversion" value="yes"><font color=red>旧版本解包</font><br>
    如果你的文件包不是使用新版本备份程序制作的，请务必选取此项）
    <p>
    <input type="submit" name="Submit" value="确认还原备份"></div>
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
      #################### 未汇总处理 ##   
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
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopen不能读取，请检查是否使用二进制模式上传(一定要这个模式上传这个压缩包)</td></tr>~;
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
                  
       ################## 读取包信息
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
       	$showmember="<input type='checkbox' name='restorelist' value='memdir'>用户资料文件";
       	}
       if ($havemsg1>0)
       {
       $showmsg="<input type='checkbox' name='restorelist' value='msg'>短消息文件";
       }
       if ($havemsg2>0)
       {
       $showmsg="<input type='checkbox' name='restorelist' value='msg'>短消息文件";
       }
       if ($haveavatar>0)
       {
       	$showavatar="<input type='checkbox' name='restorelist' value='avatar'>用户自定义头像";
       	}
       if ($havesystem>0)
       {
       $showsystem="<input type='checkbox' name='restorelist' value='system'>系统配置文件";
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
          $showforum=$showforum."<td><p><input type='checkbox' name='restorelist' value=$forumid>${forumname}</td><td>还原至$forumid号版面</td>";
          $showforum.="</tr>" if ($ii==2);
          $ii=($ii>2)?0:++$i;
        }
        $showforum.="</table>";
        }
        else
        {
        $showforum="<p>该包中没有备份论坛版面贴子<p>";
        }
      if($haveattachement>0)
       {
       $showattachement="<input type='checkbox' name='restorelist' value='attachement' checked>还原版面同时恢复该版面附件<br>"
       }
       else
       {
       $showattachement="该包中没有备份论坛版面贴子附件";
       }
       
      print qq~
       <form action="$thisprog" method=post name=form>
       <input type=hidden name="action" value="untar">
        <tr>
        <td bgcolor=#EEEEEE align=center colspan=2>
        <font color=#990000><b>请选择你要还原的项目</b>
        <p>
        备份时间:$tartime
        </td>
        </tr>          
        
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <p>
    <font color=red>系统数据：</font>
    <hr>
    $showmember &nbsp $showmsg &nbsp $showavatar &nbsp $showsystem
    <p>
    <font color=red>需要恢复的版面</font>
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
                <input type="submit" name="Submit" value="恢复文件预处理">
                <input type="reset" name="Submit2" value="重新选择">
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
    无法找到索引文件.(出错原因:很有可能这个文件不是使用本版本打包....!或者.文件被更改过) 
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
    备份资料没找到找到，请检查输入的文件名和是否已经上传！
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
        <font color=#990000><b>解包预处理</b>
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
               	      if ($fl =~ m/$a/) {push(@needtotar,"$fl\t${lbdir}${memberdir}/old");# 修正by maiweb
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
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopen不能读取，请检查是否使用二进制模式上传(一定要这个模式上传这个压缩包)</td></tr>~;
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
             if  (-e "$isok")  {$status.="$isok 分包成功<br>";} else {$status.="$isok 分包<font color=blue>未成功</font>。请检查是否使用二进制模式上传！<br>";$error="yes";}   
             if  (opendir(DIR,"$dirname")) {$status.="$dirname 存在<br>";} 
                   else {$status.="$dirname <font color=blue>不存在</font>";
                         if (mkdir("$dirname",777)) {
							 chmod(0777,"$dirname");
							 $status.="&nbsp 目录创建成功<br>";}
                            else{$status.="&nbsp目录创建失败<br>";$error="yes";}                         
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
          <div align=center>预处理完毕</div>
          <p>
          ~;
           if ($error eq "yes")
           {
             print qq~
          <p><font color=red>
          <div align=center>预处理错误，请根据错误提示，重新检查一遍。</font>
          </td></tr>
          ~;
          exit;
           
           }
           
           
           
           
         }
         else
         {
         print qq~
         <p><font color=red>
         <div align=center>预处理错误，请返回，重试一遍。</font>
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
                <input type="submit" name="Submit" value="恢复文件">
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
        <font color=#990000><b>解包恢复中。。。。。</b>
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
           $status="${lbdir}$name还原完毕。";         
           unless ($tar->read("${lbdir}$name", 0)) {
	        print qq~
	        ${lbdir}$name不能读取，请检查是否使用二进制模式上传(一定要这个模式上传这个压缩包)
	        ~;
                $status="${lbdir}$name不能读取，请检查是否使用二进制模式上传(一定要这个模式上传这个压缩包)";

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
                <input type="submit" name="Submit" value="恢复文件">
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
                  <b>还原进度</b><br>
       (还原进度体现的是以还原文件在总文件数中的比例,不能以此作为还原花费时间的推断)
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
                <input type="submit" name="Submit" value="恢复文件">
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
        还原结束..状态如下:
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
    备份资料找到，现在开始还原！
</td>
</tr>
~;
{
        my $cwd = cwd();
        my $tar =  Archive::Tar->new();
        unless ($tar->read("${lbdir}$toopen", 0)) {
	        print qq~<td class='w' align='left' width='60%'>${lbdir}$toopen不能读取，请检查是否使用二进制模式上传(一定要这个模式上传这个压缩包)</td></tr>~;
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
    还原完成！
</td>
</tr>
~;
}else {
print qq~	
<tr>
    <td bgcolor=#FFFFFF colspan=2>
    备份资料没找到找到，请检查输入的文件名和是否已经上传！ 
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
    	$last_backup = "残留备份文件存在，请及时删除!";
           $bakuptrue = 0;
    }
    else {
           $last_backup = "残留备份文件没有找到，论坛安全";
           $bakuptrue = 1;
    }   


     
    print qq~
    <tr>
    <td bgcolor=#EEEEEE align=center colspan=2>
    <font color=#990000><b>请选择你要备份的内容</b>
    </td>
    </tr>          
        
                
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><BR>检查残留备份文件： <B>$last_backup</B><BR>
    <font color=red>本检查只搜索 $imagesdir 下是否有残存的备份文件。</font>
    <BR>
     
    </td>
    </tr>
~;
    print qq~
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    <font color=#333333><b><a href="$thisprog?action=delete">删除残留备份文件</a></b>　<font color=#990000>(为了安全起见，请及时删除残留备份文件！)</font><br>
     注意：一般备份到本地完成后，应该直接删除残留备份文件，避免不必要的安全漏洞。<BR><BR>
    </td>
    </tr>
    ~ if ($bakuptrue == 0);
    
    print qq~
    <tr>
    <td colspan=2>
    <hr>
    <br>
    <div align=center>使用说明<br></div>
    <p>
    &nbsp&nbsp&nbsp&nbsp本程序的目的是为了解决由于文件尺寸过小而导致的论坛数据 上传、下载 效率低下的问题。<p>
    &nbsp&nbsp&nbsp&nbsp请在使用前注意以下几点：<p>
    <table width=70% align=center>
    <tr>
    <td>
    1、基本变量设置中，路径的配置是否使用绝对路径。如果没有，请改成绝对路径。
    <p>
    2、$lbdir <br> $imagesdir <br>${lbdir}backup/ <br>三个目录是否设置成可写。如果没有，请设为可写。
    <p>
    3、在程序备份或还原的操作中，不要因为程序的自动刷新而关闭浏览器，此时程序正在进行。
    <p>
    4、如果在程序执行的过程中出现白屏、或屏幕上显示 time out 、memory out 等字样，不要惊慌，请试着调整一下参数，通常都可以解决。
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
    <font color=#333333><a href=$thisprog?action=restore>--[还原]--</a>&nbsp&nbsp&nbsp<a href=$thisprog?action=select>--[备份]--
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
    <font color=#990000><b>请选择你要备份的内容</b>
    </td>
    </tr>
  ~;      

print qq~    
    <tr>
    <td bgcolor=#FFFFFF colspan=2>
    
                    <font color=red>请选择要备份的系统数据资料：</font>
                    <hr>
                    <p> 
                      <input type="checkbox" name="dirtoopen" value="memdir">用户资料文件&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="message">用户短消息文件&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="avatar">用户自定义头像&nbsp&nbsp&nbsp
                      <input type="checkbox" name="dirtoopen" value="system">系统配置文件
                      
                    <p><font color=red>请选择要备份的版面：</font><hr>
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
                    <div align=center><input type="checkbox" name="attachement" value="yes" checked>同时备份帖子中所包含附件文件&nbsp&nbsp&nbsp<input type="checkbox" name="packall" value="yes" checked>汇总成一个大包下载<br>
                    
                    <font color=red>(推荐使用汇总打包，如果因为你的服务商提供的资源问题，或由于论坛版面资料过多引起的无法进行，请取消该项)</font>                  
                    </div>
                    *小技巧：请根据你的实际情况选取一次打包的多少、是否汇总、调整分包数据等。多调整几次，必然可以成功备份。
                    
                    <hr>
                    分包限制(每个分包仅包含以下一个项目)：<br>
                    <input type=text size=4 name="fn" value="500">个帖子文件&nbsp&nbsp<input type=text size=4 name="an" value="50">个附件文件&nbsp&nbsp<input type=text size=4 name="mn" value="500">个用户资料文件&nbsp&nbsp<input type=text size=4 name="un" value="50">个用户自定义头像文件&nbsp&nbsp<input type=text size=4 name="mgn" value="500">个短消息文件<br>
                    <font color=red>(这个是用来设置每个分压缩包中包含文件数量的，请根据自己的服务器设置，通常缺省即可)</font>
                    <hr>
                    <div align=center>
                      <input type="submit" name="Submit" value="备份文件处理">
                      <input type="reset" name="Submit2" value="重新选择">
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
                    
        <b>打包备份准备</b><p>
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

# 修正 by maiweb begin
    	@systemdata=glob("*\.*");     
    	foreach $adas(@systemdata){
        next if ($adas=~/\./);
        @temp223=glob("$adas/*");
        push(@systemdata,@temp223);
        }# 修正 By maiweb end
shift(@dirtoopen);
chdir $lbdir;
$step="system" if ($step eq "unknow");
}

if ($dirtoopen[0]=~m/forum/)
{
   $ttotal=0;
   $atotal=0;
   @forumtotar=@dirtoopen;
   foreach $dirtoopen (@dirtoopen){
    ($a,$b)=split(/m/,$dirtoopen);
    chdir "$lbdir$dirtoopen";
    @temp1=glob("*");      
    if (($dirtoopen=~m/forum/)&&($attachement eq "yes"))
    {   
    	chdir "${imagesdir}$usrdir/$b";
    	# 修正 by maiweb begin
    	@temp2=glob("$b\_*");     
    	my @alladad=glob("*");
    	foreach $adas(@alladad){
        next if ($adas=~/\_/);
        @temp223=glob("$adas/*");
        push(@temp2,@temp223);
        }# 修正 By maiweb end
    }
   chdir $lbdir;
   open(FILE,">backuptopic_$b.temp");
   foreach(@temp1)
        {
        print FILE "$_";
        print FILE "\n";
        }
   close(FILE);
   open(FILE,">backupattachement_$b.temp");
   foreach(@temp2)
        {
        print FILE "$_";
        print FILE "\n";
        }
   close(FILE);   
   ########计算贴子和附件数
   $ttotal=$#temp1+1+$ttotal;
   $atotal=$#temp2+1+$atotal;
   
   @emoticondata=(@emoticondata,"backuptopic_$b.temp");
   @attachedata=(@attachedata,"backupattachement_$b.temp");
   @temp1=();
   @temp2=();
   $step="topic" if ($step eq "unknow");
   }
}
        
        chdir $lbdir;
        
        if ($#systemdata>=0)
        {
        open(FILE,">backupsystem.temp");
        foreach(@systemdata)
        {
        print FILE "$_";
        print FILE "\n";
        }
        close(FILE);
        }
        
        if ($#avatardata>=0)
        {
        open(FILE,">backupavatar.temp");
        foreach(@avatardata)
        {
        print FILE "$_";
        print FILE "\n";
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
        print FILE "备份时间：\t$current_time\n";
        print FILE "文件名：\t$tarname\n";
        print FILE "此次备份总文件数:\t$totalnum\n";     
        print FILE "用户资料文件数:\t$cc\n";
        print FILE "用户自定义头像数:\t$ee\n";
        print FILE "系统配置文件数:\t$dd\n";
        print FILE "贴子文件数:\t$bb\n";
        print FILE "附件文件数:\t$aa\n";
        print FILE "短消息发件箱文件数:\t$ff\n";
        print FILE "短消息收件箱文件数:\t$gg\n";
        print FILE "\n\n\n";  #为以后预留
        print FILE "备份的论坛如下：\n";
#########取论坛名
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
        print FILE "请务必保持包文件完整。。不要改动本文件";
        close(FILE);
        chdir $lbdir;


        if ($step ne "unknow")
        {
        print qq~
        </td></tr>
        <tr>
        <td bgcolor=#FFFFFF align=center colspan=2>
        <font color=red><div align=center>所有文件备份准备结束！</div></font>
       <p>
       此次备份共有 $totalnum 个文件:
       <p>
       用户资料文件 $cc 个<br>
       短消息发件箱文件 $ff 个<br>
       短消息收件箱文件 $gg 个<br>
       用户自定义头像 $ee 个<br>
       系统配置文件 $dd个<br>
       贴子文件 $bb 个<br>
       附件文件 $aa 个
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
       <input type="submit" name="Submit" value="备份文件">
      </p>
        </td></tr>
         ~;
        }
        else
        {
        
        print qq~
        <p>
        <div align=center><font color=red>
        请至少选择一个备份项目.....
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
        chdir "$lbdir$memberdir/old";#修正 By maiweb
        
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
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>用户资料备份完毕。。请继续</div></font>
        <p>
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>        
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
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>短消息资料备份完毕。。请继续</div></font>
        <p>
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>        
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
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>短消息资料备份完毕。。请继续</div></font>
        <p>
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>        
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
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
        ~;
        }
        else
        {
print qq~
        <p>
        <font color=red><div align=center>用户自定义头像文件备份完毕。。请继续</div></font>
        <p>
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
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
        <font color=red><div align=center>系统配置文件文件备份完毕。。请继续</div></font>
        <p>
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
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
     ################# 取文件列表
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
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
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
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
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
             <font color=red><div align=center>论坛贴子资料备份完毕。。请继续</div></font>
             <p>
             <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
        ~;   
          }
         }
         
         }#end if filelist>=0
        else
        {
        $step="attachement";          
        print qq~
        <p>
        <font color=red><div align=center>论坛贴子资料备份完毕。。请继续</div></font>
        <p>
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
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
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
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
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
        ~;
        }
        else 
          {
          	$step="tarall";
          	$skip="yes";          
              print qq~
             <p>
             <font color=red><div align=center>论坛贴子附件备份完毕。。请继续</div></font>
             <p>
             <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
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
        <font color=red><div align=center>论坛贴子附件备份完毕。。请继续</div></font>
        <p>
        <div align=center>程序在2秒会自动进行，如果浏览器没有自动向前进行，请点击 继续备份文件 按钮</div>
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
        <a href=$imagesurl/xq${tarname}.tar>点这儿下载到本地</a><br>
        <a href=$thisprog?action=delete>点这儿删除备份<font color=red>务必操作</font></a><Br>
~;        
        }
        else
        {
         chdir $imagesdir;
        @filename=glob("${tarname}*.tar");
        unshift(@filename,"tarfilelist.txt");
       
        foreach $fn (@filename)
         {
             print "<a href=$imagesurl/$fn>文件 $fn 点这儿下载到本地</a><br>";
         }
         $nn=$#filename+1;
         print "<p><div align=center><font color=red>共有 $nn 个文件。请下载后统一保管，勿私自改动其中内容或文件名。恢复时一并上传</font></div><p>";       
         print "<a href=$thisprog?action=delete>点这儿删除备份<font color=red>务必操作</font></a><Br>";
         print qq~</div>~;
        }
        
        
        
        }

        else
        {

$percent=int(($currentnum/$totalnum)*100);
$percent1=int(100-$percent);


print qq~
       <b>备份中。。。。。</b><p>
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
       <div align=center><input type="submit" name="Submit" value="继续备份文件"></div>
       </p>
      
       <div align=center>
       <b>备份进度</b><br>
       (备份进度体现的是以备份文件在总文件数中的比例,不能以此作为备份花费时间的推断)
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
     print "<tr><td bgcolor=#FFFFFF align=left colspan=2>删除残留备份文件${imagesdir}$backupfile成功!<br></td></tr>";
    }
}
if (-e "${imagesdir}tarfilelist.txt") {
     unlink "${imagesdir}tarfilelist.txt";
     print "<tr><td bgcolor=#FFFFFF align=left colspan=2>删除残留备份文件${imagesdir}tarfilelist.txt成功!<br></td></tr>";
    }
print qq~
<tr><td bgcolor=#FFFFFF align=left colspan=2>
<b>残留备份文件已经全部删除!</b>
</td></tr>
~;

}

print qq~</td></tr></table></body></html>~;
exit;