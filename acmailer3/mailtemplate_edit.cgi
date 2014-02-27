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
my $data_ref;

if ($FORM{reg}) {

	if ($FORM{id}) {
		# ����
		if (error_check(\%FORM, \$data_ref->{error_message})) {
			$FORM{template_name} =~ s/\t/ /gi;
			$FORM{mail_title} =~ s/\t/ /gi;
			$FORM{mail_body} =~ s/\t/ /gi;
			$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
			
			# ����
			$objAcData->UpdData("template", "TEMPLATE", $FORM{id}, \%FORM);
			
			# ������
			print "Location: mailtemplate_list.cgi?updok=1 \n\n";
			exit;
		} else {
			foreach my $n (keys %FORM) {
				$data_ref->{$n} = $FORM{$n};
			}
		}
	} else {
		# �����ɲ�
		if (error_check(\%FORM, \$data_ref->{error_message})) {
			$FORM{id} = time.$$;
			$FORM{template_name} =~ s/\t/ /gi;
			$FORM{mail_title} =~ s/\t/ /gi;
			$FORM{mail_body} =~ s/\t/ /gi;
			$FORM{mail_body} =~ s/\r\n|\r|\n/__<<BR>>__/gi;
			
			# �����ɲ�
			$objAcData->InsData("template", "TEMPLATE", \%FORM);
			
			# ������
			print "Location: mailtemplate_list.cgi?addok=1 \n\n";
			exit;
		} else {
			foreach my $n (keys %FORM) {
				$data_ref->{$n} = $FORM{$n};
			}
		}
	}
} elsif ($FORM{del} && $FORM{id}) {
	# ���
	$objAcData->DelData("template", "TEMPLATE", $FORM{id});
	
	# ������
	print "Location: mailtemplate_list.cgi?delok=1 \n\n";
	exit;
} elsif ($FORM{default_change}) {
	# �ǥե���ȥե饰����
	$objAcData->UpdTemplateDefaultFlg($FORM{default});

	# ������
	print "Location: mailtemplate_list.cgi?updok=1 \n\n";
	exit;
}

# �ƥ�ץ졼�ȥǡ�������
if ($FORM{id} && !$data_ref->{error_message}) {
	my $data = $objAcData->GetData("template", "TEMPLATE", $FORM{id});
	foreach my $n (keys %$data) {
		$data_ref->{$n} = $data->{$n};
	}
	$data_ref->{mail_body} =~ s/__<<BR>>__/\n/gi;
}

my @freecol = $objAcData->GetFreeColLoopData($SYS->{max_colnum});
$data_ref->{col_list} = \@freecol;

# �ե��������
$data_ref->{form} = \%FORM;

# �����ѿ��ɤ߹���
&set_common_value(\$data_ref, $admindata);

# HTMLɽ��
&printhtml_tk($data_ref);
exit;

# ���顼�����å�
sub error_check() {
	my $p_FORM = shift;
	my $error_message = shift;
	
	my %FORM = %$p_FORM;
	my @error;
	
	if (!$FORM{template_name}) { push(@error, "�ƥ�ץ졼��̾�����Ϥ��Ƥ���������"); }
	if (!$FORM{mail_title}) { push(@error, "��̾�����Ϥ��Ƥ���������"); }
	if (!$FORM{mail_body}) { push(@error, "��ʸ�����Ϥ��Ƥ���������"); }
	
	if ($#error >= 0) {
		$$error_message = join ("<BR>", @error);
		return 0;
	}
	return 1;
	
}
