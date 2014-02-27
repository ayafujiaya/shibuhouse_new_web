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
if ($FORM{id}) {
	# �ǡ�������
	my $data = $objAcData->GetData('enq', 'ENQ', $FORM{id});
	$data->{enq_data} =~ s/__<<BR>>__/\n/g;
	foreach my $n (%$data) {
		$data_ref->{$n} = $data->{$n};
	}
}

# �����ǡ�������
if (-e $SYS->{data_dir}.$FORM{id}.".cgi") {
	my @ans = $objAcData->GetData($FORM{id}, 'ENQANS');
	$data_ref->{total_count} = ($#ans + 1);

	# ���ܤ��������
	my @col = split(/\n/, $data_ref->{enq_data});
	my @list;
	my $i = 1;
	foreach my $v (@col) {
		my $row;
		$row->{rownum} = $i;
		$row->{value} = $v;
		# �����ǡ����η������
		foreach my $a (@ans) {
			if ($a->{answer} == $i) {
				$row->{answer_count}++;
			}
		}
		push(@list, $row);
		$i++;
	}

	$data_ref->{list} = \@list;
}

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;
