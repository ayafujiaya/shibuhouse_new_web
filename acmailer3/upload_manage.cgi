#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å�����ꥻ�å����ǡ�������
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

#my %FORM = &form_multi();

my %FORM;
my $query = new CGI;
my @names = $query->param;
foreach(@names){
	$FORM{$_} =  $query->param($_);
}

my $row = $admindata;
my $data_ref;

if ($FORM{imagefile}) {
	UploadFile(\$FORM{imagefile});
	$data_ref->{uploadok} = 1;
}

if ($FORM{mode} eq "delete" && $FORM{file_name}) {
	if (-e './upload/'.$FORM{file_name}) {
		unlink('./upload/'.$FORM{file_name});
	}
	$data_ref->{delok} = 1;
}

# ���åץ��ɤ���Ƥ���ե������������
my @f = &get_uploadimage();
foreach my $ref (@f) {
	$ref->{file_name_urlenco} = &urlencode($ref->{file_name});
}
$data_ref->{file_list} = \@f;


# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;
