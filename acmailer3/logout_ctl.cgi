#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";

our $SYS;

# �����ԤΥǡ�������
my $objAcData = new clsAcData($SYS->{data_dir});
my $admindata = $objAcData->GetAdminData();

# ���å�����ꥻ�å����ǡ�������
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
my $LOGIN = logincheck($S{login_id},$S{login_pass}, $admindata);

# ���å����񤭹���
print "Set-Cookie:"."sid=;"."path=/;"."\n";

# �ڡ���������
print "Location: $SYS->{homeurl_ssl}login.cgi" .'?'. "\n\n";
exit;
