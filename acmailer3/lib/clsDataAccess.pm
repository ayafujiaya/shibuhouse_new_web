#!/usr/bin/perl
# 
# �ƥ����ȥե�����ؤΥǡ�������������

package clsDataAccess;

use strict;

# ���󥹥ȥ饯��
# ���������ʤ�
sub new {
	my $pkg = shift;
	
	bless {
		
	} ,$pkg;
}

# �ե�����ǡ�������(���ԡ�
# ���������ե�����̾�����������
sub GetFileRowData() {
	my $this = shift;
	my $file = shift;
	my $col = shift;
	
	# �ǡ�������
	my @DATA = main::openfile2array($file);
	
	$DATA[0] =~ s/\r\n|\r|\n//g;
	my @ROW = SplitTab($this, $DATA[0]);

	# �ǡ�������
	my @col = @$col;
	my $data;
	my $i = 0;
	foreach my $n (@col) {
		$data->{$n} = $ROW[$i];
		$i++;
	}
	return $data;
}

# �ե�����ǡ�������(���ơ�
# ���������ե�����̾�����������
sub GetFileAllData() {
	my $this = shift;
	my $file = shift;
	my $col = shift;
	
	# �ǡ�������
	my @DATA = main::openfile2array($file);
	
	# �����
	my @col = @$col;
	my @RETURN;
	foreach my $row (@DATA) {
		$row =~ s/\r\n|\r|\n//g;
		# ���ֶ��ڤ�������
		my @ROW = SplitTab($this, $row);
		
		# �ǡ�������
		my $data;
		my $i = 0;
		foreach my $n (@col) {
			$data->{$n} = $ROW[$i];
			$i++;
		}
		push(@RETURN, $data);
	}
	return @RETURN;
}

# �ե�����ǡ����򹹿�
# ���������ե�����̾����������� �ǡ���
sub UpdateDataFile() {
	my $this = shift;
	my $file = shift;
	my $col = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	# ��Ͽ�ǡ�������
	my $regdata = "";
	foreach my $n (@$col) {
		$regdata .= $FORM{$n}."\t";
	}
	
	# �ǡ������
	$this ->UpdateFile($file, $regdata);
	
	return 1;
}

# �ե�������
# ���������ե����롡��񤭥ǡ���
# ����͡� 1 or 0
sub UpdateFile() {
	my $this = shift;
	my $file = shift;
	my $regdata = shift;
		
	#�ե����륪���ץ�
	open(IN, "+< $file") || main::error("�ǡ����ե�����Υ����ץ�˼��Ԥ��ޤ�����");
	flock(IN, 2);
	truncate(IN, 0);
	seek(IN, 0, 0);
	print(IN $regdata);
	close(IN);
	
	return 1;
}

# �ե�������
# ���������ե����롡��񤭥ǡ���
# ����͡� 1 or 0
sub UpdateFileForce() {
	my $this = shift;
	my $file = shift;
	my $regdata = shift;
		
	#�ե����륪���ץ�
	open(IN, "> $file") || main::error("�ǡ����ե�����Υ����ץ�˼��Ԥ��ޤ�����");
	flock(IN, 2);
	truncate(IN, 0);
	seek(IN, 0, 0);
	print(IN $regdata);
	close(IN);
	
	return 1;
}

# �ե��������ü�˥ǡ������ɲ�
# ���������ե����롡��񤭥ǡ���
# ����͡� 1 or 0
sub InsertFile() {
	my $this = shift;
	my $file = shift;
	my $regdata = shift;
	
	if (!-e $file) {
		# �����ξ��
		open (F,"> $file") || main::error($file);
		print(F "");
		close(F);
		chmod (0777,"$file");
	}
	
	my $data;
	#�ե����륪���ץ�
	open(IN, "+< $file") || main::error("�ǡ����ե�����Υ����ץ�˼��Ԥ��ޤ�����");
	flock(IN, 2);
	my @DATA = <IN>;
	foreach (@DATA) {
		$_ =~ s/\r//g;
		$_ =~ s/\n//g;
		if ($_) {
			$data .= $_."\n";
		}
	}
	$regdata = $data.$regdata;
	truncate(IN, 0);
	seek(IN, 0, 0);
	print(IN $regdata);
	close(IN);
	
	return 1;
}

# �ե�����򤽤Τޤ޸Ƥ�Ǥ���
# ���������ե�����̾
# ����͡�ʸ����
sub ReadFile() {
	my $this = shift;
	my $file = shift;
	
	#�ե����륪���ץ�
	open(IN, $file) || main::error("�ǡ����ե�����Υ����ץ�˼��Ԥ��ޤ�����");
	flock(IN, 1);
	my @DATA = <IN>;
	close(IN);
	my $data = "";
	foreach (@DATA) {
		$_ =~ s/\r//g;
		$_ =~ s/\n//g;
		if ($_) {
			$data .= $_."\n";
		}
	}
	
	return $data;
}

# ����޶��ڤ�Υǡ����������
# ��������ʸ����
# ����͡�����
sub SplitComma() {
	my $this = shift;
	my $str = shift;
	return split(/,/, $str);
}

# ���ֶ��ڤ�Υǡ����������
# ��������ʸ����
# ����͡�����
sub SplitTab() {
	my $this = shift;
	my $str = shift;
	return split(/\t/, $str);
}
# # ����޶��ڤ�Υե��������Ȥ����
# # ���������ե�����̾
# # ����͡�����
# sub GetCommaFile() {
# 	my $this = shift;
# 	my $file = shift;
# 	my @DATA = main::openfile2array($file);
# 	return SplitComma($this, $DATA[0]);
# }

# # �������ڤ�Υե��������Ȥ����
# # ���������ե�����̾
# # ����͡�����
# sub GetTabFile() {
# 	my $this = shift;
# 	my $file = shift;
# 	my @DATA = main::openfile2array($file);
# 	return SplitTab($this, $DATA[0]);
# }

1;
