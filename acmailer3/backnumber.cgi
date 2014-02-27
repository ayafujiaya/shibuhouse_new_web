#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

my %FORM = &form("noexchange");
my $data_ref;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

if (!$admindata->{backnumber_disp}) {
	&error("�Хå��ʥ�С�����ɽ�������ꤵ��Ƥ��ޤ���");
}

# ����ǡ�������
my @DATA = $objAcData->GetHistLoopData();
my @BACKDATA;

my $count = 0;
my ($next_flg, $back_flg);
foreach my $row (@DATA) {
	
	# �Хå��ʥ�С�ɽ���Τ��
	if (!$row->{backnumber}) { next; }
	
	# �Х�Х�ɽ��
	$row->{send_year} = substr($row->{start_send_date}, 0, 4);
	$row->{send_mon} = substr($row->{start_send_date}, 4, 2);
	$row->{send_day} = substr($row->{start_send_date}, 6, 2);
	$row->{send_hour} = substr($row->{start_send_date}, 8, 2);
	$row->{send_min} = substr($row->{start_send_date}, 10, 2);
	$row->{send_sec} = substr($row->{start_send_date}, 12, 2);
	$row->{send_date} = substr($row->{start_send_date}, 0, 4)."/".substr($row->{start_send_date}, 4, 2)."/".substr($row->{start_send_date}, 6, 2)." ".substr($row->{start_send_date}, 8, 2).":".substr($row->{start_send_date}, 10, 2).":".substr($row->{start_send_date}, 12, 2);
	
	# ɽ������
	$row->{start_send_date} = substr($row->{start_send_date}, 0, 4)."/".substr($row->{start_send_date}, 4, 2)."/".substr($row->{start_send_date}, 6, 2)." ".substr($row->{start_send_date}, 8, 2).":".substr($row->{start_send_date}, 10, 2).":".substr($row->{start_send_date}, 12, 2);
	$row->{end_send_date} = substr($row->{end_send_date}, 0, 4)."/".substr($row->{end_send_date}, 4, 2)."/".substr($row->{end_send_date}, 6, 2)." ".substr($row->{end_send_date}, 8, 2).":".substr($row->{end_send_date}, 10, 2).":".substr($row->{end_send_date}, 12, 2);
	
	$row->{mail_body} =~ s/__<<BR>>__/\n/gi;
	
	if ($FORM{id} eq "") { $FORM{id} = $row->{id}; $next_flg = 1; }
	
	# ���Υǡ���
	if ($back_flg) {
		$data_ref->{'back_id'} = $row->{id};
		$back_flg = 0;
	}
	
	# ���Υǡ���
	if ($FORM{id} == $row->{id}) { $next_flg = 1; $back_flg = 1;}
	if (!$next_flg) { $data_ref->{'next_id'} = $row->{id}; }
	
	# �ܺ٥ǡ���
	if ($FORM{id} eq $row->{id}) {
		my $col = $objAcData->{HIST_COL};
		my @col = @$col;
		foreach my $n (@col) {
			$data_ref->{$n} = $row->{$n};
		}
		foreach my $n (qw(send_year send_mon send_day send_hour send_min send_sec send_date)) {
			$data_ref->{$n} = $row->{$n};
		}
		if ($data_ref->{mail_type} eq "html") {
			# �����������
			$data_ref->{mail_body} =~ s/<.*?>//gi;
		}
	}
	
	push(@BACKDATA, $row);
	$count++;
	if ($count >= $admindata->{backnumber_num}) { last; }
}

my $template = "";
if ($FORM{mobile}) { $template = "tmpl/m_backnumber.tmpl"; }

# ���������
$data_ref->{backnumber_list} = \@BACKDATA;

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref, $template);
exit;
