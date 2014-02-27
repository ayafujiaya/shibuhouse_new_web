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
	
	$REGDATA{'autoform_use'} = $FORM{'autoform_use'};
	
	# ���顼�����å�
	if (&error_check(\%REGDATA, \$data_ref->{error_message})) {
		# ��ư�ե���������
		# ���Ԥ��ִ�
		for(1..$SYS->{max_colnum}) {
			$FORM{"col".$_."text"} =~ s/\r\n|\r|\n/__<<BR>>__/g;
		}
		$objAcData->ResetData("autoform", "AUTOFORM", \%FORM);

		# �����ԥǡ�������
		$objAcData->UpdAdminData(\%REGDATA);
		
		# ��ͳ���ܹ���
		$objAcData->UpdFreeColData(\%REGDATA);
		
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
&printhtml_tk($data_ref);
exit;

# ���顼�����å�
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my %FORM = %$p_FORM;
	my @error;
	
	
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;
	
}
