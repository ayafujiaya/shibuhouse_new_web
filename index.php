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
			<?php require './header.php' ?>
			<div id="slide">
				<div class="flexslider">
					<ul class="slides">
						<li>
							<img src="http://www.denden-town.or.jp/audition2013/aeri/aeri603-1.JPG"/>
						</li>
						<li>
							<img src="http://www.denden-town.or.jp/audition2013/aeri/aeri527-1.JPG"/>
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
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
						<li class="topics"><sep class="topics_date">2013/10/11</sep><img class="arrow" src="./img/arrow.png"><sep class="topics_date">アイコンを作ってみました＝〜〜〜〜〜！！！</sep></li>
					</ul>
				</div><!-- hot_topics_text -->
			</div><!-- #hot_topics -->
			<div id="content">
				<div id="what" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img  style="margin-bottom:47px" src="./img/whats_shibuhouse.png">
					<div class="midashi_text">
						集団的知性（しゅうだんてきちせい、英語：Collective Intelligence、CI）は、多くの個人の協力と競争の中から、その集団自体に知能、精神が存在するかのように見える知性である。Peter Russell（1983年）、Tom Atlee（1993年）、Howard Bloom（1995年）、Francis Heylighen（1995年）、ダグラス・エンゲルバート、Cliff Joslyn、Ron Dembo、Gottfried Mayer-Kress（2003年）らが理論を構築した。
					</div>
					<img style="margin:0 auto; display: block;" src="./img/hatena_midashi.png">
					<img style="margin:0 auto; display: block;" src="./img/about_midahsi.png">
					</div><!-- .inner_midashi -->
				</div><!-- #what -->

				<div id="bio" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img src="./img/bio_midashi.png">
					</div>
					<div class="midashi_text">
					</div>
				</div><!-- #bio -->
				<div id="member" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img src="./img/member_midashi.png">
					</div>
				</div><!-- member -->
				<div id="information" class="midashi">
					<div style="padding-top:28px; padding-bottom:26px;" class="inner_midashi">
						<img src="./img/information.png">
					</div>
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