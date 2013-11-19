<!DOCTYPE html>
<html>
	<head>
		<title>渋家 || SHIBUHOUSE</title>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
		<link href='./css/reset.css' rel='stylesheet' type='text/css'>
		<link href='./css/global.css' rel='stylesheet' type='text/css'>
		<!-- スライドショー -->
		<link href='./css/flexslider.css' rel='stylesheet' type='text/css'>
		<script type="text/javascript" src="js/modernizr.js"></script>
	</head>
	<body>
		<div id="wrap">
				<div id="logo">
					<table>
						<tr>
							<img src="img/logo.png"></br>
						</tr>
						<tr>
							<p id="text_logo">シブハウスオフィシャルホームページ</p>
						</tr>
					</table>	
				</div><!-- #logo -->
					<div id="contact">
						<table>
							<tr>
								<td><img src="./img/tell.png"></td>
								<td><img src="./img/twitter_header.png"></td>
								<td><img src="./img/like_facebook.png"></td>
							</tr>
							<tr>
								<td colspan="3"><img src="./img/mail.png"></td>
							</tr>
						</table>
					</div>
			<div id="header">
				<div id="nav">
					<table id="nav_table">
						<tr align="center" style="margin:0 25px 0 25px">
							<td class="nav_image" style="padding:0 50px;"><img src="./img/about.png"></td>
							<td class="nav_image" style="padding:0 50px;"><img src="./img/bio.png"></td>
							<td class="nav_image" style="padding:0 50px;"><img src="./img/life.png"></td>
							<td class="nav_image" style="padding:0 50px;"><img src="./img/member.png"></td>
						</tr>
						<tr>
							<td style="padding:0 45px;">アバウト＞</td>
							<td style="padding:0 21px;">バイオグラフィー＞</td>
							<td style="padding:0 50px;">ライフ＞</td>
							<td style="padding:0 45px;">メンバー＞</td>
						</tr>
					</table>
				</div><!-- #nav -->
			</div><!-- #header -->
			<div id="slide">
				<div class="flexslider">
					<ul class="slides">
						<li>
							<img src="img/aeri/06.JPG"/>
						</li>
						<li>
							<img src="img/aeri/03.JPG"/>
						</li>
					</ul>
				</div>
			</div><!-- #slide -->
			<div id="text_information">
				渋家新メンバー！　池田愛恵里さんです -> Official Web <a href="http://ameblo.jp/ikeda-aeri/">池田愛恵里オフィシャルブログ「ようこそ池田農園へ。」 powered by Ameba</a>
			</div>
			<div id="hot_topics">
				<div id="hot_topics_pic">
					<img src="./img/search.png"><img id="hot_topics_midashi" src="./img/hot_topics.png">
				</div><!-- hot_topics_pic -->
				<div id="hot_topics_text">
					<ul>
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
					</ul>
				</div><!-- hot_topics_text -->
			</div><!-- #hot_topics -->
			<div id="content">
				<div id="what" class="midashi">
				</div><!-- #what -->
				<div id="bio" class="midashi">
				</div><!-- #bio -->
				<div id="member" class="midashi">
				</div><!-- member -->
				<div id="information" class="midashi">
				</div><!-- #information -->
			</div><!-- #content -->
		</div><!-- #wrap -->
		<footer>
		</footer>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
		<script defer src="js/jquery.flexslider.js"></script>
		<script type="text/javascript">
		$(window).load(function() {
			$('.flexslider').flexslider({
				animation: "slide"
			});
		});
		</script>
	</body>
</html>