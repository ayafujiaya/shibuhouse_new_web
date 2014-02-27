#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# �ѹ����ޤ�����

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å����ǡ��������ȥ���������å�
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;
my $tmpl_file = 'mail';

if ($FORM{display}) {
	$tmpl_file = $FORM{display};
} else {
	$FORM{display} = 'mail';
}

if ($FORM{'edit'}) {
	
	my %REGDATA;
	foreach my $n (keys %$admindata) {
		$REGDATA{$n} = $admindata->{$n};
	}
	foreach my $n (keys %FORM) {
		$REGDATA{$n} = $FORM{$n};
	}
	# �饤���󥹼���
	my $li = &getlicense;
	foreach my $n (keys %$li) {
		$REGDATA{$n} = $li->{$n};
	}
	
	# ������Υ����å��ܥå����ȥ饸���ܥ������
	if ($FORM{display} eq "mail") {
		foreach my $n (qw()) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "default") {
		foreach my $n (qw(relay_use send_type qmail relay_send_mode fail_send_local sendmail_i_option)) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "autoreg") {
		
	} elsif ($FORM{display} eq "reserve") {
		foreach my $n (qw(reserve)) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "errmail") {
		foreach my $n (qw(errmail)) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "system") {
		foreach my $n (qw(backnumber_disp merumaga_usermail merumaga_adminmail double_reg double_reg_form double_opt delmode counter_disp rireki_email str_check delconfirm regdeny regdeny_timelimit)) {
			$REGDATA{$n} = $FORM{$n};
		}
		
	} elsif ($FORM{display} eq "license") {
		foreach my $n (qw(writing_hide license1 license2 license3 license4)) {
			$REGDATA{$n} = $FORM{$n};
		}
	} elsif ($FORM{display} eq "topmemo") {
		
	} elsif ($FORM{display} eq "mobile") {
		
	}
	
	# ���顼�����å�
	if (&error_check(\%REGDATA, \$data_ref->{error_message})) {
		if ($FORM{"display"} eq "autoform") {
			# ��ư�ե���������
			# ���Ԥ��ִ�
			for(1..$SYS->{max_colnum}) {
				$FORM{"col".$_."text"} =~ s/\r\n|\r|\n/__<<BR>>__/g;
			}
			$objAcData->ResetData("autoform", "AUTOFORM", \%FORM);
		} else {
			# �����ԥǡ�������
			$objAcData->UpdAdminData(\%REGDATA);
		}
		
		if ($FORM{display} eq "free") {
			# ��ͳ���ܹ���
			$objAcData->UpdFreeColData(\%REGDATA);
		}
		
		# �����ƥ�����ξ��
		if ($FORM{display} eq "system") {
			$S{login_id} = $FORM{login_id};
			$S{login_pass} = $FORM{login_pass};
			# ���å������¸
			&setsession($COOKIE{sid},%S);
		}
		
		# �����ԥǡ�����Ƽ���
		$admindata = $objAcData->GetAdminData();
		$data_ref = $admindata;
		$data_ref->{okedit} = 1;
	} else {
		foreach my $n (keys %REGDATA) {
			$data_ref->{$n} = $REGDATA{$n};
		}
	}
} else {
	# �����ԥǡ��������
	$data_ref = $admindata;
}
$data_ref->{login_pass_org} = $data_ref->{login_pass};

# �����ƥ�������
my $command = 'ls /etc -F | grep "release$\|version$"';
$data_ref->{os_type} = `$command`;
my $command = ' cat /etc/`ls /etc -F | grep "release$\|version$"`';
$data_ref->{os_version} = `$command`;
$data_ref->{perl_version} = $];
$data_ref->{jcode_version} = $Jcode::VERSION;

$data_ref->{os_type} =~ s/\r\n|\r|\n//g;
$data_ref->{os_version} =~ s/\r\n|\r|\n//g;
$data_ref->{perl_version} =~ s/\r\n|\r|\n//g;
$data_ref->{jcode_version} =~ s/\r\n|\r|\n//g;

# �����ƥ������������
if ($FORM{mode} eq "sysdown") {
	&sysdown($data_ref);
}

# ���������ץ饸���ܥ���
if (!$data_ref->{send_type}) { $data_ref->{send_type} = 0; }

# sendmail�ѥ�����äƤ��뤫�ɤ���
if(-x $data_ref->{sendmail_path}){
	$data_ref->{sendmail_path_check} = "�����С���Υѥ��Ȱ��פ��ޤ�����";
}else{
	$data_ref->{sendmail_path_check} = "�����С���Υѥ��Ȱ��פ��ޤ���";
}

# ���᡼��⥸�塼�뤬�Ȥ߹��ޤ�Ƥ�����
if (-e "./lib/autoreg.pl") {
	$data_ref->{autoreg} = "1";
	if (!$data_ref->{mypath}) {
		# pwd���ޥ�ɤǼ���
		my $path = `pwd`;
		$data_ref->{mypath} = $path;
	} else {
		$data_ref->{mypath_ok} = 1;
	}
}


my $license = $objAcData->GetLicense();
foreach my $n (qw(license1 license2 license3 license4)) {
	$data_ref->{$n} = $license->{$n};
}
$data_ref->{license_kind} = $SYS->{license_kind};

# ��ͳ����
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{freecol_list} = \@freecol;

# �����å��ܥå����Τ�ΤϤ��餫����ʸ��������
foreach my $n (@freecol) {
	if ($n->{coltype} eq "checkbox") {
		$data_ref->{checkbox_list} .= ",col".$n->{num};
	}
}

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# �ե��������
$data_ref->{form} = \%FORM;

# HTMLɽ��
&printhtml_tk($data_ref, 'tmpl/admin_'.$tmpl_file.'_edit.tmpl');
exit;

# ���顼�����å�
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my %FORM = %$p_FORM;
	my @error;
	
	#���顼�����å�
	if (!$FORM{admin_name}) {
		push(@error, "���п�̾�����Ϥ��Ƥ���������");
	#} elsif ($FORM{admin_name} =~ /[\"\'\@\;\:\,\.\<\>\\\[\]]/) {
	} elsif ($FORM{admin_name} =~ /[\"\'\<\>]/) {
		# ���ѤǤ��ʤ�ʸ���� "'<>���ѹ�
		push(@error, "���п�̾����ˡ�'�ס�\"�ס�<�ס�>�פϻ��ѤǤ��ޤ���");
	}
	if (!$FORM{login_id}) {
		push(@error, "ID�����Ϥ��Ƥ���������");
	} elsif($FORM{login_id} && ($FORM{login_id} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_id}) > 12)){
		push(@error, "ID��Ⱦ�ѱѿ�����12�����Ǥ����겼������");
	}
	
	if (!$FORM{login_pass}) {
		push(@error, "�ѥ���ɤ����Ϥ��Ƥ���������");
	}
	
	if ($FORM{display} eq "system" && $FORM{login_pass_org} ne $FORM{login_pass}) {
		if (!$FORM{login_pass2}) {
			push(@error, "�ѥ���ɡʳ�ǧ�ѡˤ����Ϥ��Ƥ���������");
		}
	}
	
	if($FORM{login_pass} && ($FORM{login_pass} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_pass}) > 12)){
		push(@error, "�ѥ���ɤ�Ⱦ�ѱѿ�����12�����Ǥ����겼������");
	}
	if($FORM{login_pass2} && ($FORM{login_pass2} !~ /^[0-9a-zA-Z_\-]+$/ || length($FORM{login_pass2}) > 12)){
		push(@error, "�ѥ���ɡʳ�ǧ�ѡˤ�Ⱦ�ѱѿ�����12�����Ǥ����겼������");
	}
	
	if($FORM{login_pass_org} ne $FORM{login_pass}){
	
		if($FORM{login_pass} ne $FORM{login_pass2}){
			push(@error, "�ѥ���ɤ����פ��ޤ���");
		}
	}
	
	if (!$FORM{admin_email}) {
		push(@error, "e-mail���ɥ쥹�����Ϥ��Ƥ���������");
	} elsif (!&CheckMailAddress($FORM{admin_email})) {
		push(@error, "e-mail���ɥ쥹�����������Ϥ��Ƥ���������");
	}
	
	if($FORM{divnum} && ($FORM{divnum} !~ /^[0-9]+$/ || $FORM{divnum} < 10)){
		push(@error, "ʬ�����������10�ʾ��Ⱦ�ѿ��ͤ����ꤷ�Ƥ���������");
	}
	if($FORM{divwait} && ($FORM{divwait} !~ /^[0-9]+$/)){
		push(@error, "ʬ���Ԥ����֤�Ⱦ�ѿ��ͤ����ꤷ�Ƥ���������");
	}
	if($FORM{send_type} == 1 && (!$FORM{divnum} || $FORM{divnum} < 10)){
		push(@error, "�����⡼�ɤ�ʬ�������ξ�硢ʬ�����������10�ʾ��Ⱦ�ѿ��ͤ����ꤷ�Ƥ���������");
	}

	if($FORM{send_type} == 1 && (!$FORM{divwait})){
		push(@error, "�����⡼�ɤ�ʬ�������ξ�硢ʬ���Ԥ����֤�Ⱦ�ѿ��ͤ����ꤷ�Ƥ���������");
	}
	if ($FORM{homeurl} && $FORM{homeurl} !~ /^https{0,1}\:\/\/.*/) {
		push(@error, "CGI����URL��https://www.abc.com/acmailer/�Τ褦�ʷ��������Ϥ��Ƥ���������");
	} elsif ($FORM{homeurl} !~ /^.*\/$/) {
		$$p_FORM{homeurl} .= "/";
	}
	if ($FORM{mypath} && $FORM{mypath} !~ /\/$/) {
		$$p_FORM{mypath} .= "/";
	}
	if ($FORM{errmail_email}) {
		if (!&CheckMailAddress($FORM{errmail_email})) {
			push(@error, "����᡼������ѥ᡼�륢�ɥ쥹�����������Ϥ��Ƥ���������");
		}
	}
	
	if ($FORM{send_stop} && $FORM{send_stop} =~ /[^0-9]/) {
		push(@error, "��ư��ߤ�Ԥ��������Ͽ��͹��ܤǤ���");
	}
	if ($FORM{errmail_log_num} && $FORM{errmail_log_num} =~ /[^0-9]/) {
		push(@error, "�����������¸����Ͽ��͹��ܤǤ���");
	}
	
	if ($FORM{double_reg_form} && !$FORM{double_reg}) {
		push(@error, "�ե����फ��ν�ʣ�ǡ�������Ĥ�����ϴ������̤���ν�ʣ�ǡ�������Ͽ����Ĥ��Ƥ���������");
	}
	
	# SMTP�����Ф����Ѥ�����
	if ($FORM{'relay_use'}) {
		
		# �ۥ���̾��ɬ��
		if (!$FORM{'relay_host'}) {
			push(@error, "������SMTP�����Ф����Ѥ�����ϥۥ���̾�����Ϥ��Ƥ���������");
		}
		# �ݡ��Ȥ�ɬ��
		if (!$FORM{'relay_port'}) {
			push(@error, "������SMTP�����Ф����Ѥ�����ϥݡ����ֹ�����ꤷ�Ƥ���������");
		}
		if ($FORM{'relay_port'} =~ /[^0-9]/) {
			push(@error, "�ݡ����ֹ��������ʸ�������Ϥ���Ƥ��ޤ���");
		}
	}
	
	# ����Ͽ�ɻߵ�ǽ�����Ѥ�����
	if ($FORM{'regdeny'}) {
		if ($FORM{'regdeny_timelimit'} eq "") {
			push(@error, "����Ͽ���ݵ�ǽ�����Ѥ�����ϡ����ݻ��֤����Ϥ��Ƥ���������");
		}
	}
	if ($FORM{'regdeny_timelimit'} && $FORM{'regdeny_timelimit'} !~ /[0-9\.]/) {
			push(@error, "����Ͽ���ݻ��֤Ͽ��͹��ܤǤ���");
	}
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;
	
}

# �ǡ�����Ͽ
sub sysdown() {
	my $data = shift;
	my $text = "ostype:".$data->{os_type}."\n";
	$text .= "osversion:".$data->{os_version}."\n";
	$text .= "acversion:".$SYS->{version}."\n";
	$text .= "perl:".$data->{perl_version}."\n";
	$text .= "Jcode:".$data->{jcode_version}."\n";
	
	my $size = length $text;
	print "Content-Type: application/octet-stream\n"; 
	print "Content-Disposition: attachment; filename=sysinfo.txt\n"; 
	print "Content-Length: $size\n\n"; 
	
	print $text;
	exit;
	
}
