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

if(!$FORM{id}){
	&error("�����ʥ��������Ǥ���");
}



if ($FORM{'edit'}) {
	my $freecol = $objAcData->GetRowData('freecol', 'FREECOL');
	# ���顼�����å�
	if (&error_check(\%FORM, \$data_ref->{error_message}, $freecol, $admindata, $objAcData)) {
		# ������������
		my %TIME = &getdatetime();
		$FORM{'edit_date'} = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
		
		# �ǡ�������
		$objAcData->UpdData('mail', 'MAIL', $FORM{id}, \%FORM);
		
		# ������
		my $sid = "";
		if ($FORM{sid}) { $sid = "&sid=".$FORM{sid}; }
		print "Location: email_list.cgi?back=1&okedit=1$sid \n\n";
		exit;
	} else {
		foreach my $n (keys %FORM) {
			$data_ref->{$n} = $FORM{$n};
		}
	}
} elsif ($FORM{del} && $FORM{id}) {
	# ���
	$objAcData->DelData('mail', 'MAIL', $FORM{id});
	
	# ������
	my $sid = "";
	if ($FORM{sid}) { $sid = "&sid=".$FORM{sid}; }
	print "Location: email_list.cgi?back=1&okdel=1$sid \n\n";
	exit;
} else {
	# �оݤΥǡ�������
	$data_ref = $objAcData->GetMailData($FORM{id});
	$data_ref->{email_org} = $data_ref->{email};
}

if(!$data_ref->{email}){
	&error("��������ǡ�����¸�ߤ��ޤ���");
}

# ��ͳ���ܼ���
my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
my $i = 1;
foreach my $row (@freecol) {
	# �᡼���������
	$row->{col} = $data_ref->{"col".$i};
	$i++;
}
$data_ref->{freecol_list} = \@freecol;

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
	my $freecol = shift;
	my $admindata = shift;
	my $objAcData = shift;
	my %FORM = %$p_FORM;
	my @error;

	#���顼�����å�
	if(!$FORM{email}){
		push(@error, "�᡼�륢�ɥ쥹�����Ϥ��Ƥ���������");
	}
	#���顼�����å�
	if(!CheckMailAddress($FORM{email})){
		push(@error, "�᡼�륢�ɥ쥹�����������Ϥ��Ƥ���������");
	}
	
	# ��ʣ��Ͽ��OK����ʤ����
	if (!$admindata->{double_reg} && $FORM{email} ne $FORM{email_org}) {
		my $buf = $objAcData->GetMailData("", $FORM{email});
		if ($buf->{id}) {
			push(@error, "Ʊ���᡼�륢�ɥ쥹��������Ͽ����Ƥ��ޤ���");
		}
	}
	
	$$p_FORM{email} = lc $$p_FORM{email};
	
	my $colsdata;
	foreach(1..$SYS->{max_colnum}){
		my $col = "col".$_;
		if($freecol->{$col."checked"} && ($FORM{$col} eq "")){
			push(@error, "��".$freecol->{$col."name"}."�פ�ɬ�ܹ��ܤǤ�");
		}
		$FORM{$col} =~ s/,/��/g;
		$colsdata .= "\t$FORM{$col}";
	}
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;;
}
