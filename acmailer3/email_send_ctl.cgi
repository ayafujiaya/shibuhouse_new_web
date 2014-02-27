#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use clsMail;
use strict;
use MailSession;

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

&writing_check(\$SYS);

# ���å����ǡ��������ȥ���������å�
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

# �������̤����꤬�Ԥ��Ƥ��뤫�ɤ���
&CheckAdminData_MailSend($admindata);


# �᡼�륻�å����
my $mail_session = MailSession->new(
    mail_id     => $FORM{mail_session_id},
    session_dir => $SYS->{dir_session_mail}
);
$FORM{mail_title} = $mail_session->get('mail_title');
$FORM{mail_body} = $mail_session->get('mail_body');
$FORM{mail_title} =~ s/__<<equal>>__/\=/gi;
$FORM{mail_body} =~ s/__<<equal>>__/\=/gi;
$FORM{mail_title} =~ s/__<<semicolon>>__/;/gi;
$FORM{mail_body} =~ s/__<<semicolon>>__/;/gi;

# �����ѥǡ�������
if ($FORM{sid}) { $COOKIE{sid} = $FORM{sid}; }
my $objAcDataSender = new clsAcData($SYS->{dir_session});
my $sender_data = $objAcDataSender->getSenderData($mail_session->mail_id());


if ($sender_data eq "") {
	&error("�����褬����ޤ���");
}

if (!$FORM{mail_title}) { &error("��̾�����Ϥ��Ƥ���������"); }
if (!$FORM{mail_body}) { &error("��ʸ�����Ϥ��Ƥ���������"); }
$data_ref = $admindata;

# ͽ���ۿ��ξ��
if ($FORM{reserve_mode}) {
	# ͽ����֥����å�
	my %TIME = &getdatetime();
	if (!$FORM{send_year} || !$FORM{send_mon} || !$FORM{send_day} || $FORM{send_hour} eq "" || $FORM{send_min} eq "") { &error("ͽ���ۿ�������ξ����ۿ����������򤷤Ƥ���������"); }
	# ���ߤ����֤���ξ��
	if ("$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}" > sprintf("%04d%02d%02d%02d%02d", $FORM{send_year}, $FORM{send_mon}, $FORM{send_day}, $FORM{send_hour}, $FORM{send_min})) {
	#	&error("�ۿ����������꤬���ߤ����ˤʤäƤ��ޤ���");
	}
}

#��̾
$data_ref->{mail_title} = &plantext2html($FORM{mail_title},"nobr");
$data_ref->{mail_title_html} = &plantext2html($FORM{mail_title});

#��ʸ
$data_ref->{mail_body} = &plantext2html($FORM{mail_body},"nobr");
$data_ref->{mail_body_html} = &plantext2html($FORM{mail_body});

# ���������
my @DATA = split(/\n/, $sender_data);
my @data;
my $i;

foreach(@DATA){
	if (!$_) { next; }
	$_ =~ s/__<<equal>>__/\=/gi;
	$_ =~ s/__<<semicolon>>__/;/gi;
	my $row;
	
	my @d = split(/\t/,$_);
	my $col = $objAcData->{MAIL_COL};
	my @col = @$col;
	my $j = 0;
	foreach my $n (@col) {
		$row->{$n} = $d[$j];
		$j++;
	}
	
	# �ۿ���ߤ�̵��
	if (!$row->{status}) { next; }
	
	$row->{subject} = $FORM{mail_title};
	$row->{body} = $FORM{mail_body};
	
	# ���ԥ���������
	if ($FORM{mail_type} eq "plain") {
		$row->{subject} =~ s/__<<BR>>__/\n/gi;
		$row->{body} =~ s/__<<BR>>__/\n/gi;
	} else {
		$row->{subject} =~ s/__<<BR>>__/<BR>/gi;
		$row->{body} =~ s/__<<BR>>__/<BR>/gi;
	}
	
	# �ִ�
	$row->{subject} = $objAcData->ReplaceMailBody($row->{subject}, $admindata, $row, $SYS->{max_colnum});
	$row->{body} = $objAcData->ReplaceMailBody($row->{body}, $admindata, $row, $SYS->{max_colnum});
	
	
	
	$row->{num} = ($i + 1);
	push (@data,$row);
	$i++;
}

#�ۿ��ƥ���
if($FORM{send_test}){
	&sendmail_admin(@data);
	exit;
}

# ���Ӥξ���ͽ��ʳ��ϥХå������ɶ���
if (!$FORM{reserve_mode} && $FORM{sid}) {
	$admindata->{send_type} = 2;
}

# �ǥ��᡼������ä����ɤ����򵭲�����
$FORM{'deco_mode'} = $mail_session->get('email_send_mode');

# �᡼������
if ($FORM{reserve_mode}) {
	# ͽ���ۿ�
	&reserve(@data);
} elsif ($admindata->{send_type} == 1 && $admindata->{divnum} =~ /^[0-9]+$/ && $admindata->{divnum} > 0){
	&sendmail_div(@data);
}elsif($admindata->{send_type} == 0){
	&sendmail(@data);
}elsif($admindata->{send_type} == 2){

	# �Хå������ɽ���
	my @NEWDATA_ORG = @data;
	
	if (!$FORM{starttime}) {
		my %STIME = &getdatetime();
		$FORM{starttime} = "$STIME{year}$STIME{mon}$STIME{mday}$STIME{hour}$STIME{min}$STIME{sec}";
	}
	

	# ����ǡ����˽񤭹���------------------------------------------
	my $id = time.$$;
	$FORM{id} = $id;
	$FORM{start_send_date} = $FORM{starttime};
	$FORM{status} = 1;
	$FORM{send_type} = $admindata->{send_type};
	for(1..5) {
		$FORM{"search".$_}      .= $mail_session->get("search".$_);	# �ʹ��ߥ����
		$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);		# �ʹ��ߥƥ�����
		$FORM{"searchlike".$_}   = $mail_session->get("searchlike".$_);
	}
	$FORM{'search_domain'} = $mail_session->get('search_domain');
	$FORM{'andor'} = $mail_session->get('andor');
	$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
	# �񤭹���
	$objAcData->InsData('hist', 'HIST', \%FORM);
	#------------------------------------------------------------------
	

	my $pid;
	# ������Хå����饦��ɤǤ���
	FORK: {
		if ($pid = fork) {
			my $sid = "";
			if ($FORM{sid}) { $sid = "sid=".$FORM{sid}; }
			print "Location:email_send_finish.cgi?$sid \n\n";
			
			# STDOUT���Ĥ��ʤ��ȡ�apache����λstatus���֤��ʤ��餷������äơ��֥饦������������ʤ���
			close(STDOUT);
			close(STDERR);
			close(STDIN);
			# �ҥץ����ν�λ���ԤäƤ��ʤ��ȡ��Ҥ�Zombie�ˤʤäƤޤ��餷��
			wait;
		} elsif (defined $pid) {
			# �Хå����饦��ɽ���
		
			close(STDOUT);
			close(STDERR);
			close(STDIN);
			my $c = 1;
			
			my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

			my $return_path = $admindata->{admin_email};
			if ($admindata->{errmail} && $admindata->{errmail_email}) {
				$return_path = $admindata->{errmail_email};
			}
			my @hist;
			my $objMail = create_clsMail($admindata);
			foreach my $row (@NEWDATA_ORG){
				my $return = 1;
				$return = $objMail->send($admindata->{sendmail_path},$row->{email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$return_path, $FORM{mail_type}, $id);
				
				# ����ֳ��Ԥ�
				if ($admindata->{'send_span'}) { select(undef, undef, undef, $admindata->{'send_span'}); }
				
				if ($return){
					my $hist;
					$hist->{email} = $row->{email};
					push(@hist, $hist);
				}else{
					
				}
				$c++;
			}
			
			# ����ǡ����˺ǽ��񤭹���
			my %TIME = &getdatetime();
			
			# �оݥǡ�������
			my $target = $objAcData->GetData('hist', 'HIST', $id);
			my %UPDATE;
			foreach my $n (keys %$target) {
				$UPDATE{$n} = $target->{$n};
			}
			$UPDATE{end_send_date} = "$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}$TIME{sec}";	# ������λ����
			$UPDATE{backnumber} = 1;
			$UPDATE{status} = 2;
			$UPDATE{total_count} = ($c - 1);
			# ����
			$objAcData->UpdData('hist', 'HIST', $id, \%UPDATE);
			
			# ���å���󥯥ꥢ
			&clear_mailsession();
			exit;
		} elsif ($! =~ /No more process/) {
			# �ץ�����¿�������硢���֤��֤��ƺƥ�����
			sleep 5;
			redo FORK;
		} else {
			# �����ˤ��뤳�ȤϤʤ�
			die "Can't fork: $\n";
		}
	}
}
&error("�����ƥ२�顼�Ǥ������������פ�Ƽ���������ꤷ�Ƥ���������");
exit;


sub sendmail{
	my @NEWDATA_ORG = @_;
	
	# ��������а���ٷƤ����뤫
	my $waitspan = 30;
	# �ٷƻ���
	my $waittime = 3;
	
	if (!$FORM{starttime}) {
		my %STIME = &getdatetime();
		$FORM{starttime} = "$STIME{year}$STIME{mon}$STIME{mday}$STIME{hour}$STIME{min}$STIME{sec}";
	}
	
	
	# ����ǡ����˽񤭹���------------------------------------------
	my $id = time.$$;
	$FORM{id} = $id;
	$FORM{start_send_date} = $FORM{starttime};
	$FORM{status} = 1;
	$FORM{send_type} = $admindata->{send_type};
	for(1..5) {
		$FORM{"search".$_}      .= $mail_session->get("search".$_);	# �ʹ��ߥ����
		$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);		# �ʹ��ߥƥ�����
		$FORM{"searchlike".$_}   = $mail_session->get("searchlike".$_);
	}
	$FORM{'search_domain'} = $mail_session->get('search_domain');
	$FORM{'andor'} = $mail_session->get('andor');
	$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
	# �񤭹���
	$objAcData->InsData('hist', 'HIST', \%FORM);
	#------------------------------------------------------------------
	
	$|=1;

	&htmlheader;
	
	# �Ĥ���ʤ��褦�ˤ���
	print '<body onBeforeUnload="return UnloadMessage();">
<script language="JavaScript" type="text/javascript">

var noLocation = 1;
<!--
function UnloadMessage(){
	if (noLocation) {
		return "���̤����ư����Ƚ��������Ǥ���Ƥ��ޤ��ޤ���";
	} else {
		
	}
}
// -->
</script>
';
	
	print '</div><br><div align="center"><div style="width:600;padding:4px 5px;border:1px solid #666;background:#FFFFFF;">'."\r\n\r\n";
	
	
	# ���������
	print &make_graph_html()."<br>";
	
	print "<div id=\"init_title\"><font color=\"#ff0000\"><b>������Ǥ�������</b></font></div><br>";
	my $c = 1;
	
	my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

	my $return_path = $admindata->{admin_email};
	if ($admindata->{errmail} && $admindata->{errmail_email}) {
		$return_path = $admindata->{errmail_email};
	}
	my @hist;
	my $objMail = create_clsMail($admindata);
	foreach my $row (@NEWDATA_ORG){
		my $return = 1;
		$return = $objMail->send($admindata->{sendmail_path},$row->{email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$return_path, $FORM{mail_type}, $id);
		
		# ����ֳ��Ԥ�
		if ($admindata->{'send_span'}) { select(undef, undef, undef, $admindata->{'send_span'}); }
		
		if ($return){
			print '<font size="-1">'."$c:"."$row->{email}</font><br>\n";
			my $hist;
			$hist->{email} = $row->{email};
			push(@hist, $hist);
		}else{
			print '<font size="-1">'."$c:"."<font color=\"#ff0000\">�������顼($row->{email})</font></font><br>\n";
		}
		# �ٷƤʤ�
		#if(defined $waitspan && ($c % $waitspan) == 0){ sleep($waittime);}
		
		my $bar = int(($c / ($#NEWDATA_ORG + 1)) * 50);
		my $per = int(($c / ($#NEWDATA_ORG + 1)) * 100);
		if ($bar > 50) { $bar = 50; }
		if ($per > 100) { $per = 100; }
		print '<script type="text/javascript">parent.setProgress('.$per.','.$bar.');</script>';
		$c++;
	}
	print "<br><font color=\"#ff0000\"><b>������λ���ޤ�����</b></font><br>";
	print "<div align=\"center\">";
	print "<br><a href=\"email_send.cgi\">���</a></div></div></div>";

	print '<script type="text/javascript"><!--
document.getElementById(\'init_title\').innerHTML = "<b>������λ���ޤ���</b>";
// --></script>';
	&htmlfooter;
	
	# ����ǡ����˺ǽ��񤭹���
	my %TIME = &getdatetime();
	
	# �оݥǡ�������
	my $target = $objAcData->GetData('hist', 'HIST', $id);
	my %UPDATE;
	foreach my $n (keys %$target) {
		$UPDATE{$n} = $target->{$n};
	}
	$UPDATE{end_send_date} = "$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}$TIME{sec}";	# ������λ����
	$UPDATE{backnumber} = 1;
	$UPDATE{status} = 2;
	$UPDATE{total_count} = ($c - 1);
	# ����
	$objAcData->UpdData('hist', 'HIST', $id, \%UPDATE);
	
	# ���å���󥯥ꥢ
	&clear_mailsession();
	print '<script language="JavaScript" type="text/javascript">noLocation = 0;</script>';
	print "<meta http-equiv=\"REFRESH\" content=\"0;URL=email_send_finish.cgi\">\n";
	exit;
}

sub sendmail_div{
	my @NEWDATA_ORG = @_;
	
	my $waittime = $admindata->{divwait};
	my $start = $FORM{"start"};
	my $end = $start + $admindata->{divnum};

	my $c = 0;
	
	my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

	my $return_path = $admindata->{admin_email};
	if ($admindata->{errmail} && $admindata->{errmail_email}) {
		$return_path = $admindata->{errmail_email};
	}
	
	if (!$FORM{starttime}) {
		my %STIME = &getdatetime();
		$FORM{starttime} = "$STIME{year}$STIME{mon}$STIME{mday}$STIME{hour}$STIME{min}$STIME{sec}";
		
		$FORM{id} = time.$$;
		# ����ǡ����˽񤭹���
		$FORM{start_send_date} = $FORM{starttime};
		$FORM{status} = 1;
		$FORM{send_type} = $admindata->{send_type};
		for(1..5) {
			$FORM{"search".$_}      .= $mail_session->get("search".$_);	# �ʹ��ߥ����
			$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);		# �ʹ��ߥƥ�����
			$FORM{"searchlike".$_}   = $mail_session->get("searchlike".$_);
		}
		$FORM{'search_domain'} = $mail_session->get('search_domain');
		$FORM{'andor'} = $mail_session->get('andor');
		$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
		# �񤭹���
		$objAcData->InsData('hist', 'HIST', \%FORM);
	}
	
	my $data_num = ($#NEWDATA_ORG + 1);
	$| = 1;
	my $wr;
	foreach my $n (keys %$admindata) {
		$wr->{admindata}{$n} = $admindata->{$n};
	}
	&writing_check(\$wr);
	my $write = '<a href="http://www.ahref.org"><img src="img/ahref_2.jpg" alt="���ޥ��ۿ�CGI acmailer" /></a>';
	if ($wr->{writing}) { $write = ""; }

	print "Content-Type: text/html; charset=EUC-JP\n\n";
	print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP" />
<title>ʬ��������</title>
<link rel="stylesheet" href="./css/common.css" type="text/css">
<link rel="stylesheet" href="./css/default.css" type="text/css">
<link rel="stylesheet" href="./css/login_etc.css" type="text/css">
<SCRIPT language="JavaScript">
<!--
var set=0;
function nidoosi() {
	if(set==0){
		set=1;
	}else{
		alert("���ٲ����Ϥ����ޤ���\\n���Ф餯���Τޤޤ��Ԥ�����������");
		return false
	}
}
function delcheck() {
	f = confirm("������Ƥ�����Ǥ�����");
	return f
}
var noLocation = 1;
function UnloadMessage(){
	if (noLocation) {
		return "���̤����ư����Ƚ��������Ǥ���Ƥ��ޤ��ޤ���";
	} else {
		
	}
}

//-->
</SCRIPT>
</head>
<body onBeforeUnload="return UnloadMessage();">
<div id="containt_panel_wrapper">
	<div id="containt_panel">
    	<div id="panel_head" class="clearfix">
        	<div id="panel_head_left"><a href="http://www.acmailer.jp"><img src="img/logo.jpg" alt="���ޥ��ۿ�CGI acmailer" /></a></div>
            <div id="panel_head_right">'.$write.'</div>
        </div>';	
	
	

	print "<br><div align=\"center\" id=\"message\"><b>�������������桦����</b><br><br>���Ф餯���ΤޤޤǤ��ޤ�����������";
	print "<br><br></div><div align=\"center\" id=\"now\">$end / $data_num</div>";
	print '<div align="center"><div style="width:600;padding:4px 5px;border:1px solid #666;background:#FFFFFF;">';
	
	# ���������
	print &make_graph_html()."<br>";
	my $bar = int((($start + 1) / ($#NEWDATA_ORG + 1)) * 50);
	my $per = int((($start + 1) / ($#NEWDATA_ORG + 1)) * 100);
	if ($bar > 50) { $bar = 50; }
	if ($per > 100) { $per = 100; }
	print '<script type="text/javascript">parent.setProgress('.$per.','.$bar.');</script><br>';
	
	my $objMail = create_clsMail($admindata);
	foreach my $row (@NEWDATA_ORG){
		if($c >= $start && $c < $end){
			my $return = 1;
			$return = $objMail->send($admindata->{sendmail_path},$row->{email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$return_path, $FORM{mail_type}, $FORM{id});
			
			if ($return){
				print ('<font size="-1">'.($c + 1).":"."$row->{email}</font><br>\n");
			}else{
				print (($c + 1).":"."<font color=\"#ff0000\">�������顼($row->{email})</font><br>\n");
			}
			my $bar = int((($c + 1) / ($#NEWDATA_ORG + 1)) * 50);
			my $per = int((($c + 1) / ($#NEWDATA_ORG + 1)) * 100);
			if ($bar > 50) { $bar = 50; }
			if ($per > 100) { $per = 100; }
			print '<script type="text/javascript">parent.setProgress('.$per.','.$bar.');</script>';
			print '<script type="text/javascript"><!--
	document.getElementById(\'now\').innerHTML = "'.($c + 1)." / ".$data_num.'";
	// --></script>';
			
			# ����ֳ��Ԥ�
			if ($admindata->{'send_span'}) { select(undef, undef, undef, $admindata->{'send_span'}); }
			
		}
		$c++;

	}

	if($data_num > $end){
	    my $mail_id = $mail_session->mail_id();
	    print '<script language="JavaScript" type="text/javascript">noLocation = 0;</script>';
	    print "<meta http-equiv=\"REFRESH\" content=\"$waittime;URL=email_send_ctl.cgi?start=$end&starttime=$FORM{starttime}&mail_type=$FORM{mail_type}&id=$FORM{id}&mail_session_id=$mail_id\">\n";
	}
	print "</head>\n";
	#print "<body bgcolor=\"#FFFFFF\">\n";

	if($data_num > $end){
		
	}else{
		print '<script type="text/javascript"><!--
document.getElementById(\'message\').innerHTML = "<b>������λ��</b><br><br>'.$data_num.'�����������λ���ޤ�����";
// --></script>';
		print "<br><a href=\"email_send.cgi\">���</a>";
		print '<script language="JavaScript" type="text/javascript">noLocation = 0;</script>';
		
		# ����ǡ����˽񤭹���
		my %TIME = &getdatetime();
		
		# �оݥǡ�������
		my $target = $objAcData->GetData('hist', 'HIST', $FORM{id});
		my %UPDATE;
		foreach my $n (keys %$target) {
			$UPDATE{$n} = $target->{$n};
		}
		$UPDATE{end_send_date} = "$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}$TIME{sec}";	# ������λ����
		$UPDATE{backnumber} = 1;
		$UPDATE{status} = 2;
		$UPDATE{total_count} = ($#NEWDATA_ORG + 1);
		# ����
		$objAcData->UpdData('hist', 'HIST', $FORM{id}, \%UPDATE);
		
		# ���å���󥯥ꥢ
		&clear_mailsession();
		
		print "<meta http-equiv=\"REFRESH\" content=\"0;URL=email_send_finish.cgi\">\n";
	}

	&htmlfooter();

	exit;
}

# �����ԥƥ�������
sub sendmail_admin{
	my @NEWDATA_ORG = @_;
	
	$|=1;
	if (&isMobile()) {
		print "Content-Type: text/html; charset=EUC-JP\n\n";
		print '<?xml version="1.0" encoding="EUC-JP"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
<head>
<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=EUC-JP" />
<title>�ƥ�������</title>
</head>
<body>
<br><br>';
	} else {
		&htmlheader;
		print "</div>";
		print '<div align="center">';
	}
	my $c = 1;
	
	my $sendername = &SetFromName(&html2plantext($admindata->{admin_email}), &html2plantext($admindata->{admin_name}));

	my $objMail = create_clsMail($admindata);
	foreach my $row (@NEWDATA_ORG){
		my $return = 1;
		#$return = $objMail->send($admindata->{sendmail_path},$admindata->{admin_email},$row->{subject},$row->{body},$sendername,$sendername,"",$sendername, $FORM{mail_type});
		$return = $objMail->send($admindata->{sendmail_path},$FORM{test_email},$row->{subject},$row->{body},$sendername,$admindata->{admin_email},"",$admindata->{admin_email}, $FORM{mail_type});
		if ($return){
			print "$FORM{test_email}<br>\n";
		}else{
			print "<font color=\"#ff0000\">�������顼($admindata->{admin_email})</font><br>\n";
		}
		last;
	}
	print "<br><font color=\"#ff0000\"><b>������λ���ޤ�����</b></font><br>";
	print "<div align=\"center\">";
	if (!&isMobile()) {
		print "<br><input type=\"button\" value=\"�Ĥ���\" onclick=\"javascript:window.close();\"></div>";
		print '<script type="text/javascript"><!--
document.getElementById(\'title\').innerHTML = "<b>������λ��</b>";
// --></script>';
	} else {
		
	}
	
	&htmlfooter;
	exit;
}

# ͽ���ۿ�
sub reserve{
	my @NEWDATA_ORG = @_;
	# ����ǡ����˽񤭹���------------------------------------------
	$FORM{id} = time.$$;
	$FORM{start_send_date} = sprintf("%04d%02d%02d%02d%02d%02d", $FORM{send_year}, $FORM{send_mon}, $FORM{send_day}, $FORM{send_hour}, $FORM{send_min}, 0);
	$FORM{status} = 3;
	$FORM{send_type} = $admindata->{send_type};
	$FORM{total_count} = ($#NEWDATA_ORG + 1);
	for(1..5) {
		$FORM{"search".$_}      .= $mail_session->get("search".$_);	# �ʹ��ߥ����
		$FORM{"search_text".$_} .= $mail_session->get("search_text".$_);		# �ʹ��ߥƥ�����
		$FORM{"searchlike".$_}   = $mail_session->get("searchlike".$_);
	}
	$FORM{'search_domain'} = $mail_session->get('search_domain');
	$FORM{'andor'} = $mail_session->get('andor');
	$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
	# �񤭹���
	$objAcData->InsData('hist', 'HIST', \%FORM);
	#------------------------------------------------------------------
	
	my $sid = "";
	if ($FORM{'sid'}) { $sid = "&sid=".$FORM{'sid'}; }
	
	# ���å���󥯥ꥢ
	&clear_mailsession();
	print "Location: email_send_finish.cgi?mode=reserve".$sid."\n\n";
	exit;
	
}


sub make_graph_html() {
	my $tag = '
    <table summary="�ץ��쥹�С�" border="0"
     cellpadding="0" cellspacing="1" height="2" bgcolor="black"><tr><td bgcolor="#FFFFFF">
	 <table class="frame" border="0" width="100%" height="100%">
      <tr>';
	for(1..50) {
		$tag .= '
        <td width="2" height="2" id="bar'.$_.'"
         style="background-color:#CCCCCC;">
            &nbsp;
        </td>';
	}
	$tag .= '</tr>
    </table></td></tr></table><table width="100%"><tr>
        <td bgcolor="white" height="5" width="100%" id="percent"
         style="font-size:1.4em"></td></tr></table>
		 <SCRIPT language="JavaScript">
<!--

function setProgress(percent,barno)
{
var node = document.getElementById(\'percent\');
node.innerHTML = percent + \'�ѡ������\';
if(barno > 0) {
	for(i = 1; i <= barno; i++) {
	    node = document.getElementById(\'bar\'+ i);
	    node.style.backgroundColor = "#FFCC00";
	}
}
}

//-->
</SCRIPT>';
	return $tag;
}

sub clear_mailsession {
    $mail_session->clear();
    return 1;
}
