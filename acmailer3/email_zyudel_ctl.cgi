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
my ($data_ref, $regdata);

#�ե����륪���ץ�
my @MAIL = $objAcData->GetData('mail', 'MAIL');
my %ZYU;
my $col = $objAcData->{MAIL_COL};
my @col = @$col;
foreach my $row (@MAIL){
	#��ʣ�������
	if($ZYU{$row->{email}}){
		#�������
	}else{
		foreach my $n (@col) {
			$regdata .= $row->{$n}."\t";
		}
		$regdata .= "\n";
	}
	$ZYU{$row->{email}}++;
}

# �ǡ�������
my $file = $objAcData->{DATA_DIR}."mail.cgi";

# �ǡ������
$objAcData->UpdateFile($file, $regdata);

# �ڡ���������
print "Location: $SYS->{homeurl_ssl}email_list.cgi?okzyudel=1\n\n";
exit;
