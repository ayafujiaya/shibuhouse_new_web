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

my $template_file = "";

my $sid = "";
if ($FORM{sid}) {
	$sid = "&sid=".$FORM{sid};
}

if ($FORM{check}) {
	# ����ǡ�������
	$data_ref->{emailall} = $objAcData->GetDelMail(\%FORM, $SYS->{max_colnum}, \$data_ref);
	
	# ��ͳ���ܼ���
	my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
	$data_ref->{freecol_list} = \@freecol;
	
	# �ƥ�ץ졼������
	$template_file = 'tmpl/email_del_check.tmpl';
	if ($FORM{sid}) { $template_file = 'tmpl/m_email_del_check.tmpl'; }
} elsif ($FORM{del}) {
	# ���
	$objAcData->DelMail(\%FORM, $SYS->{max_colnum});
	
	# �ڡ���������
	my $sid = "";
	if ($FORM{sid}) { $sid = "&sid=".$FORM{sid}; }
	print "Location: $SYS->{homeurl_ssl}email_list.cgi?okdel=1$sid \n\n";
	exit;
}

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref, $template_file);
exit;
