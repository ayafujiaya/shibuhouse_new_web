#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å����ǡ��������ȥ���������å�
my %COOKIE = &getcookie;
my %FORM = &form("noexchange");
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

my $data_ref;

if ($FORM{upd}) {
	# ���顼�����å�
	if (&error_check(\%FORM, \$data_ref->{error_message})) {
		# ��Ͽ
		$objAcData->UpdFormData(\%FORM);
		
		# �����
		print "Location: form_edit.cgi?okedit=1 \n\n";
		exit;
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} else {
	# �ե�����ǡ�������
	my $data = $objAcData->GetRowData('form', 'FORM');
	$data->{form_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form2_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_temp_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_temp_change_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_change_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_autoform_mailbody} =~ s/__<<BR>>__/\n/g;
	$data->{form_regdeny_mailbody} =~ s/__<<BR>>__/\n/g;
	foreach my $n (%$data) {
		$data_ref->{$n} = $data->{$n};
	}
}

$data_ref->{oktext} = "�ѹ�����ޤ�����" if $FORM{okedit};

# ��ͳ���ܼ���
my @collist = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{col_list} = \@collist;

# ���󥱡��ȥǡ�������
my @EDATA = $objAcData->GetData('enq', 'ENQ');
foreach my $row (@EDATA) {
	$row->{enq_data} =~ s/__<<BR>>__/\n/g;
}
$data_ref->{enq_list} = \@EDATA;

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;

# ���顼�����å�
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my @error;
	if ($FORM{form_mailtitle} eq "") {
		push(@error, "��Ͽ�ѡ���̾�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_mailbody} eq "") {
		push(@error, "��Ͽ�ѡ���ʸ�����Ϥ��Ƥ���������");
	}
	if ($FORM{form2_mailtitle} eq "") {
		push(@error, "����ѡ���̾�����Ϥ��Ƥ���������");
	}
	if ($FORM{form2_mailbody} eq "") {
		push(@error, "����ѡ���ʸ�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_temp_mailtitle} eq "") {
		push(@error, "����Ͽ�ѡ���̾�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_temp_mailbody} eq "") {
		push(@error, "����Ͽ�ѡ���ʸ�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_change_mailtitle} eq "") {
		push(@error, "�ѹ��ѡ���̾�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_change_mailbody} eq "") {
		push(@error, "�ѹ��ѡ���ʸ�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_temp_change_mailtitle} eq "") {
		push(@error, "���ѹ��ѡ���̾�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_temp_change_mailbody} eq "") {
		push(@error, "���ѹ��ѡ���ʸ�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_autoform_mailtitle} eq "") {
		push(@error, "���᡼��ե������ѡ���̾�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_autoform_mailbody} eq "") {
		push(@error, "���᡼��ե������ѡ���ʸ�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_regdeny_mailtitle} eq "") {
		push(@error, "����Ͽ�����ѡ���̾�����Ϥ��Ƥ���������");
	}
	if ($FORM{form_regdeny_mailbody} eq "") {
		push(@error, "����Ͽ�����ѡ���ʸ�����Ϥ��Ƥ���������");
	}
	
	
	# �ػ�ʸ���ִ�
	$$p_FORM{form_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form2_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form2_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_temp_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_temp_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_temp_change_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_temp_change_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_change_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_change_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_autoform_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_autoform_mailbody} =~ s/\t/ /gi;
	$$p_FORM{form_regdeny_mailtitle} =~ s/\t/ /gi;
	$$p_FORM{form_regdeny_mailbody} =~ s/\t/ /gi;
	
	if ($#error >= 0) {
		$$error_message = join("<BR>", @error);
		return 0;
	}
	return 1;


}
