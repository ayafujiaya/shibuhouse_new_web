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
my %FORM = &form();
my %S = getsession($COOKIE{sid}, $FORM{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);
my $data_ref;

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;
