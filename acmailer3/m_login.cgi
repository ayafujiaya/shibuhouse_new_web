#!/usr/bin/perl

our $SYS;
use lib "./lib/";
require "./lib/setup.cgi";
use strict;

# �����������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();
my $data_ref = $admindata;



if ($data_ref->{login_id} && $data_ref->{login_pass}) {
	# HTML�ƥ�ץ졼�ȥ����ץ�


} else {
	print "Content-type: text/html; charset=EUC-JP\n\n";
	print "�ѥ������ѥ�������̤���������ԤäƤ���������";
	exit;
}

my %FORM = &form();

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref, "", 1);
exit;
