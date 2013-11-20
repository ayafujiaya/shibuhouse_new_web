<!DOCTYPE html>
<html>
	<head>
		<title>渋家 || SHIBUHOUSE</title>
		<!-- typesqure 用タグ -->
		<script type="text/javascript" src="//typesquare.com/accessor/script/typesquare.js?E2mGUC7TkZ8%3D" charset="utf-8"></script>
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
			<?php require './content.php' ?>
		</div><!-- #wrap -->
		<?php require './footer.php' ?>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
		<script defer src="js/jquery.flexslider.js"></script>
		<script type="text/javascript" src="js/scroll_top.js"></script>
		<script type="text/javascript">
		$(window).load(function() {
			$('.flexslider').flexslider({
				animation: "slide"
			});
		});
		</script>
	</body>
</html>