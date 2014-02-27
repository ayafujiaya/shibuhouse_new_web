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
my $query = new CGI;
my %FORM = &form_multi($query);
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

my $data_ref;

my $data;
if ($FORM{data}) {
	# ���åץ��ɥǡ�������
	my $buffer;
	while(read($FORM{data}, $buffer, 2048)){ 
		$data .= $buffer;
	}
		
	if ($FORM{'mode'} eq "admin") {
		# �����ԥǡ���
		my $file = $SYS->{data_dir}."admin.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "freecol") {
		# ��ͳ���ܥǡ���
		my $file = $SYS->{data_dir}."freecol.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "errmail") {
		# ���顼�᡼��
		my $file = $SYS->{data_dir}."errmail.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "form") {
		# ��ư�ֿ��᡼��
		my $file = $SYS->{data_dir}."form.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "template") {
		# �ۿ��ƥ�ץ졼��
		my $file = $SYS->{data_dir}."template.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "hist") {
		# ����ǡ���
		my $file = $SYS->{data_dir}."hist.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "dispcol") {
		# ������ɽ������
		my $file = $SYS->{data_dir}."dispcol.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "license") {
		# ������ɽ������
		my $file = $SYS->{data_dir}."enc.cgi";
		$objAcData->UpdateFile($file, $data);
	} elsif ($FORM{'mode'} eq "autoform") {
		# �ե���������ǡ���
		my $file = $SYS->{data_dir}."autoform.cgi";
		$objAcData->UpdateFile($file, $data);
	}
	# �����
	print "Location: import.cgi?okedit=1 \n\n";
	exit;

} elsif ($FORM{mode}) {
	$data_ref->{error_message} = "�ե���������򤷤Ƥ���������";
}


# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# �ե��������
$data_ref->{form} = \%FORM;

# HTMLɽ��
&printhtml_tk($data_ref);
exit;
