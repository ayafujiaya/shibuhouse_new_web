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

# ɽ����������
my $dispcol = $objAcData->GetRowData('dispcol', 'DISPCOL');
foreach my $n (keys %$dispcol) {
	$data_ref->{$n} = $dispcol->{$n};
}

if ($FORM{'edit'}) {
	# ���顼�����å�
	if (&error_check(\%FORM, \$data_ref->{error_message})) {
		# �����ԥǡ�������
		$objAcData->UpdDispColData(\%FORM);
		
		# ���ɤ߹���
		print "Location: dispcol_edit.cgi?okedit=1 \n\n";
		exit;
		
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} else {

}

my @freecol = $objAcData->GetFreeColLoopData_EmailList($SYS->{max_colnum});
$data_ref->{freecol_list} = \@freecol;

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
