#!/usr/bin/perl

use lib "./lib/";
require "setup.cgi";
require 'jcode.pl';
require 'mimew.pl';
use clsMail;
use strict;
our $SYS;

my %FORM = &form("noexchange", "noencode");

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();
my $objMail = create_clsMail($admindata);

# ��ư�ֿ��᡼��ƥ�ץ졼�Ⱦ������
my $rowform = $objAcData->GetRowData('form', 'FORM');

# �����ԤΥ᡼�륢�ɥ쥹
my $sendername = &SetFromName($admindata->{admin_email}, $admindata->{admin_name});

# sendmail�ؤΥѥ�
my $sendmailpath = $admindata->{sendmail_path};

# ���������Ȥ������Ͽ�ػ�
# �᡼�륢�ɥ쥹��Ͽ�ե���������֤��Ƥ���URL��񤭤ޤ������㡧$limit = "http://www.ahref.org/cgi/acmailer/";��
my $limit = '';
&limit_access($limit) || &error("�����ʥ��������Ǥ���") if $limit;

($FORM{email} = lc($FORM{email})) =~ s/\r\n|\r|\n//g;

# �᡼�륢�ɥ쥹����ɽ�������å�
if ($FORM{reg} eq "edit") {
	if (!&CheckMailAddress($FORM{newemail})) {
		# �ѹ���᡼�륢�ɥ쥹
		&error("�ѹ���᡼�륢�ɥ쥹�����������Ϥ��Ƥ���������");
	} elsif (!&CheckMailAddress($FORM{oldemail})) {
		# �ѹ����᡼�륢�ɥ쥹
		&error("�ѹ����᡼�륢�ɥ쥹�����������Ϥ��Ƥ���������");
	}
} else {
	if($FORM{mode} ne "autoreg" && !&CheckMailAddress($FORM{email}) && $FORM{mode} ne "autoedit"){
		&error("��������ޤ���<br>�᡼�륢�ɥ쥹���������������Ƥ���������");
	}
}

# �ǡ������ե�������ɤ߹���
my @NEWDATA_ORG = $objAcData->GetData('mail', 'MAIL');
my @NEWDATA_ORG_BUF = $objAcData->GetTempMailLoopData();

# �����ͤؤΥ᡼��ˤĤ�����ƼԾ���
my %TIME = &getdatetime();
my $ml_comment_admin=
"
----------------------------------------
DATE              : $TIME{nowdate}
SERVER_NAME       : $ENV{'SERVER_NAME'}
HTTP_USER_AGENT   : $ENV{'HTTP_USER_AGENT'}
REMOTE_HOST       : $ENV{'REMOTE_HOST'}
REMOTE_ADDR       : $ENV{'REMOTE_ADDR'}
----------------------------------------
";


# ���Լ�����
foreach my $n (keys %FORM) {
    if ($n =~ /^col.*/) {
        $FORM{$n} =~ s/\r\n|\r|\n//g;
    }
}


# �����å��ܥå������ͤ��ѹ����Ƽ���
%FORM = &ChangeCheckboxValue(\%FORM);


# ʸ��������Ĵ��
my $enc;
if ( $FORM{force} ) {
    $enc = $FORM{force};
}
else {
    if ( $FORM{encode} ) {
        my $code = getcode($FORM{encode});
        if ( $code ne "euc" && $code ne "ascii") {
            $enc = $code;
        }
    }
}


# ʸ���������Ѵ�
if ( $enc ) {
    foreach my $n (keys %FORM) {
        next if ref $FORM{$n};
        &Jcode::convert(\$FORM{$n}, "euc", $enc);
    }
}



my $xmailer = '';

# ////////////////////////////////////////////////////////////////////////// #
# �ᥤ�����

# ������Ͽ�������
if (defined $FORM{reg}){
	if ($admindata->{double_opt} && $FORM{reg} eq "add") {
		&doubleopt();
	} elsif ($admindata->{double_opt} && $FORM{reg} eq "edit") {
		&doubleopt_edit();
	} elsif ($admindata->{reg} eq "edit") {
		&edit();
	} else {
		&regdel if ($FORM{reg} eq "del");
		&regadd if $FORM{reg} eq "add";
		&regedit if $FORM{reg} eq "edit";
	}
} elsif ($FORM{mode} eq "autoreg") {
	&regdoubleopt;
} elsif ($FORM{mode} eq "autoedit") {
	&editdoubleopt;
} elsif ($FORM{mode} eq "autoform") {
	&regautoform();
}

&error("�����ʥ��������Ǥ���");

exit;
# ////////////////////////////////////////////////////////////////////////// #

sub doubleopt{
	$FORM{id} = time.$$;
	$FORM{id} = &md5sum($FORM{id});

	my $error_data;
	# ���顼�����å�(ɬ�ܹ��ܥ����å���
	if (!$objAcData->RegCheckExists(\%FORM, $SYS->{max_colnum}, \$error_data)) {
		&error($error_data);
	}
	
	# �ۿ��ե饰��Ω�äƤ���ǡ������뤫�ɤ���
	# �ե����फ�����Ͽ�����Ĥ���Ƥ��ʤ����
	if (!$admindata->{double_reg_form}) {
		if (!$objAcData->RegCheckDouble($FORM{email}, 1)) {
			&error("���Υ��ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���");
		}
	}
	
	# 2010/11/12 ����Ͽ�ɻߵ�ǽ�ɲ�
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($FORM{'email'});
	}
	
	# �ǡ�����Ͽ
	$objAcData->AddTempData(\%FORM, $SYS->{max_colnum});
	
	my $body = $rowform->{form_temp_mailbody};
	my $userdata;
	foreach my $n (keys %FORM) {
		$userdata->{$n} = $FORM{$n};
	}
	# �ִ����
	$body = $objAcData->ReplaceMailBody($body, $admindata, $userdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/g;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
	}
	
	# ��Ͽ�Ԥإ᡼��
	$objMail->send($sendmailpath,$FORM{email},$rowform->{form_temp_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	#}
	
	
	my $param;
	
	# �����ѿ��ɤ߹���
	&set_common_value(\$param, $admindata);
	if (&isMobile()) {
		# ����ü���ξ��
		&printhtml_tk($param, "tmpl/m_reg_temp_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC��
		&printhtml_tk($param, "tmpl/reg_temp_finish.tmpl");
	}
	exit;

}


# �Խ��ǥ��֥륪�ץ�
sub doubleopt_edit{
	$FORM{id} = time.$$;
	$FORM{id} = &md5sum($FORM{id});
	
	# �ѹ����ǡ�������
	my $beforedata = $objAcData->GetMailData("", $FORM{oldemail});
	# �ѹ���ǡ�������
	my $afterdata = $objAcData->GetMailData("", $FORM{newemail});
	
	if ($FORM{newemail} eq $FORM{oldemail}) { &error("�ѹ������ѹ���Ȥǥ᡼�륢�ɥ쥹��Ʊ��Ǥ���"); }
	# �ե����फ��ν�ʣ��Ͽ�����Ĥ���Ƥ��ʤ����
	if (!$admindata->{double_reg_form}) {
		if ($afterdata->{id} && $afterdata->{status}) { &error("�ѹ���᡼�륢�ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���"); }
	}
	if (!$beforedata->{id} || ($beforedata->{id} && !$beforedata->{status})) { &error("�ѹ����᡼�륢�ɥ쥹�����Ĥ���ޤ���"); }
	
	# ���ѹ��ǡ�����Ͽ
	$objAcData->AddTempChangeData(\%FORM, $SYS->{max_colnum});
	
	my $body = $rowform->{form_temp_change_mailbody};
	my $userdata;
	foreach my $n (keys %FORM) {
		$userdata->{$n} = $FORM{$n};
	}
	# �ִ����
	$body = $objAcData->ReplaceMailBody($body, $admindata, $userdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/g;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
	}

	# ��Ͽ�Ԥإ᡼��
	$objMail->send($sendmailpath,$FORM{newemail},$rowform->{form_temp_change_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	
	my $param;
	
	# �����ѿ��ɤ߹���
	&set_common_value(\$param, $admindata);
	
	if (isMobile()) {
		# ������
		&printhtml_tk($param, "tmpl/m_edit_temp_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC��
		&printhtml_tk($param, "tmpl/edit_temp_finish.tmpl");
	}
	exit;
}

# �Խ�������
sub editdoubleopt{
	
	# ���顼�����å�
	if (!$FORM{id}) { &error("�ѥ�᡼�����顼�Ǥ���"); }
	
	# ������Ͽ�������ե��å�
	my %TIME = &getdatetime();
	$FORM{'edit_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	
	# �оݥǡ�������
	my $bufdata = $objAcData->GetData('change', 'TEMPCHANGE', $FORM{id});
	
	if (!$bufdata->{id} || !$bufdata->{newemail}) { &error("�оݤΥǡ��������˼��Ԥ��ޤ�����<br>���˽��������ꤵ��Ƥ��뤫������³���������ʤ��Ƥ��ޤ���"); }
	
	
	# �ѹ����ǡ�������
	my $beforedata = $objAcData->GetMailData("", $bufdata->{oldemail});
	# �ѹ���ǡ�������
	my $afterdata = $objAcData->GetMailData("", $bufdata->{newemail});
	
	if (!$beforedata->{email} || ($beforedata->{email} && !$beforedata->{status})) { &error("�ѹ����᡼�륢�ɥ쥹�����Ĥ���ޤ���"); }
	# �ե����फ��ν�ʣ��Ͽ�����Ĥ���Ƥ�����
	if (!$admindata->{double_reg_form}) {
		if ($afterdata->{email} && $afterdata->{status}) { &error("�ѹ���᡼�륢�ɥ쥹������¸�ߤ��ޤ���"); }
	}
	
	# Ʊ��E-mail�β���Ͽ�ǡ������
	$objAcData->DelSameMailTempChangeData($bufdata->{oldemail});
	
	# �᡼�륢�ɥ쥹�ѹ�
	$objAcData->RegChangeEmail($bufdata->{oldemail}, $bufdata->{newemail});
	
	# ����Υ᡼�륢�ɥ쥹������
	$beforedata->{oldemail} = $bufdata->{oldemail};
	$beforedata->{newemail} = $bufdata->{newemail};
	
	my $body = $rowform->{form_change_mailbody};
	# �ִ����
	$body = $objAcData->ReplaceMailBody($body, $admindata, $beforedata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# ��Ͽ�Ԥإ᡼��
		$objMail->send($sendmailpath,$bufdata->{newemail},$rowform->{form_change_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	if ($admindata->{merumaga_adminmail}) {
		# �����ͤإ᡼��
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_change_mailtitle}.$bufdata->{newemail},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	
	my $param;
	
	# �����ѿ��ɤ߹���
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $bufdata->{newemail};
	$param->{newemail} = $bufdata->{newemail};
	$param->{oldemail} = $bufdata->{oldemail};
	
	if (isMobile()) {
		# ������
		&printhtml_tk($param, "tmpl/m_edit_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC��
		&printhtml_tk($param, "tmpl/edit_finish.tmpl");
	}
	exit;
	
}

# �᡼�륢�ɥ쥹�ѹ�
sub regedit{
	
	# �ѹ����ǡ�������
	my $beforedata = $objAcData->GetMailData("", $FORM{oldemail});
	# �ѹ���ǡ�������
	my $afterdata = $objAcData->GetMailData("", $FORM{newemail});

	# ������Ͽ�������ե��å�
	my %TIME = &getdatetime();
	$FORM{'edit_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	
	if ($FORM{newemail} eq $FORM{oldemail}) { &error("�ѹ������ѹ���Ȥǥ᡼�륢�ɥ쥹��Ʊ��Ǥ���"); }
	# �ե����फ��ν�ʣ��Ͽ�����Ĥ���Ƥ��ʤ����
	if (!$admindata->{double_reg_form}) {
		if ($afterdata->{id} && $afterdata->{status}) { &error("�ѹ���᡼�륢�ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���"); }
	}
	if (!$beforedata->{id}) { &error("�ѹ����᡼�륢�ɥ쥹�����Ĥ���ޤ���"); }
	
	# Ʊ��E-mail�β���Ͽ�ǡ������
	$objAcData->DelSameMailTempChangeData($FORM{oldemail});
	
	# �᡼�륢�ɥ쥹�ѹ�
	$objAcData->RegChangeEmail($FORM{oldemail}, $FORM{newemail});
	
	$beforedata->{newemail} = $FORM{newemail};
	$beforedata->{oldemail} = $FORM{oldemail};
	my $body = $rowform->{form_change_mailbody};
	# �ִ����
	$body = $objAcData->ReplaceMailBody($body, $admindata, $beforedata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# ��Ͽ�Ԥإ᡼��
		$objMail->send($sendmailpath,$FORM{newemail},$rowform->{form_change_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	if ($admindata->{merumaga_adminmail}) {
		# �����ͤإ᡼��
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_change_mailtitle}.$FORM{newemail},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	
	my $param;
	
	# �����ѿ��ɤ߹���
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $beforedata->{newemail};
	$param->{newemail} = $beforedata->{newemail};
	$param->{oldemail} = $beforedata->{oldemail};
	
	if (isMobile()) {
		# ������
		&printhtml_tk($param, "tmpl/m_edit_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC��
		&printhtml_tk($param, "tmpl/edit_finish.tmpl");
	}
	exit;
}

sub regdoubleopt{
	
	# ���顼�����å�
	if (!$FORM{id}) { &error("�ѥ�᡼�����顼�Ǥ���"); }
	
	# ������Ͽ�������ե��å�
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	# �оݥǡ�������
	my $bufdata = $objAcData->GetData('mailbuf', 'TEMPMAIL', $FORM{id});
	
	# �оݹԼ�������
	if (!$bufdata->{id} || !$bufdata->{email}) { &error("�оݤΥǡ��������˼��Ԥ��ޤ�����<br>������Ͽ����Ƥ��뤫������Ͽ����Ƥ��ޤ���"); }

	# �ۿ��ե饰��Ω�äƤ���ǡ������뤫�ɤ���
	#if (!$objAcData->RegCheckDouble($bufdata->{email})) {
	#	&error("���Υ��ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���");
	#}
	
	# ��Ͽ����Ƥ��뤫�ɤ���
	my $targetdata = $objAcData->GetMailData("", $bufdata->{email});
	# �ե����फ��ν�ʣ��Ͽ�����Ĥ���Ƥ��ʤ����
	if (!$admindata->{double_reg_form}) {
		if ($admindata->{delmode} eq "del") {
			if ($targetdata->{id}) { &error("�оݤΥ��ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���"); }
		} else {
			if ($targetdata->{status}) {
				&error("�оݤΥ��ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���");
			}
		}
	}
	
	# Ʊ���᡼�륢�ɥ쥹�Υǡ�������
	$objAcData->DelSameMailTempData($bufdata->{email});
	
	# �оݥǡ������ʤ����ե����फ��ν�ʣ��OK�ξ��
	if (!$targetdata->{id} || $admindata->{double_reg_form}) {
		# �ǡ�����Ͽ
		foreach my $n (keys %$bufdata) {
			$FORM{$n} = $bufdata->{$n};
		}
		$objAcData->RegEmail(\%FORM);
	} else {
		# ��Ͽ�ǡ��������ƾ�񤭤��� 10/03/24
		foreach my $n (keys %$bufdata) {
			$FORM{$n} = $bufdata->{$n};
		}
		$FORM{id} = $targetdata->{id};
		$FORM{status} = 1;
		$objAcData->UpdData('mail', 'MAIL', $targetdata->{id}, \%FORM);
		
		
		# �ۿ����ơ������ѹ�
		#my $CHANGE;
		#$CHANGE->{$bufdata->{email}} = 1;
		#$FORM{"send_flg".$targetdata->{id}} = 1;
		#$FORM{"hid_email".$targetdata->{id}} = 1;
		#$objAcData->UpdMailStatus(\%FORM);
	}
	
	my $body = $rowform->{form_mailbody};
	# �ִ����
	$body = $objAcData->ReplaceMailBody($body, $admindata, $bufdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	# ����Ͽ�ɻߥꥹ�Ȥ��饯�ꥢ
	$objAcData->CleanRegDenyByEmail($bufdata->{email});
	
	if ($admindata->{merumaga_usermail}) {
		# ��Ͽ�Ԥإ᡼��
		$objMail->send($sendmailpath,$bufdata->{email},$rowform->{form_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	if ($admindata->{merumaga_adminmail}) {
		# �����ͤإ᡼��
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_mailtitle}.$bufdata->{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	
	my $param;
	
	# �����ѿ��ɤ߹���
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $bufdata->{email};
	
	if (&isMobile()) {
		# ������
		&printhtml_tk($param, "tmpl/m_reg_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC��
		&printhtml_tk($param, "tmpl/reg_finish.tmpl");
	}
	exit;
}


sub regautoform {
	
	# ���顼�����å�
	if (!$FORM{id}) { &error("�ѥ�᡼�����顼�Ǥ���"); }
	
	# ������Ͽ�������ե��å�
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	# �оݥǡ�������
	my $bufdata = $objAcData->GetData('mailbuf', 'TEMPMAIL', $FORM{id});
	
	# �оݹԼ�������
	if (!$bufdata->{id} || !$bufdata->{email}) { &error("�оݤΥǡ��������˼��Ԥ��ޤ�����<br>������Ͽ����Ƥ��뤫������Ͽ����Ƥ��ޤ���"); }
	
	# ��Ͽ����Ƥ��뤫�ɤ���
	my $targetdata = $objAcData->GetMailData("", $bufdata->{email});
	# �ե����फ��ν�ʣ��Ͽ�����Ĥ���Ƥ��ʤ����
	if (!$admindata->{double_reg_form}) {
		if ($admindata->{delmode} eq "del") {
			if ($targetdata->{id}) { &error("�оݤΥ��ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���"); }
		} else {
			if ($targetdata->{status}) {
				&error("�оݤΥ��ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���");
			}
		}
	}
	
	# 2010/11/12 ����Ͽ�ɻߵ�ǽ�ɲ�
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($bufdata->{'email'});
	}
	
	
	# ���顼�����å�(ɬ�ܹ��ܥ����å���
	my $error_data;
	if (!$objAcData->RegCheckExists(\%FORM, $SYS->{max_colnum}, \$error_data)) {
		&error($error_data);
	}
	
	# Ʊ���᡼�륢�ɥ쥹�Υǡ�������
	$objAcData->DelSameMailTempData($bufdata->{email});
	
	# �оݥǡ������ʤ����ե����फ��ν�ʣ��OK�ξ��
	if (!$targetdata->{id} || $admindata->{double_reg_form}) {
		$objAcData->RegEmail(\%FORM);
	} else {
		$FORM{id} = $targetdata->{id};
		$FORM{status} = 1;
		$objAcData->UpdData('mail', 'MAIL', $targetdata->{id}, \%FORM);
	}
	
	# ����Ͽ�ɻߥꥹ�Ȥ��饯�ꥢ
	$objAcData->CleanRegDenyByEmail($bufdata->{email});
	
	my $body = $rowform->{form_mailbody};
	# �ִ����
	$body = $objAcData->ReplaceMailBody($body, $admindata, \%FORM, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# ��Ͽ�Ԥإ᡼��
		$objMail->send($sendmailpath,$bufdata->{email},$rowform->{form_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	if ($admindata->{merumaga_adminmail}) {
		# �����ͤإ᡼��
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_mailtitle}.$bufdata->{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	
	my $param;
	
	# �����ѿ��ɤ߹���
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $bufdata->{email};
	
	if (&isMobile()) {
		# ������
		&printhtml_tk($param, "tmpl/m_reg_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC��
		&printhtml_tk($param, "tmpl/reg_finish.tmpl");
	}
	exit;
}
sub regadd{
	
	# ������Ͽ�������ե��å�
	my %TIME = &getdatetime();
	$FORM{'add_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	$FORM{'edit_date'} = $FORM{'add_date'};
	
	my $error_data;
	# ���顼�����å�(ɬ�ܹ��ܥ����å���
	if (!$objAcData->RegCheckExists(\%FORM, $SYS->{max_colnum}, \$error_data)) {
		&error($error_data);
	}
	
	# �ۿ��ե饰��Ω�äƤ���ǡ������뤫�ɤ���
	#if (!$objAcData->RegCheckDouble($FORM{email}, 1)) {
	#	&error("���Υ��ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���");
	#}
	
	# �оݤΥ᡼�륢�ɥ쥹�����
	my $maildata = $objAcData->GetMailData('', $FORM{'email'}) ;
	# �ե����फ��ν�ʣ��Ͽ�����Ĥ���Ƥ��ʤ����
	if (!$admindata->{double_reg_form}) {
		if ($maildata->{email} && $maildata->{status}) {
			&error("�оݤΥ��ɥ쥹�ϴ�����Ͽ����Ƥ��ޤ���");
		}
	}
	
	# 2010/11/12 ����Ͽ�ɻߵ�ǽ�ɲ�
	if ($admindata->{'regdeny'}) {
		$objAcData->checkRegDeny($FORM{'email'});
	}
	
	
	# �ǡ�����Ͽ
	if ($admindata->{double_reg_form}) {
		# ������Ͽ
		$objAcData->RegEmail(\%FORM);
	} elsif ($maildata->{email}) {
		# ��Ͽ�ǡ��������ƾ�񤭤��� 10/03/24
		$FORM{id} = $maildata->{id};
		$FORM{status} = 1;
		$objAcData->UpdData('mail', 'MAIL', $maildata->{id}, \%FORM);
		
		## �ۿ��ե饰����
		#$FORM{"send_flg".$maildata->{id}} = 1;
		#$FORM{"hid_email".$maildata->{id}} = 1;
		#$objAcData->UpdMailStatus(\%FORM);
	} else {
		# ������Ͽ
		$objAcData->RegEmail(\%FORM);
	}
	
	# ����Ͽ�ɻߥꥹ�Ȥ��饯�ꥢ
	$objAcData->CleanRegDenyByEmail($FORM{email});
	
	my $userdata;
	foreach my $n (keys %FORM) {
		$userdata->{$n} = $FORM{$n};
	}
	my $body = $rowform->{form_mailbody};
	# �ִ����
	$body = $objAcData->ReplaceMailBody($body, $admindata, $userdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;

	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$body =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# ��Ͽ�Ԥإ᡼��
		$objMail->send($sendmailpath,$FORM{email},$rowform->{form_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	if ($admindata->{merumaga_adminmail}) {
		# �����ͤإ᡼��
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form_mailtitle}.$FORM{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	
	my $param;
	
	# �����ѿ��ɤ߹���
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $FORM{email};
	
	if (isMobile()) {
		# ������
		&printhtml_tk($param, "tmpl/m_reg_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC��
		&printhtml_tk($param, "tmpl/reg_finish.tmpl");
	}
	exit;
	
}

sub regdel{
	
	# ���˺���Ѥߤ������å�
	my @DELMAIL = $objAcData->GetData('mail', 'MAIL');
	my $exist = 0;
	foreach my $ref (@DELMAIL) {
		if ($FORM{email} eq $ref->{email} && $ref->{status}) {
			$exist = 1;
		}
	}
	
	if(!$exist){
		&error("���Υ᡼�륢�ɥ쥹����Ͽ����Ƥ��ޤ���");
	}

	# �оݹԼ���
	my $data = $objAcData->GetMailData("", $FORM{email});
	
	
	# �����ǧ����Ѥ��뤫�ɤ���
	if ($admindata->{delconfirm} && !$FORM{checkok}) {
		my $param;
		# ��ǧ����ɽ��
		$param = \%FORM;
		
		# �����ѿ��ɤ߹���
		&set_common_value(\$param, $admindata);
	
		if (isMobile()) {
			# ������
			&printhtml_tk($param, "tmpl/m_del_confirm.tmpl", "", "Shift_JIS");
		} else {
			# PC��
			&printhtml_tk($param, "tmpl/del_confirm.tmpl");
		}
		exit;
	}
	
	# �᡼��ǡ����켰����
	#my @DELMAIL = $objAcData->GetData('mail', 'MAIL');
	foreach my $ref (@DELMAIL) {
		if ($FORM{email} eq $ref->{email}) {
			if ($admindata->{delmode} eq "del") {
				# ʪ�����
				$objAcData->DelData('mail', 'MAIL', $ref->{id});
			} else {
				# �ۿ����ơ������ѹ�
				my $CHANGE;
				$CHANGE->{$ref->{id}} = 1;
				$FORM{"send_flg".$ref->{id}} = 0;
				$FORM{"hid_email".$ref->{id}} = 1;
				$objAcData->UpdMailStatus(\%FORM);
			}
			# 2010/11/12 �����ɲá�����Ͽ�ɻߵ�ǽ
			# ����Ͽ�ɻߵ�ǽ��Ȥ����ϥꥹ����Ͽ����
			if ($admindata->{'regdeny'}) {
				my $deny;
				$deny->{'email'} = $ref->{'email'};
				$deny->{'id'} = time.$$;
				$deny->{'del_date'} = $TIME{'year'}.$TIME{'mon'}.$TIME{'mday'}.$TIME{'hour'}.$TIME{'min'}.$TIME{'sec'};
				# ����Ͽ�ɻߴ��¤����
				if ($admindata->{'regdeny_timelimit'}) {
					# ����Ͽ��ǽ���ռ���
					my @allowDate = &calcuDateTime($TIME{'year'}, $TIME{'mon'}, $TIME{'mday'}, $TIME{'hour'}, $TIME{'min'}, $TIME{'sec'}, $admindata->{'regdeny_timelimit'} * 3600);
					$deny->{'limit_date'} = sprintf("%04d%02d%02d%02d%02d%02d", $allowDate[0], $allowDate[1], $allowDate[2], $allowDate[3], $allowDate[4], $allowDate[5]);
				}
				# Ʊ���᡼�륢�ɥ쥹����Ͽ����Ƥ���о��
				my @regdeny = $objAcData->GetData("regdeny", "REGDENY");
				my $deny_exist = 0;
				foreach my $rowregdeny (@regdeny) {
					if ($rowregdeny->{'email'} eq $deny->{'email'}) {
						$objAcData->UpdData("regdeny", "REGDENY", $rowregdeny->{'id'}, $deny);
						$deny_exist = 1;
						last;			
					}
				}
				if (!$deny_exist) {
					$objAcData->InsData('regdeny', 'REGDENY', $deny);
				}
			}
		}
	}
	
	my $body = $rowform->{form2_mailbody};
	my $userdata = $data;
	# �ִ����
	$body = $objAcData->ReplaceMailBody($body, $admindata, $userdata, $SYS->{max_colnum});
	$body =~ s/__<<BR>>__/\n/gi;
	
	if ($rowform->{type} eq "html") {
		$body =~ s/\n/<br>/gi;
		$ml_comment_admin =~ s/\n/<br>/gi;
	}
	
	if ($admindata->{merumaga_usermail}) {
		# ��Ͽ�Ԥإ᡼��
		$objMail->send($sendmailpath,$FORM{email},$rowform->{form2_mailtitle},$body,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	if ($admindata->{merumaga_adminmail}) {
		# �����ͤإ᡼��
		$objMail->send($sendmailpath,$admindata->{admin_email},$rowform->{form2_mailtitle}.$FORM{email},$body.$ml_comment_admin,$sendername,$admindata->{admin_email},$xmailer,$admindata->{admin_email}, $rowform->{send_type}) || &error("�᡼�륢�ɥ쥹�������˼��Ԥ��ޤ�����<br>������Ǥ��������͡�$sendername�פˤ�Ϣ����������");
	}
	
	my $param;
	
	# �����ѿ��ɤ߹���
	&set_common_value(\$param, $admindata);
	
	$param->{email} = $FORM{email};
	
	if (isMobile()) {
		# ������
		&printhtml_tk($param, "tmpl/m_del_finish.tmpl", "", "Shift_JIS");
	} else {
		# PC��
		&printhtml_tk($param, "tmpl/del_finish.tmpl");
	}
	exit;
	
}

# ////////////////////////////////////////////////////////////////////////// #


sub md5sum{
	use integer;
	my ($l,$m,@n,$a,$b,$c,$d,@e,$r);
	# Initial values set
	$a=0x67452301;$b=0xefcdab89;$c=0x98badcfe;$d=0x10325476;
	$m=$_[0];
	# Padding
	$l=length $m;
	$m.="\x80"."\x00"x(($l%64<56?55:119)-$l%64);
	$m.=pack "VV",($l<<3)&0xffffffff,$l<<35;
	# Round
	for(0..($l+8)/64){
	@n=unpack 'V16',substr($m,$_<<6,64);
	@e[0..3]=($a,$b,$c,$d);
	$r=($a+$n[0]+0xd76aa478+($b&$c|(~$b&$d)));$a=$b+(($r<<7)|(($r>>25)&0x7f));
	$r=($d+$n[1]+0xe8c7b756+($a&$b|(~$a&$c)));$d=$a+(($r<<12)|(($r>>20)&0xfff));
	$r=($c+$n[2]+0x242070db+($d&$a|(~$d&$b)));$c=$d+(($r<<17)|(($r>>15)&0x1ffff));
	$r=($b+$n[3]+0xc1bdceee+($c&$d|(~$c&$a)));$b=$c+(($r<<22)|(($r>>10)&0x3fffff));
	$r=($a+$n[4]+0xf57c0faf+($b&$c|(~$b&$d)));$a=$b+(($r<<7)|(($r>>25)&0x7f));
	$r=($d+$n[5]+0x4787c62a+($a&$b|(~$a&$c)));$d=$a+(($r<<12)|(($r>>20)&0xfff));
	$r=($c+$n[6]+0xa8304613+($d&$a|(~$d&$b)));$c=$d+(($r<<17)|(($r>>15)&0x1ffff));
	$r=($b+$n[7]+0xfd469501+($c&$d|(~$c&$a)));$b=$c+(($r<<22)|(($r>>10)&0x3fffff));
	$r=($a+$n[8]+0x698098d8+($b&$c|(~$b&$d)));$a=$b+(($r<<7)|(($r>>25)&0x7f));
	$r=($d+$n[9]+0x8b44f7af+($a&$b|(~$a&$c)));$d=$a+(($r<<12)|(($r>>20)&0xfff));
	$r=($c+$n[10]+0xffff5bb1+($d&$a|(~$d&$b)));$c=$d+(($r<<17)|(($r>>15)&0x1ffff));
	$r=($b+$n[11]+0x895cd7be+($c&$d|(~$c&$a)));$b=$c+(($r<<22)|(($r>>10)&0x3fffff));
	$r=($a+$n[12]+0x6b901122+($b&$c|(~$b&$d)));$a=$b+(($r<<7)|(($r>>25)&0x7f));
	$r=($d+$n[13]+0xfd987193+($a&$b|(~$a&$c)));$d=$a+(($r<<12)|(($r>>20)&0xfff));
	$r=($c+$n[14]+0xa679438e+($d&$a|(~$d&$b)));$c=$d+(($r<<17)|(($r>>15)&0x1ffff));
	$r=($b+$n[15]+0x49b40821+($c&$d|(~$c&$a)));$b=$c+(($r<<22)|(($r>>10)&0x3fffff));
	$r=($a+$n[1]+0xf61e2562+($b&$d|(~$d&$c)));$a=$b+(($r<<5)|(($r>>27)&0x1f));
	$r=($d+$n[6]+0xc040b340+($a&$c|(~$c&$b)));$d=$a+(($r<<9)|(($r>>23)&0x1ff));
	$r=($c+$n[11]+0x265e5a51+($d&$b|(~$b&$a)));$c=$d+(($r<<14)|(($r>>18)&0x3fff));
	$r=($b+$n[0]+0xe9b6c7aa+($c&$a|(~$a&$d)));$b=$c+(($r<<20)|(($r>>12)&0xfffff));
	$r=($a+$n[5]+0xd62f105d+($b&$d|(~$d&$c)));$a=$b+(($r<<5)|(($r>>27)&0x1f));
	$r=($d+$n[10]+0x02441453+($a&$c|(~$c&$b)));$d=$a+(($r<<9)|(($r>>23)&0x1ff));
	$r=($c+$n[15]+0xd8a1e681+($d&$b|(~$b&$a)));$c=$d+(($r<<14)|(($r>>18)&0x3fff));
	$r=($b+$n[4]+0xe7d3fbc8+($c&$a|(~$a&$d)));$b=$c+(($r<<20)|(($r>>12)&0xfffff));
	$r=($a+$n[9]+0x21e1cde6+($b&$d|(~$d&$c)));$a=$b+(($r<<5)|(($r>>27)&0x1f));
	$r=($d+$n[14]+0xc33707d6+($a&$c|(~$c&$b)));$d=$a+(($r<<9)|(($r>>23)&0x1ff));
	$r=($c+$n[3]+0xf4d50d87+($d&$b|(~$b&$a)));$c=$d+(($r<<14)|(($r>>18)&0x3fff));
	$r=($b+$n[8]+0x455a14ed+($c&$a|(~$a&$d)));$b=$c+(($r<<20)|(($r>>12)&0xfffff));
	$r=($a+$n[13]+0xa9e3e905+($b&$d|(~$d&$c)));$a=$b+(($r<<5)|(($r>>27)&0x1f));
	$r=($d+$n[2]+0xfcefa3f8+($a&$c|(~$c&$b)));$d=$a+(($r<<9)|(($r>>23)&0x1ff));
	$r=($c+$n[7]+0x676f02d9+($d&$b|(~$b&$a)));$c=$d+(($r<<14)|(($r>>18)&0x3fff));
	$r=($b+$n[12]+0x8d2a4c8a+($c&$a|(~$a&$d)));$b=$c+(($r<<20)|(($r>>12)&0xfffff));
	$r=($a+$n[5]+0xfffa3942+($b^$c^$d));$a=$b+(($r<<4)|(($r>>28)&0xf));
	$r=($d+$n[8]+0x8771f681+($a^$b^$c));$d=$a+(($r<<11)|(($r>>21)&0x7ff));
	$r=($c+$n[11]+0x6d9d6122+($d^$a^$b));$c=$d+(($r<<16)|(($r>>16)&0xffff));
	$r=($b+$n[14]+0xfde5380c+($c^$d^$a));$b=$c+(($r<<23)|(($r>>9)&0x7fffff));
	$r=($a+$n[1]+0xa4beea44+($b^$c^$d));$a=$b+(($r<<4)|(($r>>28)&0xf));
	$r=($d+$n[4]+0x4bdecfa9+($a^$b^$c));$d=$a+(($r<<11)|(($r>>21)&0x7ff));
	$r=($c+$n[7]+0xf6bb4b60+($d^$a^$b));$c=$d+(($r<<16)|(($r>>16)&0xffff));
	$r=($b+$n[10]+0xbebfbc70+($c^$d^$a));$b=$c+(($r<<23)|(($r>>9)&0x7fffff));
	$r=($a+$n[13]+0x289b7ec6+($b^$c^$d));$a=$b+(($r<<4)|(($r>>28)&0xf));
	$r=($d+$n[0]+0xeaa127fa+($a^$b^$c));$d=$a+(($r<<11)|(($r>>21)&0x7ff));
	$r=($c+$n[3]+0xd4ef3085+($d^$a^$b));$c=$d+(($r<<16)|(($r>>16)&0xffff));
	$r=($b+$n[6]+0x04881d05+($c^$d^$a));$b=$c+(($r<<23)|(($r>>9)&0x7fffff));
	$r=($a+$n[9]+0xd9d4d039+($b^$c^$d));$a=$b+(($r<<4)|(($r>>28)&0xf));
	$r=($d+$n[12]+0xe6db99e5+($a^$b^$c));$d=$a+(($r<<11)|(($r>>21)&0x7ff));
	$r=($c+$n[15]+0x1fa27cf8+($d^$a^$b));$c=$d+(($r<<16)|(($r>>16)&0xffff));
	$r=($b+$n[2]+0xc4ac5665+($c^$d^$a));$b=$c+(($r<<23)|(($r>>9)&0x7fffff));
	$r=($a+$n[0]+0xf4292244+($c^($b|~$d)));$a=$b+(($r<<6)|(($r>>26)&0x3f));
	$r=($d+$n[7]+0x432aff97+($b^($a|~$c)));$d=$a+(($r<<10)|(($r>>22)&0x3ff));
	$r=($c+$n[14]+0xab9423a7+($a^($d|~$b)));$c=$d+(($r<<15)|(($r>>17)&0x7fff));
	$r=($b+$n[5]+0xfc93a039+($d^($c|~$a)));$b=$c+(($r<<21)|(($r>>11)&0x1fffff));
	$r=($a+$n[12]+0x655b59c3+($c^($b|~$d)));$a=$b+(($r<<6)|(($r>>26)&0x3f));
	$r=($d+$n[3]+0x8f0ccc92+($b^($a|~$c)));$d=$a+(($r<<10)|(($r>>22)&0x3ff));
	$r=($c+$n[10]+0xffeff47d+($a^($d|~$b)));$c=$d+(($r<<15)|(($r>>17)&0x7fff));
	$r=($b+$n[1]+0x85845dd1+($d^($c|~$a)));$b=$c+(($r<<21)|(($r>>11)&0x1fffff));
	$r=($a+$n[8]+0x6fa87e4f+($c^($b|~$d)));$a=$b+(($r<<6)|(($r>>26)&0x3f));
	$r=($d+$n[15]+0xfe2ce6e0+($b^($a|~$c)));$d=$a+(($r<<10)|(($r>>22)&0x3ff));
	$r=($c+$n[6]+0xa3014314+($a^($d|~$b)));$c=$d+(($r<<15)|(($r>>17)&0x7fff));
	$r=($b+$n[13]+0x4e0811a1+($d^($c|~$a)));$b=$c+(($r<<21)|(($r>>11)&0x1fffff));
	$r=($a+$n[4]+0xf7537e82+($c^($b|~$d)));$a=$b+(($r<<6)|(($r>>26)&0x3f));
	$r=($d+$n[11]+0xbd3af235+($b^($a|~$c)));$d=$a+(($r<<10)|(($r>>22)&0x3ff));
	$r=($c+$n[2]+0x2ad7d2bb+($a^($d|~$b)));$c=$d+(($r<<15)|(($r>>17)&0x7fff));
	$r=($b+$n[9]+0xeb86d391+($d^($c|~$a)));$b=$c+(($r<<21)|(($r>>11)&0x1fffff));
	$a=($a+$e[0])&0xffffffff;
	$b=($b+$e[1])&0xffffffff;
	$c=($c+$e[2])&0xffffffff;
	$d=($d+$e[3])&0xffffffff;}
	unpack('H*',(pack 'V4',$a,$b,$c,$d));
}
1;
