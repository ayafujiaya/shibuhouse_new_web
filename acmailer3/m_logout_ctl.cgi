#!/usr/bin/perl

use lib "./lib/";
require "./lib/setup.cgi";

# ���å�����ꥻ�å����ǡ�������
my %COOKIE = &getcookie;
my %S = getsession($COOKIE{sid});
#my $LOGIN = logincheck($S{login_id},$S{login_pass});

# ���å����񤭹���
print "Set-Cookie:"."sid=;"."path=/;"."\n";

# �ڡ���������
print "Location: $SYS->{homeurl_ssl}m_login.cgi" .'?'. "\n\n";
exit;
