#!/usr/bin/perl


use lib "./lib/";
require "./lib/setup.cgi";
use strict;

our $SYS;
my %FORM = &form("noexchange");

if (!$FORM{key}) { error("�ѥ�᡼�����顼�Ǥ���"); }
if (!$FORM{mail_id}) { error("�ѥ�᡼�����顼�Ǥ���");}

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

my $data_ref;

if ($FORM{reg}) {
	# ���顼�����å�
	if (&error_check(\%FORM, \$data_ref->{error_message})) {
		# ���Լ�����
		$FORM{enq_id} = $FORM{id};
		$FORM{id} = time().$$;
		
		foreach my $n (keys %FORM) {
			if ($n =~ /^answer_/ && $FORM{$n}) {
				$FORM{answer} = $FORM{$n};
			}
		}
		
		# ����
		$objAcData->InsData($FORM{enq_id}, 'ENQANS',  \%FORM);
	
		# ������
		$data_ref->{ok} = 1;
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} elsif ($FORM{key}) {
	# �ǡ�������
	my @data = $objAcData->GetData('enq', 'ENQ');
	my $data;
	foreach my $row (@data) {
		if ($FORM{key} eq $row->{enq_key}) {
			$data = $row;
		}
	}
	$data->{enq_data} =~ s/__<<BR>>__/\n/g;
	foreach my $n (%$data) {
		$data_ref->{$n} = $data->{$n};
	}
	$FORM{id} = $data_ref->{id};
}

# ���ܤ��������
my @col = split(/\n/, $data_ref->{enq_data});
my @list;
my $i = 1;
foreach my $v (@col) {
	my $row;
	$row->{rownum} = $i;
	$row->{value} = $v;
	push(@list, $row);
	$i++;
}
$data_ref->{list} = \@list;

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
	my %FORM = %$p_FORM;
	
	my @error;
	
	my $exist = 0;
	foreach my $n (keys %FORM) {
		if ($n =~ /^answer_/ && $FORM{$n}) {
			$exist = 1;
		}
	}
	if (!$exist) { &error("���������򤷤Ƥ���������"); }
	
	if ($#error >= 0) {
		$$error_message = join("<BR>", @error);
		return 0;
	}
	return 1;


}
