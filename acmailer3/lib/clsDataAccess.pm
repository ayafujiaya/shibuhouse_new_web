#!/usr/bin/perl
# 
# テキストファイルへのデータアクセス用

package clsDataAccess;

use strict;

# コンストラクタ
# 引　数：なし
sub new {
	my $pkg = shift;
	
	bless {
		
	} ,$pkg;
}

# ファイルデータ取得(１行）
# 引　数：ファイル名　カラム配列
sub GetFileRowData() {
	my $this = shift;
	my $file = shift;
	my $col = shift;
	
	# データ取得
	my @DATA = main::openfile2array($file);
	
	$DATA[0] =~ s/\r\n|\r|\n//g;
	my @ROW = SplitTab($this, $DATA[0]);

	# データ整形
	my @col = @$col;
	my $data;
	my $i = 0;
	foreach my $n (@col) {
		$data->{$n} = $ROW[$i];
		$i++;
	}
	return $data;
}

# ファイルデータ取得(全て）
# 引　数：ファイル名　カラム配列
sub GetFileAllData() {
	my $this = shift;
	my $file = shift;
	my $col = shift;
	
	# データ取得
	my @DATA = main::openfile2array($file);
	
	# カラム
	my @col = @$col;
	my @RETURN;
	foreach my $row (@DATA) {
		$row =~ s/\r\n|\r|\n//g;
		# タブ区切りを配列に
		my @ROW = SplitTab($this, $row);
		
		# データ整形
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

# ファイルデータを更新
# 引　数：ファイル名　カラム配列 データ
sub UpdateDataFile() {
	my $this = shift;
	my $file = shift;
	my $col = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	# 登録データ作成
	my $regdata = "";
	foreach my $n (@$col) {
		$regdata .= $FORM{$n}."\t";
	}
	
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
	return 1;
}

# ファイル上書き
# 引　数：ファイル　上書きデータ
# 戻り値： 1 or 0
sub UpdateFile() {
	my $this = shift;
	my $file = shift;
	my $regdata = shift;
		
	#ファイルオープン
	open(IN, "+< $file") || main::error("データファイルのオープンに失敗しました。");
	flock(IN, 2);
	truncate(IN, 0);
	seek(IN, 0, 0);
	print(IN $regdata);
	close(IN);
	
	return 1;
}

# ファイル上書き
# 引　数：ファイル　上書きデータ
# 戻り値： 1 or 0
sub UpdateFileForce() {
	my $this = shift;
	my $file = shift;
	my $regdata = shift;
		
	#ファイルオープン
	open(IN, "> $file") || main::error("データファイルのオープンに失敗しました。");
	flock(IN, 2);
	truncate(IN, 0);
	seek(IN, 0, 0);
	print(IN $regdata);
	close(IN);
	
	return 1;
}

# ファイルの末端にデータを追加
# 引　数：ファイル　上書きデータ
# 戻り値： 1 or 0
sub InsertFile() {
	my $this = shift;
	my $file = shift;
	my $regdata = shift;
	
	if (!-e $file) {
		# 新規の場合
		open (F,"> $file") || main::error($file);
		print(F "");
		close(F);
		chmod (0777,"$file");
	}
	
	my $data;
	#ファイルオープン
	open(IN, "+< $file") || main::error("データファイルのオープンに失敗しました。");
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

# ファイルをそのまま呼んでくる
# 引　数：ファイル名
# 戻り値：文字列
sub ReadFile() {
	my $this = shift;
	my $file = shift;
	
	#ファイルオープン
	open(IN, $file) || main::error("データファイルのオープンに失敗しました。");
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

# カンマ区切りのデータを配列に
# 引　数：文字列
# 戻り値：配列
sub SplitComma() {
	my $this = shift;
	my $str = shift;
	return split(/,/, $str);
}

# タブ区切りのデータを配列に
# 引　数：文字列
# 戻り値：配列
sub SplitTab() {
	my $this = shift;
	my $str = shift;
	return split(/\t/, $str);
}
# # カンマ区切りのファイルの中身を取得
# # 引　数：ファイル名
# # 戻り値：配列
# sub GetCommaFile() {
# 	my $this = shift;
# 	my $file = shift;
# 	my @DATA = main::openfile2array($file);
# 	return SplitComma($this, $DATA[0]);
# }

# # タグ区切りのファイルの中身を取得
# # 引　数：ファイル名
# # 戻り値：配列
# sub GetTabFile() {
# 	my $this = shift;
# 	my $file = shift;
# 	my @DATA = main::openfile2array($file);
# 	return SplitTab($this, $DATA[0]);
# }

1;
