#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";
use strict;
our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

print "Content-type: text/html; charset=EUC-JP\n\n";

# ͽ���ۿ�
if ($admindata->{reserve}) {
	system("./lib/reserve.pl");
	print "OK";
} else {
	print "ͽ���ۿ����꤬�Ԥ��Ƥ��ޤ���";
}

exit;
