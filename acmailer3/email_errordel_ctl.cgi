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
my %FORM = &form("noexchange");
my $regdata;

# �ǡ�������
my @MAIL = $objAcData->GetData('mail', 'MAIL');
my $col = $objAcData->{MAIL_COL};
my @col = @$col;
foreach my $row (@MAIL){
	#���顼�������
	if(!CheckMailAddress($row->{email})){
		#�������
	}else{
		foreach my $n (@col) {
			$regdata .= $row->{$n}."\t";
		}
		$regdata .= "\n";
	}
}

# �ǡ�������
my $file = $objAcData->{DATA_DIR}."mail.cgi";

# �ǡ������
$objAcData->UpdateFile($file, $regdata);

# �ڡ���������
print "Location: $SYS->{homeurl_ssl}email_list.cgi?okerrordel=1\n\n";
exit;
