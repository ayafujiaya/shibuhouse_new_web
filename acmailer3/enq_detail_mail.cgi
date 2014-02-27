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
my @ans = $objAcData->GetData($FORM{id}, 'ENQANS');
$data_ref->{total_count} = ($#ans + 1);

# ���ܤ��������
my %ANS;
foreach my $v (@ans) {
	if ($v->{mail_id} && $v->{answer} == $FORM{answer_id}) {
		$ANS{"mail".$v->{mail_id}} = 1;
	}
}

# ����ǡ�������
my @mail = $objAcData->GetData('mail', 'MAIL');
my @list;
foreach my $row (@mail) {
	if ($ANS{"mail".$row->{id}}) {
		push(@list, $row);
	}
}

# ɽ���������
my $dispcol = $objAcData->GetRowData('dispcol', 'DISPCOL');
my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
foreach my $ref (@list) {
	my $i = 1;
	# ɽ������
	my @col = @{$objAcData->{DISPCOL_COL}};
	foreach my $n (@col) {
		if ($dispcol->{$n} eq "email") {
			# �᡼�륢�ɥ쥹
			$ref->{"dispdata".$i} = $ref->{email};
			$data_ref->{"dispcolname".$i} = "�᡼�륢�ɥ쥹";
		} else {
			# ɽ���ǡ���
			$ref->{"dispdata".$i} = $ref->{"col".$dispcol->{$n}};
			# ɽ�������
			$data_ref->{"dispcolname".$i} = $freecol->{"col".$dispcol->{$n}."name"};
		}
		$i++;
	}
}
$data_ref->{list} = \@list;


# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;
