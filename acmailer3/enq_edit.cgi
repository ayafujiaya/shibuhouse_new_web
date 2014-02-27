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

if ($FORM{reg}) {
	# ���顼�����å�
	if (&error_check(\%FORM, \$data_ref->{error_message})) {
		# ���Լ�����
		$FORM{enq_data} =~ s/\r\n|\r|\n/__<<BR>>__/g;
		if ($FORM{id}) {
			# ����
			$objAcData->UpdData('enq', 'ENQ', $FORM{id}, \%FORM);
		} else {
			# ��Ͽ
			$FORM{id} = time().$$;
			$objAcData->InsData('enq', 'ENQ', \%FORM);
		}
		# ������
		print "Location: enq_list.cgi?okedit=1 \n\n";
		exit;
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} elsif ($FORM{id}) {
	# �ǡ�������
	my $data = $objAcData->GetData('enq', 'ENQ', $FORM{id});
	$data->{enq_data} =~ s/__<<BR>>__/\n/g;
	foreach my $n (%$data) {
		$data_ref->{$n} = $data->{$n};
	}
}

$data_ref->{oktext} = "�ѹ�����ޤ�����" if $FORM{okedit};

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
	if ($FORM{enq_name} eq "") {
		push(@error, "���󥱡���̾�����Ϥ��Ƥ���������");
	}
	if ($FORM{enq_key} eq "") {
		push(@error, "���󥱡��ȥ��������Ϥ��Ƥ���������");
	} elsif ($FORM{enq_key} =~ /[^a-z]/) {
		push(@error, "���󥱡��ȥ��������ѤǤ���ʸ����Ⱦ�ѱѻ��ΤߤǤ���");
	}
	if ($FORM{enq_question} eq "") {
		push(@error, "���󥱡������Ѥ����Ϥ��Ƥ���������");
	}
	if ($FORM{enq_data} eq "") {
		push(@error, "���󥱡��ȥǡ��������Ϥ��Ƥ���������");
	}
	
	if ($#error >= 0) {
		$$error_message = join("<BR>", @error);
		return 0;
	}
	return 1;


}
