
<!-- ここから -->
<?php 
#ポップアップ後の画像の位置
$full_image = './img/exhibition_full/usn/usn_002.jpg';
#ポップアップ前の画像の位置
$sum_image = './img/exhibition_sum/usn/usn_001.jpg';
#ポップアップ後のコメントの内容(空でも良い)
$comment = 'ultra super new!!';
?>

<div id="ex_image">
  <a name="<?php echo $comment ?>" rel="lightbox[imagegroup]" data-lightbox="roadtrip" href="<?php echo $full_image ?>">
    <img class="inner_ex_image" src="<?php echo $sum_image ?>">
  </a>
</div>
<!-- ここまでをテンプレートとして使う -->

<div id="ex_text">
「THE NEW BLACK」<br />
日程：2013.7.11 - 7.26<br />
会場：Ultra Super New<br />
<br />
流行発信地•原宿に創設された「Ultra Super New Gallery」は、キュレーターとのコラボレーションによって国内外からセレクトされたアーティスト作品を紹介する。展示されたすべての作品は購入可能。広さ100 平米のこのスペースは、原宿明治通り沿いのUltra Super Newオフィスの地上階に位置している。オープニング展示として、スコットランドの芸術家ジャック&middot;マクリーンと共に、渋家はメンバー3名の作品を出展した。
</div>
