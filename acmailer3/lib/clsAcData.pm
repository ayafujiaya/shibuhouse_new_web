#!/usr/bin/perl
# 
# 

package clsAcData;

use Jcode;
require 'mimew.pl';
require 'jcode.pl';
use strict;

# DataAccessを継承
#use base qw(clsDataAccess);
our @ISA = qw ( clsDataAccess ); 

# コンストラクタ
# 引　数：データディレクトリ
sub new {
	my $pkg = shift;
	my $data_dir = shift;

	# 管理者設定
	my @ADMIN_COL = ('admin_name', 'login_id', 'login_pass', 'admin_email', 'title', 'sendmail_path', 'send_type', 'divnum', 'backnumber_disp', 'counter_disp', 'homeurl', 'merumaga_usermail', 'merumaga_adminmail', 'ssl', 'divwait', 'qmail', 'rireki_email', 'mypath', 'double_opt', 'str_check', 'reserve', 'errmail', 'errmail_email', 'send_stop', 'errmail_log_num', 'delmode', 'writing_hide', 'backnumber_num', 'free_memo', 'relay_use', 'relay_host', 'relay_user', 'relay_pass', 'relay_send_mode', 'relay_port', 'mobiledomain', 'double_reg', 'reg_email', 'del_email', 'last_login_date', 'double_reg_form', 'fail_send_local', 'autoform_email', 'delconfirm', 'autoform_use', 'send_span', 'regdeny', 'regdeny_timelimit', 'sendmail_i_option');
	
	
	# 自由項目
	my @FREECOL_COL = ('col1name', 'col1checked', 'col2name', 'col2checked', 'col3name', 'col3checked', 'col4name', 'col4checked', 'col5name', 'col5checked', 'col6name', 'col6checked', 'col7name', 'col7checked', 'col8name', 'col8checked', 'col9name', 'col9checked', 'col10name', 'col10checked');
	
	# 自動フォーム生成機能
	my @AUTOFORM_COL = ('col1text', 'col1type', 'col1disp', 'col2text', 'col2type', 'col2disp', 'col3text', 'col3type', 'col3disp', 'col4text', 'col4type', 'col4disp', 'col5text', 'col5type', 'col5disp', 'col6text', 'col6type', 'col6disp', 'col7text', 'col7type', 'col7disp', 'col8text', 'col8type', 'col8disp', 'col9text', 'col9type', 'col9disp', 'col10text', 'col10type', 'col10disp');
	
	# メール送信テンプレート
	my @TEMPLATE_COL = ('id', 'template_name', 'mail_title', 'mail_body', 'default');
	
	# フォーム送信テンプレート
	my @FORM_COL = ('form_mailtitle', 'form_mailbody', 'form2_mailtitle', 'form2_mailbody', 'send_type', 'form_temp_mailtitle', 'form_temp_mailbody', 'form_temp_change_mailtitle', 'form_temp_change_mailbody', 'form_change_mailtitle', 'form_change_mailbody', 'form_autoform_mailtitle', 'form_autoform_mailbody', 'form_regdeny_mailtitle', 'form_regdeny_mailbody');
	
	# 履歴データ
	my @HIST_COL = ('id', 'start_send_date', 'end_send_date', 'mail_title', 'mail_body', 'send_type', 'mail_type', 'backnumber', 'search1', 'search_text1', 'search2', 'search_text2', 'search3', 'search_text3', 'search4', 'search_text4', 'search5', 'search_text5', 'send_list', 'total_count', 'status', 'errmail_count', 'search_domain', 'andor', 'searchlike1', 'searchlike2', 'searchlike3', 'searchlike4', 'searchlike5', 'deco_mode');
	
	# メールデータ
	my @MAIL_COL = ('id', 'email', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'status', 'add_date', 'edit_date');
	
	# 仮登録メールデータ
	my @TEMPMAIL_COL = ('id', 'date', 'email', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10');
	
	# 仮変更メールデータ
	my @TEMPCHANGE_COL = ('id', 'date', 'newemail', 'oldemail', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10');
	
	# エラーメール
	my @ERRORMAIL_COL = ('email', 'count');
	
	# writing
	my @WRITING_COL = ('data');
	
	# カラム表示設定
	my @DISPCOL_COL = ('dispcol1', 'dispcol2', 'dispcol3');
	
	# アンケートフォームデータ
	my @ENQ_COL = ("id", "enq_name", "enq_question", "enq_data", "enq_key");
	
	# アンケートフォームデータ
	my @ENQANS_COL = ("id", "mail_id", "answer");
	
	# 登録拒否データ
	my @REGDENY_COL = ("id", "email", "del_date", "limit_date");
	
	# DataAccessクラスを継承
	#my $self = new clsDataAccess();
	
	bless ({
		
		DATA_DIR		=> $data_dir,
		ADMIN_COL		=> \@ADMIN_COL,
		FREECOL_COL		=> \@FREECOL_COL,
		AUTOFORM_COL	=> \@AUTOFORM_COL,
		TEMPLATE_COL	=> \@TEMPLATE_COL,
		FORM_COL		=> \@FORM_COL,
		HIST_COL		=> \@HIST_COL,
		MAIL_COL		=> \@MAIL_COL,
		TEMPMAIL_COL	=> \@TEMPMAIL_COL,
		TEMPCHANGE_COL	=> \@TEMPCHANGE_COL,
		ERRORMAIL_COL	=> \@ERRORMAIL_COL,
		WRITING_COL		=> \@WRITING_COL,
		DISPCOL_COL		=> \@DISPCOL_COL,
		ENQ_COL			=> \@ENQ_COL,
		ENQANS_COL		=> \@ENQANS_COL,
		REGDENY_COL		=> \@REGDENY_COL,
	} ,$pkg);
}

# データ追加
# 引　数：ファイル名　テーブル名　フォーム
# 戻り値：
sub InsData() {
	my $this = shift;
	my $filename = shift;
	my $tablename = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	my $regdata = "";
	my @col = @{$this->{$tablename."_COL"}};
	foreach my $n (@col) {
		$regdata .= $FORM{$n}."\t";
	}
	$regdata .= "\n";
	
	my $file = $this->{DATA_DIR}.$filename.".cgi";
	
	
	# 追加データを上書き
	$this->InsertFile($file, $regdata);
	return 1;
}


# データ上書き
# 引　数：ファイル名　テーブル名　フォーム
# 戻り値：
sub ResetData() {
	my $this = shift;
	my $filename = shift;
	my $tablename = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	my $regdata = "";
	my @col = @{$this->{$tablename."_COL"}};
	foreach my $n (@col) {
		$regdata .= $FORM{$n}."\t";
	}
	$regdata .= "\n";
	
	my $file = $this->{DATA_DIR}.$filename.".cgi";
	
	
	# 追加データを上書き
	$this->UpdateFile($file, $regdata);
	return 1;
}


# データ更新
# 引　数：ファイル名　テーブル名　ID　更新データ
# 戻り値：
sub UpdData() {
	my $this = shift;
	my $filename = shift;
	my $tablename = shift;
	my $id = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	my $file = $this->{DATA_DIR}.$filename.".cgi";
	
	my @col = @{$this->{$tablename."_COL"}};
	
	# データ取得
	my @DATA = $this->GetFileAllData($file, \@col);
	
	my $regdata = "";
	foreach my $row (@DATA){
		if ($row->{id} eq $id) {
			foreach my $n (@col) {
				$regdata .= $FORM{$n}."\t";
			}
		} else {
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
		}
		$regdata .= "\n";
	}
	
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
	return 1;
}

# データ削除
# 引　数：ファイル名　テーブル名　ID
# 戻り値：
sub DelData() {
	my $this = shift;
	my $filename = shift;
	my $tablename = shift;
	my $id = shift;
	
	my $file = $this->{DATA_DIR}.$filename.".cgi";
	
	my @col = @{$this->{$tablename."_COL"}};
	
	# データ取得
	my @DATA = $this->GetFileAllData($file, \@col);
	
	my $regdata = "";
	foreach my $row (@DATA){
		if ($row->{id} eq $id) {
			# 削除
		} else {
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
		}
		$regdata .= "\n";
	}
	
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
	return 1;
}

# データ取得
# 引　数：ファイル名　テーブル名　ID
# 戻り値：
sub GetData() {
	my $this = shift;
	my $filename = shift;
	my $tablename = shift;
	my $id = shift;
	
	my $file = $this->{DATA_DIR}.$filename.".cgi";
	
	my @col = @{$this->{$tablename."_COL"}};
	
	# データ取得
	my @DATA = $this->GetFileAllData($file, \@col);
	
	# ID指定がない場合は全て返す
	if (!$id) { return @DATA; }
	
	foreach my $row (@DATA){
		if ($row->{id} eq $id) {
			return $row;
		}
	}
	
	my $nodata;
	return $nodata;
}


# １行だけのデータ取得
# 引　数：ファイル名　テーブル名
# 戻り値：
sub GetRowData() {
	my $this = shift;
	my $filename = shift;
	my $tablename = shift;
	
	my $file = $this->{DATA_DIR}.$filename.".cgi";
	my @col = @{$this->{$tablename."_COL"}};
	
	# データ取得
	return $this->GetFileRowData($file, \@col);
}


# 表示用カラム登録
# 引　数：フォーム
# 戻り値：1 or 0
sub UpdDispColData() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	my @dispcol = @{$this->{DISPCOL_COL}};
	my $num = ($#dispcol + 1);
	
	my $regdata = "";
	for(1..$num) {
		$regdata .= $FORM{'dispcol'.$_}."\t";
	}
	
	my $file = $this->{DATA_DIR}."dispcol.cgi";
	
	# データ上書き
	$this ->UpdateFile($file, $regdata);
}

# 管理者データ取得
# 引　数：なし
# 戻り値：
sub GetAdminData() {
	my $this = shift;
	my $file = $this->{DATA_DIR}."admin.cgi";
	
	# データ取得
	my $data = $this->GetFileRowData($file, $this->{ADMIN_COL});
	
	# 改行取り除き
	foreach my $n (keys %$data) {
		$data->{$n} =~ s/__<<BR>>__/\n/g;
	}
	
	return $data;
}

# 自由項目の配列データ取得
# 引　数：カラム最大数
# 戻り値：配列
sub GetFreeColLoopData() {
	my $this = shift;
	my $maxnum = shift;
	# 自由項目データ取得
	my $freecoldata = $this->GetRowData('freecol', 'FREECOL');
	my @freecol;
	
	# 自動項目取得
	my $autoformdata = $this->GetRowData('autoform', 'AUTOFORM');
	
	for(1..$maxnum) {
		my $row;
		# 自動フォームの改行を戻す
		$autoformdata->{"col".$_."text"} =~ s/__<<BR>>__/\n/g;
		$row->{"colname"} = $freecoldata->{"col".$_."name"};
		$row->{"colcheck"} = $freecoldata->{"col".$_."checked"};
		$row->{"coltype"} = $autoformdata->{"col".$_."type"};
		$row->{"coltext"} = $autoformdata->{"col".$_."text"};
		$row->{"coldisp"} = $autoformdata->{"col".$_."disp"};
		$row->{"num"} = $_;
		
		# 改行が含まれている場合
		my @autodata = split(/\r\n|\r|\n/, $autoformdata->{"col".$_."text"});
		my @v2;
		foreach my $n2 (@autodata) {
			if ($n2 eq "") { next; }
			my $row2;
			$row2->{"coltext"} = $n2;
			push(@v2, $row2);
		}
		$row->{"autodatalist"} = \@v2;
		push(@freecol, $row);
	}
	return @freecol;
}

# メールアドレス管理で表示する用の自由項目取得
# 引　数：カラム最大数
# 戻り値：配列
sub GetFreeColLoopData_EmailList() {
	my $this = shift;
	my $maxnum = shift;
	
	my @freecol = $this->GetFreeColLoopData($maxnum);
	
	# 登録時間、更新時間を追加
	my $row;
	$row->{"colname"} = "登録日時";
	$row->{"num"} = "add_date";
	push(@freecol, $row);
	my $row;
	$row->{"colname"} = "更新日時";
	$row->{"num"} = "edit_date";
	push(@freecol, $row);
	return @freecol;
}

# 配信履歴取得(配列)
# 引　数：なし
# 戻り値：
sub GetHistLoopData() {
	my $this = shift;
	my $file = $this->{DATA_DIR}."hist.cgi";
	
	# データ取得
	my @DATA = $this->GetFileAllData($file, $this->{HIST_COL});
	
	# 履歴データに関しては日付でソートする
	@DATA = sort { $b->{start_send_date} cmp $a->{start_send_date} } @DATA;
	
	return @DATA;
}


# メールデータ取得(１行)
# 引　数：なし
# 戻り値：配列
sub GetMailData() {
	my $this = shift;
	my $id = shift;
	my $email = shift;
	my $file = $this->{DATA_DIR}."mail.cgi";
	
	# データ取得
	my @DATA = $this->GetFileAllData($file, $this->{MAIL_COL});
	
	foreach my $row (@DATA) {
		if ($row->{id} eq $id) {
			return $row;
		} elsif ($row->{email} eq $email) {
			return $row;
		}
	}
	my $return;
	return $return;
}


# 仮登録メールデータ取得
# 引　数：なし
# 戻り値：配列
sub GetTempMailLoopData() {
	my $this = shift;
	my $file = $this->{DATA_DIR}."mailbuf.cgi";
	
	# データ取得
	my @DATA = $this->GetFileAllData($file, $this->{TEMPMAIL_COL});
	
	# 日付処理
	foreach my $row (@DATA) {
		$row->{date_disp} = substr($row->{date}, 0, 4)."/".substr($row->{date}, 4, 2)."/".substr($row->{date}, 6, 2);
	}
	
	return @DATA;
}

# 仮変更メールデータ取得
# 引　数：なし
# 戻り値：配列
sub GetTempChangeLoopData() {
	my $this = shift;
	my $file = $this->{DATA_DIR}."change.cgi";
	
	# データ取得
	my @DATA = $this->GetFileAllData($file, $this->{TEMPCHANGE_COL});
	
	# 日付処理
	foreach my $row (@DATA) {
		$row->{date_disp} = substr($row->{date}, 0, 4)."/".substr($row->{date}, 4, 2)."/".substr($row->{date}, 6, 2);
	}
	
	return @DATA;
}

# エラーメールデータ取得
# 引　数：なし
# 戻り値：配列
sub GetErrorMailLoopData() {
	my $this = shift;
	my $file = $this->{DATA_DIR}."errmail.cgi";
	
	my @DATA = $this->GetFileAllData($file, $this->{ERRORMAIL_COL});
	
	# カウントの多い順
	@DATA = sort { (split(/\t/, $b))[1] cmp (split(/\t/, $a))[1] } @DATA;

	# データ取得
	return @DATA;
}


# 不着データ全削除
# 引　数：管理者データ
# 戻り値：
sub error_mail_hist_alldel {
	my $this = shift;
	my $admindata = shift;
	
	# 不着メールカウント
	my $ERROR_MAIL_COUNT;	# 不着数
	my $ERROR_MAIL_LIST;	# 不着メールアドレスリスト
	my $SEND_STOP_LIST;		# 配信停止リスト
	
	my $RIREKI;
	# 最新の履歴ID取得
	my @DATA = $this->GetHistLoopData();
	
	opendir DATADIR, $this->{DATA_DIR};
	map {
		
		if (/^hist_(\d*?)\.cgi/) {
			my $datafile = $_;
			my $histid = $1;
			# 履歴一時データ取得
			#ファイルオープン
			my $file = $this->{DATA_DIR}.$datafile;
			my @HIST = $this->GetFileAllData($file, $this->{ERRORMAIL_COL});
			
			$ERROR_MAIL_COUNT->{"hist_".$histid} = ($#HIST + 1);
			
			if ($RIREKI->{"hist_".$histid}) {

			} else {
				# 過去のデータは削除
				unlink($file);
			}
		}
	} readdir DATADIR;
	closedir DATADIR;
	
	# 不着リスト作成
	my $regdata = "";
	# 登録データ作成
	foreach my $n (keys %$ERROR_MAIL_LIST) {
		if ($n =~ /^mail_(.*)/) {
			my $mail = $1;
			$regdata .= $mail."\t".$ERROR_MAIL_LIST->{$n}."\n";
			
			# 自動配信停止
			if ($admindata->{send_stop} && $admindata->{send_stop} <= $ERROR_MAIL_LIST->{$n}) {
				# 自動配信停止リストに追加
				$SEND_STOP_LIST->{"send_stop_".$mail} = 1;
			}
		}
	}
	my $file = $this->{DATA_DIR}."errmail.cgi";
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
# 	# 履歴データ編集
# 	my $regdata = "";
# 	# 履歴データ取得
# 	my @HIST = $this->GetHistLoopData();
# 	my @col = @{$this->{HIST_COL}};
# 	foreach my $ref (@HIST){
# 		if ($ERROR_MAIL_COUNT->{"hist_".$ref->{id}}) {
# 			$ref->{errmail_count} = $ERROR_MAIL_COUNT->{"hist_".$ref->{id}};
# 		}
# 		foreach my $n (@col) {
# 			$regdata .= $ref->{$n}."\t";
# 		}
# 		$regdata .= "\n";
# 	}
# 	my $file = $this->{DATA_DIR}."hist.cgi";
# 	# データ上書き
# 	$this ->UpdateFile($file, $regdata);
# 	
	return 1;
}


# 不着処理
# 引　数：管理画面データ
# 戻り値：
sub error_mail_work {
	my $this = shift;
	my $admindata = shift;

	# 不着メールカウント
	my $ERROR_MAIL_COUNT;	# 不着数
	my $ERROR_MAIL_LIST;	# 不着メールアドレスリスト
	my $SEND_STOP_LIST;		# 配信停止リスト
	
	my $RIREKI;
	# 最新の履歴ID取得
	my @DATA = $this->GetHistLoopData();
	
	my $i = 1;
	foreach my $ref (@DATA) {
		$RIREKI->{"hist_".$ref->{id}} = 1;
		if ($admindata->{errmail_log_num} <= $i) { last; }
		$i++;
	}
	
	opendir DATADIR, $this->{DATA_DIR};
	map {
		
		if (/^hist_(\d*?)\.cgi/) {
			my $datafile = $_;
			my $histid = $1;
			# 履歴一時データ取得
			#ファイルオープン
			my $file = $this->{DATA_DIR}.$datafile;
			my @HIST = $this->GetFileAllData($file, $this->{ERRORMAIL_COL});
			
			$ERROR_MAIL_COUNT->{"hist_".$histid} = ($#HIST + 1);
			
			if ($RIREKI->{"hist_".$histid}) {
				# 最新のデータ
				foreach my $ref (@HIST) {
					$ref->{email} =~ s/\r\n|\r|\n//g;
					$ERROR_MAIL_LIST->{"mail_".$ref->{email}} ++;
				}
			} else {
				# 過去のデータは削除
				unlink($file);
			}
		}
	} readdir DATADIR;
	closedir DATADIR;
	
	# 不着リスト作成
	my $regdata = "";
	# 登録データ作成
	foreach my $n (keys %$ERROR_MAIL_LIST) {
		if ($n =~ /^mail_(.*)/) {
			my $mail = $1;
			$regdata .= $mail."\t".$ERROR_MAIL_LIST->{$n}."\n";
			
			# 自動配信停止
			if ($admindata->{send_stop} && $admindata->{send_stop} <= $ERROR_MAIL_LIST->{$n}) {
				# 自動配信停止リストに追加
				$SEND_STOP_LIST->{"send_stop_".$mail} = 1;
			}
		}
	}
	my $file = $this->{DATA_DIR}."errmail.cgi";
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
	# 履歴データ編集
	my $regdata = "";
	# 履歴データ取得
	my @HIST = $this->GetHistLoopData();
	my @col = @{$this->{HIST_COL}};
	foreach my $ref (@HIST){
		if ($ERROR_MAIL_COUNT->{"hist_".$ref->{id}}) {
			$ref->{errmail_count} = $ERROR_MAIL_COUNT->{"hist_".$ref->{id}};
		}
		foreach my $n (@col) {
			$regdata .= $ref->{$n}."\t";
		}
		$regdata .= "\n";
	}
	my $file = $this->{DATA_DIR}."hist.cgi";
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
	# 自動停止処理
	my $regdata = "";
	
	# メールデータ取得
	my $file = $this->{DATA_DIR}."mail.cgi";
	my @MAIL = $this->GetFileAllData($file, $this->{MAIL_COL});
	my @col = @{$this->{MAIL_COL}};
	foreach my $ref (@MAIL){
		foreach my $n (@col) {
			if($SEND_STOP_LIST->{"send_stop_".$ref->{email}}){
				$ref->{status} = 0;
			}
			$regdata .= $ref->{$n}."\t";
		}
		$regdata .= "\n";
	}
	# データ上書き
	my $file = $this->{DATA_DIR}."mail.cgi";
	$this ->UpdateFile($file, $regdata);
	
	return 1;
}


# ライセンスデータ取得
sub GetLicense() {
	my $this = shift;
	my $file = $this->{DATA_DIR}."enc.cgi";
	my $data;
	my $count = 1;
	open (IN,"./data/enc.cgi");
	while(<IN>){
		$_ =~ s/\r\n|\r|\n//gi;
		$data->{"license".$count} = $_;
		$count++;
	}
	close (IN);
	return $data;
}

# 管理者データ更新
# 引　数：
# 戻り値：
sub UpdAdminData() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	my $file = $this->{DATA_DIR}."admin.cgi";
	
	# フリー項目の改行を置換
	$FORM{'free_memo'} =~ s/\r\n|\r|\n/__<<BR>>__/g;
	# 携帯ドメインの改行を置換
	$FORM{'mobiledomain'} =~ s/\r\n|\r|\n/__<<BR>>__/g;
	
	# 更新
	$this->UpdateDataFile($file, $this->{ADMIN_COL}, \%FORM);
	
	# 組み込みモジュール更新
	$this->UpdModule(\%FORM);
	
	return 1;
}

# 自由項目データ更新
# 引　数：
# 戻り値：
sub UpdFreeColData() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	my $file = $this->{DATA_DIR}."freecol.cgi";

	# 更新
	$this->UpdateDataFile($file, $this->{FREECOL_COL}, \%FORM);

	return 1;
}

# 登録フォームテンプレート更新
# 引　数：
# 戻り値：
sub UpdFormData() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	$FORM{form_mailbody} =~ s/\n\r|\n|\r/__<<BR>>__/g;
	$FORM{form2_mailbody} =~ s/\n\r|\n|\r/__<<BR>>__/g;
	$FORM{form_temp_mailbody} =~ s/\n\r|\n|\r/__<<BR>>__/g;
	$FORM{form_temp_change_mailbody} =~ s/\n\r|\n|\r/__<<BR>>__/g;
	$FORM{form_change_mailbody} =~ s/\n\r|\n|\r/__<<BR>>__/g;
	$FORM{form_autoform_mailbody} =~ s/\n\r|\n|\r/__<<BR>>__/g;
	$FORM{form_regdeny_mailbody} =~ s/\n\r|\n|\r/__<<BR>>__/g;
	
	my $file = $this->{DATA_DIR}."form.cgi";
	
	# 更新
	$this->UpdateDataFile($file, $this->{FORM_COL}, \%FORM);
	
	return 1;
}



# 配信テンプレートデフォルトフラグ更新
# 引　数：テンプレートID　更新データ
# 戻り値：
sub UpdTemplateDefaultFlg() {
	my $this = shift;
	my $id = shift;
	
	my $file = $this->{DATA_DIR}."template.cgi";
	
	my @DATA = $this->GetData("template", "TEMPLATE");
	
	my $col = $this->{TEMPLATE_COL};
	my @col = @$col;
	my $regdata = "";
	foreach my $row (@DATA){
		if ($row->{id} eq $id) {
			$row->{default} = 1;
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
		} else {
			$row->{default} = 0;
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
		}
		$regdata .= "\n";
	}
	
	
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
	return 1;
}


# バックナンバー追加
# 引　数：更新データ
# 戻り値：1 or 0
sub UpdBacknumberAdd() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	# 更新するリスト
	my $CHANGE;
	foreach my $n (keys %FORM) {
		if ($n =~ /^hid_id([0-9]*)/) {
			$CHANGE->{$FORM{$n}} = 1;
		}
	}
	
	my @DATA = $this->GetHistLoopData();
	my $regdata;
	my $col = $this->{HIST_COL};
	my @col = @$col;
	foreach my $row (@DATA){
		foreach my $n (@col) {
			if ($CHANGE->{$row->{id}}) {
				if ($FORM{$row->{id}."_backnumber"}) {
					$row->{backnumber} = 1;
				} else {
					$row->{backnumber} = 0;
				}
			}
			$regdata .= $row->{$n}."\t";
		}
		$regdata .= "\n";
	}
	
	my $file = $this->{DATA_DIR}."hist.cgi";
	
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
	return 1;
}

# 履歴データの予約をキャンセル
# 引　数：
# 戻り値：
sub HistReserveCancel() {
	my $this = shift;
	my $id = shift;
	
	#ファイルオープン
	my @DATA = $this->GetHistLoopData();
	my $regdata = "";
	my $col = $this->{HIST_COL};
	my @col = @$col;
	foreach my $row (@DATA){
		if ($row->{id} eq $id) {
			$row->{status} = 4;
		}
		foreach my $n (@col) {
			$regdata .= $row->{$n}."\t";
		}
		$regdata .= "\n";
	}

	my $file = $this->{DATA_DIR}."hist.cgi";
	
	# データ上書き
	$this->UpdateFile($file, $regdata);
}


# 同じメールアドレスの仮登録データを削除
# 引　数：
# 戻り値：
sub DelSameMailTempData() {
	my $this = shift;
	my $email = shift;
	
	# 対象データ取得
	my @data = $this->GetTempMailLoopData();
	
	my $col = $this->{TEMPMAIL_COL};
	my @col = @$col;
	my $regdata = "";
	foreach my $row (@data) {
		if ($row->{email} ne $email) {
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
			$regdata .= "\n";
		}
	}
	
	my $file = $this->{DATA_DIR}."mailbuf.cgi";
	
	# データ上書き
	$this->UpdateFile($file, $regdata);
	return 1;
}

# 同じメールアドレスの仮変更データを削除
# 引　数：
# 戻り値：
sub DelSameMailTempChangeData() {
	my $this = shift;
	my $email = shift;
	
	# 対象データ取得
	my @data = $this->GetTempChangeLoopData();
	
	my $col = $this->{TEMPCHANGE_COL};
	my @col = @$col;
	my $regdata = "";
	foreach my $row (@data) {
		# 古いメールアドレスと比較する
		if ($row->{oldemail} ne $email) {
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
			$regdata .= "\n";
		}
	}
	
	my $file = $this->{DATA_DIR}."change.cgi";
	
	# データ上書き
	$this->UpdateFile($file, $regdata);
	return 1;
}

# メール配信フラグ更新
# 引　数：
# 戻り値：1 or 0
sub UpdMailStatus() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	# 変更するアドレスリスト
	my $CHANGE;
	foreach my $n (keys %FORM) {
		if ($n =~ /^hid_email(.*)/) {
			$CHANGE->{$1} = 1;
		}
	}
	
	# メールデータ取得
	my @DATA = $this->GetData('mail', 'MAIL');
	
	my $col = $this->{MAIL_COL};
	my @col = @$col;
	my $regdata;
	foreach my $row (@DATA){
		if ($CHANGE->{$row->{id}} ne "") {
			$row->{status} = $FORM{"send_flg".$row->{id}};
		}
		foreach my $n (@col) {
			$regdata .= $row->{$n}."\t";
		}
		$regdata .= "\n";
	}
	my $file = $this->{DATA_DIR}."mail.cgi";
	
	# データ上書き
	$this->UpdateFile($file, $regdata);
	
	return 1;
}

# メールアドレス登録
# 引　数：
# 戻り値：
sub AddEmail() {
	my $this = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	
	my %FORM = %$p_FORM;
	my @DATA = $this->GetData('mail', 'MAIL');
	my (@data, %ZYU);
	
	# 管理者データ取得
	my $admindata = $this->GetAdminData();
	
	# 重複データが許可されていない場合は重複データ作成
	if (!$admindata->{double_reg}) {
		foreach my $row (@DATA){
			$row->{email} = lc($row->{email});
			$ZYU{$row->{email}}++;
		}
	}
	
	# 登録日時
	my %TIME = main::getdatetime();
	my $add_date = $TIME{'year'}."/".$TIME{'mon'}."/".$TIME{'mday'}." ".$TIME{'hour'}.":".$TIME{'min'}.":".$TIME{'sec'};
	
	$FORM{emailall} =~ s/\r//;
	my @mailline = split(/\n/,$FORM{emailall});
	my ($i, $addnum, $colsdata, $emailall);
	foreach my $ref (@mailline){
		# 改行取り除き
		$ref =~ s/\r\n|\r|\n//g;
		
		if($ref){
			my @mail = split(/,/,$ref);
			my $row;
			$row->{i} = ++$i;
			$row->{email} = $mail[0];
			for(1..$max_colnum) {
				$row->{"col".$_} = $mail[$_];
			}
	
			if(!main::CheckMailAddress($mail[0])){
				$row->{status} .= "<font color=\"red\">× (メールアドレスエラー)</font><br>";
			}elsif($ZYU{$mail[0]}){
				$row->{status} .= "<font color=\"red\">× (重複)</font><br>";
			}
	
			my $colsdata;
			# 自由項目
			my @collist = $this->GetFreeColLoopData($max_colnum);
			my $colnum = 1;
			foreach my $free (@collist) {
				if ($free->{"colcheck"} && $row->{"col".$colnum} eq "") {
					# 必須の場合
					$row->{status} .= "<font color=\"red\">× (必須「".$free->{"colname"}."」)</font><br>";
				}
				$row->{"col".$colnum} =~ s/,/，/g;
				$colsdata .= ",".$row->{$row->{"col".$colnum}};
				$colnum++;
			}
			
			if(!$row->{status}){
				$row->{status} = "○ (登録可能)";
				++$addnum;
				# 重複登録が許可されていない場合
				if (!$admindata->{double_reg}) {
					$ZYU{$mail[0]}++;
				}
				my $serial = time.($$ + $i);
				my @line = split(/,/, $ref);

				# メールアドレスを小文字化
				$line[0] = lc($line[0]);

				# タブ区切りに変換
				my $line = join("\t", @line);
				$emailall .= $serial."\t".$line."\t".$add_date."\t".$add_date."\n";
			}else{
				main::error("処理を中断しました。<br>操作中にデータファイルの更新があった可能性があります。<br>$row->{email}<br>$row->{status}");
			}
		}
	}
	
	my $file = $this->{DATA_DIR}."mail.cgi";
	
	# 追加データを上書き
	$this->InsertFile($file, $emailall);
	return 1;
}

# メールアドレス登録
# 引　数：
# 戻り値：
sub GetAddEmail() {
	my $this = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	my $data_ref = shift;
	my %FORM = %$p_FORM;
	my $filename = $FORM{filename};
	
	# アップロードデータ受取
	my $buffer;
	if($filename && !$FORM{emailall}){
		while(read($filename, $buffer, 2048)){ 
			$FORM{emailall} .= $buffer;
		}

		# CSVの文字コードからEUC-JPに変換
		if ($FORM{charset}) {
			&Jcode::convert(\$FORM{emailall}, 'euc', $FORM{charset});
		}
	}
	
	# メールアドレス取得
	my @DATA = $this->GetData('mail', 'MAIL');
	my %ZYU;
	
	# 管理者データ取得
	my $admindata = $this->GetAdminData();
	
	# 重複データの登録が許可されていない場合は重複データ作成
	if (!$admindata->{double_reg}) {
		foreach my $row (@DATA){
			$row->{email} = lc($row->{email});
			$ZYU{$row->{email}}++;
		}
	}

	# 取得メールデータ分解
	my @mailline = split(/\r\n|\r|\n/,$FORM{emailall});
	my ($i, $addnum, $totalnum, $emailall, @data);
	$i = 1;

        my $many_error_num = 10;

	foreach my $ref (@mailline){
		# 改行取り除き
		$ref =~ s/\r\n|\r|\n//g;
		if($ref){
			my $sep = ",";
			if ($FORM{sep} eq "comma") {
				# カンマ区切り
				$sep = ",";
			} elsif ($FORM{sep} eq "tab") {
				# タブ区切り
				$sep = "\t";
			}
			my @mail = split(/$sep/,$ref);
			my $row;
			
			$row->{i} = $i;
			$i++;
			$row->{email} = lc($mail[0]);
			
			for(1..$max_colnum) {
				my $num = $_ ;
				$row->{"col".$num} = $mail[$num];
			}
			
			if(!main::CheckMailAddress(lc($mail[0]))){
				$row->{status} .= "<font color=\"red\">× (メールアドレスエラー)</font><br>";
			}elsif($ZYU{lc($mail[0])}){
				$row->{status} .= "<font color=\"red\">× (重複)</font><br>";
			}
			my $colsdata;
			# 自由項目
			my @collist = $this->GetFreeColLoopData($max_colnum);
			my $colnum = 1;
			foreach my $free (@collist) {
				if ($free->{"colcheck"} && $row->{"col".$colnum} eq "") {
					# 必須の場合
					$row->{status} .= "<font color=\"red\">× (必須「".$free->{"colname"}."」)</font><br>";
				}
				$row->{"col".$colnum} =~ s/,/，/g;
				$colsdata .= ",".$row->{$row->{"col".$colnum}};
				$colnum++;
			}
			
			# 配信ステータスを読み込む場合
			if ($FORM{send_flg_read} == 1) {
				$row->{send_flg} = 1;
			} elsif ($FORM{send_flg_read} == 0) {
				$row->{send_flg} = 0;
			} else {
				$row->{send_flg} = $mail[($max_colnum + 1)];
			}
			
			if(!$row->{status}){
                                $row->{status} = "○ (登録可能)";
				++$addnum;
				# 重複登録が許可されていない場合
				if (!$admindata->{double_reg}) {
					$ZYU{lc($mail[0])}++;
				}
				#$emailall .= $ref."\n";
				# カンマ区切りのデータ作成
				foreach my $n (@mail) {
					$emailall .= $n.",";
				}
				$emailall .= "\n";
			}
			
			# 自由項目
			my @collist;
			for(1..$max_colnum) {
				my $row2;
				$row2->{"col"} = $row->{"col".$_};
				push(@collist, $row2);
			}
			$row->{col_list} = \@collist;

                        # 詳細フラグが立っていたらリストする
                        if ( $FORM{detail_flg} ) {
                            push (@data,$row);
                        }

                        $totalnum++;
		}
	}
	$$data_ref->{loop} = \@data;
        $$data_ref->{has_detail} = @data ? 1 : 0;

	# 全て配信可能フラグを立てる
	my @emailall = split(/\r\n|\r|\n/, $emailall);
	my $regdata;
	foreach my $ref (@emailall) {

		my @data = split(/,/, $ref);
		if ($FORM{send_flg_read} == 1) {
			$data[($max_colnum + 1)] = 1;
		} elsif ($FORM{send_flg_read} == 0) {
			$data[($max_colnum + 1)] = "";
		}
		my $regcol;
		for(1..$max_colnum) {
			$regcol .= $data[$_].",";
		}
		$regdata .= "$data[0],$regcol".$data[($max_colnum + 1)]."\n";
	}

	$$data_ref->{addnum} = $addnum;
        $$data_ref->{totalnum} = $totalnum;

	return $regdata;
}

# 削除用メールアドレス取得
# 引　数：
# 戻り値：
sub GetDelMail() {
	my $this = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	my $data_ref = shift;
	my %FORM = %$p_FORM;
	my $filename = $FORM{filename};
	
	# アップロードデータ取得
	my $buffer;
	if($filename && !$FORM{emailall}){
		while(read($filename, $buffer, 2048)){ 
			$FORM{emailall} .= $buffer;
		} 
	}
	
	# メールアドレス取得
	my @DATA = $this->GetData('mail', 'MAIL');
	
	# 取得メールデータ分解
	my @mailline = split(/\r\n|\r|\n/,$FORM{emailall});

	# 対象データ取得
	my @mailline2;
	foreach my $n (@mailline) {
		my $file = $this->{DATA_DIR}."mail.cgi";
		# データ取得
		my @DATA = $this->GetFileAllData($file, $this->{MAIL_COL});
		foreach my $row (@DATA) {
			if ($row->{email} eq $n) {
				push(@mailline2, $row);
			}
		}
	}

	my ($i, $addnum, $emailall, @data);


	foreach my $row (@mailline2){
		if($row->{email}){
			$row->{status}= "";
			if(!main::CheckMailAddress($row->{email})){
				$row->{status} = "<font color=\"red\">× (メールアドレスエラー)</font><br>";
			#}elsif(!$ZYU{lc($row->{email})}){
			#	$row->{status} = "<font color=\"red\">× (登録無し)</font><br>";
			}
			if(!$row->{status}){
				$row->{status} = "○ (削除可能)";
				++$addnum;
			#	$ZYU{$row->{email}}++;
				$emailall .= $row->{email}."\n";
			}
			
			# 自由項目
			my @collist;
			for(1..$max_colnum) {
				my $row2;
				$row2->{"col"} = $row->{"col".$_};
				push(@collist, $row2);
			}
			$row->{col_list} = \@collist;
			
			push(@data, $row);
		}
	}
	
	$$data_ref->{loop} = \@data;
	$$data_ref->{addnum} = $addnum;

	
	return $emailall;
	
	
}

# メールアドレス一括削除
# 引　数：
# 戻り値：
sub DelMail() {
	my $this = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	my %FORM = %$p_FORM;
	my $filename = $FORM{filename};
	
	# メールアドレス取得
	my @DATA = $this->GetData('mail', 'MAIL');

	# 取得メールデータ分解
	my @mailline = split(/\r\n|\r|\n/,$FORM{emailall});

	# 対象データ取得
	my @mailline2;
	foreach my $n (@mailline) {
		my $file = $this->{DATA_DIR}."mail.cgi";
		# データ取得
		my @DATA = $this->GetFileAllData($file, $this->{MAIL_COL});
		foreach my $row (@DATA) {
			if ($row->{email} eq $n) {
				push(@mailline2, $row);
			}
		}
	}

	my ($i, $addnum, $emailall, @data);
	foreach my $row (@mailline2){
		if($row->{email}){
			$row->{status}= "";
			if(!main::CheckMailAddress($row->{email})){
				$row->{status} = "<font color=\"red\">× (メールアドレスエラー)</font><br>";
			#}elsif(!$ZYU{lc($row->{email})}){
			#	$row->{status} = "<font color=\"red\">× (登録無し)</font><br>";
			}
			if(!$row->{status}){
				$row->{status} = "○ (削除可能)";
				++$addnum;
			#	$ZYU{$row->{email}}++;
				# 削除
				$this->DelData('mail', 'MAIL', $row->{id});
				
			}
			
		}
	}
	
	return 1;
	
	
}

# メールアドレス完全削除
# 引　数：なし
# 戻り値：1 or 0
sub DelAllMailData() {
	my $this = shift;
	
	my $file = $this->{DATA_DIR}."mail.cgi";
	
	# データ上書き
	$this->UpdateFile($file, "");
	return 1;
}

# メール検索
# 引　数：
# 戻り値：配列
sub SearchEmail() {
	my $this = shift;
	my $p_DATA = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	my @DATA = @$p_DATA;
	my %FORM = %$p_FORM;
	
	
	# 自由項目取得
	my $freecol = $this->GetRowData('freecol', 'FREECOL');
	
	# 管理者データ取得
	my $admindata = $this->GetAdminData();
	
	my (@data, %ZYU, $zyunum, $errornum, $i);
	foreach my $row (@DATA){

		$row->{i} = $i+1;
		
		# 携帯かPCか
		if ($FORM{'search_domain'}) {
			my @mobiledomain = split(/\r\n|\r|\n/, $admindata->{mobiledomain});
			my $e;
			foreach my $n (@mobiledomain) {
				chomp($n);
				if ($row->{email} =~ /$n$/i) {
					$e = 1;
				}
			}
			if ($FORM{'search_domain'} == 1) {
				# PCのみ
				if ($e) { next; }
			} elsif ($FORM{'search_domain'} == 2) {
				# 携帯のみ
				if (!$e) { next; }
			}
		}
		
		# 配信ステータスによる絞込み
		if ($FORM{sendstatus} eq "" || $FORM{sendstatus} eq "all") {
			# 何もしない
		} elsif ($FORM{sendstatus} eq "on" && !$row->{"status"}) {
			next;
		} elsif ($FORM{sendstatus} eq "off" && $row->{"status"}) {
			next;
		}
		
		# 絞り込み適用
		my $yes = 0;
		my $no = 0;
		my $search_exist = 0;
		#if ($FORM{search_exist}) {
		for (my $i = 1; $i <= 5; $i++) {
			my $column = $freecol->{"col".$FORM{"search".$i}."name"};
			my $word = $FORM{"search_text".$i};
			
			# 正規表現用サニタイズ
			$word = main::MakeRegularString($word);
			
			if ($word eq "") { next; }
			
	#	print $FORM{"search1"}.":".$column."<BR>";
				# メールアドレス比較
			if ($FORM{"search".$i} eq "email") {
				if ($FORM{"searchlike".$i} == 1) {
					# 完全一致
					if ($row->{email} eq $word) {
						$yes = 1;
						if ($FORM{"andor"} eq "or") { $no = 0; }
					} elsif ($FORM{"andor"} eq "and") {
						$no = 1;
					}
				} elsif ($FORM{"searchlike".$i} == 2) {
					# 含まない
					if ($row->{email} !~ /$word/) {
						$yes = 1;
						if ($FORM{"andor"} eq "or") { $no = 0; }
					} elsif ($FORM{"andor"} eq "and") {
						$no = 1;
					}
				} else {
					# あいまい検索
					if ($row->{email} =~ /$word/) {
						$yes = 1;
						if ($FORM{"andor"} eq "or") { $no = 0; }
					} elsif ($FORM{"andor"} eq "and") {
						$no = 1;
					}
				}
			}
			
			if ($FORM{"search".$i} ne "email") {
				for(1..$max_colnum) {
					if ($FORM{"searchlike".$i} == 1) {
						# 完全一致
						if ($freecol->{"col".$_."name"} eq $column) {
							if ($row->{"col".$_} eq $word) {
								$yes = 1;
							if ($FORM{"andor"} eq "or") { $no = 0; }
							} elsif ($FORM{"andor"} eq "and") {
								$no = 1;
							}
						}
					} elsif ($FORM{"searchlike".$i} == 2) {
						# 含む検索
						if ($freecol->{"col".$_."name"} eq $column) {
							if ($row->{"col".$_} !~ /$word/) {
								$yes = 1;
							if ($FORM{"andor"} eq "or") { $no = 0; }
							} elsif ($FORM{"andor"} eq "and") {
								$no = 1;
							}
						}
					} else {
						# あいまい検索
						if ($freecol->{"col".$_."name"} eq $column) {
							if ($row->{"col".$_} =~ /$word/) {
								$yes = 1;
							if ($FORM{"andor"} eq "or") { $no = 0; }
							} elsif ($FORM{"andor"} eq "and") {
								$no = 1;
							}
						}
					}
				}
			}
			$search_exist = 1;
			}
		#}

		
		#main::error($yes.":".$no);
		# あいまい検索
		if ($FORM{"search_text_free"}) {
			my @col = @{$this->{MAIL_COL}};
			my @s = split(/ |　/, $FORM{"search_text_free"});
			foreach my $v (@s) {
				my $lyes = 0;
				$v = main::MakeRegularString($v);
				
				foreach my $n (@col) {
					# IDは飛ばす
					if ($n eq 'id') { next; }
						
					if ($row->{$n} =~ /$v/) {
						$lyes = 1;
					}
				}
				$search_exist = 1;
				if ($lyes) {
					$yes = 1;
					if ($FORM{"andor"} eq "or") { $no = 0; }
				}
				if (!$lyes && $FORM{"andor"} eq "and") {
					$no = 1;
				}
			}
		}
		
		#if ($FORM{search_exist} && !($yes && !$no)) { next; }
		
		if ($search_exist && !($yes && !$no)) { next; }
		
		#重複カウント
		if($ZYU{$row->{email}}){
			$zyunum++;
			#$row->{status} = "<font color=\"red\">× (重複)</font>";
		}else{
			#エラーカウント
			if(!main::CheckMailAddress($row->{email})){
				$errornum++;
				#$row->{status} = "<font color=\"red\">× (エラー)</font>";
			}else{
				#$row->{status} = "○ (正常)";
			}
		}
		$ZYU{$row->{email}}++;
		
		# 配信停止カウント
		if (!$row->{status}) {
			$$p_FORM{sendstopnum} ++;
		}
		
		
		push (@data,$row);
		$i++;
	}
	
	$$p_FORM{errornum} = $errornum;
	$$p_FORM{zyunum} = $zyunum;
	return @data;
}

# メールアドレス検索項目作成
# 引　数：
# 戻り値：配列
sub MakeSearchCol() {
	my $this = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	my %FORM = %$p_FORM;
	
	# 検索項目作成
	my (@search, $search_exist);
	
	# 自由項目取得
	my $freecol = $this->GetRowData('freecol', 'FREECOL');
	
	my $COL;
	foreach(1..5){
		my $row;
		$row->{search_id} = $_;
	
		my @cols;
		foreach(1..$max_colnum) {
			my $row2;
			my $d = "col".$_."name";
			if (!$freecol->{$d}) { next; }
			$row2->{col} = $_;
			$row2->{colname} = $freecol->{$d};
			$row2->{"search_col"} = $freecol->{"col".$FORM{"search".$row->{search_id}}."name"};
			$row2->{"search_text"} = $FORM{"search_text".$row->{search_id}};
			$row2->{num} = $_;
			if (($row2->{"search_col"} ne "" && $row2->{"search_text"} ne "") || ($FORM{"search".$row->{search_id}} eq "email" && $row2->{"search_text"} ne "" )) { $search_exist = 1; }

			if ($row2->{col} eq $FORM{"search".$row->{search_id}}) { $row2->{selected} = " selected "; }
			push(@{$COL->{'col'.$row->{search_id}}}, $row2);
		}
		
		# 含むかどうか
		$row->{searchlike} = $FORM{"searchlike".$row->{search_id}};
		
		if ($FORM{"search".$row->{search_id}} && $FORM{"search_text".$row->{search_id}}) { $search_exist = 1; }
		
		$row->{select} = \@{$COL->{'col'.$row->{search_id}}};
		$row->{search_text} = $FORM{"search_text".$_};
		
		# メールアドレス
		if ($FORM{"search".$row->{search_id}} eq "email") {
			$row->{search_col} = "メールアドレス";
		} else {
			$row->{"search_col"} = $freecol->{"col".$FORM{"search".$row->{search_id}}."name"};
		}
		
		push(@search,$row);
		my $sjis_searchtext = $FORM{"search_text".$_};
		$$p_FORM{search_url} .= "&search".$_."=".$FORM{"search".$_}."&search_text".$_."=".main::urlencode($sjis_searchtext);
	}
	$$p_FORM{search_exist} = $search_exist;
	return @search;
}


# 購読者必須項目チェック
# 引　数：フォーム エラーデータ
# 戻り値：
sub RegCheckExists () {
	my $this = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	my $error_data = shift;
	my %FORM = %$p_FORM;
	
	# 自由項目取得
	my @freecol = $this->GetFreeColLoopData($max_colnum);
	
	my @error;
	my $i = 1;
	foreach my $free (@freecol) {
		
		$FORM{"col".$i} =~ s/\r\n|\r|\n//g;
		if ($free->{"colcheck"}) {
			if ($FORM{"col".$i} eq "") {
				push(@error, $free->{"colname"}."は必須項目です。");
			}
		}
		$i++;
	}
	
	if ($#error >= 0) {
		$$error_data = join("<BR>", @error);
		return 0;
	}
	return 1;
	
}

# 購読者の重複チェック
# 引　数：
# 戻り値
sub RegCheckDouble() {
	my $this = shift;
	my $email = shift;
	my $judge_status = shift;
	
	# メールデータ取得
	my @DATA = $this->GetData('mail', 'MAIL');
	foreach my $row (@DATA) {
		if (lc $row->{email} eq lc $email) {
			if ($judge_status ne "") {
				if ($row->{status} eq $judge_status) {
					return 0;
				}
			} else {
				return 0;
			}
		}
	}
	return 1;
}

# 仮登録の重複チェック
# 引　数：
# 戻り値
sub TempCheckDouble() {
	my $this = shift;
	my $email = shift;
	my $judge_status = shift;
	
	# メールデータ取得
	my @DATA = $this->GetTempMailLoopData();
	foreach my $row (@DATA) {
		if ($row->{email} eq $email) {
			if ($judge_status ne "") {
				if ($row->{status} eq $judge_status) {
					return 0;
				}
			} else {
				return 0;
			}
		}
	}
	return 1;
}


# 仮アドレス登録
# 引　数：
# 戻り値：
sub AddTempData() {
	my $this = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	
	my %FORM = %$p_FORM;
	
	# 文字コード調査
	if ($FORM{force}) {
		# 強制
		for(1..$max_colnum) {
			&Jcode::convert(\$FORM{"col".$_}, "euc", $FORM{force});
		}
	} else {
		if ($FORM{encode}) {
			my $enc = getcode($FORM{encode});
			if ($enc ne "euc") {
				for(1..$max_colnum) {
					&Jcode::convert(\$FORM{"col".$_}, "euc", $enc);
				}
			}
		}
	}
	
	my $regcol;
	for(1..$max_colnum) {
		$regcol .= $FORM{"col".$_}."\t";
	}
	
	# 現在日付取得
	my %TIME = main::getdatetime();
	my $formdata = "$FORM{id}\t$TIME{year}$TIME{mon}$TIME{mday}\t$FORM{email}\t$regcol\n";

	#if (&depend_kisyu($formdata)) { &error("登録内容に機種依存文字を使用しないでください。"); }
	
	my $file = $this->{DATA_DIR}."mailbuf.cgi";
	
	# 追加データを上書き
	$this->InsertFile($file, $formdata);
	return 1;
}

# 仮変更データ登録
# 引　数：
# 戻り値：
sub AddTempChangeData() {
	my $this = shift;
	my $p_FORM = shift;
	my $max_colnum = shift;
	
	my %FORM = %$p_FORM;
	
	# 文字コード調査
	if ($FORM{force}) {
		# 強制
		for(1..$max_colnum) {
			&Jcode::convert(\$FORM{"col".$_}, "euc", $FORM{force});
		}
	} else {
		if ($FORM{encode}) {
			my $enc = getcode($FORM{encode});
			if ($enc ne "euc") {
				for(1..$max_colnum) {
					&Jcode::convert(\$FORM{"col".$_}, "euc", $enc);
				}
			}
		}
	}
	
	my $regcol;
	for(1..$max_colnum) {
		$regcol .= $FORM{"col".$_}."\t";
	}
	
	# 現在日付取得
	my %TIME = main::getdatetime();
	my $formdata = "$FORM{id}\t$TIME{year}$TIME{mon}$TIME{mday}\t$FORM{newemail}\t$FORM{oldemail}\t$regcol\n";

	my $file = $this->{DATA_DIR}."change.cgi";
	
	# 追加データを上書き
	$this->InsertFile($file, $formdata);
	return 1;
}

# メールアドレス登録（フォームより）
# 引　数：
# 戻り値：
sub RegEmail() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	my $id = time.$$;
	my $regdata;
	my $col = $this->{MAIL_COL};
	my @col = @$col;
	
	foreach my $n (@col) {
		if ($n eq "status") {
			# 配信フラグ
			$FORM{$n} = 1;
		} elsif ($n eq "id") {
			$FORM{$n} = $id;
		}
		$regdata .= $FORM{$n}."\t";
	}
	
	my $file = $this->{DATA_DIR}."mail.cgi";
	
	# 追加データ上書き
	$this->InsertFile($file, $regdata);
	
	return 1;
}

# メールアドレスの変更
# 引　数：
# 戻り値：
sub RegChangeEmail() {
	my $this = shift;
	my $oldemail = shift;
	my $newemail = shift;
	
	# メールデータ取得
	my @DATA = $this->GetData('mail', 'MAIL');
	my $regdata = "";
	my @col = @{$this->{MAIL_COL}};
	foreach my $ref (@DATA) {
		if ($ref->{email} eq $oldemail) {
			# 変更元データの場合
			$ref->{email} = $newemail;
			# 配信フラグも立てる
			$ref->{status} = 1;
		}
		foreach my $n (@col) {
			$regdata .= $ref->{$n}."\t";
		}
		$regdata .= "\n";
	}
	
	my $file = $this->{DATA_DIR}."mail.cgi";
	
	# 追加データ上書き
	$this->UpdateFile($file, $regdata);
	
	return 1;
}

# 変数置き換え
# 引　数：対象文字列　管理データ ユーザデータ
# 戻り値：文字列
sub ReplaceMailBody() {
	my $this = shift;
	my $str = shift;
	my $admindata = shift;
	my $userdata = shift;
	my $max_colnum = shift;
	
	$str =~ s/{ENQ_URL_(.*)?}/$admindata->{homeurl}enq_form.cgi\?key\=$1\&mail_id=$userdata->{id}/g;
	$str =~ s/{REGURL_DOPT}/$admindata->{homeurl}reg.cgi\?mode\=autoreg\&id=$userdata->{id}/g;
	$str =~ s/{AUTOFORMURL_DOPT}/$admindata->{homeurl}form.cgi\?id=$userdata->{id}/g;
	$str =~ s/{EMAIL}/$userdata->{email}/gi;
	$str =~ s/{NEWEMAIL}/$userdata->{newemail}/gi;
	$str =~ s/{OLDEMAIL}/$userdata->{oldemail}/gi;
	$str =~ s/{REGURL}/$admindata->{homeurl}reg.cgi\?reg\=add\&email\=$userdata->{email}/gi;
	$str =~ s/{CHANGEURL_DOPT}/$admindata->{homeurl}reg.cgi\?mode\=autoedit\&id\=$userdata->{id}/gi;
	$str =~ s/{DELURL}/$admindata->{homeurl}reg.cgi\?reg\=del\&email\=$userdata->{email}/gi;
	my %TIME = main::getdatetime();
	$str =~ s/{YEAR}/$TIME{year}/gi;
	$str =~ s/{MONTH-00}/$TIME{mon}/gi;
	$str =~ s/{DAY-00}/$TIME{mday}/gi;
	$str =~ s/{HOUR-00}/$TIME{hour}/gi;
	$str =~ s/{MINUTE-00}/$TIME{min}/gi;
	$str =~ s/{SECOND-00}/$TIME{sec}/gi;
	$str =~ s/{MONTH}/$TIME{monint}/gi;
	$str =~ s/{DAY}/$TIME{mdayint}/gi;
	$str =~ s/{HOUR}/$TIME{hourint}/gi;
	$str =~ s/{MINUTE}/$TIME{minint}/gi;
	$str =~ s/{SECOND}/$TIME{secint}/gi;
	$str =~ s/{WEEK}/$TIME{week}/gi;
	my $weekjp = $TIME{'week-jp'};
	$str =~ s/{WEEK\-JP}/$weekjp/gi;
	
	for(1..$max_colnum) {
		my $col = "COL".$_;
		my $col2 = "col".$_;
		$str =~ s/\{$col\}/$userdata->{$col2}/g;
	}
	
	return $str;
}

# 予約データのステータスを時間より一括更新
# 引　数：履歴ID　更新データ
# 戻り値：引当データ
sub UpdHistReserveStatusData() {
	my $this = shift;
	my $p_TIME = shift;
	my %TIME = %$p_TIME;
	my $file = $this->{DATA_DIR}."hist.cgi";
	my $date = "$TIME{year}$TIME{mon}$TIME{mday}$TIME{hour}$TIME{min}$TIME{sec}";
	my @DATA = $this->GetHistLoopData();
	
	my @return;
	my @col = @{$this->{HIST_COL}};
	my $regdata = "";
	foreach my $row (@DATA){
		if ($row->{start_send_date} < $date && $row->{status} == 3) {
			# 予約配信データの引き当て
			$row->{status} = 1;
			push(@return, $row);
		} else {
			
		}
		# 登録データ作成
		foreach my $n (@col) {
			$regdata .= $row->{$n}."\t";
		}
	
		$regdata .= "\n";
	}
	
	# データ上書き
	$this ->UpdateFile($file, $regdata);
	
	return @return;
}

# 仮登録データを削除
# 引　数：フォームデータ
# 戻り値：1 or 0
sub CleanDoubleOpt() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	# 削除日付がない場合は未来に設定
	if (!$FORM{del_y}) { $FORM{del_y} = "9999"; }
	if (!$FORM{del_m}) { $FORM{del_m} = "12"; }
	if (!$FORM{del_d}) { $FORM{del_d} = "31"; }
	
	# 対象日付作成
	my $deldate = sprintf("%04d%02d%02d", $FORM{del_y}, $FORM{del_m}, $FORM{del_d});
	
	my @DATA = $this->GetTempMailLoopData();
	my $regdata = "";
	my @col = @{$this->{TEMPMAIL_COL}};
	my $i = 0;
	foreach my $row (@DATA) {
		if ($deldate >= $row->{date}) {
			# 削除
			$i++;
		} else {
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
		}
		$regdata .= "\n";
	}
	
	my $file = $this->{DATA_DIR}."mailbuf.cgi";
	
	# 追加データ上書き
	$this->UpdateFile($file, $regdata);
	$$p_FORM{delnum} = $i;
	return 1;
}

# 再登録不可データ削除
# 引　数：フォームデータ
# 戻り値：1 or 0
sub CleanRegDeny() {
	my $this = shift;
	my $p_FORM = shift;
	
	my %FORM = %$p_FORM;
	
	# 削除日付がない場合は未来に設定
	if (!$FORM{del_y}) { $FORM{del_y} = "9999"; }
	if (!$FORM{del_m}) { $FORM{del_m} = "12"; }
	if (!$FORM{del_d}) { $FORM{del_d} = "31"; }
	
	# 対象日付作成
	my $deldate = sprintf("%04d%02d%02d", $FORM{del_y}, $FORM{del_m}, $FORM{del_d})."000000";
	
	my @DATA = $this->GetData('regdeny', 'REGDENY');
	my $regdata = "";
	my @col = @{$this->{REGDENY_COL}};
	my $i = 0;
	
	foreach my $row (@DATA) {
		if ($deldate >= $row->{'del_date'}) {
			# 削除
			$i++;
		} else {
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
		}
		$regdata .= "\n";
	}
	
	my $file = $this->{DATA_DIR}."regdeny.cgi";
	
	# 追加データ上書き
	$this->UpdateFile($file, $regdata);
	$$p_FORM{delnum} = $i;
	return 1;
}

# 再登録不可データ削除(Email版)
# 引　数：フォームデータ
# 戻り値：1 or 0
sub CleanRegDenyByEmail() {
	my $this = shift;
	my $email = shift;

	my @DATA = $this->GetData('regdeny', 'REGDENY');
	my $regdata = "";
	my @col = @{$this->{REGDENY_COL}};
	
	foreach my $row (@DATA) {
		
		if ($email eq $row->{'email'} && $email) {
			# メールアドレスで検索に来た場合
		} else {
			foreach my $n (@col) {
				$regdata .= $row->{$n}."\t";
			}
			$regdata .= "\n";
		}
		
	}
	
	my $file = $this->{DATA_DIR}."regdeny.cgi";
	
	# 追加データ上書き
	$this->UpdateFile($file, $regdata);
	return 1;
}

# 再登録できるかチェック
# 引　数：メールアドレス
# 戻り値：1 or 0
sub checkRegDeny() {
	my $this = shift;
	my $email = shift;
	my $objMail = shift;
	my $max_column = shift;
	my @deny = $this->GetData('regdeny', 'REGDENY');
	my %TIME = main::getdatetime();
	my $now = $TIME{'year'}.$TIME{'mon'}.$TIME{'mday'}.$TIME{'hour'}.$TIME{'min'}.$TIME{'sec'};
	
	my $error_flg = 0;
#		print "Content-type: text/html; charset=EUC-JP\n\n";
	foreach my $row(@deny) {
		
		if ($row->{'email'} eq $email && $now < $row->{'limit_date'} && $row->{'limit_date'}) {
#			print $email.":".$row->{'email'}.":".$now.":".$row->{'limit_date'};
			# 期限日が設定されている場合
			$error_flg = 1;
			last;
		} elsif (!$row->{'limit_date'} && $row->{'email'} eq $email) {
#			print $email.":".$row->{'email'}.":".$now.":".$row->{'limit_date'};
			# 期限日が設定されていない場合
			$error_flg = 1;
			last;
		}
	}

	if (!$error_flg) { return 1; }
	if ($objMail) {
		# 自動返信メールテンプレート情報取得
		my $rowform = $this->GetRowData('form', 'FORM');
		my $admindata = $this->GetAdminData();
		my $body = $rowform->{form_regdeny_mailbody};
		my $userdata;
		$userdata->{email} = $email;
		
		# 置換作業
		$body = $this->ReplaceMailBody($body, $admindata, $userdata, $max_column);
		$body =~ s/__<<BR>>__/\n/g;
		
		if ($rowform->{type} eq "html") {
			$body =~ s/\n/<br>/gi;
		}
		my $sendername = main::SetFromName($admindata->{admin_email}, $admindata->{admin_name});
		$objMail->send($admindata->{sendmail_path},$email,$rowform->{form_regdeny_mailtitle},$body,$sendername,$admindata->{admin_email},"",$admindata->{admin_email}, $rowform->{send_type});
		exit;
	} else {
		main::error("そのアドレスは一度登録されたため再登録することはできません。");
	}
}

# 送信前用の送信データを保持
# 引　数：セッションID 送信データ
# 戻り値：1 or 0
sub setSenderData() {
	my $this = shift;
	my $sid = shift;
	my $senderdata = shift;
	
	my $file = $this->{DATA_DIR}.".".$sid."sender.cgi";
	# 追加データを上書き
	$this->UpdateFileForce($file, $senderdata);
	return 1;
}

# 送信前用の送信データを取得
# 引　数：セッションID
# 戻り値：文字列
sub getSenderData() {
	my $this = shift;
	my $sid = shift;
	my $file = $this->{DATA_DIR}.".".$sid."sender.cgi";
	my $data = $this->ReadFile($file);
	return $data;
}

# 組み込みモジュールを更新
sub UpdModule() {
	my $this = shift;
	my $p_FORM = shift;
	my %FORM = %$p_FORM;
	
	foreach my $n (qw(autoreg reserve errmail)) {
		# autoreg.pl書き込み
		if (-e "./lib/$n.pl") {
			my $regdata;
			open(IN, "+< ./lib/$n.pl") || main::error("$n.plのオープンに失敗しました。");
			flock(IN, 2);
			my @LINES_ORG = <IN>;
			foreach(@LINES_ORG){
				$_ =~ s/\r\n//g;
				$_ =~ s/\r//g;
				$_ =~ s/\n//g;
				if($_ && $_ =~ /^my \$myfilepath \= \'.*\'\;/){
					$regdata .= 'my $myfilepath = '."'$FORM{mypath}';\n";
				} else {
					$regdata .= $_."\n";
				}
			}
			truncate(IN, 0);
			seek(IN, 0, 0);
			print(IN $regdata);
			close(IN);
		}
	}

	
	if (-e "./data/enc.cgi") {
		my $regdata;
		open(IN, "+< ./data/enc.cgi") || main::error("enc.cgiのオープンに失敗しました。");
		flock(IN, 2);
		$regdata = "$FORM{license1}\n$FORM{license2}\n$FORM{license3}\n$FORM{license4}";
		truncate(IN, 0);
		seek(IN, 0, 0);
		print(IN $regdata);
		close(IN);
	}
}

1;
